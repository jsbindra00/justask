

const socket = io.connect("http://127.0.0.1:5000");


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
        newNode.innerHTML = `<b>${data.time} ${data.username} has joined the room</b>`;
        document.getElementById('messages').appendChild(newNode);
    }
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

function ClientAcknowledgeSendMessage(data){


    const messageNodeWrapper = $('<div/>', {
        "class" : "message-wrapper-master",
        "id" : data.message_id
    })


    // MESSAGE NODE
    const messageNode = $('<div/>',
     {
         "class" : "message-wrapper " + ((data.username == $('#username-metadata').attr("username"))? "native" : "foreign"),
        });
    

    const messageHeader = $('<div/>',
    {
        "class" : "message-header"
    }).append(`<p>${data.username}</p><p>at</p><p>${data.time}</p>`);

    const messagePayload = $('<div/>',
    {
        "class" : "message-payload"
    }).append(`<p>${data.message}</p>`);


    // VOTING

    const votingProperty = $('<div/>', {
        "class" : "message-property message-voting"
    });
    const votingIcons = $('<ul/>', {
        "class" : "voting-icons"
    });

    

    const upvoteMessage = $('<div/>', {
        "class" : "message-vote upvote-message",
        "click" : function(){ClientRequestVoteChange(data.message_id, 1, data.session_id)}
    }).append(`<i class="fa-solid fa-caret-up fa-lg"></i>`)
    const downvoteMessage = $('<div/>', {
        "class" : "message-vote downvote-message",
        "click" : function(){ClientRequestVoteChange(data.message_id, -1, data.session_id)}
    }).append(`<i class="fa-solid fa-caret-down fa-lg"></i>`)

    votingIcons.append(upvoteMessage).append(downvoteMessage);
    

    const voteCountWrapper = $('<div/>',{
        "class":"message-vote-count-wrapper"
    }).append(`<p class="message-vote-count">0</p>`);

    votingProperty.append(votingIcons);
    votingProperty.append(voteCountWrapper);


    messageNode.append(messageHeader);
    messageNode.append(messagePayload);
    messageNodeWrapper.append(messageNode);
    messageNodeWrapper.append(votingProperty)


    $('#messages').append(messageNodeWrapper);


    var messageBody = document.querySelector('#messages');
    messageBody.scrollTop = messageBody.scrollHeight - messageBody.clientHeight;
}



function ClientRequestLeave(){
    socket.emit('REQ_LEAVE', {
        room: "{{ room }}"
    })
}

function ClientAcknowledgeLeave(data){
    const newNode = document.createElement('div');
    newNode.innerHTML = `<b>${data.username}</b> has left the room`;
    document.getElementById('messages').appendChild(newNode);
}





function SortMessages(){

    function SortByDate(message_a, message_b){

    }
    function SortByUpvotes(message_a, message_b){
        let message_a_upvotes = parseInt(message_a.querySelector(".message-vote-count").innerText)
        let message_b_upvotes = parseInt(message_b.querySelector(".message-vote-count").innerText)

        return (message_a_upvotes > message_b_upvotes) ? 1 : -1;
    }
    function SortByAscendingUpvotes(message_a, message_b){
        return SortByUpvotes(message_a, message_b)
    }
    function SortByDescendingUpvotes(message_a, message_b){
        return SortByUpvotes(message_a, message_b) * -1;
    }


    var toSort = document.getElementsByClassName('message-wrapper-master')
    toSort = Array.prototype.slice.call(toSort, 0);

    toSort.sort(SortByAscendingUpvotes)

    var parent = document.getElementById('messages')
    parent.innerHTML = "";

    for(var i = 0, l = toSort.length; i < l; i++) {
        parent.appendChild(toSort[i]);
    }
}

$(document).ready(function(){
    $('#message_input_form').submit(function(e){e.preventDefault(); ClientRequestSendMessage();});
    $('#leave-session').click(ClientRequestLeave);
    $('#sort-chat').click(SortMessages);

    socket.on('ACK_VOTE_CHANGE', function(data){ClientAcknowledgeVoteChange(data);});
    socket.on('ACK_SEND_MESSAGE', ClientAcknowledgeSendMessage);
    socket.on('connect', ClientRequestJoin)
    socket.on('ACK_JOIN', function(data){ClientAcknowledgeJoin(data)});
    socket.on('ACK_LEAVE', ClientAcknowledgeLeave);

    
    window.onbeforeunload = ClientRequestLeave;
})





















