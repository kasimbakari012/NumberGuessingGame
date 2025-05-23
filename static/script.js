document.addEventListener("DOMContentLoaded", function() {
    const guessInput = document.getElementById("guessInput");
    const message = document.getElementById("message");

    guessInput.addEventListener("input", function() {
        guessInput.style.borderColor = "black";  // Reset border color when typing
    });

    if (message.innerText.trim() !== "") {
        message.style.color = "green";  // Change color when correct
        message.classList.add("bounce");
    }
});
