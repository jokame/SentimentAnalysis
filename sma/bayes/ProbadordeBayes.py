'''
    SentimentAnalysis. SentimentAnalysis for social networks.
    Copyright (C) 2013  Christian Ladrón, Carlos Méndez, Wulfrano Moreno.

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
'''

import ClasificadorBayes
import csv
import numpy

ColumnaTexto = 1
ColumnaClase = 0


def varparametros(filename, inicio, fin, paso):
    resultados = []
    x = []
    y = []
    probis = numpy.arange(inicio, fin, paso)
    for probi in probis:
        resultado = (probi, Probador(filename, peso=1, probi=probi))
        resultados.append(resultado)
        x.append(resultado[0])
        y.append(resultado[1])
    respaldo = open('resultados2.txt', 'w')
    for res in resultados:
        cadena = str(res[0]) + '    ' + str(res[1]) + '\n'
        respaldo.write(cadena)
    respaldo.close()
#   ply.plot(x,y,'r*-')
#   ply.show()
    return resultados


def Probador(filename, peso=1, probi=0.5):
    aciertos = 0.0
    totales = 0.0
    db_clasificador = 1
    clasi = ClasificadorBayes.ClasificadorBayes()
    clasi.loadFromRedis(db_clasificador)
    archivo = open(filename, 'r')
    csvlector = csv.reader(archivo)
    for linea in csvlector:
        texto = linea[ColumnaTexto]
        clase = linea[ColumnaClase]
        if clase in clasi.clases:
            clasi.setfprobs(texto, peso=peso, probi=probi)
            (a, claseclasif) = clasi.clasifica(texto)
            if claseclasif == clase:
                aciertos += 1
            totales += 1
            if totales % 500 == 0:
                print totales
    archivo.close()
    eficacia = (aciertos * 100) / totales
    print 'Precision de ' + str(eficacia) + '% para ' + str(probi) + ' aciertos: ' + str(aciertos) + ', total de: ' + str(totales)
    return eficacia
