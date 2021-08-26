"""
Module to handle AWS RDS instances
"""
from horey.aws_api.aws_services_entities.aws_object import AwsObject
from horey.aws_api.base_entities.region import Region


class RDSDBCluster(AwsObject):
    """
    Class representing RDS DB instance
    """

    def __init__(self, dict_src, from_cache=False):
        super().__init__(dict_src)
        self._region = None
        self.availability_zones = None
        self.db_subnet_group_name = None
        self.db_cluster_parameter_group_name = None
        self.kms_key_id = None

        if from_cache:
            self._init_object_from_cache(dict_src)
            return

        init_options = {
            "DBClusterIdentifier": lambda x, y: self.init_default_attr(x, y, formatted_name="id"),
            "DBClusterArn": lambda x, y: self.init_default_attr(x, y, formatted_name="arn"),
            "AllocatedStorage": self.init_default_attr,
            "AvailabilityZones": self.init_default_attr,
            "BackupRetentionPeriod": self.init_default_attr,
            "DatabaseName": self.init_default_attr,
            "DBClusterParameterGroup": self.init_default_attr,
            "DBSubnetGroup": self.init_default_attr,
            "Status": self.init_default_attr,
            "EarliestRestorableTime": self.init_default_attr,
            "Endpoint": self.init_default_attr,
            "ReaderEndpoint": self.init_default_attr,
            "MultiAZ": self.init_default_attr,
            "Engine": self.init_default_attr,
            "EngineVersion": self.init_default_attr,
            "LatestRestorableTime": self.init_default_attr,
            "Port": self.init_default_attr,
            "MasterUsername": self.init_default_attr,
            "PreferredBackupWindow": self.init_default_attr,
            "PreferredMaintenanceWindow": self.init_default_attr,
            "ReadReplicaIdentifiers": self.init_default_attr,
            "DBClusterMembers": self.init_default_attr,
            "VpcSecurityGroups": self.init_default_attr,
            "HostedZoneId": self.init_default_attr,
            "StorageEncrypted": self.init_default_attr,
            "KmsKeyId": self.init_default_attr,
            "DbClusterResourceId": self.init_default_attr,
            "AssociatedRoles": self.init_default_attr,
            "IAMDatabaseAuthenticationEnabled": self.init_default_attr,
            "ClusterCreateTime": self.init_default_attr,
            "EnabledCloudwatchLogsExports": self.init_default_attr,
            "EngineMode": self.init_default_attr,
            "DeletionProtection": self.init_default_attr,
            "HttpEndpointEnabled": self.init_default_attr,
            "ActivityStreamStatus": self.init_default_attr,
            "CopyTagsToSnapshot": self.init_default_attr,
            "CrossAccountClone": self.init_default_attr,
            "DomainMemberships": self.init_default_attr,
            "TagList": self.init_default_attr,
        }

        self.init_attrs(dict_src, init_options)

    def _init_object_from_cache(self, dict_src):
        """
        Init the object from saved cache dict
        :param dict_src:
        :return:
        """
        options = {}
        self._init_from_cache(dict_src, options)

    def update_from_raw_response(self, dict_src):
        init_options = {
            "DBClusterIdentifier": lambda x, y: self.init_default_attr(x, y, formatted_name="id"),
            "DBClusterArn": lambda x, y: self.init_default_attr(x, y, formatted_name="arn"),
            "AllocatedStorage": self.init_default_attr,
            "AvailabilityZones": self.init_default_attr,
            "BackupRetentionPeriod": self.init_default_attr,
            "DatabaseName": self.init_default_attr,
            "DBClusterParameterGroup": self.init_default_attr,
            "DBSubnetGroup": self.init_default_attr,
            "Status": self.init_default_attr,
            "EarliestRestorableTime": self.init_default_attr,
            "Endpoint": self.init_default_attr,
            "ReaderEndpoint": self.init_default_attr,
            "MultiAZ": self.init_default_attr,
            "Engine": self.init_default_attr,
            "EngineVersion": self.init_default_attr,
            "LatestRestorableTime": self.init_default_attr,
            "Port": self.init_default_attr,
            "MasterUsername": self.init_default_attr,
            "PreferredBackupWindow": self.init_default_attr,
            "PreferredMaintenanceWindow": self.init_default_attr,
            "ReadReplicaIdentifiers": self.init_default_attr,
            "DBClusterMembers": self.init_default_attr,
            "VpcSecurityGroups": self.init_default_attr,
            "HostedZoneId": self.init_default_attr,
            "StorageEncrypted": self.init_default_attr,
            "KmsKeyId": self.init_default_attr,
            "DbClusterResourceId": self.init_default_attr,
            "AssociatedRoles": self.init_default_attr,
            "IAMDatabaseAuthenticationEnabled": self.init_default_attr,
            "ClusterCreateTime": self.init_default_attr,
            "EnabledCloudwatchLogsExports": self.init_default_attr,
            "EngineMode": self.init_default_attr,
            "DeletionProtection": self.init_default_attr,
            "HttpEndpointEnabled": self.init_default_attr,
            "ActivityStreamStatus": self.init_default_attr,
            "CopyTagsToSnapshot": self.init_default_attr,
            "CrossAccountClone": self.init_default_attr,
            "DomainMemberships": self.init_default_attr,
            "TagList": self.init_default_attr,
        }

        self.init_attrs(dict_src, init_options)

    def generate_create_request(self):
        """
        response = client.create_db_cluster(

)
        """
        request = dict()
        if self.availability_zones:
            request["AvailabilityZones"] = self.availability_zones

        if self.db_subnet_group_name:
            request["DBSubnetGroupName"] = self.db_subnet_group_name

        if self.db_cluster_parameter_group_name:
            request["DBClusterParameterGroupName"] = self.db_cluster_parameter_group_name

        request["BackupRetentionPeriod"] = self.backup_retention_period
        request["DatabaseName"] = self.database_name
        request["DBClusterIdentifier"] = self.db_cluster_identifier
        request["VpcSecurityGroupIds"] = self.vpc_security_group_ids
        request["Engine"] = self.engine = "aurora-mysql"
        request["EngineVersion"] = self.engine_version
        request["Port"] = self.port

        request["MasterUsername"] = self.master_username
        request["MasterUserPassword"] = self.master_user_password
        request["PreferredBackupWindow"] = self.preferred_backup_window
        request["PreferredMaintenanceWindow"] = self.preferred_maintenance_window
        request["StorageEncrypted"] = self.storage_encrypted

        request["EnableCloudwatchLogsExports"] = self.enable_cloudwatch_logs_exports

        if self.kms_key_id:
            request["KmsKeyId"] = self.kms_key_id

        request["EngineMode"] = self.engine_mode

        request["DeletionProtection"] = self.deletion_protection
        request["CopyTagsToSnapshot"] = self.copy_tags_to_snapshot

        request["Tags"] = self.tags

        return request

    @property
    def region(self):
        if self._region is not None:
            return self._region

        if self.arn is not None:
            self._region = Region.get_region(self.arn.split(":")[3])

        return self._region

    @region.setter
    def region(self, value):
        if not isinstance(value, Region):
            raise ValueError(value)

        self._region = value
    """
    117 height 46 
    30 sholders 11.8
    31 body 12
    56 waist 22
    """