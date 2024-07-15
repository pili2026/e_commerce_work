from service.model.product import CreateProduct


SYSTEM_PRODUCT_LIST: list[CreateProduct] = [
    CreateProduct(name="Router", price=20.0, stock=10),
    CreateProduct(name="Switch", price=10.0, stock=10),
]
