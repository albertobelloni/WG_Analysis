import os
import re
from argparse import ArgumentParser

parser = ArgumentParser()

parser.add_argument( '--widthsHad', dest='widthsHad', default=None, help='comma separated list of widths to produce for hadronic samples' )
parser.add_argument( '--widthsLep', dest='widthsLep', default=None, help='comma separated list of widths to produce for leptonic samples' )
parser.add_argument( '--nevtHad', dest='nevtHad', default=20000, help='Number of events to run for hadronic samples' )
parser.add_argument( '--nevtLep', dest='nevtLep', default=20000, help='Number of events to run for leptonic samples' )
parser.add_argument( '--hadOnly', dest='hadOnly', default=False, action='store_true', help='make the list for only hadronic samples' )
parser.add_argument( '--lepOnly', dest='lepOnly', default=False, action='store_true', help='make the list for only leptonic samples' )
parser.add_argument( '--madgraphOnly', dest='madgraphOnly', default=False, action='store_true', help='make the list for only madgraph samples' )
parser.add_argument( '--pythiaOnly', dest='pythiaOnly', default=False, action='store_true', help='make the list for only pythia samples' )
parser.add_argument( '--prioritize', dest='prioritize', default=False, action='store_true', help='put priority samples on top' )

options = parser.parse_args()

BASE_NAME = 'MadGraphChargedResonance'
PWD = os.path.dirname(os.path.realpath(__file__))

def main() :

    selected_gp = []
    priority_gp = []

    for gp in os.listdir( '%s/../Gridpacks' %PWD ) : 

        res = re.match( '(%s_(WGToLNuG|WGToJJG)_M(\d{3,4})_width(\d{1,2}|\dp\d{2}))_slc6_amd64_gcc481_CMSSW_7_1_30_tarball.tar.xz' %( BASE_NAME ), gp )

        if res is not None :

            if options.hadOnly and res.group(2) == 'WGToLNuG' :
                continue
            if options.lepOnly and res.group(2) == 'WGToJJG' :
                continue

            if res.group(2) == 'WGToLNuG' and options.widthsLep is not None :
                matches_width_lep = False
                for testw in options.widthsLep.split(',') :
                    if res.group(4) == testw :
                        matches_width_lep = True
                        break
                if not matches_width_lep :
                    continue

            if res.group(2) == 'WGToJJG' and options.widthsHad is not None :
                matches_width_had = False
                for testw in options.widthsHad.split(',') :
                    if res.group(4) == testw :
                        matches_width_had = True
                        break
                if not matches_width_had :
                    continue

            should_prioritize = True
            if not (res.group(4) == '0p01') :
                should_prioritize = False
            if not ( int(res.group(3))%100 == 0 ) :
                should_prioritize = False
            if not ( int(res.group(3))%200 == 0 ) :
                should_prioritize = False


            if options.prioritize and should_prioritize :
                priority_gp.append( ( int(res.group(3)), gp, res.group(1) )  )
            else :
                selected_gp.append( ( int(res.group(3)), gp, res.group(1) ) )

    priority_gp.sort()
    selected_gp.sort()

    if not options.pythiaOnly :

        make_madgraph_entries( priority_gp )

    if not options.madgraphOnly :

        make_pythia_entries( priority_gp )


    if not options.pythiaOnly :

        make_madgraph_entries( selected_gp )

    if not options.madgraphOnly :

        make_pythia_entries( selected_gp )



def make_madgraph_entries( selected_gp ) :

    for mass, gp, name in selected_gp :

        row_entries = []

        row_entries.append( name )
        if name.count( 'WGToJJG' ) :
            row_entries.append( str( options.nevtHad ) )
        if name.count( 'WGToLNuG' ) :
            row_entries.append( str( options.nevtLep ) )

        row_entries.append( 'Madgraph' )
        row_entries.append( '=HYPERLINK("https://github.com/cms-sw/genproductions/blob/master/python/ThirteenTeV/Hadronizer/Hadronizer_TuneCP5_13TeV_generic_LHE_pythia8_cff.py","Hadronizer_TuneCP5_13TeV_generic_LHE_pythia8_cff.py")' )
        row_entries.append( '%s/Gridpacks/%s' %( '/'.join(PWD.split('/')[:-1]), gp ) )

        row = ' | '.join( row_entries )

        print row

def make_pythia_entries( selected_gp ) :

   for mass, gp, name in selected_gp :

       row_entries = []

       pythia_name = name.replace('MadGraph', 'Pythia')

       row_entries.append( pythia_name )

       if name.count( 'WGToJJG' ) :
           row_entries.append( str( options.nevtHad ) )
       if name.count( 'WGToLNuG' ) :
           row_entries.append( str( options.nevtLep ) )


       row_entries.append( 'Pythia' )
       row_entries.append( '%s/PythiaChargedResonance/%s_13TeV-pythia8_cff.py' %('/'.join(PWD.split('/')[:-1]), pythia_name ) )
       row_entries.append( '' )
       row_entries.append( '' )

       row = ' | '.join( row_entries )

       print row



main()
