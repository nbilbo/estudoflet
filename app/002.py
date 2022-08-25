"""First todo."""
import flet


def main(page: flet.Page) -> None:
    def add_todo(event) -> None:
        checkbox = flet.Checkbox()
        checkbox.label = todo_input.value
        column.controls.append(checkbox)
        page.update()


    row = flet.Row()
    row.alignment = 'center'
    
    column = flet.Column()
    column.alignment= 'center'
    column.horizontal_alignment = 'center'

    todo_input = flet.TextField()
    todo_input.hint_text = 'Whats needs to be done?'

    add_button = flet.ElevatedButton()
    add_button.text = 'Add'
    add_button.on_click = add_todo

    row.controls.append(todo_input)
    row.controls.append(add_button)

    container = flet.Container(content=column, alignment=flet.alignment.center, bgcolor='red')
    page.controls.append(row)
    page.controls.append(container)
    page.update()


flet.app(target=main)
