import re
import os
file1 = open("klee-out.txt","r+") 
content = file1.read()
content = content.replace("\t", " ")
content = content.replace("\n", " ")
content = content.replace("\r", " ")
content = content.replace("  ", " ")
#print (content)

class Constraint:
    
    def __init__(self, type, expr, val, total, now):
        self.type = type
        self.total = expr
        self.now = now
        self.expr = expr
        self.val = val

    def getType(self):
        return self.type

    def toKqueryExpr(self):
        return "(Eq %s (%s))\n" % (self.val, self.expr)

def loadDecl():
    # find klee-last folder
    klee_last_folder = "./klee-last/"
    # load context from test*.kquery file
    kquery_file = "test000001.kquery"
    kquery = open(klee_last_folder+kquery_file, "r+").read()
    kquery = kquery.replace("\t", " ")
    kquery = kquery.replace("\r", " ")
    kquery = kquery.replace("  ", " ")
    # load decl from context 
    decl = re.split("\n\(query", kquery)[0]
    
    return decl

def match(stream):
    regex = r"Output is (\d+), total (\d+), now (\d+)-th:\((.*)\) == (0|1) "
    
    match = re.search(regex, stream) 
    if match != None: 
        return Constraint(match.group(1), match.group(4), match.group(5), match.group(2), match.group(3))
    else: 
        return None

def findall(decl, stream):
    stream = re.split("MARK:", stream)
    types = {}
    constrs = []
    for each in stream[1:]:
        m = match(each)
        if (m is None):
            pass
        else:
            if m.type in types.keys():
                idx = types.get(m.type)
                constrs[idx].append(m)
            else:
                types[m.type] = len(constrs)
                constrs.append([m])
    folder = "./verifies"
    if not os.path.isdir(folder):
        os.mkdir(folder)
    kquery = decl 
    qIdx = 0
    for type in types.items():
        kquery = kquery + "\n# query %d, type %s\n(query [\n" % (qIdx, type[0])
        qIdx = qIdx + 1
        for each in constrs[type[1]]:
            kquery = kquery + each.toKqueryExpr()
        kquery = kquery + "] false )"
    file_name = "query.kquery"
    w = open(folder+"/"+file_name, "w+")
    w.write(kquery)
    w.close()
    cmd = "kleaver %s/%s" % (folder, file_name)
    os.system(cmd)

def main():
    decl = loadDecl()
    findall(decl, content)

main()