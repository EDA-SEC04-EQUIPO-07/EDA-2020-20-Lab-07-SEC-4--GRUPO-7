from DISClib.DataStructures import heap as hp
from DISClib.DataStructures import liststructure as lt
from DISClib.DataStructures import listiterator as it

#____________________________________________
#Implementacion usando funciones heap
#____________________________________________

def heapsort(heap):
    """
    Algoritmo Heapsort implementado.
    """
    #construccion maxHeap
    size=hp.size(heap)
    mid=int(hp.size(heap))//2
    cmpfunction=heap['cmpfunction']
    i=mid
    while i in range(1,mid+1):
        lst=heap['elements']
        rs=i*2
        ls=i*2+1
        root=lt.getElement(lst,i)
        Right_son=lt.getElement(lst, rs)
        Left_son=lt.getElement(lst, ls)
        #necesario hacer recursiva esta parte
        if cmpfunction(root, Right_son):
            hp.sink(heap, i)
        elif cmpfunction(root, Left_son):
            hp.sink(heap, i)
        i-=1
    #invirtiendo pos
    j=size-1
    while j in range(1,size):
        hp.exchange(heap, 1, j)
        hp.sink(heap, 1)
        j-=1

#____________________________________________
#Implementacion usando funciones list
#____________________________________________

def heapsort1(lst):
    """
    Implementa el heapsort sobre una lista.
    """
    size=lt.size(lst)
    mid=size//2
    cmpfunction=lst['cmpfunction']
    i=mid
    while i in range(1,mid+1):
        funcionsink(lst,i, size, cmpfunction)
        i-=1
    #invirtiendo pos
    j=size-1
    while j in range(1,size):
        hp.exchange(lst, 1, j)
        funcionsink(lst,i,size, cmpfunction)
        j-=1

#____________________________________________
#Helper list
#____________________________________________

def funcionsink(lst, i, size, cmpfunction):
    """
    Implementacion de un sink sobre listas.
    """
    rs=i*2
    ls=i*2+1
    follower=i
    stop=False
    while (rs in range(1, size)) and (ls in range(1,size)) and not stop:
            root=lt.getElement(lst,follower)
            Right_son=lt.getElement(lst, rs)
            Left_son=lt.getElement(lst, ls)
            if cmpfunction(root, Right_son):
                lt.exchange(lst, follower, rs)
                if cmpfunction(Right_son, Left_son):
                    lt.exchange(lst, follower, ls)
                follower=rs
            elif cmpfunction(root, Left_son):
                lt.exchange(lst, follower, ls)
                follower=ls
            else:
                stop=True
            rs=follower*2
            ls=follower*2+1
        
example=hp.newHeap(cmpfunction)
lst=lt.newList()

def cmpfunction(a,b ):
    """
    Compara dos números.
    """
    if a < b:
        return -1
    elif a == b:
        return 0
    else:
        return 1