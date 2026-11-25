"""
Programming 2026.

Seminar 13.

Polymorphism.

Your task is to implement the classes described below.
Pay attention to inheritance and method overriding.
"""

# Animal
## Attributes
### eating_type (predator, herbivore)
### habitat
### moving_type
## Methods
### breathe
### eat
### sleep
## Magic Methods
### __str__

# Dog (inherits from Animal)
## Attributes
### eating_type (predator)
### tamed (wild, domesticated)
### breed
### habitat
### moving_type
## Methods
### breathe (inherited)
### eat (overridden)
### sleep (inherited)
## Magic Methods
### __str__ (overridden)

# Cat (inherits from Animal)
## Attributes
### eating_type (predator)
### habitat
### moving_type
### character
### fluffiness
## Methods
### breathe (inherited)
### eat (overridden)
### sleep (inherited)
## Magic Methods
### __str__ (overridden)

# One code to process different types

# bubble = Cat(habitat='flat', character='playful', fluffiness='very')

# animals = [pug, bubble]
# for animal in animals:
#     print(animal)
#     animal.eat('meat')


def main() -> None:
    """
    Launch listing.
    """
    # student implementation goes here


if __name__ == "__main__":
    main()
