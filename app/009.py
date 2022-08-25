from flet import Column
from flet import Container
from flet import ListView
from flet import Page
from flet import Row
from flet import Text
from flet import border



def main(page: Page):
   column1 = Column() 
   list_view = ListView(expand=True)
   row1 = Row()

   column1.controls.append(list_view)
   for count in range(100):
       control = Container(content=Text(value=f'{count}'), border=border.all(5, 'green')) 
       list_view.controls.append(control)

   page.add(Container(content=column1, expand=1, border=border.all(5, 'red')))
   page.add(Container(content=row1, border=border.all(5, 'blue')))


if __name__ == '__main__':
    from flet import app

    app(target=main)
