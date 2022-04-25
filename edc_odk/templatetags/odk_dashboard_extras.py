from django import template
from django.apps import apps as django_apps
from django.conf import settings

from ..model_wrappers import ConsentCopiesModelWrapper, OmangCopiesModelWrapper
from ..model_wrappers import SpecimenConsentModelWrapper

register = template.Library()


@register.inclusion_tag('edc_odk/buttons/dashboard_button.html')
def dashboard_button(model_wrapper):
    subject_dashboard_url = settings.DASHBOARD_URL_NAMES.get(
        'subject_dashboard_url')
    return dict(
        subject_dashboard_url=subject_dashboard_url,
        subject_identifier=model_wrapper.subject_identifier)


@register.inclusion_tag('edc_odk/buttons/clinician_notes_archives_button.html')
def clinician_notes_archives_button(model_wrapper):
    title = ['clinician notes archive.']
    return dict(
        subject_identifier=model_wrapper.subject_identifier,
        add_clinician_notes_href=model_wrapper.clinician_notes.href,
        clinician_notes_model_obj=model_wrapper.clinician_notes_model_obj,
        title=' '.join(title),)


@register.inclusion_tag('edc_odk/buttons/labresults_button.html')
def labresults_button(model_wrapper):
    title = ['lab results.']
    return dict(
        subject_identifier=model_wrapper.subject_identifier,
        add_labresults_href=model_wrapper.lab_results.href,
        labresults_model_obj=model_wrapper.labresults_model_obj,
        title=' '.join(title),)


@register.inclusion_tag('edc_odk/buttons/note_to_file_button.html')
def note_to_file_button(model_wrapper):
    title = ['note to file.']
    return dict(
        subject_identifier=model_wrapper.subject_identifier,
        add_note_to_file_href=model_wrapper.note_to_file.href,
        note_to_file_model_obj=model_wrapper.note_to_file_model_obj,
        title=' '.join(title),)


@register.inclusion_tag('edc_odk/buttons/consent_copies_button.html')
def consent_copies_button(model_wrapper):
    title = ['subject copies of consent.']
    return dict(
        subject_identifier=model_wrapper.subject_identifier,
        add_consent_copies_href=model_wrapper.consent_copies.href,
        consent_copies_model_obj=model_wrapper.consent_copies_model_obj,
        title=' '.join(title),)


@register.inclusion_tag('edc_odk/buttons/omang_copies_button.html')
def omang_copies_button(model_wrapper):
    title = ['subject copies of omang.']
    return dict(
        subject_identifier=model_wrapper.subject_identifier,
        add_omang_copies_href=model_wrapper.omang_copies.href,
        omang_copies_model_obj=model_wrapper.omang_copies_model_obj,
        title=' '.join(title),)


@register.inclusion_tag('edc_odk/buttons/specimen_consent_button.html')
def specimen_consent_button(model_wrapper):
    title = ['specimen consent copies.']
    return dict(
        subject_identifier=model_wrapper.subject_identifier,
        add_specimen_consent_copies_href=model_wrapper.specimen_consent_copies.href,
        specimen_consent_copies_model_obj=model_wrapper.specimen_consent_copies_model_obj,
        title=' '.join(title),)


@register.inclusion_tag('edc_odk/buttons/adult_main_consent_button.html')
def adult_main_consent_button(model_wrapper):
    title = ['adult main consent']
    return dict(
        subject_identifier=model_wrapper.subject_identifier,
        add_adult_main_consent_href=model_wrapper.adult_main_consent.href,
        adult_main_consent_model_obj=model_wrapper.adult_main_consent,
        title=' '.join(title),)


@register.inclusion_tag('edc_odk/buttons/assents_button.html')
def assents_button(model_wrapper):
    title = ['assents']
    return dict(
        subject_identifier=model_wrapper.subject_identifier,
        add_assents_href=model_wrapper.assents.href,
        assents_model_obj=model_wrapper.assents,
        title=' '.join(title),)


@register.inclusion_tag('edc_odk/buttons/birth_certificate_button.html')
def birth_certificate_button(model_wrapper):
    title = ['birth certificate']
    return dict(
        subject_identifier=model_wrapper.subject_identifier,
        add_birth_certificate_href=model_wrapper.birth_certificate.href,
        birth_certificate_model_obj=model_wrapper.birth_certificate,
        title=' '.join(title),)


@register.inclusion_tag('edc_odk/buttons/continued_participation_button.html')
def continued_participation_button(model_wrapper):
    title = ['continued participation']
    return dict(
        subject_identifier=model_wrapper.subject_identifier,
        add_continued_participation_href=model_wrapper.continued_participation.href,
        continued_participation_model_obj=model_wrapper.continued_participation,
        title=' '.join(title),)


@register.inclusion_tag('edc_odk/buttons/parental_consent_button.html')
def parental_consent_button(model_wrapper):
    title = ['continued participation']
    return dict(
        subject_identifier=model_wrapper.subject_identifier,
        add_parental_consent_href=model_wrapper.parental_consent.href,
        parental_consent_model_obj=model_wrapper.parental_consent,
        title=' '.join(title),)


@register.inclusion_tag('edc_odk/odk_forms/sidebar/consent_copies.html')
def consent_copies_dashboard_button(subject_identifier=None):
    consent_copies_cls = django_apps.get_model(
        'edc_odk.consentcopies')
    try:
        model_obj = consent_copies_cls.objects.filter(
            subject_identifier=subject_identifier)
    except consent_copies_cls.DoesNotExist:
        return None
    else:
        consent_copies = list()
        for obj in model_obj:
            consent_copies.append(ConsentCopiesModelWrapper(model_obj=obj))
        return dict(consent_copies=consent_copies)


@register.inclusion_tag('edc_odk/odk_forms/sidebar/omang_copies.html')
def omang_copies_dashboard_button(subject_identifier=None):
    title = ['subject copies of omang.']
    omang_copies_cls = django_apps.get_model(
        'edc_odk.omangcopies')
    try:
        model_obj = omang_copies_cls.objects.get(
            subject_identifier=subject_identifier)
    except omang_copies_cls.DoesNotExist:
        return None
    else:
        omang_copies = OmangCopiesModelWrapper(model_obj=model_obj)

        return dict(
            subject_identifier=subject_identifier,
            add_omang_copies_href=omang_copies.href,
            omang_copies_model_obj=model_obj,
            title=' '.join(title),)


@register.inclusion_tag('edc_odk/odk_forms/sidebar/specimen_consent_copies.html')
def specimen_consent_copies_dash_button(subject_identifier=None):
    title = ['subject specimen consent copies.']
    specimen_consent_cls = django_apps.get_model(
        'edc_odk.specimenconsentcopies')
    try:
        model_obj = specimen_consent_cls.objects.get(
            subject_identifier=subject_identifier)
    except specimen_consent_cls.DoesNotExist:
        return None
    else:
        specimen_consent_copies = SpecimenConsentModelWrapper(
            model_obj=model_obj)

        return dict(
            subject_identifier=subject_identifier,
            add_specimen_consent_copies_href=specimen_consent_copies.href,
            specimen_consent_copies_model_obj=model_obj,
            title=' '.join(title),)


@register.filter
def remove_spaces(value):
    return value.replace(" ", "")


@register.filter
def to_list(value):
    return list(value)


@register.filter
def list_index(values, index):
    if len(values) > index:
        return values[index]
