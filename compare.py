import ast
import argparse

def Levenstein(A,B):


    F = [[(i+j) if i*j == 0 else 0 for j in range(len(B)+1)]
         for i in range (len(A)+1)]
    for i in range(1, len(A)+1):
        for j in range (1, len(B)+1):
            if A[i-1] == B[j-1]:
                F[i][j] = F[i-1][j-1]
            else:
                F[i][j] = 1 + min(F[i-1][j], F[i][j-1], F[i-1][j-1])
    return F[-1][-1]

class Visitor(ast.NodeVisitor):


    def __init__(self):
        self.token = []

    def generic_visit(self, node):

        if isinstance(node, ast.FunctionDef):
            self.token.append("K")
            for _ in range(len(node.args.args)+1):   #+1 - чтобы учитывать имя функции ещё
                self.token.append("S")

        elif isinstance(node, ast.Assign):
            self.token.append("O")
            
        elif isinstance(node, ast.Constant) or isinstance(node, ast.Name) or isinstance(node, ast.alias):
            self.token.append("S")

        elif isinstance(node, ast.Binop) or isinstance(node, ast.unaryop) or isinstance(node, ast.cmpop) or isinstance(node, ast.boolop) :
            self.token.append("O")

        elif type(node).__name__ == "For" or type(node).__name__ == "While" :
            self.token.append("C")
            
        elif isinstance(node, ast.stmt):
            self.token.append("K")

        elif isinstance(node, ast.expr):
            self.token.append("E")

        ast.NodeVisitor.generic_visit(self, node)



        
parser = argparse.ArgumentParser()
parser.add_argument('inp', type=str, help='File input')
parser.add_argument('scores', type=str, help='File scores')
args = parser.parse_args()
inp = open(args.inp,"r").read()
scores = open(args.scores, "w")

while True:
    f = inp.readline().rstrip().split()
    if not f:
        break
    file1 = f[0]
    file2 = f[1]
    x1 = Visitor()
    t1 = ast.parse(file1)
    x1.visit(t1)
    x2 = Visitor()
    t2 = ast.parse(file2)
    x2.visit(t2)
    cmp1 = "".join(x1.token)
    cmp2 = "".join(x2.token)
    scores.write(1 - Levenstein(cmp1, cmp2)/max(len(cmp1), len(cmp2)))

inp.close()
scores.close()
