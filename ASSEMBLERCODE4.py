LC = 0
tokens = list()
code = open("ALPCODE.txt",encoding="utf-8")
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
      'READ','PRINT','START','END','ORIGIN','EQU','LTORG','DS','STORE','BC',
       'DC','AREG','BREG','CREG','EQ','LT','GT','LE','GE','NE','ANY','LOAD','SUB']
MOT_IC = {'STOP':['IS','00'],'ADD':['IS','01'],'MULT':['IS','03'],'SUB':['IS','02'],
         'MOVER':['IS','04'],'MOVEM':['IS','05'],'COMP':['IS','06'],'BC':['IS','07'],
         'DIV':['IS','08'],'READ':['IS','09'],'PRINT':['IS','10'],'START':['AD','01'],
         'END':['AD','02'],'ORIGIN':['AD','03'],'EQU':['AD','04'],'LTORG':['AD','05'],
         'DS':['DL','01'],'AREG':['RG','01'],'BREG':['RG','02'],'DC':['DL','02'],
         'CREG':['RG','03'],'EQ':['CC','01'],'LT':['CC','02'],'GT':['CC','03'],
         'LE':['CC','04'],'GE':['CC','05'],'NE':['CC','06'],'ANY':['CC','07']}
fdict_sym,fdict_lit = dict(),dict()
flist,plist =  list(),list()
sym_indexc,lit_indexc,pool_variable = 0,0,0


symtab = PrettyTable(['INDEX NO.','SYMBOL','ADDRESS'])
littab = PrettyTable(['INDEX NO.','LITERAL','ADDRESS'])
pooltab = PrettyTable(['LITERAL NUMBER'])
intmcode = PrettyTable(['INTERMEDIATE CODE'])
LC = int(final_tokens[0][1])
# print(final_tokens)
for i in range(1,len(final_tokens)):
    m = re.search("(=(‘[0-9]+’))",final_tokens[i][-1])
    s=""
    if(final_tokens[i][0]!='END'):
        if(final_tokens[i][0]!='LTORG'):
            if(final_tokens[i][0] not in MOT and  m!=None ):
                if(final_tokens[i][1]!='EQU'):
                    key = final_tokens[i][0]
                    if key in fdict_sym.keys():
                        fdict_sym[final_tokens[i][0]][0]=LC
                    else:
                        fdict_sym[final_tokens[i][0]]=[LC,sym_indexc]
                        sym_indexc = sym_indexc + 1
                    if m.group() not in fdict_lit.keys():
                        fdict_lit[final_tokens[i][-1]]=[0,lit_indexc]
                        lit_indexc = lit_indexc + 1
                    LC=LC+1
                elif(final_tokens[i][1]=='EQU'):
                    p=final_tokens[i][2]
                    if(len(p)<1):
                            fdict_sym[final_tokens[i][0]][0]=fdict_sym[p[0]][0]
                    else:
                        p=re.split("\+|-",p)
                        x = p[0]
                        globals()[x] = fdict_sym[p[0]]
                        LC1 = eval(final_tokens[i][2])
                        fdict_sym[final_tokens[i][0]]=LC1
            elif(final_tokens[i][0] not in MOT ):
                if(final_tokens[i][1]!='EQU'):
                    key = final_tokens[i][0]
                    if key in fdict_sym.keys():
                        fdict_sym[final_tokens[i][0]][0]=LC
                    else:
                        fdict_sym[final_tokens[i][0]]=[LC,sym_indexc]
                        sym_indexc = sym_indexc + 1
                    LC=LC+1
                elif(final_tokens[i][1]=='EQU'):
                    p=final_tokens[i][2]
                    if(len(p)<1):
                            fdict_sym[final_tokens[i][0]][0]=fdict_sym[p][0]
                    else:
                        p=re.split("\+|-",p)
                        x = p[0]
                        globals()[x] = fdict_sym[p[0]][0]
                        LC1 = eval(final_tokens[i][2])
                        fdict_sym[final_tokens[i][0]][0]=LC1
            elif(m!=None):
                fdict_lit[m.group()] =[0,lit_indexc]
                lit_indexc = lit_indexc + 1
                LC=LC+1
            elif(final_tokens[i][0]=='ORIGIN'):
                p=final_tokens[i][1]
                if(len(p)<1):
                    fdict_sym[final_tokens[i][0]][0]=fdict_sym[p][0]
                else:
                    p=re.split("\+|-",p)
                    x = p[0]
                    globals()[x] = fdict_sym[p[0]][0]
                    LC = eval(final_tokens[i][1])      
            elif(final_tokens[i][0]!='ORIGIN'):
                st = final_tokens[i][-1]
                if(st not in fdict_sym.keys()):
                    r = re.search("[A-Z]+",st)
                    if(final_tokens[i][-1] not in MOT and bool(r) ):
                        fdict_sym[final_tokens[i][-1]]=[0,sym_indexc]
                        sym_indexc = sym_indexc + 1
                LC=LC+1
        else:
            pooltab.add_row([pool_variable])
            plist.append(pool_variable)
#             print(fdict_lit,LC)
            for key in fdict_lit.keys():
                fdict_lit[key][0] = LC
                LC = LC+1
            for l,a in fdict_lit.items():
                littab.add_row([a[1],l,a[0]])
                flist.append([a[1],l,a[0]])
                pool_variable = pool_variable+1
            fdict_lit.clear()
    else:
        if bool(fdict_lit):
            pooltab.add_row([pool_variable])
            plist.append(pool_variable)
        for key in fdict_lit.keys():
            fdict_lit[key][0] = LC
            LC = LC+1
            

print("SYMBOL TABLE")
for s,a in fdict_sym.items():
    symtab.add_row([a[1],s,a[0]])
print(symtab)
print("LITERAL TABLE")
for l,a in fdict_lit.items():
    littab.add_row([a[1],l,a[0]])
    flist.append([a[1],l,a[0]])
print(littab)
print("POOL TABLE")
print(pooltab)
lit_track_1,lit_track_2 = 0,0
#INTERMEDIATE CODE GENERATION
for i in range(len(final_tokens)):
    code = ""
    for j in range(len(final_tokens[i])):
        m = re.search("(=(‘[0-9]+’))",final_tokens[i][j])
        if final_tokens[i][j] in MOT and final_tokens[i][j]!='END':
            if final_tokens[i][j] != 'LTORG':
                if(final_tokens[i][j]=='DC'):
                    print(1)
                code = code + '(' + MOT_IC[final_tokens[i][j]][0] + ',' + MOT_IC[final_tokens[i][j]][1] + ')'
            else:
                if(lit_track_2 != len(plist)-1):
                    for h in range(plist[lit_track_2],plist[lit_track_2 + 1]):
                        if(h==plist[lit_track_2 + 1]-1):
                            code = code + '(' + MOT_IC[final_tokens[i][j]][0] + ',' + MOT_IC[final_tokens[i][j]][1] + ')'+'(' + 'DL' + ',' + '02' +')' + '(' + 'C'+','+flist[h][1][2]+')'    
                        else:
                            code = code + '(' + MOT_IC[final_tokens[i][j]][0] + ',' + MOT_IC[final_tokens[i][j]][1] + ')'+'(' + 'DL' + ',' + '02' +')' + '(' + 'C'+','+flist[h][1][2]+')' + '\n'
                    lit_track_2 = lit_track_2 + 1 
        elif(final_tokens[i][j] not in MOT):
            ks = final_tokens[i][j]
            p=re.split("\+|-",ks)
            if ks in fdict_sym.keys():
                code = code + '(' + 'S' + ',' + str(fdict_sym[final_tokens[i][j]][1]) + ')'
            elif(len(p)>1):
                x=p[0]
                globals()[x] = fdict_sym[p[0]][0]
                e= eval(final_tokens[i][j])
                code = code + '(' + 'C' + ',' + str(e) + ')'
            elif(len(p)==1 and m==None):
                code = code + '(' + 'C' + ',' + str(p[0]) + ')'
            elif(m!=None):
                code = code + '(' + 'L' + ',' + str(flist[lit_track_1][0]) + ')'
                lit_track_1 = lit_track_1 + 1
        elif(final_tokens[i][j] == 'END'):
            code = code + '(' + MOT_IC[final_tokens[i][j]][0] + ',' + MOT_IC[final_tokens[i][j]][1] + ')'+'(' + 'DL' + ',' + '02' +')' + '(' + 'C'+','+flist[plist[lit_track_2]][1][2]+')'    
            
                
        
    intmcode.add_row([code])
intmcode.align['INTERMEDIATE CODE'] = "l"
print(intmcode)