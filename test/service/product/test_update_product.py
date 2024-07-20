from unittest.mock import AsyncMock, patch
from uuid import uuid4

import pytest

from service.model.product import UpdateProduct, Product
from service.product import ProductService


@pytest.mark.asyncio
async def test_when_called_then_delegate_to_repository(product_service: ProductService):
    # Arrange
    product_id = uuid4()
    product_to_update = UpdateProduct(name="Updated Product", price=150.0, stock=5, total=20)

    stub_update_product = Product(
        id=product_id,
        name="Updated Product",
        price=150.0,
        stock=5,
        total=20,
    )

    with patch.object(
        product_service.product_repository, "update_product", AsyncMock(return_value=stub_update_product)
    ) as mock_update_product:
        # Act
        result = await product_service.update_product(product_id=product_id, update_product=product_to_update)

        # Assert
        assert result == stub_update_product
        mock_update_product.assert_called_once_with(product_id=product_id, update_product=product_to_update)
