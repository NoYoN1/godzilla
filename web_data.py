class Person:
    def __init__(self, name, age):
        self.name = name
        self.age = age


p1 = Person("Harry potter", 25)
p2 = Person("Hulk", 35)

p = [p1, p2]


class Movie:
    def __init__(self, name):
        self.name = name


m1 = Movie("Iron Man")
m2 = Movie("Spider Man")
m3 = Movie("Harry potter")

m = [m1, m2, m3]
