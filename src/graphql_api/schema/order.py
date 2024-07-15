from uuid import UUID
import strawberry

from service.model.order import OrderStatusEnum


@strawberry.type
class Order:
    id: UUID
    user_id: UUID
    status: OrderStatusEnum
