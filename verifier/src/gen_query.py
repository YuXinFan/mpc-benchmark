import re
import os

EXPR=r"\([\[\(0-9a-zA-Z\:\@\_\ \,\)\]]*\)"
def load_decls():
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

def AndCat(l):
    #print("AndCat", l)
    if len(l) == 0:
        os.error("No elements")
    if len(l) == 1:
        return "(Eq %s %s)\n" % (l[0][1], l[0][0])
    else:
        ll = len(l)
        andcat = ""
        lbracket = 0
        for i in range(0, len(l)-1):
            andcat  = andcat + "(And " + "(Eq %s %s)\n" % (l[i][1], l[i][0]) + " "
            lbracket = lbracket + 1
        andcat = andcat + "(Eq %s %s)\n" % (l[ll-1][1], l[ll-1][0]) + ")"*lbracket
        return andcat 

def find_and_replace_label_def(expr):
    defcnt = 0
    defdef = "N%d" % defcnt
    ll=re.search(defdef + ":", expr)
    while ll != None:    
        l = 1
        defexpr = "("
        idx = ll.end()+1
        while l > 0:
            if expr[idx] == "(":
                l = l + 1
                defexpr = defexpr + "("
            elif expr[idx] == ")":
                l = l - 1
                defexpr = defexpr + ")"
            else:
                defexpr = defexpr + expr[idx]
            idx = idx + 1
        expr = expr.replace(defdef+":", "")

        lop = " "+defdef+" "
        lrep = " "+defexpr+" "

        rop = " "+defdef+"\)"
        rrep = " "+defexpr+")"

        expr = re.sub(lop, lrep, expr)
        expr = re.sub(rop, rrep, expr)

        defcnt = defcnt + 1
        defdef = "N%d" % defcnt
        ll = re.search(defdef+":", expr)
    return expr 

def make_decls(path):
    fs = open(path, "r+")
    kqs = fs.read()
    kq = kqs.split("# Query")[-1]
    lines = kq.split("\n")
    decl = ""
    for line in lines:
        if "array" in line:
            decl = decl + line + "\n"
    print(decl)
    return decl
def make_assumes(part):
    l = []
    for x in part:
        if "N0:(ReadLSB w32 0 arr) N1:" in x:
            print(x)
        m = find_and_replace_label_def(x)
        l.append("(Eq 1  %s)\n" % m)
    return l 

def make_constraints(partB, partC, asize):
    # sort by id 
    # construct expr for each id 
    # merge same id
    # one expr --> multi-id 
    # one id --> multi-constraint
    
    # sort by id 
    def cmp_id(l):
        return int(l[0])
    def cmp_idx(l):
        return int(l[1])
    def cmp_result(l):
        return l[1]

    # ret expr --> milti-id
    sorted_parts = sorted(partB, key=cmp_id)
    ret_ids_map = {}
    id_exprs_map = {}
    if partB == []:
        for t in partC:
            if t[0] not in ret_ids_map.keys():
                ret_ids_map[t[0]] = [t[0]]
                id_exprs_map[t[0]] = []

    else:
        for i in range(0, len(sorted_parts), asize):
            part = sorted(sorted_parts[i:i+asize], key=cmp_idx)
            if part[0][0] in id_exprs_map.keys():
                os.error("Array size %d, find id %s appears more than %d times." %(asize, part[0][0], asize))
                #exit("more then 4")
            else:
                id_exprs_map[part[0][0]] = []
                ret =", ".join([x[2] for x in part])
                if ret in ret_ids_map.keys():
                    ret_ids_map[ret].append(part[0][0])
                else:
                    ret_ids_map[ret] = [part[0][0]]
    print("%d Different Result Expr" % len(ret_ids_map.keys()))
    for ret in ret_ids_map.keys():
        print("%d ids for %s" % (len(ret_ids_map[ret]), ret) )
    #print(ret_ids_map)

    # id --> multi-constraints
    for i in partC:
        id_exprs_map[i[0]].append((i[3],i[4]))
    
    ret_exprs_map = {}
    for ret in ret_ids_map.keys():
        print(ret)
        all_exprs = [x for id in ret_ids_map[ret] for x in id_exprs_map[id]]
        for i in range(len(all_exprs)):
            all_exprs[i] = (find_and_replace_label_def(all_exprs[i][0]), all_exprs[i][1])
        const_expr = "(Not " + AndCat(all_exprs) + ")"    
        ret_exprs_map[ret] = const_expr
    # ret expr --> constraints
    return ret_exprs_map



def make_query(file_name, decls, assumes, constraints):
    folder = "../log"
    if not os.path.isdir(folder):
        os.mkdir(folder)
    kquery = decls 
    assumes = " ".join(assumes)
    qIdx = 0
    for ret_expr in constraints.keys():
        kquery = kquery + "\n# query %d, ret expr [%s]\n" % (qIdx, ret_expr) \
             + "(query [ " + assumes + "]\n" \
             + constraints[ret_expr] + ")" 
        qIdx = qIdx + 1
    w = open(folder+"/"+file_name, "w+")
    w.write(kquery)
    w.close()
    #cmd = "kleaver %s/%s" % (folder, file_name)
    #os.system(cmd)

def main(ofile,qfile):
    #decls = load_decls()

    file1 = open(ofile,"r+") 
    #content = file1.read()
    content = []
    for line in file1.readlines():
        if "KLEE:" not in line and "WARNING:" not in line:
            content.append(line)
    content = "".join(content)
    content = " ".join(content.split())

    file2 = open("../log/temp.out", "w+")
    file2.write(content)
    file1.close()
    file2.close()


    partA = re.findall(r"\[Part\-A\] Assume:(\([\[\(0-9a-zA-Z\_\@\,\:\ \)\]]*\))", content)
    arraySize = re.findall(r"\[Array\] Size:(\d+)", content)
    partB = re.findall(r"\[Part\-B\] id (-?\d+), array idx (\d+):(\([\[\(0-9a-zA-Z\:\=\_\@\,\ \)\]]*\)|-?\d+)", content)
    partC = re.findall(r"\[Part\-C\] id (-?\d+), total (\d+), now (\d+)\-th:(\([\[\(0-9a-zA-Z\:\=\@\,\_\ \)\]]*\)|-?\d+) == (0|1)", content)
    #print("Array:\n",partB)
    assumes = make_assumes(partA)
    print("%d Assumes" % len(assumes))
    #print("Assumes:\n", partA)
    if arraySize == [] :
        arraySize = 0
    else:
        arraySize = int(arraySize[0])
    print("%d Result Expr" %  (len(partB) if arraySize==0 else len(partB)/arraySize) )
    #print("Constraints:\n", partC)
    print("%d Constraints" % len(partC))

    constraints = make_constraints(partB, partC, arraySize)
    # decls, assumes, constraints

    decls = make_decls("../build/klee-last/solver-queries.kquery")

    make_query(qfile, decls, assumes, constraints)
