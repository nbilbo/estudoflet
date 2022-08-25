from flet import Column
from flet import Container
from flet import FloatingActionButton
from flet import ListView
from flet import Page
from flet import Row
from flet import Text
from flet import TextButton
from flet import TextField
from flet.control_event import ControlEvent
from flet import border
from flet import border_radius
from flet import icons


class Todoapp(Column):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.horizontal_alignment = 'center'
        self.alignment = 'spaceBetween'
    
        self.add_button = TextButton(text='Add todo')
        self.delete_button = TextButton(text='Delete')
        self.complete_button = TextButton(text='Complete')
        # self.list_view = ListView(height=300, auto_scroll=False)

        self.controls.append(self.add_button)
        self.controls.append(self.delete_button)
        self.controls.append(Row(controls=[self.add_button, self.delete_button], alignment='spaceBetween'))


class Controller(object):
    def __init__(self, view: Todoapp) -> None:
        self.view = view

    def add_task(self, event: ControlEvent) -> None:
        print(type(event))


def main(page: Page):
    page.theme_mode = 'dark'
    todoapp = Todoapp()
    page.add(Container(content=todoapp, expand=1, border=border.all(5, '#ff0000'), border_radius=border_radius.all(10), padding=5))


if __name__ == '__main__':
    from flet import app
    
    app(target=main)
