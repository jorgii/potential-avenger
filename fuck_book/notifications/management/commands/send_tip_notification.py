from django.core.management.base import BaseCommand

from notifications.models import TipNotification
from persons.models import Person
from notifications.management.commands.send_difference_notification import get_most_recent_notification, time_to_send_notification


class Command(BaseCommand):
    def handle(self, *args, **options):
        for this_person in Person.objects.all():

            if this_person.display_tip_notification:
                last_entry = get_most_recent_notification(this_person, TipNotification)

                if time_to_send_notification(last_entry, this_person.tip_notification_period):
                    TipNotification.objects.create(person=this_person)
