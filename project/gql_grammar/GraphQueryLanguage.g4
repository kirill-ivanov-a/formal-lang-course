grammar GraphQueryLanguage;

prog : (EOL? WS? stmt SEMI EOL?)+ EOF;

stmt : PRINT expr
     | VAR WS? ASSIGN WS? expr
     ;

expr : LP expr RP
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
     ;

grph : load_graph
      | cfg
      | string
      | set_start
      | set_final
      | add_start
      | add_final
      | LP grph RP
      ;

load_graph : LOAD GRAPH (path | string);
set_start : SET START OF (grph | var) TO (vertices | var) ;
set_final : SET FINAL OF (grph | var) TO (vertices | var) ;
add_start : ADD START OF (grph | var) TO (vertices | var) ;
add_final : ADD FINAL OF (grph | var) TO (vertices | var) ;

vertices : vertex
       | vertices_range
       | vertices_set
       | select_reachable
       | select_final
       | select_start
       | select_vertices
       | LP vertices RP
       ;


vertex : INT ;

edges : edge
      | edges_set
      | select_edges ;

edge : LP vertex COMMA label COMMA vertex RP
     | LP vertex COMMA vertex RP ;

labels : label
       | labels_set
       | select_labels ;

label : string ;

anfunc : FUN variables COLON expr
       | LP anfunc RP ;

mapping : MAP anfunc expr;
filtering : FILTER anfunc expr;

select_edges : SELECT EDGES FROM (grph | var) ;
select_labels : SELECT LABELS FROM (grph | var) ;
select_reachable : SELECT REACHABLE VERTICES FROM (grph | var) ;
select_final : SELECT FINAL VERTICES FROM (grph | var) ;
select_start : SELECT START VERTICES FROM (grph | var) ;
select_vertices : SELECT VERTICES FROM (grph | var) ;
vertices_range : LCB INT DOT DOT INT RCB ;

cfg : CFG ;
string : STRING ;
path : PATH ;

vertices_set : LCB (INT COMMA)* (INT)? RCB
             | vertices_range ;

labels_set : LCB (STRING COMMA)* (STRING)? RCB ;

edges_set : LCB (edge COMMA)* (edge)? RCB ;
var : VAR ;

var_edge : LP var COMMA var RP
         | LP var COMMA var COMMA var RP
         | LP LP var COMMA var RP COMMA var COMMA LP var COMMA var RP RP
         ;

variables : (var COMMA)* var?
     | var_edge
     ;

val : boolean
    | grph
    | edges
    | labels
    | vertices
    | boolean
    ;


boolean : BOOL;


FUN : WS? 'fun' WS?;
LOAD : WS? 'load' WS? ;
SET : WS? 'set' WS? ;
ADD : WS? 'add' WS? ;
OF : WS? 'of' WS? ;
TO : WS? 'to' WS? ;
GRAPH : WS? 'graph' WS?;
VERTICES : WS? 'vertices' WS? ;
LABELS : WS? 'labels' WS? ;
SELECT : WS? 'select' WS? ;
EDGES : WS? 'edges' WS? ;
REACHABLE : WS? 'reachable' WS? ;
START : WS? 'start' WS? ;
FINAL : WS? 'final' WS? ;
FROM : WS? 'from' WS? ;
FILTER : WS? 'filter' WS? ;
MAP : WS? 'map' WS? ;
PRINT : WS? 'print' WS?;
BOOL : TRUE | FALSE;
TRUE : 'true' ;
FALSE : 'false' ;


ASSIGN : WS? '=' WS? ;
AND : WS? '&' WS?;
OR : WS? '|' WS? ;
NOT : WS? 'not' WS? ;
IN : WS? 'in' WS?;
KLEENE : WS? '*' WS?;
DOT : WS? '.' WS? ;
COMMA : WS? ',' WS?;
SEMI : ';' WS?;
LCB : '{' WS?;
RCB : WS? '}' WS?;
LP : '(' WS?;
RP : WS? ')' ;
QUOT : '"' ;
TRIPLE_QUOT : '"""' ;
COLON : ':' ;
ARROW : '->' ;



VAR : ('_' | CHAR) ID_CHAR* ;

INT : NONZERO_DIGIT DIGIT* | '0' ;
CFG : TRIPLE_QUOT (CHAR | DIGIT | ' ' | '\n' | ARROW)* TRIPLE_QUOT ;
STRING : QUOT (CHAR | DIGIT | '_' | ' ')* QUOT ;
PATH : QUOT (CHAR | DIGIT | '_' | ' ' | '/' | DOT)* QUOT ;
ID_CHAR : (CHAR | DIGIT | '_');
CHAR : [a-z] | [A-Z];
NONZERO_DIGIT : [1-9];
DIGIT : [0-9];
WS : [ \t\r]+ -> skip;
EOL : [\n]+;
