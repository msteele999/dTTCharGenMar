import json
import random
import os

class Character:
    def __init__(self):
        self.name = ""
        self.kindred = ""
        self.character_type = ""
        self.gender = ""
        self.height = 0
        self.weight = 0
        self.age = 0
        self.hair = ""
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
            self.attributes[attr] = self.roll_and_check_triples()

    def roll_and_check_triples(self):
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

    def apply_kindred_modifiers(self):
        for attr in self.attributes:
            self.attributes[attr] = int(self.attributes[attr] * self.modifiers.get(attr, 1))
        self.height = int(self.height * self.modifiers.get("Height", 1))
        self.weight = int(self.weight * self.modifiers.get("Weight", 1))

    def load_kindred_modifiers(self):
        kindred_file = self.kindred.lower().replace("-", "_") + "_modifiers.json"
        try:
            with open(kindred_file, "r") as file:
                self.modifiers = json.load(file)
        except FileNotFoundError:
            print(f"No modifiers file found for {self.kindred}. Using default modifiers.")
            self.modifiers = {attr: 1 for attr in self.attributes}
            self.modifiers.update({"Height": 1, "Weight": 1})

    def display_attributes(self):
        for attr, value in self.attributes.items():
            asterisk = "*" if attr in self.triples else ""
            print(f"{attr}: {value}{asterisk}")
        if self.triples:
            print("Specialist attributes enhanced for:", ", ".join(str(attr) for attr in self.triples))
        print(f"Combat ADDS: {self.combat_adds}")

    def prompt_for_details(self):
        self.kindred = self.select_option("Select Kindred", ["Human", "Dwarf-Midgardian", "Dwarf-Gristlegrim", "Elf", "Fairie", "Leprechaun", "Hobbs"])
        self.load_kindred_modifiers()
        self.character_type = self.select_option("Select Character Type", ["Warrior", "Wizard", "Rogue"])
        self.gender = input("Enter Gender: ")
        self.height = int(input("Enter Height (in inches): "))
        self.weight = int(input("Enter Weight (in pounds): "))
        self.age = int(input("Enter Age: "))
        self.hair = input("Enter Hair: ")

    def select_option(self, prompt, options):
        print(prompt)
        for i, option in enumerate(options, 1):
            print(f"{i}. {option}")
        choice = int(input("Enter the number of your choice: "))
        return options[choice - 1]

    def save_to_file(self, filename):
        with open(filename, 'w') as file:
            json.dump(self.__dict__, file)

    @classmethod
    def load_from_file(cls, filename):
        with open(filename, 'r') as file):
            data = json.load(file)
            character = cls()
            character.__dict__.update(data)
            return character

    def display_all_information(self):
        self.display_attributes()
        print(f"Name: {self.name}")
        print(f"Kindred: {self.kindred}")
        print(f"Character Type: {self.character_type}")
        print(f"Gender: {self.gender}")
        print(f"Height: {self.height} inches")
        print(f"Weight: {self.weight} pounds")
        print(f"Age: {self.age}")
        print(f"Hair: {self.hair}")

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def main():
    clear_screen()
    character = Character()
    character.generate_attributes()
    character.display_attributes()  # Display initial attributes before any adjustments
    character.prompt_for_details()
    character.apply_kindred_modifiers()
    character.calculate_combat_adds()  # Recalculate Combat ADDS after applying modifiers
    clear_screen()
    character.name = input("Enter your character's name: ")
    character.display_all_information()
    # Save to file or further steps

if __name__ == "__main__":
    main()
