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
      canvas: "hello world"});

    $( 'input.message' ).val( '' ).focus();
    
}
var form = $( 'form' ).on( 'submit',OnFormSubmit);

socket.on( 'connect', OnSocketConnect);


      socket.on( 'servermsg', function( msg ) {
        console.log( msg )
        if( typeof msg.user_name !== 'undefined' ) {
          $( 'h3' ).remove()
          $( 'div.message_holder' ).append( '<div><b style="color: #000">'+msg.user_name+'</b> '+msg.message+'</div>' )
        }
      })
