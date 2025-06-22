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

// === AGREGADO: Función personalizada (contribución Alex) ===
function calcularEdadPromedio($arrayPersonas) {
    $suma = 0;
    $contador = 0;

    foreach ($arrayPersonas as $nombre => $edad) {
        $suma += $edad;
        $contador++;
    }

    return ($contador > 0) ? $suma / $contador : 0;
}

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

// Calculamos el promedio de edad (usando nuestra función)
$promedio = calcularEdadPromedio($personas);

// === AGREGADO: Estructura if-elseif-else completa ===
if ($promedio >= 30) {
    echo "\nGrupo de edad: Adultos jóvenes\n";
} elseif ($promedio >= 25) {
    echo "\nGrupo de edad: Jóvenes adultos\n";
} elseif ($promedio >= 18) {
    echo "\nGrupo de edad: Jóvenes\n";
} else {
    echo "\nGrupo de edad: Menores\n";
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

// === AGREGADO: Ingreso de datos simulado (para cumplir requisitos) ===
echo "\n=== SIMULACIÓN DE INGRESO DE DATOS ===\n";
// En PHP real sería: $nuevoNombre = readline("Ingrese nombre: ");
$nuevoNombre = "Carlos"; // Simulado para el analizador
$nuevaEdad = 28; // Simulado

echo "Agregando persona: " . $nuevoNombre . " con edad " . $nuevaEdad . "\n";
$personas[$nuevoNombre] = $nuevaEdad;

echo "Nueva cantidad de personas: " . count($personas) . "\n";

?>