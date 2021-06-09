# Generated by Django 3.1.6 on 2021-06-08 22:37

from django.db import migrations

def update_intern_payment_status(apps, schema_editor):
    # Get intern selection model
    InternSelection = apps.get_model('home.InternSelection')

    # The default for the initial, midpoint, and final
    # payment status is waiting on mentor feedback.
    # That means that if the initial/midpoint/final mentor feedback object is null,
    # then the default payment status is correct.

    # Update records for requested and denied initial payments
    interns = InternSelection.objects.all().exclude(initialmentorfeedback__isnull=True)

    for i in interns.filter(initialmentorfeedback__organizer_payment_approved=True):
        i.initial_payment_status = i.REQUESTED
        i.save()

    for i in interns.filter(initialmentorfeedback__organizer_payment_approved=False):
        i.initial_payment_status = i.DONOTPAY
        i.save()

    # When an intern has an extension, the mentors will have filled out the
    # feedback form once. That means the feedback object exists.
    #
    # When the mentor fills out the feedback form after an extension is
    # complete, the "allow_edits" flag will be set to False. In this case, the
    # payment request is awaiting review by Outreachy organizers.
    #
    # If the extension is still active, the "allow_edits" flag will be True, and
    # we're waiting on feedback from the mentor. In this case, the default
    # payment status of "waiting on feedback from mentor" is correct.
    #
    # Update all payment statuses to note which ones are waiting on Outreachy
    # organizer review.
    for i in interns.filter(initialmentorfeedback__organizer_payment_approved=None, initialmentorfeedback__allow_edits=False):
        i.initial_payment_status = i.UNDERREVIEW
        i.save()

    # Update records for requested and denied midpoint payments
    interns = InternSelection.objects.all().exclude(midpointmentorfeedback__isnull=True)

    for i in interns.filter(midpointmentorfeedback__organizer_payment_approved=True):
        i.midpoint_payment_status = i.REQUESTED
        i.save()

    for i in interns.filter(midpointmentorfeedback__organizer_payment_approved=False):
        i.midpoint_payment_status = i.DONOTPAY
        i.save()

    for i in interns.filter(midpointmentorfeedback__organizer_payment_approved=None, midpointmentorfeedback__allow_edits=False):
        i.midpoint_payment_status = i.UNDERREVIEW
        i.save()

    # Update records for requested and denied final payments
    interns = InternSelection.objects.all().exclude(finalmentorfeedback__isnull=True)

    for i in interns.filter(finalmentorfeedback__organizer_payment_approved=True):
        i.final_payment_status = i.REQUESTED
        i.save()

    for i in interns.filter(finalmentorfeedback__organizer_payment_approved=False):
        i.final_payment_status = i.DONOTPAY
        i.save()

    for i in interns.filter(finalmentorfeedback__organizer_payment_approved=None, finalmentorfeedback__allow_edits=False):
        i.final_payment_status = i.UNDERREVIEW
        i.save()

class Migration(migrations.Migration):

    dependencies = [
        ('home', '0200_auto_20210608_2236'),
    ]

    operations = [
        migrations.RunPython(update_intern_payment_status),
    ]
