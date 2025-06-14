import pytest
from src.order import Order

@pytest.mark.order
@pytest.mark.pizza
def test_multiple_pizzas_in_order():
    order = Order()
    order.input_pizza("thin", "marinara", "mozzarella", ["pineapple"])
    order.input_pizza("gluten free", "liv", "mozzarella", ["mushrooms", "pepperoni"])
    assert len(order.pizzas) == 2

@pytest.mark.order
@pytest.mark.pizza
def test_order_cost_with_multiple_pizzas():
    order = Order()
    order.input_pizza("thin", "marinara", "mozzarella", ["pineapple"])        # 5 + 2 + 1
    order.input_pizza("thick", "pesto", "mozzarella", ["pepperoni", "mushrooms"])  # 6 + 3 + 2 + 3
    expected_cost = (5 + 2 + 1) + (6 + 3 + 2 + 3)
    assert order.total_cost == expected_cost
