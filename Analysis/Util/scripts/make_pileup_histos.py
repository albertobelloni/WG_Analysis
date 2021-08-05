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

_NTUPLE_DIR = '/store/group/WGAMMA/'
options.version = 'UMDNTuple_0902'
options.outputDir = '/data2/users/kakw/Resonances2016/pileup/'

def main() :

    #mc_samples = [] # empty list means run over all found subdirectories
    mc_samples = [#'MadGraphChargedResonance_WGToLNuG_M1000_width0p01',
                  #'MadGraphChargedResonance_WGToLNuG_M350_width0p01',
                  #'MadGraphChargedResonance_WGToLNuG_M500_width5',
                  'MadGraphChargedResonance_WGToLNu_M2800_width5'
                  ] # empty list means run over all found subdirectories
    data_samples = ['SingleElectron', 'SingleMuon', 'SinglePhoton', 'DoubleMuon', 'DoubleElectron', 'EGamma']

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

    outfile.cd()
    chain.Draw( '%s >> pileup_true(100,0,100)' %branch_name, '1 * ( EventWeights[0] > 0 ) - 1* ( EventWeights[0] < 0 ) ' )
    #chain.Draw( '%s >> pileup_true(100,0,100)' %branch_name, '' )

    hist = outfile.Get('pileup_true')

    hist.Write()






main()

