"""
Programming 2026.

Seminar 16.

MRO; diamond problem; multiple inheritance.

This listing demonstrates how attributes and methods are inherited from different classes
using super(). Additionally, we cover the classic diamond problem and its resolution in Python
using __mro__. Also, we examine how private attributes behave in multiple inheritance
and what problems they solve.

Classes for demonstrating multiple inheritance:
• MagicSpell - base class for spells.
• FireSpell and IceSpell - inheritors of MagicSpell.
• FrozenFireSpell - multiple inheritor of FireSpell and IceSpell.
"""

# pylint: disable=too-few-public-methods,duplicate-code,no-member
# pylint: disable=inconsistent-mro,missing-class-docstring
# mypy: disable-error-code="arg-type,misc"
from typing import Sequence

# ======================----------======================
#        The diamond problem and name mangling
# ======================----------======================


class MagicSpell:
    """
    Represents a base magical spell.

    Attributes:
        __damage (int): Base damage dealt by the spell.
    """

    def __init__(self, damage: int) -> None:
        """
        Initializes the base magic spell.

        Args:
            damage (int): Damage of the spell.
        """

    def cast_spell(self, modifiers: Sequence[int] | None = None) -> None:
        """
        Casts the spell, scaling damage by modifier multipliers if provided.

        Args:
            modifiers (Sequence[int] | None, optional): Sequence of damage multipliers.
                Defaults to None.
        """


class FireSpell(MagicSpell):
    """
    Represents a fire-based magical spell.
    """

    FIRE_MODIFIER = 2

    def __init__(self, damage: int) -> None:
        """
        Initializes a fire spell.

        Args:
            damage (int): Base fire damage.
        """

    def get_fire_damage(self) -> int:
        """
        Returns fire damage.

        Returns:
            int: total fire damage.
        """


class IceSpell(MagicSpell):
    """
    Represents an ice-based magical spell.
    """

    ICE_MODIFIER = 3

    def __init__(self, damage: int) -> None:
        """
        Initializes an ice spell.

        Args:
            damage (int): Base ice damage.
        """

    def get_ice_damage(self) -> int:
        """
        Returns ice damage.

        Returns:
            int: total ice damage.
        """


class FrozenFireSpell(IceSpell, FireSpell):
    r"""
    Represents a spell inheriting both IceSpell and FireSpell.

    Inheritance hierarchy:
             MagicSpell
             /        \
        IceSpell    FireSpell
             \        /
          FrozenFireSpell
    """


def demonstrate_diamond() -> None:
    """
    Demonstrates the diamond problem.
    """
    # 1. What if we change the order of the inheritors?
    #    and how we can see the order of initializations

    damage = ...

    spell = FrozenFireSpell(damage=damage)

    # 2. Check that FireSpell and IceSpell store independent __damage values
    assert spell.get_fire_damage() != spell.get_ice_damage()

    # 3. Why do we operate with common __damage variable
    #    but have different behaviour?
    print("Spell attributes:", spell.__dict__)

    spell.cast_spell((spell.ICE_MODIFIER, spell.FIRE_MODIFIER))


# ======================----------======================
#                       MRO Puzzles
# ======================----------======================
#    Guess MRO of classes below and try to explain it.
#           Does everything work as expected?


def puzzle1() -> int:
    r"""
    A           B
    ^           ^
    |           | \
    +-----+-----+  \
          |         |
          C         |
          ^         |
          |         |
          +----+----+
               |
               D
    """

    class A:
        pass

    class B:
        pass

    class C(A, B):
        pass

    class D(C, B):
        pass

    print(D.mro())
    return 0


def puzzle2() -> int:
    """
    +-->A<--+
    |       |
    |       |
    |       B
    |       ^
    |       |
    +---+---+
        |
        C
    """

    class A:
        pass

    class B(A):
        pass

    class C(A, B):
        pass

    print(C.mro())
    return 0


def puzzle3() -> int:
    r"""
    X           Y
    ^ \       / ^
    |   \   /   |
    |     X     |
    |   /   \   |
    |  /     \  |
    A           B
    ^           ^
    \           /
     +----+----+
          |
          Z
    """

    class X:
        pass

    class Y:
        pass

    class A(X, Y):
        pass

    class B(Y, X):
        pass

    class Z(A, B):
        pass

    print(Z.mro())
    return 0


def main() -> None:
    """
    Launch listing.
    """
    print("======================---Diamond---=====================")
    # demonstrate_diamond()
    print("======================---Puzzles---=====================")
    # print("Puzzle 1:", puzzle1())
    # print("Puzzle 2:", puzzle2())
    # print("Puzzle 3:", puzzle3())


if __name__ == "__main__":
    main()
