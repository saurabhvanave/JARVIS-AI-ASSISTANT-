$(document).ready(function () {
    // Initialize Eel with error handling
    try {
        eel.init();
        console.log("Eel initialized successfully");
    } catch (e) {
        console.error("Eel initialization failed:", e);
    }
    
    
});
   
   $('.text').textillate({
    loop:true,
    sync:true,
    in:{
        effect:"bounceIn",
    },
    out:{
        effect:"bounceOut",
    },

   });
   //siri configuration
   var siriWave = new SiriWave({
    container: document.getElementById("siri-container"),
    width: 800,
    height: 200,
    style: "ios9",
     amplitude: "1",
     speed: "0.30",
    autostart: true,

  });
  
  //siri msg animate
  $('.siri-message').textillate({
    loop:true,
    sync:true,
    in:{
        effect:"fadeInUp",
        sync:true,
    },
    out:{
        effect:"fadeOutUp",
        sync:true,
    },

   });

    // ✅ Setting button
    $("#SettingBtn").on("click", function () {
        $("#settingsPanel").toggle("fast");
        eel.openSettings();
    });


   //mic btn click
   $("#MicBtn").click(function () { 

    eel.playAssistantSound()
    $("#Oval").attr("hidden", true);
    $("#SiriWave").attr("hidden", false);
    eel.allCommands()()
   });


   




   function doc_keyUp(e) {
    // this would test for whichever key is 40 (down arrow) and the ctrl key at the same time

    if (e.key === 'j' && e.metaKey) {
        eel.playAssistantSound()
        $("#Oval").attr("hidden", true);
        $("#SiriWave").attr("hidden", false);
        eel.allCommands()()
    }
}
    document.addEventListener('keyup', doc_keyUp, false);

      // to play assisatnt 
      function PlayAssistant(message) {

        if (message != "") {

            $("#Oval").attr("hidden", true);
            $("#SiriWave").attr("hidden", false);
            eel.allCommands(message);
            $("#chatbox").val("")
            $("#MicBtn").attr('hidden', false);
            $("#SendBtn").attr('hidden', true);

        }

    }
    function ShowHideButton(message) {
        if (message.length == 0) {
            $("#MicBtn").attr('hidden', false);
            $("#SendBtn").attr('hidden', true);
        }
        else {
            $("#MicBtn").attr('hidden', true);
            $("#SendBtn").attr('hidden', false);
        }
    }

    $("#chatbox").keyup(function () {

        let message = $("#chatbox").val();
        ShowHideButton(message)
    
    });
    
    // send button event handler
    $("#SendBtn").click(function () {
    
        let message = $("#chatbox").val()
        PlayAssistant(message)
    
    });
    
    $("#chatbox").keypress(function (e) {
        key = e.which;
        if (key == 13) {
            let message = $("#chatbox").val()
            PlayAssistant(message)
        }
    });






    function saveSettings() {
    const voiceId = parseInt($("#voiceSelect").val());
    const rate = parseInt($("#speechRate").val());

    eel.saveSettings(voiceId, rate);
    alert("✅ Settings saved!");

    // 👇 Auto-close the settings panel
    document.getElementById("settingsPanel").style.display = "none";
}
