"""
Programming 2026.

Seminar 17.

Inheritance vs Composition vs Aggregation.

This listing demonstrates the differences between inheritance, composition, and aggregation.

Classes for demonstrating inheritance, composition, and aggregation:
• Equipment - base class for equipment.
• Chestplate and Mace - inheritors of Equipment (inheritance).
• Stats - character stats created inside Paladin (composition).
• Paladin - owns Stats and holds external Mace and Chestplate (aggregation).
"""

# pylint: disable=too-few-public-methods,duplicate-code,no-member

# ======================----------======================
#       Inheritance vs Composition vs Aggregation
# ======================----------======================

# Example of aggregation
# a = A()
# b = B()
# c = C(a, b)
# del c
# print(a) # still exist

# Example of composition
# c = C() # in init we create self.a = A()
# del c
# neither c nor a exist

# Now try to implement the classes below using inheritance, composition, and aggregation


class Equipment:
    """
    Represents a base piece of equipment.
    """

    def __init__(self, durability: int, weight: int) -> None:
        """
        Initializes equipment.

        Args:
            durability (int): Durability of the equipment.
            weight (int): Weight of the equipment.
        """


class Chestplate(Equipment):
    """
    Represents a chestplate.
    """

    def __init__(self, durability: int, weight: int, defense: int) -> None:
        """
        Initializes a chestplate.

        Args:
            durability (int): durability of a chestplate.
            weight (int): weight of a chestplate.
            defense (int): defense of a chestplate.
        """


class Mace(Equipment):
    """
    Represents a mace.
    """

    def __init__(self, durability: int, weight: int, damage: int) -> None:
        """
        Initializes a mace.

        Args:
            durability (int): durability of a mace.
            weight (int): weight of a mace.
            damage (int): damage of a mace.
        """


class Stats:
    """
    Represents character stats.
    """

    def __init__(self, hp: int = 100, mana: int = 100, level: int = 1) -> None:
        """
        Initializes default base character stats.

        Args:
            hp (int): Health points.
            mana (int): Mana points.
            level (int): Level of the character.
        """


class Paladin:
    """
    Represents a paladin hero.
    """

    def __init__(self, mace: Mace, chestplate: Chestplate) -> None:
        """
        Initializes a paladin.

        Args:
            mace (Mace): Mace instance.
            chestplate (Chestplate): Chestplate instance.
        """

    def attack(self) -> None:
        """
        Performs an attack.
        """


def demonstrate_composition() -> None:
    """
    Demonstrates composition and aggregation.
    """
    mace = Mace(durability=100, weight=10, damage=20)
    chestplate = Chestplate(durability=100, weight=10, defense=20)

    paladin = Paladin(mace, chestplate)
    paladin.attack()

    print(paladin.stats.hp, paladin.stats.mana, paladin.stats.level)
    del paladin

    print(mace.damage, chestplate.defense)


def main() -> None:
    """
    Launch listing.
    """
    print("====================---Composition---===================")
    # demonstrate_composition()


if __name__ == "__main__":
    main()
