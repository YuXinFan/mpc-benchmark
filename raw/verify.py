import re
file1 = open("klee-out.txt","r+") 
content = file1.read()
content = content.replace("\t", " ")
content = content.replace("\n", " ")
content = content.replace("\r", " ")
content = content.replace("  ", " ")
#print (content)


def match(stream):
    regex = r"is (\d+), total (\d+), now (\d+)-th:\((.*)\) == (0|1) "
    
    match = re.search(regex, stream) 
    if match != None: 
        
        # We reach here when the expression "([a-zA-Z]+) (\d+)" 
        # matches the date string. 
        
        # This will print [14, 21), since it matches at index 14 
        # and ends at 21.  
        print("Match at index % s, % s" % (match.start(), match.end()))
        
        # We us group() method to get all the matches and 
        # captured groups. The groups contain the matched values. 
        # In particular: 
        # match.group(0) always returns the fully matched string 
        # match.group(1) match.group(2), ... return the capture 
        # groups in order from left to right in the input string 
        # match.group() is equivalent to match.group(0) 
        
        # So this will print "June 24" 
        print("Full match: % s" % (match.group(0)))
        # So this will print "June" 
        print("Result is: % s" % (match.group(1)))
        
        # So this will print "24" 
        print("Total is: % s" % (match.group(2)))
        print("Now is: % s" % (match.group(3)))
        print("Expr is: % s" % (match.group(4)).replace("  "," "))

        print("Value is: % s" % (match.group(5)))
        

        
    else: 
        print("The regex pattern does not match.")

def findall(stream):
    stream = re.split("Output", stream)
    for each in stream[1:]:
        match(each)
        print("\n")

def main():
    findall(content)

main()