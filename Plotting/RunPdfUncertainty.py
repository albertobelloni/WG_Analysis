import os
import re
from SampleManager import SampleManager

_TREENAME = 'UMDNTuple/EventTree'
_FILENAME = 'tree.root'
_XSFILE   = '/data/users/fengyb/WGToLNuG/WG_Analysis/Plotting/cross_sections/photon15.py'
_LUMI     = 36000
_SAMPCONF = '/data/users/fengyb/WGToLNuG/WG_Analysis/Plotting/Modules/Resonance.py'

def main():

    BaseDir = "/data/users/fengyb/WGammaNtuple/SigNoFilt_2018_05_11"
    sampManNoFilt = SampleManager( BaseDir, _TREENAME, filename=_FILENAME, quiet=True)
    sampManNoFilt.ReadSamples( _SAMPCONF )

    for samp in sampManNoFilt.get_samples() :

        print 'Sample = ', samp.name

        #res = re.match( '(MadGraph|Pythia)ResonanceMass(\d+)_width(\d+)', samp.name )
        res = re.match( 'MadGraphResonanceMass(\d+)_width(\d+)', samp.name)

        if res is not None :

            mass  = int(res.group(1))
            width = int(res.group(2))
             
            print width, mass

            job_desc_file = create_job_desc_file(mass, width)

            condor_command = 'condor_submit %s ' % job_desc_file
            print '********************************'
            print condor_command
            os.system(condor_command)



def create_job_desc_file(mass, width) :

    priority              = 0

    # the header of the job description file
    desc_entries = [
                    '#Use only the vanilla universe',
                    'universe = vanilla',
                    '# This is the executable to run.  If a script,',
                    '#   be sure to mark it "#!<path to interp>" on the first line.',
                    '# Filename for stdout, otherwise it is lost',
                    'output = stdout.txt',
                    'error = stderr.txt',
                    '# Copy the submittor environment variables.  Usually required.',
                    'getenv = True',
                    '# Copy output files when done.  REQUIRED to run in a protected directory',
                    'when_to_transfer_output = ON_EXIT_OR_EVICT',
                    'priority=%d' %priority
                    ]

    initialdir = "/data/users/fengyb/WGToLNuG/WG_Analysis/Plotting/condor_output"
    executable = "/data/users/fengyb/WGToLNuG/WG_Analysis/Plotting/MakeSignalEffPdf.py"
    baseDir = "/data/users/fengyb/WGammaNtuple/SigNoFilt_2018_05_11"
    outputFile = "/data/users/fengyb/WGToLNuG/WG_Analysis/Plotting/Acceptance/pdfuncertainty/root/pdf"

    initialdir += "/mass%s_width%s"%(mass, width)

    desc_entries += [
                         'Executable = %s' %executable,
                         'Initialdir = %s' %initialdir,
                         '# This is the argument line to the Executable'
                    ]

    if not os.path.isdir( initialdir ) :
       print "make directory %s"%initialdir
       os.makedirs( initialdir )

    # assemble the argument command
    arg_command = ['arguments = "',
                    '--baseDir %s' %baseDir,
                    '--outputFile %s' %outputFile,
                    '--mass %d'%mass,
                    '--width %d'%width,
                  ]

    arg_command += ['"']

    desc_entries +=  [ ' '.join(arg_command) ]

    desc_entries += [
                          '# Queue job',
                          'queue'
                    ]

    #Determine the job description file name
    desc_name = 'job_desc.txt'

    desc_file_name =  initialdir +'/'+desc_name

    descf = open(desc_file_name, 'w')

    descf.write('\n'.join(desc_entries))
    descf.close()

    return desc_file_name

main()
