from django.contrib.auth.forms import AuthenticationForm, UserCreationForm


class BootstrapFormMixin:
    def apply_bootstrap_styles(self) -> None:
        for field in self.fields.values():
            field.widget.attrs["class"] = "form-control"
            field.widget.attrs.setdefault("placeholder", field.label)


class SignInForm(BootstrapFormMixin, AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.apply_bootstrap_styles()
        self.fields["username"].widget.attrs["autocomplete"] = "username"
        self.fields["password"].widget.attrs["autocomplete"] = "current-password"


class SignUpForm(BootstrapFormMixin, UserCreationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.apply_bootstrap_styles()
        self.fields["username"].widget.attrs["autocomplete"] = "username"
        self.fields["password1"].widget.attrs["autocomplete"] = "new-password"
        self.fields["password2"].widget.attrs["autocomplete"] = "new-password"
