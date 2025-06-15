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

