# Talking_Interactive_Cookbook

## Overview

The Talking Interactive Cookbook is a terminal-based application that helps users access and interact with recipes. It can fetch recipe details from a given URL and guide users through ingredients and cooking steps. Users can also search for additional information on YouTube.

## Features

- **Fetch Recipe**: Retrieves recipe details from a URL.
- **View Ingredients**: Displays the list of ingredients.
- **Follow Cooking Steps**: Navigates through the cooking instructions.
- **YouTube Search**: Searches YouTube for any user input not matching predefined actions.

## Usage

1. **Run the Application**:

   ```bash
   python main.py
   ```

2. **Enter the Recipe URL**: Provide the URL of the recipe when prompted.

3. **Interact**:
   - Type `ingredients` to view the ingredient list.
   - Type `steps` to follow the cooking instructions.
   - Type `exit` to quit the application.
   - Type any other text to search on YouTube.

## Requirements

- `requests`
- `beautifulsoup4`

Install dependencies using:

```bash
pip install requests beautifulsoup4
```
