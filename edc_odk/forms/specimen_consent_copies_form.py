from django import forms

from edc_base.sites import SiteModelFormMixin
from edc_form_validators import FormValidatorMixin

from ..models import SpecimenConsentCopies
from ..models import SpecimenConsentImage


class SpecimenConsentCopiesForm(
        SiteModelFormMixin, FormValidatorMixin, forms.ModelForm):

    class Meta:
        model = SpecimenConsentCopies
        fields = '__all__'


class SpecimenConsentImageForm(forms.ModelForm):

    class Meta:
        model = SpecimenConsentImage
        fields = '__all__'
