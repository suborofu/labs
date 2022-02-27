<?php
$path_to_file = 'counter.txt';

# Считывает предыдущее количество посещений страницы
$counter = file_get_contents($path_to_file);

# Увеличивает количество посещений страницы на 1
$counter++;

# Записывает количество посещений страницы
file_put_contents($path_to_file, $counter);

# Выводит количество посещений на экран
echo 'Всего посещений: '.$counter;
?>
