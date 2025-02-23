"""
Class to represent ec2 spot fleet request
"""

from horey.aws_api.aws_services_entities.aws_object import AwsObject


class EC2LaunchTemplateVersion(AwsObject):
    """
    Class to represent ec2 launch template
    """

    def __init__(self, dict_src, from_cache=False):
        """
        Init EC2 launch template version with boto3 dict
        :param dict_src:
        """
        super().__init__(dict_src)

        if from_cache:
            self._init_ec2_launch_template_version_from_cache(dict_src)
            return

        init_options = {
            "LaunchTemplateId": lambda x, y: self.init_default_attr(x, y, formatted_name="id"),
            "LaunchTemplateName": lambda x, y: self.init_default_attr(x, y, formatted_name="name"),
            "VersionNumber": self.init_default_attr,
            "CreatedBy": self.init_default_attr,
            "DefaultVersion": self.init_default_attr,
            "LaunchTemplateData": self.init_default_attr,
            "CreateTime": self.init_default_attr,
        }

        self.init_attrs(dict_src, init_options)

    def _init_ec2_launch_template_version_from_cache(self, dict_src):
        """
        Init self from preserved dict.
        :param dict_src:
        :return:
        """
        options = {}

        self._init_from_cache(dict_src, options)

    def generate_create_request(self):
        raise NotImplementedError()
        request = dict()
        request["clusterName"] = self.name
        request["tags"] = self.tags

        return request