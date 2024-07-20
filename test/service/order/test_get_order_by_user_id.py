from unittest.mock import AsyncMock, patch
from uuid import uuid4

import pytest

from service.model.order import Order, OrderStatusEnum
from service.order import OrderService


@pytest.mark.asyncio
async def test_when_called_then_delegate_to_repository(order_service: OrderService):
    # Arrange
    order_id = uuid4()
    user_id = uuid4()

    stub_order = Order(id=order_id, user_id=user_id, status=OrderStatusEnum.PROCESSING, detail=None)

    with patch.object(
        order_service.order_repository, "get_order", AsyncMock(return_value=stub_order)
    ) as mock_get_order:
        # Act
        result = await order_service.get_order(order_id=None, user_id=user_id)

        # Assert
        assert result == stub_order
        mock_get_order.assert_called_once_with(order_id=None, user_id=user_id)
