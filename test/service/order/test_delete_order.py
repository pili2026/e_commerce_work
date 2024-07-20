from unittest.mock import AsyncMock, patch
from uuid import uuid4

import pytest

from service.order import OrderService


@pytest.mark.asyncio
async def test_when_called_then_delegate_to_repository(order_service: OrderService):
    # Arrange
    order_id = uuid4()
    stub_delete_order_result = True

    with patch.object(
        order_service.order_repository, "delete_order", AsyncMock(return_value=stub_delete_order_result)
    ) as mock_delete_order:
        # Act
        result = await order_service.delete_order(order_id)

        # Assert
        assert result == stub_delete_order_result
        mock_delete_order.assert_called_once_with(order_id)
