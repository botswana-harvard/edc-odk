from django import forms
from edc_base.sites import SiteModelFormMixin
from edc_form_validators import FormValidatorMixin

from ..models import Assent, AssentImage


class AssentForm(
        SiteModelFormMixin, FormValidatorMixin, forms.ModelForm):

    subject_identifier = forms.CharField(
        label='Subject Identifier',
        widget=forms.TextInput(attrs={'readonly': 'readonly'}),
        required=False)

    class Meta:
        model = Assent
        fields = '__all__'


class AssentImageForm(forms.ModelForm):

    def has_changed(self):
        return True

    class Meta:
        model = AssentImage
        fields = '__all__'
