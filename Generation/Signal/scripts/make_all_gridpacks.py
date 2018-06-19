import os
import re

from argparse import ArgumentParser

parser = ArgumentParser()

parser.add_argument( '--proc_dir', dest='proc_dir', required=True , help='Path to proc directory (genproductions/bin/MadGraph5_aMCatNLO/)' )
parser.add_argument( '--card_dir', dest='card_dir', required=True , help='Path to card directory relative to proc directory' )
parser.add_argument( '--masses', dest='masses', default=None , help='comma separated list of masses (will make all masses by default)' )
parser.add_argument( '--widths', dest='widths', default=None , help='comma separated list of widths (will make all widths by default)' )
parser.add_argument( '--lepOnly', dest='lepOnly', default=False, action='store_true', help='only run the lepton final state' )
parser.add_argument( '--hadOnly', dest='hadOnly', default=False, action='store_true', help='only run the hadronic final state' )
parser.add_argument( '--checkExisting', dest='checkExisting', default=False, action='store_true', help='Dont run if the gridpack exists' )
parser.add_argument( '--batch', dest='batch', default=False, action='store_true', help='run on batch (makes submit directory)' )

options = parser.parse_args()

BASE_NAME = 'ChargedResonance'

def main() :

    abs_proc_dir = os.path.abspath( options.proc_dir )

    #make Gridpacks directory
    if not os.path.isdir( 'Gridpacks' ) :
        print 'Making Gridpacks directory'
        os.mkdir( 'Gridpacks')

    accept_masses = []
    if options.masses is not None :
        accept_masses = [ int(x) for x in options.masses.split(',')]

    accept_widths = []
    if options.widths is not None :
        accept_widths = [ int(x) for x in options.widths.split(',')]

    all_cards = []

    for dirname in os.listdir( abs_proc_dir+'/'+options.card_dir ) :
        res = re.match( '%s_(WGToLNu|WGToJJ)_M(\d{3,4})_width(\w+)' %( BASE_NAME ), dirname )
        if res is not None :
            if accept_masses :
                dirmass = int(res.group( 2 ))

                if dirmass not in accept_masses :
                    continue

            if accept_widths :
                width = res.group(3)
                if width not in accept_widths :
                    continue


            if options.lepOnly and res.group(1) == 'WGToJJ'  :
                continue
            if options.hadOnly and res.group(1) == 'WGToLNu'  :
                continue


            all_cards.append( dirname )

    sample_commands = {}

    for card in all_cards :

        if options.checkExisting :
            output_path = 'Gridpacks/%s_slc6_amd64_gcc481_CMSSW_7_1_30_tarball.tar.xz' %(  card ) 

            if os.path.isfile( output_path ) :
                print 'Skipping existing gripack ', output_path
                continue

        res = re.match( '%s_(WGToLNu|WGToJJ)_M(\d{3,4})_width(\w+)' %( BASE_NAME ), card )
        width = None
        if res is not None :
            width = res.group(3)

        if width is None : 
            print 'Cannot detemine width for card %s, will not produce gridpack!' %card
            continue

        commands = []

        commands.append( 'cd %s' %abs_proc_dir )
        commands.append( './gridpack_generation_exo.sh  %s %s/%s local ALL %s ' %( card, options.card_dir, card, width ) )
        commands.append( 'cd ../../..'  )
        commands.append( 'rm -rf %s/%s ' %( abs_proc_dir, card ) )
        commands.append( 'mv %s/%s.log Gridpacks/%s.log' %( abs_proc_dir, card, card) )
        commands.append( 'mv %s/%s_slc6_amd64_gcc481_CMSSW_7_1_30_tarball.tar.xz Gridpacks/%s_slc6_amd64_gcc481_CMSSW_7_1_30_tarball.tar.xz' %( abs_proc_dir, card, card ) )

        sample_commands[card] = ';'.join(commands)

    if options.batch : 

        if not os.path.isdir( 'submit' ) :
            os.mkdir( 'submit' )

        for name, cmnd in sample_commands.iteritems() :

            run_file = open('submit/run_%s.sh' %name, 'w')

            run_file.write( cmnd )

            run_file.close()

            os.system('chmod 777 submit/run_%s.sh' %name )

            os.system('bsub -q 8nh %s/submit/run_%s.sh ' %(os.getcwd(),name) ) 

    else :

        for cmnd in sample_commands.values() : 
            print cmnd 
            os.system( cmnd )

main()

