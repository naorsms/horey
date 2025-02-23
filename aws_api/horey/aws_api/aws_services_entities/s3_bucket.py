"""
Module handling S3 buckets
"""
import json
from horey.aws_api.aws_services_entities.aws_object import AwsObject
from horey.aws_api.base_entities.region import Region
import pdb


class S3Bucket(AwsObject):
    """
    Class representing S3 bucket.
    """

    def __init__(self, dict_src, from_cache=False):
        self.acl = None
        self.policy = None
        self.bucket_objects = []
        self.index_document = None
        self.error_document = None
        self.redirect_all_requests_to = None
        self.location = None

        super().__init__(dict_src)
        if from_cache:
            self._init_bucket_from_cache(dict_src)
            return

        init_options = {
            "Name": lambda x, y: self.init_default_attr(x, y, formatted_name="name"),
            "CreationDate": self.init_default_attr
        }

        self.init_attrs(dict_src, init_options)

    def _init_bucket_from_cache(self, dict_src):
        """
        Init the object from saved cache dict
        :param dict_src:
        :return:
        """
        options = {
            "acl": self._init_acl_from_cache,
            "policy": self._init_policy_from_cache,
            "region": self._init_region_from_cache,
        }

        self._init_from_cache(dict_src, options)

    def _init_region_from_cache(self, _, dict_src):
        if dict_src is None:
            return
        self.region = Region()
        self.region.init_from_dict(dict_src)

    def _init_acl_from_cache(self, _, dict_src):
        """
        Init bucket ACL from previously cached dict
        :param _:
        :param dict_src:
        :return:
        """
        if dict_src is None:
            return

        if self.acl is None:
            self.acl = S3Bucket.ACL(dict_src, from_cache=True)
        else:
            raise NotImplementedError

    def _init_policy_from_cache(self, _, dict_src):
        """
        Init policy object from previously cached dict
        :param _:
        :param dict_src:
        :return:
        """
        if self.policy is not None:
            raise NotImplementedError

        if dict_src is not None:
            self.policy = S3Bucket.Policy(dict_src, from_cache=True)

    def update_objects(self, lst_src, from_cache=False):
        """
        Update objects list with new object
        :param lst_src:
        :param from_cache:
        :return:
        """
        for dict_object in lst_src:
            bucket_object = S3Bucket.BucketObject(dict_object, from_cache=from_cache)
            self.bucket_objects.append(bucket_object)

    def update_acl(self, lst_src):
        """
        Update ACL from AWS API response list
        :param lst_src:
        :return:
        """
        if self.acl is None:
            self.acl = S3Bucket.ACL(lst_src)
        else:
            raise NotImplementedError()

    def update_policy(self, str_src):
        """
        Update Policy from AWS API response str
        :param str_src:
        :return:
        """
        if self.policy is None:
            self.policy = S3Bucket.Policy(str_src)
        else:
            raise NotImplementedError()

    def update_website(self, lst_src):
        if len(lst_src) > 1:
            raise ValueError(lst_src)

        init_options = {
            "IndexDocument": self.init_default_attr,
            "ErrorDocument": self.init_default_attr,
            "RedirectAllRequestsTo": self.init_default_attr,
            "ResponseMetadata": lambda x, y: 0
        }

        for dict_src in lst_src:
            self.init_attrs(dict_src, init_options)

    def update_location(self, lst_src):
        """
        For more info about this ugly stuff check get_dns_records docstring
        """
        if len(lst_src) > 1:
            raise ValueError(lst_src)
        self.location = lst_src[0] if lst_src[0] is not None else "us-east-1"
        return

    def get_dns_records(self):
        """
        If while reading this you say "WHAT????", read here and cry:
        https://docs.aws.amazon.com/general/latest/gr/s3.html#s3_website_region_endpoints
        and this:

        "
        LocationConstraint (string) --
        Specifies the Region where the bucket resides. For a list of all the Amazon S3 supported location constraints by Region, see Regions and Endpoints . Buckets in Region us-east-1 have a LocationConstraint of null .
        "

        Get all self dns records.
        :return:
        """

        mappings = {
                    "us-east-2": ".",
                    "us-east-1": "-",
                    "us-west-1": "-",
                    "us-west-2": "-",
                    "af-south-1": ".",
                    "ap-east-1": ".",
                    "ap-south-1": ".",
                    "ap-northeast-3": ".",
                    "ap-northeast-2": ".",
                    "ap-southeast-1": "-",
                    "ap-southeast-2": "-",
                    "ap-northeast-1": "-",
                    "eu-west-1": "-",
                    "sa-east-1": "-",
                    "us-gov-west-1": "-",
                    "ca-central-1": ".",
                    "cn-northwest-1": ".",
                    "eu-central-1": ".",
                    "eu-west-2": ".",
                    "eu-south-1": ".",
                    "eu-west-3": ".",
                    "eu-north-1": ".",
                    "me-south-1": ".",
                    "us-gov-east-1": "."}

        if self.index_document is None and self.error_document is None and self.redirect_all_requests_to is None:
            return []

        return [f"{self.name}.s3-website{mappings[self.location]}{self.location}.amazonaws.com"]

    def generate_create_request(self):
        """
            ACL='private'|'public-read'|'public-read-write'|'authenticated-read',
            'LocationConstraint': 'af-south-1'|'ap-east-1'|'ap-northeast-1'|'ap-northeast-2'|'ap-northeast-3'|'ap-south-1'|'ap-southeast-1'|'ap-southeast-2'|'ca-central-1'|'cn-north-1'|'cn-northwest-1'|'EU'|'eu-central-1'|'eu-north-1'|'eu-south-1'|'eu-west-1'|'eu-west-2'|'eu-west-3'|'me-south-1'|'sa-east-1'|'us-east-2'|'us-gov-east-1'|'us-gov-west-1'|'us-west-1'|'us-west-2'
            }
        """
        request = dict()
        request["ACL"] = self.acl
        request["Bucket"] = self.name

        request["CreateBucketConfiguration"] = {"LocationConstraint": self.region.region_mark}
        return request

    def generate_put_bucket_policy_request(self):
        request = dict()
        request["Policy"] = self.policy.generate_put_string()
        request["Bucket"] = self.name

        return request

    class ACL(AwsObject):
        """
        Class representing S3 Bucket's ACL
        """

        def __init__(self, src_data, from_cache=False):
            super(S3Bucket.ACL, self).__init__(src_data)
            self.grants = []

            if from_cache:
                if not isinstance(src_data, dict):
                    raise TypeError("Not implemented - replacement of pdb.set_trace")
                self._init_acl_from_cache(src_data)
                return

            if not isinstance(src_data, list):
                raise TypeError("Not implemented - replacement of pdb.set_trace")

            for dict_grant in src_data:
                grant = self.Grant(dict_grant)
                self.grants.append(grant)

        def _init_acl_from_cache(self, dict_src):
            """
            Init ACL from previously cached dict
            :param dict_src:
            :return:
            """
            options = {
                'grants': self._init_grants_from_cache,
            }

            self._init_from_cache(dict_src, options)

        def _init_grants_from_cache(self, _, lst_src):
            """
            Init grants from previously cached list
            :param _:
            :param lst_src:
            :return:
            """
            if self.grants:
                raise NotImplementedError("Can reinit yet")
            for dict_grant in lst_src:
                grant = self.Grant(dict_grant, from_cache=True)
                self.grants.append(grant)

        class Grant(AwsObject):
            """
            Class representing S3 bucket policy Grant.
            """

            def __init__(self, dict_src, from_cache=False):
                super(S3Bucket.ACL.Grant, self).__init__(dict_src)
                if from_cache:
                    self._init_grant_from_cache(dict_src)
                    return

                init_options = {
                    "Grantee": self.init_default_attr,
                    "Permission": self.init_default_attr
                }

                self.init_attrs(dict_src, init_options)

            def _init_grant_from_cache(self, dict_src):
                """
                Init grant from previously cached dict
                :param dict_src:
                :return:
                """
                options = {}

                self._init_from_cache(dict_src, options)

    class Policy(AwsObject):
        """
        Class representing S3 Bucket policy
        """

        def __init__(self, src_, from_cache=False):
            if isinstance(src_, str):
                dict_src = json.loads(src_)
            else:
                if from_cache:
                    self._init_policy_from_cache(src_)
                    return
                if not isinstance(src_, dict):
                    raise NotImplementedError("Not yet implemented")

                dict_src = src_

            super(S3Bucket.Policy, self).__init__(dict_src)
            if from_cache:
                raise NotImplementedError("Not yet implemented")

            init_options = {
                "Version": self.init_default_attr,
                "Statement": self.init_default_attr,
                "Id": self.init_default_attr,
            }

            self.init_attrs(dict_src, init_options)

        def _init_policy_from_cache(self, dict_src):
            """
            Init policy from previously cached dict
            :param dict_src:
            :return:
            """
            options = {}
            try:
                self._init_from_cache(dict_src, options)
            except Exception:
                print(dict_src)
                raise

        def generate_put_string(self):
            request_dict = {"Version": self.version, "Statement": self.statement}
            return json.dumps(request_dict)

    class BucketObject(AwsObject):
        """
        Class representing one saved object in S3 bucket.
        """

        def __init__(self, src_data, from_cache=False):
            self.key = None
            super(S3Bucket.BucketObject, self).__init__(src_data)

            if from_cache:
                self._init_bucket_object_from_cache(src_data)
                return

            init_options = {
                "Key": self.init_default_attr,
                "LastModified":  self.init_default_attr,
                "ETag":  self.init_default_attr,
                "Size":  self.init_default_attr,
                "StorageClass":  self.init_default_attr,
            }
            self.init_attrs(src_data, init_options)

        def _init_bucket_object_from_cache(self, dict_src):
            """
            Init object from previously cached dict.
            :param dict_src:
            :return:
            """
            options = {}
            self._init_from_cache(dict_src, options)

            self.size = dict_src["dict_src"]["Size"]
