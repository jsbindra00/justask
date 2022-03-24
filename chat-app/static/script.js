SESSION_ID_STRING_LENGTH = 10;




console.log("Exceuting js");
function GenerateSessionID(lengthofID) {
    let result = '';
    var selection = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789';
    var selectionSize = selection.length;
    for ( var i = 0; i < lengthofID; i++ ) {
      result += selection.charAt(Math.floor(Math.random() * selectionSize));
   }
   return result;
}

$(document).ready(function(){

    console.log("Initialising page.");

    // grab all sidebar elements, and add an onclick event for each.

    testingh1 = $('#testing');

    sessionIDString = GenerateSessionID(SESSION_ID_STRING_LENGTH);
    testingh1.text(sessionIDString);



})










