import logging
from celery import shared_task
from celery.signals import worker_process_init

from .classes import PullODKData

logger = logging.getLogger(__name__)


@worker_process_init.connect
def configure_workers(sender=None, conf=None, **kwargs):
    from Crypto import Random
    Random.atfork()


@shared_task
def pull_all_data_from_odk():
    """
    Pulls all form submissions data from the odk aggregate server
    """
    PullODKData().pull_clinician_notes_data()
    PullODKData().pull_consent_images_data()
    PullODKData().pull_omang_images_data()
    PullODKData().pull_specimen_consent_images_data()
