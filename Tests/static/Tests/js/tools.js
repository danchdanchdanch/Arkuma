var questionQueue = [];

function getStudentAndQuestion(question_id) {
    var result;
    var student_id = getCookie("student_id");

    $.ajax({
            url: '/API/StudentAndQuestion/get',
            async: false,
            data: {"question_id":question_id, "student_id":student_id},
            dataType: 'text',
            success: function (data) {
                result = JSON.parse(data);
            }
        });

    return result;
}

function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie != '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) == (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

function switchQuestionState(question_id) {
    var student_id = getCookie("student_id");


    $.ajax({
        async : false,
        url: '/API/switchQuestionState',
        contentType: 'application/json; charset=utf-8',
        data: {"question_id" : question_id,"student_id": student_id},
        dataType: 'text',
        beforeSend: function(xhr, settings) {
                if (!(/^http:.*/.test(settings.url) || /^https:.*/.test(settings.url))) {
                    // Only send the token to relative URLs i.e. locally.
                    xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
                }},
        success: function(result) {
            console.log(result);
        },
        error:function (result) {
            console.log(result);
        }
     });

    console.log("--------------------");
    console.log("Changing question state to non first");
    console.log("Student -> " + student_id);
    console.log("Question -> " + question_id);
    console.log("--------------------");
}

function markQuestionAsLearned(question_id) {
    var student_id = getCookie("student_id");


    $.ajax({
        async : false,
        url: '/API/markQuestionAsLearned',
        contentType: 'application/json; charset=utf-8',
        data: {"question_id" : question_id,"student_id": student_id},
        dataType: 'text',
        beforeSend: function(xhr, settings) {
                if (!(/^http:.*/.test(settings.url) || /^https:.*/.test(settings.url))) {
                    // Only send the token to relative URLs i.e. locally.
                    xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
                }},
        success: function(result) {
            console.log(result);
        },
        error:function (result) {
            console.log(result);
        }
     });

    console.log("--------------------");
    console.log("Changing question state to learned");
    console.log("Student -> " + student_id);
    console.log("Question -> " + question_id);
    console.log("--------------------");
}

function checkAnswer() {
    var question_id = document.getElementById("q-t").getAttribute("question_id");
    var theme_id = document.getElementById("main").getAttribute("theme_id")
    var result;

    var question_type = document.getElementById("q-t").getAttribute("question_type");
    var question_id = document.getElementById("q-t").getAttribute("question_id");

    var s_q = getStudentAndQuestion(question_id);

    switch (question_type) {
        case "QUESTION_TRANSLATE":
            var user_answer = document.getElementById("answer").value;
            break;
        case "QUESTION_IRREGULAR_VERB":
            var user_answer = $("#firstForm").val() + " " + $("#secondForm").val() + " " + $("#thirdForm").val();
            break;

        case "QUESTION_SELECT":

            var user_answer = $('input[name="options"]:checked').val();

            break;

        case "QUESTION_MISSED":
            var user_answer = document.getElementById("answer").value;
            break;
    }

    var answer = user_answer.toLowerCase().replace(/\s+/g, '');

    $.ajax({
        url: "/checkanswer",
        async: false,
        data : {question : question_id, answer : answer},
        dataType: 'text',
        success: function(data){
            result = JSON.parse(data);
          }
    });

    if (result["result"] == "correct") {
        if (s_q["isFirstTime"]) {
            markQuestionAsLearned(question_id);
        } else {
            addPoint(question_id)
        }

        questionJSON = getNextQuestion();
        renderQuestion(questionJSON["html"]);

    } else {
        if (s_q["isFirstTime"]) {
            switchQuestionState(question_id);
        }

        var div = document.createElement('div');
        var questionJSON = getQuestion(question_id);
        var data = questionJSON;
        var rigth_answer = data["answer"];
        var ruleHTML = data["rule"]["text"];
        div.className = "alert alert-danger";
        if (ruleHTML != "None") {
            div.innerHTML = "  <h4 class=\"alert-heading\">Ошибка!</h4>\n" +
                "<p class=\"mb-0\" > Правильный ответ : <b>" + rigth_answer + "</b></p>" +
                "  <hr>\n" +
                "<span> Правило : </span>" +
                "<span class=\"\" id=\"rules\">" + data["rule"]["text"] + "</span>"+"<br>";
        } else {
             div.innerHTML = "  <h4 class=\"alert-heading\">Ошибка!</h4>\n" +
                "<p class=\"mb-0\" > Правильный ответ : <b>" + rigth_answer + "</b></p>" +"<br>";
        }
        document.getElementById("alerts").appendChild(div);
        document.getElementById("check").innerHTML = "Понял!";
        document.getElementById("check").onclick = function() {
            questionQueue.push(question_id);
            questionJSON = getNextQuestion();
            renderQuestion(questionJSON["html"]);
        }
    }

}

function checkTest() {
    var question_count = localStorage.getItem("question_count");

    if (question_count > 0) {
        var result;
        var answers = {};
        answers.questions = {};

        for (var i = 1; i <= question_count; i++) {
            var question = "question_" + i;
            answers.questions[question] = {};
            answers.questions[question] = JSON.parse(localStorage.getItem(question));
        }

        $.ajax({
            url: '/check/',
            type: 'POST',
            async: false,
            contentType: 'application/json; charset=utf-8',
            data: JSON.stringify(answers),
            dataType: 'text',
            beforeSend: function (xhr, settings) {
                if (!(/^http:.*/.test(settings.url) || /^https:.*/.test(settings.url))) {
                    // Only send the token to relative URLs i.e. locally.
                    xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
                }
            },
            success: function (data) {
                result = JSON.parse(data);
            }
        });

        return result;
    }

    window.location.replace("/");

}

function addPoint(question_id) {
    var student_id = getCookie("student_id");


    $.ajax({
        url: '/addPoint/',
        contentType: 'application/json; charset=utf-8',
        data: {"question_id" : question_id,"student_id": student_id},
        dataType: 'text',
        beforeSend: function(xhr, settings) {
                if (!(/^http:.*/.test(settings.url) || /^https:.*/.test(settings.url))) {
                    // Only send the token to relative URLs i.e. locally.
                    xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
                }},
        success: function(result) {
            console.log(result);
        },
        error:function (result) {
            console.log(result);
        }
     });

    console.log("--------------------");
    console.log("Adding points");
    console.log("Student -> " + student_id);
    console.log("Question -> " + question_id);
    console.log("--------------------");
}

function newLife() {
    localStorage.clear();
    window.location.replace("/");
}

function getRuleForQuestion(question_id) {
    var result;

    $.ajax({
            url: '/getRule/',
            async: false,
            data: {"question_id":question_id},
            dataType: 'text',
            success: function (data) {
                result = JSON.parse(data);
            }
        });
    rule = result["rule"];
    return rule;
}

function getQuestion(question_id) {
    var result;

    $.ajax({
            url: '/API/getQuestion',
            async: false,
            data: {"question_id":question_id},
            dataType: 'text',
            success: function (data) {
                result = JSON.parse(data);
            }
        });

    return result;
}

function getQuestionsByTheme(theme_id) {

    var result;

    $.ajax({
            url: '/API/getQuestions',
            async: false,
            data: {"theme_id":theme_id},
            dataType: 'text',
            success: function (data) {
                result = JSON.parse(data);
            }
        });

    return result;

}

function getPoints(question_id) {
    var student_id = getCookie("student_id");
    var result;

    $.ajax({
        url: '/getPoints/',
        async: false,
        data: {"question_id" : question_id,"student_id": student_id},
        dataType: 'text',
        success: function(data) {
            result = JSON.parse(data);
        },
        error:function (data) {
            console.log(data);
        }
     });

    return result["points"];
}

function learning() {
    var questionJSON;
    var theme_id = document.getElementById("main").getAttribute("theme_id");
    var questionsJSON = getQuestionsByTheme(theme_id);



    for (var key in questionsJSON) {
        if (questionsJSON.hasOwnProperty(key)) {
            console.log(key + " -> " + questionsJSON[key]["question_id"]);

            questionQueue.push(questionsJSON[key]["question_id"]);

        }
    }


    /*for (var key in questionQueue) {
        questionJSON = getQuestion(questionQueue[3]);
        console.log(questionJSON);
        document.getElementById("q-t").innerHTML = questionJSON["html"];

        document.getElementById('check').onclick = function() {
            alert(key);
            alert(questionJSON["text"]);

        }

    }*/

    if (questionQueue.length > 0) {
        questionJSON = getNextQuestion();
        renderQuestion(questionJSON["html"]);
    } else {
        html = "            <div class=\"question-container\">\n" +
            "            \t<div class=\"row align-middle\">\n" +
            "            \t\t<div class=\"col\">\n" +
            "            \t\t<h4 class=\"h4 mb-3 font-weight-normal\">Cтранно!</h4>\n" +
            "            \t\t</div>\n" +
            "            \t</div>\n" +
            "            \t<div class=\"row\">\n" +
            "            \t\t<div class=\"col\">\n" +
            "            \t\t\t<h1 class=\"h4 mb-3 font-weight-normal\">Но вопросов по этой теме нет :(</h1>\n" +
            "            \t\t</div>\n" +
            "            \t</div>\n" +
            "            \t<div class=\"row\">\n" +
            "            \t\t<div class=\"col\">\n" +
            "            \t\t\t<a href=\"/learning/themes/\" class=\"btn btn-lg btn-primary btn-block\">Назад</a>\n" +
            "            \t\t</div>\n" +
            "            \t</div>\n" +
            "            </div>";
        renderQuestion(html)
    }

}

function getNextQuestion() {
    var questionJSON;
    console.log(questionQueue);
    var id;
    if(questionQueue.length > 0) {
        var id = questionQueue.shift();
        questionJSON = getQuestion(id);

        console.log(questionQueue);
        console.log(id);

        return questionJSON;
    } else {
        questionJSON = {}
        questionJSON["html"] = "            <div class=\"question-container\">\n" +
            "            \t<div class=\"row align-middle\">\n" +
            "            \t\t<div class=\"col\">\n" +
            "            \t\t<h4 class=\"h4 mb-3 font-weight-normal\">Отлично!</h4>\n" +
            "            \t\t</div>\n" +
            "            \t</div>\n" +
            "            \t<div class=\"row\">\n" +
            "            \t\t<div class=\"col\">\n" +
            "            \t\t\t<h1 class=\"h4 mb-3 font-weight-normal\">Ты решил все упражнения!</h1>\n" +
            "            \t\t</div>\n" +
            "            \t</div>\n" +
            "            \t<div class=\"row\">\n" +
            "            \t\t<div class=\"col\">\n" +
            "            \t\t\t<a href=\"/\" class=\"btn btn-lg btn-primary btn-block\">В меню!</a>\n" +
            "            \t\t</div>\n" +
            "            \t</div>\n" +
            "            </div>"

        return questionJSON;
    }
}

function renderQuestion(html) {
    document.getElementById("content").innerHTML = html;
}

function stopRKey(evt) {
   var evt = (evt) ? evt : ((event) ? event : null);
   var node = (evt.target) ? evt.target : ((evt.srcElement) ? evt.srcElement : null);
   if ((evt.keyCode == 13) && (node.type=="text")) {document.getElementById("check").click();}
   if ((evt.keyCode == 13) && (node.type=="radio")) {document.getElementById("check").click();}
   if ((evt.keyCode == 13) && (node.type=="checkbox")) {document.getElementById("check").click();}
   if ((evt.keyCode == 13) && (node.type=="textarea")) {document.getElementById("check").click();}
   if ((evt.keyCode == 13) && (node.type=="dropdown")) {return false;}
}
