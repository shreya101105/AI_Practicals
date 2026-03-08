import itertools

word1 = input("Enter first word: ").upper()
word2 = input("Enter second word: ").upper()
result = input("Enter result word: ").upper()

letters = list(set(word1 + word2 + result))

if len(letters) > 10:
    print("Too many unique letters (max 10 allowed).")
    exit()

digits = range(10)
solution_found = False

for perm in itertools.permutations(digits, len(letters)):
    d = dict(zip(letters, perm))

    # First letter of any word cannot be zero
    if d[word1[0]] == 0 or d[word2[0]] == 0 or d[result[0]] == 0:
        continue

    num1 = int("".join(str(d[ch]) for ch in word1))
    num2 = int("".join(str(d[ch]) for ch in word2))
    num3 = int("".join(str(d[ch]) for ch in result))

    if num1 + num2 == num3:
        print("\nSolution Found:\n")

        print("Letter Values:")
        for key in sorted(d.keys()):
            print(key, "=", d[key])

        print("\nVerification:")
        print(num1, "+", num2, "=", num3)

        solution_found = True
        break

if not solution_found:
    print("No solution found.")