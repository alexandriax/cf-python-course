import pickle 

def calc_difficulty(cooking_time, num_ingredients):

    if cooking_time < 10 and num_ingredients < 4:
        return "easy"
    elif cooking_time < 10 and num_ingredients >= 4:
        return "medium"
    elif cooking_time >= 10 and num_ingredients < 4:
        return "intermediate"
    else:
        return "hard"

def take_recipe(): 
    name = input("enter recipe name:")
    cooking_time = int(input("enter cooking time (minutes):"))
    ingredients = input("enter the ingredients separated by commas:").split(",")
    difficulty = calc_difficulty(cooking_time, len(ingredients))
    
    recipe = {
        "name": name,
        "cooking_time": cooking_time,
        "ingredients": ingredients,
        "difficulty": difficulty
    }

    return recipe

filename = input("enter filename to store recipes:")

try:
    with open(filename, "rb") as file:
        data = pickle.load(file)
    print("data loaded")
except FileNotFoundError:
    print("file not found, creating a new one")
    data = {"recipes_list": [], "all_ingredients": []}
except Exception as e:
    print("an error occurred:", e)
    data = {"recipes_list": [], "all_ingredients": []}

n = int(input("how many recipes would you like to enter?"))

for _ in range(n):
    recipe = take_recipe()
    data['recipes_list'].append(recipe)
    for ingredient in recipe['ingredients']:
        if ingredient not in data['all_ingredients']:
            data['all_ingredients'].append(ingredient)

with open(filename, "wb") as file:
    pickle.dump(data, file)
print("recipes saved")

    