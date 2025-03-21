class Recipe: 
    all_ingredients = set()

    def __init__(self, name):
        self.name = name
        self.ingredients = []
        self.cooking_time = None
        self.difficulty = None

    def get_name(self):
        return self.name

    def set_name(self, new_name):
        self.name = new_name

    def get_cooking_time(self):
        return self.cooking_time

    def set_cooking_time(self, time):
        self.cooking_time = time
        self.calculate_difficulty()

    def add_ingredients(self, *ingredients):
        for ingredient in ingredients:
            self.ingredients.append(ingredient)
        self.update_all_ingredients()
        self.calculate_difficulty

    def get_ingredients(self):
        return self.ingredients

    def calculate_difficulty(self): 
        num_ingredients = len(self.ingredients)

        if self.cooking_time is None or num_ingredients == 0:
            self.difficulty = None
            return
        if self.cooking_time < 10 and num_ingredients < 4:
            self.difficulty = "easy"
        elif self.cooking_time < 10 and num_ingredients >= 4:
            self.difficulty = "medium"
        elif self.cooking_time >= 10 and num_ingredients < 4:
            self.difficulty = "intermediate"
        else:
            self.difficulty = "hard"

    def get_difficulty(self):
        if self.difficulty is None:
            self.calculate_difficulty()
        return self.difficulty 

    def search_ingredient(self, ingredient):
        return ingredient in self.ingredients
    def update_all_ingredients(self):
        for ingredient in self.ingredients:
            Recipe.all_ingredients.add(ingredient)
    def __str__(self):
        return "recipe: " + self.name + "\n" + \
               "cooking time: " + str(self.cooking_time) + " minutes\n" + \
                "ingredients: " + ",".join(self.ingredients) + "\n" + \
                "difficulty: " + self.difficulty + "\n"

def recipe_search(data, search_term): 
    print("\nsearching for recipes with: " + search_term)

    found = False
    for recipe in data:
        if recipe.search_ingredient(search_term):
            print(recipe)
            found = True
    if not found: 
        print("no recipes found with that ingredient")

tea = Recipe("tea")
tea.add_ingredients("tea leaves", "sugar", "water")
tea.set_cooking_time(5)
print(tea)

coffee = Recipe("coffee")
coffee.add_ingredients("coffee powder", "sugar", "water")
coffee.set_cooking_time(5)
print(coffee)

cake = Recipe("cake")
cake.add_ingredients("sugar", "butter", "eggs", "vanilla essence", "flour", "baking powder", "milk")
cake.set_cooking_time(50)
print(cake)

banana_smoothie = Recipe("banana smoothie")
banana_smoothie.add_ingredients("bananas", "milk", "peanut butter", "sugar", "ice cubes")
banana_smoothie.set_cooking_time(5)
print(cake)

recipes_list = [tea, coffee, cake, banana_smoothie]

recipe_search(recipes_list, "water")
recipe_search(recipes_list, "sugar")
recipe_search(recipes_list, "bananas")

print("\nall ingredients across recipes:", Recipe.all_ingredients)

