#!/usr/bin/env python
import os
import ROOT
import time
ROOT.PyConfig.IgnoreCommandLineOptions = True
ROOT.gROOT.SetBatch(True)

from argparse import ArgumentParser

parser = ArgumentParser()

parser.add_argument('--version', dest='version', help='Name of version directory' )
parser.add_argument('--outputDir', dest='outputDir', required=False, default=None, help='output path' )
parser.add_argument('--fileKey', dest='fileKey', default=None, help='key to match files' )
parser.add_argument('--treeName', dest='treeName', default='UMDNTuple/EventTree', help='tree name' )
parser.add_argument('--skipDone', dest='skipDone', default=False, action = "store_true", help='skip pileup histograms already made' )
parser.add_argument('--year', dest='year', default=2016, type=int, help='set run year' )
parser.add_argument('--sample', dest='mcsample', default='', help='specify sample to run on' )
parser.add_argument('--quick', dest='quick', action = "store_true", help='run the first 3e6 events for quick result' )
parser.add_argument('--condor', dest='condor', action = "store_true", help='submit condor jobs' )
parser.add_argument('--dryrun', dest='dryrun', action = "store_true", help='produce job description but not submit job' )

options = parser.parse_args()

_NTUPLE_DIR = '/store/group/WGAMMA/'
_QUICKNMAX = 1000000
if not options.version:
    options.version = 'UMDNTuple_0902'
    if options.year == 2017:
        options.version = 'UMDNTuple_211210'
if options.outputDir is None:
    options.outputDir = '/data2/users/kakw/Resonances%i/pileup/' %options.year



mc_samples = [] # empty list means run over all found subdirectories

#mc_samples = ['MadGraphChargedResonance_WGToLNu_M1000_width0p01',
#              'MadGraphChargedResonance_WGToLNu_M350_width0p01',
#              'MadGraphChargedResonance_WGToLNu_M500_width5',
#              ]

if options.mcsample: mc_samples = [options.mcsample,]

# Data samples are skipped
data_samples = ['SingleElectron', 'SingleMuon', 'SinglePhoton', 'DoubleMuon', 'DoubleElectron', 'EGamma']




### ------------- main function -----------------



def main() :

    ## if mc_samples is empty, we start by looking for samples
    if not mc_samples:
        samples = findsamples()
    else:
        samples = mc_samples

    for samp in samples :

        samp_files = []

        for top, dirs, files in os.walk( ntuplepath(_NTUPLE_DIR, samp, options.version, options.year) ,followlinks=True) :
            for f in files :
                if options.fileKey is None or f.count( options.fileKey ) > 0 :
                    samp_files.append('%s/%s' %(top, f ) )

        if not os.path.isdir( options.outputDir ) :
            os.makedirs( options.outputDir )

        if checkskipdone(samp):
            continue

        outfile = ROOT.TFile.Open( '%s/%s_hist.root' %(options.outputDir, samp) , 'RECREATE' )

        print 'Make histogram for %s' %samp
        timer= time.time()

        if samp_files: get_histograms( samp_files, outfile )

        print "time: ", time.time()-timer

        outfile.Close()


def ntuplepath( ntupledir, samp, vers, year ):
    return "%s/%s/%s_%i" %( ntupledir, samp, vers, year )


def findsamples():
    samples = []
    for samp in os.listdir( _NTUPLE_DIR ) :

        if samp in data_samples :
            continue

        if checkskipdone(samp):
            continue

        if os.path.isdir(ntuplepath(_NTUPLE_DIR, samp, options.version, options.year)):
            samples.append( samp )
    return samples


def checkskipdone(samp):
    if options.skipDone and os.path.isfile( '%s/%s_hist.root' %( options.outputDir, samp ) ):
        f=ROOT.TFile("%s/%s_hist.root" %(options.outputDir, samp))
        h1 = f.Get("pileup_true")
        h2 = f.Get("pdfscale")
        if h1 and h2:
            print "Done, and skip: ", samp
            return True
    return False

def get_histograms(files, outfile) :

    branch_name = 'truepu_n'

    chain = ROOT.TChain( options.treeName )

    for f in files :
        chain.AddFile( f )

    chain.SetBranchStatus('*', 0)
    chain.SetBranchStatus(branch_name, 1)
    chain.SetBranchStatus('EventWeights', 1)

    outfile.cd()

    histpu = ROOT.TH1D("pileup_true","Pile up histogram", 100, 0, 100)

    if options.quick:
        chain.Draw( '%s >> pileup_true' %branch_name, '1 * ( EventWeights[0] > 0 ) - 1* ( EventWeights[0] < 0 ) ', '', _QUICKNMAX)
    else:
        chain.Draw( '%s >> pileup_true' %branch_name, '1 * ( EventWeights[0] > 0 ) - 1* ( EventWeights[0] < 0 ) ' )

    histpu.Write()


    ## Make histogram for PDF Scale weights
    histpdf = ROOT.TH1D("pdfscale","PDF Scale Weights", 100, 0, 100)

    if options.quick:
        chain.Draw( "Iteration$>>pdfscale", "EventWeights[]/EventWeights[0]", "",  _QUICKNMAX)
    else:
        chain.Draw( "Iteration$>>pdfscale", "EventWeights[]/EventWeights[0]")

    if options.quick:
        histpdf.Scale(1./_QUICKNMAX)
    else:
        histpdf.Scale(1./chain.GetEntries())

    histpdf.Write()



def submitjobs():

    desc_entries = [
        "universe = vanilla",
        "notify_user = kakw@umd.edu",
        "notification = Error",
        "getenv = True",
#        "MINUTE      = 60",
#        "periodic_hold = (CurrentTime - JobCurrentStartDate) >= 600 * $(MINUTE)",
#        "periodic_release = NumJobStarts<5",
        "Executable = make_pileup_histos.py", ]

    if not mc_samples:
        samples = findsamples()
    else:
        samples = mc_samples

    for samp in samples:
       makecondorjob(samp, desc_entries)

    if not os.path.isdir( "logs" ) :
       os.makedirs( "logs" )

    submitcondorjob(desc_entries)


def makecondorjob(samp,desc_entries):
    """ this function modifies desc_entries
        note the unconventional behavior
    """
    tag = "%s_%s_%i" %(samp, options.version, options.year)
    addtl = ""
    if options.quick:
        addtl+="  --quick"
    if options.skipDone:
        addtl+="  --skipDone"

    desc_entries+=[
        "",
        "output = logs/stdout$(cluster)_$(process)_%s.txt" %tag,
        "error = logs/stderr$(cluster)_$(process)_%s.txt" %tag,
        "log = logs/condor$(cluster)_$(process)_%s.txt" %tag,
        "arguments = --sample %s --year %i --outputDir %s %s" %(samp, options.year, options.outputDir, addtl),
        "queue",
        ]


def submitcondorjob(desc_entries):
    print "\n".join(desc_entries)
    desc_name = 'job_desc_make_pileup_histos.txt'
    descf = open(desc_name, 'w')
    descf.write('\n'.join(desc_entries))
    descf.close()
    if not options.dryrun: os.system('condor_submit %s ' % desc_name)






if options.condor:
    submitjobs()
else:
    main()

