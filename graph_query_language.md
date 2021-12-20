### Абстрактный синтаксис
```
prog = List<stmt>

stmt =
    bind of var * expr
  | print of expr

val =
    String of string
  | Int of int
  | Bool of bool
  | Graph of graph
  | Labels of labels
  | Vertices of vertices
  | Edges of edges

expr =
    Var of var                   // переменные
  | Val of val                   // константы
  | Set_start of Set<val> * expr // задать множество стартовых состояний
  | Set_final of Set<val> * expr // задать множество финальных состояний
  | Add_start of Set<val> * expr // добавить состояния в множество стартовых
  | Add_final of Set<val> * expr // добавить состояния в множество финальных
  | Get_start of expr            // получить множество стартовых состояний
  | Get_final of expr            // получить множество финальных состояний
  | Get_reachable of expr        // получить все пары достижимых вершин
  | Get_vertices of expr         // получить все вершины
  | Get_edges of expr            // получить все рёбра
  | Get_labels of expr           // получить все метки
  | Map of lambda * expr         // классический map
  | Filter of lambda * expr      // классический filter
  | Load of path                 // загрузка графа
  | Intersect of expr * expr     // пересечение языков
  | Concat of expr * expr        // конкатенация языков
  | Union of expr * expr         // объединение языков
  | Star of expr                 // замыкание языков (звезда Клини)

lambda = Lambda of variables * expr
```
### Конкретный синтаксис
```
prog -> (stmt SEMI EOL?)+

stmt -> PRINT expr
      | var ASSIGN expr

expr -> LP expr RP
      | anfunc
      | mapping
      | filtering
      | var
      | val
      | NOT expr
      | expr IN expr
      | expr AND expr
      | expr DOT expr
      | expr OR expr
      | expr KLEENE


graph -> load_graph
       | cfg
       | string
       | set_start
       | set_final
       | add_start
       | add_final
       | LP graph RP

load_graph -> LOAD GRAPH path
set_start -> SET START OF (graph | var) TO (vertices | var)
set_final -> SET FINAL OF (graph | var) TO (vertices | var)
add_start -> ADD START OF (graph | var) TO (vertices | var)
add_final -> ADD FINAL OF (graph | var) TO (vertices | var)

vertices -> vertex
          | vertices_range
          | vertices_set
          | select_reachable
          | select_final
          | select_start
          | select_vertices
          | LP vertices RP

vertex -> INT

edges -> edge
       | edges_set
       | select_edges

edge -> LP vertex COMMA label COMMA vertex RP
      | LP vertex COMMA vertex RP

labels -> label
        | labels_set
        | select_labels

label -> string

anfunc -> FUN variables COLON expr
        | LP anfunc RP

mapping -> MAP anfunc expr
filtering -> FILTER anfunc expr

select_edges -> SELECT EDGES FROM (graph | var)
select_labels -> SELECT LABELS FROM (graph | var)
select_reachable -> SELECT REACHABLE VERTICES FROM (graph | var)
select_final -> SELECT FINAL VERTICES FROM (graph | var)
select_start -> SELECT START VERTICES FROM (graph | var)
select_vertices -> SELECT VERTICES FROM (graph | var)
vertices_range -> LCB INT DOT DOT INT RCB

cfg -> CFG
string -> STRING
path -> STRING

vertices_set -> LCB (INT COMMA)* (INT)? RCB
              | vertices_range

labels_set -> LCB (STRING COMMA)* (STRING)? RCB

edges_set -> LCB (edge COMMA)* (edge)? RCB
var -> VAR

var_edge -> LP var COMMA var RP
          | LP var COMMA var COMMA var RP
          | LP LP var COMMA var RP COMMA var COMMA LP var COMMA var RP RP

variables -> (var COMMA)* var? | var_edge

val -> boolean
     | graph
     | edges
     | labels
     | vertices
     | boolean


boolean -> BOOL

FUN -> 'fun'
LOAD -> 'load'
SET -> 'set'
ADD -> 'add'
OF -> 'of'
TO -> 'to'
GRAPH -> 'graph'
VERTICES -> 'vertices'
LABELS -> 'labels'
SELECT -> 'select'
EDGES -> 'edges'
REACHABLE -> 'reachable'
START -> 'start'
FINAL -> 'final'
FROM -> 'from'
FILTER -> 'filter'
MAP -> 'map'
PRINT -> 'print'
BOOL -> TRUE | FALSE
TRUE -> 'true'
FALSE -> 'false'


ASSIGN -> '='
AND -> '&'
OR -> '|'
NOT -> 'not'
IN -> 'in'
KLEENE -> '*'
DOT -> '.'
COMMA -> ','
SEMI -> ';'
LCB -> '{'
RCB -> '}'
LP -> '('
RP -> ')'
QUOT -> '"'
TRIPLE_QUOT -> '"""'
COLON -> ':'
ARROW -> '->'

VAR -> ('_' | CHAR) ID_CHAR*

INT -> NONZERO_DIGIT DIGIT* | '0'
CFG -> TRIPLE_QUOT (CHAR | DIGIT | ' ' | '\n' | ARROW)* TRIPLE_QUOT
STRING -> QUOT (CHAR | DIGIT | '_' | ' ')* QUOT
ID_CHAR -> (CHAR | DIGIT | '_')
CHAR -> [a-z] | [A-Z]
NONZERO_DIGIT -> [1-9]
DIGIT -> [0-9]
WS -> [ \t\r]+
EOL -> [\n]+
```
### Пример 1
```
g = load graph "skos";
common_labels = (select lables from g) & (select labels from (load graph "graph.txt"));

print common_labels;
```
### Пример 2
```
g1 = load graph "hello";
g = set start of (set final of g1 to (select vertices from g1)) to {1..100};
l1 = "l1" | "l2";
q1 = ("type" | l1)*;
q2 = "subclass_of" . q;
res1 = g & q1;
res2 = g & q2;
s = select start vertices from g;
vertices1 = filter (fun v: v in s) (map (fun ((u_g,u_q1),l,(v_g,v_q1)): u_g) (select edges from res1));
vertices2 = filter (fun v: v in s) (map (fun ((u_g,u_q2),l,(v_g,v_q1)): u_g) (select edges from res2));
vertices3 = vertices1 & vertices2;

print vertices3;
```
