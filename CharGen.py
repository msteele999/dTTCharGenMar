import json
import random

class Character:
    def __init__(self, name):
        self.name = name
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

    def roll_dice(self, number_of_dice, sides):
        return [random.randint(1, sides) for _ in range(number_of_dice)]

    def generate_attributes(self):
        for attr in self.attributes:
            rolls = self.roll_dice(3, 6)
            self.attributes[attr] = sum(rolls)
            if len(set(rolls)) == 1:  # Check if all three rolls are the same
                self.triples.append(attr)

    def calculate_combat_adds(self):
        self.combat_adds = 0
        for attr in ["STR", "LK", "DEX", "SPD"]:
            if self.attributes[attr] > 12:
                self.combat_adds += self.attributes[attr] - 12

    def display_attributes(self):
        for attr, value in self.attributes.items():
            asterisk = "*" if attr in self.triples else ""
            print(f"{attr}: {value}{asterisk}")
        if self.triples:
            print("Triples rolled for:", ", ".join(self.triples))
        print(f"Combat ADDS: {self.combat_adds}")

    def save_to_file(self, filename):
        with open(filename, 'w') as file:
            json.dump(self.__dict__, file)

    @classmethod
    def load_from_file(cls, filename):
        with open(filename, 'r') as file:
            data = json.load(file)
            character = cls(data['name'])
            character.__dict__.update(data)
            return character

def main():
    name = input("Enter your character's name: ")
    character = Character(name)
    character.generate_attributes()
    character.calculate_combat_adds()
    character.display_attributes()
    # Save to file or further steps

if __name__ == "__main__":
    main()
