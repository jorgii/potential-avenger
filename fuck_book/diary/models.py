from django.db import models


class Diary(models.Model):
    creator = models.ForeignKey('persons.Person')
    participants = models.ManyToManyField('persons.Person', related_name='diary_participants', blank=True, null=True)
    checkins = models.ManyToManyField('checkin.CheckinDetails')
    datetime_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return 'DateTime: {},Creator: {},Participants: {}'.format(self.datetime_created, str(self.creator.user.username), [str(p.user.username) for p in self.participants.all()])

    def add_checkins_to_diary(self, *checkins):
        self.checkins.add(*checkins)
        self.save()
        return

    @staticmethod
    def create(creator, participants, checkins):
        diary = Diary.objects.create(creator=creator)
        diary.participants.add(*participants)
        diary.add_checkins_to_diary(checkins)
        diary.save()
        return diary

    @staticmethod
    def get_diary_for_exact_people(*people): 
        for diary in Diary.get_diaries_for_people(*people):
            if diary.participants.count() == len(people):
                return diary
        return


    @staticmethod
    def get_diaries_for_people(*people):
        for person in people:
            if person == people[0]:
                gathered_diaries = Diary.objects.filter(participants__id=person.id)
            else:
                gathered_diaries=gathered_diaries.filter(participants__id=person.id)
        return gathered_diaries
