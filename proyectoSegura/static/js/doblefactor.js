function siguienteInput(inputActual) {
    const inputs = document.querySelectorAll("input[type='text']");
    const indiceActual = Array.from(inputs).indexOf(inputActual);
    const siguienteIndice = (indiceActual + 1) % inputs.length;
    inputs[siguienteIndice].focus();
}