from django.db.models import ManyToOneRel
from django.utils.translation import ugettext_lazy as _
from PIL import Image


class StampImageActionMixin:

    def add_image_stamp(self, request, queryset):
        for obj in queryset:
            accessor_names = [field.get_accessor_name() for field in
                              obj._meta.get_fields() if issubclass(type(field), ManyToOneRel)]
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
                        pos_width = round(width/2)-round(stamp_width/2)
                        pos_height = height-stamp_height
                        position = (pos_width, pos_height)
                    elif width > height:
                        stamp = stamp.rotate(90)
                        pos_width = width-stamp_width
                        pos_height = round(height/2)-round(stamp_height/2)
                        position = (pos_width, pos_height)

                    # add stamp to image
                    base_image.paste(stamp, position, mask=stamp)
                    base_image.save(image_path)

    add_image_stamp.short_description = _(
        'Certify %(verbose_name_plural)s as true copy')

    actions = [add_image_stamp]
