
from rest_framework import serializers

from miq.models import Image


def serialize_context_pagination(request, context):
    is_paginated = context.get('is_paginated', False)

    data = {'is_paginated': is_paginated}
    if is_paginated:
        page_obj = context.get('page_obj')
        paginator = context.get('paginator')
        query_dict = request.GET.copy()

        _data = {
            'has_next': False,
            'has_previous': False,
            'page_obj_number': page_obj.number,
            'count': paginator.count,
            'per_page': paginator.per_page,
            'num_pages': paginator.num_pages,
            'allow_empty_first_page': paginator.allow_empty_first_page,
        }

        if has_next := page_obj.has_next():
            has_next_page_number = page_obj.next_page_number()
            query_dict.__setitem__('page', has_next_page_number)

            _data.update({
                'has_next': has_next,
                'has_next_page_number': has_next_page_number,
                'has_next_url': f'{request.path}?{query_dict.urlencode(safe="/")}',
            })

        if has_previous := page_obj.has_previous():
            has_previous_page_number = page_obj.previous_page_number()
            query_dict.__setitem__('page', has_previous_page_number)
            _data.update({
                'has_previous': has_previous,
                'has_previous_page_number': has_previous_page_number,
                'has_previous_url': f'{request.path}?{query_dict.urlencode(safe="/")}',
            })

        data.update(_data)

    return data


class PublicImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        read_only_fields = [
            'src', 'src_mobile', 'thumb', 'thumb_sq',
            'alt_text', 'caption',
            'height', 'width', 'height_mobile', 'width_mobile',
        ]
        fields = [*read_only_fields]

    width = serializers.ReadOnlyField()
    height = serializers.ReadOnlyField()
    width_mobile = serializers.ReadOnlyField()
    height_mobile = serializers.ReadOnlyField()
