from problems import get_problem


class State:
    def __init__(self) -> None:
        self.problems: list = []
        self.current_idx: int = 0
        self.score: int = 0
        self.total: int = 0

    def reset(self) -> None:
        self.problems = []
        self.current_idx = 0
        self.score = 0
        self.total = 0

    def start_game(self, total: int, problem_type: str) -> None:
        self.total = total
        self.score = 0
        self.current_idx = 0
        self.problems = [
            get_problem(problem_type) for _ in range(total)
        ]

    def has_next(self) -> bool:
        return self.current_idx < self.total

    def current_problem(self) -> tuple[int, int, int | float, str] | None:
        if not self.has_next():
            return None
        return self.problems[self.current_idx]

    def check_answer(self, user_answer) -> bool:
        correct = self.problems[self.current_idx][2]

        if user_answer == correct:
            self.score += 1
            result = True
        else:
            result = False

        self.current_idx += 1
        return result

    def progress(self) -> float:
        if self.total == 0:
            return 0
        return self.current_idx / self.total
