import json
import random
import os
from math import floor, ceil

class Character:
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
            "CHAR": 0
        }
        self.triples = []
        self.combat_adds = 0
        self.modifiers = {}

    def roll_dice(self, number_of_dice, sides):
        return [random.randint(1, sides) for _ in range(number_of_dice)]

    def generate_attributes(self):
        for attr in self.attributes:
            self.attributes[attr] = self.roll_and_check_triples(attr)
        self.original_attributes = self.attributes.copy()

    def roll_and_check_triples(self, attr):
        rolls = self.roll_dice(3, 6)
        total = sum(rolls)
        while len(set(rolls)) == 1:  # While all three rolls are the same
            self.triples.append(attr)  # Append attribute name instead of total
            rolls = self.roll_dice(3, 6)
            total += sum(rolls)
        return max(total, 7)  # Ensuring the value is at least 7

    def calculate_combat_adds(self):
        self.combat_adds = 0
        for attr in ["STR", "LK", "DEX", "SPD"]:
            if self.attributes[attr] > 12:
                self.combat_adds += self.attributes[attr] - 12

    def calculate_money(self):
        self.money = sum(self.roll_dice(3, 6)) * 10

    def calculate_wt_possible(self):
        self.wt_possible = self.attributes["STR"] * 100

    def calculate_level(self):
        prime_attributes = ["STR", "DEX", "IQ", "WIZ"]  # Prime attributes for level calculation
        highest_prime = max(self.attributes[attr] for attr in prime_attributes)
        self.level = floor(highest_prime / 10)

    def apply_kindred_modifiers(self):
        for attr in self.attributes:
            base_value = self.attributes[attr]
            if attr in self.triples:
                # Enhance specialist attributes before applying modifiers
                while True:
                    rolls = self.roll_dice(3, 6)
                    base_value += sum(rolls)
                    if len(set(rolls)) != 1:  # Stop if not all rolls are the same
                        break
            self.attributes[attr] = ceil(base_value * self.modifiers.get(attr, 1))
        self.display_attributes()  # Display modified attributes for debugging

    def load_kindred_modifiers(self):
        base_dir = os.path.dirname(os.path.abspath(__file__))
        kindred_file = os.path.join(base_dir, 'data', self.kindred.lower().replace("-", "_") + "_modifiers.json")
        try:
            with open(kindred_file, 'r') as file:
                self.modifiers = json.load(file)
        except FileNotFoundError:
            print(f"No modifiers file found for {self.kindred}. Using default modifiers.")
            self.modifiers = {attr: 1 for attr in self.attributes}
            self.modifiers.update({"Height": 1, "Weight": 1})

    def display_attributes(self):
        print("Initial Attribute Rolls\n")
        for attr, value in self.attributes.items():
            asterisk = "*" if attr in self.triples else ""
            print(f"{attr}: {value}{asterisk}")
        if self.triples:
            print("Specialist attributes enhanced for:", ", ".join(str(attr) for attr in self.triples))
        print(f"Combat ADDS: {self.combat_adds}\n")

    def prompt_for_details(self):
        self.kindred = self.select_option("Select Kindred", ["Human", "Midgardian Dwarf", "Gristlegrim Dwarf", "Elf", "Fairie", "Leprechaun", "Hobb"])
        self.load_kindred_modifiers()
        self.character_type = self.select_option("Select Character Type", ["Warrior", "Wizard", "Rogue"])
        self.gender = self.select_option("Select Gender", ["M", "F"])
        self.height = self.prompt_input("Enter Height (in inches): ", int)
        self.weight = self.prompt_input("Enter Weight (in pounds): ", int)
        self.age = self.prompt_input("Enter Age: ", int)
        self.hair = self.prompt_input("Enter Hair: ")

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

    def save_to_file(self, filename):
        with open(filename, 'w') as file:
            json.dump(self.__dict__, file)

    @classmethod
    def load_from_file(cls, filename):
        with open(filename, 'r') as file:
            data = json.load(file)
            character = cls()
            character.__dict__.update(data)
            return character

    def display_all_information(self):
        print(f"Name: {self.name}")
        print(f"Kindred: {self.kindred} Level: {self.level}")
        print(f"Character Type: {self.character_type}")
        print(f"Gender: {self.gender} Height: {self.height} inches Weight: {self.weight} pounds")
        print(f"Age: {self.age} Hair: {self.hair} Money: {self.money} GP")
        print(f"Wt. Possible: {self.wt_possible} pounds")
        for attr, value in self.attributes.items():
            original_value = self.original_attributes[attr]
            asterisk = "*" if attr in self.triples else ""
            print(f"{attr}: [{original_value}] -> {value}{asterisk}")
        if self.triples:
            print("Specialist attributes enhanced for:", ", ".join(str(attr) for attr in self.triples))
        print(f"Combat ADDS: {self.combat_adds}")

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def main():
    while True:
        clear_screen()
        character = Character()
        character.generate_attributes()
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
    character.load_kindred_modifiers()
    character.apply_kindred_modifiers()
    character.calculate_combat_adds()  # Recalculate Combat ADDS after applying modifiers
    character.calculate_wt_possible()  # Calculate Wt. Possible after applying modifiers
    character.calculate_level()  # Calculate level after applying modifiers
    clear_screen()
    character.name = character.prompt_input("Enter your character's name: ")
    character.display_all_information()
    # Save to file or further steps

if __name__ == "__main__":
    main()
