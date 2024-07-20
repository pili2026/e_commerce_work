from unittest.mock import MagicMock

import pytest

from service.product import ProductService
from repository.product import ProductRepository


@pytest.fixture
def product_service() -> ProductService:
    return ProductService(MagicMock(ProductRepository))
