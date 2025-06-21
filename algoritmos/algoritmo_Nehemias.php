<?php
<?php
// Algoritmo de Pila (LIFO - Last In, First Out)
// Contribuidor: NLindao2004

// Definir tamaño máximo de la pila
define("TAMAÑO_MAXIMO", 5);

// Declarar la pila como array vacío
$pila = [];

// Variable para el tope de la pila
$tope = 0;

// Agregar elementos a la pila (PUSH)
$elemento1 = 10;
$pila[] = $elemento1;
$tope = $tope + 1;

$elemento2 = 20;
$pila[] = $elemento2;
$tope = $tope + 1;

$elemento3 = 30;
$pila[] = $elemento3;
$tope = $tope + 1;

// Mostrar estado de la pila
echo "Elementos en la pila: ";
echo $tope;

// Remover elemento de la pila (POP)
$elementoRemovido = $pila[$tope];
$tope = $tope - 1;

echo "Elemento removido: ";
echo $elementoRemovido;

// Mostrar nuevo estado
echo "Nuevo tope: ";
echo $tope;

// Verificar si la pila está vacía
$estaVacia = 0;
if ($tope == 0) {
    $estaVacia = 1;
}

echo "Pila vacia: ";
echo $estaVacia;
?>