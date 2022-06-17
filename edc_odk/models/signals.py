import os
from datetime import datetime

import pyminizip
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from edc_base.utils import get_utcnow

from .adult_main_consent import AdultMainConsentImage
from .assent import AssentImage
from .birth_certificate import BirthCertificateImage
from .clinician_notes_archives import ClinicianNotesImageArchive
from .consent_copies import ConsentImage
from .continued_participation import ContinuedParticipationImage
from .lab_results_files import LabResultsFile
from .note_to_file import NoteToFileDocs
from .omang_copies import NationalIdentityImage
from .parental_consent import ParentalConsentImage
from .specimen_consent_copies import SpecimenConsentImage
import PIL
from PIL import Image


@receiver(post_save, weak=False, sender=NationalIdentityImage,
          dispatch_uid='maternal_dataset_on_post_save')
def natinal_identity_image_on_post_save(sender, instance, raw, created, **kwargs):
    if not raw and created:
        stamp_image(instance)
        subject_identifier = instance.omang_copies.subject_identifier
        encrypt_files(instance, subject_identifier)


@receiver(post_save, weak=False, sender=BirthCertificateImage,
          dispatch_uid='birth_certificate_on_post_save')
def birth_certificate_image_on_post_save(sender, instance, raw, created, **kwargs):
    if not raw and created:
        stamp_image(instance)
        subject_identifier = instance.birth_certificate.subject_identifier
        encrypt_files(instance, subject_identifier)


@receiver(post_save, weak=False, sender=AdultMainConsentImage,
          dispatch_uid='adult_main_consent_on_post_save')
def adult_main_consent_image_on_post_save(sender, instance, raw, created, **kwargs):
    if not raw and created:
        stamp_image(instance)
        subject_identifier = instance.adult_main_consent.subject_identifier
        encrypt_files(instance, subject_identifier)


@receiver(post_save, weak=False, sender=ParentalConsentImage,
          dispatch_uid='parental_consent_image_on_post_save')
def parental_consent_image_on_post_save(sender, instance, raw, created, **kwargs):
    if not raw and created:
        stamp_image(instance)
        subject_identifier = instance.parental_consent.subject_identifier
        encrypt_files(instance, subject_identifier)


@receiver(post_save, weak=False, sender=ContinuedParticipationImage,
          dispatch_uid='continued_participation_image_on_post_save')
def continued_participation_image_on_post_save(sender, instance, raw, created, **kwargs):
    if not raw and created:
        stamp_image(instance)


@receiver(post_save, weak=False, sender=AssentImage,
          dispatch_uid='assent_image_on_post_save')
def assent_image_on_post_save(sender, instance, raw, created, **kwargs):
    if not raw and created:
        stamp_image(instance)


@receiver(post_save, weak=False, sender=ClinicianNotesImageArchive,
          dispatch_uid='clinician_notes_image_archive_on_post_save')
def clinician_notes_image_archive_on_post_save(sender, instance, raw, created, **kwargs):
    if not raw and created:
        stamp_image(instance)


@receiver(post_save, weak=False, sender=ConsentImage,
          dispatch_uid='consent_image_on_post_save')
def consent_image_on_post_save(sender, instance, raw, created, **kwargs):
    if not raw and created:
        stamp_image(instance)
        subject_identifier = instance.consent_copies.subject_identifier
        encrypt_files(instance, subject_identifier)


@receiver(post_save, weak=False, sender=ContinuedParticipationImage,
          dispatch_uid='continued_participation_image_on_post_save')
def continued_participation_image_on_post_save(sender, instance, raw, created, **kwargs):
    if not raw and created:
        stamp_image(instance)


@receiver(post_save, weak=False, sender=LabResultsFile,
          dispatch_uid='lab_results_file_on_post_save')
def lab_results_file_on_post_save(sender, instance, raw, created, **kwargs):
    if not raw and created:
        stamp_image(instance)


@receiver(post_save, weak=False, sender=NoteToFileDocs,
          dispatch_uid='note_to_file_docs_on_post_save')
def note_to_file_docs_on_post_save(sender, instance, raw, created, **kwargs):
    if not raw and created:
        stamp_image(instance)


@receiver(post_save, weak=False, sender=SpecimenConsentImage,
          dispatch_uid='specimen_consent_image_on_post_save')
def specimen_consent_image_on_post_save(sender, instance, raw, created, **kwargs):
    if not raw and created:
        stamp_image(instance)


def encrypt_files(instance, subject_identifier):
    base_path = settings.MEDIA_ROOT
    if instance.image:
        upload_to = f'{instance.image.field.upload_to}'
        timestamp = datetime.timestamp(get_utcnow())
        zip_filename = f'{subject_identifier}_{timestamp}.zip'
        with open('filekey.key', 'r') as filekey:
            key = filekey.read().rstrip()
        com_lvl = 8
        pyminizip.compress(f'{instance.image.path}', None,
                           f'{base_path}/{upload_to}{zip_filename}', key, com_lvl)
    # remove unencrypted file
    if os.path.exists(f'{instance.image.path}'):
        os.remove(f'{instance.image.path}')
    instance.image = f'{upload_to}{zip_filename}'
    instance.save()

def stamp_image(instance):
    filefield = instance.image
    filename = filefield.name  # gets the "normal" file name as it was uploaded
    storage = filefield.storage
    path = storage.path(filename)
    extension_path  = path.split('.')[1]
    if extension_path != 'pdf':
        add_image_stamp(image_path=path)


def add_image_stamp(image_path=None, position=(25, 25), resize=(100, 100)):
    """
    Superimpose image of a stamp over copy of the base image
    @param image_path: dir to base image
    @param position: pixels(w,h) to superimpose stamp at
    """
    base_image = Image.open(image_path)
    stamp = Image.open('media/stamp/true-copy.png')
    if resize:
        stamp = stamp.resize(resize, PIL.Image.ANTIALIAS)

    width, height = base_image.size
    stamp_width, stamp_height = stamp.size

    # Determine orientation of the base image before pasting stamp
    if width < height:
        pos_width = round(width / 2) - round(stamp_width / 2)
        pos_height = height - stamp_height
        position = (pos_width, pos_height)
    elif width > height:
        stamp = stamp.rotate(90)
        pos_width = width - stamp_width
        pos_height = round(height / 2) - round(stamp_height / 2)
        position = (pos_width, pos_height)

    # paste stamp over image
    base_image.paste(stamp, position, mask=stamp)
    base_image.save(image_path)
