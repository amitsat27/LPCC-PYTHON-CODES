print("Code Optimization Techniques Code")
file = open('input3add.txt')
code = file.readlines()
codelist = list()

print("Three address Code To Be Optimized : ")
for i in code:
    k = i.strip('\n')
    codelist.append(k)
    print("             "+k)
def deadcodeelimition(code_lines):
    first ,temp= '',0
    track = 0
    print("|*****   Dead Code Elimination   *****|")
    for i in code_lines:
        dce = list(i)
        try:
            if(len(dce)==3):
                
                if(type(eval(dce[len(dce)-1])) == int):
                    first = dce[0]
                    track = temp
                    code_lines.pop(track)
                temp =temp +1
            else:
                temp = temp + 1
        except:
            temp=temp+1
            continue
    for i in code_lines:
            print("             "+i)
    return code_lines

def subexelimination(code_lines):
    print("|*****  Sub Expression Elimination *****|")
    temp ,repl= 0,''
    second = code_lines[0][2:]
    second_f = code_lines[0][0]
    for j in code_lines:
        if(j[2:]==second and temp >0):
            repl = j[0]
            code_lines.pop(1)
        temp = temp +1
    for j in range(len(code_lines)):
        for d in code_lines[j][2:]:
            if(d==repl):
                code_lines[j] = code_lines[j].replace(repl,second_f)
    for i in code_lines:
            print("             "+i)    
    return code_lines
         
def strengthreduction(code_lines):
    print("|*****   Strength Reduction   *****|")
    for j in range(len(code_lines)):
        for d in code_lines[j][2:]:
            if(d=='^'):
                code_lines[j] = code_lines[j].replace(code_lines[j][2:],code_lines[j][2:][0]+"*"+code_lines[j][2:][0])
    
    for i in code_lines:
            print("             "+i)  
    return code_lines  

def compiletimeval(code_lines):
    print("|*****    Compile Time Evaluation   *****|")
    for j in range(len(code_lines)):
        try:
            exp = eval(code_lines[j][2:])
            code_lines[j] = code_lines[j].replace(code_lines[j][2:],str(exp))
            constantprop = code_lines[j][0]
        except:
            continue
    for j in range(len(code_lines)):
        for d in code_lines[j][2:]:
            if(d==constantprop):
                code_lines[j] = code_lines[j].replace(constantprop,str(exp))
    for i in code_lines:
            print("             "+i)
        
    return code_lines
 
codelist = compiletimeval(codelist)
codelist = deadcodeelimition(codelist)
codelist = subexelimination(codelist)
codelist = strengthreduction(codelist)

print("|******* Final Optimized Code *******|")
for i in codelist:
    print("             "+i)