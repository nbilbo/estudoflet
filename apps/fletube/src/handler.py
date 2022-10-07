import typing

from pytube import YouTube
from pytube.streams import Stream

from src import constants
if typing.TYPE_CHECKING:
    from src.gui import Gui


class Handler:
    def __init__(self, gui: 'Gui'):
        """Configure gui widgets events."""
        self._target = None
        self._youtube = None
        self._audio_streams = None
        self._video_streams = None
        self._audio_video_streams = None
        self.gui = gui

        # config widgets.
        self.gui.search_button.on_click = lambda _: self.search_video()
        self.gui.audio_video_button.on_click = lambda _: self.download_audio_video()
        self.gui.only_audio_button.on_click = lambda _: self.download_only_audio()
        self.gui.only_video_button.on_click = lambda _: self.download_only_video()
        self.restart()


    def restart(self) -> None:
        """
        Back the application to start point.
        """
        self.gui.hide_banner()
        self.gui.hide_progress_bar()
        self.gui.disable_download_buttons() 
        self.gui.show_home_view()

    def search_video(self) -> None:
        """
        Get current searched url and
        prepare the gui to next download step.
        """
        # https://youtu.be/X1p4TerTwok
        # just trying find the video.
        try:
            self.gui.hide_banner()
            self.gui.disable_download_buttons()
            self.gui.display_progress_bar()

            url = self.gui.get_searched_url()
            self._youtube = YouTube(url)
            self._audio_streams = self._youtube.streams.filter(adaptive=True, only_audio=True)
            self._video_streams = self._youtube.streams.filter(adaptive=True, only_video=True)
            self._audio_video_streams = self._youtube.streams.filter(progressive=True)

        # ops, something gets wrong.
        except Exception as e:
            self.gui.display_warning_message(str(e))

        # ok, that's is good.
        else:
            self.gui.enable_download_buttons()

        # just stop the progress bar used to give some feedback.
        finally:
            self.gui.hide_progress_bar()

    def _download_stream(self, stream: Stream, output_path: str) -> None:
        """Start the stream download."""
        try:
            self.gui.hide_banner()
            self.gui.disable_download_buttons()
            self.gui.display_progress_bar()
            stream.download(output_path=output_path)

        except Exception as e:
            message = str(e)
            self.gui.display_warning_message(message)

        else:
            message = f'Download completed, check {output_path} directory.'
            self.gui.display_success_message(message)
            self.gui.enable_download_buttons()

        finally:
            self.gui.hide_progress_bar()

    def download_audio_video(self) -> None:
        """Download audio and video."""
        stream = self._audio_video_streams.last()
        self._download_stream(stream, constants.OUTPUT_DIR)

    def download_only_audio(self) -> None:
        """Download only audio."""
        stream = self._audio_streams.first()
        self._download_stream(stream, constants.OUTPUT_DIR)

    def download_only_video(self) -> None:
        """Download only video."""
        stream = self._video_streams.first()
        self._download_stream(stream, constants.OUTPUT_DIR)

