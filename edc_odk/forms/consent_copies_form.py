from django import forms

from edc_base.sites import SiteModelFormMixin
from edc_form_validators import FormValidatorMixin

from ..models import ConsentCopies
from ..models import ConsentImage, NationalIdentityImage, SpecimenConsentImage


class ConsentCopiesForm(
        SiteModelFormMixin, FormValidatorMixin, forms.ModelForm):

    subject_identifier = forms.CharField(
        label='Subject Identifier',
        widget=forms.TextInput(attrs={'readonly': 'readonly'}),
        required=False)

    class Meta:
        model = ConsentCopies
        fields = '__all__'


class ConsentImageForm(forms.ModelForm):

    class Meta:
        model = ConsentImage
        fields = '__all__'


class SpecimenConsentImageForm(forms.ModelForm):

    class Meta:
        model = NationalIdentityImage
        fields = '__all__'


class NationalIdentityImageForm(forms.ModelForm):

    class Meta:
        model = SpecimenConsentImage
        fields = '__all__'
