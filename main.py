import flet as ft
from logic import get_problem
from state import State


def main(page: ft.Page):
    page.title = "Математичний тренажер"
    page.theme_mode = ft.ThemeMode.DARK
    page.dark_theme = ft.Theme(color_scheme_seed=ft.Colors.BLUE)
    page.bgcolor = "#4B496E"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    state = State()
    progress_bar = ft.ProgressBar(width=400, value=0, color="green")
    title = ft.Text("Математика", size=30, weight=ft.FontWeight.BOLD)
    question_text = ft.Text("", size=40)
    answer_container = ft.Column([], horizontal_alignment=ft.CrossAxisAlignment.CENTER)
    result_text = ft.Text("", size=20)

    def start_game(e):
        try:
            n = int(num_input.value)
            if n <= 0:
                return
        except:
            return

        state.total = n
        state.score = 0
        state.current_idx = 0
        state.problems = [get_problem(
            problem_choise.value) for _ in range(n)]

        setup_view.visible = False
        game_view.visible = True
        next_problem()
        page.update()

    def next_problem():
        if state.current_idx < state.total:
            progress_bar.value = state.current_idx / state.total + 100 / state.total / 100
            p = state.problems[state.current_idx]
            question_text.value = f"{p[0]} {p[3]} {p[1]}"
            answer_field = ft.TextField(
                value="",
                label="Твоя відповідь",
                keyboard_type=ft.KeyboardType.NUMBER,
                width=200,
                autofocus=True,
                on_submit=check_answer
            )
            answer_container.controls.clear()
            answer_container.controls.append(answer_field)
            page.update()
        else:
            show_final_results()

    def check_answer(e):
        try:
            user_answer = int(answer_container.controls[0].value)
            correct_answer = state.problems[state.current_idx][2]

            if user_answer == correct_answer:
                state.score += 1

            state.current_idx += 1
            next_problem()
        except:
            answer_container.controls[0].error = "Введіть число"
        page.update()

    def show_final_results():
        game_view.visible = False
        final_view.visible = True
        final_score_text.value = f"Твій результат: {state.score} з {state.total}"
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
        progress_bar,
        question_text,
        answer_container,
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
