"""
AWS rds client to handle rds service API requests.
"""
import pdb

from horey.aws_api.aws_clients.boto3_client import Boto3Client
from horey.aws_api.aws_services_entities.rds_db_instance import RDSDBInstance
from horey.aws_api.aws_services_entities.rds_db_cluster import RDSDBCluster
from horey.aws_api.aws_services_entities.rds_db_subnet_group import RDSDBSubnetGroup
from horey.aws_api.aws_services_entities.rds_db_cluster_parameter_group import RDSDBClusterParameterGroup
from horey.aws_api.aws_services_entities.rds_db_parameter_group import RDSDBParameterGroup
from horey.aws_api.base_entities.aws_account import AWSAccount
from horey.h_logger import get_logger

logger = get_logger()


class RDSClient(Boto3Client):
    NEXT_PAGE_REQUEST_KEY = "Marker"
    NEXT_PAGE_RESPONSE_KEY = "Marker"
    """
    Client to handle specific aws service API calls.
    """
    def __init__(self):
        client_name = "rds"
        super().__init__(client_name)

    def get_all_db_instances(self, region=None):
        """
        Get all db_instances in all regions.
        :return:
        """

        if region is not None:
            return self.get_region_db_instances(region)

        final_result = list()
        for region in AWSAccount.get_aws_account().regions.values():
            final_result += self.get_region_db_instances(region)

        return final_result

    def get_region_db_instances(self, region):
        final_result = list()
        AWSAccount.set_aws_region(region)
        for response in self.execute(self.client.describe_db_instances, "DBInstances"):
            obj = RDSDBInstance(response)
            final_result.append(obj)

        return final_result
    
    def get_all_db_clusters(self, region=None):
        """
        Get all db_clusters in all regions.
        :return:
        """

        if region is not None:
            return self.get_region_db_clusters(region)

        final_result = list()
        for region in AWSAccount.get_aws_account().regions.values():
            final_result += self.get_region_db_clusters(region)

        return final_result

    def get_region_db_clusters(self, region):
        final_result = list()
        AWSAccount.set_aws_region(region)
        for response in self.execute(self.client.describe_db_clusters, "DBClusters"):
            obj = RDSDBCluster(response)
            final_result.append(obj)

        return final_result
    
    def provision_db_cluster(self, db_cluster):
        region_db_clusters = self.get_region_db_clusters(db_cluster.region)
        for region_db_cluster in region_db_clusters:
            if db_cluster.name == region_db_cluster.name:
                db_cluster.update_from_raw_response(region_db_cluster.dict_src)
                return

        AWSAccount.set_aws_region(db_cluster.region)
        response = self.provision_db_cluster_raw(db_cluster.generate_create_request())
        db_cluster.update_from_raw_response(response)
        
    def provision_db_cluster_raw(self, request_dict):
        """
        Returns ARN
        """
        logger.info(f"Creating db_cluster: {request_dict}")
        for response in self.execute(self.client.create_db_cluster, "DBCluster",
                                     filters_req=request_dict):
            return response
    
    def get_all_db_subnet_groups(self, region=None):
        """
        Get all db_subnet_groups in all regions.
        :return:
        """

        if region is not None:
            return self.get_region_db_subnet_groups(region)

        final_result = list()
        for region in AWSAccount.get_aws_account().regions.values():
            final_result += self.get_region_db_subnet_groups(region)

        return final_result

    def get_region_db_subnet_groups(self, region):
        final_result = list()
        AWSAccount.set_aws_region(region)
        for response in self.execute(self.client.describe_db_subnet_groups, "DBSubnetGroups"):
            obj = RDSDBSubnetGroup(response)
            final_result.append(obj)

        return final_result
    
    def provision_db_subnet_group(self, db_subnet_group):
        region_db_subnet_groups = self.get_region_db_subnet_groups(db_subnet_group.region)
        for region_db_subnet_group in region_db_subnet_groups:
            if db_subnet_group.name == region_db_subnet_group.name:
                db_subnet_group.update_from_raw_response(region_db_subnet_group.dict_src)
                return

        AWSAccount.set_aws_region(db_subnet_group.region)
        response = self.provision_db_subnet_group_raw(db_subnet_group.generate_create_request())
        db_subnet_group.update_from_raw_response(response)

    def provision_db_subnet_group_raw(self, request_dict):
        """
        Returns ARN
        """
        logger.info(f"Creating db_subnet_group: {request_dict}")
        for response in self.execute(self.client.create_db_subnet_group, "DBSubnetGroup",
                                     filters_req=request_dict):
            return response
    
    def get_all_db_cluster_parameter_groups(self, region=None):
        """
        Get all db_cluster_parameter_groups in all regions.
        :return:
        """

        if region is not None:
            return self.get_region_db_cluster_parameter_groups(region)

        final_result = list()
        for region in AWSAccount.get_aws_account().regions.values():
            final_result += self.get_region_db_cluster_parameter_groups(region)

        return final_result

    def get_region_db_cluster_parameter_groups(self, region, full_information=True):
        final_result = list()
        AWSAccount.set_aws_region(region)
        for response in self.execute(self.client.describe_db_cluster_parameter_groups, "DBClusterParameterGroups"):
            obj = RDSDBClusterParameterGroup(response)
            final_result.append(obj)
            if full_information:
                filters_req = {"DBClusterParameterGroupName": obj.name}
                obj.parameters = []
                for response_param in self.execute(self.client.describe_db_cluster_parameters, "Parameters", filters_req=filters_req):
                    obj.parameters.append(response_param)

        return final_result

    def get_all_db_parameter_groups(self, region=None):
        """
        Get all db_parameter_groups in all regions.
        :return:
        """

        if region is not None:
            return self.get_region_db_parameter_groups(region)

        final_result = list()
        for region in AWSAccount.get_aws_account().regions.values():
            final_result += self.get_region_db_parameter_groups(region)

        return final_result

    def get_region_db_parameter_groups(self, region, full_information=True):
        final_result = list()
        AWSAccount.set_aws_region(region)
        for response in self.execute(self.client.describe_db_parameter_groups, "DBParameterGroups"):
            obj = RDSDBParameterGroup(response)
            final_result.append(obj)
            if full_information:
                filters_req = {"DBParameterGroupName": obj.name}
                obj.parameters = []
                for response_param in self.execute(self.client.describe_db_parameters, "Parameters", filters_req=filters_req):
                    obj.parameters.append(response_param)

        return final_result

    def provision_db_cluster_parameter_group(self, db_cluster_parameter_group):
        region_db_cluster_parameter_groups = self.get_region_db_cluster_parameter_groups(db_cluster_parameter_group.region)
        for region_db_cluster_parameter_group in region_db_cluster_parameter_groups:
            if db_cluster_parameter_group.name == region_db_cluster_parameter_group.name:
                db_cluster_parameter_group.update_from_raw_response(region_db_cluster_parameter_group.dict_src)
                return

        AWSAccount.set_aws_region(db_cluster_parameter_group.region)
        response = self.provision_db_cluster_parameter_group_raw(db_cluster_parameter_group.generate_create_request())
        db_cluster_parameter_group.update_from_raw_response(response)

    def provision_db_cluster_parameter_group_raw(self, request_dict):
        """
        Returns ARN
        """
        logger.info(f"Creating db_cluster_parameter_group: {request_dict}")
        for response in self.execute(self.client.create_db_cluster_parameter_group, "DBClusterParameterGroup",
                                     filters_req=request_dict):
            return response
        
    def provision_db_parameter_group(self, db_parameter_group):
        region_db_parameter_groups = self.get_region_db_parameter_groups(db_parameter_group.region)
        for region_db_parameter_group in region_db_parameter_groups:
            if db_parameter_group.name == region_db_parameter_group.name:
                db_parameter_group.update_from_raw_response(region_db_parameter_group.dict_src)
                return

        AWSAccount.set_aws_region(db_parameter_group.region)
        response = self.provision_db_parameter_group_raw(db_parameter_group.generate_create_request())
        db_parameter_group.update_from_raw_response(response)

    def provision_db_parameter_group_raw(self, request_dict):
        """
        Returns ARN
        """
        logger.info(f"Creating db_parameter_group: {request_dict}")
        for response in self.execute(self.client.create_db_parameter_group, "DBParameterGroup",
                                     filters_req=request_dict):
            return response

    def provision_db_instance(self, db_instance):
        region_db_instances = self.get_region_db_instances(db_instance.region)
        for region_db_instance in region_db_instances:
            if db_instance.name == region_db_instance.name:
                db_instance.update_from_raw_response(region_db_instance.dict_src)
                return

        AWSAccount.set_aws_region(db_instance.region)
        response = self.provision_db_instance_raw(db_instance.generate_create_request())
        db_instance.update_from_raw_response(response)

    def provision_db_instance_raw(self, request_dict):
        """
        Returns ARN
        """
        logger.info(f"Creating db_instance: {request_dict}")
        for response in self.execute(self.client.create_db_instance, "DBInstance",
                                     filters_req=request_dict):
            return response
