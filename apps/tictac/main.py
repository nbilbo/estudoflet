import typing
from random import choice
from random import randint

from flet import AppBar
from flet import Column
from flet import Container
from flet import Icon
from flet import IconButton
from flet import Page
from flet import Row
from flet import Text
from flet import TextButton
from flet import View
from flet import border
from flet import icons


PADDING = 15


class BoardCell(Container):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.expand = 1
        self.padding = PADDING
        self.border = border.all(5, 'blue')
        self.text = Text()
        self.text.style = 'displayLarge'
        self.text.text_align = 'center'
        self.on_click = lambda _: None
        self.content = self.text


class BoardRow(Container):
    def __init__(self, *args, **kwargs) -> None:
        """
        Row with three cells.
        """
        super().__init__(*args, **kwargs)
        self.expand = 1
        self.padding = PADDING
        # self.border = border.all(5, 'green')
        self.cell_0 = BoardCell()
        self.cell_1 = BoardCell()
        self.cell_2 = BoardCell()

        content = Row()
        content.controls.append(self.cell_0)
        content.controls.append(self.cell_1)
        content.controls.append(self.cell_2)
        self.content = content

    def cells(self) -> typing.List[BoardCell]:
        return [self.cell_0, self.cell_1, self.cell_2]


class Board(Container):
    def __init__(self, *args, **kwargs) -> None:
        """
        Board with three rows.
        """
        super().__init__(*args, **kwargs)
        self.expand = 1
        self.padding = PADDING
        self.border = border.all(5, 'red')
        self.row_0 = BoardRow()
        self.row_1 = BoardRow()
        self.row_2 = BoardRow()

        content = Column()
        content.controls.append(self.row_0)
        content.controls.append(self.row_1)
        content.controls.append(self.row_2)
        self.content = content

    def rows(self) -> typing.List[BoardRow]:
        return [self.row_0, self.row_1, self.row_2]


class FeedbackBar(Container):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.border = border.all(5, 'pink')
        self.text = Text()
        self.text.style = 'displayMedium'

        content = Row([self.text], alignment='center')
        self.content = content


class GameAppBar(AppBar):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.leading = Icon(icons.GAMEPAD)
        self.back_button = IconButton(icons.EXIT_TO_APP)
        self.back_button.icon_size = 32
        self.back_button.tooltip = 'Back to home screen'
        self.actions.append(self.back_button)


class CreditsView(View):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.route = '/credits'
        self.app_bar = GameAppBar()

        programming_text = Text()
        programming_text.style = 'displayMedium'
        programming_text.value = 'Programming: Nbilbo'

        column = Column()
        column.alignment = 'center'
        column.controls.append(Row([programming_text], alignment='center'))

        self.controls.append(self.app_bar)
        self.controls.append(Container(column, expand=1))


class GameView(View):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.route = '/game'
        self.board = Board()
        self.feedback_bar = FeedbackBar()
        self.app_bar = GameAppBar()
        self.controls.append(self.app_bar)
        self.controls.append(self.board)
        self.controls.append(self.feedback_bar)


class HomeView(View):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.route = '/'
        self.new_game_button = TextButton()
        self.credits_button = TextButton()
        self.new_game_button.text = 'Start New Game'
        self.credits_button.text = 'Credits'

        column = Column()
        column.alignment = 'center'
        column.controls.append(Row([self.new_game_button], alignment='center'))
        column.controls.append(Row([self.credits_button], alignment='center'))

        content = Container(column, expand=1, border=border.all(5, 'gray'))
        self.controls.append(content)


class Application(object):
    def __init__(self, page: Page) -> None:
        # creating all graphical components.
        self.home_view = HomeView()
        self.game_view = GameView()
        self.credits_view = CreditsView()
        self.page = page
        self.page.views.append(self.home_view)
        self.page.views.append(self.game_view)
        self.page.views.append(self.credits_view)
        self.page.on_route_change = self._on_route_change
        self.page.go('/')

        # this will configure all events.
        self.handler = Handler(self)

    def _on_route_change(self, route) -> None:
        """
        Inner method, dont call this directly.
        """
        for view in self.page.views:
            if view.route == self.page.route:
                self.page.views.remove(view)
                self.page.views.append(view)
                break

    @property
    def new_game_button(self) -> TextButton:
        return self.home_view.new_game_button

    @property
    def credits_button(self) -> TextButton:
        return self.home_view.credits_button

    @property
    def game_bar_back_button(self) -> IconButton:
        return self.game_view.app_bar.back_button

    @property
    def credits_bar_back_button(self) -> IconButton:
        return self.credits_view.app_bar.back_button

    def go_home_view(self) -> None:
        """
        Go to home view.
        """
        self.page.go('/')

    def go_credits_view(self) -> None:
        """
        Go to credits view.
        """
        self.page.go('/credits')

    def go_game_view(self) -> None:
        """
        Go to game view.
        """
        self.page.go('/game')

    def rows(self) -> typing.List[BoardRow]:
        """
        Return a list with all board rows.
        """
        board = self.game_view.board
        return [board.row_0, board.row_1, board.row_2]

    def cells(self) -> typing.List[BoardCell]:
        """
        Return a list width all board cells.
        """
        board = self.game_view.board
        return board.row_0.cells() + board.row_1.cells() + board.row_2.cells()

    def cell_index(
        self, cell: 'BoardCell'
    ) -> typing.Optional[typing.Tuple[int, int]]:
        """
        Return cell index.
        """
        for i, board_row in enumerate(self.rows()):
            for j, board_cell in enumerate(board_row.cells()):
                if cell == board_cell:
                    return (i, j)
        return None

    def fill_board(self, matrix: typing.List[typing.List[str]]) -> None:
        """
        Fill the board.
        """
        for i, board_row in enumerate(self.rows()):
            for j, board_cell in enumerate(board_row.cells()):
                board_cell.text.value = matrix[i][j]
        self.page.update()

    def display_game_feedback(self, message: str) -> None:
        """
        Display a message in game view.
        """
        self.game_view.feedback_bar.text.value = message
        self.page.update()


class Handler(object):
    def __init__(self, application: 'Application') -> None:
        """
        Configure all application widgets events.
        """
        self.backend = Backend()
        self.application = application
        self.messages = [
            'Very well.',
            'Nice play.',
            'Dont give up.',
            'Keep trying.',
        ]
        self.restart_game()

        self.application.credits_button.on_click = (
            lambda _: self.go_credits_view()
        )
        self.application.new_game_button.on_click = (
            lambda _: self.go_game_view()
        )
        self.application.game_bar_back_button.on_click = (
            lambda _: self.go_home_view()
        )
        self.application.credits_bar_back_button.on_click = (
            lambda _: self.go_home_view()
        )

    def bind_cells(self) -> None:
        for cell in self.application.cells():
            cell.on_click = self.cell_clicked

    def unbind_cells(self) -> None:
        for cell in self.application.cells():
            cell.on_click = None

    def cell_clicked(self, event: 'BoardCell') -> None:
        try:
            x, y = self.application.cell_index(event.control)
            self.backend.player_turn(x, y)
            self.application.fill_board(self.backend.matrix)
            self.application.display_game_feedback(choice(self.messages))
            self.backend.cpu_turn()
            self.application.fill_board(self.backend.matrix)

        except AlreadyUsedError:
            self.application.display_game_feedback(
                'Hey, this field has already used.'
            )

        else:
            self.check()

    def restart_game(self) -> None:
        """
        Restart the game.
        """
        self.backend.reset_matrix()
        self.application.fill_board(self.backend.matrix)
        self.application.display_game_feedback(
            'Welcome, try win against our machine.'
        )
        self.bind_cells()

    def check(self) -> None:
        """
        Check if someone has wined the game.
        """
        winner = self.backend.look_for_winner()
        has_empty_space = self.backend.has_empty_space()

        if winner:
            self.unbind_cells()
            if winner == self.backend.player_symbol:
                self.application.display_game_feedback('Congratulations!!!')
            elif winner == self.backend.cpu_symbol:
                self.application.display_game_feedback(
                    'Hey, you lose but you can try again :)'
                )

        elif not has_empty_space:
            self.unbind_cells()
            self.application.display_game_feedback(
                'This is a draw, try again!!!'
            )

    def go_credits_view(self) -> None:
        self.application.go_credits_view()

    def go_home_view(self) -> None:
        self.application.go_home_view()

    def go_game_view(self) -> None:
        self.restart_game()
        self.application.go_game_view()


class Backend(object):
    def __init__(self) -> None:
        self.player_symbol = 'X'
        self.cpu_symbol = 'O'
        self.matrix = None
        self.reset_matrix()

    def reset_matrix(self) -> None:
        self.matrix = [['' for _ in range(3)] for _ in range(3)]

    def has_empty_space(self) -> bool:
        """
        Check if exists a empty space in  the `matrix`.
        """
        for row in self.matrix:
            for column in row:
                if column == '':
                    return True

        return False

    def player_turn(self, x: int, y: int) -> None:
        """
        Fill a matrix element with `player_symbol`.
        """
        if self.matrix[x][y] != '':
            raise AlreadyUsedError

        self.matrix[x][y] = self.player_symbol

    def cpu_turn(self) -> None:
        """
        Fill a matrix element with `cpu_symbol`. The cpu only play
        if have a empty space and no winner.
        """
        if (self.has_empty_space()) and (not self.look_for_winner()):
            while True:
                random_row = randint(0, 2)
                random_column = randint(0, 2)
                if self.matrix[random_row][random_column] == '':
                    break
            self.matrix[random_row][random_column] = self.cpu_symbol

    def look_for_winner(self) -> typing.Optional[str]:
        """
        Check all matrix directions to find for a winner.
        """
        for look in (
            self.look_for_horizontal_winner,
            self.look_for_vertical_winner,
            self.look_for_diagonal_winner,
            self.look_for_reverse_diagonal_winner,
        ):
            winner = look()
            if winner:
                return winner

        return None

    def look_for_horizontal_winner(self) -> typing.Optional[str]:
        """
        Check horizontal direction to find for a winner.
        """
        for row in self.matrix:
            for column in row:
                if (column != '') and (row.count(column) == len(row)):
                    return column

        return None

    def look_for_vertical_winner(self) -> typing.Optional[str]:
        """
        Check for vertical direction to find for a winner.
        """
        aux = []

        for column in range(len(self.matrix[0])):
            for row in range(len(self.matrix)):
                aux.append(self.matrix[row][column])
            if (aux.count(aux[0]) == len(aux)) and (aux[0] != ''):
                return aux[0]
            else:
                aux = []

        return None

    def look_for_diagonal_winner(self) -> typing.Optional[str]:
        """
        Check diagonal direction to find for a winner.
        """
        aux = []
        for i in range(len(self.matrix)):
            for j in range(len(self.matrix[i])):
                if i == j:
                    aux.append(self.matrix[i][j])

        if (aux[0] != '') and (aux.count(aux[0]) == len(self.matrix)):
            return aux[0]

        return None

    def look_for_reverse_diagonal_winner(self) -> typing.Optional[str]:
        """
        Check reverse-diagonal direction to find for a winner.
        """
        aux = []
        for i in range(len(self.matrix)):
            for j in range(len(self.matrix[i])):
                if i + j == len(self.matrix) - 1:
                    aux.append(self.matrix[i][j])

        if (aux[0] != '') and (aux.count(aux[0]) == len(self.matrix)):
            return aux[0]

        return None


class AlreadyUsedError(Exception):
    pass


if __name__ == '__main__':
    from flet import app

    app(target=Application)
