# -*- coding: utf-8 -*-
"""
Created on Wed Sep 26 2018

@author: Emily
"""

from OpenGL.GL import *
from OpenGL.GLU import *
import random
from math import * # trigonometry

import pygame # just to get a display

import sys
import time
import hashlib


dataDir='data/'

def createAndCompileShader(type,source):
    shader=glCreateShader(type)
    glShaderSource(shader,source)
    glCompileShader(shader)

    result=glGetShaderiv(shader,GL_COMPILE_STATUS)

    if (result!=1): # shader didn't compile
        raise Exception("Couldn't compile shader\nShader compilation Log:\n"+glGetShaderInfoLog(shader))
    return shader


_lastSeenShaderVSHash=''
_lastSeenShaderFSHash=''

def loadShader(shaderFile, shaderType): 
    global _lastSeenShaderVSHash, _lastSeenShaderFSHash
    with open(shaderFile) as f:
        content=f.read()
        if shaderType==GL_VERTEX_SHADER:
            _lastSeenShaderVSHash=hashlib.md5(content.encode('utf-8')).hexdigest()
        elif shaderType==GL_FRAGMENT_SHADER:
            _lastSeenShaderFSHash=hashlib.md5(content.encode('utf-8')).hexdigest()
        return createAndCompileShader(shaderType, content)

def isShaderNew(shaderFile, shaderType):
    with open(shaderFile) as f:
        content=f.read()
        shaderHash=hashlib.md5(content.encode('utf-8')).hexdigest()
        if shaderType==GL_VERTEX_SHADER:
            return shaderHash!=_lastSeenShaderVSHash
        elif shaderType==GL_FRAGMENT_SHADER:
            return shaderHash!=_lastSeenShaderFSHash
    return False


def buildAndUseProgram(sourceVS, sourceFS, onlyIfShaderUpdated=False):
    if (not onlyIfShaderUpdated) or (isShaderNew(sourceVS, GL_VERTEX_SHADER) or isShaderNew(sourceFS, GL_FRAGMENT_SHADER)):
        print('Load shader')
        vertex_shader=loadShader(sourceVS, GL_VERTEX_SHADER)
        fragment_shader=loadShader(sourceFS, GL_FRAGMENT_SHADER)
        program=glCreateProgram()
        glAttachShader(program,vertex_shader)
        glAttachShader(program,fragment_shader)
        glLinkProgram(program)

        # try to activate/enable shader program
        # handle errors wisely

        try:
            glUseProgram(program)   
        except OpenGL.error.GLError:
            print(glGetProgramInfoLog(program))
            raise

def loadCube(listId=1):
    # load a cube into a display list

    glNewList(listId,GL_COMPILE)

    glBegin(GL_QUADS)

    glColor3f(1,1,1)

    glNormal3f(0,0,-1)
    glVertex3f( -1, -1, -1)
    glVertex3f(  1, -1, -1)
    glVertex3f(  1,  1, -1)
    glVertex3f( -1,  1, -1)

    glNormal3f(0,0,1)
    glVertex3f( -1, -1,  1)
    glVertex3f(  1, -1,  1)
    glVertex3f(  1,  1,  1)
    glVertex3f( -1,  1,  1)

    glNormal3f(0,-1,0) 
    glVertex3f( -1, -1, -1)
    glVertex3f(  1, -1, -1)
    glVertex3f(  1, -1,  1)
    glVertex3f( -1, -1,  1)

    glNormal3f(0,1,0) 
    glVertex3f( -1,  1, -1)
    glVertex3f(  1,  1, -1)
    glVertex3f(  1,  1,  1)
    glVertex3f( -1,  1,  1)

    glNormal3f(-1,0,0)     
    glVertex3f( -1, -1, -1)
    glVertex3f( -1,  1, -1)
    glVertex3f( -1,  1,  1)
    glVertex3f( -1, -1,  1)                      

    glNormal3f(1,0,0)        
    glVertex3f(  1, -1, -1)
    glVertex3f(  1,  1, -1)
    glVertex3f(  1,  1,  1)
    glVertex3f(  1, -1,  1)

    glEnd()
    glEndList()

def start():
    # get an OpenGL surface

    pygame.init() 
    pygame.display.set_mode((800,600), pygame.OPENGL|pygame.DOUBLEBUF)


    glEnable(GL_DEPTH_TEST)

def routineSpecific(time):
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(90,1,0.01,1000)
    gluLookAt(sin(time/260.0)*4,cos(time/260.0)*4,cos(time/687.0)*3,0,0,0,0,1,0)
    
    glClearColor(0.0, 0.0, 0.0, 1.0)
    glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)

    glMatrixMode(GL_MODELVIEW)

    # calculate light source position

    ld=[sin(time/16.0)*4.0,sin(time/20.0)*4.0,cos(time/16.0)*4.0]

    # pass data to fragment shader

    glLightfv(GL_LIGHT0,GL_POSITION,[ld[0],ld[1],ld[2]]);
    
    # fallback

    glColor3f(1,1,1)

    glLoadIdentity()
    # render a pretty range of cubes
    
    for i in range(-5,5):
        for j in range(-5,5):
            for k in range(-5,5):
                glPushMatrix()
                glTranslate(i,j,k)
                glScale(0.1,0.1,0.1)
                glCallList(1)
                glPopMatrix()

def run():
    start()
    buildAndUseProgram(dataDir+'shader-1.vs', dataDir+'shader-1.fs')
    loadCube(1)

    done = False

    t=0 
    lastUpdate=0


    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = False
                pygame.display.quit()
        if t-lastUpdate > 30:
            buildAndUseProgram(dataDir+'shader-1.vs', dataDir+'shader-1.fs', True)
            lastUpdate=t

        t=t+1

        routineSpecific(t)

        pygame.display.flip()
        time.sleep(2e-3)

if __name__=="__main__":
    run()
