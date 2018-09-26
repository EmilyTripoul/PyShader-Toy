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
    gluLookAt(sin(2*time/26000.0)*4,cos(time/26000.0)*4,cos(time/68700.0)*3,0,0,0,0,1,0)
    
    glClearColor(0.0, 0.0, 0.0, 1.0)
    glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)

    glMatrixMode(GL_MODELVIEW)

    # calculate light source position

    ld=[sin(time/1600.0)*4.0,sin(time/2000.0)*4.0,cos(time/1600.0)*4.0]

    # pass data to fragment shader

    glLightfv(GL_LIGHT0,GL_POSITION,[ld[0],ld[1],ld[2]]);
    
    # fallback

    glColor3f(1,1,1)

    glLoadIdentity()
    # render a pretty range of cubes
    num = round(10*sin(time/1e3)**4)
    for i in range(-num,num+1):
        for j in range(-num,num+1):
            for k in range(-num,num+1):      
                if k==j:          
                    glPushMatrix()
                    glTranslate(i,j,k)
                    glScale(0.1,0.1,0.1)
                    glCallList(1)
                    glPopMatrix()
