dados = "d, hornui 5, joao 3, thiago 4"

dic = {}
PI = ""
while PI != "S" :

    PI = input("NOME : +")
    if PI != "S" :
        
        PI = PI.replace(" ", "")
        PI = PI.split(":")
        PI[1] = int(PI[1]) 
        dic.update({PI[0] : PI[1]})

Sdic = sorted(dic.items(), key = lambda x:x[1])
Sdic = list(reversed(Sdic))
print([Sdic[i] for i in range(len(Sdic))])
