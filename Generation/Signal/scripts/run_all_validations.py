#--------------------------------------------------------------
# Example : 
# python scripts/run_all_validations.py --base_dir Gridpacks/ --masses 3500,4000 --outputDir Validation
#--------------------------------------------------------------


import os
import re
import random

from argparse import ArgumentParser

parser = ArgumentParser()

parser.add_argument( '--base_dir', dest='base_dir', required=True, help='path to gridpacks' )
parser.add_argument( '--masses', dest='masses', default=None, help='comma separated list of masses to run on, defaults to all' )
parser.add_argument( '--widths', dest='widths', default=None, help='comma separated list of widths to run on, defaults to all' )
parser.add_argument( '--outputDir', dest='outputDir', default='/afs/cern.ch/work/j/jkunkle/public/CMS/Gridpacks/GenerateChargedResonances/Validation', help='Output directory' )
parser.add_argument( '--batch', dest='batch', default=False, action='store_true', help='submit to batch' )

options = parser.parse_args()

BASE_NAME = 'ChargedResonance'

def main() :

    all_gridpacks = []

    # find the gridpacks
    for gp in os.listdir( options.base_dir ) :
        if gp.count( 'tarball.tar.xz' ) :
            if not gp.count( 'ChargedResonance' ) :
                continue
            all_gridpacks.append( gp )

    select_masses = []
    if options.masses is not None :
        select_masses = [int(x) for x in options.masses.split(',') ]

    if not os.path.isdir( options.outputDir ) :
        os.makedirs( options.outputDir )


    for gp in all_gridpacks :

        print gp

        res = re.match( '(%s_(WGToLNu|WGToJJ)_M(\d{3,4})_width(\d{1,2}|\d{1}p\d{2}))_slc6_amd64_gcc481_CMSSW_7_1_30_tarball.tar.xz' %( BASE_NAME ), gp )
        basename = res.group(1)
        print res.group(4)
        if os.path.isdir( '%s/%s'  %( options.outputDir, basename )) :
            print 'Skipping existing directory %s' %( basename )
            continue

        os.makedirs('%s/%s'  %( options.outputDir, basename ))

        if select_masses :
            if int( res.group(3) ) not in select_masses :
                print 'Skipping gridpack ', gp
                continue
        if options.widths is not None :
            match_width = False
            for wid in options.widths.split(',') :
                if res.group( 4) == wid :
                    match_width = True
                    break

            if not match_width :
                continue

        commands_lhe = []
        commands_convert = []

        commands_lhe.append( 'mkdir -p %s/%s/Gridpack' %(options.outputDir, basename )  )
        commands_lhe.append( 'cp %s/%s %s/%s/Gridpack' %( options.base_dir, gp, options.outputDir, basename ) )
        commands_lhe.append( 'cd CMSSW_8_0_12/' )
        commands_lhe.append( 'eval `scram runtime -sh`' )
        commands_lhe.append( 'cd %s/%s/Gridpack' %(options.outputDir, basename ) )
        commands_lhe.append( 'tar -xf %s' %(gp) )
        commands_lhe.append( './runcmsgrid.sh 10000 %d 4 ' %( random.randint(1, 100000) ) )


        if not options.batch :
            all_commands = ' ; ' .join( commands_lhe )
            print all_commands
            os.system( all_commands )

        commands_convert.append( 'cd /afs/cern.ch/work/j/jkunkle/public/CMS/Gridpacks/GenerateChargedResonances/CMSSW_5_3_22_patch1 ' )
        commands_convert.append( 'eval `scram runtime -sh`' )
        commands_convert.append( 'cd .. ' )
        commands_convert.append( './MadGraph/MG5_aMC_v2_3_3/ExRootAnalysis/ExRootLHEFConverter %s/%s/Gridpack/cmsgrid_final.lhe %s/%s/Gridpack/LHEevents.root ' %( options.outputDir, basename, options.outputDir, basename ) )
        commands_convert.append( 'python scripts/make_valid_hists.py --input %s/%s/Gridpack/LHEevents.root --output %s/%s/validation.root ' %( options.outputDir, basename, options.outputDir, basename ) )
        commands_convert.append( 'rm -rf %s/%s/Gridpack ' %( options.outputDir, basename ) )
        
        if not options.batch :
            all_commands = ' ; ' .join( commands_convert )
            print all_commands
            os.system( all_commands )

        if options.batch :

            file_name = '%s/%s/run.sh' %( options.outputDir, basename )
            ofile = open( file_name, 'w' )

            ofile.write( '!#/bin/bash \n' )

            for line in commands_lhe :
                ofile.write( '%s \n' %line )
            for line in commands_convert :
                ofile.write( '%s \n' %line )

            ofile.close()

            os.system( 'chmod 777 %s' %file_name )

            os.system( 'bsub -q 1nh %s ' %file_name )




main()
