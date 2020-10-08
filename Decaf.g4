grammar Decaf;

/*LEXER RULES*/

CLASS : 'class';
LCURLY : '{';
RCURLY : '}';

fragment ALPHA : [a-zA-Z];
ID : ALPHA+;

WS : [ \t\r\n]+ -> skip;

/*parser rules*/

program : CLASS ID LCURLY RCURLY EOF;
