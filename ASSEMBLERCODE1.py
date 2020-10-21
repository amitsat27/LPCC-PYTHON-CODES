import re
from prettytable import PrettyTable
LC = 0
tokens = list()
code = open("ALPCODE_1a.txt",encoding="utf-8")
line = code.readlines()
for i in line:
    k = i.rstrip('\n')
    k = re.split(' |,',k)
    tokens.append(k)
    
for i in tokens:
    for j in i:
        if(j==''):
            i.remove(j)
final_tokens = [x for x in tokens if x!=[]]

MOT = ['STOP','ADD','MULT','MOVER','MOVEM','COMP','BC','DIV','TRANS',
      'READ','PRINT','START','END','ORIGIN','EQU','LTORG','DS','STORE',
       'DC','AREG','BREG','CREG','EQ','LT','GT','LE','GE','NE','ANY','LOAD','SUB']
fdict = dict()
LC = int(final_tokens[0][1])
sym_index = 0
for i in range(1,len(final_tokens)):
    if(final_tokens[i][0] not in MOT):
        if(final_tokens[i][1]!='EQU'):
            key = final_tokens[i][0]
            if key in fdict.keys():
                fdict[final_tokens[i][0]][0]=LC
            else:
                fdict[final_tokens[i][0]]=[LC,sym_index]
                sym_index = sym_index+1
            st = final_tokens[i][-1]
            if(st not in fdict.keys()):
                r = re.search("[A-Z]+",st)
                if(final_tokens[i][-1] not in MOT and bool(r) ):
                    fdict[final_tokens[i][-1]]=[0,sym_index]
                    sym_index = sym_index+1
            LC=LC+1
        elif(final_tokens[i][1]=='EQU'):
            p=final_tokens[i][2]
            if(len(p)<1):
                fdict[final_tokens[i][0]][0]=fdict[p][0]
            else:
                p=re.split("\+|-",p)
                x = p[0]
                globals()[x] = fdict[p[0]][0]
                LC1 = eval(final_tokens[i][2])
                fdict[final_tokens[i][0]][0]=LC1
    elif(final_tokens[i][0]!='ORIGIN'):
        st = final_tokens[i][-1]
        r = re.search("[A-Z]+",st)
        if(final_tokens[i][-1] not in MOT and bool(r)):
            fdict[final_tokens[i][-1]]=[0,sym_index]
            sym_index = sym_index+1
        LC=LC+1
    elif(final_tokens[i][0]=='ORIGIN' ):
        p=final_tokens[i][1]
        if(len(p)<1):
            LC=fdict[p][0]
        else:
            p=re.split("\+|-",p)
            x = p[0]
            globals()[x] = fdict[p[0]][0]
            LC = eval(final_tokens[i][1])
symtab = PrettyTable(['INDEX NO.','SYMBOL','ADDRESS'])
print("SYMBOL TABLE")
for s,a in fdict.items():
    symtab.add_row([a[1],s,a[0]])
print(symtab)