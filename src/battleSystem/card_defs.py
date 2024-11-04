

class CardConf:
    def __init__(self, id, name, class_, type, description, image, attack, defense, speed, range_start, range_end, beforeEffect = [], mainEffect = [], afterEffect = []):
        # For Render
        self.id = id
        self.class_ = class_
        self.type = type
        self.name = name
        self.description = description
        self.image = image

        # Card Stats
        self.attack = attack
        self.defense = defense
        self.speed = speed
        self.range_start = range_start
        self.range_end = range_end

        # Card Effects
        self.beforeEffect = beforeEffect # list of Effects
        self.mainEffect = mainEffect
        self.afterEffect = afterEffect

    def display_attributes(self):
        print(f"ID: {self.id}")
        print(f"Class: {self.class_}")
        print(f"Type: {self.type}")
        print(f"Name: {self.name}")
        print(f"Description: {self.description}")
        print(f"Image: {self.image}")
        print(f"Attack: {self.attack}")
        print(f"Defense: {self.defense}")
        print(f"Speed: {self.speed}")
        print(f"Range Start: {self.range_start}")
        print(f"Range End: {self.range_end}")
        
        # Printing effects
        print("Before Effects:")
        for effect in self.beforeEffect:
            print(f"  - {effect}")
        
        print("Main Effects:")
        for effect in self.mainEffect:
            print(f"  - {effect}")
        
        print("After Effects:")
        for effect in self.afterEffect:
            print(f"  - {effect}")

