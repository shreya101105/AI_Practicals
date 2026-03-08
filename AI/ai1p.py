# Function to generate Magic Square
def generateSquare(n):

    # Create n x n matrix filled with 0
    magicSquare = [[0 for x in range(n)] for y in range(n)]

    # Initial position
    i = n // 2
    j = n - 1

    num = 1
    while num <= (n * n):

        # Condition 3
        if i == -1 and j == n:
            j = n - 2
            i = 0
        else:
            # If column becomes n
            if j == n:
                j = 0

            # If row becomes -1
            if i < 0:
                i = n - 1

        # Condition 2
        if magicSquare[i][j] != 0:
            j = j - 2
            i = i + 1
            continue
        else:
            magicSquare[i][j] = num
            num += 1

        # Move to next position
        j += 1
        i -= 1

    # Print Magic Square
    print("Magic Square for n =", n)
    print("Sum of each row or column:", n * (n * n + 1) // 2)
    print()

    for i in range(n):
        for j in range(n):
            print('%2d ' % magicSquare[i][j], end='')
        print()


# Driver Code
n = int(input("Enter an ODD number for Magic Square: "))
generateSquare(n)