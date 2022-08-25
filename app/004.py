import typing 
from flet import Checkbox
from flet import Column
from flet import FloatingActionButton
from flet import IconButton
from flet import Page
from flet import Row
from flet import Tab
from flet import Tabs
from flet import Text
from flet import TextButton
from flet import TextField
from flet import icons


class Task(Column):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.checkbox = Checkbox(expand=True)
        self.edit_button = IconButton(icon=icons.CREATE_OUTLINED)
        self.delete_button = IconButton(icon=icons.DELETE_OUTLINED)
        self.done_button = IconButton(icon=icons.DONE_OUTLINE_OUTLINED)
        self.edit_input = TextField(expand=True)

        self.view_row = Row()
        self.view_row.controls.append(self.checkbox)
        self.view_row.controls.append(self.edit_button)
        self.view_row.controls.append(self.delete_button)

        self.edit_row = Row()
        self.edit_row.controls.append(self.edit_input)
        self.edit_row.controls.append(self.done_button)

        self.controls.append(self.view_row)
        self.controls.append(self.edit_row)


class TodoApp(Column):
    def __init__(self) -> None:
        super().__init__()
        self.text_input = TextField(expand=True)
        self.add_button = FloatingActionButton(icon=icons.ADD)

        self.all_tab = Tab(text='All')
        self.active_tab = Tab(text='Active')
        self.completed_tab = Tab(text='Completed')

        row = Row()
        row.controls.append(self.text_input)
        row.controls.append(self.add_button)

        tabs = Tabs()
        tabs.tabs.append(self.all_tab)
        tabs.tabs.append(self.active_tab)
        tabs.tabs.append(self.completed_tab)

        self.controls.append(row)
        self.controls.append(tabs)

    def set_all_tasks(self, tasks: typing.List[typing.Tuple[str, bool]]) -> None:
        content = Column(horizontal_alignment='center')
        controls = []

        for task in tasks:
            task_text, task_value = task
            new_task = Task()
            new_task.checkbox.label = task_text
            new_task.checkbox.value = task_value
            content.controls.append(new_task)
            controls.append(new_task)
        self.all_tab.content = content
        self.update()

        return controls

    def set_active_tasks(self, tasks: typing.List[typing.Tuple[str, bool]]) -> None:
        content = Column(horizontal_alignment='center')
        controls = []

        for task in tasks:
            task_text, task_value = task
            new_task = Task()
            new_task.checkbox.label = task_text
            new_task.checkbox.value = task_value
            content.controls.append(new_task)
            controls.append(new_task)
        self.active_tab.content = content
        self.update()

        return controls

    def set_completed_tasks(self, tasks: typing.List[typing.Tuple[str, bool]]) -> None:
        pass


class Mainwindow(Column):
    def __init__(self) -> None:
        super().__init__()
        self.todo_app = TodoApp()
        self.controls.append(self.todo_app)
        self.controller = Controller(self)
    
    def text_input(self) -> str:
        return self.todo_app.text_input.value

    def set_text_input(self, value: str) -> None:
        self.todo_app.text_input.value = value

    def add_button(self) -> FloatingActionButton:
        return self.todo_app.add_button
    
    def set_all_tasks(self, *args, **kwargs) -> None:
        return self.todo_app.set_all_tasks(*args, **kwargs)

    def set_active_tasks(self, *args, **kwargs) -> None:
        return self.todo_app.set_active_tasks(*args, **kwargs)

    def set_completed_tasks(self, *args, **kwargs) -> None:
        return self.todo_app.set_completed_tasks(*args, **kwargs)


class Controller:
    def __init__(self, view: Mainwindow) -> None:
        self.model = {}
        self.view = view
        self.view.add_button().on_click = self.add_task

    def update_tasks(self) -> None:
        all = [task for task in self.model.items()]
        active = [task for task in all if task[1] == False]

        controls = self.view.set_all_tasks(all)
        for control in controls:
            # pass
            control.checkbox.on_change = lambda event: print('a')

        controls = self.view.set_active_tasks(active)
        for control in controls:
            pass
            # control.checkbox.on_change = lambda event: self.update_tasks()




    def add_task(self, event) -> None:
        task = self.view.text_input()
        self.model[task] = False
        self.update_tasks()



def main(page: Page):
    main_window = Mainwindow()
    page.add(Mainwindow())


if __name__ == '__main__':
    from flet import app
    app(target=main)
