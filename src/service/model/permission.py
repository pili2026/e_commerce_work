from enum import StrEnum


class PermissionNamesEnum(StrEnum):
    CREATE_PRODUCT = "create_product"
    READ_PRODUCT = "read_product"
    UPDATE_PRODUCT = "update_product"
    DELETE_PRODUCT = "delete_product"
    CREATE_ORDER = "create_order"
    READ_OWN_ORDER = "read_own_order"
    READ_ALL_ORDERS = "read_all_orders"
    UPDATE_ORDER = "update_order"
    DELETE_ORDER = "delete_order"

    @staticmethod
    def get_all_values():
        return [e.value for e in PermissionNamesEnum]

    @staticmethod
    def get_all_names():
        return [e.name for e in PermissionNamesEnum]
