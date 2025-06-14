# src/order.py

"""
order module

This module defines the Order class for managing pizza orders.
"""

from src.pizza import Pizza


class Order:
    """
    This creates an order.

    Attributes:
        pizzas: list of Pizza objects in the order.
        total_cost: cumulative cost of the order.
        paid: boolean indicating whether the order has been paid.
    """

    def __init__(self):
        """
        Initialize a new Order with an empty pizzas list, zero total cost, and unpaid status.
        """
        self.pizzas = []
        self.total_cost = 0
        self.paid = False

    def input_pizza(self, crust, sauce, cheese, toppings):
        """
        Add a new Pizza to the order and update the total cost.

        Args:
            crust: the crust type for the pizza.
            sauce: the sauce type for the pizza.
            cheese: the cheese type for the pizza.
            toppings: list of toppings for the pizza.

        Raises:
            ValueError: if Pizza(...) raises due to an invalid crust or other issue.
        """
        pizza = Pizza(crust, sauce, cheese, toppings)
        self.pizzas.append(pizza)
        self.total_cost += pizza.cost()

    def order_paid(self):
        """
        Mark this order as paid by setting the paid flag to True.
        """
        self.paid = True

    def __str__(self):
        """
        Return a formatted string representation of the order.

        Returns:
            A multi-line string listing each pizza and the total cost.
        """
        pizzas_str = "\n".join(str(pizza) for pizza in self.pizzas)
        return f"Customer Order:\n{pizzas_str}\nTotal Cost: ${self.total_cost}"
