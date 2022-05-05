import os
import pyminizip
from datetime import datetime
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from edc_base.utils import get_utcnow

from .omang_copies import NationalIdentityImage
from .birth_certificate import BirthCertificateImage
from .parental_consent import ParentalConsentImage
from .adult_main_consent import AdultMainConsentImage
from .continued_participation import ContinuedParticipationImage
from .assent import AssentImage


@receiver(post_save, weak=False, sender=NationalIdentityImage,
          dispatch_uid='maternal_dataset_on_post_save')
def natinal_identity_image_on_post_save(sender, instance, raw, created, **kwargs):
    if not raw and created:
        subject_identifier = instance.omang_copies.subject_identifier
        encrypt_files(instance, subject_identifier)


@receiver(post_save, weak=False, sender=BirthCertificateImage,
          dispatch_uid='birth_certificate_on_post_save')
def birth_certificate_image_on_post_save(sender, instance, raw, created, **kwargs):
    if not raw and created:
        subject_identifier = instance.birth_certificate.subject_identifier
        encrypt_files(instance, subject_identifier)


@receiver(post_save, weak=False, sender=AdultMainConsentImage,
          dispatch_uid='adult_main_consent_on_post_save')
def adult_main_consent_image_on_post_save(sender, instance, raw, created, **kwargs):
    if not raw and created:
        subject_identifier = instance.adult_main_consent.subject_identifier
        encrypt_files(instance, subject_identifier)


@receiver(post_save, weak=False, sender=ParentalConsentImage,
          dispatch_uid='parental_consent_image_on_post_save')
def parental_consent_image_on_post_save(sender, instance, raw, created, **kwargs):
    if not raw and created:
        subject_identifier = instance.parental_consent.subject_identifier
        encrypt_files(instance, subject_identifier)


@receiver(post_save, weak=False, sender=ContinuedParticipationImage,
          dispatch_uid='continued_participation_image_on_post_save')
def continued_participation_image_on_post_save(sender, instance, raw, created, **kwargs):
    if not raw and created:
        subject_identifier = instance.continued_participation.subject_identifier
        encrypt_files(instance, subject_identifier)


@receiver(post_save, weak=False, sender=AssentImage,
          dispatch_uid='assent_image_on_post_save')
def assent_image_on_post_save(sender, instance, raw, created, **kwargs):
    if not raw and created:
        subject_identifier = instance.assent.subject_identifier
        encrypt_files(instance, subject_identifier)


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
