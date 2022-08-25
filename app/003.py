"""https://flet.dev/docs/tutorials/python-todo"""
from flet import Checkbox
from flet import Column
from flet import FloatingActionButton
from flet import IconButton
from flet import OutlinedButton
from flet import Page
from flet import Row
from flet import Tab
from flet import Tabs
from flet import Text
from flet import TextField
from flet import UserControl
from flet import app
from flet import icons


class Task(UserControl):
    def __init__(self, task_name: str, task_status_change, task_delete) -> None:
        self.is_completed = False
        super().__init__()
        self.task_name = task_name
        self.task_status_change = task_status_change
        self.task_delete = task_delete
        self.is_completed = False

    def build(self):
        # creating the display section 
        self.display_task = Checkbox()
        self.display_task.label = self.task_name
        self.display_task.expand = True
        self.display_task.on_change = self.status_changed

        edit_button = IconButton()
        edit_button.icon = icons.CREATE_OUTLINED
        edit_button.tooltip = 'Edit To-Do'
        edit_button.on_click = self.edit_clicked

        delete_button = IconButton()
        delete_button.icon = icons.DELETE_OUTLINED
        delete_button.tooltip = 'Delete To-Do'
        delete_button.on_click = self.delete_clicked

        self.display_view = Row()
        self.display_view.controls.append(self.display_task)
        self.display_view.controls.append(edit_button)
        self.display_view.controls.append(delete_button)
        
        # creating edit section
        self.edit_name = TextField()
        self.edit_name.expand = True 
        self.edit_name.value = self.task_name

        done_button = IconButton()
        done_button.icon = icons.DONE_OUTLINE_OUTLINED
        done_button.tooltip = 'Update To-Do'
        done_button.on_click = self.done_clicked

        self.edit_view = Row()
        self.edit_view.controls.append(self.edit_name)
        self.edit_view.controls.append(done_button)
        self.edit_view.visible = False

        return Column(controls=[self.display_view, self.edit_view])

    def status_changed(self, event) -> None:
        self.is_completed = not self.is_completed
        self.task_status_change(self)

    def edit_clicked(self, event) -> None:
       self.edit_view.visible = True 
       self.display_view.visible = False
       self.edit_name.value = self.display_task.label
       self.update()

    def done_clicked(self, event) -> None:
        self.edit_view.visible = False
        self.display_view.visible = True
        self.display_task.label = self.edit_name.value
        self.update()

    def delete_clicked(self, event) -> None:
        self.task_delete(self)


class TodoApp(UserControl):

    def build(self):
        header = Row([Text('Todos', style='headlineMedium')], alignment='center')

        self.new_task = TextField()
        self.new_task.text_size = 32
        self.new_task.expand = True
        self.new_task.hint_text = 'Whats needs to be done ?'

        add_button = FloatingActionButton()
        add_button.icon = icons.ADD
        add_button.on_click = self.add_clicked 

        task_input_row = Row()
        task_input_row.controls.append(self.new_task)
        task_input_row.controls.append(add_button)

        self.tasks = Column()

        self.tabs = Tabs(
            selected_index=0, 
            tabs=[Tab(text='all'), Tab('active'), Tab('completed')],
            on_change=self.update
        )

        self.items_left = Text('0 items left.')
        clear_button = OutlinedButton(text='Clear completed.')
        clear_button.on_click = command=self.clear_clicked
        clear_row = Row(controls=[self.items_left, clear_button])
        clear_row.alignment = 'spaceBetween'

        view = Column()
        view.width = 600
        view.controls.append(header)
        view.controls.append(task_input_row)
        view.controls.append(Column(controls=[self.tabs, self.tasks]))
        view.controls.append(Column(controls=[clear_row]))

        return view

    def update(self, *args, **kwargs) -> None:
        status = self.tabs.tabs[self.tabs.selected_index].text
        count = 0
        
        for task in self.tasks.controls:
            task.visible = False
            if status == 'active' and task.is_completed == False:
                task.visible = True
            elif status == 'completed' and task.is_completed == True:
                task.visible = True
            elif status == 'all':
                task.visible = True
            if not task.is_completed:
                count += 1

        self.items_left.value = f'{count} active items left.'

        super().update()

    def add_clicked(self, event) -> None:
        task = Task(self.new_task.value, self.task_status_change, self.task_delete)
        self.tasks.controls.append(task)
        self.new_task.value = ''
        self.update()

    def clear_clicked(self, event) -> None:
        print('clear clicked')
        for task in self.tasks.controls[:]:
            if task.is_completed:
                self.task_delete(task)

    def task_status_change(self, task) -> None:
        self.update()

    def task_delete(self, task) -> None:
        self.tasks.controls.remove(task)
        self.update()



def main(page: Page) -> None:
    todo = TodoApp()
    page.controls.append(todo)
    page.horizontal_alignment = 'center'
    page.window_width = 600
    page.window_height = 400
    page.window_center()
    page.bgcolor = '#ffffff'
    page.update()


if __name__ == '__main__':
    app(target=main)

