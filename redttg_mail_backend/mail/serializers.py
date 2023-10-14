import json
from rest_framework import serializers
from .models import Attachment, Mail

class PreviewAttachmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attachment
        fields = ('id', 'filename', 'type')

class AttachmentSerializer(PreviewAttachmentSerializer):
    def to_representation(self, instance):
        fields = super().to_representation(instance)
        fields['file'] = instance.file.file.name
        return fields


class PreviewMailSerializer(serializers.ModelSerializer):
    attachments = PreviewAttachmentSerializer(many=True, read_only=True)

    class Meta:
        model = Mail
        fields = ('id', 'subject', 'created', 'envelope', 'attachments')

    def to_representation(self, instance):
        fields = super().to_representation(instance)
        fields['envelope'] = json.loads(fields['envelope'])
        return fields
    


class MailSerializer(PreviewMailSerializer):
    attachments = AttachmentSerializer(many=True, read_only=True)

    class Meta:
        model = Mail
        fields = '__all__'
