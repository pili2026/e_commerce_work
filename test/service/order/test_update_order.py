from unittest.mock import AsyncMock, patch
from uuid import uuid4

import pytest

from service.model.order import OrderStatusEnum, UpdateOrder, Order
from service.order import OrderService


@pytest.mark.asyncio
async def test_when_called_then_delegate_to_repository(order_service: OrderService):
    # Arrange
    order_id = uuid4()
    update_order = UpdateOrder(status=OrderStatusEnum.PROCESSING)

    stub_updated_order = Order(id=order_id, user_id=uuid4(), status=OrderStatusEnum.DONE, detail=None)

    with patch.object(
        order_service.order_repository, "update_order", AsyncMock(return_value=stub_updated_order)
    ) as mock_update_order:
        # Act
        result = await order_service.update_order(order_id=order_id, update_order=update_order)

        # Assert
        assert result == stub_updated_order
        mock_update_order.assert_called_once_with(order_id=order_id, update_order=update_order)
