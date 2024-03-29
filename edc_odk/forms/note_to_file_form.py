from django import forms

from edc_base.sites import SiteModelFormMixin
from edc_form_validators import FormValidatorMixin

from ..models import NoteToFile
from ..models import NoteToFileDocs


class NoteToFileForm(SiteModelFormMixin, FormValidatorMixin, forms.ModelForm):

    subject_identifier = forms.CharField(
        label='Subject Identifier',
        widget=forms.TextInput(attrs={'readonly': 'readonly'}),
        required=False)

    class Meta:
        model = NoteToFile
        fields = '__all__'


class NoteToFileDocsForm(forms.ModelForm):

    def has_changed(self):
        return True

    class Meta:
        model = NoteToFileDocs
        fields = '__all__'
