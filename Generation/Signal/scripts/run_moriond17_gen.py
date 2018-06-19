#!/cvmfs/cms.cern.ch/slc6_amd64_gcc491/external/python/2.7.6-cms/bin//python
import os
import sys
import random

from argparse import ArgumentParser

parser = ArgumentParser()

parser.add_argument( '--prod_dir', dest='prod_dir', required=True, help='Directoy where output is located' )
parser.add_argument( '--name', dest='name', required=True, help='Name of sample' )
parser.add_argument( '--gridpack', dest='gridpack', required=True, help='Path to the gridpack' )
parser.add_argument( '--nevt', dest='nevt', type=int, default=100,  help='Number of events to run' )
parser.add_argument( '--writeShellScript', dest='writeShellScript', action='store_true', default=False, help='Do not run the commands, just write a shell script' )
parser.add_argument( '--proxyName', dest='proxyName',  default=None, help='Name of proxy.  If provided a file with this name will be copied to /tmp' )
parser.add_argument( '--proxyPath', dest='proxyPath',  default=None, help='path to proxy.  Do not keep it, but set export X509_USER_PROXY=/afs/cern.ch/user/u/username/x509up_uXXXX' )
parser.add_argument( '--scriptName', dest='scriptName',  default='run.sh', help='Name of shell script where commands are written' )

options = parser.parse_args()

LHE_DIR='MakeLHE'
GENSIM_DIR='MakeGENSIM'
AOD_DIR='MakeAOD'
MINIAOD_DIR='MakeMINIAOD'

random.seed()

def main() :


    print 'RUNNING'

    # make top directories
    subdirs = [LHE_DIR, GENSIM_DIR, AOD_DIR, MINIAOD_DIR]

    if not os.path.isdir( options.prod_dir) :
        os.makedirs( options.prod_dir )

    for d in subdirs :
        if not os.path.isdir( options.prod_dir + '/' + d ) :
            os.mkdir( options.prod_dir + '/' + d )

    lhe_output = '%s_LHE.root' %( options.name )
    gs_output = '%s_GENSIM.root' %( options.name )
    step1_output = '%s_step1.root' %( options.name )
    aod_output = '%s_AOD.root' %( options.name )
    miniAOD_output = '%s_MINIAOD.root' %( options.name )

    arch_early = 'slc6_amd64_gcc481'
    arch_aod = 'slc6_amd64_gcc530'

    # ------------------------------------
    # START LHE STEP
    # ------------------------------------
    # some common items
    lhe_config_filename = '%s_LHE-fragment.py' %( options.name )
    cmssw_lhe = 'CMSSW_7_1_25_patch1'

    # write the LHE config file
    lhe_file = []
    lhe_file.append('import FWCore.ParameterSet.Config as cms' )
    
    lhe_file.append('externalLHEProducer = cms.EDProducer("ExternalLHEProducer",' )
    lhe_file.append('    args = cms.vstring("%s"),' %options.gridpack )
    lhe_file.append('    nEvents = cms.untracked.uint32(%d),' %options.nevt )
    lhe_file.append('    numberOfParameters = cms.uint32(1),' )
    lhe_file.append('    outputFile = cms.string("cmsgrid_final.lhe"),' )
    lhe_file.append('    scriptName = cms.FileInPath("GeneratorInterface/LHEInterface/data/run_generic_tarball_cvmfs.sh")' )
    lhe_file.append(')' )

    ofile = open( '%s/%s/%s' %( options.prod_dir, LHE_DIR, lhe_config_filename), 'w' )

    for line in lhe_file :
        ofile.write( line + '\n' )
    ofile.close()

    random_gen_text_lhe = make_random_gen_text( ['externalLHEProducer', 'generator'] )

    lhe_cfg_name = '%s_LHE_cfg.py' %( options.name)

    # Collect the commands
    lhe_commands = make_common_commands( options.prod_dir, LHE_DIR, cmssw_lhe, arch_early, lhe_config_filename, proxyPath=options.proxyPath )
    lhe_commands.append( 'cmsDriver.py Configuration/GenProduction/python/%s --fileout file:%s --mc --eventcontent LHE --datatier LHE --conditions MCRUN2_71_V1::All --step LHE --python_filename %s_LHE_cfg.py --no_exec --customise Configuration/DataProcessing/Utils.addMonitoring -n %d  ' %( lhe_config_filename, lhe_output, options.name, options.nevt ) )
    lhe_commands.append( 'awk \'NR==32{$0="%s"$0}1\' %s >> tmp.py' %( r'\n'.join( random_gen_text_lhe ), lhe_cfg_name ) )

    lhe_commands.append( 'mv tmp.py %s ' %( lhe_cfg_name ) )
    lhe_commands.append( 'cmsRun -e -j lhe_step.xml %s' %( lhe_cfg_name ) )
    lhe_commands.append( 'cd ../..' )


    ## run the commands
    #print 'RUNNING LHE STEP'
    #full_commands = ' ; ' .join( lhe_commands )
    #os.system( full_commands )

    # ------------------------------------
    # START GEN-SIM STEP
    # ------------------------------------
    cmssw_gensim = 'CMSSW_7_1_20_patch3' 
    gs_config_filename = '%s_GENSIM-fragment.py' %options.name

    
    # write the GEN-SIM config file
    gs_file = []
    gs_file.append('import FWCore.ParameterSet.Config as cms' )
    gs_file.append('from Configuration.Generator.Pythia8CommonSettings_cfi import *')
    gs_file.append('from Configuration.Generator.Pythia8CUEP8M1Settings_cfi import *')
    gs_file.append('from Configuration.Generator.Pythia8aMCatNLOSettings_cfi import *')
    gs_file.append('generator = cms.EDFilter("Pythia8HadronizerFilter",' )
    gs_file.append('    maxEventsToPrint = cms.untracked.int32(1),' )
    gs_file.append('    pythiaPylistVerbosity = cms.untracked.int32(1),' )
    gs_file.append('    filterEfficiency = cms.untracked.double(1.0), ' )
    gs_file.append('    pythiaHepMCVerbosity = cms.untracked.bool(False),' )
    gs_file.append('    comEnergy = cms.double(13000.),' )
    gs_file.append('    PythiaParameters = cms.PSet(' )
    gs_file.append('        pythia8CommonSettingsBlock,' )
    gs_file.append('        pythia8CUEP8M1SettingsBlock,' )
    gs_file.append('        pythia8aMCatNLOSettingsBlock,' )
    gs_file.append('        processParameters = cms.vstring(' )
    gs_file.append('            "TimeShower:nPartonsInBorn = 0", #number of coloured particles (before resonance decays) in born matrix element' )
    gs_file.append('        ),' )
    gs_file.append('        parameterSets = cms.vstring("pythia8CommonSettings",' )
    gs_file.append('                                    "pythia8CUEP8M1Settings",' )
    gs_file.append('                                    "pythia8aMCatNLOSettings",' )
    gs_file.append('                                    "processParameters",' )
    gs_file.append('                                    )' )
    gs_file.append('    )' )
    gs_file.append(')' )

    ofile = open( '%s/%s/%s' %( options.prod_dir, GENSIM_DIR, gs_config_filename), 'w' )

    for line in gs_file :
        ofile.write( line + '\n' )
    ofile.close()

    random_gen_text_gs = make_random_gen_text( ['VtxSmeared', 'g4SimHits', 'generator'] )

    gs_cfg_name = '%s_GENSIM_cfg.py ' %( options.name ) 

    # Collect the commands
    gs_commands = []
    gs_commands = make_common_commands( options.prod_dir, GENSIM_DIR, cmssw_gensim, arch_early, gs_config_filename, proxyPath=options.proxyPath )
    gs_commands.append( 'cmsDriver.py Configuration/GenProduction/python/%s --filein file:../%s/%s --fileout file:%s --mc --eventcontent RAWSIM --customise SLHCUpgradeSimulations/Configuration/postLS1Customs.customisePostLS1,Configuration/DataProcessing/Utils.addMonitoring --datatier GEN-SIM --conditions MCRUN2_71_V1::All --beamspot Realistic50ns13TeVCollision --step GEN,SIM --magField 38T_PostLS1 --python_filename %s --no_exec -n %d ' %( gs_config_filename, LHE_DIR, lhe_output, gs_output, gs_cfg_name, options.nevt ) )
    gs_commands.append( 'awk \'NR==29{$0="%s"$0}1\' %s >> tmp.py' %( r'\n'.join( random_gen_text_gs ), gs_cfg_name ) )
    gs_commands.append( 'cmsRun -e -j gensim_step.xml %s ' %( gs_cfg_name ) )
    gs_commands.append( 'cd ../..' )

    ## run the commands
    #print 'RUNNING GEN-SIM STEP'
    #full_commands = ' ; ' .join( gs_commands )
    #os.system( full_commands )


    # ------------------------------------
    # START AOD STEP
    # ------------------------------------

    random_gen_text_s1 = make_random_gen_text( ['mix', 'simMuonCSCDigis', 'simMuonDTDigis', 'simMuonRPCDigis', 'generator'] )

    s1_cfg_name = '%s_STEP1_cfg.py ' %( options.name ) 

    cmssw_aod = 'CMSSW_8_0_21' 
    AOD_commands = []
    AOD_commands = make_common_commands( options.prod_dir, AOD_DIR, cmssw_aod, arch_aod, proxyPath=options.proxyPath )
    #AOD_commands.append( 'cmsDriver.py step1 --filein file:../%s/%s --fileout file:%s --pileup_input "file:/data/users/jkunkle/Samples/MinBias_TuneCUETP8M1_13TeV-pythia8/GEN-SIM/MCRUN2_71_V1-v2/10000/004CC894-4877-E511-A11E-0025905C3DF8.root,file:/data/users/jkunkle/Samples/MinBias_TuneCUETP8M1_13TeV-pythia8/GEN-SIM/MCRUN2_71_V1-v2/10000/0063EDE9-2F77-E511-BAF6-0002C90B7F30.root,file:/data/users/jkunkle/Samples/MinBias_TuneCUETP8M1_13TeV-pythia8/GEN-SIM/MCRUN2_71_V1-v2/10000/0091527A-3E77-E511-B123-002590AC4BF6.root,file:/data/users/jkunkle/Samples/MinBias_TuneCUETP8M1_13TeV-pythia8/GEN-SIM/MCRUN2_71_V1-v2/10000/00BA861E-7779-E511-85DC-0024E85A3F69.root,file:/data/users/jkunkle/Samples/MinBias_TuneCUETP8M1_13TeV-pythia8/GEN-SIM/MCRUN2_71_V1-v2/10000/00F372BD-3C77-E511-8D36-0025901E4F3C.root,file:/data/users/jkunkle/Samples/MinBias_TuneCUETP8M1_13TeV-pythia8/GEN-SIM/MCRUN2_71_V1-v2/10000/00FCB56F-4377-E511-8F47-0025905C2CBC.root,file:/data/users/jkunkle/Samples/MinBias_TuneCUETP8M1_13TeV-pythia8/GEN-SIM/MCRUN2_71_V1-v2/10000/02310BE5-8F79-E511-AD22-02163E010E73.root,file:/data/users/jkunkle/Samples/MinBias_TuneCUETP8M1_13TeV-pythia8/GEN-SIM/MCRUN2_71_V1-v2/10000/023B5EF1-4177-E511-A3E7-00266CFFC7CC.root,file:/data/users/jkunkle/Samples/MinBias_TuneCUETP8M1_13TeV-pythia8/GEN-SIM/MCRUN2_71_V1-v2/10000/02469931-4377-E511-8A79-00259048AC98.root,file:/data/users/jkunkle/Samples/MinBias_TuneCUETP8M1_13TeV-pythia8/GEN-SIM/MCRUN2_71_V1-v2/10000/0275943C-5477-E511-A9C5-002481D24972.root" --mc --eventcontent RAWSIM --pileup 2016_25ns_SpringMC_PUScenarioV1_PoissonOOTPU --datatier GEN-SIM-RAW --conditions 80X_mcRun2_asymptotic_2016_v3 --step DIGI,L1,DIGI2RAW,HLT:@frozen25ns --era Run2_25ns --python_filename %s --no_exec --customise Configuration/DataProcessing/Utils.addMonitoring -n %d ' %( GENSIM_DIR, gs_output, step1_output, s1_cfg_name, options.nevt ) )
    #AOD_commands.append( 'cmsDriver.py step1 --filein file:../%s/%s --fileout file:%s --pileup_input "dbs:/Neutrino_E-10_gun/RunIISpring15PrePremix-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v2-v2/GEN-SIM-DIGI-RAW" --mc --eventcontent PREMIXRAW --datatier GEN-SIM-RAW --conditions 80X_mcRun2_asymptotic_2016_TrancheIV_v6 --step DIGIPREMIX_S2,DATAMIX,L1,DIGI2RAW,HLT:@frozen2016 --nThreads 4 --datamix PreMix --era Run2_2016 --python_filename %s --no_exec --customise Configuration/DataProcessing/Utils.addMonitoring -n %d ' %( GENSIM_DIR, gs_output, step1_output, s1_cfg_name, options.nevt ) )
    AOD_commands.append( 'cmsDriver.py step1 --filein file:../%s/%s --fileout file:%s --pileup_input "root://cms-xrd-global.cern.ch//store/mc/RunIISpring15PrePremix/Neutrino_E-10_gun/GEN-SIM-DIGI-RAW/PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v2-v2/100000/001EB167-3781-E611-BE3C-0CC47A4D75F4.root" --mc --eventcontent PREMIXRAW --datatier GEN-SIM-RAW --conditions 80X_mcRun2_asymptotic_2016_TrancheIV_v6 --step DIGIPREMIX_S2,DATAMIX,L1,DIGI2RAW,HLT:@frozen2016 --nThreads 4 --datamix PreMix --era Run2_2016 --python_filename %s --no_exec --customise Configuration/DataProcessing/Utils.addMonitoring -n %d ' %( GENSIM_DIR, gs_output, step1_output, s1_cfg_name, options.nevt ) )
    AOD_commands.append( 'awk \'NR==58{$0="%s"$0}1\' %s >> tmp.py' %( r'\n'.join( random_gen_text_s1 ), s1_cfg_name ) )
    AOD_commands.append( 'cmsRun -e -j step1.xml %s ' %( s1_cfg_name ) )

    AOD_commands.append( 'cmsDriver.py step2 --filein file:%s --fileout file:%s --mc --eventcontent AODSIM --runUnscheduled --datatier AODSIM --conditions 80X_mcRun2_asymptotic_2016_TrancheIV_v6 --step RAW2DIGI,RECO,EI --nThreads 4 --era Run2_2016 --python_filename %s_AOD_cfg.py --no_exec --customise Configuration/DataProcessing/Utils.addMonitoring -n %d ' %( step1_output, aod_output, options.name, options.nevt ) )
    AOD_commands.append( 'cmsRun -e -j aod_step.xml %s_AOD_cfg.py' %( options.name ) ) ; 
    AOD_commands.append( 'cd ../..' )

    ## run the commands
    #print 'RUNNING AOD STEPs'
    #full_commands = ' ; ' .join( AOD_commands )
    #print full_commands
    #os.system( full_commands )

    # ------------------------------------
    # START MINIAOD STEP
    # ------------------------------------
    cmssw_miniaod = 'CMSSW_8_0_21' 
    miniAOD_commands = []
    miniAOD_commands = make_common_commands( options.prod_dir, MINIAOD_DIR, cmssw_miniaod, arch_aod, proxyPath=options.proxyPath )
    miniAOD_commands.append( 'cmsDriver.py step1 --filein file:../%s/%s --fileout file:%s --mc --eventcontent MINIAODSIM --runUnscheduled --datatier MINIAODSIM --conditions 80X_mcRun2_asymptotic_2016_TrancheIV_v6 --step PAT --era Run2_2016 --python_filename %s_MINIAOD_cfg.py --no_exec --customise Configuration/DataProcessing/Utils.addMonitoring -n %d ' %( AOD_DIR, aod_output, miniAOD_output, options.name, options.nevt ) )
    miniAOD_commands.append('cmsRun -e -j miniaod_step.xml %s_MINIAOD_cfg.py ' %( options.name) )
    miniAOD_commands.append( 'cd ../..' )



    ## run the commands
    #print 'RUNNING MINIAOD STEP'
    #full_commands = ' ; ' .join( miniAOD_commands )
    #print full_commands
    #os.system( full_commands )

    
    #proxy_commands = ['voms-proxy-init --noregen']
    proxy_commands = []
    if options.proxyName is not None :
        proxy_commands.append( 'mkdir /tmp' )
        proxy_commands.append( 'cp %s /tmp' %options.proxyName )
        #proxy_commands.append( 'voms-proxy-init -noregen' )

    setup_commands = ['. /afs/cern.ch/sw/lcg/external/gcc/4.6/x86_64-slc6/setup.sh',
                      'source /afs/cern.ch/sw/lcg/app/releases/ROOT/5.34.07_python2.7/x86_64-slc6-gcc46-opt/root/bin/thisroot.sh' ]

    #all_commands = setup_commands + lhe_commands + gs_commands + AOD_commands + miniAOD_commands
    all_commands = setup_commands + lhe_commands + gs_commands + AOD_commands

    if options.writeShellScript :
        fname = '%s/%s' %(options.prod_dir, options.scriptName)
        ofile = open( fname, 'w' )
        print 'file = ', fname
        ofile.write( '#!/bin/bash \n' )
        for cmd in all_commands :
            ofile.write( '%s \n' %cmd )
        ofile.close()
        os.system( 'chmod 777 %s/%s' %(options.prod_dir, options.scriptName) )
    else :
        print 'RUNNING ALL STEPS'

        full_commands = 'voms-proxy-init -voms cms ; ' + ' ; '.join( all_commands )
        print 'FIRST GENERATE A PROXY'
        os.system( full_commands )


def make_common_commands( prod_dir, sub_dir, cmssw_vers, arch, config_filename=None, proxyPath=None ) :

    commands = []

    if proxyPath is not None :
        commands.append( 'export X509_USER_PROXY=%s' %proxyPath  ) 
    commands.append( 'cd %s/%s' %( prod_dir, sub_dir ) )
    #commands.append( 'source  /sharesoft/cmssw/' )
    commands.append( 'source /cvmfs/cms.cern.ch/cmsset_default.sh' )
    commands.append( 'export SCRAM_ARCH=%s' %arch )
    commands.append( 'scram p CMSSW %s' %cmssw_vers )
    commands.append( 'cd %s/src' %cmssw_vers )
    commands.append( 'eval `scram runtime -sh`' )
    if config_filename is not None :
        commands.append( 'mkdir -p Configuration/GenProduction/python/' )
        commands.append( 'mv ../../%s Configuration/GenProduction/python/' %config_filename)
    commands.append( 'scram b')
    commands.append( 'cd ../..')

    return commands

def make_random_gen_text( producers ) :

    random_gen_text = []
    random_gen_text.append( r'process.RandomNumberGeneratorService = cms.Service(\"RandomNumberGeneratorService\",' )
    for  prod in producers :
        random_gen_text.append( '    %s = cms.PSet( ' %prod ) 
        random_gen_text.append( '            initialSeed = cms.untracked.uint32(%d), ' %random.randint(1, 100000000 ) )
        random_gen_text.append( r'            engineName = cms.untracked.string(\"TRandom3\"),' )
        random_gen_text.append( '                 ),' )

    random_gen_text.append( ')' )
    random_gen_text.append( '' )
    random_gen_text.append( '' )

    return random_gen_text
    

main()
