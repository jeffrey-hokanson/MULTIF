#!/usr/bin/env python

import os, time, sys, shutil, copy



from optparse import OptionParser
import textwrap

import multif
from multif import SU2



# -------------------------------------------------------------------
#  Main 
# -------------------------------------------------------------------

def main():
	 
	sys.stdout.write('-' * 90);
	sys.stdout.write('\n');
	sys.stdout.write('\t __  __ _   _ _  _____ ___         ___ \t\n') ;
	sys.stdout.write('\t|  \/  | | | | ||_   _|_ _|  ___  | __|\t\n');
	sys.stdout.write('\t| |\/| | |_| | |__| |  | |  |___| | _| \t\t Dev. : R. Fenrich & V. Menier\n');
	sys.stdout.write('\t|_|  |_|\___/|____|_| |___|       |_|  \t\t        Stanford University\n\n');
	sys.stdout.write('-' * 90);
	sys.stdout.write('\n\n');
	
	# Command Line Options
	parser = OptionParser()
	parser.add_option("-f", "--file", dest="filename",
	                  help="read config from FILE", metavar="FILE")
	parser.add_option("-n", "--partitions", dest="partitions", default=0,
	                  help="number of PARTITIONS", metavar="PARTITIONS")
	
	parser.add_option("-l", "--flevel", dest="flevel", default=-1,
	                  help="fidelity level to run", metavar="FLEVEL")	

	parser.add_option('-i', '--iter', dest='maxiter', default = 300, help = "SU2 maxiter")

	parser.add_option('-c', '--convergence', dest = 'convergence', default = 3, help = "SU2 convergence order")
	
	(options, args)=parser.parse_args()
	
	options.partitions = int( options.partitions )
	options.flevel     = int( options.flevel )
	options.maxiter    = int( options.maxiter)
	options.convergence = int(options.convergence)
	
	if options.flevel < 0 :
		sys.stderr.write("  ## ERROR : Please choose a fidelity level to run (option -l or --flevel)");
		sys.exit(0);
	
	nozzle = multif.nozzle.NozzleSetup( options.filename, options.flevel );
	nozzle.su2_convergence_order = options.convergence 	
	### HACK
	#multif.MEDIUMF.AEROSPostProcessing(nozzle);
	#sys.exit(1);
	
	if nozzle.method == 'NONIDEALNOZZLE' :
		multif.LOWF.Run(nozzle);
	elif nozzle.method == 'EULER' or nozzle.method == 'RANS':
		multif.MEDIUMF.Run(nozzle, maxiter = options.maxiter);
		
	# --- Output functions 
	
	#nozzle.WriteOutputFunctions_Plain ();
	nozzle.WriteOutputFunctions_Dakota ();
	
	sys.stdout.write('\n');
	
	# --- Print warning in case the wrong SU2 version was run
	if nozzle.method != 'NONIDEALNOZZLE' and nozzle.SU2Version != 'OK':
		sys.stdout.write('\n');
		sys.stdout.write('#' * 90);
		sys.stdout.write('\n  ## WARNING : You are not using the right version of SU2. This may have caused robustness issues.\n');
		sys.stdout.write('#' * 90);
		sys.stdout.write('\n\n');
	
# -------------------------------------------------------------------
#  Run Main Program
# -------------------------------------------------------------------

if __name__ == '__main__':
    main()
