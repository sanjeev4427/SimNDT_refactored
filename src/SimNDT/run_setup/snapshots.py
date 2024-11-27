__author__ = 'Miguel Molero'

import os
import sys
import numpy as np
import matplotlib.pyplot as plt
from  scipy.misc import imsave
from scipy.io import savemat

import math

class SnapShots:
    def __init__(self, Enable=False, Extension='.png', Step=200, Filename=None, File_path = None, dB=60, Color=0, 
                       Field = 0,
                       enableFields=False,
                       enableSignals=False,
                       enableImages=False,
                       enableNumPy=False,
                       enableVolume=False,
                       enableView=False,
                       sensorShape = [],
                       sensorPlacement = [],
                       sensorSize = 0):

        self.IsEnable = Enable
        self.Extension = Extension
        self.Step = Step
        self.Filename = Filename
        self.File_path = File_path
        self.DB = dB
        self.Color = Color
        self.Field = Field
        self.enableFields   = enableFields
        self.enableSignals  = enableSignals
        self.enableImages   = enableImages
        self.enableNumPy    = enableNumPy
        self.enableVolume   = enableVolume
        self.enableView     = enableView
        self.sensorShape    = sensorShape
        self.sensorPlacement = sensorPlacement
        self.sensorSize      = sensorSize
        self.volF = []
        self.volS = []
        self.volP = []

        # if self.File_path does not exist, create it
        if not os.path.exists(self.File_path):
            os.makedirs(self.File_path)
              
    def save_fields(self, Fx, Fy, n):

        if self.enableVolume:
          self.volF.append(np.array([Fx,Fy]))
        elif self.enableNumPy:
          FILE = self.Filename + ("-fields-%05d" % (int(n / self.Step)))
          
          FIle_PATH = os.path.join(self.File_path, FILE)
          np.save(FIle_PATH,np.array([Fx,Fy]))
          print("Fields saved in numpy format at: ", FILE)
        else:  
          dict = {}
          dict['Vx'] = Fx
          dict['Vy'] = Fy
          FILE = self.Filename + ("-fields-%05d" % (int(n / self.Step))) + ".mat"
          savemat(FILE, dict)

    # @blab+
    def save_signal(self, D , n, Label):
        self.Label = Label       
        xn = D.shape[1]
        yn = D.shape[0]
        dx = 1 # sensor delta
        dy = 1
        ox = 0 # offset
        oy = 0
        if len(self.sensorShape) > 0:
          # size of sensor matrix
          sx = self.sensorShape[0]
          sy = self.sensorShape[1]
          S = np.zeros([sy,sx])
          if len(self.sensorPlacement):
            p=self.sensorPlacement
            ox=p[0]
            dx=p[1]
            oy=p[2]
            dy=p[3]
          else:
            ox=dx=round(xn/(sx+1.0))
            oy=dy=round(yn/(sy+1.0))
          for x in range(0,sx):
            for y in range(0,sy):
              S[y,x]=D[oy+y*dy,ox+x*dx]
        else:
          S = D 

        if self.enableVolume:
          self.volS.append(np.copy(S))
        elif self.enableNumPy:
          FILE = self.Filename + ("-signal-"+Label+"-%05d" % (int(n / self.Step)))
          np.save(FILE,S)
        else:
          FILE = self.Filename + ("-signal-"+Label+"-%05d" % (int(n / self.Step))) + ".mat"
          savemat(FILE, S)

    def save_power(self, Vx, Vy, n):
        
        S =  np.sqrt(Vx ** 2 + Vy ** 2)
        
        if self.enableVolume:
          self.volP.append(np.copy(S))
        elif self.enableNumPy:
          FILE = self.Filename + ("-power-%05d" % (int(n / self.Step)))
          np.save(FILE,S)
        else:
          FILE = self.Filename + ("-power-%05d" % (int(n / self.Step))) + ".mat"
          savemat(FILE, S)

    def save_fig(self, SV, n, idx=None):

        SV += self.DB
        ind = np.nonzero(SV < 0)
        SV[ind] = 0
        SV /= np.max(SV)

        if self.Color == 0:
            cmap = plt.get_cmap('jet')
        elif self.Color == 1:
            cmap = plt.get_cmap('gray')

        try:
            _resize = False
            M, N = np.shape(SV)
            if M >= 2000:
                _resize = True
            if N >= 2000:
                _resize = True

            if _resize:
                SVV = SV[::3, ::3]
                rgba_img = cmap(SVV)
            else:
                SVV = SV[::2, ::2]
                rgba_img = cmap(SVV)

            rgb_img = np.delete(rgba_img, 3, 2)

            if idx is not None:
                FILE = self.Filename + "_insp%d_" % idx + str(int(n / self.Step)) + self.Extension
            else:
                FILE = self.Filename + ("%05d" % (int(n / self.Step))) + self.Extension
            imsave(FILE, rgb_img)

        except:
          raise ValueError("Too large Snapshots Size!!!!!!!!")

    def save_vol(self):
    
        if len(self.volF) > 0:
          if self.enableNumPy:
            FILE = self.Filename + '-fields'
            np.save(FILE,np.array(self.volF))
            self.volF=[]
            
        if len(self.volS) > 0:
          if self.enableNumPy:
            FILE = self.Filename + '-signal-'+self.Label
            np.save(FILE,np.array(self.volS))
            self.volS=[]
          
        if len(self.volP) > 0:
          if self.enableNumPy:
            FILE = self.Filename + '-power'
            np.save(FILE,np.array(self.volP))
            self.volP=[]
        
