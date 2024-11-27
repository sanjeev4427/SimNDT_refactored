#!/usr/bin/env python
# encoding: utf-8
"""
simPack.py

Created by Miguel Molero on 2013-10-01.
Copyright (c) 2013 MMolero. All rights reserved.
"""

class SimPack:
    
    def __init__(self, scenario, materials, boundary, inspection, source, transducers, \
        			signal, simulation, geom_objects, receivers, snapShots):
        """
        Initializes the SimPack class with the provided simulation components.
        
        Parameters:
        - scenario: The scenario object.
        - materials: List of material objects.
        - boundary: List of boundary condition objects.
        - inspection: The inspection object.
        - source: The source object.
        - transducers: List of transducer objects.
        - signal: The signal object.
        - simulation: The simulation object.
        - SimNDT_geom_objects: List of geometric objects.
        - SimNDT_Receivers: The receivers object.
        - SimNDT_SnapShots: The snapshots object.
        """
        self.Boundary = boundary
        self.Inspection = inspection
        self.Source = source
        self.Materials = materials
        self.Transducers = transducers
        self.Simulation = simulation
        self.Scenario = scenario
        self.Signal = signal
        self.Geom_objects = geom_objects
        self.Receivers = receivers
        self.SnapShots = snapShots

