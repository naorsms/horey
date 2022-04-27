import pdb

from horey.provision_constructor.system_function_factory import SystemFunctionFactory


@SystemFunctionFactory.register
class Builder(SystemFunctionFactory.SystemFunction):
    def __init__(self, root_deployment_dir, provisioner_script_name, force=False):
        super().__init__(root_deployment_dir, provisioner_script_name, force=force)
        pdb.set_trace()
        

