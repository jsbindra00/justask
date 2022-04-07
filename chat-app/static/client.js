

const socket = io.connect("http://127.0.0.1:5000");
var roomID = ""

var ACTIVE_SORT;

var CURRENTLY_RESPONDING_TO_MESSAGE_ID = "";
var voted_messages = []


function SignOfNumber(num){
    if(num < 0) return -1;
    if (num == 0) return 0;
    if (num > 0) return num;
}


function MessageExists(message_id){
    
    for (var j=0; j<voted_messages.length; ++j) {

        if(voted_messages[j].message_id == message_id) return true;
    }
    return false;
}
function HasMessageBeenVotedByUser (message_id, vote_amount) {


function ClientRequestJoin(){
    socket.emit('REQ_JOIN', {
        username: "{{ username }}",
        room: "{{ room }}"
    });
}


    for (var j=0; j<voted_messages.length; ++j) {

        let current_message = voted_messages[j]

        if(current_message.message_id == message_id){
            
            return (SignOfNumber(current_message.vote_amount) == SignOfNumber(vote_amount))
        } 
    }
    return false;
}


function RespondToMessage(message_id){
    CURRENTLY_RESPONDING_TO_MESSAGE_ID = message_id;
    $("#commenting-status").show();
    //alert("responding " + CURRENTLY_RESPONDING_TO_MESSAGE_ID);
}
function ViewMessageFlairs(message_id){
    // alert("view flairs " +  message_id)
}


function LocalUpdateMessageVoteChange(message_id,current_vote_amount, vote_amount){
    
    for (var j=0; j<voted_messages.length; ++j) {
        let current_message = voted_messages[j]
        if(current_message.message_id == message_id){
            if (SignOfNumber(current_message.vote_amount) == SignOfNumber(vote_amount)) return false;
            current_message.vote_amount = current_message.vote_amount + vote_amount;
            return true
        } 
    }
    voted_messages.push({message_id : message_id, vote_amount : current_vote_amount});
    return false;
}
function ClientRequestVoteChange(message_id, vote_amount){

    target = $("#" + message_id).find("*").find(".message-vote-count").get(0)
    if (!LocalUpdateMessageVoteChange(message_id, parseInt(target.textContent), vote_amount)) return;

    
    new_upvote_amount = parseInt(target.textContent) + vote_amount;
    socket.emit('REQ_MESSAGE_VOTE_CHANGE', {message_id : message_id, vote_amount: new_upvote_amount, session_id : roomID});
}

function ClientAcknowledgeVoteChange(data){
    message_id = data.message_id;
    vote_amount = data.vote_amount;
    target = $("#" + message_id).find("*").find(".message-vote-count").get(0)
    target.textContent = vote_amount;
}

function ClientRequestJoin(){
    socket.emit('REQ_JOIN', {
        username: "{{ username }}",
        room: "{{ room }}"
    });
}

function ClientAcknowledgeJoin(data){
    
    if (data.username !== "{{username}}") {
        const newNode = document.createElement('div');
        newNode.className = "acknowledge";
        newNode.innerHTML = `<b>${data.time} ${data.username} has joined the room</b>`;
        document.getElementById('messages').appendChild(newNode);
    }
    $('#session-clients').append(`<div class="session-client">${data.username}</div>`)
    roomID = data.ACTIVE_SESSION;
    ClientRequestMessageCacheUpdate()

}

function ClientRequestSendMessage(){

    let message_input = document.getElementById('chatbar');
    let message = message_input.value.trim();
    if (message.length) {
        socket.emit('REQ_SEND_MESSAGE', {
            message: message,
            FROM_PARENT_ID : CURRENTLY_RESPONDING_TO_MESSAGE_ID
        })
    }

    message_input.value = '';
    message_input.focus();
}

function ConstructMessage(username,time,message_id,message,vote_count, time_since_epoch){

    master_wrapper_class = (CURRENTLY_RESPONDING_TO_MESSAGE_ID == ""? "message-wrapper-master" : "message-wrapper-master-child") 
    
    const messageNodeWrapper = $('<div/>', {
        "class" : master_wrapper_class,
        // "class" : "message-wrapper-master",
        "id" : message_id,
        "time_since_epoch" : time_since_epoch,
        "FROM_PARENT_ID" : CURRENTLY_RESPONDING_TO_MESSAGE_ID
    })

    const messageNode = $('<div/>',
     {
         "class" : "message-wrapper " + ((username == $('#username-metadata').attr("username"))? "native" : "foreign"),
        });
    

    const messageHeader = $('<div/>',
    {
        "class" : "message-header"
    }).append(`<p>${username}</p><p>at</p><p>${time}</p>`);

    const messagePayload = $('<div/>',
    {
        "class" : "message-payload"
    }).append(`<p>${message}</p>`);


    const messagePropertiesWrapper = $('<div/>',
    {
        "class" : "message-properties-wrapper"
    });


    const commentProperty = $('<li/>',
    {
        "class" : "message-property",
        "id": "commenting_wrapper",
        "click" : function(){RespondToMessage(message_id);}

    }).append(
        `
        <i style="display:inline;" class="fa-regular fa-comment-dots fa-lg"></i> 
        <a class="comment-button">Comment</a>
        `
    );
    const messageProperties = $('<ul/>', 
    {
        "class" : "message-properties"
    }).append(commentProperty);

    messagePropertiesWrapper.append(messageProperties)
    const messageResponse = $('<div/>',
    {
        "class" : "message-response"
    });


    const votingProperty = $('<div/>', {
        "class" : "message-property message-voting"
    });
    const votingIcons = $('<ul/>', {
        "class" : "voting-icons"
    });
    

    const upvoteMessage = $('<div/>', {
        "class" : "message-vote upvote-message",
        "click" : function(){ClientRequestVoteChange(message_id, 1)}
    }).append(`<i class="fa-solid fa-caret-up fa-2xl"></i>`)
    const voteCountWrapper = $('<div/>',{
        "class":"message-vote-count-wrapper"
    }).append(`<div class="message-vote-count">${vote_count}</div>`);
    const downvoteMessage = $('<div/>', {
        "class" : "message-vote downvote-message",
        "click" : function(){ClientRequestVoteChange(message_id, -1)}
    }).append(`<i class="fa-solid fa-caret-down fa-2xl"></i>`)

    votingIcons.append(upvoteMessage).append(downvoteMessage);
    

    
    votingProperty.append(upvoteMessage);
    votingProperty.append(voteCountWrapper);
    votingProperty.append(downvoteMessage);


    messageNode.append(messageHeader);
    messageNode.append(messagePayload);
    messageNode.append(messagePropertiesWrapper);
    messageNode.append(messageResponse);

    messageNodeWrapper.append(votingProperty);
    messageNodeWrapper.append(messageNode);

    return messageNodeWrapper;
}
function AppendMessage(message)
{
    if (CURRENTLY_RESPONDING_TO_MESSAGE_ID != ""){
        $('#' + CURRENTLY_RESPONDING_TO_MESSAGE_ID).find(".message-response").append(message)
    } 

    else{
        // alert("appending to body")
        $('#messages').append(message);
    } 
    var messageBody = document.querySelector('#messages');
    messageBody.scrollTop = messageBody.scrollHeight - messageBody.clientHeight;
    // SortMessages(ACTIVE_SORT)
}
function ClientAcknowledgeSendMessage(data){
    messageNodeWrapper = ConstructMessage(data.username, data.time, data.message_id, data.message, data.vote_count, data.time_since_epoch)
    AppendMessage(messageNodeWrapper)
}
function ClientRequestLeave(){
    socket.emit('REQ_LEAVE', {
        room: "{{ room }}"
    })
}
function ClientAcknowledgeLeave(data){
    const newNode = document.createElement('div');
    newNode.className = "acknowledge";
    newNode.innerHTML = `<b>${data.username}</b> has left the room`;
    document.getElementById('messages').appendChild(newNode);
}

function SortByFlairPredicate(flairname){

}
function SortByDatePredicate(message_a, message_b){
    let message_a_time_since_epoch = parseInt(message_a.getAttribute("time_since_epoch"))
    let message_b_time_since_epoch = parseInt(message_b.getAttribute("time_since_epoch"))

    return (message_a_time_since_epoch > message_b_time_since_epoch) ? 1 : -1;
}
function SortByUpvotesPredicate(message_a, message_b){
    let message_a_upvotes = parseInt(message_a.querySelector(".message-vote-count").innerText)
    let message_b_upvotes = parseInt(message_b.querySelector(".message-vote-count").innerText)

    return (message_a_upvotes > message_b_upvotes) ? 1 : -1;
}
function SortByAscendingUpvotesPredicate(message_a, message_b){
    return SortByUpvotesPredicate(message_a, message_b)
}
function SortByDescendingUpvotesPredicate(message_a, message_b){
    return SortByUpvotesPredicate(message_a, message_b) * -1;
}
function SortByAscendingDatePredicate(message_a,message_b){
    return SortByDatePredicate(message_a, message_b)
}
function SortByDescendingDatePredicate(message_a,message_b){
    return SortByDatePredicate(message_a,message_b) * -1;
}

function SortMessages(predicate){


    // only get the first parents as we want 
    var to_sort = document.getElementsByClassName('message-wrapper-master')
    to_sort = Array.prototype.slice.call(to_sort, 0);

    to_sort.sort(predicate)

    var parent = document.getElementById('messages')
    parent.innerHTML = "";

    for(var i = 0, l = to_sort.length; i < l; i++) {
        parent.appendChild(to_sort[i]);
    }

    

    ACTIVE_SORT = predicate;
}


function ClientRequestMessageCacheUpdate(){
    socket.emit("REQ_MESSAGE_CACHE_UPDATE", {from_session_id : roomID})

}
function ClientAcknowledgeMessageHistoryCache(packet){
    message_history = packet.MESSAGE_HISTORY
    for(var i = 0; i < message_history.length; ++i){
        current_msg_json = message_history[i]
        msg = ConstructMessage(current_msg_json.FROM_USER, current_msg_json.DATE_SENT, current_msg_json.MESSAGE_ID, current_msg_json.PAYLOAD, current_msg_json.NUM_UPVOTES, current_msg_json.TIME_SINCE_EPOCH);
        AppendMessage(msg)
    }
}

// function attachflair(flair){
//     if (flair == "question"){
//         alert("q")
//         return "Question"
//     }else if (flair == "feedback"){
//         alert("f")
//         return "Feedback"
//     }else if (flair == "discussion"){
//         alert("d")
//         return "Discussion"
//     }
//     return ""
// }


$(document).ready(function(){
    $('#message_input_form').submit(function(e){e.preventDefault(); ClientRequestSendMessage();});
    $('#leave-session').click(ClientRequestLeave);
    $('#most-popular').click(function(){SortMessages(SortByDescendingUpvotesPredicate)})
    $('#least-popular').click(function(){SortMessages(SortByAscendingUpvotesPredicate)})
    $('#newest').click(function(){SortMessages(SortByAscendingDatePredicate)})
    $('#oldest').click(function(){SortMessages(SortByDescendingDatePredicate)})

    $("#message_input_form").click(function(){
        $("#commenting-status").hide();
    });
    $('.flair').on('click', function(){
	$('.flair-options').toggle();
	});

    

    socket.on('ACK_VOTE_CHANGE', function(data){ClientAcknowledgeVoteChange(data);});
    socket.on('ACK_SEND_MESSAGE', ClientAcknowledgeSendMessage);
    socket.on('connect', ClientRequestJoin)
    socket.on('ACK_JOIN', function(data){ClientAcknowledgeJoin(data)});
    socket.on('ACK_LEAVE', ClientAcknowledgeLeave);
    socket.on('ACK_MESSAGE_CACHE_UPDATE', function(data){ClientAcknowledgeMessageHistoryCache(data);});


    
    window.onbeforeunload = ClientRequestLeave;
})





















