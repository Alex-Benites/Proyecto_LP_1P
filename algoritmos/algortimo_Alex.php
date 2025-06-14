<?php
<?php
// Algoritmo de ejemplo - Alex
$numeros = [10, 25, 3, 45, 7];

// Encontrar el mayor número
$mayor = $numeros[0];
foreach ($numeros as $num) {
    if ($num > $mayor) {
        $mayor = $num;
    }
}

echo "El número mayor es: $mayor\n";

// Validación con if-else
if ($mayor > 20) {
    echo "El número mayor es mayor que 20\n";
} elseif ($mayor == 20) {
    echo "El número mayor es igual a 20\n";
} else {
    echo "El número mayor es menor que 20\n";
}

// Variable string
$mensaje = "Hola mundo PHP";
echo $mensaje . "\n";
?>