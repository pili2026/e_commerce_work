from uuid import UUID
import strawberry


@strawberry.input
class InputOrderDetail:
    product_name: str
    quantity: int


@strawberry.type
class OrderDetail:
    id: UUID
    order_id: UUID
    product_id: UUID
    product_name: str
    product_price: float
    quantity: int
    total_price: float


@strawberry.input
class CreateOrderDetailInput(InputOrderDetail):
    pass


@strawberry.input
class UpdateOrderDetailInput(InputOrderDetail):
    pass
