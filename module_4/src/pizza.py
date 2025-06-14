class Pizza:
    CRUST_PRICES = {"thin": 5, "thick": 6, "gluten free": 8}
    SAUCE_PRICES = {"marinara": 2, "pesto": 3, "liv": 5}
    TOPPING_PRICES = {"pineapple": 1, "pepperoni": 2, "mushrooms": 3}

    def __init__(self, crust, sauce, cheese, toppings):
        self.crust = crust
        self.sauce = sauce
        self.cheese = cheese
        self.toppings = toppings

    def cost(self):
        total = 0
        total += self.CRUST_PRICES.get(self.crust, 0)
        total += self.SAUCE_PRICES.get(self.sauce, 0)
        for topping in self.toppings:
            total += self.TOPPING_PRICES.get(topping, 0)
        return total

    def __str__(self):
        return f"Pizza with {self.crust} crust, {self.sauce} sauce, {self.cheese}, toppings: {', '.join(self.toppings)}. Cost: ${self.cost()}"
