from django import forms
from edc_base.sites import SiteModelFormMixin
from edc_form_validators import FormValidatorMixin

from ..models import ClinicianNotesArchives, ClinicianNotesImageArchive


class ClinicianNotesArchivesForm(
        SiteModelFormMixin, FormValidatorMixin, forms.ModelForm):

    subject_identifier = forms.CharField(
        label='Subject Identifier',
        widget=forms.TextInput(attrs={'readonly': 'readonly'}),
        required=False)

    class Meta:
        model = ClinicianNotesArchives
        fields = '__all__'


class ClinicianNotesImageArchiveForm(forms.ModelForm):

    def has_changed(self):
        return True

    class Meta:
        model = ClinicianNotesImageArchive
        fields = '__all__'
