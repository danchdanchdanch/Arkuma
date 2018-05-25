from django.contrib import admin
from Tests.models import *
# Register your models here.

admin.site.register(Theme)
admin.site.register(Rule)
admin.site.register(QuestionText)

@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('text','exercise', 'type', 'theme')
    list_filter = ('type',)
    list_filter = ('theme__name',)

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('name', 'surname', 'code', 'points')
    readonly_fields = ('points',)

@admin.register(StudentAndQuestion)
class StudentAndQuestion(admin.ModelAdmin):
    list_display = ('question', 'student', 'points', 'is_learned', 'is_first_time')
    readonly_fields = ('points',)

