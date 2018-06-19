import os
import re

from argparse import ArgumentParser

parser = ArgumentParser()

parser.add_argument( '--original_config', dest='original_config', required=True, help='path to start from' )
parser.add_argument( '--output_dir', dest='output_dir', required=True, help='location to write new directories' )
parser.add_argument( '--base_name', dest='base_name', default='ChargedResonance_WGToLNu', help='Base name of samples.  Should be ChargedResonance_WGToLNu or ChargedResonance_WGToJJ' )

options = parser.parse_args()

mass_points = [200, 250, 300, 350, 400, 450, 500, 600, 700, 800, 900, 1000, 1200, 1400, 1600, 1800, 2000, 2200, 2400, 2600, 2800, 3000, 3500, 4000]
#mass_points = [3500, 4000]
widths = ['0p01', '5']

def main() :


    # find the mass and width point of the original directory
    original_name = options.original_config.rstrip('/').split('/')[-1]
    res = re.match( '%s_M(\d{3,4})_width(\w+)_13TeV-pythia8_cff.py' %options.base_name, original_name )
    if res is not None :
        original_mass = int(res.group(1))
        original_width = res.group(2)
    else :
        print 'Could not parse original name %s, Exiting' %options.original_config
        return

    for mass_point in mass_points :

        for width in widths : 

            # this is the new file name
            new_config_name = '%s_M%d_width%s_13TeV-pythia8_cff.py' %( options.base_name, mass_point, width)

            # make the directory if it hasn't been made
            # note that if the directory exists it'll be overwritten
            if not os.path.isdir( options.output_dir ) :
                os.mkdir( options.output_dir )

            # read in the original card and write to the new card
            orig_file = open( options.original_config )

            new_file = open( '%s/%s' %(options.output_dir, new_config_name), 'w' )

            for line in orig_file :
                modline = line

                if line.count('37:m0') :
                    eq_pos = line.find( '=' )
                    modline = '%s %s",\n' %(line[:eq_pos+1],str( mass_point) )

                if line.count('37:mWidth') :
                    eq_pos = line.find( '=' )
                    if width.find('p') :
                        width_factor = float( width.replace('p', '.') )
                    else :
                        width_factor = float( width )

                    new_width = mass_point*width_factor/(100 )
                    modline = '%s %s",\n' %(line[:eq_pos+1], str( new_width) )

                new_file.write( modline )


            orig_file.close()
            new_file.close()


main()

