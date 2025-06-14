"""
This module defines the Pizza class, which represents a single pizza with its crust, sauce, cheese, and optional toppings,
and can compute its total cost.
"""
class Pizza:
    """
    A class to represent an individual pizza

    Args:
        crust (str): The crust of the pizza.
        sauce (str): The sauce of the pizza.
        cheese (str): The type of cheese on the pizza.
        toppings (List[str]): A list of toppings on the pizza.
    """
    CRUST_PRICES = {"thin": 5, "thick": 6, "gluten free": 8}
    SAUCE_PRICES = {"marinara": 2, "pesto": 3, "liv": 5}
    TOPPING_PRICES = {"pineapple": 1, "pepperoni": 2, "mushrooms": 3}

    def __init__(self, crust, sauce, cheese, toppings):
        """
        Initialize a new Pizza instance.

        Raises:
            ValueError: If crust type is not one of the known bases.
        """
        self.crust = crust
        self.sauce = sauce
        self.cheese = cheese
        self.toppings = toppings

    def cost(self):
        """
        Calculate the total cost of this pizza.

        Combines:
          - Crust cost
          - Sauce cost
          - Topping cost

        Returns:
            float: The total cost of the pizza.
        """
        total = 0
        total += self.CRUST_PRICES.get(self.crust, 0)
        total += self.SAUCE_PRICES.get(self.sauce, 0)
        for topping in self.toppings:
            total += self.TOPPING_PRICES.get(topping, 0)
        return total

    def __str__(self):
        return f"Pizza with {self.crust} crust, {self.sauce} sauce, {self.cheese}, toppings: {', '.join(self.toppings)}. Cost: ${self.cost()}"
