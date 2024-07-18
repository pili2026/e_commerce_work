from enum import StrEnum


class RoleNamesEnum(StrEnum):
    MANAGER = "manager"
    CUSTOMER = "customer"

    @staticmethod
    def get_all_values():
        return [e.value for e in RoleNamesEnum]

    @staticmethod
    def get_all_names():
        return [e.name for e in RoleNamesEnum]
