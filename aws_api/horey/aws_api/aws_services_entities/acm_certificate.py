"""
AWS Lambda representation
"""
import pdb

from horey.aws_api.aws_services_entities.aws_object import AwsObject
from horey.aws_api.base_entities.region import Region


class ACMCertificate(AwsObject):
    """
    AWS ACMCertificate class
    """

    def __init__(self, dict_src, from_cache=False):
        super().__init__(dict_src)
        self._region = None
        self.status = None

        if from_cache:
            self._init_object_from_cache(dict_src)
            return

        init_options = {
            "CertificateArn": lambda x, y: self.init_default_attr(x, y, formatted_name="arn"),
            "DomainName": self.init_default_attr,
            "SubjectAlternativeNames": self.init_default_attr,
            "DomainValidationOptions": self.init_default_attr,
            "Serial": self.init_default_attr,
            "Subject": self.init_default_attr,
            "Issuer": self.init_default_attr,
            "CreatedAt": self.init_default_attr,
            "IssuedAt": self.init_default_attr,
            "Status": self.init_default_attr,
            "NotBefore": self.init_default_attr,
            "NotAfter": self.init_default_attr,
            "KeyAlgorithm": self.init_default_attr,
            "SignatureAlgorithm": self.init_default_attr,
            "InUseBy": self.init_default_attr,
            "Type": self.init_default_attr,
            "KeyUsages": self.init_default_attr,
            "ExtendedKeyUsages": self.init_default_attr,
            "RenewalEligibility": self.init_default_attr,
            "Options": self.init_default_attr,
            "ImportedAt": self.init_default_attr,
            "RenewalSummary": self.init_default_attr,
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
            "CertificateArn": lambda x, y: self.init_default_attr(x, y, formatted_name="arn"),
            "DomainName": self.init_default_attr,
            "SubjectAlternativeNames": self.init_default_attr,
            "DomainValidationOptions": self.init_default_attr,
            "Serial": self.init_default_attr,
            "Subject": self.init_default_attr,
            "Issuer": self.init_default_attr,
            "CreatedAt": self.init_default_attr,
            "IssuedAt": self.init_default_attr,
            "Status": self.init_default_attr,
            "NotBefore": self.init_default_attr,
            "NotAfter": self.init_default_attr,
            "KeyAlgorithm": self.init_default_attr,
            "SignatureAlgorithm": self.init_default_attr,
            "InUseBy": self.init_default_attr,
            "Type": self.init_default_attr,
            "KeyUsages": self.init_default_attr,
            "ExtendedKeyUsages": self.init_default_attr,
            "RenewalEligibility": self.init_default_attr,
            "Options": self.init_default_attr,
            "ImportedAt": self.init_default_attr,
            "RenewalSummary": self.init_default_attr,
        }

        self.init_attrs(dict_src, init_options)

    def generate_create_request(self):
        """
        DomainName='string',
    ValidationMethod='EMAIL'|'DNS',
    SubjectAlternativeNames=[
        'string',
    ],
    IdempotencyToken='string',
    DomainValidationOptions=[
        {
            'DomainName': 'string',
            'ValidationDomain': 'string'
        },
    ],
    Options={
        'CertificateTransparencyLoggingPreference': 'ENABLED'|'DISABLED'
    },
    CertificateAuthorityArn='string',
    Tags=[
        {
            'Key': 'string',
            'Value': 'string'
        },
    ]
)
        """
        request = dict()
        request["DomainName"] = self.domain_name
        request["ValidationMethod"] = self.validation_method

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
