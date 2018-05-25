from django.apps import AppConfig
from django.db.models.signals import post_save


class TestsConfig(AppConfig):
    name = 'Tests'

    def ready(self):
        from Tests.signals.handlers import add_question_to_students,add_student_to_questions
        from Tests.models import Student, Question, StudentAndQuestion
        from django.core.signals import request_finished

        post_save.connect(add_question_to_students, sender=Question)
        post_save.connect(add_student_to_questions, sender=Student)
