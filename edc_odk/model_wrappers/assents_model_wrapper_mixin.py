from django.apps import apps as django_apps
from django.core.exceptions import ObjectDoesNotExist

from .assents_model_wrapper import AssentsModelWrapper


class AssentsModelWrapperMixin:
    assents_model_wrapper_cls = AssentsModelWrapper

    @property
    def assents_model_obj(self):
        """Returns a assents model instance or None.
        """
        try:
            return self.assents_cls.objects.get(
                **self.assents_options)
        except ObjectDoesNotExist:
            return None

    @property
    def assents(self):
        """Returns a wrapped saved or unsaved assents.
        """
        model_obj = self.assents_model_obj or self.assents_cls(
            **self.create_assents_options)
        if 'dashboard' in self.next_url_name:
            next_url_name = self.next_url_name
            return self.assents_model_wrapper_cls(
                model_obj=model_obj, next_url_name=next_url_name)
        return self.assents_model_wrapper_cls(model_obj=model_obj)

    @property
    def assents_cls(self):
        return django_apps.get_model('edc_odk.assent')

    @property
    def create_assents_options(self):
        """ Returns a dictionary of options to create a new
            unpersisted assents model instance.
        """
        options = dict(
            subject_identifier=self.object.subject_identifier)
        return options

    @property
    def assents_options(self):
        """ Returns a dictionary of options to get an existing assents
            model instance.
        """
        options = dict(
            subject_identifier=self.object.subject_identifier)
        return options
