"""
Some reusable stuff.
"""
import datetime
import importlib
import os
import sys


class CommonUtils:
    """
    Some stuff to be reused
    """
    @staticmethod
    def find_objects_by_values(objects, values, max_count=None):
        """
        Find objects with all specified values.
        If no such attr: do not add to the return list

        :param objects: list of objects
        :param values: dict of key - value
        :param max_count: Maximum amount to return
        :return:
        """

        objects_ret = []
        for obj in objects:
            for key, value in values.items():
                try:
                    if getattr(obj, key) != value:
                        break
                except AttributeError:
                    break
            else:
                objects_ret.append(obj)
                if max_count is not None and len(objects_ret) >= max_count:
                    break

        return objects_ret

    @staticmethod
    def int_to_str(number):
        """
        Int to comma separated string
        :param number:
        :return:
        """
        if not isinstance(number, int):
            raise ValueError(number)

        str_ret = '{:,}'.format(number)

        return str_ret

    @staticmethod
    def bytes_to_str(number):
        """
        Pretty print of storage
        :param number:
        :return:
        """
        if not isinstance(number, int):
            raise ValueError(number)

        if number < 0:
            raise ValueError(number)

        if number == 0:
            return "0"

        mapping = {
                    1: "Bytes",
                    1024: "KiB",
                    1024 ** 2: "MiB",
                    1024 ** 3: "GiB",
                    1024 ** 4: "TiB",
                    1024 ** 5: "PiB"
        }

        key_limit = 1

        for key_limit_tmp, _ in mapping.items():
            if number < key_limit_tmp:
                break
            key_limit = key_limit_tmp
        quotient, remainder = divmod(number, key_limit)
        int_percent_reminder = round((remainder/key_limit)*100)
        if int_percent_reminder == 0:
            return_number = str(quotient)
        else:
            float_result = float(f"{quotient}.{int_percent_reminder}")
            return_number = str(round(float_result, 2))
        return f"{return_number} {mapping[key_limit]}"

    @staticmethod
    def timestamp_to_datetime(timestamp, microseconds_value=False):
        """
        int/str to datetime.

        @param timestamp:
        @param microseconds_value: Is the value in microseconds
        :return:
        """

        if microseconds_value:
            try:
                timestamp /= 1000
            except TypeError:
                timestamp = int(timestamp) / 1000

        return datetime.datetime.fromtimestamp(timestamp)

    @staticmethod
    def load_object_from_module(module_full_path, callback_function_name):
        module_path = os.path.dirname(module_full_path)
        sys.path.insert(0, module_path)
        module_name = os.path.basename(module_full_path).strip(".py")
        module = importlib.import_module(module_name)
        module = importlib.reload(module)
        main_func = getattr(module, callback_function_name)
        ret_object = main_func()

        popped_path = sys.path.pop(0)
        if popped_path != module_path:
            raise RuntimeError(f"System Path must not be changed while importing configuration_policy: {module_full_path}. "
                               f"Changed from {module_path} to {popped_path}")

        return ret_object