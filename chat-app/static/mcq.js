class poll {
    constructor(){
        this.question = "";
        this.options = [];
        this.pollCount = 0;
        this.answersWeight = [0,0,0,0,0,0];
        this.selectedAnswer = -1;
        this.id = 0;
    }
    
}

let pollDOM = {
    question:document.querySelector(".poll .question"),
    answers:document.querySelector(".poll .answers")
};
let pollArray = [];

function ClientRequestSendPoll(){
    
    const newPoll = new poll();
    newPoll.id = pollArray.length;
    
    let quest = document.getElementById("question_input").value.trim();
    newPoll.question = quest;
    //pollDOM.question.innerHTML = quest;

    let inputForm = document.getElementById("answerDiv").getElementsByTagName("input");
    let len = inputForm.length;

    for(let j = 0; j < len; j++){
        var id = "answer" + j;
        option = document.getElementById(id).value.trim();
        newPoll.options.push(option);
    }
    pollArray.push(newPoll);
    pollDiv = $('<div>',
    {
        "style" : "cursor : pointer",
        "id"    : "Poll" + newPoll.id,
        "html"  : "Poll " + (newPoll.id + 1),
        "onclick": "ClientRequestPoll(\"" + newPoll.id + "\")",
    });
    $('#question-list-wrapper').append(pollDiv);
    //window.localStorage.setItem('content', pollDiv[0].outerHTML)
}
function ClientRequestPoll(id){
    id = parseInt(id);
    
    for (i = 0;i < pollArray.length; i++){
        if (pollArray[i].id == id){
            break;
        }
    }
    let pollData = pollArray[i];
    pollDOM.question.innerHTML = pollData.question;
    document.getElementById("poll").style.display = "inline";
    pollDOM.answers.innerHTML = pollData.options.map(function(answer, i){
        return (
        `
            <div class="answer" id="option${i}" onclick="markAnswer(${pollData.id},${i})">
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
    let len = answerDiv.getElementsByTagName("input").length;
    let newEntry = document.createElement("input");
    id = "answer" + len;
    placeholder = "Option " + (len +1);
    newEntry.setAttribute("id", id);
    newEntry.setAttribute("placeholder", placeholder);
    newEntry.required = true;
    newEntry.classList.add("answerDiv");
    if (len < 6){
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
        return(answers[len-1].remove()); 
    }
    else{
        return alert("One option required");
    }
}

function markAnswer(id,i){
    for (j = 0;j < pollArray.length; j++){
        if (pollArray[j].id == id){
            var pollData = pollArray[j];
            break;
        }
    }
    pollData.selectedAnswer = +i;
    var length = document.querySelectorAll(".poll .answers .answer").length
    try {
        document.querySelector(".poll .answers. answer.selected").classList.remove("selected"); 
    } catch(msg){}
    document.querySelectorAll(".poll .answers .answer")[+i].classList.add("selected");
    showResults(pollData);
    pollData.pollCount++;
    for(let k = 0; k< length; k++){
        if (k == i){
            continue;
        }
        document.querySelectorAll(".poll .answers .answer")[+k].classList.add("disabledbutton");
    }
}

function showResults(pollData){

    let answers = document.querySelectorAll(".poll .answers .answer");
    for (let i=0; i<answers.length; i++){
        let percentage = 0;
        //var id = "option" + i;
        if(i == pollData.selectedAnswer){
            percentage = Math.round((pollData.answersWeight[i]+1) * 100 / (pollData.pollCount+1));
            pollData.answersWeight[i]++;
        } else {
            percentage = Math.round((pollData.answersWeight[i]) * 100/ (pollData.pollCount+1));
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
$(document).ready(function(){
    //$('#question-list-wrapper').append(window.localStorage.getItem('content'));
    $('#message_input_form').submit(function(e){e.preventDefault(); ClientRequestSendPoll();});
    $('#add-option').click(function(){add();});
    $('#delete-option').click(function(){del();});
})
