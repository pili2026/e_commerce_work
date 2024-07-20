from unittest.mock import AsyncMock, patch
from uuid import uuid4

import pytest

from service.model.product import Product
from service.product import ProductService


@pytest.mark.asyncio
async def test_when_called_then_delegate_to_repository(product_service: ProductService):
    # Arrange
    stub_get_product = Product(
        id=uuid4(),
        name="Sample Product",
        description="This is a sample product",
        price=100.0,
        quantity=10,
    )

    with patch.object(
        product_service.product_repository, "get_product", AsyncMock(return_value=stub_get_product)
    ) as mock_get_product:
        # Act
        result = await product_service.get_product(product_name=stub_get_product.name)

        # Assert
        assert result == stub_get_product
        mock_get_product.assert_called_once_with(product_name=stub_get_product.name, product_id=None)
