$(document).ready(function () {
    // --- Get All UI Elements ---
    const startScreen = $("#Start");
    const ovalScreen = $("#Oval");
    const siriWaveScreen = $("#SiriWave");
    const micButton = $("#MicBtn");
    const userQueryText = $("#user-query-text");
    const jarvisResponseText = $("#jarvis-response-text");
    const statusText = $(".status-text");

    // --- Initialize Textillate for animated text ---
    $('.siri-message').textillate({
        loop: true,
        sync: true,
        in: { effect: "fadeInUp", sync: true },
        out: { effect: "fadeOutUp", sync: true },
    });

    // --- Initialize SiriWave ---
    var siriWave = new SiriWave({
        container: document.getElementById("siri-container"),
        width: 800,
        height: 200,
        style: "ios9",
        amplitude: 1,
        speed: 0.30,
        autostart: false
    });

    // --- Initial Loading Sequence ---
    setTimeout(() => {
        startScreen.fadeOut(500, () => {
            startScreen.attr("hidden", true);
            ovalScreen.attr("hidden", false).addClass("animate__animated animate__zoomIn");
            
            // Start the particle animation only after its container is visible
            if (typeof canvasApp === 'function') {
                canvasApp();
            }
        });
    }, 4000); // Show loading screen for 4 seconds

    // --- Mic Button Click Handler ---
    micButton.click(() => {
        ovalScreen.attr("hidden", true);
        siriWaveScreen.attr("hidden", false);
        siriWave.start();
        eel.start_interaction()(); // Use the function name from our stable backend
    });

    // --- Functions Exposed to Python ---

    // Updates the main status text (e.g., "Listening...")
    eel.expose(update_status);
    function update_status(status) {
        // This function can be expanded to show status on the SiriWave screen if needed
        console.log("Status from Python: " + status);
        if (status === "Ready" || status === "Sleeping") {
            // After a command, return to the idle screen
            setTimeout(() => {
                siriWaveScreen.attr("hidden", true);
                ovalScreen.attr("hidden", false);
                siriWave.stop();
            }, 2000); // Wait 2 seconds before returning
        }
    }

    // Displays the query spoken by the user
    eel.expose(update_user_query);
    function update_user_query(text) {
        userQueryText.text(text);
    }

    // Displays the response spoken by Jarvis
    eel.expose(update_jarvis_response);
    function update_jarvis_response(text) {
        // Use Textillate to animate the response
        jarvisResponseText.text(text).textillate('start');
    }
});