<?php
// Constante que define la edad mínima para ser considerado adulto
define("EDAD_MINIMA", 18);
// Declaración de un arreglo con datos de personas (nombre y edad)
$personas = [
    ["nombre" => "Ana", "edad" => 23],
    ["nombre" => "Luis", "edad" => 30],
    ["nombre" => "Carla", "edad" => 17],
    ["nombre" => "Pedro", "edad" => 25],
    ["nombre" => "Laura", "edad" => 40],
];
// Variables para almacenar datos
$edades = []; // Arreglo para guardar las edades
$adultos = 0; // Contador de adultos
$totalEdades = 0; // Suma total de todas las edades
$cantidadPersonas = count($personas); // Número total de personas

// Recorremos el arreglo para analizar a cada persona
foreach ($personas as $persona) {
    // Agregamos la edad al arreglo de edades
    $edades[] = $persona["edad"];
    // Sumamos la edad al total
    $totalEdades += $persona["edad"];

    // Verificamos si es mayor de edad
    if ($persona["edad"] >= EDAD_MINIMA) {
        $adultos++;
        echo $persona["nombre"] . " es mayor de edad\n";
    } else {
        echo $persona["nombre"] . " es menor de edad\n";
    }
}

// Calculamos el promedio de edad (evitando división por cero)
if ($cantidadPersonas > 0) {
    $promedio = $totalEdades / $cantidadPersonas;
} else {
    $promedio = 0;
}

// Mostramos resultados finales
echo "\nCantidad de personas: " . $cantidadPersonas;
echo "\nCantidad de adultos: " . $adultos;
echo "\nPromedio de edad: " . $promedio . "\n";

//definicion de funcion
function sumar($num1, $num2) {
    $resultado = $num1 + $num2;
    return $resultado;
}

