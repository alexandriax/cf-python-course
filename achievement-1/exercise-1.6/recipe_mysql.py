import mysql.connector
database = mysql.connector.connect(host="localhost", user="cf-python", passwd="NewPassword123")
conn = mysql.connector.connect(host='localhost', user='cf-python', passwd='NewPassword123')
cursor = conn.cursor()
cursor.execute("CREATE DATABASE IF NOT EXISTS task_database")
cursor.execute("USE task_database")
cursor.execute("CREATE TABLE IF NOT EXISTS Recipes ( id INT AUTO_INCREMENT PRIMARY KEY, name VARCHAR(50), ingredients VARCHAR(255), cooking_time INT, difficulty VARCHAR(20))")

def calculate_difficulty(cooking_time, ingredients):
      if cooking_time < 10 and len(ingredients) < 4:
          return "easy"
      elif cooking_time < 10 and len(ingredients) >= 4:
          return "medium"
      elif cooking_time >= 10 and len(ingredients) < 4:
          return "intermediate"
      else:
          return "hard"
def create_recipe():
      name = input("enter recipe name: ")
      cooking_time = int(input("enter cooking time in minutes: "))
      ingredients = input("enter ingredients separated by a comma: ").split(",")
      difficulty = calculate_difficulty(cooking_time, ingredients)
      ingredients_str = ", ".join(ingredients)
      cursor.execute("INSERT INTO Recipes (name, ingredients, cooking_time, difficulty) VALUES (%s, %s, %s, %s)", (name, ingredients_str, cooking_time, difficulty))
      conn.commit()
      print("recipe added successfully!")
def search_recipe():
      cursor.execute("SELECT ingredients FROM Recipes")
      results = cursor.fetchall()
      all_ingredients = set()
      for row in results:
          ingredient_list = row[0].split(", ")
          all_ingredients.update(ingredient_list)
      print("\navailable ingredients:")
      all_ingredients = list(all_ingredients)
      for i, ingredient in enumerate(all_ingredients, 1):
          print(f"{i}. {ingredient}")
      choice = int(input("\nenter number of ingredient you want to search for: ")) - 1
      search_ingredient = all_ingredients[choice]
      cursor.execute("SELECT * FROM Recipes WHERE ingredients LIKE %s", (f"%{search_ingredient}%",))
      recipes = cursor.fetchall()
      if recipes:
          print("\nrecipes found:")
          for recipe in recipes:
              print(f"{recipe[0]}. {recipe[1]} - {recipe[2]} (cooking time: {recipe[3]} min, difficulty: {recipe[4]})")
      else:
          print("\nno recipes found with that ingredient")
def update_recipe():
      cursor.execute("SELECT * FROM Recipes")
      recipes = cursor.fetchall()
      if not recipes:
          print("no recipes found")
          return
      print("\navailable recipes:")
      for recipe in recipes:
          print(f"{recipe[0]}. {recipe[1]} - {recipe[2]} (cooking time: {recipe[3]} min, difficulty: {recipe[4]})")
      recipe_id = int(input("\nenter the ID of the recipe you want to update: "))
      print("\nwhat would you like to update?")
      print("1. name")
      print("2. cooking time")
      print("3. ingredients")
      choice = int(input("enter your choice: "))
      if choice == 1:
          new_value = input("enter new name: ")
          cursor.execute("UPDATE Recipes SET name = %s WHERE id = %s", (new_value, recipe_id))
      elif choice == 2:
          new_value = int(input("enter new cooking time: "))
          cursor.execute("UPDATE Recipes SET cooking_time = %s WHERE id = %s", (new_value, recipe_id))
          cursor.execute("SELECT ingredients FROM Recipes WHERE id = %s", (recipe_id,))
          ingredients = cursor.fetchone()[0].split(", ")
          new_difficulty = calculate_difficulty(new_value, ingredients)
          cursor.execute("UPDATE Recipes SET difficulty = %s WHERE id = %s", (new_difficulty, recipe_id))
      elif choice == 3:
          new_value = input("enter new ingredients: ").split(", ")
          new_ingredients_str = ", ".join(new_value)
          cursor.execute("UPDATE Recipes SET ingredients = %s WHERE id = %s", (new_ingredients_str, recipe_id))
          cursor.execute("SELECT cooking_time FROM Recipes WHERE id = %s", (recipe_id,))
          cooking_time = cursor.fetchone()[0]
          new_difficulty = calculate_difficulty(cooking_time, new_value)
          cursor.execute("UPDATE Recipes SET difficulty = %s WHERE id = %s", (new_difficulty, recipe_id))
      else:
          print("invalid choice")
      conn.commit()
      print("recipe updated successfully!")
def delete_recipe():
      cursor.execute("SELECT * FROM Recipes")
      recipes = cursor.fetchall()
      if not recipes:
          print("no recipes found")
          return
      print("\navailable recipes:")
      for recipe in recipes:
          print(f"{recipe[0]}. {recipe[1]} - {recipe[2]} (cooking time: {recipe[3]} min, difficulty: {recipe[4]})")
      recipe_id = int(input("\nenter id of recipe to delete: "))
      cursor.execute("DELETE FROM Recipes WHERE id = %s", (recipe_id,))
      conn.commit()
      print("recipe deleted!")
def main_menu():
        while True: 
            print("\nrecipe manager")
            print("1. create a new recipe")
            print("2. search for a recipe by ingredient")
            print("3. update a recipe")
            print("4. delete a recipe")
            print("type 'quit' to exit")
            choice = input("\nenter your choice: ")
            if choice == "1":
                create_recipe()
            elif choice == "2":
                search_recipe()
            elif choice == "3":
                update_recipe()
            elif choice == "4":
                delete_recipe()
            elif choice.lower() == "quit":
                print("goodbye!")
                conn.commit()
                cursor.close()
                conn.close()
                break
            else:
                print("invalid choice, please enter a number between 1-4")
if __name__ == "__main__":
    main_menu()

