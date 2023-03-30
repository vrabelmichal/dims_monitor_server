from django import forms
from django.utils import timezone
from dateutil.relativedelta import relativedelta

from rest_server.models import Station, UfoCaptureOutputEntry


class UfoThumbnailsMaintenanceForm(forms.Form):

    stations = forms.ModelMultipleChoiceField(
        queryset=Station.objects.all(),
    )
    # start_datetime = forms.DateField(label='Starting date')
    # end_datetime = forms.DateField(label='Ending date', initial=UfoCaptureOutputEntry.objects.first())
    # Set the end date to the current date minus 1 month
    end_datetime = forms.DateTimeField(label='Ending datetime')
    # Set the start date to the oldest date in the UfoCaptureOutputEntry model
    start_datetime = forms.DateTimeField(label='Starting datetime')
    det_level_preview = forms.BooleanField(required=False, label='Detected Level preview images (det_level_preview)', initial=True)
    long_term_avg_preview = forms.BooleanField(required=False, label='Long term averaged brightness images (long_term_avg_preview)', initial=True)
    peak_hold_preview = forms.BooleanField(required=False, label='Peak hold images (peak_hold_preview)', initial=True)
    width = forms.IntegerField(min_value=64, max_value=1920, label='New width', initial=480)
    height = forms.IntegerField(min_value=34, max_value=1920, label='New height', initial=270)
    jpeg_quality = forms.IntegerField(min_value=10, max_value=100, label='JPEG quality', initial=50)
    confirmation_password = forms.CharField(widget=forms.PasswordInput, label='Confirmation password')
    log_every_operation = forms.BooleanField(required=False, label='Log every image operation', initial=True)
    always_resize = forms.BooleanField(required=False, label='Always resize', initial=False)

    def clean_confirmation_password(self):
        confirmation_password = self.cleaned_data['confirmation_password']
        if self.request_user is None:
            raise RuntimeError('Form initialized without request_user object reference')
        user = self.request_user
        if not user.check_password(confirmation_password):
            raise forms.ValidationError('Incorrect password.')
        return confirmation_password


    def __init__(self, *args, **kwargs):
        self.request_user = kwargs.pop('request_user', None)
        super().__init__(*args, **kwargs)
        # Update the end date field with the current date minus 1 month
        self.fields['stations'].initial = Station.objects.all().values_list('id', flat=True)
        self.fields['start_datetime'].initial = (
            UfoCaptureOutputEntry.objects.order_by('filename_datetime').first().filename_datetime
        )
        self.fields['end_datetime'].initial = timezone.now() - relativedelta(months=1)
        # self.fields['confirmation_password'].validators.append(self.clean_confirmation_password)


    # from django.contrib.auth.models import User
    # class Meta:
    #     model = YourModel
    #
    # def __init__(self, *args, **kwargs):
    #     super(ChoiceForm, self).__init__(*args, **kwargs)
    #     self.fields['countries'] =  ModelChoiceField(queryset=YourModel.objects.all()),
    #                                          empty_label="Choose a countries",)