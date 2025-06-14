"""
The order module handles customer orders made up of pizza objects.
"""

from src.pizza import Pizza

class Order:
    """A class to house the customer order."""

    def __init__(self):
        """
        Initializes the Order with an empty list of pizzas and unpaid status.
        """
        self.pizzas = []
        self.total_cost = 0
        self.paid = False

    def input_pizza(self, crust, sauce, cheese, toppings):
        """
        Adds a pizza to the order and updates the total cost.

        Parameters:
            crust (str): The crust of the pizza.
            sauce (str): The sauce of the pizza.
            cheese (str): The cheese of the pizza.
            toppings (list of str): The toppings of the pizza.
        """
        pizza = Pizza(crust, sauce, cheese, toppings)
        self.pizzas.append(pizza)
        self.total_cost += pizza.cost()

    def order_paid(self):
        """
        Marks the order as paid.
        """
        self.paid = True

    def __str__(self):
        """
        Returns a string summarizing the customer's order.

        Returns:
            str: Summary of pizzas and cost.
        """
        header = "Customer Requested:\n"
        pizzas_str = "\n".join(str(pizza) for pizza in self.pizzas)
        return header + pizzas_str
