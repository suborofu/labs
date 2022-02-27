<?php
$path_to_file = 'counter.txt';

$file = fopen($path_to_file, 'r');
$counter = fgets($file);
fclose($file);

$counter++;

$file = fopen($path_to_file, 'w');
fwrite($file, $counter);
fclose($file);

echo 'Всего посещений: '.$counter;
?>
