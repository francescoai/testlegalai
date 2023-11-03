// script.js

const sendButton = document.getElementById("sendButton");
const userInput = document.getElementById("userInput");
const chatBox = document.querySelector(".chat-box");
const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;

sendButton.addEventListener("click", function() {
    const inputText = userInput.value;
    const userMessageElement = document.createElement("div");
    userMessageElement.textContent = `Tu: ${inputText}`;
    chatBox.appendChild(userMessageElement);

    fetch("/chatbot/", {
        method: "POST",
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrfToken,
        },
        body: JSON.stringify({ message: inputText })
    })
    .then(response => {
        if (!response.ok) {
            throw new Error(`Errore HTTP! Stato: ${response.status}`);
        }
        return response.json();
    })
    .then(data => {
        console.log("Risposta dal server:", data); // Logga l'intero oggetto risposta
        if (!data.message) {
            throw new Error('La risposta dal server non contiene il campo "message".');
        }
        const botMessageElement = document.createElement("div");
        botMessageElement.textContent = `Assistente: ${data.message}`;
        chatBox.appendChild(botMessageElement);
    })
    .catch(error => {
        console.error('Errore nel recuperare la risposta del chatbot:', error);
        const errorMessageElement = document.createElement("div");
        errorMessageElement.textContent = `Errore: ${error.message}`;
        chatBox.appendChild(errorMessageElement);
    });

    userInput.value = ""; // Svuota l'input dopo l'invio del messaggio
});
