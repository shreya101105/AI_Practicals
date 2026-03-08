a = int(input("Enter capacity of Jug A: "))
b = int(input("Enter capacity of Jug B: "))
goal = int(input("Enter goal amount: "))

x = 0
y = 0

print("Jug A:", x, "Jug B:", y)

while x != goal:
    if x == 0:
        x = a
    elif y == b:
        y = 0
    else:
        t = min(x, b - y)
        x = x - t
        y = y + t
    print("Jug A:", x, "Jug B:", y)

print("Goal achieved")
