"""
sudo mount -t nfs4 -o  nfsvers=4.1,rsize=1048576,wsize=1048576,hard,timeo=600,retrans=2,noresvport  172.31.14.49:/ /home/ubuntu/efs
"""
import pdb

import pytest
import os
from horey.gcp_api.gcp_service_entities.bucket import Bucket
from horey.gcp_api.gcp_clients.storage_client import StorageClient
from horey.h_logger import get_logger
from horey.gcp_api.gcp_api_configuration_policy import GCPAPIConfigurationPolicy
logger = get_logger()

configuration = GCPAPIConfigurationPolicy()
configuration.configuration_file_full_path = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..", "ignore", "gcp_api_configuration_values.py"))
configuration.init_from_file()


# region done
@pytest.mark.skip(reason="IAM policies will be inited explicitly")
def test_provision_bucket():
    pdb.set_trace()
    bucket = Bucket({})
    bucket.name = "horey-test"
    client = StorageClient()
    client.provision_bucket(Bucket)


if __name__ == "__main__":
    test_provision_bucket()

