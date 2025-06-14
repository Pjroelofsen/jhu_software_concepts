from src.pizza import Pizza

class Order:
    def __init__(self):
        self.pizzas = []
        self.total_cost = 0
        self.paid = False

    def input_pizza(self, crust, sauce, cheese, toppings):
        pizza = Pizza(crust, sauce, cheese, toppings)
        self.pizzas.append(pizza)
        self.total_cost += pizza.cost()

    def order_paid(self):
        self.paid = True

    def __str__(self):
        pizzas_str = "\n".join(str(pizza) for pizza in self.pizzas)
        return f"Customer Order:\n{pizzas_str}\nTotal Cost: ${self.total_cost}"
