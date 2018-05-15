from django.contrib import admin

from .models import Choice, Question

class ChoiceAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'win_count')

class QuestionAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'voteA', 'voteB')

admin.site.register(Choice, ChoiceAdmin)
admin.site.register(Question, QuestionAdmin)
