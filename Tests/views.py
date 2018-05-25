from django.shortcuts import render
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.http import JsonResponse
from django.template import loader
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import redirect
from Tests.models import *

import json
import random
# Create your views here.


def index(request):
        session_id = request.COOKIES.get('student_id')
        if session_id is not None and session_id is not "":
            try:
                s = Student.objects.get(code=session_id)
            except ObjectDoesNotExist:
                response = HttpResponseRedirect("/")
                response.set_cookie('student_id', "")
                return response
            context = {
                "student" : s,
            }
            template = loader.get_template('Tests/index_logged.html')
            return HttpResponse(template.render(context,request))
        else:
            template = loader.get_template('Tests/index_login.html')
            return HttpResponse(template.render({},request))

        return HttpResponse("OKAY!")


def registration(request):
    if request.method == 'POST':
        return HttpResponse("NOT BAT")
    return render(request, 'Tests/reg.html',{})


def stat(request):
    session_id = request.COOKIES.get('student_id')
    if session_id != None:
        try:
            s = Student.objects.get(code=session_id)
        except ObjectDoesNotExist:
            return HttpResponse("NOT USER FINDED BY {}!".format(session_id))
        qd = StudentAndQuestion.objects.filter(student=s,is_learned=True)
        qil = StudentAndQuestion.objects.filter(student=s,is_learned=False)
        themes = Theme.objects.all()

        quil_val = 0
        quil = {}
        for t in themes:
            quil[t] = {}
            quil[t] = 0
            for q in qil:
                if q.is_first_time == False:
                    if q.question.theme == t:
                        quil_val = quil_val+1
                        quil[t] = quil[t] + 1

        quid = {}
        for t in themes:
            quid[t] = {}
            quid[t] = 0
            for q in qd:
                if q.question.theme == t:
                    quid[t] = quid[t] + 1
        context = {
            "student": s,
            "questions_done" : qd,
            "questions_in_learning" :qil,
            "quil" : quil,
            "quil_val" : quil_val,
            "quid" : quid,
            "themes" : themes
        }
        template = loader.get_template('Tests/stat.html')
        return HttpResponse(template.render(context, request))


def login(request):
    student_id = request.GET.get('code', None)
    data = {
        'exist': Student.objects.filter(code=student_id).exists()
    }
    if data['exist']:
        data['message'] = 'A user with this code exists!'
    else:
        data['message'] = 'We have not student with this id!'
    return JsonResponse(data)


def test(request):
    theme_id = request.GET.get("theme_id")
    session_id = request.COOKIES.get('student_id')

    if session_id != None:
        try:
            s = Student.objects.get(code=session_id)
        except ObjectDoesNotExist:
            return HttpResponse("NOT USER FINDED BY {}!".format(session_id))
        t = Theme.objects.get(pk=theme_id);
        questions_by_theme = Question.objects.filter(theme=t)
        questions_to_learn = StudentAndQuestion.objects.filter(student=s, points__lte=3,question__in=questions_by_theme).order_by('?')
        questions_count = questions_to_learn.count()

        if questions_count > 0:
            paginator = Paginator(questions_to_learn, 1)
            page = request.GET.get('question')
            try:
                qs = paginator.page(page)
                page = int(page)
            except PageNotAnInteger:
                qs = paginator.page(1)
                page = 1
            except EmptyPage:
                qs = paginator.page(paginator.num_pages)
            if qs[0].question.type == "QUESTION_SELECT":
                vars = qs[0].question.variants.split("//")
                context = {
                    'learning': True,
                    'page': page,
                    'test': qs,
                    'points' : qs[0].points,
                    'question' : qs[0].question,
                    'questions_count' : questions_count,
                    'paginator' : paginator,
                    'var1' : vars[0],
                    'var2' : vars[1],
                    'var3' : vars[2],
                    'var4' : vars[3],
                    'theme_id': theme_id
                }
            elif qs[0].question.type == "QUESTION_IRREGULAR_VERB":
                q = qs[0].question.exercise.split("//")

                random_num = random.randint(1,3)

                if random_num == 1:
                    var1 = q[0]
                else:
                    var1 = ""
                if random_num == 2:
                    var2 = q[1]
                else:
                    var2 = ""
                if random_num == 3:
                    var3 = q[2]
                else:
                    var3 =""

                context = {
                    'learning': True,
                    'page': page,
                    'test': qs,
                    'points': qs[0].points,
                    'question': qs[0].question,
                    'questions_count': questions_count,
                    'paginator': paginator,
                    'var1': var1,
                    'var2': var2,
                    'var3': var3,
                    'theme_id': theme_id
                }
            else:
                context = {
                    'learning': True,
                    'page': page,
                    'test': qs,
                    'points': qs[0].points,
                    'question': qs[0].question,
                    'questions_count': questions_count,
                    'paginator': paginator,
                    'theme_id' : theme_id
                }

            return render(
                request,
                'Tests/question_base.html', context

            )
        else:
            template = loader.get_template("Tests/no_questions.html")
            return HttpResponse(template.render({},request))


def check_test(request):
    if request.is_ajax():
        if request.method == 'POST':
            json_object = request.body.decode("utf-8")

            j = json.loads(json_object)

            response = {}

            for q in j["questions"]:
                q_id = j["questions"][q]["question_id"]
                a = j["questions"][q]["tech_answer"]
                result = check_answer(question_id=q_id,answer=a).content.decode('utf8')
                response[q] = {}
                response[q]["question_id"] = q_id
                response[q]["result"] = json.loads(result)["result"]
            return JsonResponse(response)
    return JsonResponse({"Result":"Something gone bad"})


def check_answer(request=None,question_id=None,answer=None):
    if request:
        question_id = request.GET.get('question')
        answer = request.GET.get('answer')

    try:
        question = Question.objects.get(pk=question_id)
    except Question.DoesNotExist:
        raise Http404("Question does not exist")

    if answer:

        response = {}
        q_tech = question.answer.split("//")

        for q in q_tech:

            q_answer = q.replace(" ", "").lower()
            if q_answer == answer:
                response["result"] = 'correct'
                return JsonResponse(response)
        response["result"] = 'incorrect'
        return JsonResponse(response)

    raise Http404("Question does not exist")


def select_theme(request, type):
    if type == "learning":
        themes = Theme.objects.all()
        context = {
            "themes" : themes,
            "type" : "learning"
        }
        template = loader.get_template('Tests/select_theme.html')
        return HttpResponse(template.render(context, request))
    if type == "test":
        themes = Theme.objects.all()
        context = {
            "themes": themes,
            "type": "test"
        }
        template = loader.get_template('Tests/select_theme.html')
        return HttpResponse(template.render(context, request))

    return redirect("/")


def add_point(request):
        if request.method == 'GET':

            question_id = request.GET.get("question_id")
            student_id = request.GET.get("student_id")

            question = Question.objects.get(pk=question_id)
            student = Student.objects.get(code=student_id)

            s_q = StudentAndQuestion.objects.get(student=student,question=question)
            if s_q.points <= 3:
                s_q.points = s_q.points + 1

            if s_q.points == 4 :
                s_q.is_learned = True
            s_q.save()

            return JsonResponse({"Result":"okey!"})
        return JsonResponse({"Result":"Not okay"})


def learning(request):
    theme_id = request.GET.get("theme_id")

    template = loader.get_template('Tests/question_base.html')


    context = {
        "theme_id" : theme_id
    }
    return HttpResponse(template.render(context,request))


def result(request):
    return render(request,"Tests/result.html",{})

def get_points(request):
            question_id = request.GET.get("question_id")
            student_id = request.GET.get("student_id")

            question = Question.objects.get(pk=question_id)
            student = Student.objects.get(code=student_id)

            s_q = StudentAndQuestion.objects.get(student=student,question=question)

            return JsonResponse({"points":s_q.points})


def get_rule(request):
    theme_id = request.GET.get("theme_id")

    theme = Theme.objects.get(pk=theme_id)

    rule = theme.rule

    return JsonResponse({"rule": rule})


def api_get_questions(request):
    session_id = request.COOKIES.get('student_id')
    theme_id = request.GET.get("theme_id")

    try:
        s = Student.objects.get(code=session_id)
    except ObjectDoesNotExist:
        raise Http404("User Not Found")
    try:
        questions = Question.objects.filter(theme=theme_id)
        questions_to_learn = StudentAndQuestion.objects.filter(student=s, points__lte=3,question__in=questions,
                                                               is_learned=False)
    except Question.DoesNotExist:
        raise Http404("Theme not found")


    response = {}

    i = 1

    for q in questions_to_learn:
        name = 'question_' + str(i)
        response[name] = {}
        response[name]["question_id"] = q.question.id

        i = i +  1

    return JsonResponse(response)


def api_get_question(request):
    if request:
        question_id = request.GET.get('question_id')

    try:
        question = Question.objects.get(pk=question_id)
    except Question.DoesNotExist:
        raise Http404("Question does not exist")

    response = {}

    response["text"]  = question.text.text
    response["theme"] = question.theme.name
    response["exercise"] = question.exercise
    response["variants"] = question.variants
    response["type"] = question.type
    response["answer"] = question.answer
    if question.rule == None:
        response["rule"] = {}
        response["rule"]["short_name"] = "None"
        response["rule"]["text"] = "None"
    else:
        response["rule"] = {}
        response["rule"]["short_name"] = question.rule.short_name
        response["rule"]["text"] = question.rule.rule

    if question.type == "QUESTION_SELECT":
        vars = question.variants.split("//")
        context = {
            'question': question,
            'var1': vars[0],
            'var2': vars[1],
            'var3': vars[2],
            'var4': vars[3]
        }
    elif question.type == "QUESTION_IRREGULAR_VERB":
        q = question.exercise.split("//")
        random_num = random.randint(1, 3)

        if random_num == 1:
            var1 = q[0]
        else:
            var1 = ""
        if random_num == 2:
            var2 = q[1]
        else:
            var2 = ""
        if random_num == 3:
            var3 = q[2]
        else:
            var3 = ""

        context = {
            'question': question,
            'var1': var1,
            'var2': var2,
            'var3': var3,
        }
    else:
        context = {
            'question': question
        }

    template = loader.get_template("Tests/questions.html")

    response["html"] = template.render(context,request)

    return JsonResponse(response)


def api_registration(request):
    if request.GET.get("name") != None:
        name = request.GET.get("name")
        surname = request.GET.get("surname")

        okay = False

        while(not okay):
            random.seed()
            a = str(random.randint(0,1))
            b = str(random.randint(1000,9999))

            code = a + b

            try:
                s = Student.objects.get(code=code)
            except ObjectDoesNotExist:
                s = Student()
                s.name = name
                s.surname = surname
                s.code = code
                s.save()

                responce = {}
                responce["result"] = "okey"
                responce["name"] = name
                responce["surname"] = surname
                responce["code"] = code

                return JsonResponse(responce)
                break

            continue
    return JsonResponse({"result":"error"})


def api_update_student_and_question(request):
    question_id = request.GET.get('question_id')
    student_id = request.GET.get('student_id')

    pass


def api_switch_question_state(request):
    if request.method == 'GET':

        question_id = request.GET.get("question_id")
        student_id = request.GET.get("student_id")

        question = Question.objects.get(pk=question_id)
        student = Student.objects.get(code=student_id)

        s_q = StudentAndQuestion.objects.get(student=student, question=question)

        s_q.is_first_time = False

        s_q.save()

        return JsonResponse({"Result": "okey!"})
    return JsonResponse({"Result": "Not okay"})


def api_mark_as_learned(request):
    if request.method == 'GET':

        question_id = request.GET.get("question_id")
        student_id = request.GET.get("student_id")

        question = Question.objects.get(pk=question_id)
        student = Student.objects.get(code=student_id)

        s_q = StudentAndQuestion.objects.get(student=student, question=question)

        s_q.is_learned = True

        s_q.save()

        return JsonResponse({"Result": "okey!"})
    return JsonResponse({"Result": "Not okay"})


def api_student_and_question_get(request):
    question_id = request.GET.get("question_id")
    student_id = request.GET.get("student_id")

    question = Question.objects.get(pk=question_id)
    student = Student.objects.get(code=student_id)

    s_q = StudentAndQuestion.objects.get(student=student, question=question)

    response = {}
    response["isFirstTime"] = s_q.is_first_time
    response["isLearned"] = s_q.is_learned
    response["points"] = s_q.points

    return JsonResponse(response)