// Things that need to be done on the page load
function onload() {
    var sessionStorage_transfer = function(event) {
      if(!event) { event = window.event; } // ie suq
      if(!event.newValue) return;          // do nothing if no value to work with
      if (event.key == 'getSessionStorage') {
        // another tab asked for the sessionStorage -> send it
        localStorage.setItem('sessionStorage', JSON.stringify(sessionStorage));
        // the other tab should now have it, so we're done with it.
        localStorage.removeItem('sessionStorage'); // <- could do short timeout as well.
      } else if (event.key == 'sessionStorage' && !sessionStorage.length) {
        // another tab sent data <- get it
        var data = JSON.parse(event.newValue);
        for (var key in data) {
          sessionStorage.setItem(key, data[key]);
        }
      }
    };
    // listen for changes to localStorage
    if(window.addEventListener) {
      window.addEventListener("storage", sessionStorage_transfer, false);
    } else {
      window.attachEvent("onstorage", sessionStorage_transfer);
    };
    // Ask other tabs for session storage (this is ONLY to trigger event)
    if (!sessionStorage.length) {
      localStorage.setItem('getSessionStorage', 'foobar');
      localStorage.removeItem('getSessionStorage', 'foobar');
    };
    if (sessionStorage.length) {
      localStorage.setItem('getSessionStorage', 'foobar');
      localStorage.removeItem('getSessionStorage', 'foobar');
    };
    displayChatHistory();
}


// Counter to store the number messages in the current conversation (0 will be the first message)
var chatCounter = sessionStorage.length;

// Function that updates the chat history when the user submits input
function updateChatHistory() {
    // If the input is not empty
    if (document.getElementById("inputBox").value != "") {
        sessionStorage.setItem(chatCounter, document.getElementById("inputBox").value);
        chatCounter++;
        clearInputBox();
        displayChatHistory();
        resetScrollBar();
    } else {
        alert("The input box cannot be empty!");
    }
}

// Function that displays the chat history for the current session
function displayChatHistory() {
    document.getElementById("chatHistory").innerHTML = "";
    var chatDiv = document.getElementById("chatHistory");
    for (var i = 0; i < sessionStorage.length; i++) {
        var newInput = document.createElement("p");
        var boldElem = document.createElement("b");
        // Is even so it is the bot
        if (i == 0 || i % 2 == 0) {
            boldElem.innerHTML = "Bot: ";
            newInput.appendChild(boldElem)
        }
        else {
            boldElem.innerHTML = "You: ";
            newInput.appendChild(boldElem)
        }
        newInput.innerHTML += urlify(sessionStorage.getItem(sessionStorage.key(i)));
        chatDiv.appendChild(newInput);
    }
}

// Function to clear the user input box after it has been submitted
function clearInputBox() {
    document.getElementById("inputBox").value = "";
}

// Function to set the chat history scroll bar to the bottom when input is submitted
function resetScrollBar() {
    var element = document.getElementById("chatHistory");
    element.scrollTop = element.scrollHeight;
}

// function to turn text into clickable links
function urlify(inputText) {
    var replacedText, replacePattern1, replacePattern2, replacePattern3;

    //URLs starting with http://, https://, or ftp://
    replacePattern1 = /(\b(https?|ftp):\/\/[-A-Z0-9+&@#\/%?=~_|!:,.;]*[-A-Z0-9+&@#\/%=~_|])/gim;
    replacedText = inputText.replace(replacePattern1, '<a href="$1" target="_blank">$1</a>');

    //URLs starting with "www." (without // before it, or it'd re-link the ones done above).
    replacePattern2 = /(^|[^\/])(www\.[\S]+(\b|$))/gim;
    replacedText = replacedText.replace(replacePattern2, '$1<a href="http://$2" target="_blank">$2</a>');

    //Change email addresses to mailto:: links.
    replacePattern3 = /(([a-zA-Z0-9\-\_\.])+@[a-zA-Z\_]+?(\.[a-zA-Z]{2,6})+)/gim;
    replacedText = replacedText.replace(replacePattern3, '<a href="mailto:$1">$1</a>');

    return replacedText;
}