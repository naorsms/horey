import os
import pytest

from horey.aws_api.aws_api import AWSAPI

from horey.h_logger import get_logger
from horey.aws_api.aws_api_configuration_policy import AWSAPIConfigurationPolicy


logger = get_logger()
configuration = AWSAPIConfigurationPolicy()
configuration.configuration_file_full_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "configuration_values.py")
configuration.init_from_file()

aws_api = AWSAPI(configuration=configuration)


@pytest.mark.skip(reason="IAM policies cleanup will be enabled explicitly")
def test_init_from_cache_and_cleanup_report_iam_policies():
    aws_api.init_iam_policies(from_cache=True, cache_file=configuration.aws_api_iam_policies_cache_file)
    aws_api.init_iam_roles(from_cache=True, cache_file=configuration.aws_api_iam_roles_cache_file)
    aws_api.cleanup_report_iam_policies(configuration.aws_api_cleanups_iam_policies_report_file)


@pytest.mark.skip(reason="IAM roles cleanup will be enabled explicitly")
def test_init_from_cache_and_cleanup_report_iam_roles():
    aws_api.init_iam_roles(from_cache=True, cache_file=configuration.aws_api_iam_roles_cache_file)
    aws_api.cleanup_report_iam_roles(configuration.aws_api_cleanups_iam_roles_report_file)


@pytest.mark.skip(reason="No way of currently testing this")
def test_init_from_cache_and_cleanup_lambdas():
    aws_api.init_security_groups(from_cache=True, cache_file=configuration.aws_api_ec2_security_groups_cache_file)
    aws_api.init_lambdas(from_cache=True, cache_file=configuration.aws_api_lambdas_cache_file)
    aws_api.init_cloud_watch_log_groups(from_cache=True, cache_file=configuration.aws_api_cloudwatch_log_groups_cache_file)
    tb_ret = aws_api.cleanup_report_lambdas(configuration.aws_api_cleanups_lambda_file, configuration.aws_api_cloudwatch_log_groups_streams_cache_dir)
    assert tb_ret is not None


@pytest.mark.skip(reason="No way of currently testing this")
def test_cleanup_report_cloud_watch_logs():
    aws_api.init_cloud_watch_log_groups(from_cache=True, cache_file=configuration.aws_api_cloudwatch_log_groups_cache_file)
    aws_api.cleanup_report_cloud_watch_log_groups(configuration.aws_api_cloudwatch_log_groups_streams_cache_dir, configuration.aws_api_cleanup_cloudwatch_logs_report_file)

@pytest.mark.skip(reason="No way of currently testing this")
def test_cleanup_report_cloud_watch_metrics():
    aws_api.cleanup_report_cloud_watch_metrics(configuration.aws_api_cloudwatch_metrics_cache_dir, configuration.aws_api_cleanup_cloudwatch_metrics_report_file)


@pytest.mark.skip(reason="No way of currently testing this")
def test_init_from_cache_and_cleanup_s3_buckets():
    aws_api.init_s3_buckets(from_cache=True, cache_file=configuration.aws_api_s3_buckets_cache_file)
    aws_api.generate_summarised_s3_cleanup_data(configuration.aws_api_s3_bucket_objects_cache_dir, configuration.aws_api_cleanups_s3_summarized_data_file)
    aws_api.cleanup_report_s3_buckets_objects(configuration.aws_api_cleanups_s3_summarized_data_file, configuration.aws_api_cleanups_s3_report_file)


@pytest.mark.skip(reason="No way of currently testing this")
def test_init_from_cache_and_cleanup_load_balancers():
    aws_api.init_classic_load_balancers(from_cache=True, cache_file=configuration.aws_api_classic_loadbalancers_cache_file)
    aws_api.init_load_balancers(from_cache=True, cache_file=configuration.aws_api_loadbalancers_cache_file)
    aws_api.init_target_groups(from_cache=True, cache_file=configuration.aws_api_loadbalancer_target_groups_cache_file)
    aws_api.cleanup_load_balancers(configuration.aws_api_cleanups_loadbalancers_report_file)


@pytest.mark.skip(reason="No way of currently testing this")
def test_init_from_cache_and_cleanup_report_dns_records():
    aws_api.init_ec2_instances(from_cache=True, cache_file=configuration.aws_api_ec2_instances_cache_file)
    aws_api.init_classic_load_balancers(from_cache=True, cache_file=configuration.aws_api_classic_loadbalancers_cache_file)
    aws_api.init_load_balancers(from_cache=True, cache_file=configuration.aws_api_loadbalancers_cache_file)
    aws_api.init_rds_db_instances(from_cache=True, cache_file=configuration.aws_api_databases_cache_file)
    aws_api.init_hosted_zones(from_cache=True, cache_file=configuration.aws_api_hosted_zones_cache_file)
    aws_api.init_cloudfront_distributions(from_cache=True, cache_file=configuration.aws_api_cloudfront_distributions_cache_file)
    aws_api.init_s3_buckets(from_cache=True, cache_file=configuration.aws_api_s3_buckets_cache_file)

    aws_api.cleanup_report_dns_records(configuration.aws_api_cleanups_dns_report_file)


@pytest.mark.skip(reason="No way of currently testing this")
def test_init_from_cache_and_cleanup_report_security_groups():
    aws_api.init_security_groups(from_cache=True, cache_file=configuration.aws_api_ec2_security_groups_cache_file)
    aws_api.init_target_groups(from_cache=True, cache_file=configuration.aws_api_loadbalancer_target_groups_cache_file)
    aws_api.init_classic_load_balancers(from_cache=True, cache_file=configuration.aws_api_classic_loadbalancers_cache_file)
    aws_api.init_load_balancers(from_cache=True, cache_file=configuration.aws_api_loadbalancers_cache_file)
    aws_api.init_network_interfaces(from_cache=True, cache_file=configuration.aws_api_ec2_network_interfaces_cache_file)

    aws_api.cleanup_report_security_groups(configuration.aws_api_cleanups_security_groups_report_file)


@pytest.mark.skip(reason="No way of currently testing this")
def test_init_from_cache_and_cleanup_report_network_interfaces():
    aws_api.init_network_interfaces(from_cache=True, cache_file=configuration.aws_api_ec2_network_interfaces_cache_file)

    aws_api.cleanup_report_network_interfaces(configuration.aws_api_cleanups_network_interfaces_report_file)


if __name__ == "__main__":
    test_init_from_cache_and_cleanup_s3_buckets()
