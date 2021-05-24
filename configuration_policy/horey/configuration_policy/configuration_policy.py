import os
import json
import sys
import argparse


from horey.h_logger import get_logger
from horey.common_utils.common_utils import CommonUtils
logger = get_logger()
import pdb


class ConfigurationPolicy:
    """
    Base class to handle Configuration Policies.
    Should be capt as simple as possible as it should run in various environments.
    ENVIRON_ATTRIBUTE_PREFIX - prefix used to specify which environ values should be used to init configuration.
    """

    ENVIRON_ATTRIBUTE_PREFIX = "horey_"

    def __init__(self):
        """
        Save all the files used to configure - used for prints in
        """
        self._configuration_file_full_path = []
    
    @property
    def configuration_file_full_path(self):
        if len(self._configuration_file_full_path) > 0:
            return self._configuration_file_full_path[-1]
        return None
    
    @configuration_file_full_path.setter
    def configuration_file_full_path(self, value):
        if not os.path.exists(value):
            raise ValueError(f"File does not exist: {value}")

        self._configuration_file_full_path.append(value)

    @property
    def configuration_files_history(self):
        return self._configuration_file_full_path

    @configuration_files_history.setter
    def configuration_files_history(self, _):
        raise ValueError("Readonly property")

    def _set_attribute_value(self, attribute_name, attribute_value):
        if not hasattr(self, f"_{attribute_name}"):
            raise ValueError(attribute_name)

        setattr(self, attribute_name, attribute_value)

    def init_from_command_line(self, parser=None):
        """
        Very important notice: expects all values are strings. Attributes with None value - being removed.
        """

        if parser is None:
            parser = self.generate_parser()
        namespace_arguments = parser.parse_args()
        dict_arguments = vars(namespace_arguments)

        dict_arguments = {key: value for key, value in dict_arguments.items() if value is not None}

        self.init_from_dictionary(dict_arguments, custom_source_log="Init attribute '{}' from command line argument")

    def init_from_dictionary(self, dict_src, custom_source_log=None):
        """

        :param dict_src:
        :param custom_source_log: Because everything is a dict we will path custom log line to indicate what is the real source of the value.
        :return:
        """
        for key, value in dict_src.items():
            if custom_source_log is not None:
                log_line = custom_source_log.format(key)
            else:
                log_line = f"Init attribute '{key}' from dictionary"
            logger.info(log_line)
            self._set_attribute_value(key, value)

    def init_from_environ(self):
        for key_tmp, value in os.environ.items():
            key = key_tmp.lower()
            if key.startswith(self.ENVIRON_ATTRIBUTE_PREFIX):
                key = key[len(self.ENVIRON_ATTRIBUTE_PREFIX):]

                log_line = f"Init attribute '{key}' from environment variable '{key_tmp}'"
                logger.info(log_line)

                self._set_attribute_value(key, value)

    def init_from_file(self):
        if self.configuration_file_full_path is None:
            raise ValueError("Configuration file was not set")

        if self.configuration_file_full_path.endswith(".py"):
            return self.init_from_python_file()

        if self.configuration_file_full_path.endswith(".json"):
            return self.init_from_json_file()

        raise TypeError(self.configuration_file_full_path)

    def init_from_python_file(self):
        config = CommonUtils.load_object_from_module(self.configuration_file_full_path, "main")
        self.init_from_dictionary(config.__dict__, custom_source_log="Init attribute '{}' from python file: '" + self.configuration_file_full_path + "'")

    def init_from_json_file(self):
        with open(self.configuration_file_full_path) as file_handler:
            dict_arguments = json.load(file_handler)
        self.init_from_dictionary(dict_arguments, custom_source_log="Init attribute '{}' from json file: '" + self.configuration_file_full_path + "'")

    def generate_parser(self):
        """
        This function generates a parser based on exposed parameters.
        """

        """
        parse_known_args - if Tr
        """
        description = f"{self.__class__.__name__} autogenerated parser"
        parser = argparse.ArgumentParser(description=description)

        for parameter in self.__dict__:
            if not parameter.startswith("_"):
                continue
            parameter = f"--{parameter[1:]}"
            parser.add_argument(parameter, type=str, required=False)

        return parser

    def convert_to_dict(self):
        dict_ret = {}
        for key in self.__dict__.keys():
            if not key.startswith("_"):
                continue
            attr_name = key[1:]
            dict_ret[attr_name] = getattr(self, attr_name)

        if dict_ret["configuration_file_full_path"] is None:
            del dict_ret["configuration_file_full_path"]

        return dict_ret

    class StaticValueError(RuntimeError):
        pass

