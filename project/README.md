# Как использовать приложение

```bash
usage: python -m project [-h] {print-graph-info,graphs-list,gen-graph} ...

optional arguments:
  -h, --help            show this help message and exit

graph utilities:
  {print-graph-info,graphs-list,gen-graph}
    print-graph-info    prints graph info
    graphs-list         prints list of available graphs
    gen-graph           generates graph
```

## graphs-list
Возвращает список имен доступных графов.
```bash
python -m project graphs-list
```
## print-graph-info
Возвращает информацию о графе по его имени.
```bash
python -m project print-graph-info graph-name
```
#### Пример
```bash
python -m project print-graph-info "generations"
```
## gen-graph
Создает граф в формате `DOT`.

### По имени графа
```bash
python -m project gen-graph by-name [-h] [--output PATH] name
```
* Если `--output PATH` указан, граф сохранится в файл, иначе – будет выведен на консоль.
#### Пример
```bash
python -m project gen-graph by-name "pizza" --output pizza.dot
```

### Граф с двумя циклами
```bash
python -m project gen-graph two-cycles [-h] [--edge-labels L1 L2] [--output PATH] num-first-cycle-nodes num-second-cycle-nodes
```
* Если `--output PATH` указан, граф сохранится в файл, иначе – будет выведен на консоль.
* Параметры по умолчанию для `--edge-labels`: 'a' и 'b'.

#### Пример
```bash
python -m project gen-graph two-cycles 2 3 --edge-labels "x" "y" --output test.dot
```
