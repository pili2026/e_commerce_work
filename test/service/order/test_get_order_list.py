from unittest.mock import AsyncMock, patch
from uuid import uuid4

import pytest

from service.model.order import Order, OrderStatusEnum
from service.order import OrderService


@pytest.mark.asyncio
async def test_when_called_then_delegate_to_repository(order_service: OrderService):
    # Arrange
    order_id_list = [uuid4(), uuid4()]
    user_id_list = [uuid4(), uuid4()]

    stub_order_list = [
        Order(id=order_id_list[0], user_id=user_id_list[0], status=OrderStatusEnum.PROCESSING, detail=None),
        Order(id=order_id_list[1], user_id=user_id_list[1], status=OrderStatusEnum.PROCESSING, detail=None),
    ]

    with patch.object(
        order_service.order_repository, "get_order_list", AsyncMock(return_value=stub_order_list)
    ) as mock_get_order_list:
        # Act
        result = await order_service.get_order_list(order_id_list=order_id_list, user_id=user_id_list)

        # Assert
        assert result == stub_order_list
        mock_get_order_list.assert_called_once_with(order_id_list=order_id_list, user_id=user_id_list)
