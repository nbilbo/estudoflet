import typing
from flet import AppBar
from flet import Banner
from flet import Column
from flet import Container        
from flet import GridView
from flet import Icon
from flet import Image
from flet import ListView
from flet import OutlinedButton
from flet import Page
from flet import ProgressBar
from flet import Text
from flet import TextButton
from flet import TextField
from flet import Row
from flet import View
from flet import colors
from flet import icons
from src.handler import Handler



class CustomBanner(Banner):
    def __init__(self) -> None:
        """Custom Banner."""
        super().__init__()
        self.text = Text()
        self.text.weight = 'bold'
        self.content = self.text
        self.actions.append(TextButton('Ok', on_click=lambda _:self.close()))

    def close(self) -> None:
        self.open = False
        self.update()


class CustomAppBar(AppBar):
    def __init__(self) -> None:
        """Custom App Bar."""
        super().__init__()
        self.leading = Icon(icons.VIDEOCAM)
        self.title = Text('Fletube Downloader')


class HomeView(View):
    def __init__(self) -> None:
        """Organize all Home View widgets."""
        super().__init__()
        self.route = '/'

        self.appbar = CustomAppBar()

        self.url_field = TextField()
        self.url_field.expand = True
        self.url_field.label = 'Youtube video url'
        self.url_field.hint_text = 'https://youtu.be/X1p4TerTwok'

        self.search_button = OutlinedButton()
        self.search_button.expand = True
        self.search_button.text = 'Search'
        self.search_button.icon = Icon(name=icons.YOUTUBE_SEARCHED_FOR)

        self.only_audio_button = OutlinedButton()
        self.only_video_button = OutlinedButton()
        self.audio_video_button = OutlinedButton()
        self.only_audio_button.text = 'Only Audio'
        self.only_video_button.text = 'Only Video'
        self.audio_video_button.text = 'Audio and Video'
        self.only_audio_button.icon = Icon(name=icons.DOWNLOAD)
        self.only_video_button.icon = Icon(name=icons.DOWNLOAD)
        self.audio_video_button.icon = Icon(name=icons.DOWNLOAD)

        download_options = Row()
        download_options.alignment = 'center'
        download_options.controls.append(self.audio_video_button)
        download_options.controls.append(self.only_audio_button)
        download_options.controls.append(self.only_video_button)

        self.progress_bar = ProgressBar()
        self.progress_bar.color = colors.AMBER
        self.progress_bar.expand = True
        self.progress_bar.value = 0

        column = Column()
        column.alignment = 'spaceAround'
        column.controls.append(Row([self.url_field]))
        column.controls.append(Row([self.search_button]))
        column.controls.append(download_options)
        column.controls.append(Row([self.progress_bar]))
        content = Container(column, expand=1)
        self.controls.append(content)


class Gui:
    def __init__(self, page: Page) -> None:
        """Construct the graphical user interface."""
        self.page = page
        self.home_view = HomeView()
        self.page.banner = CustomBanner()
        self.page.views.append(self.home_view)
        self.page.on_route_change = self._on_route_change
        self.handler = Handler(self)

    def _on_route_change(self, route) -> None:
        """Inner method, dont call this directly."""
        for view in self.page.views:
            if view.route == self.page.route:
                self.page.views.remove(view)
                self.page.views.append(view)
                break

    def show_home_view(self) -> None:
        """Show home view."""
        self.page.go(self.home_view.route)

    def display_warning_message(self, message: str) -> None:
        """Display a warning message."""
        leading = Icon(icons.WARNING_AMBER_ROUNDED, color=colors.AMBER, size=40)
        self.page.banner.leading = leading
        self.page.banner.bgcolor = colors.AMBER_100
        self.page.banner.text.value = message
        self.page.banner.open = True
        self.page.update()

    def display_success_message(self, message: str) -> None:
        """Display a success message."""
        leading = Icon(icons.DONE_ALL_ROUNDED, color=colors.GREEN, size=40)
        self.page.banner.leading = leading
        self.page.banner.bgcolor = colors.GREEN_100
        self.page.banner.text.value = message
        self.page.banner.open = True
        self.page.update()
    
    def disable_download_buttons(self) -> None:
        """Disable all download buttons."""
        self.home_view.only_audio_button.disabled = True
        self.home_view.only_video_button.disabled = True
        self.home_view.audio_video_button.disabled = True
        self.page.update()

    def enable_download_buttons(self) -> None:
        """Enable all download buttons."""
        self.home_view.only_audio_button.disabled = False 
        self.home_view.only_video_button.disabled = False
        self.home_view.audio_video_button.disabled = False 
        self.page.update()

    def display_progress_bar(self) -> None:
        """Display the progress bar."""
        self.home_view.progress_bar.value = None
        self.page.update()

    def hide_progress_bar(self) -> None:
        """Hide the progress bar."""
        self.home_view.progress_bar.value = 0
        self.page.update()

    def hide_banner(self) -> None:
        """Hide the banner."""
        self.page.banner.open = False
        self.page.update()

    def get_searched_url(self) -> typing.Optional[str]:
        """Return the searched url."""
        url = self.home_view.url_field.value
        return url if url else None

    @property
    def search_button(self) -> OutlinedButton:
        return self.home_view.search_button

    @property
    def audio_video_button(self) -> OutlinedButton:
        return self.home_view.audio_video_button

    @property
    def only_audio_button(self) -> OutlinedButton:
        return self.home_view.only_audio_button
    
    @property
    def only_video_button(self) -> OutlinedButton:
        return self.home_view.only_video_button

