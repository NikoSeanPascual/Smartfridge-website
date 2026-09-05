# SmartFridge 🧊

SmartFridge is a Django-powered web application designed to reduce food waste and simplify meal planning. By tracking the ingredients currently in your fridge, SmartFridge dynamically calculates which dishes you can prepare right now, displays percentage matches, alerts you to missing items, and provides step-by-step cooking instructions.

---

## 🛠️ Tech Stack

* **Backend:** Python, Django
* **Database:** SQLite3
* **Frontend:** HTML5, CSS3 (Custom CSS with CSS variables & responsive layout), JavaScript (ES6)
* **Design & Typography:** Google Fonts (*Jersey 10* pixel display font, *Inter* body font), Dark/Light theme switching

---

## ✨ Features

* **Pantry Inventory Tracker (`My Fridge`):**
  * Add ingredients with custom quantities (e.g., `10pcs`, `100g`).
  * Real-time freshness and expiration status monitoring (`Fresh`, `Expiring Soon`, `Expired`).
  * Quick removal or consumption of ingredients with a single click.

* **Smart Recipe Matcher (`What Can I Cook?`):**
  * **Dynamic Matching Algorithm:** Calculates a match percentage based on available inventory vs. required recipe ingredients.
  * **Smart Sorting:** Automatically orders recipes from highest match (100%) to lowest match (0%).
  * **Ingredient Breakdown:** Displays precise match counts (e.g., `3/3` or `1/4`) and highlights missing items in red.
  * **Interactive Instructions:** Expandable step-by-step cooking guides for each dish.

* **Dark / Light Mode Toggle:**
  * Persistent visual theme toggle button in the navbar for seamless dark/light styling.

---

## 📁 Project Structure

```text
smartfridge_project/
│
├── core/                       # Django project configuration
│   ├── __init__.py
│   ├── asgi.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
│
├── pantry/                     # Main pantry & recipe Django app
│   ├── migrations/
│   ├── __init__.py
│   ├── admin.py
│   ├── models.py               # Models: Ingredient, PantryItem, Recipe, RecipeIngredient
│   ├── urls.py
│   └── views.py                # Logic for inventory & recipe matching engine
│
├── static/                     # Static web assets
│   ├── css/
│   │   └── style.css           # Global layout, theme variables & pixel typography
│   └── js/
│       └── main.js             # Theme toggling & UI interactive logic
│
├── templates/                  # HTML Templates
│   ├── base.html               # Base layout template with navbar
│   ├── inventory.html          # "My Fridge" inventory dashboard view
│   └── recipes.html            # "What Can I Cook?" recipe matcher view
│
├── db.sqlite3                  # Local SQLite database
└── manage.py                   # Django CLI executable
```


## 🚀 Setup & Installation
1. Prerequisites
  * Python 3.10+ installed on your machine.

2. Virtual Environment & Setup
```console
# Navigate to project directory
cd smartfridge_project

# Create a virtual environment
python -m venv .venv

# Activate virtual environment
# Windows:
.venv\Scripts\activate
# macOS/Linux:
source .venv/bin/activate
```

3. Install Dependencies & Run Database Migrations
```console
# Install Django
pip install django

# Run migrations
python manage.py migrate
```

4. Create Superuser (Optional)
```console
python manage.py createsuperuser
```

5. Launch Development Server
```console
python manage.py runserver
```
