from random import randrange


def get_problem(problem_type) -> tuple[int, int, int | float, str]:
    if problem_type == "Додавання":
        a, b = 100, 100
        while a + b >= 100:
            a = randrange(1, 101)
            b = randrange(1, 101)
        return a, b, a + b, "+"

    if problem_type == "Віднімання":
        a, b = 0, 0
        while a <= b:
            a = randrange(1, 101)
            b = randrange(1, 101)
        return a, b, a - b, "-"

    if problem_type == "Множення":
        a = randrange(1, 101)
        b = randrange(1, 101)
        return a, b, a * b, "*"

    if problem_type == "Просте множення":
        a = randrange(1, 11)
        b = randrange(1, 11)
        return a, b, a * b, "*"

    if problem_type == "Ділення":
        a, b = 0, 0
        while a <= b or a % b != 0 or b == 0:
            a = randrange(1, 101)
            b = randrange(1, 101)
        return a, b, a / b, "/"

    if problem_type == "Просте ділення":
        a, b = 0, 0
        while a <= b or a % b != 0 or b == 0:
            a = randrange(1, 11)
            b = randrange(1, 11)
        return a, b, a / b, "/"

    raise ValueError(f"Невідомий тип задачі: {problem_type}")
