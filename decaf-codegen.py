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
        self.st = SymbolTable()

    def visitProgram(self, ctx: DecafParser.ProgramContext):
        self.st.enterScope()
        self.visitChildren(ctx)
        self.st.exitScope()

    def visitField_decl(self, ctx: DecafParser.Field_declContext):
        line_num = ctx.start.line
        data_type = ctx.data_type().getText()

        field_count = len(ctx.field_name())
        for i in range(field_count):
            field_name = ctx.field_name(i).getText()

            if ctx.field_name(i).int_literal():
                array_size = int(ctx.field_name(i).int_literal().getText())
                if array_size <= 0:
                    print('Error on line', line_num, 'array declared with length 0')
            else:
                array_size = 1

            field_symbol = self.st.probe(field_name)

            if field_symbol:
                print('Error on line', line_num, 'field', field_name, 'is already declared on line', field_symbol.line)
            else:
                field_symbol = VarSymbol(id=field_name,
                                         type=data_type,
                                         line=line_num,
                                         size=8 * array_size,
                                         mem=HEAP)
                self.st.addSymbol(field_symbol)

        self.visitChildren(ctx)

    def visitMethod_decl(self, ctx: DecafParser.Method_declContext):
        line_num = ctx.start.line
        method_name = ctx.ID(0).getText()
        method_type = ctx.return_type().getText()
        method_params = []

        for i in range(len(ctx.data_type())):
            param_type = ctx.data_type(i).getText()
            param_name = ctx.ID(i + 1).getText()
            param_symbol = VarSymbol(id=param_name, type=param_type, line=line_num, size=8, mem=STACK)
            method_params.append(param_symbol)

        method_symbol = MethodSymbol(method_name,
                                     method_type,
                                     line_num,
                                     method_params)
        self.st.addSymbol(method_symbol)

        self.body += method_name + ':\n'
        if method_name == 'main':
            self.body += 'movq %rsp, %rbp\n'

        self.st.enterScope()
        for i in range(len(method_params)):
            self.st.addSymbol(method_params[i])
            self.body += 'movq ' + param_registers[i] + ',' + str(method_params[i].getAddr()) + '(%rsp)\n'

        self.visitChildren(ctx)
        self.body += 'ret\n'
        self.st.exitScope()

    def visitMethod_call(self, ctx: DecafParser.Method_callContext):
        if ctx.method_name():
            for i in range(len(ctx.expr())):
                self.visit(ctx.expr(i))
                self.st.stack_pointer[-1] += 8
                self.body += 'movq %rax, ' + str(-self.st.stack_pointer[-1]) + '(%rsp)\n'

            for i in range(len(ctx.expr())):
                self.body += 'movq ' + str(-self.st.stack_pointer[-1]) + '(%rsp), ' + param_registers[
                    len(ctx.expr()) - i - 1] + '\n'
                self.st.stack_pointer[-1] -= 8

            # adjust stack to 16-byte alignment (multiple of 8 that is not divisible by 16)
            stack_len = self.st.stack_pointer[-1]
            stack_len = stack_len + (stack_len // 8 + 1 % 2) * 8
            self.body += 'subq $' + str(stack_len) + ', %rsp\n'

            method_name = ctx.method_name().getText()
            self.body += 'call ' + method_name + '\n'

            self.body += 'addq $' + str(stack_len) + ', %rsp\n'
        elif ctx.CALLOUT():
            pass

    def visitExpr(self, ctx: DecafParser.ExprContext):
        if ctx.literal():
            int_literal = ctx.getText()
            self.body += 'movq $' + int_literal + ', %rax\n'
        elif ctx.location():
            loc_name = ctx.getText()
            location = self.st.lookup(loc_name)
            addr = str(location.getAddr())

            if location.mem == HEAP:
                self.body += 'movq ' + addr + '(%rbp), %rax\n'
            else:
                self.body += 'movq ' + addr + '(%rsp), %rax\n'
        else:
            self.visitChildren(ctx)


filein = open('testdata/codegen/17-webinar_test.dcf', 'r')
lexer = DecafLexer(ant.InputStream(filein.read()))

stream = ant.CommonTokenStream(lexer)

parser = DecafParser(stream)
tree = parser.program()

visitor = DecafSemanticChecker()
visitor.visit(tree)

code = visitor.head + visitor.body
print(code)
