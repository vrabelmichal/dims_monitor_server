from rest_framework import serializers

from rest_server.models import Process, Report


class ProcessSerializer(serializers.ModelSerializer):

    cmdline = serializers.ListSerializer(
        child=serializers.CharField(allow_blank=True),
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
        validated_data['cmdline'] = '\t'.join(validated_data['cmdline'])
        return super().create(validated_data)
