from django.apps import apps as django_apps
from django.core.exceptions import ObjectDoesNotExist

from .note_to_file_model_wrapper import NoteToFileModelWrapper


class NoteToFileModelWrapperMixin:

    note_to_file_model_wrapper_cls = NoteToFileModelWrapper

    @property
    def note_to_file_model_obj(self):
        """Returns a note to file model instance or None.
        """
        try:
            return self.note_to_file_cls.objects.get(
                **self.note_to_file_options)
        except ObjectDoesNotExist:
            return None

    @property
    def note_to_file(self):
        """Returns a wrapped saved or unsaved note to file.
        """
        model_obj = self.note_to_file_model_obj or self.note_to_file_cls(
            **self.create_note_to_file_options)
        if 'subject_dashboard' in self.next_url_name:
            next_url_name = self.next_url_name
            return self.note_to_file_model_wrapper_cls(
                model_obj=model_obj, next_url_name=next_url_name)
        return self.note_to_file_model_wrapper_cls(model_obj=model_obj)

    @property
    def note_to_file_cls(self):
        return django_apps.get_model('edc_odk.notetofile')

    @property
    def create_note_to_file_options(self):
        """Returns a dictionary of options to create a new
        unpersisted note to file model instance.
        """
        options = dict(
            subject_identifier=self.object.subject_identifier)
        return options

    @property
    def note_to_file_options(self):
        """Returns a dictionary of options to get an existing
        note to file model instance.
        """
        options = dict(
            subject_identifier=self.object.subject_identifier)
        return options
