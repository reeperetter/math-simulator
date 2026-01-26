import flet as ft
from state import State


def main(page: ft.Page):
    page.title = "Математичний тренажер"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.padding = 0

    page.bgcolor = ft.Colors.TRANSPARENT
    page.decoration = ft.BoxDecoration(
        image=ft.DecorationImage(
            src="assets/bg.webp",
            fit=ft.BoxFit.COVER,
        )
    )

    state = State()
    progress_bar = ft.ProgressBar(width=400, value=0, color="green")
    title = ft.Text("Математика", size=30, weight=ft.FontWeight.BOLD)
    question_text = ft.Text("", size=40)
    answer_container = ft.Column(
        [], horizontal_alignment=ft.CrossAxisAlignment.CENTER)
    result_text = ft.Text("", size=20)

    def start_game(e):
        try:
            n = int(num_input.value)
            if n <= 0:
                return
        except:
            return

        choise = problem_choise.value
        if choise is None:
            return
        state.start_game(n, choise)

        setup_view.visible = False
        game_view.visible = True
        show_problem()
        page.update()

    def show_problem():
        if not state.has_next():
            show_final_results()
            return

        progress_bar.value = state.current_idx / state.total + 100 / state.total / 100
        p = state.current_problem()
        if p is None:
            return
        question_text.value = f"{p[0]} {p[3]} {p[1]}"
        answer_container.controls.clear()
        answer_container.controls.append(
            ft.TextField(
                label="Твоя відповідь",
                keyboard_type=ft.KeyboardType.NUMBER,
                autofocus=True,
                on_submit=check_answer
            )
        )
        page.update()

    def check_answer(e):
        try:
            value = int(answer_container.controls[0].value)
        except:
            answer_container.controls[0].error = "Введіть число"
            page.update()
            return

        state.check_answer(value)
        show_problem()

    def show_final_results():
        game_view.visible = False
        final_view.visible = True
        final_score_text.value = f"Твій результат: {state.score} з {state.total}"
        page.update()

    def restart(e):
        state.reset()
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
        ft.ElevatedButton("Почати", on_click=start_game,
                          bgcolor=ft.Colors.BLUE_700, color=ft.Colors.WHITE)
    ], horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        alignment=ft.MainAxisAlignment.CENTER
    )

    game_view = ft.Column([
        ft.Text("Розв'яжи приклад:", size=20),
        progress_bar,
        question_text,
        answer_container,
        ft.ElevatedButton("Відповісти", on_click=check_answer,
                          bgcolor=ft.Colors.BLUE_700, color=ft.Colors.WHITE)
    ], visible=False, horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        alignment=ft.MainAxisAlignment.CENTER
    )

    final_score_text = ft.Text("", size=25)
    final_view = ft.Column([
        ft.Text("Гру закінчено!", size=30),
        final_score_text,
        ft.ElevatedButton("Спробувати знову", on_click=restart)
    ], visible=False, horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        alignment=ft.MainAxisAlignment.CENTER
    )

    def centered(view: ft.Control) -> ft.Container:
        return ft.Container(
            expand=True,
            alignment=ft.Alignment.CENTER,
            content=view
        )

    page.add(setup_view, game_view, final_view)

ft.run(main)