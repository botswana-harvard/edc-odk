import os
import pyminizip
from datetime import datetime
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from edc_base.utils import get_utcnow

from .omang_copies import NationalIdentityImage


@receiver(post_save, weak=False, sender=NationalIdentityImage,
          dispatch_uid='maternal_dataset_on_post_save')
def natinal_identity_image_on_post_save(sender, instance, raw, created, **kwargs):
    """
    -
    """
    if not raw:
        if created:
            encrypt_files(instance)


def encrypt_files(instance):
    base_path = settings.MEDIA_ROOT
    if instance.image:
        upload_to = f'{instance.image.field.upload_to}'
        timestamp = datetime.timestamp(get_utcnow())
        zip_filename = f'{instance.omang_copies.subject_identifier}_{timestamp}.zip'
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
