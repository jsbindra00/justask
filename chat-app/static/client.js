 

// we have a class which stores the messages.
// messages have flairs associated with them. 
// we render the messages how we want with external js.



// client upvotes message.
    // do we want upvotes to be stored? yes. they must be global.
        // we need a message class on server side.
            // store each message.
    // client wishes to sort messages.
    // external js sorting function which rearranges elements in the chat wrapper.







const socket = io.connect("http://127.0.0.1:5000");



function OnMessageVote(message_id, vote_amount){
    if (vote_amount < 0){
        alert("downvote")
    }
    else alert("upvote");
    socket.emit('on_message_vote', {message_id : message_id, vote_amount: vote_amount});
}
socket.on('connect', function () {
    socket.emit('join_room', {
        username: "{{ username }}",
        room: "{{ room }}"
    });

    let message_input = document.getElementById('chatbar');

    document.getElementById('message_input_form').onsubmit = function (e) {
        e.preventDefault();
        let message = message_input.value.trim();
        if (message.length) {
            socket.emit('send_message', {
                message: message
            })
        }
        message_input.value = '';
        message_input.focus();

    }
});

window.onbeforeunload = function () {
    socket.emit('leave_room', {
        room: "{{ room }}"
    })
};

socket.on('receive_message', function (data) {
    console.log(data);

    const messageNode = $('<div/>',
     {
         "class" : "message-wrapper " + ((data.username == $('#username-metadata').attr("username"))? "native" : "foreign"),
         "id" : data.message_id
        });

    const messageHeader = $('<div/>',
    {
        "class" : "message-header"
    }).append(`<p>${data.username}</p><p>at</p><p>${data.time}</p>`);

    const messagePayload = $('<div/>',
    {
        "class" : "message-payload"
    }).append(`<p>${data.message}</p>`);

    



    const upvoteMessage = $('<div/>', {
        "class" : "upvote-message",
        "click" : function(){OnMessageVote(data, 1)}
    }).append(`<i class="fa-solid fa-up fa-lg"></i>`)
    const downvoteMessage = $('<div/>', {
        "class" : "downvote-message",
        "click" : function(){OnMessageVote(data, -1)}
    }).append(`<i class="fa-solid fa-down fa-lg"></i>`)


    const messageProperties = $('<div/>',
    {
        "class" : "message-properties"
    }).append(`<div class="message-flairs">`).append(upvoteMessage).append(downvoteMessage);


    messageNode.append(messageHeader);
    messageNode.append(messagePayload);
    messageNode.append(messageProperties)
    // messageNode.append(messageProperties);

    // messageNode.click(function(){alert("hello world");});

    // messageNode.get(0).children[0].onclick = function(){OnMessageVote(data.message_id, )}};
    // messageNode.get(0).children[1].onclick = function(){alert("header");};

    // messageNode.get(0)click(function(){alert("header");});
    // messageNode.get(0).click(function(){alert("payload");});


    $('#messages').append(messageNode);

 
    // document.getElementById('messages').appendChild(newNode);

    // keep the scroll at the bottom.
    var messageBody = document.querySelector('#messages');
    messageBody.scrollTop = messageBody.scrollHeight - messageBody.clientHeight;
});

socket.on('join_room_announcement', function (data) {
    console.log(data);
    if (data.username !== "{{username}}") {
        const newNode = document.createElement('div');
        newNode.innerHTML = `<b>${data.time} ${data.username} has joined the room</b>`;
        document.getElementById('messages').appendChild(newNode);
    }
});

socket.on('leave_room_announcement', function (data) {
    console.log(data);
    const newNode = document.createElement('div');
    newNode.innerHTML = `<b>${data.username}</b> has left the room`;
    document.getElementById('messages').appendChild(newNode);
});


function openForm() {
document.getElementById("myForm").style.display = "block";
}

function closeForm() {
document.getElementById("myForm").style.display = "none";
}





function RequestSessionMessages(){
    // we can't store the flair in the raw html.

    // client sends message.
        // message contains header and payload.
            // header consists of flairs, upvotes, date sent.
}





$(document).ready(function(){



})