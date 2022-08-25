"""Trying learn tab and tabs."""
from flet import Column
from flet import ElevatedButton
from flet import Page
from flet import Row
from flet import Tab
from flet import Tabs
from flet import Text
from flet import UserControl
from flet import alignment
from flet import icons


class Students(Column):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.horizontal_alignment = 'center'
        self.header = Text(value='Students Section', style='headlineMedium')
        self.confirm_button = ElevatedButton(text='click me')
        self.controls.append(Row([self.header], alignment='center'))
        self.controls.append(self.confirm_button)


class Volunteers(Column):
    def __init__(self):
        super().__init__()
        self.horizontal_alignment = 'center'
        self.header = Text(value='Volunteers Section', style='headlineMedium')
        self.confirm_button = ElevatedButton(text='click me')
        self.controls.append(Row([self.header], alignment='center'))
        self.controls.append(self.confirm_button)


class News(Tab):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.text = 'News'
        self.header = Text('Last news', style='headlineMedium')
        self.confirm_button = ElevatedButton(text='Click me')

        column = Column()
        column.horizontal_alignment = 'center' 
        column.controls.append(Row([self.header], alignment='center'))
        column.controls.append(self.confirm_button)
        self.content = column


class MainWindow(Column):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # controls
        self.students = Students()
        self.volunteers = Volunteers()
        self.news = News()

        students_tab = Tab(text='Students', content=self.students)
        volunteers_tab = Tab(text='Volunteers', content=self.volunteers)
        tabs = Tabs(tabs=[students_tab, volunteers_tab, self.news])
        self.controls.append(tabs)
        
        # commands
        self.students_confirm_button.on_click = self.hello_students
        self.volunteers_confirm_button.on_click = self.hello_volunteers
        self.news_confirm_button.on_click = self.hello_news

    def hello_students(self, event) -> None:
        phrases = ['hello students', 'hello again, students']
        current = self.students_header.value
        current_index = phrases.index(current) if current in phrases else 0
        next_index = (current_index+1) % len(phrases)
        self.students_header.value = phrases[next_index]
        self.update()

    def hello_volunteers(self, event) -> None:
        phrases = ['hello volunteers', 'hello again, volunteers']
        current = self.volunteers_header.value
        current_index = phrases.index(current) if current in phrases else 0
        next_index = (current_index+1) % len(phrases)
        self.volunteers_header.value = phrases[next_index]
        self.update()

    def hello_news(self, event) -> None:
        self.news_header.value = 'There are no news.'
        self.update()

    @property
    def students_confirm_button(self) -> ElevatedButton:
        return self.students.confirm_button
    
    @property
    def volunteers_confirm_button(self) -> ElevatedButton:
        return self.volunteers.confirm_button 

    @property
    def news_confirm_button(self) -> ElevatedButton:
        return self.news.confirm_button

    @property
    def students_header(self) -> Text:
        return self.students.header

    @property
    def volunteers_header(self) -> Text:
        return self.volunteers.header

    @property
    def news_header(self) -> Text:
        return self.news.header



def main(page: Page):
    page.add(MainWindow())

if __name__ == '__main__':
    from flet import app
    app(target=main)
