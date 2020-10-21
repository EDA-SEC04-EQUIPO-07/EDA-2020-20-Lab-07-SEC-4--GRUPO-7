from DISClib.DataStructures import heap as hp
from DISClib.DataStructures import liststructure as lt
from DISClib.DataStructures import listiterator as it
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
        
        
example=hp.newHeap(cmpfunction)

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