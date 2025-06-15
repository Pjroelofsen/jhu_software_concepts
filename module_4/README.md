# Pizza Application

[![Documentation Status](https://readthedocs.org/projects/module-4-rtd/badge/?version=latest)](https://module-4-rtd.readthedocs.io/en/latest/modules.html)

A simple Python package for building and totaling pizza orders, plus generated Sphinx documentation.

## Overview

- **`src/pizza.py`**  
  Defines a `Pizza` class with customizable crust, sauce, cheese, and toppings, and computes its cost.

- **`src/order.py`**  
  Defines an `Order` class that aggregates one or more `Pizza` objects, tracks total cost, and payment status.

## Prerequisites

- Python **3.10** or higher

## Installation

1. Clone the repo and enter its root directory:
   ```bash
   git clone <your-repo-url>
   cd your-project
   ```
2. Create and activate a virtual environment:
   ```bash
   python3.10 -m venv venv
   source venv/bin/activate   # on Linux/macOS
   venv\Scripts\activate    # on Windows
   ```
3. Install dependencies:
   ```bash
   pip install --upgrade pip
   pip install -r requirements.txt
   ```

## Usage

```python
from src.order import Order

order = Order()
order.input_pizza('thin', 'tomato', 'mozzarella', ['pepperoni', 'olives'])
order.input_pizza('stuffed', 'pesto', 'parmesan', [])
print(order)
# Customer Order:
# Pizza(thin, tomato, mozzarella, ['pepperoni', 'olives'])
# Pizza(stuffed, pesto, parmesan, [])
# Total Cost: $...
```

Mark an order as paid:
```python
order.order_paid()
```

## Generating Documentation

We use Sphinx with the ReadTheDocs theme and Napoleon for Google-style docstrings.

1. Ensure the docs requirements are installed (they’re included in `requirements.txt`).
2. From the project root run:
   ```bash
   sphinx-apidoc -f -o docs/source src --separate
   cd docs
   make clean html
   ```
3. Open `docs/build/html/index.html` in your browser.  

## Documentation

Full API docs are hosted on Read the Docs:

🔗 https://module-4-rtd.readthedocs.io/en/latest/modules.html

## Project Structure

```
your-project/
├── src/
│   ├── pizza.py
│   └── order.py
├── docs/
│   ├── Makefile
│   └── source/
│       ├── conf.py
│       ├── index.rst
│       ├── modules.rst
│       ├── src.rst
│       ├── src.pizza.rst
│       └── src.order.rst
├── requirements.txt
└── README.md
```
