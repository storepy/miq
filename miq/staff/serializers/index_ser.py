from rest_framework import serializers

from miq.models import Index


fields = ('slug', 'title', 'sections',)


class IndexSerializer(serializers.ModelSerializer):
    class Meta:
        model = Index
        read_only_fields = ('slug', 'sections')
        fields = (*read_only_fields, *fields)

    sections = serializers.SlugRelatedField(
        slug_field="slug", read_only=True,
        many=True, required=False,
    )
