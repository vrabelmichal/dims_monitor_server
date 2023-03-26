from django import forms

from rest_server.models import Station


class UfoThumbnailsMaintenanceForm(forms.Form):
    stations = forms.ModelMultipleChoiceField(queryset=Station.objects.all())
    start_date = forms.DateField(label='Starting date')
    end_date = forms.DateField(label='Ending date')
    det_level_preview = forms.BooleanField(required=False, label='Detected Level preview images (det_level_preview)', initial=True)
    long_term_avg_preview = forms.BooleanField(required=False, label='Long term averaged brightness images (long_term_avg_preview)', initial=True)
    peak_hold_preview = forms.BooleanField(required=False, label='Peak hold images (peak_hold_preview)', initial=True)
    width = forms.IntegerField(min_value=64, max_value=1920, label='New width', initial=480)
    height = forms.IntegerField(min_value=34, max_value=1920, label='New height', initial=270)
    jpeg_quality = forms.IntegerField(min_value=10, max_value=100, label='JPEG quality', initial=50)
    confirmation_password = forms.CharField(widget=forms.PasswordInput, label='Confirmation password')

    def clean_confirmation_password(self):
        confirmation_password = self.cleaned_data['confirmation_password']
        user = self.request.user
        if not user.check_password(confirmation_password):
            raise forms.ValidationError('Incorrect password.')
        return confirmation_password


    # from django.contrib.auth.models import User
    # class Meta:
    #     model = YourModel
    #
    # def __init__(self, *args, **kwargs):
    #     super(ChoiceForm, self).__init__(*args, **kwargs)
    #     self.fields['countries'] =  ModelChoiceField(queryset=YourModel.objects.all()),
    #                                          empty_label="Choose a countries",)