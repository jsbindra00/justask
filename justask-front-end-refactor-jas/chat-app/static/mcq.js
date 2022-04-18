

const socket = io.connect("http://127.0.0.1:5000");
var ACITVE_POLL = false
class poll {
    constructor(){
        this.question = "";
        this.options = [];
        this.pollCount = 25;
        this.answersWeight = [2,10,7,5,6,0];
        this.selectedAnswer = -1;
        this.id = 0;
    } 
}
let pollArray = [];

function ClientRequestSendPoll(){
    
    const newPoll = new poll();
    newPoll.id = pollArray.length;
    
    let quest = document.getElementById("question_input").value.trim();
    newPoll.question = quest;

    let inputForm = document.getElementById("answerDiv").getElementsByTagName("input");
    let len = inputForm.length;

    for(let j = 0; j < len; j++){
        var id = "answer" + j;
        option = document.getElementById(id).value.trim();
        newPoll.options.push(option);
    }
    if (newPoll != null) {
        socket.emit('REQ_SEND_POLL', {
            question : newPoll.question,
            option1 : newPoll.options[0],
            option2 : newPoll.options[1],
            option3 : newPoll.options[2],
            option4 : newPoll.options[3],
        })
    }
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

function ClientSendPollVote(i, data){
    socket.emit('REQ_SEND_POLL_VOTE',{
        mcq_id : data["mcq_id"],
        index : i
    });
}
function getPoll(id){
    for (const poll of document.querySelectorAll(".poll")){
        if (poll.id == id){
            return poll;
        }
    }
}
function ClientAcknowledgePollVote(data){
    i = data["index"];
    var current_poll = getPoll(data["mcq_id"])
    var length = current_poll.querySelectorAll(".answers .answer").length
    try {
        current_poll.querySelector(".answers. answer.selected").classList.remove("selected"); 
    } catch(msg){}
    current_poll.querySelectorAll(".answers .answer")[i-1].classList.add("selected");
    showResults(data, current_poll);
    for(let k = 0; k< length; k++){
        if (k == (i-1)){
            continue;
        }
        current_poll.querySelectorAll(".answers .answer")[k].classList.add("disabledbutton");
    }
}
function showResults(data, current_poll){
    selectedAnswer = data["index"]
    let answers = current_poll.querySelectorAll(".answers .answer");
    for (let i=1; i<=answers.length; i++){
        let percentage = 0;
        if(i == selectedAnswer){
            percentage = Math.round((getVote(data,i)) * 100 / (getPollCount(data)));

        } else {
            percentage = Math.round((getVote(data,i)) * 100/ (getPollCount(data)));
        }
        answers[i-1].querySelector (".percentage-bar").style.width = percentage + "%";
        answers[i-1].querySelector (".percentage-value").innerText = percentage + "%";
    }
}

function ClientShowPoll(data){
    if (ACITVE_POLL == false){
        $('#' + data["mcq_id"]).show()
        ACITVE_POLL = true
    }
    else{
        for (const poll of document.querySelectorAll(".poll")){
            if (poll.id != data["mcq_id"]){
                $('#' + poll.id).hide()
            }
        }
        $('#' + data["mcq_id"]).show()
    }
}
function createPollDiv(data){
    var pollDiv = document.createElement("div")
    pollDiv.classList.add("poll")
    pollDiv.setAttribute("id", data["mcq_id"])
    $('#poll-wrapper').append(pollDiv)
    let questionDiv = createQuestionDiv(data["question"])
    let answerDiv = createAnswerDiv(data)
    pollDiv.append(questionDiv, answerDiv)
    
   assignMarkAnswer(data)
}
function assignMarkAnswer(data){
    for (let k=1; k <= 4; k++){
        let answerID = "option" + k + data["mcq_id"];
        var answerDiv = document.getElementById(answerID);
        answerDiv.addEventListener("click", function(){
            ClientSendPollVote(k, data)
        });
    }

}
function createQuestionDiv(question){
    let div = document.createElement("div");
    div.classList.add("question");
    div.innerHTML = question;
    return div
}

function createAnswerDiv(data){
    let answers = document.createElement("div");
    answers.classList.add("answers")

    var options = [];
    for (let i=1; i <=4; i++){
        let entry = "option" + i;
        options.push(data[entry])
    }
    answers.innerHTML = options.map(function(answer, i){
        return (
            `
            <div class="answer" id="option${i+1}${data["mcq_id"]}">
            ${answer}
            <span class="percentage-bar"></span>
            <span class="percentage-value"></span>
            </div>
            `
            );
        }).join("");
    return answers

}

function ClientAcknowledgeSendPoll(data){
    var question_list_div = document.createElement("div");
    question_list_div.setAttribute("style", "cursor : pointer");
    question_list_div.innerHTML = data["question"];
    question_list_div.id = "P" + data["mcq_id"]
    createPollDiv(data)
    question_list_div.addEventListener("click", function() {
        ClientShowPoll(data)
    })
    $('#question-list-wrapper').append(question_list_div);
}

function getVote(data, i){
    return data["vote"+i];
}

function getPollCount(data){
    var pollCount = 0;
    for (let i = 1 ; i <= 4; i++){
        pollCount= pollCount + data["vote" + i];
    }
    return pollCount;
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
    $('#message_input_form').submit(function(e){e.preventDefault(); ClientRequestSendPoll();});
    $('#add-option').click(function(){add();});
    $('#delete-option').click(function(){del();});

    socket.on('ACK_SEND_POLL', ClientAcknowledgeSendPoll)
    socket.on('ACK_POLL_VOTE', ClientAcknowledgePollVote)
})
