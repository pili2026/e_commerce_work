from unittest.mock import AsyncMock, patch
from uuid import UUID
import pytest

from service.model.product import CreateProduct, Product
from service.product import ProductService


@pytest.mark.asyncio
async def test_when_called_then_delegate_to_repository(product_service: ProductService):
    # Arrange
    create_product = CreateProduct(
        name="Sample Product",
        description="This is a sample product",
        price=100.0,
        quantity=10,
    )

    stub_inserted_product = Product(
        id=UUID("00000000-0000-0000-0000-000000000000"),
        name="Sample Product",
        description="This is a sample product",
        price=100.0,
        quantity=10,
    )

    with patch.object(
        product_service.product_repository,
        "insert_product",
        AsyncMock(return_value=stub_inserted_product),
    ) as mock_insert_product:

        # Act
        result = await product_service.create_product(create_product)

        # Assert
        assert result == stub_inserted_product
        mock_insert_product.assert_called_once_with(create_product)
