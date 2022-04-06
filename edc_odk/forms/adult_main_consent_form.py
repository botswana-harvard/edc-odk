from django import forms
from edc_base.sites import SiteModelFormMixin
from edc_form_validators import FormValidatorMixin

from ..models import AdultMainConsent, AdultMainConsentImage


class AdultMainConsentForm(
        SiteModelFormMixin, FormValidatorMixin, forms.ModelForm):

    subject_identifier = forms.CharField(
        label='Subject Identifier',
        widget=forms.TextInput(attrs={'readonly': 'readonly'}),
        required=False)

    class Meta:
        model = AdultMainConsent
        fields = '__all__'


class AdultMainConsentImageForm(forms.ModelForm):

    def has_changed(self):
        return True

    class Meta:
        model = AdultMainConsentImage
        fields = '__all__'
