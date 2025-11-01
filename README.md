# project2_zhabinskaya_m25-555

# Управление таблицами
| Команда | Описание | 
|----------------|---------|
| create_table \<имя_таблицы> \<столбец1:тип> .. | создать таблицу|
| list_tables| показать список всех таблиц|
| drop_table \<имя_таблицы>  | удалить таблицу|
| help  | справочная информация|
| exit |  выход из программы|

[демонстрация управления таблицами ](https://asciinema.org/a/cGkhINqIgWXkpSOlMmVw517xE)

[![asciicast](https://asciinema.org/a/cGkhINqIgWXkpSOlMmVw517xE.svg)](https://asciinema.org/a/cGkhINqIgWXkpSOlMmVw517xE)

# CRUD-операции
| Команда | Описание | 
|----------------|---------|
| insert into \<имя_таблицы> values (\<значение1>, \<значение2>, ...)| создать запись|
| select from \<имя_таблицы> where \<столбец> = \<значение> | прочитать записи по условию|
| select from \<имя_таблицы> | прочитать все записи|
| update \<имя_таблицы> set \<столбец1> = \<новое_значение1> where \<столбец_условия> = \<значение_условия> | обновить запись|
| delete from \<имя_таблицы> where \<столбец> = \<значение> |  удалить запись|
| info \<имя_таблицы> |  вывести информацию о таблице|

[демонстрация работы CRUD-операций ](https://asciinema.org/a/DZHFaOHVBeRtdJSpMhLVUbMto)

[![asciicast](https://asciinema.org/a/DZHFaOHVBeRtdJSpMhLVUbMto.svg)](https://asciinema.org/a/DZHFaOHVBeRtdJSpMhLVUbMto)
