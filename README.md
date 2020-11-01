This project is practice for building a Compiler using Antlr4

# Commands

## Parser (Java)

`antlr4 Decaf.g4`

`javac Decaf*.java` <!-- compiles java bytecode files -->

`grun Decaf program -gui testdata/parser/legal-01`

## Parser (with Python target modules)

`antlr4 Decaf.g4 -Dlanguage=Python3`

`antlr4 Decaf.g4 -Dlanguage=Python3 -visitor` <!-- Creates a template Vistor python file with a template Class of Antlr objects -->

## Decaf Compiler Semantic rules todo
- [x] (1) No identifier is declared twice in the same scope.
- [x] (2) No identifier is used before it is declared.
- [ ] (3) The program contains a definition for a method called main that has no parameters (note that since execution starts at method main, any methods defined after main will never be executed).
- [x] (4) The int_literal in an array declaration must be greater than 0.
- [x] (5) The number and types of arguments in a method call must be the same as the number and types of the formals, i.e., the signatures must be identical.
- [ ] (6) If a method call is used as an expression, the method must return a result.
- [ ] (7) A return statement must not have a return value unless it appears in the body of a method that is declared to return a value.
- [ ] (8) The expression in a return statement must have the same type as the declared result type of the enclosing method definition.
- [ ] (9) An id used as a location must name a declared local/global variable or formal parameter. 
- [ ] (10) For all locations of the form id[expr] 
  - [ ] id must be an array variable
  - [ ] the type of expr must be int
- [ ] (11) The expr in an if statement must have type boolean
- [ ] (12) The operands of arith_op and rel_op must have type int.
- [ ] (13) The operands of eq_op must have the same type, either int or boolean
- [ ] (14) The operands of cond_op and logical not ! must have type boolean
- [ ] (15) The location and the expr in an assignment, location = expr, must have the same type.
- [ ] (16) The location and the expr in an incrementing/decrementing assignment, location += expr and location --= expr, must be of type
- [ ] (17) The initial expr and the ending expr of for must have type int.
- [ ] (18) Break and continue statements must be within the body of a for.

## Decaf Code generation testing todo
testdata/codegen
- [x] 00-empty
- [x] 01-callout Add Decaf callout string to Head section of GNU assembly 
- [ ] 02-expr
- [ ] 03-math
- [ ] 04-math2
- [ ] 05-calls
- [ ] 06-control-flow
- [ ] 07-recursion
- [ ] 08-array
- [ ] 09-global
- [ ] 10-bounds

see codegen directory for more ...
- [x] 17-webinar_test.dcf
- [ ] 18-Arrays implement array declaration with statements and expressions
