import pytest
from src.pizza import Pizza

@pytest.mark.pizza
def test_pizza_init_attributes_and_cost():
    pizza = Pizza("gluten free", "liv", "mozzarella", ["mushrooms"])
    assert pizza.crust == "gluten free"
    assert pizza.sauce == "liv"
    assert pizza.cheese == "mozzarella"
    assert pizza.toppings == ["mushrooms"]
    assert pizza.cost() > 0

@pytest.mark.pizza
def test_pizza_str_contains_description_and_cost():
    pizza = Pizza("thin", "marinara", "mozzarella", ["pepperoni"])
    pizza_str = str(pizza)
    assert "thin" in pizza_str
    assert "marinara" in pizza_str
    assert "pepperoni" in pizza_str
    assert "$" in pizza_str

@pytest.mark.pizza
def test_pizza_cost_calculation():
    pizza = Pizza("thick", "pesto", "mozzarella", ["pineapple", "mushrooms"])
    expected_cost = 6 + 3 + 1 + 3
    assert pizza.cost() == expected_cost
