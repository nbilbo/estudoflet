from flet import Column
from flet import Container
from flet import ListView
from flet import Page
from flet import Row
from flet import Text
from flet import border


class Header(Container):
    def __init__(self) -> None:
        super().__init__()
        self.expand = 1
        self.border = border.all(5, 'red')

        text = Text(value='Header')
        content = Row(alignment='center')
        content.controls.append(text)
        self.content = content


class Body(Container):
    def __init__(self) -> None:
        super().__init__()
        self.expand = 2
        self.border = border.all(5, 'pink')

        text = Text(value='Body')
        list_view = ListView(expand=True)
        list_view.scroll = 'always'
        for count in range(10):
            list_view.controls.append(Text(f'Text {count}'))
        
        content = Column()
        content.controls.append(text)
        content.controls.append(list_view)
        self.content = content


class Mainwindow(Container):
    def __init__(self) -> None:
        super().__init__()
        self.expand = 1
        self.padding = 5
        self.border = border.all(5, 'blue')

        self.header = Header()
        self.body = Body()

        content = Column()
        content.controls.append(self.header)
        content.controls.append(self.body)
        self.content = content


def main(page: Page) -> None:
    page.alignment = 'center'
    page.horizontal_alignment = 'center'
    page.add(Mainwindow())


if __name__ == '__main__':
    from flet import app

    app(target=main)
