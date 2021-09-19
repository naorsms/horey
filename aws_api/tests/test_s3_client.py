import os

from horey.aws_api.aws_clients.s3_client import S3Client
from horey.aws_api.aws_services_entities.s3_bucket import S3Bucket
from horey.aws_api.base_entities.aws_account import AWSAccount
from horey.aws_api.base_entities.region import Region


AWSAccount.set_aws_region(Region.get_region('us-west-2'))

TEST_BUCKET_NAME = "horey-test-bucket"


def test_init_s3_client():
    assert isinstance(S3Client(), S3Client)


def test_provision_s3_bucket():
    region = Region.get_region("us-west-2")
    s3_client = S3Client()

    s3_bucket = S3Bucket({})
    s3_bucket.region = region
    s3_bucket.name = TEST_BUCKET_NAME
    s3_bucket.acl = "private"

    s3_bucket.policy = S3Bucket.Policy({})
    s3_bucket.policy.version = "2012-10-17"
    s3_bucket.policy.statement = [
          {
            "Sid": "AllowReadAny",
            "Effect": "Allow",
            "Principal": "*",
            "Action": "s3:GetObject",
            "Resource": f"arn:aws:s3:::{s3_bucket.name}/*"
          }
        ]

    s3_client.provision_bucket(s3_bucket)


def create_test_file(path, size):
    print(f"Creating test file {path}")
    with open(path, "w+") as file_handler:
        file_handler.write("a" * size)


def test_upload_small_file_to_s3():
    path = "./test_file"
    # 10 Byte
    size = 10

    create_test_file(path, size)

    s3_client = S3Client()
    src_data_path = path
    dst_root_key = "root"
    s3_client.upload(TEST_BUCKET_NAME, src_data_path, dst_root_key, keep_src_object_name=False)


def test_upload_small_dir_to_s3():
    dir_path = "./test_files_dir"
    file_name = "test_file"
    path = os.path.join(dir_path, file_name)
    os.makedirs(dir_path, exist_ok=True)
    size = 10

    create_test_file(path, size)

    s3_client = S3Client()
    src_data_path = dir_path
    dst_root_key = "root"
    s3_client.upload(TEST_BUCKET_NAME, src_data_path, dst_root_key, keep_src_object_name=True)


def test_upload_large_file_to_s3():
    dir_path = "./test_files_dir"
    file_name = "test_file"
    path = os.path.join(dir_path, file_name)
    os.makedirs(dir_path, exist_ok=True)
    size = 500 * 1024 * 1024

    create_test_file(path, size)

    s3_client = S3Client()
    src_data_path = path
    dst_root_key = "root"
    s3_client.upload(TEST_BUCKET_NAME, src_data_path, dst_root_key, keep_src_object_name=True)


def test_upload_large_files_directory_to_s3():
    dir_path = "./test_files_dir"
    os.makedirs(dir_path, exist_ok=True)
    for counter in range(10):
        file_name = f"test_file_{counter}"
        path = os.path.join(dir_path, file_name)
        size = 500 * 1024 * 1024

        create_test_file(path, size)

    s3_client = S3Client()
    src_data_path = dir_path
    dst_root_key = "root"
    s3_client.upload(TEST_BUCKET_NAME, src_data_path, dst_root_key, keep_src_object_name=True)


def test_upload_small_files_directory_to_s3():
    dir_path = "./test_files_dir"
    os.makedirs(dir_path, exist_ok=True)
    for counter in range(100000):
        file_name = f"test_file_{counter}"
        path = os.path.join(dir_path, file_name)
        # 100KB
        size = 100 * 1024

        create_test_file(path, size)

    s3_client = S3Client()
    src_data_path = dir_path
    dst_root_key = "root"
    s3_client.upload(TEST_BUCKET_NAME, src_data_path, dst_root_key, keep_src_object_name=True)


if __name__ == "__main__":
    #test_init_s3_client()
    #test_provision_s3_bucket()
    test_upload_small_file_to_s3()
    #test_upload_large_file_to_s3()
    #test_upload_large_files_directory_to_s3()
    #test_upload_small_files_directory_to_s3()
    #test_multipart_upload_file()
