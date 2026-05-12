# RPG Character System Project

!!! tip "Mental Model"
    An RPG character system is a natural fit for OOP: every character shares a common base (health, level, attack) but each class (Warrior, Mage, Archer) has a unique special ability. Inheritance captures the shared structure, and polymorphism lets the combat engine call `character.special_ability()` without caring which type it is -- the right behavior fires automatically.

## Overview
Build a complete RPG (Role-Playing Game) character system using inheritance and polymorphism.

## Objectives
- Design a class hierarchy for different character types
- Implement combat mechanics using polymorphism
- Create character abilities and skills
- Manage character stats and leveling

## Requirements

### 1. Base Character Class
Create an abstract `Character` class with:

- Attributes: name, level, health, max_health, attack, defense, experience
- Methods:
  - `take_damage(amount)` - reduce health, check if alive
  - `heal(amount)` - restore health (max = max_health)
  - `is_alive()` - return True if health > 0
  - `gain_experience(amount)` - add XP, level up if threshold reached
  - `level_up()` - increase stats when leveling up
  - `get_stats()` - return character statistics
  - Abstract method: `special_ability()` - unique to each character type

### 2. Character Classes
Implement these character types:

**Warrior**

- High health and defense
- Moderate attack
- Special ability: "Power Strike" - deals 2x attack damage
- Gains +10 health, +3 attack, +2 defense per level

**Mage**

- Low health and defense
- High attack (magical)
- Special ability: "Fireball" - deals 3x attack damage but costs health
- Gains +5 health, +5 attack, +1 defense per level

**Rogue**

- Moderate health
- High attack
- Low defense
- Special ability: "Backstab" - deals 2.5x attack damage, 30% chance to dodge next attack
- Gains +7 health, +4 attack, +1 defense per level

**Healer**

- Moderate health
- Low attack
- Moderate defense
- Special ability: "Holy Light" - heals self for 50% max health
- Gains +8 health, +2 attack, +3 defense per level

!!! tip "Avoiding Hardcoded Stats"
    Rather than hardcoding stat growth values (e.g., +10 health, +3 attack per level) directly
    in each subclass, consider loading them from a data structure such as a dictionary or
    configuration file. This separates **game data** from **game logic**, making it easy to
    rebalance characters without modifying class code. This is the **data-driven design**
    pattern used in real game engines.

### 3. Combat System
Create a `Battle` class that:

- Manages turn-based combat between two characters
- Allows characters to attack or use special abilities
- Displays combat log
- Determines winner
- Awards experience to winner

!!! note "Adding Strategic Depth"
    A simple alternating-turns system where characters always attack is predictable. Consider
    adding: (1) an action selection phase where each character chooses between attack, defend,
    use item, or special ability; (2) a speed/initiative stat that determines turn order;
    (3) elemental strengths and weaknesses (e.g., fire beats ice). These additions create a
    strategy layer that makes the combat system a genuine design challenge.

### 4. Character Party
Create a `Party` class that:

- Stores multiple characters
- Has methods to add/remove characters
- Calculate total party stats
- Find character by name
- Display all party members

## Sample Combat Flow
```
=== BATTLE START ===
Warrior (HP: 100/100) vs Mage (HP: 60/60)

Turn 1:
Warrior attacks Mage for 15 damage!
Mage HP: 45/60

Turn 2:
Mage uses Fireball! Deals 45 damage!
Warrior HP: 55/100

... combat continues ...

=== BATTLE END ===
Winner: Warrior
Experience gained: 150
```

## Bonus Features
- Add status effects (poison, stun, etc.)
- Implement equipment system
- Add character skills tree
- Create AI for computer-controlled characters
- Add multiplayer party battles
- Load character stats from a configuration file (data-driven design)

## Testing Requirements
Your implementation should:

1. Create one of each character type
2. Display their initial stats
3. Simulate a battle between two characters
4. Show leveling up
5. Demonstrate all special abilities
6. Test party management

## Files to Create
- `characters.py` - All character classes
- `battle.py` - Combat system
- `party.py` - Party management
- `main.py` - Demo program
- `README.md` - This file

!!! warning "Inheritance Explosion"
    With four character classes, inheritance works well. But what happens when you add
    Paladin, Necromancer, Ranger, Bard, Monk, and Druid? Each new subclass duplicates
    boilerplate and the hierarchy grows linearly. At that point, consider switching to
    **composition**: define abilities as objects (`PowerStrike`, `Fireball`, `Backstab`)
    and attach them to a generic `Character`. This is the same design shift covered in
    the [Composition vs Inheritance](../composition/composition_vs_inheritance.md) section.

!!! tip "Separation of Concerns"
    Consider splitting the project further: keep character **data** (stats, growth rates) in a
    separate module or JSON file, game **logic** (combat rules, XP formulas) in the engine, and
    **presentation** (combat log formatting, display) in a UI layer. This separation makes each
    component independently testable and modifiable.

Good luck, adventurer!

## Exercises

**Exercise 1.**
Explain how `special_ability()` demonstrates polymorphism. Write a function `use_ability(character)` that calls `character.special_ability()` without checking the character's type. Show that it works correctly for `Warrior`, `Mage`, and `Healer` instances.

??? success "Solution to Exercise 1"

        from abc import ABC, abstractmethod

        class Character(ABC):
            def __init__(self, name, health, attack):
                self.name = name
                self.health = health
                self.attack = attack

            @abstractmethod
            def special_ability(self):
                pass

        class Warrior(Character):
            def special_ability(self):
                damage = self.attack * 2
                return f"{self.name} uses Power Strike for {damage} damage!"

        class Mage(Character):
            def special_ability(self):
                damage = self.attack * 3
                return f"{self.name} casts Fireball for {damage} damage!"

        class Healer(Character):
            def special_ability(self):
                heal = self.health // 2
                return f"{self.name} uses Holy Light, healing for {heal} HP!"

        def use_ability(character):
            # No type checking — polymorphism handles dispatch
            print(character.special_ability())

        for c in [Warrior("Conan", 100, 15), Mage("Gandalf", 60, 25), Healer("Mercy", 80, 8)]:
            use_ability(c)

    `use_ability` works because all subclasses implement `special_ability()` — the ABC guarantees it. The caller does not need `if isinstance(...)` checks. This is polymorphism: same interface, different behavior based on type.

---

**Exercise 2.**
The current design uses one subclass per character type. Describe what happens when you need to add 10 more character types. Sketch a composition-based alternative where abilities are objects attached to a generic `Character`, and explain how this avoids the hierarchy explosion.

??? success "Solution to Exercise 2"

    With inheritance, 10 more types means 10 more subclasses — each duplicating the same `__init__` boilerplate and differing only in `special_ability()` and stat growth. This is the **inheritance explosion** problem.

    **Composition-based alternative:**

        class Ability:
            def __init__(self, name, multiplier, description):
                self.name = name
                self.multiplier = multiplier
                self.description = description

            def use(self, character):
                damage = character.attack * self.multiplier
                return f"{character.name} uses {self.name} for {damage} damage!"

        class Character:
            def __init__(self, name, health, attack, defense, ability):
                self.name = name
                self.health = health
                self.attack = attack
                self.defense = defense
                self.ability = ability  # Composition

            def special_ability(self):
                return self.ability.use(self)

        # Create characters by composing different abilities
        power_strike = Ability("Power Strike", 2, "A powerful melee attack")
        fireball = Ability("Fireball", 3, "A devastating fire spell")

        warrior = Character("Conan", 100, 15, 10, power_strike)
        mage = Character("Gandalf", 60, 25, 5, fireball)

    Adding a new character type now requires only a new `Ability` instance, not a new class. This is data-driven design.

---

**Exercise 3.**
Design the `level_up()` method. It should increase stats based on the character type. Implement it using a data-driven approach: store stat growth rates in a dictionary or class attribute rather than hardcoding values in the method body. Explain why this separation of data and logic is beneficial.

??? success "Solution to Exercise 3"

        class Character:
            GROWTH_RATES = {}  # Subclasses override

            def __init__(self, name, health, attack, defense):
                self.name = name
                self.health = health
                self.max_health = health
                self.attack = attack
                self.defense = defense
                self.level = 1
                self.experience = 0

            def level_up(self):
                rates = self.GROWTH_RATES
                self.level += 1
                self.max_health += rates.get("health", 0)
                self.health = self.max_health
                self.attack += rates.get("attack", 0)
                self.defense += rates.get("defense", 0)
                print(f"{self.name} leveled up to {self.level}!")

        class Warrior(Character):
            GROWTH_RATES = {"health": 10, "attack": 3, "defense": 2}

        class Mage(Character):
            GROWTH_RATES = {"health": 5, "attack": 5, "defense": 1}

        w = Warrior("Conan", 100, 15, 10)
        w.level_up()
        print(f"HP: {w.max_health}, ATK: {w.attack}, DEF: {w.defense}")
        # HP: 110, ATK: 18, DEF: 12

    **Benefits of data-driven design:** growth rates can be loaded from a JSON file, changed without touching code, and tested independently. Game designers can rebalance characters without developer intervention.

---

**Exercise 4.**
The `Battle` class manages combat between two characters. Explain why `Battle` should not inherit from `Character`. What relationship does `Battle` have with `Character`, and which OOP principle does this illustrate?

??? success "Solution to Exercise 4"

    A `Battle` is not a kind of `Character` — it does not have health, attack, or a `special_ability()`. Using inheritance here would violate the **is-a** test and the Liskov Substitution Principle: you could not pass a `Battle` to any function expecting a `Character`.

    `Battle` has a **"uses"** relationship with `Character` — it receives two `Character` instances and orchestrates their interaction. This is composition/association:

        class Battle:
            def __init__(self, char_a, char_b):
                self.char_a = char_a  # Uses, does not own
                self.char_b = char_b

            def fight(self):
                # Orchestrate turns between char_a and char_b
                ...

    This illustrates the **Single Responsibility Principle**: `Character` is responsible for its own stats and abilities, while `Battle` is responsible for combat rules and turn order. Neither knows about the other's internal implementation.
