"""
The pizza module defines pizza structure and pricing.
"""

class Pizza:
    """A class representing a single pizza."""

    CRUST_PRICES = {"thin": 5, "thick": 6, "gluten free": 8}
    SAUCE_PRICES = {"marinara": 2, "pesto": 3, "liv": 5}
    TOPPING_PRICES = {"pineapple": 1, "pepperoni": 2, "mushrooms": 3}

    def __init__(self, crust, sauce, cheese, toppings):
        """
        Initialize a pizza with crust, sauce, cheese, and toppings.

        Parameters:
            crust (str): Crust type.
            sauce (str): Sauce type.
            cheese (str): Cheese name.
            toppings (list of str): List of toppings.
        """
        self.crust = crust
        self.sauce = sauce
        self.cheese = cheese
        self.toppings = toppings

    def cost(self):
        """
        Compute total cost of the pizza.

        Returns:
            int: Price of the pizza.
        """
        total = self.CRUST_PRICES.get(self.crust, 0)
        total += self.SAUCE_PRICES.get(self.sauce, 0)
        for topping in self.toppings:
            total += self.TOPPING_PRICES.get(topping, 0)
        return total

    def __str__(self):
        """
        Return a string description of the pizza.

        Returns:
            str: Human-readable description.
        """
        return f"Crust: {self.crust}, Sauce: [{self.sauce}], Cheese: {self.cheese}, Toppings: {self.toppings}, Cost: {self.cost()}"
