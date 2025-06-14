<?php
// Algoritmo de ejemplo - Alex con Arrays Asociativos

define("EDAD_MINIMA", 18);

// Declaración de un arreglo (nombre => edad)
$personas = [
    "Ana" => 23,
    "Luis" => 30,
    "Carla" => 17,
    "Pedro" => 25,
    "Laura" => 40
];

// Variables para almacenar datos
$edades = [];
$adultos = 0;
$totalEdades = 0;
$cantidadPersonas = count($personas);

foreach ($personas as $persona => $edad) {
    $edades[] = $edad;
    $totalEdades += $edad;

    if ($edad >= EDAD_MINIMA) {
        $adultos++;
        echo $persona . " es mayor de edad\n";
    } else {
        echo $persona . " es menor de edad\n";
    }
}

// Calculamos el promedio de edad
if ($cantidadPersonas > 0) {
    $promedio = $totalEdades / $cantidadPersonas;
} else {
    $promedio = 0;
}

echo "\nCantidad de personas: " . $cantidadPersonas;
echo "\nCantidad de adultos: " . $adultos;
echo "\nPromedio de edad: " . $promedio . "\n";

$estadisticas = [
    "total_personas" => $cantidadPersonas,
    "adultos" => $adultos,
    "menores" => $cantidadPersonas - $adultos,
    "promedio_edad" => $promedio,
    "edad_minima_adulto" => EDAD_MINIMA
];

echo "\n=== ESTADÍSTICAS ===\n";
foreach ($estadisticas as $clave => $valor) {
    echo ucfirst(str_replace("_", " ", $clave)) . ": " . $valor . "\n";
}

?>