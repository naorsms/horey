"""
AWS Lambda representation
"""
import pdb

from horey.aws_api.aws_services_entities.aws_object import AwsObject
from horey.aws_api.base_entities.region import Region
from enum import Enum

class ECSCluster(AwsObject):
    """
    AWS VPC class
    """

    def __init__(self, dict_src, from_cache=False):
        super().__init__(dict_src)
        self._region = None
        self.capacity_providers = None
        self.default_capacity_provider_strategy = None

        if from_cache:
            self._init_object_from_cache(dict_src)
            return

        init_options = {
            "clusterArn": lambda x, y: self.init_default_attr(x, y, formatted_name="arn"),
            "clusterName": lambda x, y: self.init_default_attr(x, y, formatted_name="name"),
            "status": self.init_default_attr,
            "registeredContainerInstancesCount": self.init_default_attr,
            "runningTasksCount": self.init_default_attr,
            "pendingTasksCount": self.init_default_attr,
            "activeServicesCount": self.init_default_attr,
            "statistics": self.init_default_attr,
            "tags": self.init_default_attr,
            "settings": self.init_default_attr,
            "capacityProviders": self.init_default_attr,
            "defaultCapacityProviderStrategy": self.init_default_attr,
            "attachments": self.init_default_attr,
            "attachmentsStatus": self.init_default_attr,
        }

        self.init_attrs(dict_src, init_options)

    def _init_object_from_cache(self, dict_src):
        """
        Init from cache
        :param dict_src:
        :return:
        """
        options = {}
        self._init_from_cache(dict_src, options)

    def update_from_raw_response(self, dict_src):
        init_options = {
            "clusterArn": lambda x, y: self.init_default_attr(x, y, formatted_name="arn"),
            "clusterName": lambda x, y: self.init_default_attr(x, y, formatted_name="name"),
            "status": self.init_default_attr,
            "registeredContainerInstancesCount": self.init_default_attr,
            "runningTasksCount": self.init_default_attr,
            "pendingTasksCount": self.init_default_attr,
            "activeServicesCount": self.init_default_attr,
            "statistics": self.init_default_attr,
            "tags": self.init_default_attr,
            "settings": self.init_default_attr,
            "capacityProviders": self.init_default_attr,
            "defaultCapacityProviderStrategy": self.init_default_attr,
            "attachments": self.init_default_attr,
            "attachmentsStatus": self.init_default_attr,
        }

        self.init_attrs(dict_src, init_options)

    def generate_create_request(self):
        request = dict()
        request["clusterName"] = self.name
        request["tags"] = self.tags
        request["settings"] = self.settings
        request["configuration"] = self.configuration
        if self.capacity_providers is not None:
            request["capacityProviders"] = self.capacity_providers
        if self.default_capacity_provider_strategy is not None:
            request["defaultCapacityProviderStrategy"] = self.default_capacity_provider_strategy

        return request

    def update_from_raw_create(self, dict_src):
        raise NotImplementedError()
        pdb.set_trace()
        init_options = {
            "ECSClusterId": lambda x, y: self.init_default_attr(x, y, formatted_name="id"),
            "ECSClusterArn": lambda x, y: self.init_default_attr(x, y, formatted_name="arn"),
            "AvailabilityZone": self.init_default_attr,
            "AvailabilityZoneId": self.init_default_attr,
            "AvailableIpAddressCount": self.init_default_attr,
            "CidrBlock": self.init_default_attr,
            "DefaultForAz": self.init_default_attr,
            "MapPublicIpOnLaunch": self.init_default_attr,
            "MapCustomerOwnedIpOnLaunch": self.init_default_attr,
            "State": self.init_default_attr,
            "VpcId": self.init_default_attr,
            "OwnerId": self.init_default_attr,
            "AssignIpv6AddressOnCreation": self.init_default_attr,
            "Ipv6CidrBlockAssociationSet": self.init_default_attr,
            "Tags": self.init_default_attr,
        }

        self.init_attrs(dict_src, init_options)

    @property
    def region(self):
        if self._region is not None:
            return self._region

        if self.arn is None:
            raise NotImplementedError()
        self._region = Region.get_region(self.arn.split(":")[3])

        return self._region

    @region.setter
    def region(self, value):
        if not isinstance(value, Region):
            raise ValueError(value)

        self._region = value

    def generate_dispose_request(self, cluster):
        request = dict()
        request["cluster"] = cluster.name
        return request

    def get_status(self):
        return self.Status[self.status]

    class Status(Enum):
        ACTIVE = 0
        PROVISIONING = 1
        DEPROVISIONING = 2
        FAILED = 3
        INACTIVE = 4
