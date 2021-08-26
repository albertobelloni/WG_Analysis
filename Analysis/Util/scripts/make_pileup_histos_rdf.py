#!/usr/bin/env python
import os
import ROOT
ROOT.PyConfig.IgnoreCommandLineOptions = True
ROOT.gROOT.SetBatch(True)

from argparse import ArgumentParser

parser = ArgumentParser()

#parser.add_argument('--version', dest='version', required=True, help='Name of version directory (Resonances_v10)' )
#parser.add_argument('--outputDir', dest='outputDir', required=True, help='output path' )
parser.add_argument('--fileKey', dest='fileKey', default=None, help='key to match files' )
parser.add_argument('--treeName', dest='treeName', default='UMDNTuple/EventTree', help='tree name' )
parser.add_argument('--skipDone', dest='skipDone', default=False, action = "store_true", help='skip pileup histograms already made' )

options = parser.parse_args()

#_NTUPLE_DIR = '/eos/cms/store/group/phys_exotica/Wgamma'
#options.outputDir = '/afs/cern.ch/work/k/kawong/Resonances2018/pileup'
_NTUPLE_DIR = '/store/user/mseidel/WGamma/'
options.version = 'UMDNTuple_1129_2016/'
# single top
_NTUPLE_DIR = '/store/user/kawong/WGamma2/'
options.version = 'UMDNTuple_2016_1003/'
options.outputDir = '/data/users/mseidel/Resonances2016/pileup/'

def main() :

    data_samples = ['SingleElectron', 'SingleMuon', 'SinglePhoton', 'DoubleMuon', 'DoubleElectron', 'EGamma']
    #data_samples = ['SingleMuon','SingleElectron']
    #mc_samples = ['DYJetsToLL_M-50_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8','DYJetsToLL_M-50_TuneCUETP8M1_13TeV-madgraphMLM-pythia8','DiPhotonJets_MGG-80toInf_13TeV_amcatnloFXFX_pythia8',]
    #mc_samples = ['GJets_HT-100To200_TuneCUETP8M1_13TeV-madgraphMLM-pythia8','GJets_HT-200To400_TuneCUETP8M1_13TeV-madgraphMLM-pythia8','GJets_HT-400To600_TuneCUETP8M1_13TeV-madgraphMLM-pythia8','GJets_HT-40To100_TuneCUETP8M1_13TeV-madgraphMLM-pythia8','GJets_HT-600ToInf_TuneCUETP8M1_13TeV-madgraphMLM-pythia8',]
    #mc_samples = ['TTGJets_TuneCUETP8M1_13TeV-amcatnloFXFX-madspin-pythia8','TTJets_DiLept_TuneCUETP8M1_13TeV-madgraphMLM-pythia8','TTJets_SingleLeptFromT_TuneCUETP8M1_13TeV-madgraphMLM-pythia8','TTJets_SingleLeptFromTbar_TuneCUETP8M1_13TeV-madgraphMLM-pythia8',]
    #mc_samples = ['WGToLNuG_PtG-130_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8','WGToLNuG_PtG-130_TuneCUETP8M1_13TeV-madgraphMLM-pythia8','WGToLNuG_PtG-500_TuneCUETP8M1_13TeV-madgraphMLM-pythia8','WGToLNuG_TuneCUETP8M1_13TeV-madgraphMLM-pythia8',]
    #mc_samples = ['WJetsToLNu_HT-100To200_TuneCUETP8M1_13TeV-madgraphMLM-pythia8','WJetsToLNu_HT-1200To2500_TuneCUETP8M1_13TeV-madgraphMLM-pythia8','WJetsToLNu_HT-200To400_TuneCUETP8M1_13TeV-madgraphMLM-pythia8','WJetsToLNu_HT-2500ToInf_TuneCUETP8M1_13TeV-madgraphMLM-pythia8','WJetsToLNu_HT-400To600_TuneCUETP8M1_13TeV-madgraphMLM-pythia8','WJetsToLNu_HT-600To800_TuneCUETP8M1_13TeV-madgraphMLM-pythia8','WJetsToLNu_HT-800To1200_TuneCUETP8M1_13TeV-madgraphMLM-pythia8','WJetsToLNu_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8','WJetsToLNu_TuneCUETP8M1_13TeV-madgraphMLM-pythia8',]
    #mc_samples = ['WWG_TuneCUETP8M1_13TeV-amcatnlo-pythia8','WWTo2L2Nu_13TeV-powheg','WZG_TuneCUETP8M1_13TeV-amcatnlo-pythia8','ZGTo2LG_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8']
    mc_samples = ['WGToLNuG_PtG-500_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8']
    mc_samples = [
        'WJetsToLNu_Pt-100To250_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8',
        'WJetsToLNu_Pt-250To400_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8',
        'WJetsToLNu_Pt-400To600_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8',
        'WJetsToLNu_Pt-600ToInf_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8',
    ]
    mc_samples = [
        'ST_tW_antitop_5f_NoFullyHadronicDecays_13TeV-powheg_TuneCUETP8M1',
        'ST_tW_top_5f_NoFullyHadronicDecays_13TeV-powheg_TuneCUETP8M1',
    ]

    # mc_samples = [] # empty list means run over all found subdirectories

    if not mc_samples:
        for samp in os.listdir( _NTUPLE_DIR ) :

            if samp in data_samples :
                continue

            if options.skipDone and os.path.isfile( '%s/%s/hist.root' %( options.outputDir, samp ) ) :
                continue

            if os.path.isdir( '%s/%s/%s' %( _NTUPLE_DIR, samp, options.version ) ) :
                mc_samples.append( samp )

    for samp in mc_samples :

        samp_files = []

        for top, dirs, files in os.walk( _NTUPLE_DIR + '/' + samp + '/' + options.version ,followlinks=True) :
            for f in files :
                if options.fileKey is None or f.count( options.fileKey ) > 0 :
                    samp_files.append('%s/%s' %(top, f ) ) 

        samp_dir = '%s/%s' %( options.outputDir, samp )

        if not os.path.isdir(samp_dir ) :
            os.makedirs( samp_dir )

        if options.skipDone and os.path.isfile('%s/hist.root' %samp_dir):
            continue
        outfile = ROOT.TFile.Open( '%s/hist.root' %samp_dir , 'RECREATE' )

        print 'Make histogram for %s' %samp


        if samp_files: get_histograms( samp_files, outfile )

        outfile.Close()


def get_histograms(files, outfile) :

    branch_name = 'truepu_n'

    chain = ROOT.TChain( options.treeName )

    for f in files :
        chain.AddFile( f )

    chain.SetBranchStatus('*', 0)
    chain.SetBranchStatus(branch_name, 1)
    chain.SetBranchStatus('EventWeights', 1)

    ROOT.ROOT.EnableImplicitMT()
    rdf = ROOT.RDataFrame(chain)
    hist = rdf.Histo1D(('pileup_true', 'pileup_true', 100, 0, 100), branch_name)

    outfile.cd()
    hist.Write()






main()

