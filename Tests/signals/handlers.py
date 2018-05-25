from Tests.models import Student, Question, StudentAndQuestion
from django.core.signals import request_finished
from django.dispatch import receiver


@receiver(request_finished)
def add_question_to_students(sender, instance=None, created=None, *args, **kwargs):
    question = instance
    if created:
        StudentAndQuestion.objects.bulk_create([
            StudentAndQuestion(question=question, student_id=student_id)
            for student_id in Student.objects.values_list("id", flat=True)
    ])


@receiver(request_finished)
def add_student_to_questions(sender, instance=None, created=None, *args, **kwargs):
    student = instance
    if created:
        StudentAndQuestion.objects.bulk_create([
            StudentAndQuestion(question=question, student=student)
            for question in Question.objects.all()
        ])

