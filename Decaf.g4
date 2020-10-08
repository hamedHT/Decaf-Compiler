grammar Decaf;

/*LEXER RULES*/
/* variables names, reserved words, literals, symbols, operators */

CLASS: 'class';
LCURLY: '{';
RCURLY: '}';
LSQBRACKET: '[';
RSQBRACKET: ']';

PLUS : '+';
MINUS : '-';
MULTIPLY : '*';
LESS_THAN: '<';
LESS_THAN_EQUAL_TO: '<=';
NOT : '!=';
AND : '&&';
IF : 'if';
NEW : 'new';
INT: [0-9];
BOOL: 'true' | 'false';
STRING : '"' (ALPHA | DIGIT | ' ')* '"';

fragment TAB : '\t';
CHAR: '\'' (ALPHA | [0-9] | TAB) '\'';

fragment ALPHA: [a-zA-Z];
ID: ALPHA+;

IDENTIFIER : (ALPHA | '_')+;
HEX_LITERAL : '0x' HEX_DIGIT HEX_DIGIT*;
fragment HEX_DIGIT : DIGIT | [a-zA-Z];
DIGIT : [0-9];

// INT_LITERAL : DECIMAL_LITERAL | HEX_LITERAL;
DECIMAL_LITERAL: DIGIT DIGIT*;

COMMENT: '//' ~'\n'* '\n' -> skip;
WS: [ \t\r\n]+ -> skip;

/*parser rules*/

program: CLASS ID LCURLY field_decl* RCURLY EOF;
// field_decl: data_type (ID | ID '[' INT_LITERAL ']')+; /* check , COMMA syntax */
field_decl: data_type field_name (',' field_name)* ';';
field_name : ID | ID LSQBRACKET int_literal RSQBRACKET;
int_literal : DECIMAL_LITERAL | HEX_LITERAL;
data_type: 'int' | 'boolean';