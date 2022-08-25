import time
import flet


def button_clicked(event):
    attrs = [attr for attr in dir(event) if not attr.startswith('__')]
    # ['control', 'data', 'name', 'page', 'target']
    print('-'*10)
    print('button clicked.')
    print('control:', event.control)
    print('data:', event.data)
    print('name:', event.page)
    print('target:', event.target)
    print('-'*10)


def main(page: flet.Page) -> None:
    text = flet.Text()
    text.value = 'Hello, world.'
    text.color = 'green'
    page.controls.append(text)
    page.update()

    row = flet.Row()
    row.controls.append(flet.Text('first phrase'))
    row.controls.append(flet.Text('second phrase'))
    page.controls.append(row)
    page.update()

    text_field = flet.TextField(label='Your name')
    elevate_button = flet.ElevatedButton(text='Say my name')
    elevate_button.on_click = button_clicked
    second_row = flet.Row()
    second_row.controls.append(text_field)
    second_row.controls.append(elevate_button)
    page.controls.append(second_row)
    page.update()
    
    for count in range(10):
        text.value = f'Count: {count}'
        time.sleep(1)
        page.update()


flet.app(target=main)
