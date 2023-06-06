import random

# Constants
GRID_SIZE = 30
TERRAIN_TYPES = {'T': 'Trees', 'M': 'Mountain', 'L': 'Lake', 'R': 'Field', 'D': 'Desert'}
COMMANDS = ['build', 'scavenge']
UNIT_SYMBOL = 'D'
HOUSE_SYMBOL = 'H'
FOOD_SYMBOL = 'F'
MAX_HOUSE_DISTANCE = 2
MAX_FOOD_DISTANCE = 2
HAPPINESS_THRESHOLD = 24
DEATH_THRESHOLD = 48
FOOD_START_COUNT = 10
FOOD_EATEN_PER_UNIT = 1
FOOD_SUCCESS_CHANCE = 0.7
AGE_THRESHOLD = 360
TIME_INCREMENT = 12
DEFAULT_HUNGER = 5
UNIT_NAMES = ['Alice', 'Bob', 'Charlie', 'David', 'Eve', 'Frank', 'Grace', 'Henry', 'Ivy', 'Jack']

class Unit:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.houses = []
        self.happiness = 0
        self.hunger = DEFAULT_HUNGER
        self.age = 0
        self.name = random.choice(UNIT_NAMES)

    def move(self, new_x, new_y):
        self.x = new_x
        self.y = new_y

    def build_house(self, x, y):
        if abs(x - self.x) <= MAX_HOUSE_DISTANCE and abs(y - self.y) <= MAX_HOUSE_DISTANCE:
            terrain = next((symbol for (x_w, y_w, symbol) in world if x_w == x and y_w == y), '')
            if terrain in ['R', 'D']:
                self.houses.append((x, y))
                world.append((x, y, HOUSE_SYMBOL))
                print("House built!")
            else:
                print("Invalid terrain for building a house.")
        else:
            print("Coordinates are too far from the unit.")

    def scavenge_food(self):
        nearby_tiles = [(self.x + dx, self.y + dy) for dx in range(-MAX_FOOD_DISTANCE, MAX_FOOD_DISTANCE + 1)
                        for dy in range(-MAX_FOOD_DISTANCE, MAX_FOOD_DISTANCE + 1)
                        if (dx == 0 or dy == 0) and abs(dx) + abs(dy) <= MAX_FOOD_DISTANCE]
        valid_locations = [tile for tile in nearby_tiles if 0 <= tile[0] < GRID_SIZE and 0 <= tile[1] < GRID_SIZE]

        if len(valid_locations) > 0:
            food_location = random.choice(valid_locations)
            if random.random() <= FOOD_SUCCESS_CHANCE:
                world.append((food_location[0], food_location[1], FOOD_SYMBOL))
                print("Food scavenged!")
                return True
            else:
                print("Failed to scavenge for food.")
                return False
        else:
            print("No valid location nearby to scavenge food.")
            return False

    def check_happiness(self):
        if len(self.houses) == 0:
            return 0

        unhappiness = 0
        for house in self.houses:
            distance = abs(house[0] - self.x) + abs(house[1] - self.y)
            if distance > MAX_HOUSE_DISTANCE:
                unhappiness += 1

        return unhappiness

    def check_hunger(self):
        if self.hunger > 0:
            self.hunger -= 1
            print("Unit", self.name, "has eaten.")
        else:
            print("Unit", self.name, "is hungry!")

    def age_unit(self):
        self.age += TIME_INCREMENT
        if self.age >= AGE_THRESHOLD:
            self.death()

    def death(self):
        print("Unit", self.name, "has died.")
        units.remove(self)


# Generate world
world = []
for x in range(GRID_SIZE):
    for y in range(GRID_SIZE):
        terrain = random.choice(list(TERRAIN_TYPES.keys()))
        world.append((x, y, terrain))

# Adjust terrain generation
for i in range(len(world)):
    x, y, terrain = world[i]

    if terrain == 'F':
        min_size = 3
        max_size = 5
        size_x = random.randint(min_size, max_size)
        size_y = random.randint(min_size, max_size)
        for dx in range(size_x):
            for dy in range(size_y):
                if x + dx < GRID_SIZE and y + dy < GRID_SIZE:
                    world.append((x + dx, y + dy, terrain))
        del world[i]

    if terrain == 'L':
        min_size = 1
        max_size = 6
        size_x = random.randint(min_size, max_size)
        size_y = random.randint(min_size, max_size)
        for dx in range(size_x):
            for dy in range(size_y):
                if x + dx < GRID_SIZE and y + dy < GRID_SIZE:
                    world.append((x + dx, y + dy, terrain))
        del world[i]

    if terrain == 'R':
        min_size = 4
        max_size = 10
        size_x = random.randint(min_size, max_size)
        size_y = random.randint(min_size, max_size)
        for dx in range(size_x):
            for dy in range(size_y):
                if x + dx < GRID_SIZE and y + dy < GRID_SIZE:
                    world.append((x + dx, y + dy, terrain))
        del world[i]

    if terrain == 'M':
        min_size = 2
        max_size = 8
        size_x = random.randint(min_size, max_size)
        size_y = random.randint(min_size, max_size)
        for dx in range(size_x):
            for dy in range(size_y):
                if x + dx < GRID_SIZE and y + dy < GRID_SIZE:
                    world.append((x + dx, y + dy, terrain))
        del world[i]

    if terrain == 'D':
        min_size = 3
        max_size = 9
        size_x = random.randint(min_size, max_size)
        size_y = random.randint(min_size, max_size)
        for dx in range(size_x):
            for dy in range(size_y):
                if x + dx < GRID_SIZE and y + dy < GRID_SIZE:
                    world.append((x + dx, y + dy, terrain))
        del world[i]

# Create units
units = []
for _ in range(10):
    x = random.randint(0, GRID_SIZE - 1)
    y = random.randint(0, GRID_SIZE - 1)
    units.append(Unit(x, y))

# Player's food count
food_count = FOOD_START_COUNT

# Game loop
while True:
    # Print world
    print("    ", end="")
    for x in range(GRID_SIZE):
        print(chr(x + ord('A')), end=" ")
    print()
    for y in range(GRID_SIZE):
        print(str(y + 1).zfill(2), end=" ")
        for x in range(GRID_SIZE):
            terrain = next((symbol for (x_w, y_w, symbol) in world if x_w == x and y_w == y), '')
            unit = next((u for u in units if u.x == x and u.y == y), None)
            if unit:
                print(UNIT_SYMBOL, end=' ')
            elif terrain:
                print(terrain, end=' ')
            else:
                print('.', end=' ')
        print()

    # Print units and select a unit
    print("Units:")
    for i, unit in enumerate(units):
        print(f"{i + 1}. {unit.name} - Position: ({chr(unit.x + ord('A'))}, {unit.y + 1})")

    unit_index = int(input("Select a unit (enter the number): ")) - 1
    selected_unit = units[unit_index]

    # Process command for the selected unit
    print(f"Selected unit: {selected_unit.name} - Position: ({chr(selected_unit.x + ord('A'))}, {selected_unit.y + 1})")
    command = input("Enter a command (build, scavenge): ")

    if command == 'build':
        coords = input("Enter the coordinates for the house (e.g., A1): ")
        x = ord(coords[0].upper()) - ord('A')
        y = int(coords[1:]) - 1
        selected_unit.build_house(x, y)
    elif command == 'scavenge':
        success = selected_unit.scavenge_food()
        if success:
            food_count += 3

    # Time increment
    for unit in units:
        unit.check_hunger()
        unit.age_unit()

    # Check unit happiness and hunger
    for unit in units:
        unit.check_happiness()

    # Check food count
    if food_count <= 0:
        print("No more food left! Game Over.")
        break

    # Time increment
    food_count -= len(units) * FOOD_EATEN_PER_UNIT
    print("Food count:", food_count)
    print("Time incremented by", TIME_INCREMENT, "hours.")

    # Check unit age and death
    for unit in units:
        unit.age_unit()
