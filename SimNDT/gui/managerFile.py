__author__ = 'Miguel Molero'

import os
from PySide.QtCore import *
from PySide.QtGui import *


def fileNew(filename):

	dir = os.path.dirname(filename) if filename is not None else "."
	formats = ["*.%s" % "sim","*.%s" % "json"]
	fname = None
	fname, filters = QFileDialog.getSaveFileName(None, "New Simulation File (.sim/.json)", dir,"sim Files (%s)"%" ".join(formats))
	return fname



def fileOpen(filename):

	dir = os.path.dirname(filename) if filename is not None else "."
	formats = ["*.%s" % "sim","*.%s" % "json"]
	fname, filters = QFileDialog.getOpenFileName(None,"Open Simulation File (.sim/.json)", dir,"sim Files (%s)"%" ".join(formats))
	return fname



def fileSaveAs(filename):

	fname = filename if filename is not None else "."
	formats = ["*.%s" % "sim","*.%s" % "json"]
	fname, filters = QFileDialog.getSaveFileName(None, "Save Simulation File As (.sim/.json)", fname,"sim Files (%s)"%" ".join(formats))
	return fname




def exportMatlab(filename):

	print (filename)
	if filename is not None:
		fname  = os.path.splitext(filename)[0]
	else:
		fname = "."


	formats = ["*.%s" % "mat"]
	fname, filters = QFileDialog.getSaveFileName(None, "Export Simulation in (.mat) File", fname,".mat Files (%s)"%" ".join(formats))
	return fname

def importJSON(filename):

	print (filename)
	if filename is not None:
		fname  = os.path.splitext(filename)[0]
	else:
		fname = "."


	formats = ["*.%s" % "json"]
	fname, filters = QFileDialog.getOpenFileName(None, "Import Simulation from (.json) File", fname,".json Files (%s)"%" ".join(formats))
	return fname
	
def exportJSON(filename):

	print (filename)
	if filename is not None:
		fname  = os.path.splitext(filename)[0]
	else:
		fname = "."


	formats = ["*.%s" % "json"]
	fname, filters = QFileDialog.getSaveFileName(None, "Export Simulation in (.json) File", fname,".json Files (%s)"%" ".join(formats))
	return fname



