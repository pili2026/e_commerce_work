from unittest.mock import MagicMock

import pytest

from service.order import OrderService
from repository.order import OrderRepository


@pytest.fixture
def order_service() -> OrderService:
    return OrderService(MagicMock(OrderRepository))
