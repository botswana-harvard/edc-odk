from .classes import PullODKData


def pull_all_data_from_odk():
    """
    Pulls all form submissions data from the odk aggregate server
    """
    PullODKData().pull_clinician_notes_data()
    PullODKData().pull_consent_images_data()
    PullODKData().pull_omang_images_data()
    PullODKData().pull_specimen_consent_images_data()
