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
    analyzer={'lstaccident': None, 'dateIndex': None, 'coordinatesIndex': None}

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

def addNewDate(analyzer, accident):
    """
    Agrega un fecha al mapa de fechas.
    """
    dates=analyzer['dateIndex']
    date_row=accident['Start_Time']
    date=datetime.datetime.strptime(date_row, '%Y-%m-%d %H:%M:%S')
    entry=om.get(dates, date.date())
    if entry is None:
        value=newDateIndex()
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

def newDateIndex():
    """
    Crea la primera capa de informacion en el analyzador.
    """
    entry={'lstaccident': None, 'hourIndex':None}

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
    minkey=om.minKey(map)
    rank=om.keys(map, minkey, key)
    iterator= it.newIterator(rank)
    total_accidentes=0
    lista2=None
    while it.hasNext(iterator):
        llave= it.next(iterator)
        lista1=om.get(map,key)
        lista2=me.getValue(lista1)
    print(lista2)
        
    

    return total_accidentes


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