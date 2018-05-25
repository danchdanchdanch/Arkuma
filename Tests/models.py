from django.db import models

from tinymce import models as tinymce_models
from django.db.models.signals import post_delete, post_save
# Create your models here.

class Rule(models.Model):
	short_name = models.CharField(max_length=1500)
	rule = tinymce_models.HTMLField(max_length=14000, null=True)

	def __str__(self):
		return self.short_name

class QuestionText(models.Model):
    class Meta:
        verbose_name_plural = "Short text for question"

    name = models.CharField(max_length=150)
    text = tinymce_models.HTMLField(max_length=14000, null=True)

    def __str__(self):
        return self.name

class Theme(models.Model):
    class Meta:
        verbose_name_plural = "Themes"

    name = models.CharField(max_length=150)
    description = models.CharField(max_length=1500)
#    rule = tinymce_models.HTMLField(max_length=14000, null=True)


    def __str__(self):
        return self.name


# class Group(models.Model):
#    class Meta:
#        verbose_name_plural = "Groups"
#    name = models.CharField(max_length=150)
#
#    def __str__(self):
#        return self.name


class Question(models.Model):
    class Meta:
        verbose_name_plural = "Questions"

    Q_S  = "QUESTION_SELECT"
    Q_T  = "QUESTION_TRANSLATE"
    Q_IV = "QUESTION_IRREGULAR_VERB"
    Q_M  = "QUESTION_MISSED"

    QUESTION_TYPE = (
        (Q_S,  "Question Select"),
        (Q_T,  "Question Translate"),
        (Q_IV, "Question with irregular verb"),
        (Q_M,  "Question with missed")
    )

    type = models.CharField(max_length=28, choices=QUESTION_TYPE ,help_text="Что это за вопрос : Вопрос-выбор, вопрос-перевод, вопрос с неправильным глаголом или вопрос с пропущенным словом")
    text = models.ForeignKey(QuestionText,on_delete=models.DO_NOTHING,null=True,blank=True,help_text="Текст вопроса - должен включать в себя задание!")
    exercise = models.CharField(max_length=1500,help_text="Текст задания")
    variants = models.CharField(max_length=1500, blank=True,help_text="Варианты, если множестевенный выбор, варианты через //")
    theme = models.ForeignKey(Theme, on_delete=models.DO_NOTHING,null=True,blank=True,help_text="К какому сборнику вопросов относится")
    answer = models.CharField(max_length=1500,help_text="Правильный ответ")
    rule = models.ForeignKey(Rule,on_delete=models.DO_NOTHING,null=True,blank=True,help_text="Правило, по которому правильный ответ правильный")

    def __str__(self):
        return str(self.exercise)



class Student(models.Model):
    class Meta:
        verbose_name_plural = "Students"
    name = models.CharField(max_length=150)
    surname = models.CharField(max_length=150)
    code = models.CharField(max_length=10)
#    group = models.ForeignKey(Group,on_delete=models.CASCADE)
    points = models.IntegerField(default=0)

    def __str__(self):
        return self.name + " " + self.surname


class StudentAndQuestion(models.Model):
    question = models.ForeignKey(Question,on_delete=models.CASCADE)
    student = models.ForeignKey(Student,on_delete=models.CASCADE)
    is_first_time = models.BooleanField(default=1)
    is_learned = models.BooleanField(default=0)
    points = models.IntegerField(default=0)

    def __str__(self):
        return str(self.student.name + " and " + self.question.text.name + " -> " + str(self.points) + "points")

    def calculate_points(self):
        return self.points
