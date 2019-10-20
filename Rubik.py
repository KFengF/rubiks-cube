'''
Python version 3.7.4
Vpython version 7.5.1
'''
from vpython import *
from random import choice, randrange
from functools import partial

def tamano(n):
    if n % 2 == 0:
        return -n/2+0.5, (n/2)-0.5, n/2
    else:
        return int(-n/2), (n/2)-0.5, n/2

def posicion_camara(n): 
    if n > 4:
        scene.camera.pos = vec(13.5971, 12.8445, 19.8748)
        scene.camera.axis = vec(-13.5971, -12.8445, -19.8748)
    else:
        scene.camera.pos = vec(7.86468, 6.90072, 12.8276)
        scene.camera.axis = vec(-7.86468, -6.90072, -12.8276)

def boton_reset(buttton):
    reset_camara()

def escoger_tamano(boton):
    global n
    n = int(boton.selected)

def generador(colores, x, y, z, inicio, final, cuadros=[]):
    cuadros.append(box(pos=vec(z,y,x), color=colores[0], size=vec(0.05,0.98,0.98)))
    cuadros.append(box(pos=vec(x,y,z), color=colores[1], size=vec(0.98,0.98,0.05)))
    cuadros.append(box(pos=vec(-z,y,x), color=colores[2], size=vec(0.05,0.98,0.98)))
    cuadros.append(box(pos=vec(x,y,-z), color=colores[3], size=vec(0.98,0.98,0.05)))
    cuadros.append(box(pos=vec(y,z,x), color=colores[4], size=vec(0.98,0.05,0.98)))
    cuadros.append(box(pos=vec(y,-z,x), color=colores[5], size=vec(0.98,0.05,0.98)))
    if x < final:
        return generador(colores, x+1, y, z, inicio, final, cuadros)
    if y < final:
        return generador(colores, inicio, y+1, z, inicio, final, cuadros)
    return cuadros

def frange(start, stop, step):
    while True:
        if step > 0 and start >= stop:
            break
        elif step < 0 and start <= stop:
            break
        yield ('%g' % start)
        start = start + step

def separacion(n):
    arreglo = []
    if n % 2 == 0:
        for i in frange(0.5, n/2, 1):
            arreglo.append(float(i))
    else:
        for i in frange(1, n/2, 1):
            arreglo.append(float(i))
    return arreglo

def creacion_switcher(arreglo, minusculas, mayusculas):
    switcher = {}
    for i in range(len(arreglo)):
        switcher[minusculas[6*i]] = (vec(1,0,0), arreglo[i], pi/2, 'derecha capa '+str(i+1))
        switcher[mayusculas[6*i]] = (vec(1,0,0), arreglo[i], -pi/2)
        switcher[minusculas[(6*i)+1]] = (vec(-1,0,0), arreglo[i], pi/2, 'izquierda capa '+str(i+1))
        switcher[mayusculas[(6*i)+1]] = (vec(-1,0,0), arreglo[i], -pi/2)
        switcher[minusculas[(6*i)+2]] = (vec(0,1,0), arreglo[i], pi/2, 'arriba capa '+str(i+1))
        switcher[mayusculas[(6*i)+2]] = (vec(0,1,0), arreglo[i], -pi/2)
        switcher[minusculas[(6*i)+3]] = (vec(0,-1,0), arreglo[i], pi/2, 'abajo capa '+str(i+1))
        switcher[mayusculas[(6*i)+3]] = (vec(0,-1,0), arreglo[i], -pi/2)
        switcher[minusculas[(6*i)+4]] = (vec(0,0,1), arreglo[i], pi/2, 'frente capa '+str(i+1))
        switcher[mayusculas[(6*i)+4]] = (vec(0,0,1), arreglo[i], -pi/2)
        switcher[minusculas[(6*i)+5]] = (vec(0,0,-1), arreglo[i], pi/2, 'atrás capa '+str(i+1))
        switcher[mayusculas[(6*i)+5]] = (vec(0,0,-1), arreglo[i], -pi/2)
    return switcher

def movimientos_random(minusculas, switcher, cuadros):
    for i in range(randrange(20, 30)):
        switch(choice(minusculas), switcher, cuadros)

def creacion_texto(switcher):
    texto = ''
    for key in switcher.keys():
        if len(switcher[key]) == 4:
            texto += key + ': Para girar '+ switcher[key][3] + '\n'
    return texto

def movimiento(vect, cos, angulo, cuadros):
    fps = 24
    for i in frange(0, angulo-angulo*0.01, angulo/fps):
        rate(fps)
        for cuadro in cuadros:
            if dot(cuadro.pos, vect) >= cos-0.02 and dot(cuadro.pos, vect) < cos+0.6:
                cuadro.rotate(angle=angulo/fps, axis=vect, origin=vec(0,0,0))

def switch(tecla, switcher, cuadros):
    try:
        return movimiento(switcher[tecla][0], switcher[tecla][1], switcher[tecla][2], cuadros)
    except: pass

'''-----               COMIENZO DEL PROGRAMA               -----'''

'''Preparación del escenario'''

n = 0

menu_tamano = menu( choices=['2', '3', '4', '5', '6', '7'], bind=escoger_tamano, selected='Seleccionar tamaño' )

while n == 0:
    '''Esperando... a escoger una respuesta en el menu'''

menu_tamano.disabled = True
scene.height = 1200
scene._lights = []
local_light(pos=vec(3,3,-5))
local_light(pos=vec(-3,-3,-5))
local_light(pos=vec(0,3,5))
reset_camara = partial(posicion_camara, n)
reset_camara()
button( bind=reset_camara, text='Reset camara', pos=scene.title_anchor )

'''Creación del Cubo de Rubik'''

minusculas = 'rludfbekicgvtjoxhn'
mayusculas = minusculas.upper()
colores = [color.green, color.red, color.blue, vec(0.886, 0.415, 0.000), color.yellow, color.white]
inicio, final, z = tamano(n)
cuadros = generador(colores, inicio, inicio, z, inicio, final)
arreglo = separacion(n)
switcher = creacion_switcher(arreglo, minusculas, mayusculas)

desordenar_cubo = partial(movimientos_random, minusculas[:int(len(switcher)/2)], switcher, cuadros)
button( bind=desordenar_cubo, text='Desordenar cubo', pos=scene.title_anchor )


'''Creación de las instrucciones'''

texto = creacion_texto(switcher)
label(text='''Hola a todos, a continuación se mostrará las teclas para mover.
El sentido del movimiento es horaria, y para el sentido antihorario se usa la tecla en mayúscula
''' + texto, yoffset=110, height=14)

'''Receptor de movimientos'''

while True:
    tecla = scene.waitfor('keydown').key
    if tecla:
        switch(tecla, switcher, cuadros)