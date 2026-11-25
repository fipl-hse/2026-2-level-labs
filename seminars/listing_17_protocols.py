"""
Programming 2026.

Seminar 17.

Protocols: basic and advanced magic methods.
"""

# pylint: disable=too-few-public-methods, duplicate-code


class DemoBox:
    """
    Simple container to demonstrate basic dunder methods.
    """

    def __init__(self, items: list[str]) -> None:
        self.items = items

    def __str__(self) -> str:
        return f"Box with {len(self.items)} items"

    def __repr__(self) -> str:
        return f"DemoBox({self.items!r})"

    def __len__(self) -> int:
        return len(self.items)

    def __bool__(self) -> bool:
        return len(self.items) > 0


box = DemoBox(["apple", "book"])
print("str(box) :", str(box))
print("repr(box):", repr(box))
print("in list  :", [box])
print("len(box) :", len(box))
print("bool(box):", bool(box))


class CountDown:
    """
    Simple iterator counting down from start to 1.
    """

    def __init__(self, start: int) -> None:
        self.current = start

    def __iter__(self) -> "CountDown":
        return self

    def __next__(self) -> int:
        if self.current <= 0:
            raise StopIteration
        value = self.current
        self.current -= 1
        return value


print("CountDown:", list(CountDown(3)))


# TASKS


class Student:
    """
    A single student with a name.
    """

    def __init__(self, name: str) -> None:
        self.name = name

    def __str__(self) -> str:
        return self.name

    def __repr__(self) -> str:
        return f"Student({self.name!r})"


class StudentGroup:
    """
    Container of students.
    Demonstrates basic protocols: str/repr, len, bool.
    Demonstrates advanced protocols: iadd/add, truediv, gt.
    """

    def __init__(self, students: list[Student] | None = None) -> None:
        self.students = list(students) if students else []

    def __str__(self) -> str:
        """
        String representation for users: comma-separated student names,
        or 'StudentGroup(empty)' if the group has no students.

        Returns:
            str: user-friendly string representation
        """
        # student implementation goes here

    def __repr__(self) -> str:
        """
        String representation for developers in format 'StudentGroup([...])'.

        Returns:
            str: unambiguous string representation
        """
        # student implementation goes here

    def __len__(self) -> int:
        """
        Return number of students in the group.

        Returns:
            int: number of students
        """
        # student implementation goes here

    def __bool__(self) -> bool:
        """
        Return True if the group is not empty, False otherwise.

        Returns:
            bool: truthiness of the group
        """
        # student implementation goes here

    def __iadd__(self, student: Student) -> "StudentGroup":
        """
        a += b: append a student to the group in place.
        Return NotImplemented if student is not a Student.

        Args:
            student (Student): student to append

        Returns:
            StudentGroup: self after appending
        """
        # student implementation goes here

    def __add__(self, student: Student) -> "StudentGroup":
        """
        a + b: return a new group with the student appended.
        Return NotImplemented if student is not a Student.

        Args:
            student (Student): student to append

        Returns:
            StudentGroup: new group with the student
        """
        # student implementation goes here

    def __truediv__(self, parts: int) -> tuple["StudentGroup", "StudentGroup"]:
        """
        a / 2: split the group into two groups.
        The first group gets the first half (ceil) of students,
        the second gets the rest. Only division by 2 is supported.

        Args:
            parts (int): must be 2

        Returns:
            tuple[StudentGroup, StudentGroup]: two new groups

        Raises:
            ValueError: if parts != 2
        """
        # student implementation goes here

    def __gt__(self, other: "StudentGroup") -> bool:
        """
        Check if this group has more students than other.
        Return NotImplemented if other is not StudentGroup.

        Args:
            other (StudentGroup): another group

        Returns:
            bool: True if self has more students, False otherwise
        """
        # student implementation goes here


class IterableGroup(StudentGroup):
    """
    StudentGroup that supports iteration over its students.
    Demonstrates advanced protocols: iter + next.
    """

    def __init__(self, students: list[Student] | None = None) -> None:
        super().__init__(students)
        self._index = 0

    def __iter__(self) -> "IterableGroup":
        """
        Reset index and return the iterator object itself.

        Returns:
            IterableGroup: self
        """
        # student implementation goes here

    def __next__(self) -> Student:
        """
        Return the next student until the end of the group,
        then raise StopIteration.

        Returns:
            Student: next student
        """
        # student implementation goes here


# a = StudentGroup()
# b = Student("Alice")
# c = Student("Bob")

# a += b -> a == StudentGroup([Student('Alice')])
# a += c -> a == StudentGroup([Student('Alice'), Student('Bob')])
# print(a) -> StudentGroup(Alice, Bob)
# print(len(a)) -> 2
# print(bool(a)) -> True

# group_1, group_2 = a / 2
# print(group_1) -> StudentGroup(Alice)
# print(group_2) -> StudentGroup(Bob)
# print(group_1 > group_2) -> False
# print(group_2 > group_1) -> False

# d = Student("Carol")
# group_1 += d
# print(group_1) -> StudentGroup(Alice, Carol)
# print(group_1 > group_2) -> True   (2 студента против 1)

# iterable_group = IterableGroup([b, c, d])
# for student in iterable_group:
#     print(student) ->
# Alice
# Bob
# Carol

# print(list(iterable_group)) -> [Alice, Bob, Carol]


def main() -> None:
    """
    Launch listing and demonstrate protocols.
    """
    # student implementation goes here


if __name__ == "__main__":
    main()
