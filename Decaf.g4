grammar Decaf;

/*
  LEXER RULES
  variables names, reserved words, literals, symbols, operators
*/

BOOLEAN : 'boolean';
BREAK : 'break';
CALLOUT : 'callout';
CLASS : 'class';
CONTINUE : 'continue';
ELSE : 'else';
FALSE : 'false';
FOR : 'for';
IF : 'if';
INT : 'int';
RETURN : 'return';
TRUE : 'true';
VOID : 'void';
LCURLY : '{';
RCURLY : '}';
LSQUARE : '[';
RSQUARE : ']';
LBRACE : '(';
RBRACE : ')';
PLUS : '+';
MINUS : '-';
MULTIPLY : '*';
DIVIDE : '/';
MOD : '%';
SEMICOLON : ';';
COMMA : ',';
EXCLAMATION : '!';
LESS_THAN : '<';
GREATER_THAN : '>';
LESS_OR_EQUAL : '<=';
GREATER_OR_EQUAL : '>=';
DOUBLE_EQUAL : '==';
NOT_EQUAL : '!=';
AND : '&&';
OR : '||';
ASSIGN : '=';
PLUS_ASSIGN : '+=';
MINUS_ASSIGN : '-=';

fragment ALPHA : [a-zA-Z_];
fragment DIGIT : [0-9];
fragment ALPHA_NUM : ALPHA | DIGIT;
ID : ALPHA ALPHA_NUM*;

DECIMAL_LITERAL : DIGIT+;
fragment HEX_DIGIT : DIGIT | [a-fA-F];
HEX_LITERAL : '0x' HEX_DIGIT+;

WS : [ \t\r\n]+ -> skip;
COMMENT : '//' ~'\n'* '\n' -> skip;

fragment GOOD_CHARS : [ -~];
fragment DOUBLE_CHARS : '\\' ('n' | '"' | '\'' | '\\');
CHAR : '\'' (GOOD_CHARS | DOUBLE_CHARS) '\'';

STRING_LITERAL : '"' (GOOD_CHARS | DOUBLE_CHARS)* '"';

/*
  PARSER RULES
*/

program : CLASS ID LCURLY field_decl* method_decl* RCURLY EOF;

field_name : ID | ID LSQUARE int_literal RSQUARE;
field_decl : data_type field_name (COMMA field_name)* SEMICOLON;

//warning: type conflicts with a variable in ANTLR4
data_type : INT | BOOLEAN;

expr :  location
  |     method_call
  |     literal
  |     LBRACE expr RBRACE
  |     MINUS expr
  |     EXCLAMATION expr
  |     expr (MULTIPLY | DIVIDE | MOD) expr
  |     expr (PLUS | MINUS) expr
  |     expr (LESS_THAN | GREATER_THAN | LESS_OR_EQUAL | GREATER_OR_EQUAL) expr
  |     expr (DOUBLE_EQUAL | NOT_EQUAL) expr
  |     expr AND expr
  |     expr OR expr;

method_call : method_name LBRACE (expr (COMMA expr)*)? RBRACE
  |           CALLOUT LBRACE STRING_LITERAL (COMMA callout_arg)* RBRACE;

method_name : ID;
callout_arg : expr | STRING_LITERAL;

bool_literal : TRUE | FALSE;
char_literal : CHAR;
int_literal : DECIMAL_LITERAL | HEX_LITERAL;
literal : int_literal | bool_literal | char_literal;

location : ID | ID LSQUARE expr RSQUARE;

method_decl : return_type ID LBRACE (data_type ID (COMMA data_type ID)*)? RBRACE block;

return_type : data_type | VOID;

block : LCURLY var_decl* statement* RCURLY;

var_decl : data_type ID (COMMA ID)* SEMICOLON;

assign_op : ASSIGN | PLUS_ASSIGN | MINUS_ASSIGN;

statement :   location assign_op expr SEMICOLON
            | method_call SEMICOLON
            | IF LBRACE expr RBRACE block (ELSE block)?
            | FOR ID ASSIGN expr COMMA expr block
            | RETURN expr? SEMICOLON
            | BREAK SEMICOLON
            | CONTINUE SEMICOLON
            | block;