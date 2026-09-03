# FINISHED

from django.db import models
from django.contrib.auth.models import User
from datetime import date


class Ingredient(models.Model):
    CATEGORY_CHOICES = [
        ('produce', 'Produce'),
        ('dairy', 'Dairy & Eggs'),
        ('meat', 'Meat & Seafood'),
        ('pantry', 'Pantry Essentials'),
        ('beverage', 'Beverages'),
    ]
    name = models.CharField(max_length=100, unique=True)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='pantry')
    default_shelf_life = models.IntegerField(default=7, help_text="Default shelf life in days")

    def __str__(self):
        return f"{self.name} ({self.get_category_display()})"


class PantryItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='pantry_items')
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    quantity = models.CharField(max_length=50, default="1 unit")
    added_date = models.DateField(auto_now_add=True)
    expiration_date = models.DateField()

    def days_until_expiration(self):
        return (self.expiration_date - date.today()).days

    def is_expiring_soon(self):
        return 0 <= self.days_until_expiration() <= 3

    def is_expired(self):
        return self.days_until_expiration() < 0

    def __str__(self):
        return f"{self.ingredient.name} ({self.user.username})"


class Recipe(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    instructions = models.TextField(blank=True)
    prep_time = models.IntegerField(default=15, help_text="Prep time in minutes")

    def __str__(self):
        return self.title


class RecipeIngredient(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    quantity_required = models.CharField(max_length=50, default="1 unit")

    class Meta:
        unique_together = ('recipe', 'ingredient')

    def __str__(self):
        return f"{self.quantity_required} {self.ingredient.name} for {self.recipe.title}"
