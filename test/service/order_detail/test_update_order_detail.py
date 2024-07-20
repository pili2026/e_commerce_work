from unittest.mock import AsyncMock, patch
from uuid import uuid4

import pytest

from service.model.order import UpdateOrderDetail, OrderDetail
from service.order_detail import OrderDetailService


@pytest.mark.asyncio
async def test_when_called_then_delegate_to_repository(order_detail_service: OrderDetailService):
    # Arrange
    order_detail_id = uuid4()
    update_order_detail = UpdateOrderDetail(product_name="AP", quantity="5")

    stub_updated_order_detail = OrderDetail(
        id=uuid4(),
        order_id=uuid4(),
        user_id=uuid4(),
        product_id=uuid4(),
        product_name=update_order_detail.product_name,
        quantity=update_order_detail.quantity,
        product_price=10,
        total_price=10 * update_order_detail.quantity,
    )

    with patch.object(
        order_detail_service.order_detail_repository,
        "update_detail_with_product",
        AsyncMock(return_value=stub_updated_order_detail),
    ) as mock_update_detail_with_product:
        # Act
        result = await order_detail_service.update_order_detail(
            order_detail_id=order_detail_id, update_order_detail=update_order_detail
        )

        # Assert
        assert result == stub_updated_order_detail
        mock_update_detail_with_product.assert_called_once_with(
            order_detail_id=order_detail_id, update_order_detail=update_order_detail
        )
