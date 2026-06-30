
from django import forms
from .models import UserProfile, EmergencyReport
from .nigeria_locations import NIGERIA_LOCATIONS


class RegisterForm(forms.ModelForm):

    state = forms.ChoiceField(
        choices=[
            (state, state)
            for state in NIGERIA_LOCATIONS.keys()
        ]
    )

    lga = forms.CharField()

    confirm_password = forms.CharField(
        widget=forms.PasswordInput()
    )

    class Meta:

        model = UserProfile

        fields = [
            "full_name",
            "username",
            "email",
            "phone_number",
            "state",
            "lga",
            "password"
        ]

        widgets = {
            "password": forms.PasswordInput()
        }

    def clean(self):

        cleaned_data = super().clean()

        password = cleaned_data.get(
            "password"
        )

        confirm_password = cleaned_data.get(
            "confirm_password"
        )

        if password != confirm_password:

            raise forms.ValidationError(
                "Passwords do not match"
            )

        return cleaned_data


class EmergencyReportForm(forms.ModelForm):

    class Meta:

        model = EmergencyReport

        fields = [
            "emergency_type",
            "description",
            "state",
            "lga",
            "address",
            "severity"
        ]

