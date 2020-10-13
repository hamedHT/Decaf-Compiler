This project is practice for building a Compiler using Antlr4

# Commands

## Parser (Java)

`antlr4 Decaf.g4`
`javac Decaf*.java` <!-- compiles java bytecode files -->
`grun Decaf program -gui testdata/parser/legal-01`

## Parser (with Python target modules)

`antlr4 Decaf.g4 -Dlanguage=Python3`
`antlr4 Decaf.g4 -Dlanguage=Python3 -visitor` <!-- Creates a template Vistor python file with a template Class of Antlr objects -->
