import os
import re
import sys
import random

from argparse import ArgumentParser

parser = ArgumentParser()

parser.add_argument( '--masses', dest='masses', default=None, help='comma separated list of masses to run on' )
parser.add_argument( '--widths', dest='widths', default=None, help='comma separated list of widths to run on' )
parser.add_argument( '--outputDir', dest='outputDir', default='/afs/cern.ch/work/j/jkunkle/public/CMS/Gridpacks/GenerateChargedResonances/Validation', help='Output directory' )
parser.add_argument( '--batch', dest='batch', default=False, action='store_true', help='submit to batch' )

options = parser.parse_args()

BASE_NAME = 'ChargedResonance'

ALL_MASSES = [200, 250, 300, 350, 400, 450, 500, 600, 700, 800, 900, 1000, 1200, 1400, 1600, 1800, 2000, 2200, 2400, 2600, 2800, 3000, 3500, 4000]
ALL_WIDTHS = [0.01, 5.0, 10.0, 20.0]

def main() :

    all_samples = []

    if not os.path.isdir( options.outputDir ) :
        os.makedirs( options.outputDir )


    for mass in ALL_MASSES :

        for width in ALL_WIDTHS :

            if width < 1 : 
                width_name = '0p01'
            else :
                width_name = '%d' %width

            name = 'PythiaChargedResonance_WGToLNu_M%d_width%s' %( mass, width_name )

            if os.path.isdir( '%s/%s'  %( options.outputDir, name )) :
                print 'Skipping existing directory %s' %( name )
                continue

            os.makedirs('%s/%s'  %( options.outputDir, name ))

            commands_setup = []
            commands_pythia = []
            commands_convert = []

            commands_setup.append( 'mkdir -p %s/%s' %(options.outputDir, name )  )
            commands_setup.append( 'cp ~/Programs/pythia8219/examples/scalarWA.cmnd %s/%s/scalarWA.cmnd.orig' %(options.outputDir, name )  )

            all_commands = ' ; '.join( commands_setup )
            print all_commands
            os.system( all_commands )

            # now modify the card
            infile = open( '%s/%s/scalarWA.cmnd.orig' %( options.outputDir, name ), 'r' )
            outfile = open( '%s/%s/scalarWA.cmnd' %( options.outputDir, name ), 'w' )

            for line in infile :

                if line.count ( 'Main:numberOfEvents' ) :
                    outfile.write( 'Main:numberOfEvents = 100000 \n' ) 
                elif line.count( '37:m0' ) :
                    outfile.write( '37:m0 = %d \n' %mass )
                elif line.count( '37:mWidth' ) :
                    outfile.write( '37:mWidth = %f \n' %( mass * float( width )/100 ) )
                else :
                    outfile.write( line )

            infile.close()
            outfile.close()


            commands_pythia.append( 'cd  %s/%s/' %( options.outputDir, name ) )
            commands_pythia.append( '~/Programs/pythia8219/examples/main16 scalarWA.cmnd >> pythialog.txt' )


            if not options.batch :
                all_commands = ' ; ' .join( commands_pythia )
                print all_commands
                os.system( all_commands )

            commands_convert.append( 'cd /afs/cern.ch/work/j/jkunkle/public/CMS/Gridpacks/GenerateChargedResonances/CMSSW_5_3_22_patch1 ' )
            commands_convert.append( 'eval `scram runtime -sh`' )
            commands_convert.append( 'cd .. ' )
            commands_convert.append( './MadGraph/MG5_aMC_v2_3_3/ExRootAnalysis/ExRootLHEFConverter %s/%s/scalarWA.lhe %s/%s/LHEevents.root ' %( options.outputDir, name, options.outputDir, name ) )
            commands_convert.append( 'python scripts/make_valid_hists.py --input %s/%s/LHEevents.root --output %s/%s/validation.root ' %( options.outputDir, name, options.outputDir, name ) )
            commands_convert.append( 'rm  %s/%s/scalarWA.lhe ' %( options.outputDir, name ) )
            commands_convert.append( 'rm  %s/%s/LHEevents.root ' %( options.outputDir, name ) )
            
            if not options.batch :
                all_commands = ' ; ' .join( commands_convert )
                print all_commands
                os.system( all_commands )

            if options.batch :

                file_name = '%s/%s/run.sh' %( options.outputDir, name )
                ofile = open( file_name, 'w' )

                ofile.write( '#!/bin/bash \n' )

                for line in commands_pythia :
                    ofile.write( '%s \n' %line )
                for line in commands_convert :
                    ofile.write( '%s \n' %line )

                ofile.close()
                os.system( 'chmod 777 %s ' %file_name )

                os.system( 'bsub -q 8nm %s ' %file_name )




main()
