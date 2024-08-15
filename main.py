import requests
from bs4 import BeautifulSoup

class Recipe:
    def __init__(self, name, ingredients, instructions):
        self.name = name
        self.ingredients = ingredients
        self.instructions = instructions

class RecipeFetcher:
    def __init__(self, recipe_url):
        self.recipe_url = recipe_url
        self.page_content = None

    def retrieve_page(self):
        # Set up a session to fetch the web page
        session = requests.Session()
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1'
        }
        # Send a GET request to the URL
        response = session.get(self.recipe_url, headers=headers)
        print(f"Page loaded with status: {response.status_code}")

        # Check if the request was successful
        if response.status_code == 200:
            self.page_content = BeautifulSoup(response.text, 'html.parser')
        else:
            raise Exception("Error loading page.")

    def extract_recipe(self):
        # Locate the recipe title
        title_tag = self.page_content.find('h1', class_='article-heading type--lion')
        if not title_tag:
            raise Exception("Recipe title not found.")
        
        recipe_name = title_tag.get_text().strip()

        # Retrieve ingredients
        ingredient_list = []
        ingredients_section = self.page_content.find('ul', class_='mm-recipes-structured-ingredients__list')
        if not ingredients_section:
            raise Exception("Ingredients not found.")

        ingredient_items = ingredients_section.find_all('li', class_='mm-recipes-structured-ingredients__list-item')
        for item in ingredient_items:
            amount = item.find('span', attrs={"data-ingredient-quantity": "true"}).get_text(strip=True)
            measurement = item.find('span', attrs={"data-ingredient-unit": "true"}).get_text(strip=True)
            ingredient_name = item.find('span', attrs={"data-ingredient-name": "true"}).get_text(strip=True)
            
            # Combine all parts into one string
            full_ingredient = f"{amount} {measurement} {ingredient_name}".strip()
            ingredient_list.append(full_ingredient)

        # Retrieve cooking steps
        step_list = []
        steps_section = self.page_content.find('ol', id='mntl-sc-block_1-0')
        if not steps_section:
            raise Exception("Recipe steps not found.")

        step_items = steps_section.find_all('li')
        for step in step_items:
            step_description = step.find('p').get_text(strip=True)
            step_list.append(step_description)

        return Recipe(recipe_name, ingredient_list, step_list)

    def get_recipe(self):
        # Fetch and extract recipe details
        self.retrieve_page()
        return self.extract_recipe()

import webbrowser

# class CookingAssistant:
#     def __init__(self, recipe):
#         self.recipe = recipe
#         self.current_instruction = 0

#     def start(self):
#         print(f"Welcome! Today we'll prepare '{self.recipe.name}' together.")

#         while True:
#             # Present options to the user
#             print("\nWhat would you like to do?")
#             print("1. View ingredients")
#             print("2. Follow cooking instructions")
#             print("3. Exit")
#             choice = input("Type your choice (ingredients/steps/exit) or else you can type what you want to search for! : ").strip().lower()

#             if choice == 'ingredients':
#                 self.show_ingredients()
#             elif choice == 'steps':
#                 self.navigate_steps()
#             elif choice == 'exit':
#                 print("Goodbye, and happy cooking!")
#                 break
#             else:
#                 # Search online if the input doesn't match available options
#                 self.search_online(choice)

#     def show_ingredients(self):
#         # Display the list of ingredients
#         print("\nHere's what you'll need:")
#         for ingredient in self.recipe.ingredients:
#             print(ingredient)

#     def navigate_steps(self):
#         while True:
#             # Provide options to navigate through cooking steps
#             print("\nWhat next?")
#             print("1. Current instruction")
#             print("2. Next step")
#             print("3. Previous step")
#             print("4. Back to main menu")
#             action = input("Type your choice (current/next/previous/back): ").strip().lower()

#             if action == 'current':
#                 self.display_current_instruction()
#             elif action == 'next':
#                 self.next_instruction()
#             elif action == 'previous':
#                 self.previous_instruction()
#             elif action == 'back':
#                 break
#             else:
#                 self.search_online(action)

#     def display_current_instruction(self):
#         # Show the current step in the recipe
#         if 0 <= self.current_instruction < len(self.recipe.instructions):
#             print(f"Step {self.current_instruction + 1}: {self.recipe.instructions[self.current_instruction]}")
#         else:
#             print("No more steps available.")

#     def next_instruction(self):
#         # Move to the next step in the recipe
#         if self.current_instruction < len(self.recipe.instructions) - 1:
#             self.current_instruction += 1
#             self.display_current_instruction()
#         else:
#             print("You're at the final step.")

#     def previous_instruction(self):
#         # Move to the previous step in the recipe
#         if self.current_instruction > 0:
#             self.current_instruction -= 1
#             self.display_current_instruction()
#         else:
#             print("You're at the first step.")

#     def search_online(self, query):
#         # Search for additional information or videos related to the query on YouTube
#         search_query = query.replace(' ', '+')
#         url = f"https://www.youtube.com/results?search_query={search_query}"
#         print(f"Searching for '{query}' on YouTube...")
#         print(url)
#         #webbrowser.open(url)

import webbrowser

class CookingAssistant:
    def __init__(self, recipe):
        self.recipe = recipe
        self.current_instruction = 0

    def start(self):
        print(f"\n🍽️ Welcome to the cooking assistant for '{self.recipe.name}'! 🍽️\n")
        print("Let's get started with your recipe!")

        while True:
            print("\n📋 What would you like to do?")
            print("1. View ingredients")
            print("2. Follow cooking instructions")
            print("3. Exit")
            choice = input("Enter your choice (ingredients/steps/exit) or search for something else: ").strip().lower()

            if choice == 'ingredients':
                self.show_ingredients()
            elif choice == 'steps':
                self.navigate_steps()
            elif choice == 'exit':
                print("👋 Goodbye, and happy cooking!")
                break
            else:
                self.search_online(choice)

    def show_ingredients(self):
        print("\n🛒 Here's what you'll need:")
        for ingredient in self.recipe.ingredients:
            print(f"  - {ingredient}")

    def navigate_steps(self):
        while True:
            print("\n🔄 What do you want to do next?")
            print("1. Show current instruction")
            print("2. Go to next step")
            print("3. Go back one step")
            print("4. Return to main menu")
            action = input("Choose an action (current/next/previous/back) or type something to search on YouTube: ").strip().lower()

            if action == 'current':
                self.display_current_instruction()
            elif action == 'next':
                self.next_instruction()
            elif action == 'previous':
                self.previous_instruction()
            elif action == 'back':
                break
            else:
                self.search_online(action)

    def display_current_instruction(self):
        if 0 <= self.current_instruction < len(self.recipe.instructions):
            print(f"\n🔢 Step {self.current_instruction + 1}:")
            print(f"  {self.recipe.instructions[self.current_instruction]}")
        else:
            print("No more steps available.")

    def next_instruction(self):
        if self.current_instruction < len(self.recipe.instructions) - 1:
            self.current_instruction += 1
            self.display_current_instruction()
        else:
            print("You're already at the final step.")

    def previous_instruction(self):
        if self.current_instruction > 0:
            self.current_instruction -= 1
            self.display_current_instruction()
        else:
            print("You're already at the first step.")

    def search_online(self, query):
        search_query = query.replace(' ', '+')
        url = f"https://www.youtube.com/results?search_query={search_query}"
        print(f"\n🔍 Searching for '{query}' on YouTube...")
        print(f"📺 {url}")
        # Uncomment the following line to open the search in a browser
        # webbrowser.open(url)


def main():
    # Entry point of the program
    url = input("Enter the recipe URL: ")
    parser = RecipeFetcher(url)
    recipe = parser.get_recipe()

    assistant = CookingAssistant(recipe)
    assistant.start()

if __name__ == "__main__":
    main()
