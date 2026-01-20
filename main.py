import flet as ft
from random import randrange

def get_problem(problem_type):
    if problem_type == "Додавання":
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


def main(page: ft.Page):
    # page.window_icon = "icon.png"
    # page.favicon = "icon.png"
    page.window.width = 300
    page.window.height = 400
    page.title = "Математичний тренажер"
    page.theme_mode = ft.ThemeMode.DARK
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    # Змінні стану
    state = {
        "problems": [],
        "current_idx": 0,
        "score": 0,
        "total": 0
    }

    # Елементи інтерфейсу
    title = ft.Text("Математика", size=30, weight=ft.FontWeight.BOLD)
    question_text = ft.Text("", size=40)
    answer_field = ft.TextField(label="Твоя відповідь", keyboard_type=ft.KeyboardType.NUMBER,
                                width=200, on_submit=lambda _: check_answer(None))
    result_text = ft.Text("", size=20)

    # Функція для початку нової гри
    def start_game(e):
        try:
            n = int(num_input.value)
            if n <= 0:
                return
        except:
            return

        state["total"] = n
        state["score"] = 0
        state["current_idx"] = 0
        state["problems"] = [get_problem(problem_choise.value) for _ in range(n)]

        setup_view.visible = False
        game_view.visible = True
        next_problem()
        page.update()

    # Функція для відображення наступного прикладу
    def next_problem():
        if state["current_idx"] < state["total"]:
            p = state["problems"][state["current_idx"]]
            question_text.value = f"{p[0]} {p[3]} {p[1]}"
            answer_field.value = ""
            answer_field.focus()
        else:
            show_final_results()
        page.update()

    # Перевірка відповіді
    def check_answer(e):
        try:
            user_answer = int(answer_field.value)
            correct_answer = state["problems"][state["current_idx"]][2]

            if user_answer == correct_answer:
                state["score"] += 1

            state["current_idx"] += 1
            next_problem()
        except:
            answer_field.error = "Введіть число"
            page.update()

    def show_final_results():
        game_view.visible = False
        final_view.visible = True
        final_score_text.value = f"Твій результат: {state['score']} з {state['total']}"
        page.update()

    def restart(e):
        final_view.visible = False
        setup_view.visible = True
        num_input.value = "5"
        page.update()


    # Екрани (View)
    num_input = ft.TextField(value="5", label="Скільки прикладів?", width=200)
    problem_choise = ft.Dropdown(
        value="Додавання",
        label="Яка дія?",
        options=[
            ft.dropdown.Option("Додавання"),
            ft.dropdown.Option("Віднімання"),
            ft.dropdown.Option("Множення"),
            ft.dropdown.Option("Просте множення"),
            ft.dropdown.Option("Ділення"),
            ft.dropdown.Option("Просте ділення"),
        ])

    setup_view = ft.Column([
        title,
        problem_choise,
        num_input,
        ft.ElevatedButton("Почати", on_click=start_game)
    ], horizontal_alignment=ft.CrossAxisAlignment.CENTER)

    game_view = ft.Column([
        ft.Text("Розв'яжи приклад:", size=20),
        question_text,
        answer_field,
        ft.ElevatedButton("Відповісти", on_click=check_answer,
                          bgcolor=ft.Colors.BLUE_700, color=ft.Colors.WHITE)
    ], visible=False, horizontal_alignment=ft.CrossAxisAlignment.CENTER)

    final_score_text = ft.Text("", size=25)
    final_view = ft.Column([
        ft.Text("Гру закінчено!", size=30),
        final_score_text,
        ft.ElevatedButton("Спробувати знову", on_click=restart)
    ], visible=False, horizontal_alignment=ft.CrossAxisAlignment.CENTER)

    page.add(setup_view, game_view, final_view)


ft.run(main)
