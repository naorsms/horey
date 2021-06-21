import json
import pdb
import time

import paramiko
from sshtunnel import open_tunnel
import os
from horey.deployer.machine_deployment_block import MachineDeploymentBlock
from horey.deployer.machine_deployment_step import MachineDeploymentStep
from typing import List
from contextlib import contextmanager
from io import StringIO

from horey.h_logger import get_logger

logger = get_logger()


class HoreySFTPClient(paramiko.SFTPClient):
    """
    Stolen from here:
    https://stackoverflow.com/questions/4409502/directory-transfers-with-paramiko

    """
    def put_dir(self, source, target):
        """
        Uploads the contents of the source directory to the target path. The
        target directory needs to exists. All subdirectories in source are
        created under target.
        """
        for item in os.listdir(source):
            if os.path.isfile(os.path.join(source, item)):
                self.put(os.path.join(source, item), os.path.join(target, item), confirm=True)
            else:
                self.mkdir(os.path.join(target, item), ignore_existing=True)
                self.put_dir(os.path.join(source, item), os.path.join(target, item))

    def mkdir(self, path, mode=511, ignore_existing=False):
        """
        Augments mkdir by adding an option to not fail if the folder exists
        """

        try:
            super(HoreySFTPClient, self).mkdir(path, mode)
        except IOError:
            if ignore_existing:
                pass
            else:
                raise


class RemoteDeployer:
    def __init__(self, configuration=None):
        self.configuration = configuration

    def deploy_blocks(self, blocks_to_deploy: List[MachineDeploymentBlock]):
        self.provision_remote_deployer_infrastructure(blocks_to_deploy)

        self.begin_provisioning_deployment_code(blocks_to_deploy)

        self.wait_for_deployment_code_provisioning_to_end(blocks_to_deploy)

        self.begin_deployment(blocks_to_deploy)

        self.wait_for_deployment_to_end(blocks_to_deploy)

    def provision_remote_deployer_infrastructure(self, deployment_targets):
        """
        """
        for deployment_target in deployment_targets:
            self.perform_recursive_replacements(deployment_target.replacements_base_dir_path, deployment_target.string_replacements)
            with self.get_deployment_target_client(deployment_target) as client:
                target_remote_scripts_dir_path = os.path.join(deployment_target.remote_deployment_dir_path, deployment_target.remote_scripts_dir_name)
                command = f"rm -rf {target_remote_scripts_dir_path}"
                logger.info(f"[REMOTE] {command}")
                client.exec_command(command)

                transport = client.get_transport()
                sftp_client = HoreySFTPClient.from_transport(transport)

                logger.info(f"sftp: mkdir {target_remote_scripts_dir_path}")
                sftp_client.mkdir(target_remote_scripts_dir_path, ignore_existing=True)

                logger.info(f"sftp: put_dir {target_remote_scripts_dir_path}")
                sftp_client.put_dir(os.path.join(deployment_target.local_deployment_dir_path, deployment_target.remote_scripts_dir_name),
                                    target_remote_scripts_dir_path)

                logger.info(f"sftp: Uploading '{os.path.join(target_remote_scripts_dir_path, 'remote_step_executor.sh')}'")
                sftp_client.put(os.path.join(os.path.dirname(os.path.abspath(__file__)), "data", "remote_step_executor.sh"),
                                    os.path.join(target_remote_scripts_dir_path, "remote_step_executor.sh"))

                command = f"sudo chmod +x {os.path.join(target_remote_scripts_dir_path, 'remote_step_executor.sh')}"
                logger.info(f"[REMOTE] {command}")
                client.exec_command(command)

    def perform_recursive_replacements(self, replacements_base_dir_path, string_replacements):
        for root, _, filenames in os.walk(replacements_base_dir_path):
            for filename in filenames:
                if filename.startswith("template_"):
                    self.perform_file_string_replacements(root, filename, string_replacements)

    def perform_file_string_replacements(self, root, filename, string_replacements):
        logger.info(f"Performing replacements on template dir: '{root}' name: '{filename}'")
        with open(os.path.join(root, filename)) as file_handler:
            str_file = file_handler.read()

        for key in sorted(string_replacements.keys(), key=lambda key_string: len(key_string), reverse=True):
            if not key.startswith("STRING_REPLACEMENT_"):
                raise ValueError("Key must start with STRING_REPLACEMENT_")
            logger.info(f"Performing replacement in template: {filename}, key: {key}")
            value = string_replacements[key]
            str_file = str_file.replace(key, value)

        new_filename = filename[len("template_"):]

        with open(os.path.join(root, new_filename), "w+") as file_handler:
            file_handler.write(str_file)

        if "STRING_REPLACEMENT_" in str_file:
            raise ValueError(f"Not all STRING_REPLACEMENT_ were replaced in {os.path.join(root, new_filename)}")

    def begin_provisioning_deployment_code(self, deployment_targets: List[MachineDeploymentBlock]):
        for deployment_target in deployment_targets:
            self.perform_recursive_replacements(deployment_target.replacements_base_dir_path, deployment_target.string_replacements)
            with self.get_deployment_target_client(deployment_target) as client:
                transport = client.get_transport()
                sftp_client = HoreySFTPClient.from_transport(transport)
                self.execute_step(client, deployment_target.application_infrastructure_provision_step)
                self.wait_for_step_to_finish(deployment_target.application_infrastructure_provision_step, deployment_target.local_deployment_data_dir_path, sftp_client)

            deployment_target.deployment_code_provisioning_ended = True

    def wait_for_step_to_finish(self, step, local_deployment_data_dir_path, sftp_client):
        retry_attempts = 10
        sleep_time = 60
        for retry_counter in range(retry_attempts):
            try:
                sftp_client.get(step.configuration.finish_status_file_path,
                        os.path.join(local_deployment_data_dir_path, step.configuration.finish_status_file_name))

                sftp_client.get(step.configuration.output_file_path,
                                os.path.join(local_deployment_data_dir_path, step.configuration.output_file_name))
                break
            except IOError as error_received:
                if "No such file" not in repr(error_received):
                    raise
                logger.info(f"Retrying to fetch remote script's status in {sleep_time} seconds ({retry_counter}/{retry_attempts})")
            time.sleep(sleep_time)
        else:
            raise TimeoutError("Failed to fetch remote script's status")

        step.update_finish_status(local_deployment_data_dir_path)
        step.update_output(local_deployment_data_dir_path)

        if step.status_code != step.StatusCode.SUCCESS:
            last_lines = '\n'.join(step.output.split("\n")[-50:])
            raise RuntimeError(f"Step finished with status: {step.status}, error: \n{last_lines}")

        logger.info(f"Step finished successfully output in: '{step.configuration.output_file_name}'")

    def wait_for_deployment_code_provisioning_to_end(self, blocks_to_deploy: List[MachineDeploymentBlock]):
        for block_to_deploy in blocks_to_deploy:
            for i in range(60):
                if block_to_deploy.deployment_code_provisioning_ended:
                    break
                time.sleep(1)
            else:
                raise RuntimeError("Deployment failed at wait_for_deployment_code_provisioning_to_end")
        logger.info("Deployment provisioning finished successfully")

    def begin_deployment(self, deployment_targets: List[MachineDeploymentBlock]):
        for deployment_target in deployment_targets:
            with self.get_deployment_target_client(deployment_target) as client:
                transport = client.get_transport()
                sftp_client = HoreySFTPClient.from_transport(transport)

                self.execute_step(client, deployment_target.application_deploy_step)
                self.wait_for_step_to_finish(deployment_target.application_deploy_step, deployment_target.local_deployment_data_dir_path, sftp_client)

            deployment_target.deployment_code_provisioning_ended = True

    @staticmethod
    @contextmanager
    def get_deployment_target_client(block_to_deploy: MachineDeploymentBlock):
        with open(block_to_deploy.bastion_ssh_key_path, 'r') as bastion_key_file_handler:
            bastion_key = paramiko.RSAKey.from_private_key(StringIO(bastion_key_file_handler.read()))
        with open(block_to_deploy.deployment_target_ssh_key_path, 'r') as bastion_key_file_handler:
            deployment_target_key = paramiko.RSAKey.from_private_key(StringIO(bastion_key_file_handler.read()))

        with open_tunnel(
                ssh_address_or_host=(block_to_deploy.bastion_address, 22),
                remote_bind_address=(block_to_deploy.deployment_target_address, 22),
                ssh_username=block_to_deploy.bastion_user_name,
                ssh_pkey=bastion_key) as tunnel:
            logger.info(f"Opened SSH tunnel to {block_to_deploy.deployment_target_address} via {block_to_deploy.bastion_address} ")

            with paramiko.SSHClient() as client:
                client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                client.connect(
                    'localhost',
                    port=tunnel.local_bind_port,
                    username=block_to_deploy.deployment_target_user_name,
                    pkey=deployment_target_key,
                    compress=True)

                yield client

    def execute_step(self, client: paramiko.SSHClient, step):
        command = f"screen -S deployer -dm {step.configuration.step_scripts_dir_path}/remote_step_executor.sh {step.configuration.remote_script_file_path} {step.configuration.script_configuration_file_path} {step.configuration.finish_status_file_path} {step.configuration.output_file_path}"
        logger.info(f"[REMOTE] {command}")

        client.exec_command(command)

    def get_status_path_from_script_path(self, script_path):
        pdb.set_trace()

    def get_output_path_from_script_path(self, script_path):
        pdb.set_trace()

    def wait_for_deployment_to_end(self, blocks_to_deploy):
        lst_errors = []
        for block in blocks_to_deploy:
            if block.application_deploy_step.status_code != MachineDeploymentStep.StatusCode.SUCCESS:
                lst_errors.append(block.application_infrastructure_provision_step.configuration.output_file_path)

        if lst_errors:
            raise RuntimeError(str(lst_errors))
        logger.info("Deployment finished successfully output in")

