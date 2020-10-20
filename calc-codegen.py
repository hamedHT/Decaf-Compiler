import antlr4 as ant
from CalcLexer import CalcLexer
from CalcParser import CalcParser
from CalcVisitor import CalcVisitor
from SymbolTable import HEAP, STACK, SymbolTable, VarSymbol, MethodSymbol

class CalcSemanticChecker(CalcVisitor):
    def __init__(self):
        super().__init__()
        self.head = '.data\n'
        self.body = '.global main\n'

    def visitCalculator(self, ctx:CalcParser.CalculatorContext):
        self.body += 'main:\n'
        val = self.visitChildren(ctx)
        self.body += 'ret\n'
        return val

    def visitStatement(self, ctx:CalcParser.StatementContext):
        return self.visitChildren(ctx)

    def visitExpr(self, ctx:CalcParser.ExprContext):
        return self.visitChildren(ctx)

filein = open('testdata/test_06.calc', 'r')
lexer = CalcLexer(ant.InputStream(filein.read()))

stream = ant.CommonTokenStream(lexer)

parser = CalcParser(stream)
tree = parser.calculator()

visitor = CalcSemanticChecker()
visitor.visit(tree)

code = visitor.head + visitor.body
print(code)
