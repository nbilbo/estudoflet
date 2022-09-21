import typing
from flet import (
    AppBar,
    Icon,
    IconButton,
    Page,
    Row,
    Text,
    TextButton,
    TextField,
    View,
    icons,
)


class HomeView(View):
    def __init__(self, *args, **kwargs) -> None:
        """
        Home view.
        """
        super().__init__(*args, **kwargs)
        self.route = '/'

        self.logout_button = IconButton()
        self.logout_button.icon = icons.LOGOUT
        self.logout_button.tooltip = 'Logout'

        app_bar = AppBar()
        app_bar.leading = Icon(icons.ANDROID)
        app_bar.title = Text('Home')
        app_bar.actions = [self.logout_button]

        title = Text()
        title.value = 'Welcome'
        title.style = 'displayMedium'

        self.controls = [app_bar, Row([title], alignment='center')]


class LoginView(View):
    def __init__(self, *args, **kwargs) -> None:
        """
        Organize controllers to receive login inputs.
        """
        super().__init__(*args, **kwargs)
        self.route = '/login'

        app_bar = AppBar()
        app_bar.leading = Icon(icons.ANDROID)
        app_bar.title = Text('Sign in')

        self.username_field = TextField()
        self.username_field.label = 'Username'

        self.password_field = TextField()
        self.password_field.label = 'Password'
        self.password_field.password = True
        self.password_field.can_reveal_password = True

        self.login_button = TextButton()
        self.login_button.text = 'Sign in'

        self.register_button = TextButton()
        self.register_button.text = 'Dont have an account? Sign Up'

        self.controls = [
            app_bar,
            self.username_field,
            self.password_field,
            self.login_button,
            self.register_button,
        ]


class RegisterView(View):
    def __init__(self, *args, **kwargs) -> None:
        """
        Organize controllers to receive register inputs.
        """
        super().__init__(*args, **kwargs)
        self.route = '/register'

        app_bar = AppBar()
        app_bar.leading = Icon(icons.ANDROID)
        app_bar.title = Text('Sign up')

        self.fullname_field = TextField()
        self.fullname_field.label = 'Full Name'

        self.email_field = TextField()
        self.email_field.label = 'E-mail'

        self.username_field = TextField()
        self.username_field.label = 'Username'

        self.password1_field = TextField()
        self.password1_field.label = 'Password'
        self.password1_field.password = True
        self.password1_field.can_reveal_password = True

        self.password2_field = TextField()
        self.password2_field.label = 'Repeat Password'
        self.password2_field.password = True
        self.password2_field.can_reveal_password = True

        self.register_button = TextButton()
        self.register_button.text = 'Sign up'

        self.login_button = TextButton()
        self.login_button.text = 'Already have an account? Sign in'

        self.controls = [
            app_bar,
            self.fullname_field,
            self.email_field,
            self.username_field,
            self.password1_field,
            self.password2_field,
            self.register_button,
            self.login_button,
        ]


class MainView(View):
    def __init__(self, page: Page) -> None:
        """
        Create and organize all others views.
        """
        super().__init__()
        self.page = page
        self.route = '/'
        self.home_view = HomeView()
        self.login_view = LoginView()
        self.register_view = RegisterView()
        self.page.views.append(self.home_view)
        self.page.views.append(self.login_view)
        self.page.views.append(self.register_view)

        self.login_button.on_click = lambda _: self.go_home_view()
        self.register_button.on_click = lambda _: self.go_home_view()
        self.logout_button.on_click = lambda _: self.go_login_view()
        self.dont_have_account_button.on_click = (
            lambda _: self.go_register_view()
        )
        self.already_have_account_button.on_click = (
            lambda _: self.go_login_view()
        )

    @property
    def login_button(self) -> TextButton:
        return self.login_view.login_button

    @property
    def register_button(self) -> TextButton:
        return self.register_view.register_button

    @property
    def dont_have_account_button(self) -> TextButton:
        return self.login_view.register_button

    @property
    def already_have_account_button(self) -> TextButton:
        return self.register_view.login_button

    @property
    def logout_button(self) -> IconButton:
        return self.home_view.logout_button

    def go_home_view(self) -> None:
        self.page.go('/')
        print(f'login form: {self.login_form()}')
        print(f'register form: {self.register_form()}')
        self.clear_login_form()
        self.clear_register_form()

    def go_login_view(self) -> None:
        self.page.go('/login')

    def go_register_view(self) -> None:
        self.page.go('/register')

    def login_form(self) -> typing.Dict[typing.Any, typing.Any]:
        """
        Return a dict with login fields values.
        """
        username_field = self.login_view.username_field
        password_field = self.login_view.password_field

        username = username_field.value.strip()
        password = password_field.value.strip()

        result = {}
        result['username'] = username or None
        result['password'] = password or None

        return result

    def register_form(self) -> typing.Dict[typing.Any, typing.Any]:
        """
        Return a dict with register fields values.
        """
        fullname_field = self.register_view.fullname_field
        email_field = self.register_view.email_field
        username_field = self.register_view.username_field
        password1_field = self.register_view.password1_field
        password2_field = self.register_view.password2_field

        fullname = fullname_field.value.strip()
        email = email_field.value.strip()
        username = username_field.value.strip()
        password1 = password1_field.value.strip()
        password2 = password2_field.value.strip()

        result = {}
        result['fullname'] = fullname or None
        result['email'] = email or None
        result['username'] = username or None
        result['password1'] = password1 or None
        result['password2'] = password2 or None

        return result

    def clear_login_form(self) -> None:
        """
        Clear all login form fields.
        """
        self.login_view.username_field.value = ''
        self.login_view.password_field.value = ''

    def clear_register_form(self) -> None:
        """
        Clear all register form fields.
        """
        self.register_view.fullname_field.value = ''
        self.register_view.email_field.value = ''
        self.register_view.username_field.value = ''
        self.register_view.password1_field.value = ''
        self.register_view.password2_field.value = ''


def main(page: Page):
    def route_change(route):
        for view in page.views:
            if view.route == page.route:
                page.views.remove(view)
                page.views.append(view)
                break

    page.on_route_change = route_change
    main_view = MainView(page)
    main_view.go_login_view()


if __name__ == '__main__':
    from flet import app, WEB_BROWSER

    # app(target=main, view=WEB_BROWSER)
    app(target=main)
