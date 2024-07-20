from unittest.mock import AsyncMock, patch
from uuid import uuid4

import pytest

from service.product import ProductService


@pytest.mark.asyncio
async def test_when_called_then_delegate_to_repository(product_service: ProductService):
    # Arrange
    product_id = uuid4()
    stub_delete_product = True

    with patch.object(
        product_service.product_repository, "delete_product", AsyncMock(return_value=stub_delete_product)
    ) as mock_delete_product:

        # Act
        result = await product_service.delete_product(product_id)

        # Assert
        assert result == stub_delete_product
        mock_delete_product.assert_called_once_with(product_id)
