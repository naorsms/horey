import os
from horey.configuration_policy.configuration_policy import ConfigurationPolicy


class AWSAPIConfigurationPolicy(ConfigurationPolicy):
    def __init__(self):
        super().__init__()
        self._aws_api_regions = None
        self._aws_api_account = None
        self._aws_api_cache_dir = None
        self._aws_api_s3_cache_dir = None
        self._aws_api_s3_bucket_objects_cache_dir = None
        self._aws_api_ec2_cache_dir = None
        self._aws_api_lambda_cache_dir = None
        self._aws_api_cleanup_cache_dir = None
        self._aws_api_cloudwatch_log_groups_cache_dir = None
        self._aws_api_cloudwatch_log_groups_streams_cache_dir = None
        self._accounts_file = None

    @property
    def aws_api_regions(self):
        if self._aws_api_regions is None:
            raise ValueError("aws_api_regions were not set")
        return self._aws_api_regions

    @aws_api_regions.setter
    def aws_api_regions(self, value):
        if not isinstance(value, list):
            raise ValueError(f"aws_api_regions must be a list received {value} of type: {type(value)}")

        self._aws_api_regions = value

    @property
    def aws_api_account(self):
        if self._aws_api_account is None:
            raise ValueError("aws_api_account was not set")
        return self._aws_api_account

    @aws_api_account.setter
    def aws_api_account(self, value):
        if not isinstance(value, str):
            raise ValueError(f"aws_api_account must be a string received {value} of type: {type(value)}")

        self._aws_api_account = value

    @property
    def aws_api_cache_dir(self):
        if self._aws_api_cache_dir is None:
            raise ValueError("aws_api_cache_dir was not set")
        return self._aws_api_cache_dir

    @aws_api_cache_dir.setter
    def aws_api_cache_dir(self, value):
        self._aws_api_cache_dir = value
        os.makedirs(self._aws_api_cache_dir, exist_ok=True)

    # region s3

    @property
    def aws_api_s3_cache_dir(self):
        if self._aws_api_s3_cache_dir is None:
            self._aws_api_s3_cache_dir = os.path.join(self.aws_api_cache_dir, self.aws_api_account, "s3")
            os.makedirs(self._aws_api_s3_cache_dir, exist_ok=True)
        return self._aws_api_s3_cache_dir

    @aws_api_s3_cache_dir.setter
    def aws_api_s3_cache_dir(self, value):
        raise ValueError(value)
    
    @property
    def aws_api_s3_buckets_cache_file(self):
        return os.path.join(self.aws_api_s3_cache_dir, "buckets.json")

    @aws_api_s3_buckets_cache_file.setter
    def aws_api_s3_buckets_cache_file(self, value):
        raise ValueError(value)

    @property
    def aws_api_s3_bucket_objects_cache_dir(self):
        if self._aws_api_s3_bucket_objects_cache_dir is None:
            self._aws_api_s3_bucket_objects_cache_dir = os.path.join(self.aws_api_s3_cache_dir, "s3_buckets_objects")
            os.makedirs(self._aws_api_s3_bucket_objects_cache_dir, exist_ok=True)
        return self._aws_api_s3_bucket_objects_cache_dir

    @aws_api_s3_bucket_objects_cache_dir.setter
    def aws_api_s3_bucket_objects_cache_dir(self, value):
        raise ValueError(value)

    # endregion
    # region cloudwatch
    @property
    def aws_api_cloudwatch_log_groups_cache_dir(self):
        if self._aws_api_cloudwatch_log_groups_cache_dir is None:
            self._aws_api_cloudwatch_log_groups_cache_dir = os.path.join(self.aws_api_cache_dir, self.aws_api_account, "cloudwatch")
            os.makedirs(self._aws_api_cloudwatch_log_groups_cache_dir, exist_ok=True)
        return self._aws_api_cloudwatch_log_groups_cache_dir

    @aws_api_cloudwatch_log_groups_cache_dir.setter
    def aws_api_cloudwatch_log_groups_cache_dir(self, value):
        raise ValueError(value)

    @property
    def aws_api_cloudwatch_log_groups_streams_cache_dir(self):
        if self._aws_api_cloudwatch_log_groups_streams_cache_dir is None:
            self._aws_api_cloudwatch_log_groups_streams_cache_dir = os.path.join(self.aws_api_cloudwatch_log_groups_cache_dir, "streams")
            os.makedirs(self._aws_api_cloudwatch_log_groups_streams_cache_dir, exist_ok=True)
        return self._aws_api_cloudwatch_log_groups_streams_cache_dir

    @aws_api_cloudwatch_log_groups_streams_cache_dir.setter
    def aws_api_cloudwatch_log_groups_streams_cache_dir(self, value):
        raise ValueError(value)


    @property
    def aws_api_cloudwatch_log_groups_cache_file(self):
        return os.path.join(self.aws_api_cloudwatch_log_groups_cache_dir, "cloudwatch_log_groups.json")

    @aws_api_cloudwatch_log_groups_cache_file.setter
    def aws_api_cloudwatch_log_groups_cache_file(self, value):
        raise ValueError(value)


    # endregion
    
    # region ec2
    @property
    def aws_api_ec2_cache_dir(self):
        if self._aws_api_ec2_cache_dir is None:
            self._aws_api_ec2_cache_dir = os.path.join(self.aws_api_cache_dir, self.aws_api_account, "ec2")
            os.makedirs(self._aws_api_ec2_cache_dir, exist_ok=True)
        return self._aws_api_ec2_cache_dir

    @aws_api_ec2_cache_dir.setter
    def aws_api_ec2_cache_dir(self, value):
        raise ValueError(value)

    @property
    def aws_api_ec2_instances_cache_file(self):
        return os.path.join(self.aws_api_ec2_cache_dir, "instances.json")

    @aws_api_ec2_instances_cache_file.setter
    def aws_api_ec2_instances_cache_file(self, value):
        raise ValueError(value)
    
    @property
    def aws_api_ec2_security_groups_cache_file(self):
        return os.path.join(self.aws_api_ec2_cache_dir, "security_groups.json")

    @aws_api_ec2_security_groups_cache_file.setter
    def aws_api_ec2_security_groups_cache_file(self, value):
        raise ValueError(value)
    # endregion

    # region lambda
    @property
    def aws_api_lambda_cache_dir(self):
        if self._aws_api_lambda_cache_dir is None:
            self._aws_api_lambda_cache_dir = os.path.join(self.aws_api_cache_dir, self.aws_api_account, "lambda")
            os.makedirs(self._aws_api_lambda_cache_dir, exist_ok=True)
        return self._aws_api_lambda_cache_dir

    @aws_api_lambda_cache_dir.setter
    def aws_api_lambda_cache_dir(self, value):
        raise ValueError(value)

    @property
    def aws_api_lambdas_cache_file(self):
        return os.path.join(self.aws_api_lambda_cache_dir, "lambdas.json")

    @aws_api_lambdas_cache_file.setter
    def aws_api_lambdas_cache_file(self, value):
        raise ValueError(value)
    # endregion
    
    # region cleanup
    @property
    def aws_api_cleanup_cache_dir(self):
        if self._aws_api_cleanup_cache_dir is None:
            self._aws_api_cleanup_cache_dir = os.path.join(self.aws_api_cache_dir, self.aws_api_account, "cleanup")
            os.makedirs(self._aws_api_cleanup_cache_dir, exist_ok=True)
        return self._aws_api_cleanup_cache_dir

    @aws_api_cleanup_cache_dir.setter
    def aws_api_cleanup_cache_dir(self, value):
        raise ValueError(value)

    @property
    def aws_api_cleanups_lambda_file(self):
        return os.path.join(self.aws_api_cleanup_cache_dir, "lambda.txt")

    @aws_api_cleanups_lambda_file.setter
    def aws_api_cleanups_lambda_file(self, value):
        raise ValueError(value)

    @property
    def aws_api_cleanups_s3_report_file(self):
        return os.path.join(self.aws_api_cleanup_cache_dir, "s3_report.txt")

    @aws_api_cleanups_s3_report_file.setter
    def aws_api_cleanups_s3_report_file(self, value):
        raise ValueError(value)

    @property
    def aws_api_cleanups_s3_summarized_data_file(self):
        return os.path.join(self.aws_api_cleanup_cache_dir, "s3_cleanup_data.json")

    @aws_api_cleanups_s3_summarized_data_file.setter
    def aws_api_cleanups_s3_summarized_data_file(self, value):
        raise ValueError(value)

    @property
    def aws_api_cleanup_cloudwatch_report_file(self):
        return os.path.join(self.aws_api_cleanup_cache_dir, "cloudwatch_report.txt")

    @aws_api_cleanup_cloudwatch_report_file.setter
    def aws_api_cleanup_cloudwatch_report_file(self, value):
        raise ValueError(value)

    @property
    def accounts_file(self):
        return self._accounts_file

    @accounts_file.setter
    def accounts_file(self, value):
        self._accounts_file = value

    # endregion
    #HOSTED_ZONES_CACHE_FILE = os.path.join(CACHE_DIR, "hosted_zones.json")
    #IAM_POLICIES_CACHE_FILE = os.path.join(CACHE_DIR, "iam_policies.json")

