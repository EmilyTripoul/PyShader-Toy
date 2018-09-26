# -*- coding: utf-8 -*-
"""
Created on Wed Sep 26 2018

@author: Emily
"""

from OpenGL.GL import *
from OpenGL.GLU import *

import pygame # just to get a display

import sys
import time
import importlib

from src.utils import *

dataDir='data/'
routineFile=dataDir+'routine-1'

routineLib=None

def start():
    # get an OpenGL surface

    pygame.init() 
    pygame.display.set_mode((800,600), pygame.OPENGL|pygame.DOUBLEBUF)


    glEnable(GL_DEPTH_TEST)

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
                done = True
                pygame.display.quit()
        if t-lastUpdate > 30:
            buildAndUseProgram(dataDir+'shader-1.vs', dataDir+'shader-1.fs', True)
            lastUpdate=t

        t=t+1

        routineLib.routineSpecific(t)

        pygame.display.flip()
        time.sleep(2e-3)

if __name__=="__main__":
    run()
