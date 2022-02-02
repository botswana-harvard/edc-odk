from django import forms

from edc_base.sites import SiteModelFormMixin
from edc_form_validators import FormValidatorMixin

from ..models import ConsentCopies
from ..models import ConsentImage


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

    def has_changed(self):
        return True

    class Meta:
        model = ConsentImage
        fields = '__all__'
