# hse_prolog_parser

## Синтаксический анализатор с использованием yacc

<details>
<summary>
 Перед запуском
</summary>
Инструкция действительна только для пользователей Ubuntu.

Для работы необходим инструмент синтаксического анализа `parsec` для `python3` установить его можно через `pip3`
Установка `pip3`:
```bash
sudo apt update
sudo apt install python3-pip
```
Установка `parsec`:
```bash
pip3 install parsec
```
</details>

### Использование
Если хочется проверить свою программу с названием `program`, то надо написать:
```
python3 syntacticalAnalyzer.py program
```
Вы можете ввести сразу несколько программ и проверить их. 
Если ничего не вводить, то ввод программы будет из консоли. Когда Вы введете всю программу, воспользуйтесь `Ctrl + D`, чтобы закончить. Выходной файл будет `<stdin>.out`

Если программа синтаксически корректна, то вы увидите `Correct` и в файле `program.out` результат анализа, или указание, в какой момент произошла синтаксическая ошибка.
