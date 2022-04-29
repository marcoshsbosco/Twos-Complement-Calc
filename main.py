def read_input():
    a = int(input("Supply first operand: "))
    op = input("Supply operator (*, /): ")
    b = int(input("Supply second operand: "))

    print("")

    return a, b, op


def to_binary(n):
    negative = True if n < 0 else False
    binary = ""

    n = abs(n)

    while n > 0:
        b = n % 2
        n = n // 2

        binary += str(b)

    binary += "0" * (16 - len(binary))  # zero pad until 16 bits

    binary = binary[::-1]  # reverse string

    if negative:
        complement = ""

        # boolean complement
        for bit in binary:
            complement += "0" if bit == "1" else "1"

        binary = add(complement, "0" * 15 + "1")  # two's complement

    return binary


def add(a, b):
    res = ""
    carry = 0

    for i in range(len(a) - 1, -1, -1):  # loop bits from right to left
        tmp = int(a[i]) + int(b[i]) + carry

        if tmp > 1:
            res += "0" if tmp == 2 else "1"  # tmp is either 2 or 3 (10 or 11), so store 2nd bit
            carry = 1
        else:
            res += str(tmp)
            carry = 0

    res = res[::-1]

    return res


def subtract(a, b):
    # make b negative (a - b = a + (-b))
    complement = ""

    for bit in b:
        complement += "0" if bit == "1" else "1"

    b = add(complement, "0" * 15 + "1")  # negative b

    return add(a, b)


def multiply(q, m):
    a = "0" * 16
    qm1 = "0"

    print("\n---Initial values---")
    print(f"a: {a}")
    print(f"q: {q}")
    print(f"q-1: {qm1}")
    print(f"m: {m}")

    for i in range(16):
        print(f"\n---Cycle {i + 1}---")

        q0qm1 = q[len(q) - 1] + qm1

        if q0qm1 == "10":
            print(f"a = a - m")

            a = subtract(a, m)

            print(f"a: {a}")
            print(f"q: {q}")
            print(f"q-1: {qm1}")
            print(f"m: {m}\n")
        elif q0qm1 == "01":
            print(f"a = a + m")

            a = add(a, m)

            print(f"a: {a}")
            print(f"q: {q}")
            print(f"q-1: {qm1}")
            print(f"m: {m}\n")

        print("Right-shifting a,q,q-1")
        qm1 = q[len(q) - 1]
        q = a[len(a) - 1] + q[:-1]
        a = a[0] + a[:-1]

        print(f"a: {a}")
        print(f"q: {q}")
        print(f"q-1: {qm1}")
        print(f"m: {m}")

    res = a + q

    return res


a, b, op = read_input()

a = to_binary(a)
b = to_binary(b)
print(f"a: {a}")
print(f"b: {b}")
print("")

if op == "*":
    res = multiply(a, b)

print(f"\nResult: {res}")
