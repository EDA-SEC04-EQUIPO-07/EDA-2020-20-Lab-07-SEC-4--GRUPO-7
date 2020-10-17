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

# -----------------------------------------------------
# API del TAD Catalogo de accidentes
# -----------------------------------------------------
def newAnalaizer():
    """
    Inicia un nuevo analizador.
    
    Inicia un nuevo analizador.
    El analizador esta compuesto inicialmente por: 
        -Un ordered map que tiene por llaves las fechas en la que ocurrieron los crimenes.
        -Un ordered map que por llaves tiene las latitudes y longitudes en las que ocurrieron los crimenes.
        -Una lista de crimenes vacia.
    """
    analyzer={'lstaccident': None, 'dateIndex': None, 'coordinatesIndex': None, 'Number':0}

    analyzer['lstaccident']=lt.newList(datastructure='SINGLE_LINKED',cmpfunction=cmpIDs )
    
    analyzer['dateIndex']=om.newMap(omaptype='RBT',
                                    comparefunction=cmpDates)
    #analyzer['coordinateIndex']=om.newMap(omaptype='RBT',
                                    #comparefunction= cmpCoordinates)

    return analyzer

# ==============================
# Funciones para agregar informacion al catalogo
# ==============================

def addAccident(analyzer, accident):
    """
    Agrega un accidente al mapa de accidentes.
    """
    lt.addLast(analyzer['lstaccident'], accident)
    addNewDate(analyzer, accident)
    analyzer['Number']+=1

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
    addHourIndex(value['hourIndex'], accident, date)
  
def addHourIndex(map, accident, date):
    """
    Agrega informacion al mapa de Ids.
    """
    hour=date.time()
    entry=om.get(map, hour)
    if entry is None:
        value=newHourIndex(hour)
        om.put(map, hour, value)
    else:
        value=me.getValue(entry)
    lt.addLast(value['lstaccident'],accident)

# ==============================
# Creacion de entradas
# ==============================

def newDateIndex(date):
    """
    Crea la primera capa de informacion en el analyzador.
    """
    entry={'date':None,'lstaccident': None, 'hourIndex':None}
    entry['date']=date
    entry['lstaccident']=lt.newList(datastructure='SINGLE_LINKED', cmpfunction=cmpDates)
    entry['hourIndex']=om.newMap(omaptype='RBT', comparefunction=cmpDates)
    return entry

def newHourIndex(hour):
    """
    Crea un elmento del arbol que organiza los eventos por hora.
    """
    entry={'hour':None, 'lstaccident':None}
    entry['hour']=hour
    entry['lstaccident']=lt.newList(datastructure='SINGLE_LINKED', cmpfunction=cmpDates)
    return entry

# ==============================
# Funciones de consulta
# ==============================

def findByday(map,key):
    """
    Busca todas los accidentes que ocurrieron en una fecha específica
    """
    entry=om.get(map, key)
    value=me.getValue(entry)
    try:
        accidents=value['lstaccident']
        size=lt.size(accidents)
        return (accidents,size)
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

def RangeHours(analyzer, hour1, hour2):
    """
    Dadas dos horas busca la canridad de accidentes que han ocurrido entre esas dos horas.
    """
    try:
        dateIndex=analyzer['dateIndex']
        min_key=om.minKey(dateIndex)
        max_key=om.maxKey(dateIndex)
        keys_date=om.keys(dateIndex, min_key,max_key)
        maps=lt.newList(datastructure='SINGLE_LINKED')
        iterator1=it.newIterator(keys_date)
        while it.hasNext(iterator1):
            key=it.next(iterator1)
            entry=om.get(dateIndex,key)
            value=me.getValue(entry)
            mp=value['hourIndex']
            lt.addLast(maps, mp)
        #parte2
        accidents=lt.newList(datastructure='SINGLE_LINKED')
        iterator2=it.newIterator(maps)
        while it.hasNext(iterator2):
            mp=it.next(iterator2)
            keys_hour=om.keys(mp, hour1, hour2)
            keysiterator=it.newIterator(keys_hour)
            while it.hasNext(keysiterator):
                entry=om.get(mp, it.next(keysiterator))
                value=me.getValue(entry)
                lst=value['lstaccident']
                iterator3=it.newIterator(lst)
                while it.hasNext(iterator3):
                    accident=it.next(iterator3)
                    lt.addLast(accidents, accident)
        size=lt.size(accidents)
        return (accidents,size)
    except:
        return None
def distance_between_2_points(lt1,lt2,ln1,ln2,):
    """
    calcula la distancia entre 2 coordenadas, con un radio específico.
    lt1=latititud 1   //coordenadas
    lt2= latitud 2    // coordenadas
    ln1= longitud 1   //coordenadas
    ln2= longitud 2   //coordenadas
    """
    radio= 6371e3 #radio de la tierra
    rad1 = lt1 * math.pi/180 
    rad2 = lt2 * math.pi/180
    delta1 = (lt2-lt1) * math.pi/180
    delta2 = (ln2-ln1) * math.pi/180
    a = math.sin(delta1/2) * math.sin(delta1/2) + math.cos(rad1) * math.cos(rad2) * math.sin(delta2/2) * math.sin(delta2/2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
    d= radio*c
    return (d)

# ==============================
# Funciones de Comparacion
# ==============================

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

def cmpCoordinates(coordinate1, coordinate2):
    """
    Compara las coordenadas de dos accidentes
    """
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