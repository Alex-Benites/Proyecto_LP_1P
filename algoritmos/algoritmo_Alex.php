<?php
// Algoritmo que simula el comportamiento de una PILA (Stack) en PHP
// Contribución de: Alex Benites

echo "=== SIMULACIÓN DE PILA (STACK) EN PHP ===\n";

// Inicializar pila vacía
$pila = [];
$tamano_maximo = 5;

echo "Estado inicial de la pila:\n";
print_r($pila);

// === OPERACIONES DE PILA ===
echo "\n=== OPERACIONES PUSH (APILAR) ===\n";

// Push: Agregar elementos al tope de la pila
array_push($pila, "Documento A");
array_push($pila, "Documento B");
array_push($pila, "Documento C");
array_push($pila, "Documento D");

echo "Estado de la pila después de agregar elementos:\n";
print_r($pila);

echo "\n=== OPERACIONES POP (DESAPILAR) ===\n";

// Pop: Remover elementos del tope de la pila
$documento_removido = array_pop($pila);
echo "Documento removido: " . $documento_removido . "\n";

$documento_removido2 = array_pop($pila);
echo "Documento removido: " . $documento_removido2 . "\n";

echo "Estado de la pila después de remover elementos:\n";
print_r($pila);

echo "\n=== OPERACIONES ADICIONALES ===\n";

// Peek: Ver el elemento del tope sin removerlo
$tamano_actual = count($pila);
if ($tamano_actual > 0) {
    $tope = $pila[$tamano_actual - 1];
    echo "Elemento en el tope: " . $tope . "\n";
} else {
    echo "La pila está vacía\n";
}

// Verificar tamaño
echo "La pila tiene " . count($pila) . " elementos\n";

// === PRUEBAS SEMÁNTICAS DE ALEX ===
echo "\n=== PRUEBAS DE VALIDACIÓN SEMÁNTICA ===\n";

// Primera regla semántica: División por cero
echo "Realizando operaciones matemáticas...\n";
$documentos_total = 10;
$divisor_cero = 0;

// Casos que DEBEN generar error semántico:
$promedio1 = 100 / 0;                    // División directa por cero
$promedio2 = $documentos_total / 0;      // División con variable cero
$promedio3 = 50 / 0.0;                   // División por cero decimal

echo "Promedio de procesamiento calculado\n";

// Segunda regla semántica: Acceso a arrays con índices problemáticos
echo "\n=== PRUEBAS DE ACCESO A ARRAYS ===\n";

// Casos que DEBEN generar error semántico:
$indice_negativo = 0 - 1;
$error1 = $pila[$indice_negativo];       // Índice negativo via variable

$indice_negativo2 = 0 - 5;
$error2 = $pila[$indice_negativo2];      // Índice negativo mayor

$error3 = $pila["texto"];                // Índice string en array simple

// Casos válidos (no deben generar error):
$valido1 = $pila[0];                     // Índice válido
$valido2 = $pila[1];                     // Índice válido

echo "Acceso a elementos completado\n";

// === DEMOSTRACIÓN FINAL DE PILA ===
echo "\n=== DEMOSTRACIÓN FINAL ===\n";

// Agregar más elementos para mostrar el comportamiento
array_push($pila, "Último Documento");
echo "Agregado elemento final a la pila\n";

echo "Estado final de la pila:\n";
print_r($pila);

echo "Tamaño final de la pila: " . count($pila) . " elementos\n";
echo "\n=== ANÁLISIS DE PILA COMPLETADO ===\n";
?>
