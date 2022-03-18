// Render the web socket for this client.
var socket = io.connect('http://' + document.domain + ':' + location.port);
function OnSocketConnect()
{
    socket.emit( 'clientmsg', {data: 'User Connected'} );
}

function OnFormSubmit(OnFormSubmitEvent)
{
    OnFormSubmitEvent.preventDefault();
    let user_name = $( 'input.username' ).val();
    let user_input = $( 'input.message' ).val();
    let canvas = $('#can').get(0)
    let context = canvas.getContext('2d');

    var canvasContents = canvas.toDataURL();
    var data = JSON.stringify(canvasContents);


    socket.emit( 'clientmsg', {
      user_name : user_name,
      message : user_input,
      canvasData: data});

    $( 'input.message' ).val( '' ).focus();
    
}
var form = $( 'form' ).on( 'submit',OnFormSubmit);

socket.on( 'connect', OnSocketConnect);




function OnServerMessage(msg)
{
    console.log( msg )
    if( typeof msg.user_name !== 'undefined' ) {
        $( 'h3' ).remove()
        $( 'div.message_holder' ).append( '<div><b style="color: #000">'+msg.user_name+'</b> '+msg.message+'</div>' )
    }
    if($('#updatecanvas').get(0).checked)
    {   

        if(msg.hasOwnProperty('canvasData'))
        {
            console.log("updating canvas");
            var canvas = $('#can').get(0);
            var ctx = canvas.getContext('2d');
    
            var data = JSON.parse(msg.canvasData);
            var image = new Image();
            image.src = data;

            image.onload = function(){

                ctx.clearRect(0, 0, canvas.width, canvas.height);
                ctx.drawImage(image, 0, 0);
            }

            console.log("set context")
            $('#can').replaceWith(canvas);

        }

     
    }
}

socket.on( 'servermsg', OnServerMessage);