from django.apps import apps as django_apps
from django.core.exceptions import ObjectDoesNotExist

from .continued_participation_model_wrapper import ContinuedParticipationModelWrapper


class ContinuedParticipationModelWrapperMixin:
    continued_participation_model_wrapper_cls = ContinuedParticipationModelWrapper

    @property
    def continued_participation_model_obj(self):
        """Returns a continued participation model instance or None.
        """
        try:
            return self.continued_participation_cls.objects.get(
                **self.continued_participation_options)
        except ObjectDoesNotExist:
            return None

    @property
    def continued_participation(self):
        """Returns a wrapped saved or unsaved continued participation.
        """
        model_obj = self.continued_participation_model_obj or self.continued_participation_cls(
            **self.create_continued_participation_options)
        if 'dashboard' in self.next_url_name:
            next_url_name = self.next_url_name
            return self.continued_participation_model_wrapper_cls(
                model_obj=model_obj, next_url_name=next_url_name)
        return self.continued_participation_model_wrapper_cls(model_obj=model_obj)

    @property
    def continued_participation_cls(self):
        return django_apps.get_model('edc_odk.continuedparticipation')

    @property
    def create_continued_participation_options(self):
        """ Returns a dictionary of options to create a new
            unpersisted continued participation model instance.
        """
        options = dict(
            subject_identifier=self.object.subject_identifier)
        return options

    @property
    def continued_participation_options(self):
        """ Returns a dictionary of options to get an existing continued participation
            model instance.
        """
        options = dict(
            subject_identifier=self.object.subject_identifier)
        return options
