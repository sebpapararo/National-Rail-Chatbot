function userUpdateChat(input) {
    var chatDiv = document.getElementById("chatHistory");
    var newInput = document.createElement("p");
    newInput.appendChild(document.createTextNode('You: ' + input.value));
    chatDiv.appendChild(newInput);
    document.getElementById("inputBox").value = "";
}