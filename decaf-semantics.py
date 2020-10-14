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
        self.st.enterScope()  # enter symbol table scope
        self.visitChildren(ctx)
        self.st.exitScope()

    def visitVar_decl(self, ctx: DecafParser.Var_declContext):
        # semantic rule: No identifier is declared twice in the same scope
        line_num = ctx.start.line
        for var_decl in ctx.ID():
            var_name = var_decl.getText()  # gets the variable name (eg. x)
            var_symbol = self.st.probe(
                var_name)  # search Symbol Table for variable entry

            if var_symbol != None:  # if variable does NOT exist in Symbol Table
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

    def visitStatement(self, ctx: DecafParser.StatementContext):
        # semantic rule: No identifier is used before it is declared
        if ctx.location() != None:
            line_num = ctx.start.line
            var_name = ctx.location().ID().getText()

            var_symbol = self.st.lookup(var_name)

            if var_symbol == None:
                print('Error on line', line_num, 'variable \'', var_name,
                      '\'is not declared')

        self.visitChildren(ctx)

    # warn the user that any method defined after the main method will never be executed.

    # semantic rule: int_literal in an array declaration must be greater than 0
    def visitField_name(self, ctx: DecafParser.Field_nameContext):
        if ctx.int_literal() != None:
            if int(ctx.int_literal().DECIMAL_LITERAL().getText()) < 1:
                line_num = ctx.start.line
                var_name = ctx.ID().getText()
                print("Error on line", line_num, "variable '", var_name,
                      "' array size must be greater than 0")

        return self.visitChildren(ctx)

    # semantic rule: number and types of arguments in a method call must be the same as 
    #   the number and types of the formals, i.e., the signatures must be identical.
    # 1. check lengths of method_call params === method_decl params
    def visitMethod_call(self, ctx:DecafParser.Method_callContext):
        print(len(ctx.expr()))
        return self.visitChildren(ctx)


filein = open('testdata/semantics/illegal-05.dcf', 'r')
lexer = DecafLexer(ant.InputStream(filein.read()))

stream = ant.CommonTokenStream(lexer)

parser = DecafParser(stream)
tree = parser.program()

visitor = DecafSemanticChecker()
visitor.visit(tree)
