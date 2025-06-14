import pytest
from src.order import Order

@pytest.mark.order
def test_order_init():
    order = Order()
    assert order.pizzas == []
    assert order.total_cost == 0
    assert order.paid is False

@pytest.mark.order
def test_order_str():
    order = Order()
    order.input_pizza("thin", "marinara", "mozzarella", ["pineapple"])
    order_str = str(order)
    assert "thin" in order_str
    assert "marinara" in order_str
    assert "pineapple" in order_str
    assert "$" in order_str

@pytest.mark.order
def test_order_input_pizza_updates_cost():
    order = Order()
    order.input_pizza("thick", "pesto", "mozzarella", ["pepperoni"])
    assert order.total_cost > 0

@pytest.mark.order
def test_order_paid_sets_paid_true():
    order = Order()
    order.order_paid()
    assert order.paid is True
