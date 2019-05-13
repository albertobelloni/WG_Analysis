import os
from check_dataset_completion import check_dataset_completion

#base_data     ='root://eoscms//eos/cms/store/group/phys_egamma/ymaravin/ggNtuples/V05-03-07-06'
base_data     ='/eos/cms/store/group/phys_smp/ggNtuples/data'
#base_data = '/eos/cms/store/user/jkunkle/Wgamgam/FilteredSamplesFeb14/'

from argparse import ArgumentParser
import eos_utilities as eosutil

parser = ArgumentParser()

parser.add_argument( '--filteredPath', dest='filteredPath', default=None, help='Path to the directory contating filtered samples', required=True )

parser.add_argument( '--originalPath', dest='originalPath', default=None, help='Path to the directory contating orginal samples', required=True )

parser.add_argument( '--singleFiles', dest='singleFiles', default=False, action='store_true', help='if true, each sample is an individual root file' )

parser.add_argument( '--key', dest='key', default=None, help='Only check datasets matching key' )


options = parser.parse_args()

original_samples = []
filtered_samples = []

if options.originalPath.count('/eos/') :
    if options.singleFiles :
        for top, dirs, files, sizes in eosutil.walk_eos( options.originalPath ) :
            for file in files :
                original_samples.append( file.rstrip('.root') )
            #only run once because the sample files should be in the given directory
            break
    else :
        for top, dirs, files, sizes in eosutil.walk_eos( options.originalPath ) :
            for dir in dirs :
                original_samples.append( dir )
            #only run once because the sample directories should be in the given directory
            break
else :
    # use os.walk locally
    for top, dirs, files in os.walk( options.originalPath ) :
        for dir in dirs :
            original_samples.append( dir )
        break

if options.filteredPath.count('/eos/') :
    for top, dirs, files, sizes in eosutil.walk_eos( options.filteredPath ) :
        for dir in dirs :
            filtered_samples.append( dir )
        #only run once because the sample files should be in the given directory
        break
else :
    for top, dirs, files in os.walk( options.filteredPath ) :
        for dir in dirs :
            filtered_samples.append( dir )
        break

missing = set( original_samples ) - set( filtered_samples )
if missing :
    print 'Datasets not present in filtered samples : '
    for miss in missing :
        print miss


for sample in filtered_samples :

    if options.key is not None :
        if sample.count(options.key) == 0 :
            continue

    filt_path = options.filteredPath + '/' + sample
    if options.singleFiles :
        orig_path = options.originalPath
    else :
        orig_path = options.originalPath + '/' + sample
    

    if options.singleFiles :
        os.system( 'python scripts/check_dataset_completion.py --originalDS %s --filteredDS %s --treeNameOrig ggNtuplizer/EventTree --treeNameFilt ggNtuplizer/EventTree --histNameFilt=ggNtuplizer/filter --fileKeyOrig %s --fileKeyFilt tree.root' %( orig_path, filt_path, sample+'.root') )
    else :
        #orig_nevt_tree, orig_nevt_hist, filt_nevt_tree, filt_nevt_hist = check_dataset_completion( originalDS=orig_path, filteredDS=filt_path, treeNameOrig='ggNtuplizer/EventTree', treeNameFilt='ggNtuplizer/EventTree',histNameFilt='ggNtuplizer/filter', fileKeyOrig='tree.root', fileKeyFilt='tree.root' )
        os.system( 'python scripts/check_dataset_completion.py --originalDS %s --filteredDS %s --treeNameOrig ggNtuplizer/EventTree  --histNameFilt=ggNtuplizer/filter --fileKeyOrig tree.root --fileKeyFilt tree.root' %( orig_path, filt_path) )

