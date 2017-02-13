# -*- coding: utf-8 -*-
"""
Created on Thu May 26 09:26:40 2016

@author: James Diamond
""" 
import numpy as _np
class CalibrationDummy():
    """
    This class is a test function to calibrate the manipulator 
    A is a change in degrees(theta 1), B is a change in degrees(theta 2) and C is a change in mm(x) at the appointed speed
    """
    def __init__(self):
        
        self.A = [0.001,   #speed 1 left
                  0.001,    #speed 1 right
                  0.01,    #speed 2 left
                  0.01,     #speed 2 right
                  0.10,    #speed 3 left
                  0.10,     #speed 3 right
                  0.20,    #speed 4 left
                  0.20,     #speed 4 right
                  0.30,    #speed 5 left 
                  0.30,     #speed 5 right
                  1200,    #speed 6 left
                  1200]     #speed 6 right
        
        self.B = [0.001,   #speed 1 down
                  0.001,    #speed 1 up
                  0.01,    #speed 2 down
                  0.01,     #speed 2 up
                  0.10,    #speed 3 down
                  0.10,     #speed 3 up
                  0.20,    #speed 4 down
                  0.20,     #speed 4 up
                  0.30,    #speed 5 down
                  0.30,     #speed 5 up
                  0.35,    #speed 6 down
                  0.35]     #speed 6 up
        
        self.C = [0.001,   #speed 1 extend
                  0.001,    #speed 1 retract
                  0.01,    #speed 2 extend
                  0.01,     #speed 2 retract
                  0.03,    #speed 3 extend
                  0.03,     #speed 3 retract
                  0.05,    #speed 4 extend
                  0.05,     #speed 4 retract
                  0.07,    #speed 5 extend
                  0.07,     #speed 5 retract
                  0.1,     #speed 6 extend
                  0.1]      #speed 6 retract 
           
    def _configuration(self,steps):
        """
        This function assign a value of X,Y,Z as a certain number of steps.
        """
        self.X=_np.zeros(len(self.A))
        self.Y=_np.zeros(len(self.B))
        self.Z=_np.zeros(len(self.C))
        for i in range(6):      #for 6 different speeds
             for j in range(2): #odd and even number
                 if j==0:
                    self.X[2*i-1]=self.A[2*i-1]*steps
                    self.Y[2*i-1]=self.B[2*i-1]*steps
                    self.Z[2*i-1]=self.C[2*i-1]*steps
                 if j==1:
                    self.X[2*i]=self.A[2*i]*steps
                    self.Y[2*i]=self.B[2*i]*steps
                    self.Z[2*i]=self.C[2*i]*steps
        #r=[self.X,self.Y,self.Z]
        #print r
        print 'Configured'
        return self.X,self.Y,self.Z
    
   
                
        
        
        
    


                            
                    
                