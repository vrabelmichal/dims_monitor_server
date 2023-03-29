import os
import typing

from PIL import Image
import logging

from django.http import HttpResponse
from django.shortcuts import redirect
from django.template import loader
from django.contrib.auth.decorators import login_required

from rest_server.forms.ufo_thumbnails_maintenance import UfoThumbnailsMaintenanceForm
from django.contrib import messages

from rest_server.models import Station, Report
from rest_server.models.ufo_capture_output import get_base_preview_image_dir_path, UfoCaptureOutputEntry, \
    get_preview_image_dir_path

THUMB_MAINTENANCE_LOGGER = logging.getLogger('dims_monitor_server.ufo_thumbnails_maintenance')


def _resize_image(
        image_pathname,
        width,
        height,
        jpeg_quality,
        logger=THUMB_MAINTENANCE_LOGGER,
        extra_info=''
):
    if len(extra_info) > 0 and extra_info[0] != ' ':
        extra_info = ' ' + extra_info
    image_basename = os.path.basename(image_pathname)
    # Open the image file with PIL
    image = Image.open(image_pathname)
    # Resize the image according to the width and height from the form
    image = image.resize((width, height))
    # Save the image with the same name and format, but with different quality for jpg images
    if image_basename.lower().endswith('.jpg'):
        image.save(image_pathname, quality=jpeg_quality)
        # Log the file replacement with size and quality
        logger.info(
            'Replaced %s with resized image of size %dx%d and quality %d.%s',
            image_pathname, width, height, jpeg_quality,
            extra_info
        )
    else:
        image.save(image_pathname)
        # Log the file replacement with size only
        logger.info(
            'Replaced %s with resized image of size %dx%d.%s',
            image_pathname, width, height, extra_info
        )


class ResizeImagesStats(typing.NamedTuple):
    total_expected_successes: int
    total_num_successful_reports: int
    total_num_failed_reports: int
    total_num_partially_failed_reports: int
    total_num_successful_operations: int
    total_num_failed_operations: int


def _resize_images(
        station_ids,
        start_datetime,
        end_datetime,
        resize_det_level_preview,
        resize_long_term_avg_preview,
        resize_peak_hold_preview,
        width,
        height,
        jpeg_quality,
        logger=THUMB_MAINTENANCE_LOGGER
):
    total_expected_successes = 0
    total_num_successful_reports = 0
    total_num_failed_reports = 0
    total_num_partially_failed_reports = 0
    total_num_successful_operations = 0
    total_num_failed_operations = 0

    for ufo_capture_entry in UfoCaptureOutputEntry.objects.filter(
        xml_datetime__gte=start_datetime,
        xml_datetime__lte=end_datetime,
        station_id__in=station_ids
    ).all():
        # report_start_utc = ufo_capture_entry.report__start_utc
        report_id = ufo_capture_entry.report_id
        det_level_preview = ufo_capture_entry.det_level_preview
        long_term_avg_preview = ufo_capture_entry.long_term_avg_preview
        peak_hold_preview = ufo_capture_entry.peak_hold_preview

        log_extra_info_str = f'(report id: {report_id})'

        expected_successes = 0
        num_successful = 0
        num_failed = 0

        for preview_image_file_field, apply_resize in (
                (det_level_preview, resize_det_level_preview),
                (long_term_avg_preview, resize_long_term_avg_preview),
                (peak_hold_preview, resize_peak_hold_preview)
        ):
            if not apply_resize or not preview_image_file_field:
                continue
            preview_image_pathname = preview_image_file_field.path

            expected_successes += 1

            try:
                _resize_image(
                    image_pathname=preview_image_pathname,
                    width=width,
                    height=height,
                    jpeg_quality=jpeg_quality,
                    logger=logger,
                    extra_info=log_extra_info_str
                )
                num_successful += 1
            except Exception as e:
                num_failed += 1
                THUMB_MAINTENANCE_LOGGER.info(
                    'Failed to resize image "%s" (%s: %s; report id: %d).',
                    preview_image_file_field, e.__class__.__name__, str(e), report_id
                )

        total_num_successful_operations += num_successful
        total_num_failed_operations += num_failed

        if expected_successes != 0:
            if expected_successes == num_successful:
                total_num_successful_reports += 1
            elif num_successful > 0:
                total_num_partially_failed_reports += 1
            else:
                total_num_failed_reports += 1
            total_expected_successes += 1

    return ResizeImagesStats(
        total_expected_successes=total_expected_successes,
        total_num_successful_reports=total_num_successful_reports,
        total_num_failed_reports=total_num_failed_reports,
        total_num_partially_failed_reports=total_num_partially_failed_reports,
        total_num_successful_operations=total_num_successful_operations,
        total_num_failed_operations=total_num_failed_operations,
    )


@login_required
def ufo_thumbnails_maintenance(request):

    if request.method == 'POST':
        form = UfoThumbnailsMaintenanceForm(request.POST, request_user=request.user)
        if form.is_valid():
            stations = form.cleaned_data['stations']
            start_datetime = form.cleaned_data['start_datetime']
            end_datetime = form.cleaned_data['end_datetime']
            resize_det_level_preview = form.cleaned_data['det_level_preview']
            resize_long_term_avg_preview = form.cleaned_data['long_term_avg_preview']
            resize_peak_hold_preview = form.cleaned_data['peak_hold_preview']
            width = form.cleaned_data['width']
            height = form.cleaned_data['height']
            jpeg_quality = form.cleaned_data['jpeg_quality']
            # confirmation_password = form.cleaned_data['confirmation_password']

            s = _resize_images(
                station_ids=stations,
                start_datetime=start_datetime,
                end_datetime=end_datetime,
                resize_det_level_preview=resize_det_level_preview,
                resize_long_term_avg_preview=resize_long_term_avg_preview,
                resize_peak_hold_preview=resize_peak_hold_preview,
                width=width,
                height=height,
                jpeg_quality=jpeg_quality
            )
            if s.total_expected_successes == 0:
                messages.warning(request, 'Event preview images maintenance: No valid entries found')
            else:
                messages.add_message(
                    request,
                    messages.WARNING if s.total_num_failed_operations > 0 else messages.INFO,
                    'Event preview images maintenance: '
                    f'Successfully processed {s.total_num_successful_reports} reports, '
                    f'some error occurred when processing {s.total_num_partially_failed_reports} reports, '
                    f'failed to process {s.total_num_failed_reports} reports '
                    f'(successfully processed {s.total_num_successful_operations} files, '
                    f'failed to process {s.total_num_failed_operations} entries).'
                )
            return redirect('ufo_thumbnails_maintenance')
    else:
        form = UfoThumbnailsMaintenanceForm()

    template = loader.get_template('ufo_thumbnails_maintenance.html')  # getting our template

    return HttpResponse(template.render(
        dict(
            segment='ufo_thumbnails_maintenance',
            form=form
        ),
        request
    ))
