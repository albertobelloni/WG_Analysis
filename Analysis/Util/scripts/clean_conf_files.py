
import sys
import os
import eos_utilities as eosutil
from argparse import ArgumentParser

p = ArgumentParser()

p.add_argument( '--path', dest='path', default=None, 
                 help='Path to directory containing analysis configuration files' )

options = p.parse_args()

def main() :


    if options.path is None :
        print 'Must provide a path'
        sys.exit(-1)

    top_dir = options.path.split('/')[-1]
    output_file = 'anaysis_config_all.txt'
    output_path='/tmp/jkunkle/%s/%s' %(top_dir, output_file)

    # gahter a list of files
    ana_files = []
    if options.path.count( '/eos' ) :
        dirs, files, sizes = eosutil.parse_eos_dir( options.path ) 
        for file in files :
            if file.count('.txt') :
                ana_files.append( options.path + '/' + file )

        # if the output file is in the 
        # list of input files, remove it
        # so it is not removed from 
        # disk
        if len(ana_files) < 2 :
            print 'It looks like files have already been combined.  Will abort.'
            return

        # sort the files so they have some reasonable ordering
        ana_files.sort()

        if output_file in ana_files :
            print 'Output file already in list of input files.  Has the script already been run on this directory?'
            ana_files.remove( output_file )

        print 'Will combine %d files' %len(ana_files)

        # copy files locally
        for filepath in ana_files :
            filename = filepath.split('/')[-1]
            eosutil.copy_eos_to_local( filepath, '/tmp/jkunkle/%s/%s' %(top_dir, filename) )

        print 'files copied locally'

        ## cat the files
        for filepath in ana_files :
            filename = filepath.split('/')[-1]

            os.system( 'echo "%s" >> %s' %(filename, output_path) )
            os.system( 'cat /tmp/jkunkle/%s/%s >> %s' %(top_dir, filename, output_path) )
            os.system( 'echo "" >> %s' %(output_path) )
            os.system( 'echo "" >> %s' %(output_path) )

        print 'catted files'

        eosutil.copy_eos_to_local( output_path, options.path +'/' + output_file )
        
        print 'copied output file to eos'

        # delete original file
        for filepath in ana_files :
            eosutil.rm_eos( filepath )

        print 'deleted %d files from eos' %len(ana_files)
        print '\033[1;32m^.^ FINISHED ^.^\033[0m'

    else :
        wrapper_files = []
        for top, dirs, files in os.walk( options.path ) :
            for file in files :
                if file.count('.txt') :
                    ana_files.append( top + '/' + file )

                elif file.count('wrapper') :
                    wrapper_files.append( top + '/' + file )

        # if the output file is in the 
        # list of input files, remove it
        # so it is not removed from 
        # disk
        if len(ana_files) < 2 :
            print 'It looks like files have already been combined.  Will abort.'
            return

        # sort the files so they have some reasonable ordering
        ana_files.sort()

        print 'Will combine %d files' %len(ana_files)

        if output_file in ana_files :
            print 'Output file already in list of input files.  Has the script already been run on this directory?'
            ana_files.remove( output_file )

        # cat the files
        for filepath in ana_files :
            filename = filepath.split('/')[-1]
            os.system( 'echo  "%s" >> %s/%s ' %( filename, options.path, output_file ) )
            os.system( 'cat %s >> %s/%s' %(filepath, options.path, output_file) ) 
            os.system( 'echo "" >> %s/%s' %(options.path, output_file) )
            os.system( 'echo "" >> %s/%s' %(options.path, output_file) )

        # delete original file
        for filepath in ana_files+wrapper_files :
            os.system( 'rm %s ' %filepath )

        print 'deleted %d files ' %(len(ana_files)+len(wrapper_files))
        print '\033[1;32m^.^ FINISHED ^.^\033[0m'








    
main()
