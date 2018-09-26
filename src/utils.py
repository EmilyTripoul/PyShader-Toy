# -*- coding: utf-8 -*-
"""
Created on Thu Sep 20 2018

@author: Emily
"""

from OpenGL.GL import *
from OpenGL.GLU import *
import hashlib
import importlib

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


_lastSeenShaderRoutineHash=''

def isRoutineNew(routineFile):
    with open(routineFile+'.py') as f:
        content=f.read()
        newHash=hashlib.md5(content.encode('utf-8')).hexdigest()
        return newHash!=_lastSeenShaderRoutineHash

def loadRoutineLib(routineFile, onlyIfLibUpdated=False):
    global _lastSeenShaderRoutineHash
    with open(routineFile+'.py') as f:
        content=f.read()
        newHash=hashlib.md5(content.encode('utf-8')).hexdigest()
        if (not onlyIfLibUpdated) or newHash!=_lastSeenShaderRoutineHash:
            _lastSeenShaderRoutineHash=newHash
            return importlib.import_module(routineFile.replace('/', '.'))
    return None

