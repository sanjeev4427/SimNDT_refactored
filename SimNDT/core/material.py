#!/usr/bin/env python
# encoding: utf-8
"""
material.py

Created by Miguel Molero on 2013-09-11.
Copyright (c) 2013 MMolero. All rights reserved.
"""

from math import sqrt


class Material:

	def __init__(self, name="Water",rho=1000,c11=2.19e9,c12=2.19e9,c22=2.19e9,c44=1e-30,label=0, damping = False, eta_v=1e-30, eta_s = 1e-30):
		
		self.Name	 =  name
		self.Rho	 =  rho
		self.C11	 =  c11
		self.C12	 =  c12
		self.C22	 =  c22
		self.C44	 =  c44
		self.VL		 =  sqrt( c11/rho )
		self.VT		 =  sqrt( c44/rho )
		self.Label	 =  label
		self.Eta_v   =  eta_v
		self.Eta_s   =  eta_s
		self.Damping =  damping

		
	def __str__(self):
		# return "Material:"
		return "Material(Name={Name}, Rho={Rho}, C11={C11}, C12={C12}, C22={C22}, C44={C44}, VL={VL}, VT={VT}, Label={Label}, Damping={Damping}, Eta_v={Eta_v}, Eta_s={Eta_s})".format(
			Name=self.Name, Rho=self.Rho, C11=self.C11, C12=self.C12, C22=self.C22, C44=self.C44, VL=self.VL, VT=self.VT, Label=self.Label, Damping=self.Damping, Eta_v=self.Eta_v, Eta_s=self.Eta_s)

	def __repr__(self):
		# return "Material:"
		return "Material Properties: (Name={Name}, Rho={Rho}, C11={C11}, C12={C12}, C22={C22}, C44={C44}, VL={VL}, VT={VT}, Label={Label}, Damping={Damping}, Eta_v={Eta_v}, Eta_s={Eta_s})".format(
			Name=self.Name, Rho=self.Rho, C11=self.C11, C12=self.C12, C22=self.C22, C44=self.C44, VL=self.VL, VT=self.VT, Label=self.Label, Damping=self.Damping, Eta_v=self.Eta_v, Eta_s=self.Eta_s)