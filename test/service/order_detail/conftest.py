from unittest.mock import MagicMock

import pytest

from service.order_detail import OrderDetailService
from repository.order_detail import OrderDetailRepository


@pytest.fixture
def order_detail_service() -> OrderDetailService:
    return OrderDetailService(MagicMock(OrderDetailRepository))
