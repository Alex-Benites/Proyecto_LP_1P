<?php
// Algoritmo que simula el comportamiento de una cola en PHP
$cola = [];

// Mostramos estado inicial
echo "Estado inicial de la cola:\n";
print_r($cola);
$cola[] = "Cliente 1";
$cola[] = "Cliente 2";
$cola[] = "Cliente 3";

echo "\nEstado de la cola después de hacer ENQUEUE:\n";
print_r($cola);

$clienteAtendido = array_shift($cola);

echo "\nCliente atendido (DEQUEUE): " . $clienteAtendido . "\n";
echo "Estado de la cola después del DEQUEUE:\n";
print_r($cola);

if (empty($cola)) {
    echo "\nLa cola está vacía.\n";
} else {
    echo "\nQuedan " . count($cola) . " clientes en la cola.\n";
}

$siguienteCliente = $cola[0];

echo "\nEl siguiente cliente en la cola es: " . $siguienteCliente . "\n";

//Pruebas semanticas de Alex: División por cero
echo "\n=== PRUEBAS DE VALIDACIÓN SEMÁNTICA ===\n";

// Casos que me deberiann generar error semántico:
echo "Realizando operaciones matemáticas...\n";
$clientes_total = 10;
$divisor_cero = 0;

// División directa por cero
$promedio1 = 100 / 0;

// División con variable cero
$promedio2 = $clientes_total / 0;

// División con decimal cero
$promedio3 = 50 / 0.0;

// Casos validos que no deben generar error:
$promedio_valido = $clientes_total / 2;
$tiempo_atencion = 60 / count($cola);

echo "Promedio de atención por cliente: " . $promedio_valido . " minutos\n";

// Segunda regla semantica de ALex: Validación de acceso a arrays
echo "\n=== PRUEBAS DE ACCESO A ARRAYS ===\n";

// Casos que si me van a generar error en el analisis semántico:
$indice_negativo = 0 - 1;
$error1 = $cola[$indice_negativo];

$indice_negativo2 = 0 - 5;
$error2 = $cola[$indice_negativo2];

$error3 = $cola["texto"];
// Casos validos que no deben generar error:
$valido1 = $cola[0];
$valido2 = $cola[1];
$valido3 = $cola[2];

echo "Acceso válido completado\n";
?>
