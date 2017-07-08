# -*- coding: utf-8 -*-
"""
Created on Wed Mar 16 16:25:07 2016

@author: Harsh
"""

"""
A game and simulation.
Please read article Bubblies
[Broken-link]
"""

import random
import math

def WinToss(p=0.5):
	"""
	Returns True with probability 'p'
	"""
	if random.random() <= p:
		return True
	else:
		return False

class Universe():
	
	
	#Origin at bottom left
	def bigBang(self,bubbly_seed=7 , height=1024 ,length=1024 ):
		self.height=height
		self.length=length
		self.bubbly_list=[]
		for i in range(bubbly_seed):
			new_x = int( random.random() * self.length )
			new_y = int( random.random() * self.height )
			new_pos = complex(new_x,new_y)
			new_bubbly = Bubbly(0,new_pos,1)
			self.bubbly_list.append(new_bubbly)
	
	def doTime(self):
		#1. growTurn
		#2. collision Check
		#3. Colliders fight
		#4. losers burst ,escapers burst
		
		print "Not Implemented fully Yet"
		#1
		self.growTurn()
		
	def growTurn(self):
		for bubbly in self.bubbly_list:
			bubbly.growBig()
	
	
	
	
	
	def inBox(self,thing):
		"""
		Accepts |Bubbly , complex point
		Returns |True if 'thing' is in Universe bounds
		"""
		
		#Origin at bottom left	
		
		if type(thing)==Bubbly:
			pos = thing.getPos()
			rad = thing.getRad()
			top = pos.imag + rad
			bottom = pos.imag - rad
			left  = pos.real - rad
			right =pos.real + rad
			
			if (top < self.height) and bottom > 0 and left > 0 and right < self.length :
				return True
			else :
				return False
		if type(thing) == complex :
			pos=thing			
			rad = 0
			top = pos.imag + rad
			bottom = pos.imag - rad
			left  = pos.real - rad
			right =pos.real + rad
			
			if top < self.height and bottom > 0 and left > 0 and right < self.length :
				return True
			else :
				return False
		
	def mapUniverse(self):
		s=''
		s+='\n height: '+str(self.height)
		s+='\n length: '+str(self.length)
		n=0
		for bubbly in self.bubbly_list:
			b=bubbly
			n+=1
			s+= '\n Bubbly %d : pos=%s , r=%s' %(n,b.getPos(),b.getRad())
		
		print s


class Bubbly(object):
	
	#Static Variables
	
	#default [constants]
	BASE_GROWTHRATE=1 
	POOF_PROB=0.1
	
	# MERGE_PROB + REBIRTH_PROB=1
	REBIRTH_PROB=0.5
	# ==>MERGE_PROB=1-REBIRTH_PROB
	
	
	#default starter [variables]
	baby_life_force = 1
	
	#Note operations will be done on lf,gr not the above variable
	
	
	
	
	def __init__(self,r=0, pos=complex(0,0), lf=baby_life_force):
		"""
		r  : radius     |int
		pos: position   |complex number
		lf : life_force |int
		"""
		#radius : int
		#position	: complex	number
		self.rad=r
		self.pos=pos
		
		#gr : growth_rate
		#lf : life_force
		
		self.lf=lf
		self.gr=self.BASE_GROWTHRATE * self.lf
		
	def getPos(self):
		return self.pos
	def getRad(self):
		return self.rad
	def getLf(self):
		return self.lf
	def getGr(self):
		return self.gr
		
	def addLf(self,extra_lf):
		self.lf += extra_lf
		self.gr = self.BASE_GROWTHRATE * self.lf
	def growBig(self):
		self.rad+=self.gr
		
	def doBurst(self):
		"""
		returns a tuple of (babies ,dropped_lf)
		"""
		#([baby_list],int(dropped life force))
		self.babies=[]
		self.dropped_lf=0
		
		while self.lf > 0:
			
					
			
			if WinToss(p=self.POOF_PROB):
				#no babies , nothing dropped
				self.lf -= 1
			else:
				if WinToss(p=self.REBIRTH_PROB):
					#Won Toss .Making Baby
					
					#Note : If life_force not sufficient ie lf<baby_life_force
					#	Choice 1: Abandon. Drop lf
					#	Choice 2: Make baby with leftover lf
					#	Choice 3: No baby but Consume lf
					
					if self.lf > self.baby_life_force:
						#Sufficient lf
						delta_x=(2*random.random()-1)*self.rad
						delta_y=(2*random.random()-1)*self.rad
						
						baby_pos= self.pos + complex(delta_x , delta_y)
						
						Baby = Bubbly(0 , baby_pos , self.baby_life_force)
						
						self.babies.append(Baby)
						
						self.lf -= self.baby_life_force
					else:
						#Using Choice 3
						self.babies += []
						self.lf -= self.baby_life_force
				else:
					#Lost Toss .Dropping lf
					self.dropped_lf += 1
					self.lf -= 1
				
		return (self.babies,self.dropped_lf)




from math import sqrt

# Determines whether two circles collide and, if applicable,
# the points at which their borders intersect.
# Based on an algorithm described by Paul Bourke:
# http://local.wasp.uwa.edu.au/~pbourke/geometry/2circle/
# Arguments:
#   P0 (complex): the centre point of the first circle
#   P1 (complex): the centre point of the second circle
#   r0 (numeric): radius of the first circle
#   r1 (numeric): radius of the second circle
# Returns:
#   False if the circles do not collide
#   True if one circle wholly contains another such that the borders
#       do not overlap, or overlap exactly (e.g. two identical circles)
#   An array of two complex numbers containing the intersection points
#       if the circle's borders intersect.
def IntersectPoints(P0, P1, r0, r1):
    if type(P0) != complex or type(P1) != complex:
        raise TypeError("P0 and P1 must be complex types")
    # d = distance
    d = sqrt((P1.real - P0.real)**2 + (P1.imag - P0.imag)**2)
    # n**2 in Python means "n to the power of 2"
    # note: d = a + b

    if d > (r0 + r1):
        return False
    elif d < abs(r0 - r1):
        return True
    elif d == 0:
        return True
    else:
        a = (r0**2 - r1**2 + d**2) / (2 * d)
        b = d - a
        h = sqrt(r0**2 - a**2)
        P2 = P0 + a * (P1 - P0) / d

        i1x = P2.real + h * (P1.imag - P0.imag) / d
        i1y = P2.imag - h * (P1.real - P0.real) / d
        i2x = P2.real - h * (P1.imag - P0.imag) / d
        i2y = P2.imag + h * (P1.real - P0.real) / d

        i1 = complex(i1x, i1y)
        i2 = complex(i2x, i2y)

        return [i1, i2]

def CompToStr(c):
    return "(" + str(c.real) + ", " + str(c.imag) + ")"

def PairToStr(p):
    return CompToStr(p[0]) + " , " + CompToStr(p[1])

def Test():
    ip = IntersectPoints

    i = ip(complex(0,0), complex(1, 0), 2, 2)
    s = ip(complex(0,0), complex(4, 0), 2, 2)

    print "Intersection:", PairToStr(i)
    print "Wholly inside:", ip(complex(0,0), complex(1, 0), 5, 2)
    print "Single-point edge collision:", PairToStr(s)
    print "No collision:", ip(complex(0,0), complex(5, 0), 2, 2)
