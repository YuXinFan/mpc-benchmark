import re
import os
file1 = open("klee-out.txt","r+") 
content = file1.read()
content = content.replace("\t", " ")
content = content.replace("\n", " ")
content = content.replace("\r", " ")
content = content.replace("  ", " ")
#print (content)

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
    if len(l) == 1:
        return "(Eq %s %s)\n" % (l[0][1], l[0][0])
    else:
        andcat = ""
        lbracket = 0
        for i in range(0, len(l)-1):
            andcat  = andcat + "(And " + "(Eq %s %s)\n" % (l[i][1], l[i][0]) + " "
            lbracket = lbracket + 1
        andcat = andcat + "(Eq %s %s)\n" % (l[len(l)-1][1], l[len(l)-1][0]) + ")"*lbracket
        return andcat 


def make_assumes(part):
    return ["(Eq 1 %s)\n" % x for x in part]

def make_constraints(partB, partC):
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
        for i in range(0, len(sorted_parts), 4):
            part = sorted(sorted_parts[i:i+4], key=cmp_idx)
            if part[0][0] in id_exprs_map.keys():
                print("morethan 4:", part[0][0])
                #exit("more then 4")
            else:
                id_exprs_map[part[0][0]] = []
                ret =", ".join([x[2] for x in part])
                if ret in ret_ids_map.keys():
                    ret_ids_map[ret].append(part[0][0])
                else:
                    ret_ids_map[ret] = [part[0][0]]
    print("%d different results" % len(ret_ids_map.keys()))
    print(ret_ids_map)

    # id --> multi-constraints
    for i in partC:
        id_exprs_map[i[0]].append((i[3],i[4]))
    
    ret_exprs_map = {}
    for ret in ret_ids_map.keys():
        all_exprs = [x for id in ret_ids_map[ret] for x in id_exprs_map[id]]
        const_expr = "(Not " + AndCat(all_exprs) + ")"    
        ret_exprs_map[ret] = const_expr
    # ret expr --> constraints
    return ret_exprs_map



def make_query(decls, assumes, constraints):
    folder = "./verifies"
    if not os.path.isdir(folder):
        os.mkdir(folder)
    kquery = decls 
    assumes = " ".join(assumes)
    qIdx = 0
    for ret_expr in constraints.keys():
        kquery = kquery + "\n# query %d, ret expr %s\n" % (qIdx, ret_expr) \
             + "(query [ " + assumes + "]\n" \
             + constraints[ret_expr] + ")" 
        qIdx = qIdx + 1
    file_name = "query.kquery"
    w = open(folder+"/"+file_name, "w+")
    w.write(kquery)
    w.close()
    #cmd = "kleaver %s/%s" % (folder, file_name)
    #os.system(cmd)

def main():
    #decls = load_decls()
    decls = ""
    isArray = False
    partA = re.findall(r"\[Part\-A\] Assume:(\([\(0-9a-zA-Z\_\ \)]*\))", content)
    assumes = make_assumes(partA)
    print("Assumes:\n", partA)
    partB = re.findall(r"\[Part\-B\] id (-?\d+), array idx (\d+):(\([\(0-9a-zA-Z\_\ \)]*\)|-?\d+)", content)
    #print(partB)[Part-C] id 1502742394, total 6, now 1-th:(ZExt w32 (Extract 0 (
    print("Array:\n",partB)
    partC = re.findall(r"\[Part\-C\] id is (-?\d+), total (\d+), now (\d+)\-th:(\([\(0-9a-zA-Z\_\ \)]*\)|-?\d+) == (0|1)", content)
    print("Constraints:\n", partC)
    constraints = make_constraints(partB, partC)
    #assumes = load_assumes()
    #print(partC)
    print(assumes)
    # decls, assumes, constraints
    make_query(decls, assumes, constraints)
    #constraints = load_constraints(splits[1:])
    #gen_queries(decls, assumes, constraints)

main()