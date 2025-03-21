recipes_list = []
ingredients_list = []

def take_recipe():
    name = input("enter recipe name:")
    cooking_time = int(input("enter cooking time (minutes):"))
    ingredients = input("enter the ingredients separated by commas:").split(",")

    recipe = {
        'name': name,
        'cooking_time': cooking_time,
        'ingredients': ingredients
    }

    return recipe

n = int(input("how many recipes would you like to enter?"))

for _ in range(n):
    recipe = take_recipe()

    for ingredient in recipe['ingredients']:
        if ingredient not in ingredients_list:
            ingredients_list.append(ingredient)

    recipes_list.append(recipe)

for recipe in recipes_list:
    cooking_time = recipe['cooking_time']
    num_ingredients = len(recipe['ingredients'])

    if cooking_time < 10 and num_ingredients < 4:
        difficulty = "easy"
    elif cooking_time < 10 and num_ingredients >= 4:
        difficulty = "medium"
    elif cooking_time >= 10 and num_ingredients < 4:
        difficulty = "intermediate"
    else:
        difficulty = "hard"

    recipe["difficulty"] = difficulty

    print("\nRecipe:", recipe['name'])
    print("cooking time (min):", recipe['cooking_time'])
    print("ingredients:")
    for ingredient in recipe['ingredients']:
        print(ingredient)
    print("difficulty level:", recipe['difficulty'])
        

recipes_list = [
    {'name': 'pasta', 'cooking_time': 15, 'ingredients': ['tomato', 'garlic', 'olive oil', 'basil']},
    {'name': 'salad', 'cooking_time': 5, 'ingredients': ['tomato', 'lettuce', 'olive oil', 'balsamic vinegar']},
    {'name': 'omelette', 'cooking_time': 10, 'ingredients': ['eggs', 'cheese', 'salt', 'pepper']},
]

ingredients_list.sort()

print("\n ---- ingredients available across all recipes ----")
for ingredient in ingredients_list:
    print(ingredient)
