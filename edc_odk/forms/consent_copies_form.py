from django import forms

from edc_base.sites import SiteModelFormMixin
from edc_form_validators import FormValidatorMixin

from ..models import ConsentCopies
from ..models import ConsentImage


class ConsentCopiesForm(
        SiteModelFormMixin, FormValidatorMixin, forms.ModelForm):

    class Meta:
        model = ConsentCopies
        fields = '__all__'


class ConsentImageForm(forms.ModelForm):

    class Meta:
        model = ConsentImage
        fields = '__all__'
