from django import forms
from edc_base.sites import SiteModelFormMixin
from edc_form_validators import FormValidatorMixin

from ..models import BirthCertificate, BirthCertificateImage


class BirthCertificateForm(
        SiteModelFormMixin, FormValidatorMixin, forms.ModelForm):

    subject_identifier = forms.CharField(
        label='Subject Identifier',
        widget=forms.TextInput(attrs={'readonly': 'readonly'}),
        required=False)

    class Meta:
        model = BirthCertificate
        fields = '__all__'


class BirthCertificateImageForm(forms.ModelForm):

    def has_changed(self):
        return True

    class Meta:
        model = BirthCertificateImage
        fields = '__all__'
