# Commands

## Parser (Java)

antlr4 Decaf.g4
javac Decaf\*.java <!-- compiles java bytecode files -->
grun Decaf program -gui testdata/parser/legal-01

## Parser (with Python target modules)

antlr4 Decaf.g4 -Dlanguage=Python3
