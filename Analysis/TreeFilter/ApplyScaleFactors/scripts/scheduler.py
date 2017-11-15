import os
from argparse import ArgumentParser

p = ArgumentParser()
p.add_argument( '--run'     , dest='run'     , default=False, action='store_true', help='Run filtering'              )
p.add_argument( '--check'   , dest='check'   , default=False, action='store_true', help='Run check of completion'    )
p.add_argument( '--clean'   , dest='clean'   , default=False, action='store_true', help='Run cleanup of extra files' )
p.add_argument( '--resubmit', dest='resubmit', default=False, action='store_true', help='Only submit missing output' )
p.add_argument( '--local'   , dest='local'   , default=True , action='store_true', help='Run locally'                )
options = p.parse_args()

if not options.run and not options.check :
    options.run = True

base = '/data/users/jkunkle/Resonances'

class JobConf( ) :

    def __init__( self, base, name, suffix='') :
        self.base = base
        self.name = name
        self.suffix = suffix

jobs_data = [
        #JobConf(base, base_orig, 'job_muon_2012a_Jan22rereco'),
        #JobConf(base, base_orig, 'job_muon_2012b_Jan22rereco'),
        #JobConf(base, base_orig, 'job_muon_2012c_Jan22rereco'),
        #JobConf(base, base_orig, 'job_muon_2012d_Jan22rereco'),
        #JobConf(base, base_orig, 'job_electron_2012a_Jan22rereco'),
        #JobConf(base, base_orig, 'job_electron_2012b_Jan22rereco'),
        #JobConf(base, base_orig, 'job_electron_2012c_Jan2012rereco'),
        #JobConf(base, base_orig, 'job_electron_2012d_Jan22rereco'),
]
jobs_mc = [
        JobConf(base,'MadGraphChargedResonance_WGToLNu_M2600_width0p01' ),
]

if options.local :
    #--------------------
    # not batch
    #--------------------
    #command_base = 'python scripts/filter.py  --filesDir %(base)s/%(input)s/%(job)s --outputDir %(base)s/%(output)s/%(job)s --outputFile tree.root --treeName %(treename)s --fileKey tree.root --module scripts/%(module)s --confFileName %(job)s.txt --nFilesPerJob %(nFilesPerJob)d --nproc %(nproc)d --exeName %(exename)s --moduleArgs "%(moduleArgs)s" '
    command_base = 'python scripts/filter.py  --filesDir %(base)s/%(input)s/%(job)s --outputDir %(output)s --outputFile tree.root --treeName %(treename)s --fileKey tree.root --module scripts/%(module)s --confFileName %(job)s.txt --nFilesPerJob %(nFilesPerJob)d --nproc %(nproc)d --exeName %(exename)s --moduleArgs "%(moduleArgs)s" '
    
else :
    #--------------------
    # for batch submission
    #--------------------
    #command_base = 'python scripts/filter.py  --filesDir %(base)s/%(input)s/%(job)s --outputDir %(base)s/%(output)s/%(job)s --outputFile tree.root --treeName %(treename)s --fileKey tree.root --module scripts/%(module)s --batch --confFileName %(job)s.txt --nFilesPerJob %(nFilesPerJob)d --exeName %(exename)s_%(job)s  --moduleArgs "%(moduleArgs)s"'
    command_base = 'python scripts/filter.py  --filesDir %(base)s/%(input)s/%(job)s --outputDir %(output)s --outputFile tree.root --treeName %(treename)s --fileKey tree.root --module scripts/%(module)s --batch --confFileName %(job)s.txt --nFilesPerJob %(nFilesPerJob)d --exeName %(exename)s_%(job)s  --moduleArgs "%(moduleArgs)s"'

if options.resubmit :
    command_base += ' --resubmit '

module = 'Conf.py'
nFilesPerJob = 1
nProc = 6
exename='RunAnalysis'
treename='tupel/EventTree'

top_configs = [
    {   
     'module'      : 'Conf.py', 
     #'args'        : {'functions' : 'get_muon_sf,get_electron_sf,get_photon_sf,get_pileup_sf' },
     'args'        : {'functions' : 'get_muon_sf' },
     'input_name'  : 'LepGamma_mug_2017_09_05',
     'output_tag'  : 'TESTSF',
     'tag'         : 'muFinalSF'
    },

]

if options.run :
    for config in top_configs :
        first = True
        for job_conf in jobs_data :
            base      = job_conf.base
            job       = job_conf.name
            suffix    = job_conf.suffix

            if options.local :
                job_exename = exename+'Data'
            else :
                job_exename = exename

            module_arg = config['args']
            module_arg['isData'] = ' == True '

            module_str = '{ '
            for key, val in module_arg.iteritems() :
                module_str += '\'%s\' : \'%s\',' %( key, val)
            module_str += '}'

            if 'output_name' in config :
                output = '%s/%s/%s%s' %(base,config['output_name'],job, suffix)
            else :
                output = '%s/%s/%s%s%s' %(base, config['input_name'], job, suffix,config['output_tag'])
            

            command = command_base %{ 'base' : base, 'job' : job+suffix, 'nFilesPerJob' : nFilesPerJob, 'input' : config['input_name'], 'output' : output, 'nproc' : nProc, 'exename' : job_exename, 'treename' : treename, 'module' : config['module'], 'moduleArgs' : module_str }

            if not first :
                command += ' --noCompileWithCheck '
            print command
            os.system(command)
            if first :
                first = False

        first = True
        for job_conf in jobs_mc :

            base      = job_conf.base
            job       = job_conf.name
            suffix    = job_conf.suffix

            if options.local :
                job_exename = exename+'MC'
            else :
                job_exename = exename

            module_arg = config['args']

            module_str = '{ '
            for key, val in module_arg.iteritems() :
                module_str += '\'%s\' : \'%s\',' %( key, val)

            module_str += '}'

            if 'output_name' in config :
                output = '%s/%s/%s%s' %(base,config['output_name'],job, suffix)
            else :
                output = '%s/%s/%s%s%s' %(base, config['input_name'], job, suffix, config['output_tag'])
            

            command = command_base %{ 'base' : base, 'job' : job+suffix, 'nFilesPerJob' : nFilesPerJob, 'input' : config['input_name'], 'output' : output, 'nproc' : nProc, 'exename' : job_exename, 'treename' : treename, 'module' : config['module'], 'moduleArgs' : module_str }
            if not first :
                command += ' --noCompileWithCheck '

            print command
            os.system(command)
            if first :
                first = False


