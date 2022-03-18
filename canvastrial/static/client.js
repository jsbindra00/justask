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
    socket.emit( 'clientmsg', {
      user_name : user_name,
      message : user_input,
      canvas: $('#can')});

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
    if($('#updatecanvas').checked)
    {
        console.log("updating canvas");
        $('#can') = msg.canvas;
    }
}

socket.on( 'servermsg', OnServerMessage);