from django.apps import apps as django_apps
from django.core.exceptions import ObjectDoesNotExist

from .labresults_model_wrapper import LabResultsModelWrapper


class LabResultsModelWrapperMixin:

    labresults_model_wrapper_cls = LabResultsModelWrapper

    @property
    def labresults_model_obj(self):
        """Returns a lab results model instance or None.
        """
        try:
            return self.labresults_cls.objects.get(
                **self.labresults_options)
        except ObjectDoesNotExist:
            return None

    @property
    def lab_results(self):
        """Returns a wrapped saved or unsaved lab results.
        """
        model_obj = self.labresults_model_obj or self.labresults_cls(
            **self.create_labresults_options)
        if 'dashboard' in self.next_url_name:
            next_url_name = self.next_url_name
            return self.labresults_model_wrapper_cls(
                model_obj=model_obj, next_url_name=next_url_name)
        return self.labresults_model_wrapper_cls(model_obj=model_obj)

    @property
    def labresults_cls(self):
        return django_apps.get_model('edc_odk.labresultsfiles')

    @property
    def create_labresults_options(self):
        """Returns a dictionary of options to create a new
        unpersisted lab results model instance.
        """
        options = dict(
            subject_identifier=self.object.subject_identifier)
        return options

    @property
    def labresults_options(self):
        """Returns a dictionary of options to get an existing
        lab results model instance.
        """
        options = dict(
            subject_identifier=self.object.subject_identifier)
        return options
