"""
 * Copyright 2020, Departamento de sistemas y Computación
 * Universidad de Los Andes
 *
 *
 * Desarrolado para el curso ISIS1225 - Estructuras de Datos y Algoritmos
 *
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with this program.  If not, see <http://www.gnu.org/licenses/>.
 """
import config
from DISClib.ADT import list as lt
from DISClib.DataStructures import listiterator as it
from DISClib.ADT import orderedmap as om
from DISClib.DataStructures import mapentry as me
from DISClib.DataStructures import linkedlistiterator as it 
from DISClib.DataStructures import arraylist as array 
from DISClib.ADT import map as m
import math
import datetime
assert config

"""
En este archivo definimos los TADs que vamos a usar,
es decir contiene los modelos con los datos en memoria


"""

# ___________________________________________________
# API del TAD Catalogo de accidentes
# ___________________________________________________
def newAnalaizer():
    """
    Inicia un nuevo analizador.
    
    Inicia un nuevo analizador.
    El analizador esta compuesto inicialmente por: 
        -Un ordered map que tiene por llaves las fechas en la que ocurrieron los crimenes.
        -Un ordered map que por llaves tiene las latitudes y longitudes en las que ocurrieron los crimenes.
        -Una lista de crimenes vacia.
    """
    analyzer={'dateIndex': None, 'lstaccidents': None, 'Number':0}
    
    analyzer['dateIndex']=om.newMap(omaptype='RBT',
                                    comparefunction=cmpDates)
    analyzer['lstaccidents']=lt.newList(datastructure='SINGLE_LINKED')
    return analyzer

# ___________________________________________________
# Funciones para agregar informacion al catalogo
# ___________________________________________________

def addAccident(analyzer, accident):
    """
    Agrega un accidente al mapa de accidentes.
    """
    addNewDate(analyzer, accident)
    lt.addLast(analyzer['lstaccidents'], accident)

def addNewDate(analyzer, accident):
    """
    Agrega un fecha al mapa de fechas.
    """
    dates=analyzer['dateIndex']
    date_row=accident['Start_Time']
    date=datetime.datetime.strptime(date_row, '%Y-%m-%d %H:%M:%S')
    entry=om.get(dates, date.date())
    if entry is None:
        value=newDateIndex(date.date())
        om.put(dates, date.date(), value)
    else:
        value=me.getValue(entry)
    lt.addLast(value['lstaccident'],accident)
 
# ___________________________________________________
# Creacion de entradas
# ___________________________________________________

def newDateIndex(date):
    """
    Crea la primera capa de informacion en el analyzador.
    """
    entry={'date':None,'lstaccident': None}
    entry['date']=date
    entry['lstaccident']=lt.newList(datastructure='SINGLE_LINKED', cmpfunction=cmpDates)
    return entry

# ___________________________________________________
# Funciones de consulta
# ___________________________________________________

def findByday(map,key):
    """
    Busca todas los accidentes que ocurrieron en una fecha específica
    """
    entry=om.get(map, key)
    try:
        value=me.getValue(entry)
        accidents=value['lstaccident']
        categories=countCategories(accidents)
        size=lt.size(accidents)
        return (categories,size)
    except:
        return None

def findBydate(map, key):
    """
    Busca los accidentes menores que una fecha.
    """
    try:
        min_key=om.minKey(map)
        rank=om.keys(map, min_key,key)
        iterator1= it.newIterator(rank)
        buckets=lt.newList(datastructure='SINGLE_LINKED')
        while it.hasNext(iterator1):
            key=it.next(iterator1)
            entry=om.get(map, key)
            value=me.getValue(entry)
            lt.addLast(buckets, value)
        #parte dos 
        total_accidents=0
        max_accident={'size':0,'date':None}
        iterator2=it.newIterator(buckets)
        while it.hasNext(iterator2):
            value=it.next(iterator2)
            lst=value['lstaccident']
            size=int(lt.size(lst))
            if size > max_accident['size']:
                max_accident['size']=size
                max_accident['date']=value['date']
            total_accidents=total_accidents+size
        return(max_accident, total_accidents)
    except:
        return None

def findByDateRank(map, key1, key2):
    """
    Busca los accidentes en un rango de fechas y la categoria de accidentes más reportadas en dicho rango.
    """
    try:
        rank=om.keys(map, key1, key2)
        iterator1= it.newIterator(rank)
        buckets=lt.newList(datastructure='SINGLE_LINKED')

        while it.hasNext(iterator1):
            key2=it.next(iterator1)
            entry=om.get(map, key2)
            value=me.getValue(entry)
            lt.addLast(buckets, value)

        total_accidents=0
        dic_categorias={'1':0,'2':0,'3':0,'4':0}
        iterator2=it.newIterator(buckets)
        while it.hasNext(iterator2):
            value=it.next(iterator2)
            lst=value['lstaccident']
            size=int(lt.size(lst))
            total_accidents=total_accidents+size
            iterator3=it.newIterator(lst)
            while it.hasNext(iterator3):
                value=it.next(iterator3)
                categoria=value["Severity"]
                if categoria == "1":
                    dic_categorias["1"]+=1
                elif categoria == "2":
                    dic_categorias["2"]+=1
                elif categoria == "3":
                    dic_categorias["3"]+=1
                elif categoria == "4":
                    dic_categorias["4"]+=1
        max_categoria=0
        for i in dic_categorias:
            if dic_categorias[i] > max_categoria:
                max_categoria= dic_categorias[i]
                max_Severity=i
        
        return(max_Severity, total_accidents)
    except:
        return None

def findByDateState(map, key1, key2):
    """
    Busca los accidentes en un rango de fechas y la categoria de accidentes más reportadas en dicho rango.
    """
    try:
        rank=om.keys(map, key1, key2)
        iterator1= it.newIterator(rank)
        buckets=lt.newList(datastructure='SINGLE_LINKED')

        while it.hasNext(iterator1):
            key2=it.next(iterator1)
            entry=om.get(map, key2)
            value=me.getValue(entry)
            lt.addLast(buckets, value)
        max_accident={'size':0,'date':None}
        iterator2=it.newIterator(buckets)
        while it.hasNext(iterator2):
            value=it.next(iterator2)
            lst=value['lstaccident']
            size=int(lt.size(lst))
            if size > max_accident['size']:
                max_accident['size']=size
                max_accident['date']=value['date']  

        list_estados=[]
        dict_estados={}     
        iterator3=it.newIterator(buckets)
        while it.hasNext(iterator3):
            value=it.next(iterator3)
            lst=value['lstaccident']
            iterator4=it.newIterator(lst)
            while it.hasNext(iterator4):
                value=it.next(iterator4)
                estado=value["State"]
                if estado not in list_estados:
                    list_estados.append(estado)
                    dict_estados[estado]=1
                elif estado in list_estados:
                    dict_estados[estado]+=1
        max_state=0
        for i in dict_estados:
            if dict_estados[i] > max_state:
                max_state= dict_estados[i]
                state=i
        return(max_accident, state )
    except:
        return None

def RangeHours(analyzer, hour1, hour2):
    """
    Dadas dos horas busca la cantidad de accidentes que han ocurrido entre esas dos horas.
    """
    dateIndex=analyzer['dateIndex']
    min_key=om.minKey(dateIndex)
    max_key=om.maxKey(dateIndex)
    keys_date=om.keys(dateIndex, min_key,max_key)
    accidents=lt.newList(datastructure='SINGLE_LINKED')
    iterator1=it.newIterator(keys_date)
    while it.hasNext(iterator1):
        key=it.next(iterator1)
        entry=om.get(dateIndex,key)
        value=me.getValue(entry)
        mp=value['lstaccident']
        iteratormp=it.newIterator(mp)
        while it.hasNext(iteratormp):
            accident=it.next(iteratormp)
            lt.addLast(accidents, accident)
    #parte2
    final_accidents=lt.newList()
    counter=0
    iterator2=it.newIterator(accidents)
    while it.hasNext(iterator2):
        accident=it.next(iterator2)
        hour_row=accident['Start_Time']
        hour=datetime.datetime.strptime(hour_row, '%Y-%m-%d %H:%M:%S')
        if cmpDates(hour1, hour.time()) == -1:
            if cmpDates(hour.time(), hour2) == -1:
                lt.addLast(final_accidents, accident)
                counter+=1
    T_categories=countCategories(final_accidents)
    return (counter,T_categories)

def findBycoordinates(lst,latitud,longitud,radio):
    """
    Busca las accidentes dentro de un radio dadas unas coordenadas.
    """
    try:
        inside=lt.newList()
        days={}
        iterator1=it.newIterator(lst)
        while it.hasNext(iterator1):
            accident=it.next(iterator1)
            ac_latitud=accident['Start_Lat']
            ac_longitud=accident['Start_Lng']
            if distance_between_2_points(latitud, ac_latitud, longitud, ac_longitud) <= radio:
                lt.addLast(inside, accident)
                date_row=datetime.datetime.strptime(accident['Start_Time'], '%Y-%m-%d %H:%M:%S')
                date=date_row.date()
                day=date.weekday()
                if day in days:
                    days[day]+=1
                else:
                    days[day]=1
        days=day_of_week(days)
        size=lt.size(inside)
        return(days, size)
    except:
        return None

# ___________________________________________________
# Funciones de Comparacion
# ___________________________________________________

def cmpIDs(id1,id2):
    """
    Compara los IDS de dos crimenes.
    """
    id1=str(id1)
    id2=str(id2)
    if id1 < id2:
        return -1
    elif id1 == id2:
        return 0
    else:
        return 1



def cmpDates(date1, date2):
    """
    Compara la fecha de dos crimenes.
    """
    if date1 < date2:
        return -1
    elif date1 == date2:
        return 0
    else: 
        return 1

def cmpLatitude(coordinate1, coordinate2):
    """
    Compara las coordenadas de dos accidentes
    """
    coordinate1=float(coordinate1)
    coordinate2=float(coordinate2)

    if coordinate1 < coordinate2:
        return -1
    elif coordinate1 == coordinate2:
        return 0
    else:
        return 1
def cmpLongitude(coordinate1, coordinate2):
    """
    Compara las coordenadas de dos accidentes
    """
    coordinate1=float(coordinate1)
    coordinate2=float(coordinate2)
    if coordinate1 < coordinate2:
        return -1
    elif coordinate1 == coordinate2:
        return 0
    else:
        return 1


def cmpSeverity(accident1,accident2):
    """
    Compara la severidad de dos accidentes
    """
    Severity1=accident1['Severity']
    Severity2=accident2['Severity']
    if Severity1 > Severity2:
        return -1
    elif Severity1 == Severity1:
        return 0
    else:
        return 1  

# ___________________________________________________
#  Helper
# ___________________________________________________

def aproxhour(hour):
    """
    Aproxima los valores de ciertas horas.
    """
    try:
        hours=int(hour[:2])
        minutes=int(hour[3:])
        if minutes in range(0,11):
            minutes=00
        elif minutes in range(10,20):
            minutes=15
        elif minutes in range(20,30):
            minutes=30
        else:
            minutes=00
            hours+=1
        minutes=str(minutes)
        hours=str(hours)
        if len(minutes) == 1:
            minutes= '0' + minutes
        if len(hours) == 1:
            minutes= '0' + hours
        hour= hours + ':' +minutes
        return hour
    except:
        return None

def countCategories(lst):
    """
    Cuenta los accidentes por categorias en una lista.

    retorna:
        -diccionario con las categorias como llaves y valor la cantidad de accidentes
    """
    iterator=it.newIterator(lst)
    dic={}
    while it.hasNext(iterator):
        value=it.next(iterator)
        categorie=value['Severity']
        if categorie in dic:
            dic[categorie]+=1
        else:
            dic[categorie]=1
    return dic
def distance_between_2_points(lt1:float,lt2:float,ln1:float,ln2:float):
    """
    calcula la distancia entre 2 coordenadas, con un radio específico.
    lt1=latititud 1   //coordenadas
    lt2= latitud 2    // coordenadas
    ln1= longitud 1   //coordenadas
    ln2= longitud 2   //coordenadas
    """
    radio= 6371e3 #radio de la tierra en metros
    rad1 = float(lt1) * float(math.pi/180) 
    rad2 = float(lt2) * float(math.pi/180)
    delta1 = (float(lt2)-float(lt1)) * float(math.pi/180)
    delta2 = (float(ln2)-float(ln1)) * float(math.pi/180)
    a = math.sin(delta1/2) * math.sin(delta1/2) + math.cos(rad1) * math.cos(rad2) * math.sin(delta2/2) * math.sin(delta2/2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
    d= radio*c
    return (d)
def day_of_week(dic):
    days={}
    for day in dic:
        if day == 0:
            days['Lunes']=dic[day]
        elif day == 1:
            days['Martes']=dic[day]
        elif day == 2:
            days['Miercoles']=dic[day]
        elif day == 3:
            days['Jueves']=dic[day]
        elif day == 4:
            days['Viernes']=dic[day]
        elif day == 5:
            days['Sabado']=dic[day]
        elif day == 6:
            days['Domingo']=dic[day]
    return(days)