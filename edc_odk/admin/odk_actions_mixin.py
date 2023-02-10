from PIL import Image
from django.db.models import ManyToOneRel
from django.utils.translation import ugettext_lazy as _
from edc_base.utils import get_utcnow

from ..classes.adult_reports import AdultReports
from ..classes.children_reports import ChildrenReports


class ODKActionMixin:

    def add_image_stamp(self, request, queryset):
        for obj in queryset:
            accessor_names = [field.get_accessor_name() for field in
                              obj._meta.get_fields() if
                              issubclass(type(field), ManyToOneRel)]
            for accessor_name in accessor_names:
                images = getattr(obj, accessor_name).all()
                for image in images:
                    image_path = image.image.path

                    base_image = Image.open(image_path)
                    stamp = Image.open('media/stamp/true-copy.png')
                    stamp = stamp.resize((600, 600))

                    width, height = base_image.size
                    stamp_width, stamp_height = stamp.size
                    if width < height:
                        pos_width = round(width / 2) - round(stamp_width / 2)
                        pos_height = height - stamp_height
                        position = (pos_width, pos_height)
                    elif width > height:
                        stamp = stamp.rotate(90)
                        pos_width = width - stamp_width
                        pos_height = round(height / 2) - round(stamp_height / 2)
                        position = (pos_width, pos_height)

                    # add stamp to image
                    base_image.paste(stamp, position, mask=stamp)
                    base_image.save(image_path)

    def verify_image(self, request, queryset):
        for obj in queryset:
            obj.is_verified = True
            obj.verified_by = request.user.get_username()
            obj.is_verified_datetime = get_utcnow()
            obj.save()

    verify_image.short_description = _(
        'Verify %(verbose_name_plural)s as true copy')

    add_image_stamp.short_description = _(
        'Certify %(verbose_name_plural)s as true copy')

    actions = [add_image_stamp, verify_image]

    def changelist_view(self, request, extra_context=None):
        extra_context = extra_context or {}
        adult_reports = AdultReports()
        children_reports = ChildrenReports()
        model_name = self.model._meta.model_name
        adult_reports_data = {
            'adultmainconsent': (
                adult_reports.missing_adult_main_consent, adult_reports.all_caregivers),
            'omangcopies': (
                adult_reports.missing_omang_copies, adult_reports.all_caregivers),
            'parentalconsent': (
                adult_reports.missing_parental_consent, adult_reports.all_caregivers),
            'notetofiles': (
                adult_reports.missing_note_to_files, adult_reports.all_caregivers),
            'labresultsfiles': (
                adult_reports.missing_lab_results_files, adult_reports.all_caregivers),
            'specimenconsentcopies': (
                adult_reports.missing_specimen_consent_copies,
                adult_reports.all_caregivers),
            'continuedparticipation': (children_reports.missing_continued_participation,
                                       children_reports.all_caregivers),
            'consentcopies': (
                adult_reports.missing_consent_copies, adult_reports.all_caregivers),
            'cliniciannotesarchives': (
                adult_reports.missing_clinician_notes_archives,
                adult_reports.all_caregivers),
            'birthcertificate': (
                children_reports.missing_birth_certificate,
                children_reports.all_caregivers),
            'assent': (children_reports.missing_assent, children_reports.all_caregivers)
        }

        if model_name in adult_reports_data:
            extra_context['data'], caregivers = adult_reports_data[model_name]
            extra_context['all_caregivers'] = len(list(set(caregivers)))

        return super().changelist_view(request, extra_context=extra_context)
