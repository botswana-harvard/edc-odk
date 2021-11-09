from celery import shared_task
from celery.signals import worker_process_init
from celery.utils.log import get_task_logger

from .classes import PullODKData, ODKCentralPullData

logger = get_task_logger(__name__)


@worker_process_init.connect
def configure_workers(sender=None, conf=None, **kwargs):
    from Crypto import Random
    Random.atfork()


@shared_task
def pull_crf_data_from_odk():
    """
    Pulls all form submissions data from the odk aggregate server
    """
    PullODKData().pull_clinician_notes_data()
    PullODKData().pull_labresults_data()


@shared_task
def pull_non_crf_odk_data():
    PullODKData().pull_note_to_file_data()
    PullODKData().pull_consent_images_data()
    PullODKData().pull_omang_images_data()
    PullODKData().pull_specimen_consent_images_data()


@shared_task
def pull_all_data_from_odkcentral():
    ODKCentralPullData().pull_clinician_notes_data()
