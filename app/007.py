
from flet import Column
from flet import Container
from flet import ListView
from flet import Page
from flet import Row
from flet import Text
from flet import TextButton
from flet import TextField
from flet import border
from flet import border_radius



class Mainwindow(Row):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        r = Column([
            Container(expand=1, border=border.all(5, 'red'), content=Text("A")),
            Container(expand=3, border=border.all(5, 'green'), content=Text("B")),
            Container(expand=1, border=border.all(5, 'blue'), content=Text("C"))
        ])

        r = Column([
            Container(expand=1, content=Text("Header")),
            Container(expand=2, content=Text("Body")),
            # Container(content=Text("Body")),
            # Container(expand=3, content=Text("Body")),
            # Container(expand=1, content=Text("Footer"))
        ])

        self.controls.append(r)


class A(Column):
    def __init__(self) -> None:
        super().__init__()
        self.scroll = 'auto'
        self.auto_scroll = True
        for i in range(100):
            self.controls.append(TextButton(f'{i}'))

class B(Container):
    def __init__(self) -> None:
        super().__init__()
        self.expand = 1
        
        column = Column()
        column.scroll = 'auto'
        column.auto_scroll = True
        for i in range(100):
            column.controls.append(TextButton(f'{i}'))
        self.content = column

def main(page: Page):
    page.horizontal_alignment = 'center'
    page.add(Container(content=A(), expand=1))
    page.add(B())


if __name__ == '__main__':
    from flet import app
    app(target=main)
