// This function will be called by Python to display the user's spoken query
eel.expose(senderText);
function senderText(query) {
    // Hide the idle ring screen and show the Siri wave screen
    $("#Oval").attr("hidden", true);
    $("#SiriWave").attr("hidden", false);

    // Display the user's query
    $("#user-query").text(query).show();
    // Clear any previous Jarvis response
    $(".siri-message").text("");
}

// This function will be called by Python to display Jarvis's response
eel.expose(receiverText);
function receiverText(message) {
    // Use Textillate to animate Jarvis's response
    $(".siri-message").text(message).textillate('start');

    // After 5 seconds, hide the Siri wave and go back to the idle ring screen
    setTimeout(() => {
        $("#SiriWave").attr("hidden", true);
        $("#Oval").attr("hidden", false);
        // Clear the text for the next interaction
        $("#user-query").text("");
        $(".siri-message").text("");
    }, 5000);
}