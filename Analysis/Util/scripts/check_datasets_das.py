import os
import json
import re
from argparse import ArgumentParser

from check_dataset_completion import get_dataset_counts

parser = ArgumentParser()

parser.add_argument( '--version', dest='version', required=True, default=None, help='Name of processing version (subdirectory under sample directory)' )
parser.add_argument( '--mcOnly', dest='mcOnly',  default=False, action='store_true', help='only process MC samples (check DATA_SAMPLES list)' )
parser.add_argument( '--dataOnly', dest='dataOnly',  default=False, action='store_true', help='only process data samples (check DATA_SAMPLES list)' )
parser.add_argument( '--dataEras', dest='dataEras',  default=None, help='List of data eras to expect, should be a list of single letters.  This should be provided if you want to have correct event counting' )
parser.add_argument( '--sampleKey', dest='sampleKey',  default=None, help='Filter samples based on this key' )

options = parser.parse_args()

BASE_DIR   = '/store/user/jkunkle'
SCRIPT_DIR = os.path.dirname(os.path.realpath(__file__))
#DATA_SAMPLES = ['SingleElectron', 'SingleMuon', 'SinglePhoton']
DATA_SAMPLES = ['SingleElectron']
RUN_YEAR = 'Run2016'
#RECO_TYPE = ['23Sep2016', 'H-PromptReco']
RECO_TYPE = ['03Feb2017']
FILE_KEY = 'ntuple'
TREE_NAME = 'tupel/EventTree'
MC_CAMPAIGN_STR = 'RunIISummer16'


def main() :


    print 'MAKE A GRID PROXY'
    os.system( 'voms-proxy-init -voms cms' )

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
            if subdir == options.version :
                found_samples.append( sampdir )

    das_events = {}

    print '******************************************'
    print ' Getting DAS events'
    print '******************************************'

    for samp in found_samples :

        isData = ( samp in DATA_SAMPLES )

        prodname = []

        if isData :
            for rt in RECO_TYPE :
                miniaodname = 'MINIAOD'
                prodname.append('%s*%s*' %( RUN_YEAR, rt ) )
        else :
            miniaodname = 'MINIAODSIM'
            prodname.append('*')

        nevents_das = 0
        for pd in prodname :

            query = '"dataset=/%s/%s/%s"' %( samp, pd, miniaodname )

            json_name = '%s_step1.json' %( samp )

            print 'python %s/das_client.py --query=%s --format=json --limit=0 ' %( SCRIPT_DIR, query )

            os.system( 'python %s/das_client.py --query=%s --format=json --limit=0 >& %s' %( SCRIPT_DIR, query, json_name ) )
            

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
                            print 'Found multiple MC campaigns that match! Using only the first'
                            continue



                json_name = '%s_step2_%d.json' %( samp, idx )
                
                os.system( 'python %s/das_client.py --query=%s --format=json >& %s' %( SCRIPT_DIR, subdata['dataset'][0]['name'], json_name ) )
                
                ofile = open(  json_name )

                data = json.load( ofile )

                ofile.close()

                if 'data' not in data :
                    print 'Could not locate data!'
                    continue

                for dataset in data['data'][0]['dataset'] :

                    if 'nevents' in dataset :
                        nevents_das += dataset['nevents']
                        break

        das_events[samp] = nevents_das


    print '******************************************'
    print ' Getting Local events'
    print '******************************************'
    local_events = {}
    for samp in found_samples :

        #tree_counts, hist_counts = get_dataset_counts( '%s/%s/%s' %( BASE_DIR, samp, options.version ), FILE_KEY, treeName=TREE_NAME, vetoes='failed' )
        tree_counts, hist_counts = get_dataset_counts( '%s/%s/%s' %( BASE_DIR, samp, options.version ), FILE_KEY, treeName=TREE_NAME)

        local_events[samp] = tree_counts

    print '******************************************'
    print ' Results '
    print '******************************************'
    for samp in found_samples :

        print '%s : Orignal = %d events, filtered = %d events.  \033[1mDifference = %d\033[0m' %( samp, das_events[samp], local_events[samp],das_events[samp]-local_events[samp] )








main()
