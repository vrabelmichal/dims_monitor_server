from rest_framework import serializers

from rest_server.models import Process, Report


class ProcessSerializer(serializers.ModelSerializer):

    cmdline = serializers.ListSerializer(
        child=serializers.CharField(allow_blank=True),
        allow_empty=True, required=False,
        allow_null=True
    )

    report = serializers.PrimaryKeyRelatedField(
        many=False, read_only=False, required=False,
        queryset=Report.objects.all()
    )

    class Meta:
        model = Process
        fields = '__all__'

    def validate(self, attrs):
        result = super().validate(attrs)
        return result

    def create(self, validated_data):
        cmdline = validated_data.get('cmdline', None)
        validated_data['cmdline'] = '\t'.join(cmdline) if isinstance(cmdline, (list, tuple)) else None
        return super().create(validated_data)
