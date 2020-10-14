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
    addIdIndex(value['idIndex'], accident)
  
def addIdIndex(map, accident):
    """
    Agrega informacion al mapa de Ids.
    """
    id=accident['ID']
    value=newIdIndex(accident)
    m.put(map, id, value)

# ==============================
# Creacion de entradas
# ==============================

def newDateIndex():
    """
    Crea la primera capa de informacion en el analyzador.
    """
    entry={'lstaccident': None, 'idIndex':None}

    entry['lstaccident']=lt.newList(datastructure='SINGLE_LINKED', cmpfunction=cmpDates)
    entry['idIndex']=m.newMap(numelements=350000,
                            maptype='PROBING',
                            loadfactor=0.4, 
                            comparefunction=cmpIDs)
    return entry

def newIdIndex(accident):
    """
    Crea la entrada de Index.
    """
    entry={'id':None, 'accident':None}
    entry['id']=accident['ID']
    entry['accident']=accident
    return entry

# ==============================
# Funciones de consulta
# ==============================

def findBydate(map, key):
    """
    Busca los accidentes menores que una fecha.
    """
    minkey=om.minKey(map)
    rank=om.keys(map, minkey, key)
    return rank


# ==============================
# Funciones de Comparacion
# ==============================

def cmpIDs(id1,id2):
    """
    Compara los IDS de dos crimenes.
    """
    print(id1)
    print(id2)
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
    Compara las coordenadas de dos crimenes
    """
    if coordinate1 < coordinate2:
        return -1
    elif coordinate1 == coordinate2:
        return 0
    else:
        return 1