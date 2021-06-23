from django.db import models
from django.db.models.deletion import PROTECT
from edc_base.model_mixins import BaseUuidModel
from edc_base.utils import get_utcnow


class Appointment(BaseUuidModel):

    subject_identifier = models.CharField(max_length=25)

    appt_datetime = models.DateTimeField(default=get_utcnow)

    visit_code = models.CharField(max_length=25)


class SubjectVisit(BaseUuidModel):

    report_datetime = models.DateTimeField(default=get_utcnow)

    appointment = models.OneToOneField(Appointment, on_delete=PROTECT)

    subject_identifier = models.CharField(max_length=50)

    visit_code = models.CharField(max_length=25)

    visit_code_sequence = models.IntegerField()


class ClinicianNotes(BaseUuidModel):

    report_datetime = models.DateTimeField(default=get_utcnow)

    subjectvisit = models.OneToOneField(SubjectVisit, on_delete=PROTECT)


class ClinicianNotesImage(BaseUuidModel):

    clinician_notes = models.ForeignKey(ClinicianNotes, on_delete=models.PROTECT)

    image = models.ImageField(upload_to='test_images/')

    user_uploaded = models.CharField(max_length=50, blank=True)

    datetime_captured = models.DateTimeField(default=get_utcnow)
