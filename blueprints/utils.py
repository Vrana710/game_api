# =============================================================================
# Project: Game Api App
# Developer: Varsha Rana
# File: utils.py
# Description:
# The `utils.py` file provides utility functions for the Game API App, primarily
# focused on fetching character data from a local JSON file (`characters.json`).
# It includes a private function `_fetch_character_data` that retrieves character
# details based on the provided character name. This function performs error handling
# for missing environment variables, invalid file paths, and issues during JSON
# parsing. The public function `fetch_character_data` serves as a wrapper to
# access the private function, ensuring proper use and error handling.
#
# Key Features:
# 1. **Character Data Fetching**: The app can fetch character details from a local
#    JSON file (`characters.json`) by matching the character name (case-insensitive).
# 2. **Error Handling**: Implements robust error handling for missing environment
#    variables, nonexistent files, invalid JSON format, and any other runtime errors.
# 3. **Private Function**: The `_fetch_character_data` function is responsible for
#    reading the `characters.json` file and returning character data or error messages.
# 4. **Public Wrapper**: The `fetch_character_data` function acts as a public interface
#    to access the protected `_fetch_character_data` function safely.
# 5. **Environment Variables**: The file loads the path to the `characters.json`
#    file from environment variables, ensuring flexibility and configuration through
#    a `.env` file.
#
# Created: 2024-12-02
# Updated: 2024-12-08
# =============================================================================


import os
import json
from dotenv import load_dotenv

# Load environment variables from the .env file
load_dotenv()

# Fetch the characters.json path from the .env file
CHARACTERS_JSON_PATH = os.getenv('CHARACTERS_JSON_PATH')


def _fetch_character_data(character_name):
    """
    Fetches character data from the local characters.json file using the provided character name.

    Parameters:
    character_name (str): The name of the character to fetch data for.

    Returns:
    dict: A dictionary containing the character data or None if not found.
    """
    try:
        # Check if the path is set
        if not CHARACTERS_JSON_PATH:
            print("Error: CHARACTERS_JSON_PATH is not set in the .env file.")
            return None

        # Check if the file exists
        if not os.path.exists(CHARACTERS_JSON_PATH):
            print(f"Error: The file {CHARACTERS_JSON_PATH} does not exist.")
            return None

        # Open and read the characters.json file
        with open(CHARACTERS_JSON_PATH, 'r') as file:
            characters_data = json.load(file)

        # Look for the character by name (partial match)
        character = next(
            (char for char in characters_data if character_name.lower() in char['name'].lower()),
            None
        )

        if character:
            return character
        else:
            print(f"Character '{character_name}' not found in characters.json.")
            return None
    except json.JSONDecodeError:
        print("Error: Could not parse the JSON data from the characters file.")
    except Exception as e:
        print(f"Error: {e}")

    return None


def fetch_character_data(character_name):
    """
    Public function to fetch character data, using the internal _fetch_character_data function.

    This function is a wrapper that ensures the protected function is accessed
    properly and only through this public interface.

    Parameters:
    character_name (str): The name of the character to fetch data for.

    Returns:
    dict: A dictionary containing the character data or None if not found.
    """
    return _fetch_character_data(character_name)

