#AA - tema 2: Algoritmi genetici

import copy
import random
import math

#preluarea inputului

# dim = int(input("Introduceti dimensiunea populatiei: \n"))
# inf = int(input("Introduceti limita inferioara a domeniului de definitie al functiei: \n"))
# sup = int(input("Introduceti limita superioara a domeniului de definitie al functiei: \n"))
# a = int(input("Introduceti parametrul a al functiei de maximizat: \n"))
# b = int(input("Introduceti parametrul b al functiei de maximizat: \n"))
# c = int(input("Introduceti parametrul c al functiei de maximizat: \n"))
# prec = int(input("Introduceti precizia cu care se discretizeaza intervalul: \n"))
# pIncr = float(input("Introduceti probabilitatea de incrucisare: \n"))
# pMut = float(input("Introduceti probabilitatea de incrucisare: \n"))
# etape = int(input("Introduceti numarul de etape: \n"))

dim = 20
inf = -1
sup = 2
a = -1
b = 1
c = 2
prec = 6
pIncr = 0.25
pMut = 0.01
etape = 30

#deschiderea fisierului in care sunt evidentiate operatiile din prima etapa a algoritmului

output = open("Evolutie.txt", "w")

#definirea variabilelor suport

#lungimea cromozomilor, conform formulei din curs
lenCrom = math.ceil(math.log2((sup-inf)*(10**prec)))

#definirea functiilor pe care le voi utiliza: cea de maximizare, binary search

def f(x, a, b, c): # functia de fitness, chiar f
    return a * (x**2) + b * x + c


def decode(x):
    return (int(str(x),2) * ((sup -inf) / ((2**lenCrom) - 1))) + int(inf)


#generarea populatiei initiale
def generateInitial(dim, inf, sup, prec):
        return [("".join([str(random.randint(0,1)) for x in range(lenCrom)])) for i in range(dim)]

#lista cu valorile decodate
def decodeInit(initial):
    return [decode(x) for x in initial]

#lista cu f-urile, aplicand f asupra valorilor decodate
def applyF(initial):
    return [f(round(x, prec), a, b, c) for x in initial]

#afiseaza populatia initiala
def printPopInit(dim,init, dec, a_f):
    output.write("Populatia initiala: \n")
    for i in range(dim):
        output.write(str(i + 1) + ": " + str(init[i]) + " x = " + str(dec[i]) + " f = " + str(a_f[i]) + "\n")

#returneaza lista cu prob de selectie
def getProbSel(a_f):
    F = sum(a_f)
    return [x/F for x in a_f]

#afis prob de selectie pentru fiecare cromozom
def afisProbSel(dim, probSel):
    for i in range(dim):
        output.write("cromozom    " + str(i+1) + " probabilitate " + str(probSel[i]) + "\n")


#returneaza lista cu intervalele de selectie, utilizand lista cu prob de selectie
def getIntSel(probSel):
    ans = [0]
    aux = 0
    for p in probSel:
        aux += p
        ans.append(aux)
    return ans


def binarySearch(u, v, st, dr):  # cautarea binara pentru a gasi intervalul potrivit pentru un u dat
    global last
    while st <= dr:
        mij = (st + dr) // 2
        if v[mij] <= u:
            last = mij
            st = mij + 1
        elif v[mij] > u:
            dr = mij - 1
    return last + 1

#inlocuieste bitii lui A cu cei ai lui B pana la punctul de ruptura
def swapCrom(cromA, cromB, punct, lenCrom):
    newA = []
    for i in range(punct):
        newA.append(cromB[i])
    for i in range(punct, lenCrom):
        newA.append(cromA[i])

    return "".join(newA)

#schimba valoarea unui bit
def changeBit(bit):
    return str(1 - int(bit))

#returneaza indicele cromozomului cu f ul cel mai mare
def getFittest(a_f, dim):
    max = a_f[0]
    ind = 0
    for i in range(1,dim):
        if a_f[i] > max:
            max = a_f[i]
            ind = i
    return ind

#returneaza indicele cromozomului cu f ul cel mai mic
def getWorst(a_f, dim):
    min = a_f[0]
    ind = 0
    for i in range(1,dim):
        if a_f[i] < min:
            min = a_f[i]
            ind = i
    return ind

#lista in care retin valorile binare (genele cromozomilor)
init = []

for i in range(etape):
    if(i == 0):
        #la etapa 1, voi genera populatia initiala; altfel, va fi pop anterioara
        init = generateInitial(dim, inf, sup, prec)
    dec = decodeInit(init) #lista cu valorile decodate din init
    a_f = applyF(dec) #lista cu f urile valorilor decodate

    #aflu probabilitatea de selectie pentru fiecare cromozom
    probSel = getProbSel(a_f)

    if(i == 0): #suntem la etapa 1, afisez prob de selectie
        printPopInit(dim,init,dec,a_f)
        output.write("Probabilitati selectie\n")
        afisProbSel(dim, probSel)

    #retin intervalele de selectie in InterSel
    InterSel = getIntSel(probSel)

    if(i == 0): #pentru etapa 1, afisez intervalele de selectie
        output.write("Intervale probabilitati selectie ")
        for x in InterSel:
            output.write(str(x) + " ")
        output.write("\n")

    #in selected retin tupluri (valoare random generata, cromozom in functie de intervalul de selectie corespunzator)
    selected = []
    for z in range(dim):
        u = random.random()
        #print(str(i) + " " + str(u))
        selected.append((u,binarySearch(u, InterSel, 0, dim)))

    if(i == 0):
        for x in selected:
            output.write("u = " + str(x[0]) + " selectam cromozomul " + str(x[1]) + "\n")

    #listele pentru noua populatie
    new_init = []
    new_dec = []
    new_a_f = []

    if(i == 0): #pentru prima etapa, trebuie sa le afisez, pe parcurs
        output.write("Dupa selectie:\n")
        for j in range(dim):
            output.write(str(j+1) + ": " + str(init[selected[j][1] - 1]) + " x= " + str(dec[selected[j][1] - 1]) + " f= " + str(a_f[selected[j][1] - 1]) + "\n")
            new_init.append(init[selected[j][1] - 1])
            new_dec.append(dec[selected[j][1] - 1])
            new_a_f.append(a_f[selected[j][1] - 1])
    else:
        for j in range(dim):
            new_init.append(init[selected[j][1] - 1])
            new_dec.append(dec[selected[j][1] - 1])
            new_a_f.append(a_f[selected[j][1] - 1])

    if(i == 0):
        output.write("Probabilitate incrucisare " + str(pIncr) + "\n")

    selectedIncr = [] #retin cromozomii pe care ii voi recombina
    for j in range(dim):
        u = random.random()
        if(i == 0):
            output.write(str(j+1) + ": " + str(init[selected[j][1] - 1]) + " u =" + str(u))
        if (pIncr > u):
            if(i == 0):
                output.write("<0.25 participa" + "\n")
            selectedIncr.append(j + 1)
        else:
            if (i == 0):
                output.write("\n")
            #selectedIncr.append(j+1) #index ul din selected

    nrRecomb = len(selectedIncr) #numarul crom pe care ii voi recombina
    if(nrRecomb % 2 == 1): selectedIncr.pop() #daca e impar, nu il voi lua in considerare pe ultimul selectat
    nrRecomb = len(selectedIncr)

    for index in range(0,nrRecomb,2):
        pct_rupere = random.randrange(0, lenCrom) #aleg un punct de rupere random pe lungimea cromozomului
        if(i == 0):
            output.write("Recombinare dintre cromozomul " + str(selectedIncr[index]) + " cu cromozomul " + str(selectedIncr[index + 1]) + "\n")
            output.write(str(new_init[selectedIncr[index] - 1]) + " " + str(new_init[selectedIncr[index + 1] - 1]) + " punct " + str(pct_rupere) + "\n")
        #actualizez valorile cromozomilor din toate listele pop noi
        cromA = new_init[selectedIncr[index] - 1]
        cromB = new_init[selectedIncr[index + 1] - 1]
        new_init[selectedIncr[index] - 1] = swapCrom(cromA, cromB, pct_rupere,lenCrom)
        new_init[selectedIncr[index + 1] - 1] = swapCrom(cromB, cromA, pct_rupere, lenCrom)
        new_dec[selectedIncr[index] - 1] = decode( new_init[selectedIncr[index] - 1])
        new_dec[selectedIncr[index + 1] - 1] = decode(new_init[selectedIncr[index + 1] - 1])
        new_a_f[selectedIncr[index] - 1] = f(new_dec[selectedIncr[index] - 1],a,b,c)
        new_a_f[selectedIncr[index + 1] - 1] = f(new_dec[selectedIncr[index + 1] - 1], a, b, c)
        if(i == 0): #pentru etapa 1, afisez rezultatul recombinarii
            output.write("Rezultat    " + str(new_init[selectedIncr[index] - 1]) + " " + str(new_init[selectedIncr[index + 1] - 1]) + "\n")


    #afisez din nou cromozomii : gene val_decodata f
    if(i == 0):
        output.write("Dupa recombinare:\n")
        for z in range(dim):
            output.write(str(z + 1) + ": " + str(new_init[z]) + " x = " + str(new_dec[z]) + " f = " + str(new_a_f[z]) + "\n")

    if(i == 0):
        output.write("Probabilitate mutatie pentru fiecare gena " + str(pMut) + "\n")
        output.write("Au fost modificati cromozomii: \n")

        for z in range(dim):
            u = random.random()
            if u < pMut:
                poz = random.randrange(lenCrom-1) #aleg o pozitie random pe lung cromozomului
                aux = list(new_init[z])
                aux[poz] = changeBit(new_init[z][poz]) #schimb valoarea bitului
                new_init[z] = "".join(aux)

                new_dec[z] = decode(new_init[z])
                new_a_f[z] = f(new_dec[z], a, b, c)
                if i == 0:
                    output.write(str(z + 1) + "\n")

    #afisez din nou cromozomii dupa mutatie
    if (i == 0):
        output.write("Dupa mutatie:\n")
        for z in range(dim):
            output.write(str(z + 1) + ": " + str(new_init[z]) + " x = " + str(new_dec[z]) + " f = " + str(new_a_f[z]) + "\n")


    #selectie de tip elitist: inlocuiesc cromozomul cu worst f din pop noua cu cromozomul cu fittest f din pop veche
    index_best_pop_veche = getFittest(a_f, dim)
    index_worst_pop_noua = getWorst(new_a_f, dim)

    #actualizez valoarea din pop noua
    new_init[getWorst(new_a_f, dim)] = init[index_best_pop_veche]
    new_dec[ index_worst_pop_noua] = dec[index_best_pop_veche]
    new_a_f[index_worst_pop_noua] = a_f[index_best_pop_veche]

    #afisez evolutia maximului si mediei
    if (i == 0):
        output.write("Evolutia maximului\n") #maxim mediu
    output.write(str(new_a_f[getFittest(new_a_f, dim)]) + " " + str(sum(new_a_f) / dim) + "\n")

    #trecerea la urmatoarea populatie
    init = copy.deepcopy(new_init )










