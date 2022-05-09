from django import forms
from edc_base.sites import SiteModelFormMixin
from edc_form_validators import FormValidatorMixin

from ..models import ParentalConsent, ParentalConsentImage


class ParentalConsentForm(
        SiteModelFormMixin, FormValidatorMixin, forms.ModelForm):

    subject_identifier = forms.CharField(
        label='Subject Identifier',
        widget=forms.TextInput(attrs={'readonly': 'readonly'}),
        required=False)

    class Meta:
        model = ParentalConsent
        fields = '__all__'


class ParentalConsentImageForm(forms.ModelForm):

    def has_changed(self):
        return True

    class Meta:
        model = ParentalConsentImage
        fields = '__all__'
