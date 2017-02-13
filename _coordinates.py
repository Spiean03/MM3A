# -*- coding: utf-8 -*-
"""
@author:    Andreas Spielhofer
            Ph.D. Candidate
            SPM group - http://spm.physics.mcgill.ca/
            
            Department of Physics
            McGill University
            3600 Rue University
            Montreal H3A 2T8
            Canada
            
@email:     andreas.spielhofer@mail.mcgill.ca
"""

import math

class KleindiekCoordinates(object):
    """
    This class defines the coordinate system ONLY for the micromanipulator 
    (without four point probe holder).
    If you have a a holder on the end of the manipulator(what is normally the 
    case), use class FourPointProbeCoordinates instead.
    """
    
    def __init__(self):
        #here are the lenghts of the arms of the manipulator.
        self.l1 = float(21.0)  #length of first arm
        self.l2 = float(18.0)  #length of second arm. this one is longer than from KleindiekCoordinates since the chipholder has an additional extension of 3mm

    def forward(self,theta1,theta2,extension): #angles in degrees, extension in millimeter!
        """
        The forward function translates the angles and the extension directly
        into coordinates X,Y,Z (in mm). The (0,0,0) is in the base of the 
        manipulator. If you have 0degrees angle and 0mm extension, the end effector 
        points towards the x-axis with position (39,0,0), as proposed.
        """
        # translate angles from degrees in radiants, make sure that values are in 
        # correct range:
        
        if -90.0 <= theta1 <= 90.0 and -90.0 <= theta2 <= 90.0:
            theta1 = float(theta1/360.0*2*math.pi)
            theta2 = float(theta2/360.0*2*math.pi)
        else:
            print "Theta1 or Theta2 not in range -90,90 degrees"
            return     
        if 0.0 <= extension <= 12.0:
            extension = float(extension)
        else:
            print "Value for extension not allowed. Use values between 0-12(mm)"
            return
        
        X = float(self.l1*math.cos(theta1) + (self.l2+extension)*math.cos(theta1)*math.cos(theta2))
        Y = float(self.l1*math.sin(theta1) + (self.l2+extension)*math.sin(theta1)*math.cos(theta2))
        Z = float((self.l2 +extension)*math.sin(theta2))
        
        self.forwardvalue = [round(X,6),round(Y,6),round(Z,6)]
    
    def reverse(self,X,Y,Z):
        """
        The reverse function translates absolute coordinates (X,Y,Z) directly
        into the angles theta1, theta2 and the extension of the manipulator.
        """
        
        theta1 = float(math.atan(Y/X))
        theta2 = float(math.atan(Z/(math.sqrt(X**2+Y**2)-self.l1)))
        ext = float(math.sqrt(Z**2+(math.sqrt(X**2+Y**2)-self.l1)**2)-self.l2)
        
        # the output will directly give the angles in degrees and extension in mm
        self.reversevalue = [round(math.degrees(theta1),6),round(math.degrees(theta2),6),round(ext,6)]

class FourPointProbeCoordinates(object):
    """
    This class defines the coordinate system with an additional holder on front 
    of the effector of the manipulator.
    The lenght l2 is different than in KleindiekCoordinates, because I added
    the extra 3mm extension of the pin of the four point-probe holder directly
    to l2. Also, important values are the lenght of the chipholder (14.75mm, l3)
    and the relative angle to l2 (30 degrees). You can directly change them in
    case you add somethin different, but be aware of what values you put in.
    If you have no holder at the end of the manipulator(what is normally NOT the 
    case), use class KleindiekCoordinates instead.
    """
    
    def __init__(self):
        #here are the lenghts of the arms of the manipulator.
        #standard: l1=21.0mm,l2=21.0mm,l3=14.75mm, theta3 = 30deg
        self.l1 = float(21.0)  #length of first arm
        self.l2 = float(21.0)  #length of second arm. this one is longer than from KleindiekCoordinates since the chipholder has an additional extension of 3mm
        self.l3 = float(14.75) #length of the chipholder to the front of the tip
        self.theta3 = float(30.0/360.0*2*math.pi) #the angle of the chip relatively to the extension arm, 30degree

        
    def forward(self,theta1,theta2,extension): #angles in degrees!!
        """
        The forward function translates the angles and the extension directly
        into coordinates X,Y,Z (in mm). The (0,0,0) is in the base of the 
        manipulator. If you have 0degree angle in theta1, it points towards the 
        x-axis.
        """
        # Values that are allowedd for theta1 and theta2 are +-90degrees, for extension 0-12mm
        # the inputs theta1, theta2 are in degrees! we will first 
        # convert them into radiants
        if -90.0 <= theta1 <= 90.0 and -90.0 <= theta2 <= 90.0:
            theta1 = float(theta1/360.0*2*math.pi)
            theta2 = float(theta2/360.0*2*math.pi)
            
        else:
            print "Theta1 or Theta2 not in range -90,90 degrees"
            return
        
        if 0.0 <= extension <= 12.0:
            extension = float(extension)
        else:
            print "Value for extension not allowed. Use values between 0-12(mm)"
            return

        #since the four point probe will produce another angle to the second joint
        #of the manipulator arm, one has to calculate the effective angle theta4
        #which will replace theta2
        theta4 = float(theta2-math.atan((self.l3*math.sin(self.theta3))/(self.l2+extension+self.l3*math.cos(self.theta3))))
        
        #to calculate X,Y,Z, one can use the following coordinates:
        #self.X = float(self.l1*math.cos(theta1) + (self.l2+self.l3*math.cos(self.theta3)+extension)*math.cos(theta1)*math.cos(theta4))
        X = self.l1*math.cos(theta1) + math.sqrt((self.l2+extension+self.l3*math.cos(self.theta3))**2+(self.l3*math.sin(self.theta3))**2)*math.cos(theta1)*math.cos(theta4)
        #self.Y = float(self.l1*math.sin(theta1) + (self.l2+self.l3*math.cos(self.theta3)+extension)*math.sin(theta1)*math.cos(theta4))
        Y = self.l1*math.sin(theta1) + math.sqrt((self.l2+extension+self.l3*math.cos(self.theta3))**2+(self.l3*math.sin(self.theta3))**2)*math.sin(theta1)*math.cos(theta4)
        #self.Z = float((self.l2+self.l3*math.cos(self.theta3)+extension)*math.sin(theta4))
        Z = math.sqrt((self.l2+extension+self.l3*math.cos(self.theta3))**2+(self.l3*math.sin(self.theta3))**2)*math.sin(theta4)
        
        #As a return, you will get the forward values X,Y,Z:
        self.forwardvalue = [X,Y,Z]
        return self.forwardvalue
    
    def reverse(self,X,Y,Z): #values in millimeters!!!
        """
        The reverse function translates absolute coordinates (X,Y,Z) directly
        into the angles theta1, theta2 and the extension of the manipulator.
        """
        
        #calculations:
        x1 = float(self.l1) #lenght of the first arm
        x2 = float(math.sqrt(X**2+Y**2)-x1) #how much is left in XY from the second joint to the end of the 4pp
        theta_diagonal = math.atan(Z/x2) #effective angle from second joint to the end of the 4pp
        diagonal1 = float(math.sqrt(x2**2+Z**2)) #diagonal from the second joint to the Z position
        
        # calculate theta1,theta2 and extension
        theta1 = float(math.atan(Y/X)) # this is the angle of the first joint
        ext = math.sqrt(diagonal1**2 - (self.l3*math.sin(self.theta3))**2)-self.l2-self.l3*math.cos(self.theta3) #extension value
        theta2 = theta_diagonal + math.atan((self.l3*math.sin(self.theta3))/(ext+self.l2+self.l3*math.cos(self.theta3))) #angle of second joint
        
        # As a return, you get a list of reverse[theta1,theta2,extension], in degrees and mm
        self.reversevalue = [round(math.degrees(theta1),6),round(math.degrees(theta2),6),round(ext,6)]
        return self.reversevalue
 
#Text KleindiekCoordinates:
#kd = KleindiekCoordinates()
#kd.forward(45,45,12)
#print kd.forwardvalue
#kd.reverse(kd.forwardvalue[0],kd.forwardvalue[1],kd.forwardvalue[2])
#print kd.reversevalue



# Test FourPointProbeCoordinates:      
#fpp = FourPointProbeCoordinates()
#fpp.forward(0,0,2)
#fpp.reverse(fpp.X,fpp.Y,fpp.Z)
#print "%s,%s,%s" %(fpp.X ,fpp.Y, fpp.Z)
#print fpp.reversevalue[0]
#print fpp.reversevalue[1]
#print fpp.reversevalue[2]
#print fpp.forwardvalue[2]
    