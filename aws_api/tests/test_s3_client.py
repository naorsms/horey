import os
import sys

from horey.aws_api.aws_clients.s3_client import S3Client
from horey.aws_api.aws_services_entities.s3_bucket import S3Bucket
import pdb
from horey.h_logger import get_logger
from horey.aws_api.base_entities.aws_account import AWSAccount
from horey.aws_api.base_entities.region import Region
from horey.common_utils.common_utils import CommonUtils

from unittest.mock import Mock
configuration_values_file_full_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "h_logger_configuration_values.py")
logger = get_logger(configuration_values_file_full_path=configuration_values_file_full_path)

accounts_file_full_path = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "ignore", "aws_api_managed_accounts.py"))

accounts = CommonUtils.load_object_from_module(accounts_file_full_path, "main")
AWSAccount.set_aws_account(accounts["1111"])
AWSAccount.set_aws_region(accounts["1111"].regions['us-west-2'])

mock_values_file_path = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "ignore", "mock_values.py"))
mock_values = CommonUtils.load_object_from_module(mock_values_file_path, "main")


def test_init_ecs_client():
    assert isinstance(S3Client(), S3Client)


def test_provision_s3_bucket():
    region = Region.get_region("us-west-2")
    s3_client = S3Client()

    #ecs_task_definition = Mock()
    #ecs_task_definition.arn = mock_values["ecs_task_definition.arn"]

    s3_bucket = S3Bucket({})
    s3_bucket.region = region
    s3_bucket.name = "horey-alexey-ytest-test"
    s3_bucket.acl = "private"

    s3_client.provision_bucket(s3_bucket)


if __name__ == "__main__":
    test_init_ecs_client()
    test_provision_s3_bucket()
