from django.db import models

class Choice(models.Model):
    image = models.ImageField(unique=True)
    available = models.BooleanField(default=True)
    win_against_m2m = models.ManyToManyField('self', symmetrical=False, blank=True)

    def win_against(self, other_choice):
        self.win_against_m2m.add(other_choice)
        other_choice.win_against_m2m.remove(self)
        self.save()
        other_choice.save()
        return

    def draw_against(self, other_choice):
        self.win_against_m2m.remove(other_choice)
        other_choice.win_against_m2m.remove(self)
        self.save()
        other_choice.save()
        return

    def win_count(self):
        return self.win_against_m2m.count()

    def __str__(self):
        return self.image.url

class Question(models.Model):
    choiceA = models.ForeignKey(Choice, on_delete=models.CASCADE, related_name='choiceA')
    choiceB = models.ForeignKey(Choice, on_delete=models.CASCADE, related_name='choiceB')
    voteA = models.IntegerField(default=0)
    voteB = models.IntegerField(default=0)

    def get_cookie_key(self):
        return 'question_%d' % self.id

    # pick or create a question of two random choices
    def pick_or_create():
        # pick random choice from queryset
        def pick_choice(queryset):
            from random import randint
            count = queryset.count()
            random_index = randint(0, count - 1)
            return queryset[random_index]

        # get two random different choices
        choiceA = pick_choice(Choice.objects.all())
        choiceB = pick_choice(Choice.objects.exclude(pk=choiceA.pk))

        # check question existence
        question = Question.objects.filter(choiceA__in=[choiceA, choiceB], choiceB__in=[choiceA, choiceB])
        if question:
            # question exists: pick the first one from the queryset
            question = question[0]
        else:
            # create question if doesn't exist
            question = Question(choiceA=choiceA, choiceB=choiceB)
            question.save()

        return question

    def is_available(self):
        return self.choiceA.available and self.choiceB.available

    def __str__(self):
        return 'Question'


















def test():
    import os
    from django.conf import settings
    from polls.models import Choice
    from django.db.utils import IntegrityError
    from PIL import Image

    for filename in os.listdir(settings.MEDIA_ROOT):
        try:
            Image.open(settings.MEDIA_ROOT + filename)
        except:
            pass
        else:
            if not Choice.objects.filter(image=filename):
                choice = Choice(image=filename)
                choice.save()

test()


