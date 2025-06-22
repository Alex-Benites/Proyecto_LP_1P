<?php

// Algoritmo de Cola (FIFO) con Funciones
// Contribuidor: NLindao2004

// Variables globales de la cola
$cola = [];
$frente = 0;
$final = 0;
$contador = 0;
define("TAMAÑO_MAXIMO", 5);

// Función para encolar (ENQUEUE)
function encolar($elemento) {
    $cola[] = $elemento;
    $final = $final + 1;
    $contador = $contador + 1;
}

// Función para desencolar (DEQUEUE)
function desencolar() {
    $elementoRemovido = $cola[$frente];
    $frente = $frente + 1;
    $contador = $contador - 1;
    return $elementoRemovido;
}

// Función para verificar si está vacía
function estaVacia() {
    if ($contador == 0) {
        return 1;
    }
    return 0;
}

// Usar las funciones
encolar(10);
encolar(20);
encolar(30);

echo "Elementos en cola: ";
echo $contador;

$removido = desencolar();
echo "Elemento removido: ";
echo $removido;

$vacia = estaVacia();
echo "Cola vacia: ";
echo $vacia;
?>