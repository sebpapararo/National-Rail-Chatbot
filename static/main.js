// Counter to store the number messages in the current conversation (0 will be the first message)
var chatCounter = 0;

// Function that updates the chat history when the user submits input
function updateChatHistory() {
    // If the input is not empty
    if (document.getElementById("inputBox").value != "") {
        sessionStorage.setItem(chatCounter, document.getElementById("inputBox").value);
        chatCounter++;
        displayChatHistory();
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
        newInput.appendChild(document.createTextNode(sessionStorage.getItem(sessionStorage.key(i))));
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