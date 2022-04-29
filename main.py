def read_input():
    a = int(input("Supply first operand: "))
    op = input("Supply operator (*, /): ")
    b = int(input("Supply second operand: "))

    print("")

    return a, b, op


def to_binary(n):
    if n > 32767:
        raise ArithmeticError('OverflowError')
    elif n < -32768:
        raise ArithmeticError('UnderflowError')

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
            res += str(tmp)  # tmp is either 0 or 1
            carry = 0

    res = res[::-1]

    if a[0] == b[0] and res[0] != a[0]:  # overflow rule
        raise ArithmeticError("OverflowError")

    return res


def subtract(a, b):  # subtraction rule
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

        print("Arithmetic right-shifting a,q,q-1")
        qm1 = q[len(q) - 1]
        q = a[len(a) - 1] + q[:-1]
        a = a[0] + a[:-1]

        print(f"a: {a}")
        print(f"q: {q}")
        print(f"q-1: {qm1}")
        print(f"m: {m}")

    res = a + q

    return res


def divide(q, m):
    # check if m is zero
    if m == "0" * 16:
        if q == "0" * 16:
            print("q and m are zero, result is indeterminate (trivial)")

            return "Indeterminate"
        else:
            print("m is zero, can't divide")

            return "Undefined"

    a = "0" * 16

    print("\n---Initial values---")
    print(f"a: {a}")
    print(f"q: {q}")
    print(f"m: {m}")

    for i in range(16):
        print(f"\n---Cycle {i + 1}---")

        print("Left-shifting a,q")
        a = a[1:] + q[0]
        q = q[1:] + "0"

        print(f"a: {a}")
        print(f"q: {q}")
        print(f"m: {m}")

        print("\na = a - m")
        a = subtract(a, m)

        print(f"a: {a}")
        print(f"q: {q}")
        print(f"m: {m}")

        if a[0] == "1":  # a is negative
            print("\na < 0? Yes, q0 = 0 and a = a + m")

            q = q[:-1] + "0"
            a = add(a, m)
        else:  # a >= 0
            print("\na < 0? No, q0 = 1")

            q = q[:-1] + "1"

        print(f"a: {a}")
        print(f"q: {q}")
        print(f"m: {m}")

    print(f"\nRemainder: {a}")

    return q


a, b, op = read_input()

try:
    a = to_binary(a)
    b = to_binary(b)
except ArithmeticError:
    print("Please use numbers between -32768 and 32767 (inclusive)\n")

    raise

print(f"a: {a}")
print(f"b: {b}")
print("")

if op == "*":
    res = multiply(a, b)
if op == "/":
    res = divide(a, b)

print(f"\nResult: {res}")
