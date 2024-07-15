import json
import random
import os
from math import floor, ceil

# Class to represent a character
class Character:
    # Initialize the character with default values
    def __init__(self):
        self.name = ""
        self.kindred = ""
        self.level = 0
        self.character_type = ""
        self.gender = ""
        self.height = 0
        self.weight = 0
        self.age = 0
        self.hair = ""
        self.money = 0
        self.wt_possible = 0
        self.original_attributes = {}
        self.attributes = {
            "STR": 0,
            "CON": 0,
            "DEX": 0,
            "SPD": 0,
            "LK": 0,
            "IQ": 0,
            "WIZ": 0,
            "CHA": 0
        }
        self.triples = []
        self.combat_adds = 0
        self.modifiers = {}
        self.notes = ""

    # Roll a specified number of dice with a given number of sides
    def roll_dice(self, number_of_dice, sides):
        return [random.randint(1, sides) for _ in range(number_of_dice)]

    # Generate the character's attributes
    def generate_attributes(self):
        for attr in self.attributes:
            self.attributes[attr] = self.roll_and_check_triples(attr)
        self.original_attributes = self.attributes.copy()

    # Roll dice and check for triples (three identical rolls)
    def roll_and_check_triples(self, attr):
        rolls = self.roll_dice(3, 6)
        total = sum(rolls)
        while len(set(rolls)) == 1:  # While all three rolls are the same
            self.triples.append(attr)  # Append attribute name instead of total
            rolls = self.roll_dice(3, 6)
            total += sum(rolls)
        return max(total, 7)  # Ensuring the value is at least 7

    # Calculate combat adds based on specific attributes
    def calculate_combat_adds(self):
        self.combat_adds = 0
        for attr in ["STR", "LK", "DEX", "SPD"]:
            if self.attributes[attr] > 12:
                self.combat_adds += self.attributes[attr] - 12

    # Calculate the character's money
    def calculate_money(self):
        self.money = sum(self.roll_dice(3, 6)) * 10

    # Calculate the character's weight carrying capacity
    def calculate_wt_possible(self):
        self.wt_possible = self.attributes["STR"] * 100

    # Calculate the character's level
    def calculate_level(self):
        prime_attributes = ["STR", "CON", "DEX", "SPD", "LK", "IQ", "WIZ", "CHA"]  # Prime attributes for level calculation
        highest_prime = max(self.attributes[attr] for attr in prime_attributes)
        self.level = floor(highest_prime / 10)

    # Apply modifiers based on the character's kindred
    def apply_kindred_modifiers(self):
        print(f"Applying kindred modifiers for: {self.kindred}")
        print(f"Original attributes: {self.attributes}")
        for attr in self.attributes:
            base_value = self.attributes[attr]
            modified_value = ceil(base_value * self.modifiers.get(attr, 1))
            print(f"{attr}: {base_value} -> {modified_value} (modifier: {self.modifiers.get(attr, 1)})")
            self.attributes[attr] = modified_value
        self.display_attributes()  # Display modified attributes for debugging

    # Load kindred-specific modifiers from a file
    def load_kindred_modifiers(self):
        base_dir = os.path.dirname(os.path.abspath(__file__))
        kindred_file_map = {
            "Dwarf Midgardian": "dwarf_midgardian_modifiers.json",
            "Dwarf Gristlegrim": "dwarf_gristlegrim_modifiers.json",
            "Human": "human_modifiers.json",
            "Elf": "elf_modifiers.json",
            "Fairie": "fairie_modifiers.json",
            "Leprechaun": "leprechaun_modifiers.json",
            "Hobb": "hobb_modifiers.json"
        }
        kindred_file = kindred_file_map.get(self.kindred, "default_modifiers.json")
        kindred_file_path = os.path.join(base_dir, 'data', kindred_file)
        try:
            with open(kindred_file_path, 'r') as file:
                self.modifiers = json.load(file)
                print(f"Loaded modifiers for {self.kindred}: {self.modifiers}")
        except FileNotFoundError:
            print(f"No modifiers file found for {self.kindred}. Using default modifiers.")
            self.modifiers = {attr: 1 for attr in self.attributes}
            self.modifiers.update({"Height": 1, "Weight": 1})

    # Load specialist notes based on enhanced attributes
    def load_specialist_notes(self):
        base_dir = os.path.dirname(os.path.abspath(__file__))
        notes_file_path = os.path.join(base_dir, 'data', 'specialists_notes.json')
        try:
            with open(notes_file_path, 'r') as file:
                notes_data = json.load(file)
                self.notes = "\n".join(f"{attr}: {notes_data[attr]}" for attr in self.triples if attr in notes_data)
        except FileNotFoundError:
            print("No specialist notes file found.")
            self.notes = ""

    # Display the character's attributes
    def display_attributes(self):
        print("ENTER Q AT ANY TIME TO QUIT\n")
        print("Initial Attribute Rolls\n")
        for attr, value in self.attributes.items():
            asterisk = "*" if attr in self.triples else ""
            print(f"{attr}: {value}{asterisk}")
        if self.triples:
            print("Specialist attributes enhanced for:", ", ".join(str(attr) for attr in self.triples))
        print(f"Combat ADDS: {self.combat_adds}\n")

    # Prompt the user to enter character details
    def prompt_for_details(self):
        self.kindred = self.select_option("\nSelect Kindred\n", ["Human", "Dwarf Midgardian", "Dwarf Gristlegrim", "Elf", "Fairie", "Leprechaun", "Hobb\n"])
        print("\n")
        self.load_kindred_modifiers()
        self.character_type = self.select_option("\nSelect Character Type\n", ["Warrior", "Wizard", "Rogue\n"])
        self.gender = self.select_option("\nSelect Gender\n", ["M", "F\n"])
        self.height = self.prompt_input("\nEnter Height (in inches): ", int)
        self.weight = self.prompt_input("\nEnter Weight (in pounds): ", int)
        self.age = self.prompt_input("\nEnter Age: ", int)
        self.hair = self.prompt_input("\nEnter Hair: ")
        self.name = self.prompt_input("\nEnter your character's name: ")

    # Helper function to display options and get user choice
    def select_option(self, prompt, options):
        while True:
            print(prompt)
            for i, option in enumerate(options, 1):
                print(f"{i}. {option}")
            choice = input("Enter the number of your choice: ").strip().upper()
            if choice == "Q":
                print("Program quit by user.")
                exit()
            if choice.isdigit() and 1 <= int(choice) <= len(options):
                return options[int(choice) - 1]
            print("Invalid choice. Please try again.")

    # Helper function to prompt for user input and convert to the correct type
    def prompt_input(self, prompt, input_type=str):
        while True:
            value = input(prompt).strip().upper()
            if value == "Q":
                print("Program quit by user.")
                exit()
            try:
                return input_type(value)
            except ValueError:
                print("Invalid input. Please try again.")

    # Save character data to a file
    def save_to_file(self, filename):
        with open(filename, 'w') as file:
            json.dump(self.__dict__, file)

    # Load character data from a file
    @classmethod
    def load_from_file(cls, filename):
        with open(filename, 'r') as file:
            data = json.load(file)
            character = cls()
            character.__dict__.update(data)
            return character

    # Display all character information
    def display_all_information(self):
        # define the ASCII characters to use for the character card
        top_left = '╔'
        top_right = '╗'
        bottom_left = '╚'
        bottom_right = '╝'
        horizontal = '═'
        vertical = '║'
        print("\n")
        print(top_left + horizontal * 48 + top_right) # print the top of the character card
        print(f"║ Name: {self.name}")
        print(f"║ Kindred: {self.kindred} Level: {self.level}")
        print(f"║ Character Type: {self.character_type}")
        print(f"║ Gender: {self.gender} Height: {self.height} inches Weight: {self.weight} pounds")
        print(f"║ Age: {self.age} Hair: {self.hair} Money: {self.money} GP")
        print(f"║ Wt. Possible: {self.wt_possible} Weight Units / {self.wt_possible/10} Pounds")
        for attr, value in self.attributes.items():
            original_value = self.original_attributes[attr]
            asterisk = "*" if attr in self.triples else ""
            print(f"║ {attr}: [{original_value}] -> {value}{asterisk}")
        if self.triples:
            print("\n║ Specialist attributes enhanced for:", ", ".join(str(attr) for attr in self.triples))
        print(f"║ Combat ADDS: {self.combat_adds}")
        if self.notes:
            print("\n║ Specialist Notes:")
            print(self.notes)

# Clear the screen
def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

# Main function to drive the character creation process
def main():
    while True:
        clear_screen()
        character = Character()
        character.generate_attributes()
        character.calculate_combat_adds()  # Calculate the initial Combat ADDS before applying modifiers
        character.calculate_money()
        character.display_attributes()  # Display initial attributes before any adjustments

        while True:
            keep_attributes = input("Do you want to keep these attributes (Y/N)? ").strip().upper()
            if keep_attributes == "Q":
                print("Program quit by user.")
                return
            if keep_attributes in ["Y", "N"]:
                break
            print("Invalid choice. Please enter Y or N.")

        if keep_attributes == "Y":
            break

    character.prompt_for_details()
    character.apply_kindred_modifiers()
    character.calculate_combat_adds()  # Recalculate Combat ADDS after applying modifiers
    character.calculate_wt_possible()  # Calculate Wt. Possible after applying modifiers
    character.calculate_level()  # Calculate level after applying modifiers
    character.load_specialist_notes()  # Load notes based on specialist attributes
    clear_screen()
    character.display_all_information()

    # Ask if the user wants to roll another character
    while True:
        roll_another = input("\nDo you want to roll another character? (Y/N): ").strip().upper()
        if roll_another == "Q":
            print("Program quit by user.")
            return
        if roll_another in ["Y", "N"]:
            break
        print("Invalid choice. Please enter Y or N.")
    
    if roll_another == "Y":
        main()  # Restart the main function
    else:
        print("\nThank you for using the character generator!\n")
        return

if __name__ == "__main__":
    main()
