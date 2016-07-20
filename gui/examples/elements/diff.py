def fibonacci(x):
    if x < 2:
        return 1
    return fibonacci(x-2) + fibonacci(x-1)


def factorial(x):
    if x < 2:
        return 1
    return x * factorial(x-1)


def main():
    funcs = [fibonacci, factorial]
    n = 10
    for i in range(len(funcs)):
        print funcs[i](n)

main()