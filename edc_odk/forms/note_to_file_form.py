from django import forms

from edc_base.sites import SiteModelFormMixin
from edc_form_validators import FormValidatorMixin

from ..models import NoteToFile
from ..models import NoteToFileDocs


class NoteToFileForm(SiteModelFormMixin, FormValidatorMixin, forms.ModelForm):

    class Meta:
        model = NoteToFile
        fields = '__all__'


class NoteToFileDocsForm(forms.ModelForm):

    class Meta:
        model = NoteToFileDocs
        fields = '__all__'
