import antlr4 as ant
from DecafLexer import DecafLexer
from DecafParser import DecafParser
from DecafVisitor import DecafVisitor
from SymbolTable import HEAP, STACK, SymbolTable, VarSymbol, MethodSymbol, param_registers

class DecafSemanticChecker(DecafVisitor):
    def __init__(self):
        super().__init__()
        self.head = '.data\n'
        self.body = '.global main\n'
        
    def visitProgram(self, ctx:DecafParser.ProgramContext):
        return self.visitChildren(ctx)

filein = open('testdata/codegen/02-expr.dcf', 'r')
lexer = DecafLexer(ant.InputStream(filein.read()))

stream = ant.CommonTokenStream(lexer)

parser = DecafParser(stream)
tree = parser.program()

visitor = DecafSemanticChecker()
visitor.visit(tree)

code = visitor.head + visitor.body
print(code)
