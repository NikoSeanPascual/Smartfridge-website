import json
from datetime import date, timedelta
from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from .models import PantryItem, Ingredient, Recipe


@login_required(login_url='/admin/login/')
def inventory_view(request):
    items = PantryItem.objects.filter(user=request.user).select_related('ingredient').order_by('expiration_date')
    ingredients = Ingredient.objects.all().order_by('name')
    return render(request, 'pantry/inventory.html', {
        'items': items,
        'ingredients': ingredients
    })


@login_required(login_url='/admin/login/')
@require_POST
def add_item_api(request):
    try:
        data = json.loads(request.body)
        ingredient_name = data.get('ingredient_name', '').strip()
        quantity = data.get('quantity', '1 unit').strip() or '1 unit'

        if not ingredient_name:
            return JsonResponse({'status': 'error', 'message': 'Ingredient name is required'}, status=400)

        # Get the ingredient, or create it if it's completely new!
        ingredient, created = Ingredient.objects.get_or_create(
            name__iexact=ingredient_name,
            defaults={
                'name': ingredient_name.title(),
                'category': 'pantry',
                'default_shelf_life': 7
            }
        )

        exp_date = date.today() + timedelta(days=ingredient.default_shelf_life)

        item = PantryItem.objects.create(
            user=request.user,
            ingredient=ingredient,
            quantity=quantity,
            expiration_date=exp_date
        )

        return JsonResponse({
            'status': 'success',
            'item_id': item.id,
            'name': ingredient.name,
            'category': ingredient.get_category_display(),
            'quantity': item.quantity,
            'exp_date': exp_date.strftime('%b %d, %Y'),
            'is_expiring_soon': item.is_expiring_soon(),
            'is_expired': item.is_expired()
        })
    except json.JSONDecodeError:
        return JsonResponse({'status': 'error', 'message': 'Invalid data'}, status=400)


@login_required(login_url='/admin/login/')
@require_POST
def delete_item_api(request, item_id):
    try:
        item = PantryItem.objects.get(id=item_id, user=request.user)
        item.delete()
        return JsonResponse({'status': 'success', 'item_id': item_id})
    except PantryItem.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'Item not found'}, status=404)


@login_required(login_url='/admin/login/')
def recipe_matcher_view(request):
    user_pantry_names = set(
        PantryItem.objects.filter(user=request.user)
        .values_list('ingredient__name', flat=True)
    )
    user_pantry_names = {name.lower() for name in user_pantry_names}

    recipes = Recipe.objects.prefetch_related('recipeingredient_set__ingredient')
    matched_recipes = []

    for recipe in recipes:
        recipe_ingredients = recipe.recipeingredient_set.all()
        if not recipe_ingredients:
            continue

        required_names = {ri.ingredient.name.lower() for ri in recipe_ingredients}

        matching_names = user_pantry_names.intersection(required_names)
        match_percentage = int((len(matching_names) / len(required_names)) * 100)

        missing_ingredients = [
            ri.ingredient.name for ri in recipe_ingredients
            if ri.ingredient.name.lower() not in user_pantry_names
        ]

        matched_recipes.append({
            'recipe': recipe,
            'match_percentage': match_percentage,
            'has_count': len(matching_names),
            'total_count': len(required_names),
            'missing_ingredients': missing_ingredients
        })

    matched_recipes.sort(key=lambda x: x['match_percentage'], reverse=True)

    return render(request, 'pantry/recipes.html', {'recipes': matched_recipes})
