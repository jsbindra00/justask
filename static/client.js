// // Render the web socket for this client.
// var socket = io.connect('http://' + document.domain + ':' + location.port);
// function OnSocketConnect()
// {
//     socket.emit( 'clientmsg', {data: 'User Connected'} );
// }

// function OnFormSubmit(OnFormSubmitEvent)
// {
//     OnFormSubmitEvent.preventDefault();
//     let user_name = $( 'input.username' ).val();
//     let user_input = $( 'input.message' ).val();
//     let canvas = $('#can').get(0)
//     let context = canvas.getContext('2d');

//     var canvasContents = canvas.toDataURL();
//     var data = JSON.stringify(canvasContents);


//     socket.emit( 'clientmsg', {
//       user_name : user_name,
//       message : user_input,
//       canvasData: data});

//     $( 'input.message' ).val( '' ).focus();
    
// }
// var form = $( 'form' ).on( 'submit',OnFormSubmit);

// socket.on( 'connect', OnSocketConnect);




// function OnServerMessage(msg)
// {
//     console.log( msg )

//     // if($('#updatecanvas').get(0).checked)
//     // {   

//         if(msg.hasOwnProperty('canvasData'))
//         {
//             console.log("updating canvas");
//             var canvas = $('#can').get(0);
//             var ctx = canvas.getContext('2d');
    
//             var data = JSON.parse(msg.canvasData);
//             var image = new Image();
//             image.src = data;

//             image.onload = function(){

//                 ctx.clearRect(0, 0, canvas.width, canvas.height);
//                 ctx.drawImage(image, 0, 0);
//             }

//             console.log("set context")
//             $('#can').replaceWith(canvas);

//         }

     
//   //  }
// }

// socket.on( 'servermsg', OnServerMessage);

const socket = io.connect("http://127.0.0.1:5000");

socket.on('connect', function () {
    socket.emit('join_room', {
        username: "{{ username }}",
        room: "{{ room }}"
    });

    let message_input = document.getElementById('message_input');

    document.getElementById('message_input_form').onsubmit = function (e) {
        e.preventDefault();
        let message = message_input.value.trim();
        let description = message_description.value.trim();
        if (message.length) {
            socket.emit('send_message', {
                username: "{{ username }}",
                room: "{{ room }}",
                message: message,
                description: description,
            })
        }
        message_input.value = '';
        message_input.focus();
        message_description.value = '';
        message_description.focus();
    }
});

window.onbeforeunload = function () {
    socket.emit('leave_room', {
        username: "{{ username }}",
        room: "{{ room }}"
    })
};

socket.on('receive_message', function (data) {
    console.log(data);
    const newNode = document.createElement('div');
    newNode.className = 'card';
    newNode.innerHTML = `${data.time} <b>${data.username}</b> </br> <div class= 'message'> <b><h4>${data.message}</h4></b>${data.description} </div>`;
    document.getElementById('messages').appendChild(newNode);
});

socket.on('join_room_announcement', function (data) {
    console.log(data);
    if (data.username !== "{{ username }}") {
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
function openForm() {
document.getElementById("myForm").style.display = "block";
}

function closeForm() {
document.getElementById("myForm").style.display = "none";
}