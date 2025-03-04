import pickle 

def display_recipe(recipe):
    print("\nrecipe:", recipe['name'])
    print('cooking time:', recipe['cooking_time'], 'minutes')
    print('ingredients:', ','.join(recipe['ingredients']))
    print('difficulty:', recipe['difficulty'])

def search_ingredient(data):
    print('\navailable ingredients:')
    for index, ingredient in enumerate(data['all_ingredients']):
        print(str(index + 1) + '.' + ingredient)

    try:
        choice = int(input('\nenter the number of an ingredient to search for:')) - 1
        ingredient_searched = data['all_ingredients'][choice]
    except (IndexError, ValueError):
        print('invalid entry, please try again')
        return

    print('recipes containing' + ingredient_searched + ':')
    for recipe in data['recipes_list']:
        if ingredient_searched in recipe['ingredients']:
            display_recipe(recipe)

filename = input('enter the filename containing the recipe:')

try:
    with open(filename, 'rb') as file:
        data = pickle.load(file)
    print('success!')
except FileNotFoundError:
    print('file not found, please try again')
except Exception as e:
    print('an error occurred:', e)
else:
    search_ingredient(data)