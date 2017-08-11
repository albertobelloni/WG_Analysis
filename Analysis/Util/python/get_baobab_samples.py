
import pickle
from eos_utilities import walk_eos

from argparse import ArgumentParser


parser = ArgumentParser()

parser.add_argument( '--baseDir', dest='baseDir', default=None, required=True, help='path to Baobab base directory' )
parser.add_argument( '--version', dest='version', default=None, required=True, help='Baobab version' )

options = parser.parse_args()


def main() :


    mc_path   = '%s/MC/%s/Ntuple' %( options.baseDir, options.version )
    data_path = '%s/Data/%s/Ntuple' %( options.baseDir, options.version )

    data_files = []
    for top, dirs, files, sizes in walk_eos( data_path ) :
        for f in files :
            data_files.append( '%s/%s' %( top, f ) )

    mc_files = []
    for top, dirs, files, sizes in walk_eos( mc_path ) :
        for f in files :
            mc_files.append( '%s/%s' %( top, f ) )

    all_files = data_files + mc_files

    outfile = open('files.pickle', 'w' )
    pickle.dump( all_files, outfile )
    outfile.close()














main()
