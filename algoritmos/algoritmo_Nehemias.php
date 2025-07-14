<?php
// PRUEBA 1: UNDERFLOW DE COLA
echo "\n=== PRUEBA UNDERFLOW DE COLA ===\n";
$contador = 0;  // Simular cola completamente vacía
desencolar();   // ❌ Error semántico: underflow
echo "Intentó desencolar de cola vacía\n";
?>