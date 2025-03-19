from sqlalchemy import create_engine, Column, or_
from sqlalchemy.types import Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

engine = create_engine("mysql://cf-python:NewPassword123@localhost/task_database")
Session = sessionmaker(bind=engine)
session = Session()
Base = declarative_base()

class Recipe(Base):
    __tablename__ = "final_recipes"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50))
    ingredients = Column(String(255))
    cooking_time = Column(Integer)
    difficulty = Column(String(20))

    def __repr__(self):
        return "<Recipe: " + str(self.id) + "-" + self.name + self.difficulty + ">"

    def __str__(self):
        return "\n================================\n" + \
            "recipe number " + str(self.id) + "\n" + \
            "name: " + self.name + "\n" + \
            "ingredients: " + self.ingredients + "\n" + \
            "cooking time: " + str(self.cooking_time) + " minutes\n" + \
            "difficulty: " + self.difficulty + "\n" + \
            "================================\n"

    def calculate_difficulty(self):
        num_ingredients = len(self.return_ingredients_as_list())
        if self.cooking_time < 10 and num_ingredients < 4:
            self.difficulty = "easy"
        elif self.cooking_time < 10 and num_ingredients >= 4:
            self.difficulty = "medium"
        elif self.cooking_time >=10 and num_ingredients < 4:
            self.difficulty = "intermediate"
        else:
            self.difficulty = "hard"

    def return_ingredients_as_list(self):
        if not self.ingredients:
            return []
        return self.ingredients.split(", ")

Base.metadata.create_all(engine)

# create recipe

def create_recipe():
    name = input("enter recipe name (max 50 characters): ")
    if len(name) > 50:
        print("recipe name is too long, try again")
        return

    ingredients = input("enter ingredients separated by commas: "). strip()
    if not ingredients: 
        print("you must enter at least one ingredient")
        return
    
    ingredients_list = ingredients.split(", ")
    num_ingredients = len(ingredients_list)

    cooking_time = input("enter cooking time in minutes: ")
    if not cooking_time.isdigit():
        print("must be a number")
        return

    recipe_entry = Recipe(name=name, ingredients=ingredients, cooking_time=int(cooking_time), difficulty="")
    recipe_entry.calculate_difficulty()

    session.add(recipe_entry)
    session.commit()
    print("recipe added successfully!")

# view all recipes

def view_all_recipes():
    recipes = session.query(Recipe).all()
    if not recipes:
        print("no recipes found")
        return
    for recipe in recipes:
        print(recipe)

# search by ingredients

def search_by_ingredients():
    if session.query(Recipe).count() == 0:
        print("no recipes available")
        return

    all_ingredients = []
    results = session.query(Recipe.ingredients).all()

    for row in results:
        ingredients = row[0].split(", ")
        for ing in ingredients:
            if ing not in all_ingredients:
                all_ingredients.append(ing)

    print("available ingredients:")
    for i in range(len(all_ingredients)):
        print(str(i + 1) + ". " + all_ingredients[i])

    selections = input("select ingredients by number (separate with space): ").split()
    search_ingredients = [all_ingredients[int(i) - 1] for i in selections if i.isdigit() and 1 <= int(i) <= len(all_ingredients)]

    conditions = [Recipe.ingredients.like("%" + ingredient + "%") for ingredient in search_ingredients]
    recipes = session.query(Recipe).filter(or_(*conditions)).all()

    if not recipes:
        for recipe in recipes:
            print(recipe)
        else:
            print("no recipes found with those ingredients")

# edit recipe

def edit_recipe():
    recipes = session.query(Recipe.id, Recipe.name).all()
    if not recipes:
        print("no recipes available")
        return

    for id, name in recipes:
        print(str(id) + ". " + name)

    recipe_id = input("enter the ID of the recipe to edit: ")
    if not recipe_id.isdigit():
        print("invalid")
        return

    recipe_to_edit = session.query(Recipe).get(int(recipe_id))
    if not recipe_to_edit:
        print("recipe not found")
        return

    print("1. edit name\n2. edit ingredients\n3. edit cooking time")
    choice = input("select something to edit: ")

    if choice == "1":
        new_name = input("enter new name: ")
        if len(new_name) > 50:
            print("name too long")
            return
        recipe_to_edit.name = new_name

    elif choice == "2":
        new_ingredients = input("enter new ingredients separated by commas: ")
        recipe_to_edit.ingredients = new_ingredients

    elif choice == "3":
        new_cooking_time = input("enter new cooking time: ")
        if not new_cooking_time.isdigit():
            print("invalid number")
            return
        recipe_to_edit.cooking_time = int(new_cooking_time)

    else: 
        print("invalid choice")
        return

    recipe_to_edit.calculate_difficulty()
    session.commit()
    print("recipe updated!")

# delete recipe

def delete_recipe():
    recipes = session.query(Recipe.id, Recipe.name).all()
    if not recipes:
        print("no recipes available")
        return
    
    for id, name in recipes:
        print(str(id) + ". " + name)

    recipe_id = input("enter the ID of the recipe to delete: ")
    if not recipe_id.isdigit():
        print("invalid input")
        return

    recipe_to_delete = session.query(Recipe).get(int(recipe_id))
    if not recipe_to_delete:
        print("recipe not found")
        return

    confirm = input("are you sure you want to delete " + recipe_to_delete.name + "? (yes/no): ")
    if confirm.lower() == "yes": 
        session.delete(recipe_to_delete)
        session.commit()
        print("recipe deleted!")

# main menu

def main(): 
    while True:
        print("\nrecipe app menu:")
        print("1. create a new recipe")
        print("2. view all recipes")
        print("3. search recipes by ingredients")
        print("4. edit a recipe")
        print("5. delete a recipe")
        print("type 'quit' to exit")

        choice = input("enter your choice: ")

        if choice == "1":
            create_recipe()
        elif choice == "2": 
            view_all_recipes()
        elif choice == "3":
            search_by_ingredients()
        elif choice == "4":
            edit_recipe()
        elif choice == "5":
            delete_recipe()
        elif choice.lower() == "quit":
            session.close()
            engine.dispose()
            print("goodbye!")
            break
        else:
            print("invalid choice")
if __name__ == "__main__":
    main()
