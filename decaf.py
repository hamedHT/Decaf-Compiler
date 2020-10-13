import antlr4 as ant
from DecafLexer import DecafLexer
from DecafParser import DecafParser

fileIn = open('testdata/semantics/illegal-01.dcf', 'r')
lexer = DecafLexer(ant.InputStream(fileIn.read()))

# tokens = lexer.getAllTokens()
# for token in tokens:
#     print(lexer.symbolicNames[token.type])

parser = DecafParser(ant.CommonTokenStream(lexer))
tree = parser.program()  # parser.x() x being the g4 parser rule entry point
