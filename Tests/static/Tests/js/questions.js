function saveAnswer() {
    var question_type = document.getElementById("q-t").getAttribute("question_type");
    var question_id = document.getElementById("q-t").getAttribute("question_id");

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


    var question_number = document.getElementById("q-t").getAttribute("question_number")
    var question_count = document.getElementById("q-t").getAttribute("question_count")


    var q = {
        "question_id" : question_id,
        "user_answer" : user_answer,
        "tech_answer" : user_answer.toLowerCase().replace(/\s+/g, '')
    }

    localStorage.setItem("question_" + question_number,JSON.stringify(q))
}


window.onload = function load() {

    var question_count = document.getElementById("q-t").getAttribute("question_count")

    localStorage.setItem("question_count",question_count);

    var question_number = document.getElementById("q-t").getAttribute("question_number")
    var question_id = document.getElementById("q-t").getAttribute("question_id");
    var question_type = document.getElementById("q-t").getAttribute("question_type");
    var storedValue = JSON.parse(localStorage.getItem("question_" + question_number));

    if (storedValue) {
        switch (question_type) {
            case "QUESTION_TRANSLATE":
                document.getElementById("answer").value = storedValue.user_answer;
                break;
            case "QUESTION_IRREGULAR_VERB":
                var anwsers = storedValue.user_answer.split(" ");
                $("#firstForm").val(anwsers[0]);
                $("#secondForm").val(anwsers[1]);
                $("#thirdForm").val(anwsers[2]);
                break;

            case "QUESTION_SELECT":
                break;

            case "QUESTION_MISSED":
                document.getElementById("answer").value = storedValue.user_answer;
                break;
        }
    }


}
