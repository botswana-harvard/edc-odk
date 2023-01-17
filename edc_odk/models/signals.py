import os
from datetime import datetime

import PIL
import img2pdf
import pyminizip
import pypdfium2 as pdfium
from PIL import Image
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
        subject_identifier = instance.parental_consent.subject_identifier
        encrypt_files(instance, subject_identifier)


@receiver(post_save, weak=False, sender=ContinuedParticipationImage,
          dispatch_uid='continued_participation_image_on_post_save')
def continued_participation_image_on_post_save(sender, instance, raw, created, **kwargs):
    if not raw and created:
        stamp_image(instance)
        subject_identifier = instance.continued_participation.subject_identifier
        encrypt_files(instance, subject_identifier)


@receiver(post_save, weak=False, sender=AssentImage,
          dispatch_uid='assent_image_on_post_save')
def assent_image_on_post_save(sender, instance, raw, created, **kwargs):
    if not raw and created:
        stamp_image(instance)
        subject_identifier = instance.assent.subject_identifier
        encrypt_files(instance, subject_identifier)


@receiver(post_save, weak=False, sender=ClinicianNotesImageArchive,
          dispatch_uid='clinician_notes_image_archive_on_post_save')
def clinician_notes_image_archive_on_post_save(sender, instance, raw, created, **kwargs):
    if not raw and created:
        stamp_image(instance)
        subject_identifier = instance.clinician_notes.subject_identifier
        encrypt_files(instance, subject_identifier)


@receiver(post_save, weak=False, sender=ConsentImage,
          dispatch_uid='consent_image_on_post_save')
def consent_image_on_post_save(sender, instance, raw, created, **kwargs):
    if not raw and created:
        stamp_image(instance)
        subject_identifier = instance.consent_copies.subject_identifier
        encrypt_files(instance, subject_identifier)


@receiver(post_save, weak=False, sender=LabResultsFile,
          dispatch_uid='lab_results_file_on_post_save')
def lab_results_file_on_post_save(sender, instance, raw, created, **kwargs):
    if not raw and created:
        stamp_image(instance)
        subject_identifier = instance.lab_results.subject_identifier
        encrypt_files(instance, subject_identifier)


@receiver(post_save, weak=False, sender=NoteToFileDocs,
          dispatch_uid='note_to_file_docs_on_post_save')
def note_to_file_docs_on_post_save(sender, instance, raw, created, **kwargs):
    if not raw and created:
        stamp_image(instance)
        subject_identifier = instance.notes_to_file.subject_identifier
        encrypt_files(instance, subject_identifier)


@receiver(post_save, weak=False, sender=SpecimenConsentImage,
          dispatch_uid='specimen_consent_image_on_post_save')
def specimen_consent_image_on_post_save(sender, instance, raw, created, **kwargs):
    if not raw and created:
        stamp_image(instance)
        subject_identifier = instance.consent_copies.subject_identifier
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


def stamp_image(instance):
    filefield = instance.image
    filename = filefield.name  # gets the "normal" file name as it was uploaded
    storage = filefield.storage
    path = storage.path(filename)
    if '.pdf' not in path:
        base_image=Image.open(path)
        stamped_img = add_image_stamp(base_image=base_image)
        stamped_img.save(path)
    else:
        print_pdf(path)


def add_image_stamp(base_image=None, position=(25, 25),
        resize=(150, 150)):
    """
    Superimpose image of a stamp over copy of the base image
    @param image_path: dir to base image
    @param dont_save: boolean for not saving the image just converting
    @param position: pixels(w,h) to superimpose stamp at
    """
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
    return base_image


def print_pdf(filepath):
    pdf = pdfium.PdfDocument(filepath)
    page_indices = [i for i in range(len(pdf))]
    renderer = pdf.render_to(
        pdfium.BitmapConv.pil_image,
        page_indices=page_indices,
        scale=300 / 72
    )
    stamped_pdf_images = []
    for image, index in zip(renderer, page_indices):
        stamped_pdf_images.append(add_image_stamp(base_image=image, resize=(300, 300)))
    first_img = stamped_pdf_images[0]
    first_img.save(filepath, save_all=True, append_images=stamped_pdf_images[1:])
