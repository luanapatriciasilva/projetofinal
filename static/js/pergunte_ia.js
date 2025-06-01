document.addEventListener("DOMContentLoaded", function () {
    const textarea = document.getElementById("user_input");
    const form = textarea.closest("form"); // Encontra o formulário pai do textarea

    textarea.addEventListener("keydown", function (event) {
        // Verifica se a tecla Enter foi pressionada E Shift NÃO foi pressionada
        if (event.key === "Enter" && !event.shiftKey) {
            event.preventDefault(); // Impede a quebra de linha padrão no textarea
            form.submit(); // Envia o formulário
        }
    });
});