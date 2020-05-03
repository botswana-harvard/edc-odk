from django import template
from django.conf import settings


register = template.Library()


@register.inclusion_tag('edc_odk/buttons/dashboard_button.html')
def dashboard_button(model_wrapper):
    subject_dashboard_url = settings.DASHBOARD_URL_NAMES.get(
        'subject_dashboard_url')
    return dict(
        subject_dashboard_url=subject_dashboard_url,
        subject_identifier=model_wrapper.subject_identifier)


@register.inclusion_tag('edc_odk/buttons/consent_copies_button.html')
def consent_copies_button(model_wrapper):
    title = ['subject copies of consent.']
    return dict(
        subject_identifier=model_wrapper.subject_identifier,
        add_consent_copies_href=model_wrapper.consent_copies.href,
        consent_copies_model_obj=model_wrapper.consent_copies_model_obj,
        title=' '.join(title),)
