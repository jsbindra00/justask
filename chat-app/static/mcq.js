

const socket = io.connect("http://127.0.0.1:5000");
var ACITVE_POLL = false

function ClientRequestJoinMCQ(){
    socket.emit('REQ_JOIN',{
        username: "{{ username }}",
        room: "{{ room }}"
    })
}

function ClientAcknowledgeJoinMCQ(data){
    $('#session-clients').append(`<div class="session-client">${data.username}</div>`)
    roomID = data.ACTIVE_SESSION
    ClientRequestPollCache()
}
function ClientRequestPollCache(){
    socket.emit('REQ_POLL_CACHE', {
        room: roomID
    })
}
function ClientAcknowledgePollCache(data){
    var poll_history = data.poll_history
    for (let polls of data.poll_history){
        if (hasUserVoted(poll_history, polls["mcq_id"], data["username"])[0]){
            polls["index"] = hasUserVoted(poll_history, polls["mcq_id"], data["username"])[1]
            ClientAcknowledgeSendPoll(polls)
            ClientAcknowledgePollVote(polls)
        }
        else{
            ClientAcknowledgeSendPoll(polls)
        }
    }
}
function hasUserVoted(poll_history, mcq_id, user){
    for (let polls of poll_history){
        if(polls["from_user"] == user && polls["mcq_id"] == mcq_id){
            for (var i = 1; i <=4; i++){
                if (polls["option_" + i + "_vote"] >0){
                    break
                }
            }
            return [true, i]
        }
    }
    return [false, 0]

}
function ClientRequestSendPoll(){
    
    let quest = document.getElementById("question_input").value.trim();

    let inputForm = document.getElementById("answerDiv").getElementsByTagName("input");
    let len = inputForm.length;
    var options =[]
    for(let j = 0; j < len; j++){
        var id = "answer" + j;
        option = document.getElementById(id).value.trim();
        options.push(option);
    }
    if (options != null) {
        socket.emit('REQ_SEND_POLL', {
            question : quest,
            option_1 : options[0],
            option_2 : options[1],
            option_3 : options[2],
            option_4 : options[3],
        })
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
    var i = data["index"];
    var current_poll = getPoll(data["mcq_id"])
    var length = current_poll.querySelectorAll(".answers .answer").length
    try {
        current_poll.querySelector(".answers. answer.selected").classList.remove("selected"); 
    } catch(msg){}
    current_poll.querySelectorAll(".answers .answer")[i-1].classList.add("selected");
    showResults(data, current_poll);
    for(let k = 0; k< length; k++){
        if (k == (i-1)){
            current_poll.querySelectorAll(".answers .answer")[k].classList.add("disabledbutton2");
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
        let entry = "option_" + i;
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
        const question_list_div = $('<div>',{
            "class" : "question-list",
            "stlye" : "cursor : pointer",
            "id"    : "P" + data["mcq_id"]
        }).append(`${data["question"]}`)
        createPollDiv(data)
        question_list_div.on("click", function() {
            ClientShowPoll(data)
        })
        $('#question-list-wrapper').append(question_list_div);
    }
    
    function getVote(data, i){
        return data["option_" + i +"_vote"];
    }
    
    function getPollCount(data){
        var pollCount = 0;
        for (let i = 1 ; i <= 4; i++){
            pollCount= pollCount + data["option_" + i + "_vote"];
        }
        return pollCount;
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

    
    socket.on('connect', ClientRequestJoinMCQ)
    socket.on('ACK_SEND_POLL', ClientAcknowledgeSendPoll)
    socket.on('ACK_POLL_VOTE', ClientAcknowledgePollVote)
    socket.on('ACK_JOIN', function(data){ClientAcknowledgeJoinMCQ(data)})
    socket.on('ACK_POLL_CACHE_UPDATE', function(data){ClientAcknowledgePollCache(data)})
})
