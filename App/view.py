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

import sys
import config
import datetime
from DISClib.ADT import list as lt
from DISClib.DataStructures import listiterator as it
from App import controller
assert config
sys.setrecursionlimit(10000)

"""
La vista se encarga de la interacción con el usuario.
Presenta el menu de opciones  y  por cada seleccion
hace la solicitud al controlador para ejecutar la
operación seleccionada.
"""

# ___________________________________________________
#  Ruta a los archivos
# ___________________________________________________

file='\\us_accidents_small.csv'

# ___________________________________________________
#  Funciones de impresion
# ___________________________________________________

def printlist1(lst):
    """
    Imprime los elementos de una lista.
    """
    iterator=it.newIterator(lst)
    while it.hasNext(iterator):
        value=it.next(iterator)
        id=value['ID']
        severity=value['Severity']
        start=value['Start_Time']
        print('\nEl id del accidente es: ', str(id), ' con severidad de: ', str(severity), ' con hora de inicio: ', str(start) , '.')

# ___________________________________________________
#  Menu principal
# ___________________________________________________


def printMenu():
    print("\n")
    print("*******************************************")
    print("Bienvenido")
    print("1- Inicializar Analizador")
    print("2- Cargar información de accidentes")
    print("3- Conocer los accidentes en una fecha")
    print("4- Buscando accidentes anteriores a una fecha")
    print("5- Buscando accidentes en el rango de fechas")
    print("0- Salir")
    print("*******************************************")


"""
Menu principal
"""
while True:
    printMenu()
    inputs = input('Seleccione una opción para continuar\n>')

    if int(inputs[0]) == 1:
        print("\nInicializando....")
        # cont es el controlador que se usará de acá en adelante
        cont = controller.init()

    elif int(inputs[0]) == 2:
        print("\nCargando información de accidentes ....")
        controller.loadData(cont, file)
        (high,nodes,min_key,max_key)=controller.infAnalyzer(cont)
        print('\nLa altura del arbol cargado es igual a: ', str(high))
        print('\nLa cantidad de nodos de arbol son: ', str(nodes))
        print('\nLa primera fecha registrada es: ', str(min_key))
        print('\nLa ultima fecha registrada es: ', str(max_key))
        
    elif int(inputs[0]) == 3:
        print('\nRecuerde el formato YYYY-mm-dd')
        date_row=input('\nIngrese la fecha con la que desea investigar:\n>')
        try:
            date=datetime.datetime.strptime(date_row, '%Y-%m-%d')
        except:
            date=None
        if date is None:
            print('\nEl formato no es correcto.')
        else:
            ans=controller.findByday(cont,date.date())
            if ans is None:
                print('\nLa fecha ingresada no se encuentra dentro del rango de fechas registradas.')
            else:
                (lst, size)= controller.findByday(cont,date.date())
                print('\nLa cantidad de accidentes reportados para ese día fue de: ', str(size),'.\n')
                printlist1(lst)

    elif int(inputs[0]) == 4:
        print('\nRecuerde formato YYYY-mm-dd')
        date_row=input('\nIngrese la fecha con la que desea investigar:\n>')
        try:
            date=datetime.datetime.strptime(date_row, '%Y-%m-%d')
        except:
            date=None
        if date is None:
            print('\nEl Formato ingresado no es valido.')
        else:
            ans=controller.findBydate(cont, date.date())
            if ans is None:
                print('\nLa fecha ingresada no se encuentra dentro del rango de fechas registradas.')
            else:
                (max_date, size)=ans
                print('\nLa cantidad de accidentes registrados hasta la fecha es: ', str(size), '.')
                date=max_date['date']
                accidents=max_date['size']
                print('\nLa fecha con más accidentes registrados fue: ', str(date), 
                'con un total de : ', str(accidents), 'acidentes.')
    elif int(inputs[0]) == 5:
        print('\nRecuerde formato YYYY-mm-dd')
        date_row1=input('\nIngrese la fecha inicial que desea investigar:\n>')
        date_row2=input('\nIngrese la fecha final que desea investigar:\n>')
        try:
            date1=datetime.datetime.strptime(date_row1, '%Y-%m-%d')
        except:
            date1=None
        try:
            date2=datetime.datetime.strptime(date_row2, '%Y-%m-%d')
        except:
            date2=None
        if date1 is None or date2 is None:
            print('\nEl Formato ingresado no es valido.')
        else:
            ans=controller.findByDateRank(cont, date1.date(), date2.date())
            if ans is None:
                print('\nLa fecha ingresada no se encuentra dentro del rango de fechas registradas.')
            else:
                (max_date, size)=ans
                print('\nLa cantidad de accidentes registrados entre las fechas es: ', str(size), '.')
                date=max_date['date']
                accidents=max_date['size']
                print('\nLa fecha con más accidentes registrados fue: ', str(date), 
                'con un total de : ', str(accidents), 'acidentes.')

    else:
        sys.exit(0)
sys.exit(0)
