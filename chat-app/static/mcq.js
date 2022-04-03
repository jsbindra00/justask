let poll = { 
    question:"",
    answers:[
      //"C", "Java", "PHP", "JavaScript"
    ],
    pollCount:0,
    answersWeight: [0, 0, 0, 0],
    selectedAnswer:-1
};

let pollDOM = {
    question:document.querySelector(".poll .question"),
    answers:document.querySelector(".poll .answers")
};

document.getElementById("message_input_form").onsubmit = function(e){
    e.preventDefault();
    const quest = document.getElementById("question_input");
    var inputForm = document.getElementById("answerDiv").getElementsByTagName("input");
    var len = inputForm.length
    pollDOM.question.innerHTML = quest.value.trim();
    poll.answers = [];
    for(let j = 0; j < len; j++){
        var id = "answer" + j;
        option = document.getElementById(id).value.trim();
        poll.answers.push(option);
    }
    document.getElementById("poll").style.display = "inline";
    pollDOM.answers.innerHTML = poll.answers.map(function(answer, i){
    return (    
        `
            <div class="answer" id="option${i}" onclick="markAnswer ('${i}')">
                ${answer}
                <span class="percentage-bar"></span>
                <span class="percentage-value"></span>
            </div>
        `
    );
}).join("");
}

function add(){
    var answerDiv = document.getElementById("answerDiv");
    var len = answerDiv.getElementsByTagName("input").length;
    var newEntry = document.createElement("input");
    id = "answer" + len;
    placeholder = "Option " + (len +1);
    newEntry.setAttribute("id", id);
    newEntry.setAttribute("placeholder", placeholder);
    newEntry.required = true;
    newEntry.classList.add("answerDiv");
    if (len < 6){
        poll.answersWeight.push(0)
        return(answerDiv.append(newEntry));
    }
    else{
        return alert("no more than 6 possible answers");
    }
}
function del(){
    var answers = document.getElementById("answerDiv").getElementsByTagName("input");
    var len = answers.length
    if (len > 1){
        answers[len-1].remove();
        return poll.answersWeight.pop()
    }
    else{
        return alert("One option required");
    }
}

function markAnswer(i){
    poll.selectedAnswer = +i;
    const length = document.querySelectorAll(".poll .answers .answer").length
    try {
        document.querySelector(".poll .answers. answer.selected").classList.remove("selected"); 
    } catch(msg){}
    document.querySelectorAll(".poll .answers .answer")[+i].classList.add("selected");
    showResults();
    for(let k = 0; k< length; k++){
        if (k == i){
            continue;
        }
        document.querySelectorAll(".poll .answers .answer")[+k].classList.add("disabledbutton");
    }
}

function showResults(){
    let answers = document.querySelectorAll(".poll .answers .answer");
    for (let i=0; i<answers.length; i++){
        let percentage = 0;
        var id = "option" + i;
        if(i == poll.selectedAnswer){
            percentage = Math.round((poll.answersWeight[i]+1) * 100 / (poll.pollCount+1));
        } else {
            percentage = Math.round((poll.answersWeight[i]) * 100/ (poll.pollCount+1));
        }
        answers[i].querySelector (".percentage-bar").style.width = percentage + "%";
        answers[i].querySelector (".percentage-value").innerText = percentage + "%";
    }
}
// Get the modal
var modal = document.getElementById("myModal");

// Get the button that opens the modal
var btn = document.getElementById("myBtn");

// Get the <span> element that closes the modal
var span = document.getElementsByClassName("close")[0];

// When the user clicks the button, open the modal 
btn.onclick = function() {
modal.style.display = "block";
}

// When the user clicks on <span> (x), close the modal
span.onclick = function() {
modal.style.display = "none";
}
// When the user posts question, close the modal
post.onclick  = function() {
modal.style.display = "none";
}
// When the user clicks anywhere outside of the modal, close it
window.onclick = function(event) {
    if (event.target == modal) {
        modal.style.display = "none";
    }
}    