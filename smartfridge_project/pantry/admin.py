from django.contrib import admin
from .models import Ingredient, PantryItem, Recipe, RecipeIngredient

admin.site.register(Ingredient)
admin.site.register(PantryItem)


class RecipeIngredientInline(admin.TabularInline):
    model = RecipeIngredient
    extra = 1


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    inlines = [RecipeIngredientInline]
