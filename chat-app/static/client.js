

const socket = io.connect("192.168.0.29:5000");
var roomID = ""




function ConvertJSONToMessage(){

}

function ClientRequestVoteChange(message_id, vote_amount, sesh_id){

    new_upvote_amount = parseInt($("#" + message_id).find("*").find(".message-vote-count").text()) + vote_amount
    socket.emit('REQ_MESSAGE_VOTE_CHANGE', {message_id : message_id, vote_amount: new_upvote_amount, session_id : sesh_id});
}

function ClientAcknowledgeVoteChange(data){
    message_id = data.message_id;
    vote_amount = data.vote_amount;

    upvote_amount_p = $("#" + message_id).find("*").find(".message-vote-count");
    upvote_amount_p.text(vote_amount) 
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
            message: message
        })
    }
    message_input.value = '';
    message_input.focus();
}



function ConstructMessage(username,time,message_id,message,vote_count){

    const messageNodeWrapper = $('<div/>', {
        "class" : "message-wrapper-master",
        "id" : message_id
    })

    // MESSAGE NODE
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


    // VOTING

    const votingProperty = $('<div/>', {
        "class" : "message-property message-voting"
    });
    const votingIcons = $('<ul/>', {
        "class" : "voting-icons"
    });

    

    const upvoteMessage = $('<div/>', {
        "class" : "message-vote upvote-message",
        "click" : function(){ClientRequestVoteChange(message_id, 1, session_id)}
    }).append(`<i class="fa-solid fa-caret-up fa-2xl"></i>`)
    const voteCountWrapper = $('<div/>',{
        "class":"message-vote-count-wrapper"
    }).append(`<div class="message-vote-count">${vote_count}</div>`);
    const downvoteMessage = $('<div/>', {
        "class" : "message-vote downvote-message",
        "click" : function(){ClientRequestVoteChange(message_id, -1, session_id)}
    }).append(`<i class="fa-solid fa-caret-down fa-2xl"></i>`)

    votingIcons.append(upvoteMessage).append(downvoteMessage);
    

    
    votingProperty.append(upvoteMessage);
    votingProperty.append(voteCountWrapper);
    votingProperty.append(downvoteMessage);


    messageNode.append(messageHeader);
    messageNode.append(messagePayload);
    messageNodeWrapper.append(votingProperty);
    messageNodeWrapper.append(messageNode);

    return messageNodeWrapper;
}
function AppendMessage(message)
{
    $('#messages').append(message);

    var messageBody = document.querySelector('#messages');
    messageBody.scrollTop = messageBody.scrollHeight - messageBody.clientHeight;

}
function ClientAcknowledgeSendMessage(data){
    messageNodeWrapper = ConstructMessage(data.username, data.message_id, data.time, data.payload, data.vote_count)
    AppendMessage(messageNde)
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
function SortMessages(predicate){

    var to_sort = document.getElementsByClassName('message-wrapper-master')
    to_sort = Array.prototype.slice.call(to_sort, 0);

    to_sort.sort(predicate)

    var parent = document.getElementById('messages')
    parent.innerHTML = "";

    for(var i = 0, l = to_sort.length; i < l; i++) {
        parent.appendChild(to_sort[i]);
    }

    
}





function ClientRequestMessageCacheUpdate(){
    socket.emit("REQ_MESSAGE_CACHE_UPDATE", {from_session_id : roomID})
}
function ClientAcknowledgeMessageHistoryCache(packet){
    message_history = packet.MESSAGE_HISTORY
    for(var i = 0; i < message_history.length; ++i){
        current_msg_json = message_history[i]
        msg = ConstructMessage(current_msg_json.FROM_USER, current_msg_json.DATE_SENT, current_msg_json.MESSAGE_ID, current_msg_json.PAYLOAD, current_msg_json.NUM_UPVOTES);
        AppendMessage(msg)
    }
    alert(message_history.length)
}


$(document).ready(function(){
    $('#message_input_form').submit(function(e){e.preventDefault(); ClientRequestSendMessage();});
    $('#leave-session').click(ClientRequestLeave);
    $('#most-popular').click(function(){SortMessages(SortByAscendingUpvotesPredicate)})
    $('#least-popular').click(function(){SortMessages(SortByDescendingUpvotesPredicate)})
    $('#newest').click(function(){alert("IMPL_SORT_BY_NEWEST");})
    $('#oldest').click(function(){alert("IMPL_SORT_BY_OLDEST");})

    

    socket.on('ACK_VOTE_CHANGE', function(data){ClientAcknowledgeVoteChange(data);});
    socket.on('ACK_SEND_MESSAGE', ClientAcknowledgeSendMessage);
    socket.on('connect', ClientRequestJoin)
    socket.on('ACK_JOIN', function(data){ClientAcknowledgeJoin(data)});
    socket.on('ACK_LEAVE', ClientAcknowledgeLeave);
    socket.on('ACK_MESSAGE_CACHE_UPDATE', function(data){ClientAcknowledgeMessageHistoryCache(data);});


    
    window.onbeforeunload = ClientRequestLeave;
})





















