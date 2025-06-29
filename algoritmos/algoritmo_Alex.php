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

// ✅ PRUEBAS SEMÁNTICAS DE ALEX: División por cero
echo "\n=== PRUEBAS DE VALIDACIÓN SEMÁNTICA ===\n";

// Casos que DEBEN generar error semántico:
echo "Realizando operaciones matemáticas...\n";
$clientes_total = 10;
$divisor_cero = 0;

// División directa por cero
$promedio1 = 100 / 0;        // Error semántico esperado

// División con variable cero
$promedio2 = $clientes_total / 0;  // Error semántico esperado

// División con decimal cero
$promedio3 = 50 / 0.0;       // Error semántico esperado

// Casos VÁLIDOS (no deben generar error):
$promedio_valido = $clientes_total / 2;  // Válido
$tiempo_atencion = 60 / count($cola);    // Válido si $cola no está vacía

echo "Promedio de atención por cliente: " . $promedio_valido . " minutos\n";
?>