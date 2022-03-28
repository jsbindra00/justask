 
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
                message: message
            })
            alert("sent");

            
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
    newNode.className = 'message-wrapper';

    console.log(data.username);


    let newMessage = `
    <div class="message-header">
        <p>${data.username}</p>
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
