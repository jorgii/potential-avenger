from django.db import models
from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFit
from json_field import JSONField


from notifications.models import NotificationTypes


def get_upload_file_name(instance, filename):
    return 'profile_photos/{}_{}{}'.format(instance.user.username, instance.user.id, str(filename[filename.rfind('.'):len(filename)]))


class Person(models.Model):
    user = models.OneToOneField('auth.User')
    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female')
    )
    ORIENTATION_CHOICES = (
        ('H', 'Heterosexual'),
        ('L', 'Lesbian'),
        ('G', 'Gay'),
        ('BM', 'Bisexual(Male)'),
        ('BF', 'Bisexual(Female)'),
    )
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    birth_date = models.DateField(blank=True, null=True)
    city = models.CharField('City', max_length=255, blank=True, null=True)
    nickname = models.CharField('Nickname', max_length=255, blank=True, null=True)
    orientation = models.CharField(max_length=1, choices=ORIENTATION_CHOICES, blank=True, null=True)
    photo = ProcessedImageField(upload_to=get_upload_file_name,
                                       verbose_name="Profile photo",
                                       processors=[ResizeToFit(500,500,upscale=False)],
                                       format='JPEG',
                                       options={'quality':60},
                                       blank=True,
                                       null=True)
    preferred_poses = models.ManyToManyField('hardcoded_models.PosesList', blank=True, null=True)
    preferred_places = models.ManyToManyField('hardcoded_models.PlacesList', blank=True, null=True)

    notification_settings = JSONField()


    def __str__(self):
        return '{} {}'.format(self.user.first_name, self.user.last_name)


    def populate_notification_settings(self):
        self.notification_settings = dict()
        for notification_type in NotificationTypes.objects.all():
            self.notification_settings[notification_type.name] = {'period':'0', 'active':False,}
        self.save()
