import re
import os
import timeit
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

def make_decls(path, symbolics):
    fs = open(path, "r+")
    kqs = fs.read()
    kq = kqs.split("# Query")[-1]
    lines = kq.split("\n")
    decl = ""
    for line in lines:
        if "array" in line:
            decl = decl + line + "\n"
    decl_prime = decl.replace("array", "*****")
    decl_prime = decl_prime.replace("symbolic", "&&&&&")

    for sym in symbolics:
        decl_prime = decl_prime.replace(sym, sym+"_")
    
    decl_prime = decl_prime.replace("*****", "array")
    decl_prime = decl_prime.replace("&&&&&", "symbolic")

    print(decl)
    print(decl_prime)
    return decl + decl_prime
def make_assumes(part):
    l = ["(Eq 1 %s)" % m for m in part]
    # for x in part:
    #     if "N0:(ReadLSB w32 0 arr) N1:" in x:
    #         print(x)
    #     #m = find_and_replace_label_def(x)
    #     l.append("(Eq 1  %s)\n" % m)
    return "\n".join(l) 

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
        path_cond_split_ = path_cond_split[1]
        if "model_version" in path_cond_split_:
            path_cond_split_ = "true"
        if path_cond_split[0] == str(cur_idx):
            path_dict["path_conds"] =  path_dict["path_conds"] + [path_cond_split_]
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
    print(results_split)
    print(arr_size)
    results_pathIDs_map = {}
    for i in range(0, int(len(results_split)/arr_size)):
        result_split = sorted(results_split[i*arr_size:(i+1)*arr_size], key = cmp_idx)
        result = [j[2] for j in result_split]
        result_str = " ".join(result)
        if result_str in results_pathIDs_map.keys():
            temp = results_pathIDs_map[result_str]["path_id"]
            temp += [result_split[0][0]]
            results_pathIDs_map[result_str]["path_id"] = temp
        else:
            temp = {}
            temp["raw"] = result
            temp["path_id"] = [result_split[0][0]]
            results_pathIDs_map[result_str] = temp

    #for k in results_pathIDs_map.keys():
    #    print(k)
    print("Total results: ", len(results_pathIDs_map.keys()))
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
        expr = "true" if expr == "1" else "false" if expr == "0" else expr  
        val = val if (expr != "true" and expr != "false") else "true" if val == "1" else "false"
        declassifieds.setdefault(declassified_id, []).append((path_id, val, expr))
    declassifieds_paths = {}
    for key in declassifieds.keys():
        pathID_declassified_map = {}
        for path_id, val, expr in declassifieds[key]:
            pathID_declassified_map.setdefault(path_id, []).append((val,expr))
        declassifieds_paths[key] = pathID_declassified_map

    print("Total deciassifieds ", len(declassifieds_paths.keys()))  
    return declassifieds_paths

def make_trace(results_ids_map, path_conds, declassifieds):

    pathId_result_map = {}
    for result in results_ids_map.keys():
        for path_id in results_ids_map[result]["path_id"]:
            pathId_result_map[path_id] = results_ids_map[result]["raw"]

    trace = {}
    for path_id in pathId_result_map.keys():
        trace[path_id] = {
            "result": pathId_result_map[path_id],
            "path_cond": path_conds[int(path_id)-1]["path_conds"]
        }
        for key in declassifieds.keys():
            if path_id in declassifieds[key].keys():
                trace[path_id][key] = declassifieds[key][path_id]
            else:
                trace[path_id][key] = [("true", "false")]
    
    return trace 

def ListAndCat(list):
    if len(list) == 0:
        pass 
    elif len(list) == 1:
        return list[0]
    else:
        return " (And " + list[0] + ListAndCat(list[1:]) + " ) "
def make_constraints(trace, symbolics):
    const = []
    import copy
    trace_prime = copy.deepcopy(trace)
    path_id_list = list(trace.keys())
    for i in range(len(path_id_list)):
        path_id = path_id_list[i]
        result = trace_prime[path_id]["result"]
        path_cond = trace_prime[path_id]["path_cond"]
        for sym in symbolics:
            for j in range(len(result)):
                result[j] = result[j].replace(sym, sym+"_")
            for j in range(len(path_cond)):
                path_cond[j] = path_cond[j].replace(sym, sym+"_")
        trace_prime[path_id]["result"] = result
        trace_prime[path_id]["path_cond"] = path_cond 
        num_declass = len(trace_prime[path_id].keys()) - 2 
        for k in range(num_declass):
            declass = trace_prime[path_id][str(k)]
            for sym in symbolics:
                declass = [(val, expr.replace(sym, sym+"_")) for val, expr in declass]
            trace_prime[path_id][str(k)] = declass 
    #print(trace["1"]["path_cond"])
    for i in range(len(path_id_list)):
        for j in range(i+1,len(path_id_list)):
            path_id1 = path_id_list[i]
            path_id2 = path_id_list[j]

            path_cond1 = trace[path_id1]["path_cond"]
            path_cond1_andcat = ListAndCat(path_cond1)
            result1 = trace[path_id1]["result"]

            path_cond2_prime = trace_prime[path_id2]["path_cond"]
            path_cond2_andcat_prime = ListAndCat(path_cond2_prime)
            result2_prime = trace_prime[path_id2]["result"]
            result_const = []
            filted = False
            for x,y in zip(result1, result2_prime):
                if (x.isdigit() and y.isdigit()) and (x != y):
                    filted = True 
            if filted:
                continue
            result_const = ["(Eq w32 (w32 %s) (w32 %s))" % (x, y) if x.isdigit() and y.isdigit() else "(Eq %s %s )" % (x,y) for x,y in zip(result1,result2_prime)]
            result_andcat = ListAndCat(result_const)
            left_const = ListAndCat([path_cond1_andcat, path_cond2_andcat_prime,  result_andcat])

            num_declassify = len(trace[path_id1].keys())-2
            for kk in range(num_declassify):
                declassify1 = trace[path_id1][str(kk)]
                declassify2_prime = trace_prime[path_id2][str(kk)]
                #declassify1 = ["(Eq %s %s)" % (x,y) for x,y in declassify1]
                declassify1 = [y for x,y in declassify1]
                #declassify2_prime = ["(Eq %s %s)" % (x,y) for x,y in declassify2_prime]
                declassify2_prime = [y  for x,y in declassify2_prime]
                declassify = ["(Eq %s %s)" % (x,y) for x,y in zip(declassify1, declassify2_prime)]
                declassify_andcat = ListAndCat(declassify)
                if len(const) == kk:
                    const.append([])
                const[kk].append("(Or (Not %s) %s)" % (left_const, declassify_andcat))
    return const


def make_query(file_name, decls, assumes, const):
    folder = "../log"
    if not os.path.isdir(folder):
        os.mkdir(folder)
    kquery = decls 
    for i in range(len(const)):
        w = open(folder+"/"+file_name+str(i), "w+")
        w.write(decls)
        qIdx = 0
        print("Making %d-th Kquery file" % i)
        for expr in const[i]:
            qIdx = qIdx + 1
            qLine = "\n# query %d\n" % qIdx + "(query [ " + assumes + " ]\n" + expr + " )"
            w.write(qLine)
        w.close()
        kquery = decls

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

    assumes_split = re.findall(r"\[\~Assume\]:(\([\[\(0-9a-zA-Z\:\=\_\@\,\ \)\]]*\)|-?\d+)", content)
    print("%d Assumes" % len(assumes_split))

    symbolics = re.findall(r"\[\~Make Symbolic\] ([0-9a-zA-Z\_]*)\:", content)
    for i in symbolics:
        print("Make symbolic", i)

    path_conds_split = re.findall(r"\[\~State ID\]\[(\d+)\] \[PathCond\](\([\[\(0-9a-zA-Z\:\=\_\@\,\ \)\]]*\)|-?\d+)", content)
    print("Total Path Conditions Split: ", len(path_conds_split))

    results_split = re.findall(r"\[\~State ID\]\[(\d+)\] \[Array IDX\]\[(\d+)\] Expr\=(\([\[\(0-9a-zA-Z\:\=\_\@\,\ \)\]]*\)|-?\d+)", content)
    print("Total Result Split: ", len(results_split))

    # path_id, declassified_id, cur_declassified, total_declassified, value, expr
    declassifieds_split = re.findall(r"\[\~State ID\]\[(\d+)\] \[Declassified\]\[(\d+)\] \[(\d+)\/(\d+)\] (\d)\=\=(\([\[\(0-9a-zA-Z\:\=\_\@\,\ \)\]]*\)|-?\d+)", content)
    print("Total Declassified Split: ", len(declassifieds_split))
    
    arraySize = re.findall(r"\[Array\] Size:(\d+)", content)
    assumes = make_assumes(assumes_split)
    if arraySize == [] :
        arraySize = 1
    else:
        arraySize = int(arraySize[0])

    path_conds = make_path_conds(path_conds_split)

    results_ids_map = make_results(results_split, arraySize)

    declassifieds = make_declassifieds(declassifieds_split)

    traces = make_trace(results_ids_map, path_conds, declassifieds)
    print("Numer of Trace: ", traces.keys())

    # # decls, assumes, constraints

    const = make_constraints(traces, symbolics)
    print("Numer of declassified:", len(const))
    for i in const:
        print("Number of query of deciassified ", len(i))
    decls = make_decls("../build/klee-last/solver-queries.kquery", symbolics)
    print("Make Decl Done")

    make_query(qfile, decls, assumes, const)
    return len(const)
