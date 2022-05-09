from django import forms
from edc_base.sites import SiteModelFormMixin
from edc_form_validators import FormValidatorMixin

from ..models import ContinuedParticipation, ContinuedParticipationImage


class ContinuedParticipationForm(
        SiteModelFormMixin, FormValidatorMixin, forms.ModelForm):

    subject_identifier = forms.CharField(
        label='Subject Identifier',
        widget=forms.TextInput(attrs={'readonly': 'readonly'}),
        required=False)

    class Meta:
        model = ContinuedParticipation
        fields = '__all__'


class ContinuedParticipationImageForm(forms.ModelForm):

    def has_changed(self):
        return True

    class Meta:
        model = ContinuedParticipationImage
        fields = '__all__'
