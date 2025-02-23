"""
AWS lambda client to handle lambda service API requests.
"""
import pdb

import time

from horey.aws_api.aws_clients.boto3_client import Boto3Client

from horey.aws_api.base_entities.aws_account import AWSAccount
from horey.aws_api.base_entities.region import Region
from horey.aws_api.aws_services_entities.ecs_cluster import ECSCluster
from horey.aws_api.aws_services_entities.ecs_service import ECSService
from horey.aws_api.aws_services_entities.ecs_task import ECSTask
from horey.aws_api.aws_services_entities.ecs_capacity_provider import ECSCapacityProvider
from horey.aws_api.aws_services_entities.ecs_task_definition import ECSTaskDefinition
from horey.aws_api.aws_services_entities.ecs_container_instance import ECSContainerInstance

from horey.h_logger import get_logger

logger = get_logger()


class ECSClient(Boto3Client):
    """
    Client to handle specific aws service API calls.
    """

    def __init__(self):
        client_name = "ecs"
        super().__init__(client_name)

    def run_task(self, request_dict):
        for response in self.execute(self.client.run_task, "tasks", filters_req=request_dict):
            return response

    def get_all_clusters(self, region=None):
        """
        Get all clusters in all regions.
        :return:
        """

        if region is not None:
            return self.get_region_clusters(region)
        final_result = list()
        for region in AWSAccount.get_aws_account().regions.values():
            final_result += self.get_region_clusters(region)

        return final_result

    def get_all_capacity_providers(self, region=None):
        """
        Get all capacity_providers in all regions.
        :return:
        """

        if region is not None:
            return self.get_region_capacity_providers(region)

        final_result = list()
        for region in AWSAccount.get_aws_account().regions.values():
            final_result += self.get_region_capacity_providers(region)

        return final_result

    def get_region_capacity_providers(self, region):
        final_result = list()
        AWSAccount.set_aws_region(region)
        for dict_src in self.execute(self.client.describe_capacity_providers, "capacityProviders"):
            obj = ECSCapacityProvider(dict_src)
            final_result.append(obj)

        return final_result

    def get_region_clusters(self, region, cluster_identifiers=None):
        AWSAccount.set_aws_region(region)

        final_result = list()
        if cluster_identifiers is None:
            cluster_identifiers = []
            for cluster_arn in self.execute(self.client.list_clusters, "clusterArns"):
                cluster_identifiers.append(cluster_arn)

        if len(cluster_identifiers) > 100:
            raise NotImplementedError("""clusters (list) -- A list of up to 100 cluster names or full cluster 
            Amazon Resource Name (ARN) entries. If you do not specify a cluster, the default cluster is assumed.""")

        filter_req = {"clusters": cluster_identifiers,
                      "include": ["ATTACHMENTS", "CONFIGURATIONS", "SETTINGS", "STATISTICS", "TAGS"]}

        for dict_src in self.execute(self.client.describe_clusters, "clusters", filters_req=filter_req):
            obj = ECSCluster(dict_src)
            final_result.append(obj)

        return final_result

    def provision_capacity_provider(self, capacity_provider):
        """
        self.client.delete_capacity_provider(capacityProvider='test-capacity-provider')
        """
        region_objects = self.get_region_capacity_providers(capacity_provider.region)
        for region_object in region_objects:
            if region_object.name == capacity_provider.name:
                capacity_provider.update_from_raw_response(region_object.dict_src)
                return

        AWSAccount.set_aws_region(capacity_provider.region)
        response = self.provision_capacity_provider_raw(capacity_provider.generate_create_request())
        capacity_provider.update_from_raw_response(response)

    def provision_capacity_provider_raw(self, request_dict):
        logger.info(f"Creating ECS Capacity Provider: {request_dict}")
        for response in self.execute(self.client.create_capacity_provider, "capacityProvider",
                                     filters_req=request_dict):
            return response

    def provision_cluster(self, cluster: ECSCluster):
        """
        self.client.delete_cluster(capacityProvider='test-capacity-provider')
        """
        region_objects = self.get_region_clusters(cluster.region, cluster_identifiers=[cluster.name])
        if len(region_objects) == 1:
            region_cluster = region_objects[0]
            if region_cluster.get_status() == region_cluster.Status.ACTIVE:
                cluster.update_from_raw_response(region_cluster.dict_src)
                return

        if len(region_objects) == 0 or region_cluster.get_status() == region_cluster.Status.INACTIVE:
            AWSAccount.set_aws_region(cluster.region)
            response = self.provision_cluster_raw(cluster.generate_create_request())
            cluster.update_from_raw_response(response)

        timeout = 300
        sleep_time = 5
        for i in range(timeout // sleep_time):
            region_objects = self.get_region_clusters(cluster.region, cluster_identifiers=[cluster.name])
            region_cluster = region_objects[0]

            if region_cluster.get_status() == region_cluster.Status.FAILED:
                raise RuntimeError(f"cluster {region_cluster.name} provisioning failed. Cluster in FAILED status")

            if region_cluster.get_status() != region_cluster.Status.ACTIVE:
                time.sleep(sleep_time)
                continue

            cluster.update_from_raw_response(region_cluster.dict_src)
            return
        raise TimeoutError(f"Cluster did not become available for {timeout} seconds")

    def provision_cluster_raw(self, request_dict):
        logger.info(f"Creating ECS Capacity Provider: {request_dict}")
        for response in self.execute(self.client.create_cluster, "cluster", filters_req=request_dict):
            return response

    def get_all_services(self, cluster):
        filters_req = {"cluster": cluster.name}
        AWSAccount.set_aws_region(cluster.region)

        final_result = []
        service_arns = []

        for dict_src in self.execute(self.client.list_services, "serviceArns", filters_req=filters_req):
            service_arns.append(dict_src)

        if len(service_arns) == 0:
            return []

        if len(service_arns) > 10:
            raise NotImplementedError()
        filters_req["services"] = service_arns
        for dict_src in self.execute(self.client.describe_services, "services", filters_req=filters_req):
            final_result.append(ECSService(dict_src))

        return final_result

    def get_all_tasks(self, cluster):
        filters_req = {"cluster": cluster.name}
        AWSAccount.set_aws_region(cluster.region)

        final_result = []
        task_arns = []

        for arn in self.execute(self.client.list_tasks, "taskArns", filters_req=filters_req):
            task_arns.append(arn)

        if len(task_arns) == 0:
            return []

        if len(task_arns) > 100:
            raise NotImplementedError()

        filters_req["tasks"] = task_arns
        filters_req["include"] = ["TAGS"]

        for dict_src in self.execute(self.client.describe_tasks, "tasks", filters_req=filters_req):
            final_result.append(ECSTask(dict_src))

        return final_result

    def get_all_task_definitions(self, region=None):
        if region is not None:
            return self.get_region_task_definitions(region)

        final_result = list()
        for region in AWSAccount.get_aws_account().regions.values():
            final_result += self.get_region_task_definitions(region)

        return final_result

    def get_region_task_definitions(self, region, family_prefix=None):
        list_arns = list()
        AWSAccount.set_aws_region(region)
        filters_req = dict()
        if family_prefix is not None:
            filters_req["familyPrefix"] = family_prefix

        for dict_src in self.execute(self.client.list_task_definitions, "taskDefinitionArns", filters_req=filters_req):
            list_arns.append(dict_src)

        if len(list_arns) == 0:
            return []

        final_result = list()
        for arn in list_arns:
            filters_req = {"taskDefinition": arn, "include": ['TAGS']}
            for dict_src in self.execute(self.client.describe_task_definition, "taskDefinition",
                                         filters_req=filters_req):
                final_result.append(ECSTaskDefinition(dict_src))

        return final_result

    def provision_ecs_task_definition(self, task_definition):
        AWSAccount.set_aws_region(task_definition.region)
        response = self.provision_ecs_task_definition_raw(task_definition.generate_create_request())
        task_definition.update_from_raw_response(response)

    def provision_ecs_task_definition_raw(self, request_dict):
        logger.info(f"Creating ECS task definition: {request_dict}")
        for response in self.execute(self.client.register_task_definition, "taskDefinition", filters_req=request_dict):
            return response

    @staticmethod
    def get_cluster_from_arn(cluster_arn):
        cluster = ECSCluster({})
        cluster.name = cluster_arn.split(":")[-1].split("/")[-1]
        cluster.arn = cluster_arn
        cluster.region = Region.get_region(cluster_arn.split(":")[3])
        return cluster

    def provision_service(self, service):
        cluster = self.get_cluster_from_arn(service.cluster_arn)
        region_objects = self.get_all_services(cluster)
        for region_object in region_objects:
            if region_object.name == service.name:
                AWSAccount.set_aws_region(service.region)
                response = self.update_service_raw(service.generate_update_request())
                service.update_from_raw_response(response)
                return

        AWSAccount.set_aws_region(service.region)
        response = self.create_service_raw(service.generate_create_request())
        service.update_from_raw_response(response)

    def create_service_raw(self, request_dict):
        logger.info(f"Creating ECS Service: {request_dict}")
        for response in self.execute(self.client.create_service, "service", filters_req=request_dict):
            return response

    def update_service_raw(self, request_dict):
        logger.info(f"Updating ECS Service: {request_dict}")
        for response in self.execute(self.client.update_service, "service", filters_req=request_dict):
            return response

    def dispose_service(self, cluster, service: ECSService):
        AWSAccount.set_aws_region(service.region)
        self.dispose_service_raw(service.generate_dispose_request(cluster))

    def dispose_service_raw(self, request_dict):
        logger.info(f"Disposing ECS Service: {request_dict}")
        for response in self.execute(self.client.delete_service, "service", filters_req=request_dict):
            return response

    def get_region_container_instances(self, region, cluster_identifier=None):
        AWSAccount.set_aws_region(region)

        if cluster_identifier is None:
            cluster_identifiers = []
            for cluster_arn in self.execute(self.client.list_clusters, "clusterArns"):
                cluster_identifiers.append(cluster_arn)
        else:
            cluster_identifiers = [cluster_identifier]

        final_result = list()

        for cluster_identifier in cluster_identifiers:
            cluster_container_instances_arns = []
            filter_req = {"cluster": cluster_identifier,
                          "maxResults": 100}

            for container_instance_arn in self.execute(self.client.list_container_instances, "containerInstanceArns",
                                                       filters_req=filter_req):
                cluster_container_instances_arns.append(container_instance_arn)

            if len(cluster_container_instances_arns) == 0:
                continue

            filter_req = {"cluster": cluster_identifier,
                          "containerInstances": cluster_container_instances_arns,
                          "include": ["TAGS"]
                          }

            for dict_src in self.execute(self.client.describe_container_instances, "containerInstances",
                                         filters_req=filter_req):
                obj = ECSContainerInstance(dict_src)
                final_result.append(obj)

        return final_result

    def dispose_cluster(self, cluster: ECSCluster):
        """
        response = client.deregister_container_instance(
         cluster='string',
        containerInstance='string',
        force=True|False
        )
        @param cluster:
        @return:
        """
        cluster_container_instances = self.get_region_container_instances(cluster.region,
                                                                          cluster_identifier=cluster.name)
        self.dispose_container_instances(cluster_container_instances, cluster)
        AWSAccount.set_aws_region(cluster.region)
        self.dispose_cluster_raw(cluster.generate_dispose_request(cluster))

    def dispose_cluster_raw(self, request_dict):
        logger.info(f"Disposing ECS Cluster: {request_dict}")
        for response in self.execute(self.client.delete_cluster, "cluster", filters_req=request_dict):
            return response

    def dispose_container_instances(self, container_instances, cluster):
        for container_instance in container_instances:
            self.dispose_container_instance_raw(container_instance.generate_dispose_request(cluster))

    def dispose_container_instance_raw(self, request_dict):
        logger.info(f"Disposing ECS container instance: {request_dict}")
        for response in self.execute(self.client.deregister_container_instance, "containerInstance",
                                     filters_req=request_dict):
            return response

    def dispose_tasks(self, tasks, cluster_name):
        for task in tasks:
            for response in self.execute(self.client.stop_task, "task", filters_req={"cluster": cluster_name, "task": task.arn}):
                logger.info(response)

    def attach_capacity_providers_to_ecs_cluster(self, ecs_cluster, capacity_provider_names,
                                                 default_capacity_provider_strategy):
        request_dict = {"cluster": ecs_cluster.name,
                        "capacityProviders": capacity_provider_names,
                        "defaultCapacityProviderStrategy": default_capacity_provider_strategy
                        }
        self.attach_capacity_providers_to_ecs_cluster_raw(request_dict)

    def attach_capacity_providers_to_ecs_cluster_raw(self, request_dict):
        logger.info(f"Attaching capacity provider to ecs cluster: {request_dict}")
        for response in self.execute(self.client.put_cluster_capacity_providers, "cluster",
                                     filters_req=request_dict):
            return response
