from unittest.mock import AsyncMock, patch
from uuid import uuid4

import pytest

from service.model.order import CreateOrder, OrderDetail
from service.model.order_detail import CreateOrderDetail
from service.order_detail import OrderDetailService


@pytest.mark.asyncio
async def test_when_called_then_delegate_to_repository(order_detail_service: OrderDetailService):
    # Arrange
    create_order = CreateOrder(user_id=uuid4())

    create_order_detail = CreateOrderDetail(order_id=create_order.id, product_name="AP", quantity=10)

    stub_created_order_detail = OrderDetail(
        id=uuid4(),
        order_id=uuid4(),
        user_id=create_order.user_id,
        product_id=uuid4(),
        product_name=create_order_detail.product_name,
        quantity=create_order_detail.quantity,
        product_price=10,
        total_price=10 * create_order_detail.quantity,
    )

    with patch.object(
        order_detail_service.order_detail_repository,
        "insert_order_with_detail",
        AsyncMock(return_value=stub_created_order_detail),
    ) as mock_insert_order_with_detail:
        # Act
        result = await order_detail_service.create_order_detail(
            create_order_detail=create_order_detail, create_order=create_order
        )

        # Assert
        assert result == stub_created_order_detail
        mock_insert_order_with_detail.assert_called_once_with(
            create_order=create_order, create_order_detail=create_order_detail
        )
