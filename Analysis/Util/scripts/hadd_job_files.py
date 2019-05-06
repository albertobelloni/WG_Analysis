import os
from argparse import ArgumentParser

def main() :

    parser = ArgumentParser()
    parser.add_argument( '--path', dest='path', default=None, required=True, help='Path to directory having job directories to combine' )
    parser.add_argument( '--factor', dest='factor', type=int, default=10, help='Reduction factor' )

    options = parser.parse_args()

    # assume that the files are local 

    if not os.path.isdir( options.path ) :
        print 'Could not find input dir'
        return

    job_dirs = []
    job_files = []
    for dir in os.listdir( options.path ) :
        if dir.count('Job_') and os.path.isdir( options.path + '/' + dir ) :
            found_files = []
            for file in os.listdir( options.path + '/' + dir ) :
                if file.count('.root') :
                    found_files.append( file )

            if not len( found_files ) == 1 :
                print 'Did not find one root file in job directory!'

            job_files.append( found_files[0] )
            job_dirs.append( options.path + '/' + dir )

    uniq_job_files = list( set( job_files ) )
    if not len(uniq_job_files) == 1 :
        print 'Found multiple names for files to hadd!'
        print 'This functionality is not supported!'
        return

    # divide by the reduction factor
    # need to be careful when the
    # number of files is not a multiple
    # of the reduction factor
    #new_n_jobs = 0
    #if len(job_dirs) % options.factor == 0 :
    #    new_n_jobs = len(job_dirs)/options.factor
    #else :
    #    new_n_jobs = int(len(job_dirs)/float(options.factor))+1
    #if new_n_jobs == 0 :
    #    new_n_jobs = 1

    split_jobs = [job_dirs[i:i+options.factor] for i in range(0, len(job_dirs), options.factor)]

    new_idxs = []
    for idx, files in enumerate(split_jobs) :
        new_idxs.append(idx)
        output_dir = 'NewJob_%04d' %idx
        files_str = ' '.join( [ '%s/%s' %( f, uniq_job_files[0] ) for f in files ] )
        hadd_str = 'hadd %s/%s/%s %s' %( options.path, output_dir, uniq_job_files[0], files_str )

        #os.mkdir( '%s/%s' %( options.path, output_dir ) )

        #os.system( hadd_str )


    # remove old job files
    for job_dir in job_dirs :
        os.system( 'rm -rf %s' %job_dir )

    for ni in new_idxs :
        mv_cmd = 'mv %s/NewJob_%04d %s/Job_%04d' %( options.path, ni, options.path, ni )
        os.system( mv_cmd )




if __name__ == '__main__' :
    main()
