class Point:
    x = 0
    y = 0

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y


p1 = Point(3,4)
p2 = Point(3,4)

p3 = p1

print(p1 == p2)
print(p1 is p2)
print(p1 == p3)
print(p1 is p3)