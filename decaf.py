import antlr4 as ant
from DecafLexer import DecafLexer

filein = open('testdata/lexer/id1', 'r')
lexer = DecafLexer(ant.InputStream(filein.read()))

tokens = lexer.getAllTokens()
print(lexer.symbolicNames[tokens[0].type])
