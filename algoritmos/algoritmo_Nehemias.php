<?php
// Algoritmo para probar redefinición de función

function operacion($a, $b) {
    return $a + $b;
}


function operacion($x, $y) {
    return $x - $y;
}


function mostrarDatos($nombre, $edad) {
    echo "Nombre: $nombre, Edad: $edad";
}

// Llamada con menos argumentos
mostrarDatos("Alex");



echo "\n=== PRUEBA UNDERFLOW DE COLA ===\n";
$contador = 0;  // Simular cola completamente vacía
desencolar();   // Error semántico: underflow
echo "Intentó desencolar de cola vacía\n";



define("TAMAÑO_MAXIMO", 5);
echo "\n=== PRUEBA OVERFLOW DE COLA ===\n";
$contador = 5;  // Simular cola llena (TAMAÑO_MAXIMO = 5)
encolar(999);   // Error semántico: overflow
echo "Intentó encolar en cola llena\n";
echo "\n=== FIN DE PRUEBAS ===\n";


?>