import os
import json
import re
from argparse import ArgumentParser
from collections import defaultdict
#works if you setup CMSSW_5_3_22_patch1 first

from check_dataset_completion import get_dataset_counts

parser = ArgumentParser()

parser.add_argument( '--version', dest='version', default=None, help='Name of processing version (subdirectory under sample directory)' )
parser.add_argument( '--mcOnly', dest='mcOnly',  default=False, action='store_true', help='only process MC samples (check DATA_SAMPLES list)' )
parser.add_argument( '--dataOnly', dest='dataOnly',  default=False, action='store_true', help='only process data samples (check DATA_SAMPLES list)' )
parser.add_argument( '--dataEras', dest='dataEras',  default=None, help='List of data eras to expect, should be a list of single letters.  This should be provided if you want to have correct event counting' )
parser.add_argument( '--sampleKey', dest='sampleKey',  default=None, help='Filter samples based on this key' )
parser.add_argument( '--nodas', dest='nodas',  default=False,action='store_true', help='skip inquiring das' )
parser.add_argument( '--notree', dest='notree',  default=False,action='store_true', help='skip reading tree' )
parser.add_argument( '--vetofail', dest='vetofail',default =False, action='store_true',help='veto failed jobs')

options = parser.parse_args()

BASE_DIR   = '/store/user/kawong/WGamma2'
#BASE_DIR   = '/store/user/friccita/'
SCRIPT_DIR = os.path.dirname(os.path.realpath(__file__))
DATA_SAMPLES = ['SingleElectron', 'SingleMuon', 'HLT']

## information from https://twiki.cern.ch/twiki/bin/view/CMSPublic/WorkBookMiniAOD
RUN_YEAR = 'Run2016'
RECO_TYPE_DATA = ['07Aug17']
RECO_TYPE_MC   = ['12Apr2018']
FILE_KEY = 'ntuple'
TREE_NAME = 'UMDNTuple/EventTree'
MC_CAMPAIGN_STR = 'RunIIFall17'
DATA_VERSION = 'UMDNTuple_0506_2016'
MC_VERSION = 'UMDNTuple_0506_2016'


def main() :


    print 'MAKE A GRID PROXY'
    if not options.nodas: os.system( 'voms-proxy-init -voms cms -rfc' )

    found_samples = []
    for sampdir in os.listdir( BASE_DIR  ) :

        isData = ( sampdir in DATA_SAMPLES )

        if options.dataOnly and not isData :
            continue
        if options.mcOnly and isData :
            continue

        if options.sampleKey is not None :
            if not sampdir.count( options.sampleKey ) :
                continue

        for subdir in os.listdir( BASE_DIR + '/' + sampdir ) :
            if subdir == options.version or subdir == MC_VERSION or subdir == DATA_VERSION:
                found_samples.append( sampdir )

    das_events = defaultdict(list)

    print '******************************************'
    print ' Getting DAS events'
    print '******************************************'

    for samp in found_samples :

        isData = ( samp in DATA_SAMPLES )

        prodname = []

        if isData :
            for rt in RECO_TYPE_DATA :
                miniaodname = 'MINIAOD'
                prodname.append('%s*%s*' %( RUN_YEAR, rt ) )
        else :
            for rt in RECO_TYPE_MC :
                miniaodname = 'MINIAODSIM'
                prodname.append('%s*%s*' %(MC_CAMPAIGN_STR, rt))

        nevents_das = 0
        for pd in prodname :

            query = '"dataset=/%s/%s/%s"' %( samp, pd, miniaodname )

            json_name = '%s_step1.json' %( samp )

            print 'dasgoclient --query=%s --format=json --limit=0 ' %(  query )
            if not options.nodas: os.system('cd /cvmfs/cms.cern.ch/slc6_amd64_gcc530/cms/cmssw/CMSSW_8_0_25/src/;eval `scramv1 runtime -sh`;cd -')
            if not options.nodas: os.system( 'dasgoclient --query=%s --format=json --limit=0 >& %s' %(query, json_name ) )

            

            ofile = open(  json_name )

            print 'Open json %s' %json_name

            data = json.load( ofile )

            ofile.close()

            # if this is data we want to sum over
            # the data eras that were provided on 
            # the command line.  If this is MC we
            # need to select the appropriate MC campaign
            # assumption is given by the MC_CAMPAIGN_STR 
            # at the top
            for idx, subdata in enumerate(data['data']) :

                # find the era name from the dataset name
                if isData :
                    print 'dataset = ', subdata['dataset'][0]['name']
                    era_str = subdata['dataset'][0]['name'].split('/')[2]

                    if subdata['dataset'][0]['name'].count( 'Run2016B' ) and subdata['dataset'][0]['name'].count( '_ver1-v1' ) :
                        print 'Skipping datset ', subdata['dataset'][0]['name']
                        continue

                    res = re.match( '%s(\w).*' %( RUN_YEAR ), era_str )

                    if res is not None :
                        if options.dataEras is not None :
                            if res.group(1) not in options.dataEras.split(',') :
                                continue
                    else :
                        print 'Could not parse era from dataset!  Dataset string is ', era_str
                else :

                    campaign_str = subdata['dataset'][0]['name'].split('/')[2]

                    if not campaign_str.count( MC_CAMPAIGN_STR ) :
                        continue
                    else :
                        if nevents_das > 0 :
                           print 'Found multiple MC campaigns that match!'



                json_name = '%s_step2_%d.json' %( samp, idx )
                
                print 'dasgoclient --query=%s --format=json >& %s' %(  subdata['dataset'][0]['name'], json_name ) 
                if not options.nodas: os.system( 'dasgoclient --query=%s --format=json >& %s' %(  subdata['dataset'][0]['name'], json_name ) )
                
                ofile = open(  json_name )

                data = json.load( ofile )

                ofile.close()

                if 'data' not in data :
                    print 'Could not locate data!'
                    continue

                for d in data['data']:
                  for dataset in d['dataset'] :

                    if 'nevents' in dataset :
                        nevents_das = dataset['nevents'] 
                        das_events[samp] .append( nevents_das)
                        break



    print '******************************************'
    print ' Getting Local events'
    print '******************************************'
    local_events = {}
    if options.notree:
        ofile = open("treecount.json")
    
        local_events=json.load(ofile )
    
        ofile.close()
    else:	
        for samp in found_samples :
            isData = ( samp in DATA_SAMPLES )

            if options.version:
                version = options.version
            elif isData:
                version = DATA_VERSION
            else:
                version = MC_VERSION
            tree_counts, hist_counts = get_dataset_counts( '%s/%s/%s' %( BASE_DIR, samp, version ), FILE_KEY, treeName=TREE_NAME, vetoes='failed' )

            local_events[samp] = tree_counts

            ##old results
            #isData = ( samp in DATA_SAMPLES )
            if not das_events[samp]:
                continue
            #print das_events[samp]
            diffs = [s-local_events[samp] for s in das_events[samp] if s -local_events[samp]>=0]
            if isData:
                das_total = sum(das_events[samp])
                diff = das_total - local_events[samp] 
                print '%s : Original = %d events, filtered = %d events.  \033[1mDifference = %d (%.4g%%)\033[0m' %( samp, das_total, local_events[samp], diff, 100.0*diff/das_total)
            elif not diffs:
                maxevent = max(das_events[samp])
                print '%s : Original = %d events, filtered = %d events.  \033[31mDifference = %d\033[0m' %( samp, maxevent, local_events[samp],maxevent - local_events[samp])
            else:
                mindiff = min(diffs)
                print '%s : Original = %d events, filtered = %d events.  \033[1mDifference = %d\033[0m' %( samp, mindiff+local_events[samp], local_events[samp],mindiff)
    
        ofile = open("treecount.json",'w')
    
        json.dump( local_events, ofile )
    
        ofile.close()



    print '******************************************'
    print ' Results '
    print '******************************************'
    for samp in found_samples :
        isData = ( samp in DATA_SAMPLES )
        if not das_events[samp]:
                continue
        print das_events[samp],
        diffs = [s-local_events[samp] for s in das_events[samp] if s -local_events[samp]>=0]
        if isData:
            das_total = sum(das_events[samp])
            diff = das_total - local_events[samp] 
            print "%s : Original = %d events, filtered = %d events.  \033[1mDifference = %d (%.4g%%)\033[0m"\
                         %( samp, das_total, local_events[samp], diff, 100.0*diff/das_total)
        elif not diffs:
            maxevent = max(das_events[samp])
            print "%s : Original = %d events, filtered = %d events.  \033[31mDifference = %d (%.2g%%)\033[0m"\
                        %( samp, maxevent, local_events[samp],maxevent - local_events[samp], 100.*(maxevent - local_events[samp])/maxevent)
        else:
            mindiff = min(diffs)
            print "%s : Original = %d events, filtered = %d events.  \033[1mDifference = %d (%.2g%%)\033[0m"\
                %( samp, mindiff+local_events[samp], local_events[samp],mindiff,100.0*mindiff/(mindiff+local_events[samp]))



main()
