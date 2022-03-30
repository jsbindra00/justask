 

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
                message: message,
                m_session_id: "m_sessionid"
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

    const newNode = document.createElement('div');

    let owned_message = ((data.username == $('#username-metadata').attr("username"))? "native" : "foreign")
    newNode.className = 'message-wrapper ' + owned_message;


    console.log(data.username);

    let newMessage = `
    <div class="message-header">
        <p>${data.username}</p>
        <p>at</p>
        <p>${data.time}</p>
    </div>
    <div class="message-payload">
        <p>${data.message}</p>
    </div>

    `

    newNode.innerHTML = newMessage;

 
    document.getElementById('messages').appendChild(newNode);

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



function GenerateMessageID(){
    // returns a unique message id for a given message.

    let current_date = Date();
    console.log(current_date)
}




$(document).ready(function(){





    // socket.on('connect', function () {
    //     socket.emit('join_room', {
    //         username: "{{ username }}",
    //         room: "{{ room }}"
    //     });
    
    //     let message_input = document.getElementById('chatbar');
    
    //     document.getElementById('message_input_form').onsubmit = function (e) {
    //         e.preventDefault();
    //         let message = message_input.value.trim();
    //         if (message.length) {
    //             socket.emit('send_message', {
    //                 message: message
    //             })
    //         }
    //         message_input.value = '';
    //         message_input.focus();
    
    //     }
    // });
    // apply a sort to the chat.

    // request the messages for this session from socket io server.
})