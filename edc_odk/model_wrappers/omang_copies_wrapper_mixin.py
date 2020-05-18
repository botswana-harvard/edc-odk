from django.apps import apps as django_apps
from django.core.exceptions import ObjectDoesNotExist

from .omang_copies_model_wrapper import OmangCopiesModelWrapper


class OmangCopiesModelWrapperMixin:

    omang_copies_model_wrapper_cls = OmangCopiesModelWrapper

    @property
    def omang_copies_model_obj(self):
        """Returns a omang copies model instance or None.
        """
        try:
            return self.omang_copies_cls.objects.get(
                **self.omang_copies_options)
        except ObjectDoesNotExist:
            return None

    @property
    def omang_copies(self):
        """Returns a wrapped saved or unsaved omang copies.
        """
        model_obj = self.omang_copies_model_obj or self.omang_copies_cls(
            **self.create_omang_copies_options)
        return self.omang_copies_model_wrapper_cls(model_obj=model_obj)

    @property
    def omang_copies_cls(self):
        return django_apps.get_model('edc_odk.omangcopies')

    @property
    def create_omang_copies_options(self):
        """Returns a dictionary of options to create a new
        unpersisted omang copies model instance.
        """
        options = dict(
            subject_identifier=self.object.subject_identifier)
        return options

    @property
    def omang_copies_options(self):
        """Returns a dictionary of options to get an existing
        omang copies model instance.
        """
        options = dict(
            subject_identifier=self.object.subject_identifier)
        return options
