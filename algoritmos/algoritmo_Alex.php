<?php
// Algoritmo simplificado de Alex - Solo 3 reglas sintácticas y 3 semánticas
// Contribución de: Alex Benites

echo "=== SIMULACIÓN DE PILA (STACK) SIMPLIFICADA ===\n";

// Inicializar pila vacía
$pila = [];
$pila_tamano = 0; // Simular tamaño para underflow

echo "Estado inicial de la pila:\n";
print_r($pila);

// === PRUEBA REGLA SINTÁCTICA 1: Operaciones de pila ===
echo "\n=== OPERACIONES PUSH (APILAR) ===\n";
array_push($pila, "Documento A");
array_push($pila, "Documento B");

echo "\n=== OPERACIONES POP (DESAPILAR) ===\n";
$documento_removido = array_pop($pila);
echo "Documento removido: " . $documento_removido . "\n";

// === PRUEBA REGLA SEMÁNTICA 1: División por cero ===
echo "\n=== PRUEBA DIVISIÓN POR CERO ===\n";
$resultado1 = 100 / 0;          // ❌ Error semántico
$resultado2 = 50 / 0.0;         // ❌ Error semántico

// === PRUEBA REGLA SEMÁNTICA 2: Acceso seguro a arrays ===
echo "\n=== PRUEBA ACCESO SEGURO A ARRAYS ===\n";
$indice_negativo = 0 - 1;       // Índice negativo
$error1 = $pila[$indice_negativo];    // ❌ Error semántico (índice negativo)
$error2 = $pila["Texto"];             // ❌ Error semántico (string en array simple)

// === PRUEBA REGLA SEMÁNTICA 3: Underflow de pila ===
echo "\n=== PRUEBA UNDERFLOW DE PILA ===\n";
// Simular pila vacía
$pila_tamano = 0;
array_pop($pila); // ❌ Error semántico (underflow)

echo "Estado final de la pila:\n";
print_r($pila);
echo "\n=== ANÁLISIS COMPLETADO ===\n";
?>
