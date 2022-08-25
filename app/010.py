import typing
from flet import Checkbox
from flet import Column
from flet import Container
from flet import Icon
from flet import ListView
from flet import Page
from flet import Text
from flet import TextField
from flet import TextButton
from flet import Row
from flet import border
from flet import icons


class Task(Row):
    def __init__(self) -> None:
        super().__init__()
        self.checkbox = Checkbox(expand=True)
        self.status = Icon(name=icons.CHECK)

        self.controls.append(self.checkbox)
        self.controls.append(self.status)
        
    def description(self) -> str:
        return self.checkbox.label
    
    def set_description(self, value: str) -> None:
        self.checkbox.label = value

    def is_completed(self) -> bool:
        return self.checkbox.value

    def set_is_completed(self, value: bool) -> None:
        pass

    def is_checked(self) -> bool:
        return self.checkbox.value

    def set_is_checked(self, value: bool) -> None:
        self.checkbox.value = value


class TodoApp(Column):
    def __init__(self) -> None:
        super().__init__()
        self.expand = True
        
        self.list_view = ListView() 
        list_view_container = Container(content=self.list_view)
        list_view_container.expand = 1
        list_view_container.border = border.all(5, 'blue')
        self.controls.append(list_view_container)

        self.delete_button = TextButton(text='Delete', expand=True)
        self.complete_button = TextButton(text='Complete', expand=True)
        self.controls.append(Row([self.delete_button, self.complete_button]))

        self.text_field = TextField(text_align='center')
        self.controls.append(self.text_field)

        self.add_button = TextButton(text='Add Todo', expand=1)
        self.controls.append(Row([self.add_button]))

    def text(self) -> str:
        return self.text_field.value
    
    def set_text(self, value: str) -> None:
        self.text_field.value = value
        self.update()

    def selected_tasks(self) -> typing.List:
        selected = []
        for task in self.list_view.controls:
            if task.is_completed():
                selected.append(task.description())

        return selected

    def add_task(self, description: str) -> None:
        task = Task()
        task.set_description(description)
        self.list_view.controls.append(task)
        self.update()

    def show_tasks(self, tasks: typing.List[typing.Dict[str, bool]]) -> None:
        self.list_view.controls = []
        for task in tasks:
            description = task['description']
            is_completed = task['is_completed']
            new_task = Task()
            new_task.set_description(description)
            new_task.set_is_completed(is_completed)
            self.list_view.controls.append(new_task)
        self.update()
    
    def focus_text_field(self) -> None:
        self.text_field.focus()


class Controller(object):
    def __init__(self, todoapp: 'TodoApp') -> None:
        self.model = []
        self.todoapp = todoapp
        self.todoapp.add_button.on_click = self.add_task
        self.todoapp.delete_button.on_click = self.delete_task
        self.todoapp.complete_button.on_click = self.complete_task

    def add_task(self, event) -> None:
        description = self.todoapp.text()
        self.model.append({'description':description, 'is_completed':False})
        self.todoapp.show_tasks(self.model)
        self.todoapp.set_text('')
        self.todoapp.focus_text_field()

    def delete_task(self, event) -> None:
        selected_tasks = self.todoapp.selected_tasks()
        for index, register in enumerate(self.model):
            if register['description'] in selected_tasks:
                self.model.pop(index)
                break
        self.todoapp.show_tasks(self.model)

    def complete_task(self, event) -> None:
        selected_tasks = self.todoapp.selected_tasks()
        for index, register in enumerate(self.model):
            if register['description'] in selected_tasks:
                register['is_completed'] = True
        print(self.model)



def main(page: Page):
    todoapp = TodoApp()
    controller = Controller(todoapp)
    page.add(todoapp)


if __name__ == '__main__':
    from flet import app
    app(target=main)
