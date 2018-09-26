# -*- coding: utf-8 -*-
"""
Created on Thu Sep 20 2018

@author: Emily
"""
from OpenGL.GL import *
from OpenGL.GLU import *
import random
from math import * # trigonometry

def routineSpecific(time):
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(90,1,0.01,1000)
    gluLookAt(sin(2*time/260.0)*4,cos(time/260.0)*4,cos(time/687.0)*3,0,0,0,0,1,0)
    
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
    
    for i in range(-10,10):
        for j in range(-10,10):
            for k in range(-5,5):
                glPushMatrix()
                glTranslate(i,j,k)
                glScale(0.1,0.1,0.1)
                glCallList(1)
                glPopMatrix()
