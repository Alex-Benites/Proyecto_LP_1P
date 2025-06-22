<?php

// Algoritmo de Cola (FIFO - First In, First Out)
// Contribuidor: NLindao2004

// Definir tamaño máximo de la cola
define("TAMAÑO_MAXIMO", 5);

// Declarar la cola como array vacío
$cola = [];

// Variables para control de la cola
$frente = 0;
$final = 0;
$contador = 0;

// Agregar elementos a la cola (ENQUEUE)
$elemento1 = 10;
$cola[] = $elemento1;
$final = $final + 1;
$contador = $contador + 1;

$elemento2 = 20;
$cola[] = $elemento2;
$final = $final + 1;
$contador = $contador + 1;

$elemento3 = 30;
$cola[] = $elemento3;
$final = $final + 1;
$contador = $contador + 1;

// Mostrar estado de la cola
echo "Elementos en cola: ";
echo $contador;

echo "Frente: ";
echo $frente;

echo "Final: ";
echo $final;

// Remover elemento de la cola (DEQUEUE)
$elementoRemovido = $cola[$frente];
$frente = $frente + 1;
$contador = $contador - 1;

echo "Elemento removido: ";
echo $elementoRemovido;

// Mostrar nuevo estado
echo "Nuevo frente: ";
echo $frente;

echo "Elementos restantes: ";
echo $contador;

// Verificar si la cola está vacía
$estaVacia = 0;
if ($contador == 0) {
    $estaVacia = 1;
}

echo "Cola vacia: ";
echo $estaVacia;

// Verificar si la cola está llena
$estaLlena = 0;
if ($contador == 5) {
    $estaLlena = 1;
}

echo "Cola llena: ";
echo $estaLlena;
?>