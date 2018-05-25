window.onload = function() {
    $(function () {
      $('[data-toggle="tooltip"]').tooltip()
    });

    var testResults = checkTest();
    var html = "";
    var result;

    for(var k in testResults) {
       console.log(k, testResults[k]);

       if(testResults[k]["result"] === "correct") {
   //        addPoint(testResults[k]["question_id"]);
            result = "<i class=\"fas fa-check-circle\"></i>"
       } else {
           result = "<i class=\"fas fa-times-circle\"></i>"
       }
       question = getQuestion(testResults[k]["question_id"])
       question_name = question["text"];
       question_theme = question["theme"];
       question_points = getPoints(testResults[k]["question_id"]);
       question_variants = question["variants"];
       tooltipHTML = "<b>Вопрос: </b>"+question_name+"<br/>" + "<b>Варианты: </b>" + question_variants;

       html = "<div class=\"row\">\n" +
           "            <div class=\"col \">\n" + question_name +
           //"<span data-toggle=\"tooltip\" data-placement=\"right\" data-html=\"true\" title=\""+tooltipHTML+"\"><i class=\"far fa-question-circle\"></i></span>" +
           "            </div>\n" +
           "            <div class=\"col text-center align-middle\">\n" +
           "             " + result +
           "            </div>\n" +
           "            <div class=\"col text-center\">\n" +
           "             " + question_theme +
           "            </div>\n";

       document.getElementById("q-c").innerHTML+= html;
    }

}

