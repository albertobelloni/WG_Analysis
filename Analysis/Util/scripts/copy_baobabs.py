import pickle
import os

from argparse import ArgumentParser

parser = ArgumentParser()

parser.add_argument( '--outputBase', dest='outputBase', default=None, required=True, help='path where output files will go' )
parser.add_argument( '--fileList', dest='fileList', default=None, required=True, help='path to file containing list of files' )

options = parser.parse_args()

veto_dirs = [
            'crab_DoubleEG-0001',
            'crab_DoubleEG-0002',
            'crab_DoubleEG-0003',
            'crab_DoubleEG-0004',
            'crab_DoubleMuon-0001',
            'crab_DoubleMuon-0002',
            'crab_DoubleMuon-0003',
            'DYJetsToLL_M-50_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8',
            'GJet_Pt-15ToInf_TuneCUETP8M1_13TeV-pythia8',
            'TT_TuneCUETP8M1_13TeV-powheg-pythia8',
            'WGToLNuG_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8',
            'WJetsToLNu_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8',
            'ZGTo2LG_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8',
]

keep_dirs = [
            'DiPhotonJetsBox_M40_80-Sherpa',
            'DiPhotonJetsBox_MGG-80toInf_13TeV-Sherpa',
]

def main() :

    ofile = open( options.fileList ) 

    file_list = pickle.load( ofile )

    paired_file_list = format_files_for_copy( file_list, options.outputBase, veto_dirs, keep_dirs )

    for remote, local in paired_file_list :

        local_dir = os.path.dirname( local )

        if os.path.isfile( local ) :
            print 'File Exists! %s ' %local
            continue

        if not os.path.isdir( local_dir ) :

            os.makedirs( local_dir )


        copy_command = 'xrdcp %s %s ' %( remote, local )

        print copy_command
        os.system( copy_command )



def format_files_for_copy( file_list, output_base, veto_dirs,keep_dirs ) :

    copy_files = []
    for f in file_list :

        dir_paths = f.split('/')

        # do the veto
        if ( set( dir_paths ) & set( veto_dirs ) ) :
            continue

        # do the keep
        if not ( set(dir_paths) & set( keep_dirs ) ) :
            continue

        # now find out where to start the directory output
        ntuple_idx = dir_paths.index('Ntuple')

        out_path = output_base + '/'.join(dir_paths[ntuple_idx+1:])

        copy_files.append( ('root://eoscms.cern.ch/%s' %f, out_path ) )


    return copy_files






main()
