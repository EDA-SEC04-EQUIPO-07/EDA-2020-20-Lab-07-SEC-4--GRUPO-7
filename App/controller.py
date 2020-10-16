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

import config as cf
from App import model
import datetime
import csv
from DISClib.ADT import orderedmap as om
from DISClib.Algorithms.Sorting import mergesort

"""
El controlador se encarga de mediar entre la vista y el modelo.
Existen algunas operaciones en las que se necesita invocar
el modelo varias veces o integrar varias de las respuestas
del modelo en una sola respuesta.  Esta responsabilidad
recae sobre el controlador.
"""

# ___________________________________________________
#  Inicializacion del catalogo
# ___________________________________________________


def init():
    """
    Llama la funcion de inicializacion del modelo.
    """
    analyzer=model.newAnalaizer()
    return analyzer


# ___________________________________________________
#  Funciones para la carga de datos y almacenamiento
#  de datos en los modelos
# ___________________________________________________

def loadData(analyzer, accidentsfile):
    """
    Carga los datos de los archivos CSV en el modelo
    """
    accidentfile = cf.data_dir + accidentsfile
    input_file = csv.DictReader(open(accidentfile, encoding="utf-8"),
                                delimiter=",")
    for accident in input_file:
        model.addAccident(analyzer, accident)
    return analyzer


# ___________________________________________________
#  Funciones para consultas
# ___________________________________________________

def infAnalyzer(analyzer):
    """
    Dado un analizador retorna informacion sobre este.
    """
    high=om.height(analyzer['dateIndex'])
    nodes=om.size(analyzer['dateIndex'])
    min_key=om.minKey(analyzer['dateIndex'])
    max_key=om.maxKey(analyzer['dateIndex'])
    return (high,nodes,min_key,max_key)

def findBydate(analyzer, date):
    """
    Busca todas los accidentes que ocurrieron antes de una fecha.
    """
    mp=analyzer['dateIndex']
    return model.findBydate(mp, date)

def findByDateRank(analyzer, date1, date2):
    """
    Busca todas los accidentes que ocurrieron antes de una fecha.
    """
    mp=analyzer['dateIndex']
    return model.findByDateRank(mp, date1, date2)

def findByday(analyzer,date):
    """
    Busca todas los accidentes que ocurrieron en una fecha específica, reportando la cantidad de accidentes por severidad para dicha fecha
    """
    mp=analyzer["dateIndex"]
    try:
        (lst, size) = model.findByday(mp,date)
        mergesort.mergesort(lst, model.cmpSeverity)
        return (lst, size)
    except:
        return None
