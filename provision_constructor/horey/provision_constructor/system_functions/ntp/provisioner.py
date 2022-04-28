import os.path
import pdb

from horey.provision_constructor.system_function_factory import SystemFunctionFactory


@SystemFunctionFactory.register
class Provisioner(SystemFunctionFactory.SystemFunction):
    def __init__(self, root_deployment_dir, provisioner_script_name, force=False):
        super().__init__(root_deployment_dir, provisioner_script_name, force=force)

    def _test_provisioned(self):
        pdb.set_trace()
        os.path.join(os.path.dirname(os.path.abspath(__file__)), "timesyncd.conf")

    def _provision(self):
        pdb.set_trace()
