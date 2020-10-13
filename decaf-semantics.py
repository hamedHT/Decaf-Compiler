import antlr4 as ant
from DecafLexer import DecafLexer
from DecafParser import DecafParser
from DecafVisitor import DecafVisitor
from SymbolTable import HEAP, STACK, SymbolTable, VarSymbol, MethodSymbol

class DecafSemanticChecker(DecafVisitor):
    def __init__(self):
        super().__init__()
        self.st = SymbolTable()
        # initialise an empty Symbol Table object

    def visitProgram(self, ctx: DecafParser.ProgramContext):
        self.st.enterScope() # enter symbol table scope
        self.visitChildren(ctx)
        self.st.exitScope()

    def visitVar_decl(self, ctx: DecafParser.Var_declContext):
        line_num = ctx.start.line
        for var_decl in ctx.ID():
            var_name = var_decl.getText() # gets the variable name (eg. x)
            var_symbol = self.st.probe(var_name) # search Symbol Table for variable entry
            
            if var_symbol != None: # if variable does NOT exist in Symbol Table
                print('Error on line', line_num, 'variable \'', var_name,
                    '\' already declared on line', var_symbol.line)
            else:
                var_symbol = VarSymbol(id=var_name,
                                    type='int',
                                    line=line_num,
                                    size=8,
                                    mem=STACK)
                self.st.addSymbol(
                    var_symbol
                )  # add var_symbol to the scope (st abbreviation of SymbolTable)

        return self.visitChildren(ctx)

    # attempt to check all statement rules for a location symbol table check
    def visitStatement(self, ctx:DecafParser.StatementContext):
        if ctx.location() != None:
            line_num = ctx.start.line
            var_name = ctx.location().ID().getText()

            var_symbol = self.st.lookup(var_name)

            if var_symbol == None:
                print('Error on line', line_num, 'variable \'', var_name,
                      '\'is not declared')

        self.visitChildren(ctx)


filein = open('testdata/semantics/illegal-02.dcf', 'r')
lexer = DecafLexer(ant.InputStream(filein.read()))

stream = ant.CommonTokenStream(lexer)

parser = DecafParser(stream)
tree = parser.program()

visitor = DecafSemanticChecker()
visitor.visit(tree)
