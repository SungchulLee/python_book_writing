# Aggregation Pattern

Aggregation is a form of "has-a" relationship where the contained objects have independent lifetimes. Unlike composition, the container does not create or destroy its parts. Instead, pre-existing objects are passed into the container, and they survive even if the container is destroyed. This distinction makes aggregation the right choice when objects need to be shared across multiple containers or reused after a container is gone.

## Aggregation as a Has-A Relationship

### 1. Weaker Has-A

In aggregation the container holds references to objects it did not create. This is a "weaker" form of has-a compared to composition, because the container has no control over the lifecycle of its parts.

```python
class Wheel:
    pass

class Car:
    def __init__(self, wheels):
        self.wheels = wheels  # Aggregation

# Wheels exist independently
wheels = [Wheel(), Wheel(), Wheel(), Wheel()]
car = Car(wheels)
```

Here, the `Wheel` objects are created before the `Car` exists. The `Car` merely holds a reference to the list that was passed in.

## Independence

### 1. Separate Lifetimes

The defining characteristic of aggregation is that aggregated objects exist before being associated with the container and continue to exist after the container is destroyed.

```python
# Wheels can exist without car
del car
print(len(wheels))  # 4 — wheels still exist
```

Because `wheels` was created outside of `Car`, deleting the `Car` instance has no effect on the `Wheel` objects. They remain accessible through the original `wheels` variable.

## Danger: Shared Mutable State

Because aggregated objects can be shared across multiple containers, mutations through one container are visible everywhere. This is the main trade-off of aggregation versus [composition](composition_pattern.md).

```python
wheels = [Wheel(), Wheel()]
car_a = Car(wheels)
car_b = Car(wheels)

car_a.wheels.append(Wheel())
print(len(car_b.wheels))  # 3 — surprise!
```

If shared mutation is a concern, the container should store a **copy** of the list, or the aggregated objects themselves should be immutable.

## Summary

- Aggregation is a weaker has-a relationship where the container does not own the lifecycle of its parts.
- Contained objects have independent lifetimes and can exist before and after the container.
- Multiple containers can share the same aggregated objects, enabling flexible designs.
- **Watch for shared mutable state** --- mutations through one container affect all others holding the same references.
- Aggregation produces loose coupling between the container and its parts, making each component easier to test and reuse independently.

---

## Exercises

**Exercise 1.**
Create a `Player` class with a `name` attribute and a `Team` class that accepts a list of `Player` objects in its constructor. Demonstrate aggregation: create players first, add them to a team, delete the team, and show the players still exist. Then add one player to two different teams to show objects can be shared.

??? success "Solution to Exercise 1"

        class Player:
            def __init__(self, name):
                self.name = name

            def __repr__(self):
                return f"Player('{self.name}')"

        class Team:
            def __init__(self, name, players):
                self.name = name
                self.players = players  # Aggregation: not owned

        p1 = Player("Alice")
        p2 = Player("Bob")
        p3 = Player("Charlie")

        team_a = Team("Alpha", [p1, p2])
        team_b = Team("Beta", [p2, p3])  # p2 shared!

        del team_a
        print(p1)  # Player('Alice') — still exists
        print(p2)  # Player('Bob') — still exists

        # p2 is in team_b
        print(team_b.players)  # [Player('Bob'), Player('Charlie')]

---

**Exercise 2.**
Model a `Classroom` that aggregates `Student` objects. The `Classroom` should have an `add_student(student)` and `remove_student(name)` method. Create three students, add them to a classroom, remove one, and show the removed student still exists outside the classroom.

??? success "Solution to Exercise 2"

        class Student:
            def __init__(self, name, grade):
                self.name = name
                self.grade = grade

            def __repr__(self):
                return f"Student('{self.name}')"

        class Classroom:
            def __init__(self):
                self.students = []

            def add_student(self, student):
                self.students.append(student)

            def remove_student(self, name):
                self.students = [s for s in self.students if s.name != name]

        s1 = Student("Alice", "A")
        s2 = Student("Bob", "B")
        s3 = Student("Charlie", "C")

        room = Classroom()
        room.add_student(s1)
        room.add_student(s2)
        room.add_student(s3)

        room.remove_student("Bob")
        print(room.students)  # [Student('Alice'), Student('Charlie')]
        print(s2)             # Student('Bob') — still exists

---

**Exercise 3.**
Design a `Playlist` class that aggregates `Song` objects. A `Song` has `title` and `artist`. The `Playlist` holds a list of songs passed in or added later. Create several songs, build two playlists that share some songs, delete one playlist, and verify the shared songs are still accessible from the other playlist.

??? success "Solution to Exercise 3"

        class Song:
            def __init__(self, title, artist):
                self.title = title
                self.artist = artist

            def __repr__(self):
                return f"Song('{self.title}')"

        class Playlist:
            def __init__(self, name, songs=None):
                self.name = name
                self.songs = list(songs) if songs else []

            def add(self, song):
                self.songs.append(song)

        s1 = Song("Song A", "Artist 1")
        s2 = Song("Song B", "Artist 2")
        s3 = Song("Song C", "Artist 3")

        pl1 = Playlist("Morning", [s1, s2])
        pl2 = Playlist("Evening", [s2, s3])  # s2 shared

        del pl1
        print(s1)  # Song('Song A') — still exists
        print(s2)  # Song('Song B') — still exists
        print(pl2.songs)  # [Song('Song B'), Song('Song C')]
