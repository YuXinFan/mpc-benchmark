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

def make_path_conds(path_conds_split):
    def cmp_id(l):
        return int(l[0])
    path_conds_split = sorted(path_conds_split, key = cmp_id)

    path_list = []
    path_dict = {}
    cur_idx = 1
    path_dict["path_conds"] = []
    #print(path_conds_split[-1])
    for path_cond_split in path_conds_split:
        if path_cond_split[0] == str(cur_idx):
            path_dict["path_conds"] =  path_dict["path_conds"] + [path_cond_split[1]]
        else:
            cur_idx += 1
            path_list.append(path_dict)
            path_dict = {} 
            path_dict["path_conds"] = []
    path_list.append(path_dict)
    # for i in path_list:
    #     print(i)
    print("Total Path: ", len(path_list))
    #print(path_list[-1])
    return path_list

def make_results(results_split, arr_size):
    def cmp_id(l):
        return int(l[0])
    def cmp_idx(l):
        return int(l[1])

    results_split = sorted(results_split, key = cmp_id)

    results_pathIDs_map = {}
    for i in range(0, int(len(results_split)/arr_size)):
        result_split = sorted(results_split[i*arr_size:(i+1)*arr_size], key = cmp_idx)
        result = [i[2] for i in result_split]
        result_str = " ".join(result)
        if result_str in results_pathIDs_map.keys():
            temp = results_pathIDs_map["result_str"]
            temp["path_id"] += [result_split[0][0]]
            results_pathIDs_map[result_str] += temp
        else:
            temp = {}
            temp["raw"] = result
            temp["path_id"] = [result_split[0][0]]
            results_pathIDs_map[result_str] = temp

    #for k in results_pathIDs_map.keys():
    #    print(k)
    #print("Total results: ", len(results_pathIDs_map))
    #k = results_pathIDs_map.items()
    return results_pathIDs_map

def make_declassifieds(declassifieds_split):
    def cmp_id(l):
        return int(l[0])
    def cmp_idx(l):
        return int(l[1])

    declassifieds_split = sorted(declassifieds_split, key = cmp_id)
    declassifieds = {}
    for path_id, declassified_id, _, _, val, expr in declassifieds_split:
        declassifieds.setdefault(declassified_id, []).append((path_id, val, expr))
    declassifieds_paths = {}
    for key in declassifieds.keys():
        pathID_declassified_map = {}
        for path_id, val, expr in declassifieds[key]:
            pathID_declassified_map.setdefault(path_id, []).append((val,expr))
        declassifieds_paths[key] = pathID_declassified_map

    for key in declassifieds_paths.keys():
        print(len(declassifieds_paths[key]))  
    return declassifieds_paths

def make_constraints(results_ids_map, path_conds, declassifieds):
    # sort by id 
    def cmp_id(l):
        return int(l[0])
    def cmp_idx(l):
        return int(l[1])
    def cmp_result(l):
        return l[1]

    pathId_result_map = {}
    for result in results_ids_map.keys():
        for path_id in results_ids_map[result]["path_id"]:
            pathId_result_map[path_id] = results_ids_map[result]["raw"]

    trace = {}
    for path_id in pathId_result_map.keys():
        trace[path_id] = {
            "result": pathId_result_map[path_id],
            "path_cond": path_conds[int(path_id)]["path_conds"]
        }
        for key in declassifieds.keys():
            trace[path_id][key] = declassifieds[key][path_id]
    
    print(trace["1"])



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

    path_conds_split = re.findall(r"\[\~State ID\]\[(\d+)\] \[PathCond\](\([\[\(0-9a-zA-Z\:\=\_\@\,\ \)\]]*\)|-?\d+)", content)
    print("Total Path Conditions Split: ", len(path_conds_split))

    results_split = re.findall(r"\[\~State ID\]\[(\d+)\] \[Array IDX\]\[(\d+)\] Expr\=(\([\[\(0-9a-zA-Z\:\=\_\@\,\ \)\]]*\)|-?\d+)", content)
    print("Total Result Split: ", len(results_split))

    # path_id, declassified_id, cur_declassified, total_declassified, value, expr
    declassifieds_split = re.findall(r"\[\~State ID\]\[(\d+)\] \[Declassified\]\[(\d+)\] \[(\d+)\/(\d+)\] (\d)\=\=(\([\[\(0-9a-zA-Z\:\=\_\@\,\ \)\]]*\)|-?\d+)", content)
    print("Total Declassified Split: ", len(declassifieds_split))
    print(declassifieds_split[0])
    # partA = re.findall(r"\[State ID] Assume:(\([\[\(0-9a-zA-Z\_\@\,\:\ \)\]]*\))", content)
    
    arraySize = re.findall(r"\[Array\] Size:(\d+)", content)
    # partB = re.findall(r"\[Part\-B\] id (-?\d+), array idx (\d+):(\([\[\(0-9a-zA-Z\:\=\_\@\,\ \)\]]*\)|-?\d+)", content)
    # partC = re.findall(r"\[Part\-C\] id (-?\d+), total (\d+), now (\d+)\-th:(\([\[\(0-9a-zA-Z\:\=\@\,\_\ \)\]]*\)|-?\d+) == (0|1)", content)
    # assumes = make_assumes(partA)
    # print("%d Assumes" % len(assumes))
    if arraySize == [] :
        arraySize = 0
    else:
        arraySize = int(arraySize[0])
    # print("%d Result Expr" %  (len(partB) if arraySize==0 else len(partB)/arraySize) )
    # print("%d Constraints" % len(partC))

    path_conds = make_path_conds(path_conds_split)

    results_ids_map = make_results(results_split, arraySize)

    declassifieds = make_declassifieds(declassifieds_split)

    constraints = make_constraints(results_ids_map, path_conds, declassifieds)
    # # decls, assumes, constraints

    # decls = make_decls("../build/klee-last/solver-queries.kquery")

    # make_query(qfile, decls, assumes, constraints)
