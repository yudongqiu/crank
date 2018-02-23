#!/usr/bin/env python
# -*- coding: utf-8 -*-

#================================================#
#| Minimum-energy one dimensional torsion scan  |#
#|         Yudong Qiu, Lee-Ping Wang            |#
#================================================#

import numpy as np

class DihedralGrid:
    def __init__(self, engine, dihedrals, grid_size, work_queue):
        self.engine = engine
        self.M = engine.molecule
        self.dihedrals = np.array(dihedrals, dtype=int)
        self.grid_size = grid_size
        self.work_queue = work_queue
        self.setup_grid()

class DihedralGrid_1D(DihedralGrid):

    def setup_grid(self):
        assert self.dihedrals.shape == (1,4), "1D dihedral scan should have shape (1,4)"
        self.grid = np.arange(-180, 180, self.grid_size, dtype=int) + self.grid_size

    def run_minimize(self, dih12=None, dih120=None, frame=0):
        """
        Run a single minimization job
        determine if the job has already been run and queue it up if necessary.
        """

    def launch_iteration(self):
        """ Launch an iteration (which looks like a wavefront propagation on the dihedral surface). """
        # We should not start any new calculations if there are already some running.
        if self.running: return 1
        # This list contains the phi-psi values and working directory of each minimization.
        self.optinfo = []
        if self.iteration == 0:
            # Run a constrained minimization for each geometry in the provided file.
            for i in range(len(self.M)):
                fy1, dnm = self.run_minimize(frame=i)
                self.optnext.append(([fy1],fy1))
                self.optinfo.append((fy1, dnm))
            print "Initializing, %i optimizations in this cycle" % (len(self.optnext))
            self.print_ascii_image()
        else:
            # These constrained minimizations should have been scheduled by read_minimize().
            print "Iteration %i, %ix4 optimizations in the queue" % (self.iteration, len(self.optnext))
            self.print_ascii_image()
            if len(self.optnext) == 0:
                print "Scan is finished"
                return 0
            for fys, fy0 in self.optnext:
                for fy in fys:
                    fy1, dnm = self.run_minimize(fy, fy0)
                    self.optinfo.append((fy1, dnm))
        # Clear the list of optimizations that need to be done next, because we just launched them.
        self.optnext = []
        self.running = 1
        return 1

    def finish(self):
        pass

class DihedralGrid_2D(DihedralGrid):
    def setup_grid(self):
        assert self.dihedrals.shape == (2,4)


def main():
    import argparse
    parser = argparse.ArgumentParser(description="Potential energy scan of dihedral angle from -180 to 180")
    parser.add_argument('inputfile', type=str, help='Input template file for engine to load. Initial coordinates will be used by default.')
    parser.add_argument('dihedral', type=int, nargs=4, help='4 atom indices that defines dihedral angle.')
    parser.add_argument('--init_coords', type=str, help='File contain a list of geometries, that will be used as multiple starting points, overwriting the geometry in input file.')
    parser.add_argument('-g' '--grid_size', type=int, default=15, help='Grid spacing for dihedral scan, i.e. every 15 degrees')
    parser.add_argument('-e', '--engine', type=str, default="psi4", choices=['qchem, psi4'], help='Engine for running scan')
    args = parser.parse_args()

    # initialize QM Engine for computing gradients
    from QMEngine import EnginePsi4, EngineQChem
    engine_dict = {'psi4': EnginePsi4, 'qchem': EngineQChem}
    engine = engine_dict[args.engine](args.inputfile)

    # use init_coords instead of input geometry from input file
    if args.init_coords:
        engine.molecule = Molecule(args.init_coords)

    # initialize a work_queue
    from WQtools import WorkQueue
    work_queue = WorkQueue()

    DG = DihedralGrid_1D(engine, dihedrals=[args.dihedral], args.grid_size, work_queue)

    while True:
        # Determine which new optimizations to start
        # and schedule them in the reservoir.
        if not DG.launch_iteration():
            DG.finish()
            break
        manage_wq()
        # Read the results for the sets of optimizations that are finished
        # and schedule new jobs if necessary.
        DG.read_iteration()
    print "Dihedral scan is finished!"

if __name__ == "__main__":
    main()
