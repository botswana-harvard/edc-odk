from django import forms

from edc_base.sites import SiteModelFormMixin
from edc_form_validators import FormValidatorMixin

from ..models import OmangCopies
from ..models import NationalIdentityImage


class OmangCopiesForm(
        SiteModelFormMixin, FormValidatorMixin, forms.ModelForm):

    subject_identifier = forms.CharField(
        label='Subject Identifier',
        widget=forms.TextInput(attrs={'readonly': 'readonly'}),
        required=False)

    class Meta:
        model = OmangCopies
        fields = '__all__'


class NationalIdentityImageForm(forms.ModelForm):

    def has_changed(self):
        return True

    class Meta:
        model = NationalIdentityImage
        fields = '__all__'
