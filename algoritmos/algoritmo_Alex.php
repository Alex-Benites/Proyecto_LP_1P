<?php
// Algoritmo que simula el comportamiento de una cola en PHP

// Creamos la cola como un arreglo vacío
$cola = [];

// Mostramos estado inicial
echo "Estado inicial de la cola:\n";
print_r($cola);

// Agregamos elementos a la cola (ENQUEUE - al final)
$cola[] = "Cliente 1";
$cola[] = "Cliente 2";
$cola[] = "Cliente 3";

echo "\nEstado de la cola después de hacer ENQUEUE:\n";
print_r($cola);

// Atendemos al primer cliente (DEQUEUE - al inicio)
$clienteAtendido = array_shift($cola);

echo "\nCliente atendido (DEQUEUE): " . $clienteAtendido . "\n";
echo "Estado de la cola después del DEQUEUE:\n";
print_r($cola);

// Verificamos si la cola está vacía
if (empty($cola)) {
    echo "\nLa cola está vacía.\n";
} else {
    echo "\nQuedan " . count($cola) . " clientes en la cola.\n";
}

// Accedemos al siguiente cliente sin retirarlo
$siguienteCliente = $cola[0]; // Primer elemento de la cola

echo "\nEl siguiente cliente en la cola es: " . $siguienteCliente . "\n";
?>