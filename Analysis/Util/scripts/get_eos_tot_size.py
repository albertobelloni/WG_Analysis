
import eos_utilities as eosutil


def main() :
    from argparse import ArgumentParser
    parser = ArgumentParser()
    parser.add_argument('--dir', dest='dir', default=None, required=True, help='Base directory for which the total size is computed' )
    options = parser.parse_args()

    tot_size, subdir_sizes = get_eos_tot_size( options.dir )

    sorted_sizes = []
    for dir, size in subdir_sizes.iteritems( ) :
        sorted_sizes.append( (size, dir) )

    sorted_sizes.sort()

    for size, dir in reversed(sorted_sizes) :

        conv_size = size/(1024*1024*1024.0)

        print 'Size for %s is %f Gb' %( dir, conv_size )

    print 'Total is %f Gb' %( tot_size / (1024*1024*1024.0) )

def get_eos_tot_size( top_dir ) :

    top_size = 0
    subdir_sizes = {}
    iteration = 0
    dirs, files, sizes = eosutil.parse_eos_dir( top_dir )
    # only iterate once here to
    # get the directories
    if dirs :
        for sdir in dirs :
            subdir_sizes[sdir] = 0
            for stop, sdirs, sfiles, ssizes in eosutil.walk_eos( top_dir+'/'+sdir) :
                for size in ssizes :
                    subdir_sizes[sdir] = subdir_sizes[sdir] + size
    
        top_size = reduce(lambda x, y : x+y , subdir_sizes.values() )

    for size in sizes :
        top_size += size




    return top_size, subdir_sizes
    

if __name__ == '__main__' :
    main()
