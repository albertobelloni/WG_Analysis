#!/usr/bin/env python
import os
import ROOT

from argparse import ArgumentParser

parser = ArgumentParser()

parser.add_argument( '--dir', dest='directory', default=None, help='Path to directory containing ntuples' )
parser.add_argument( '--fileKey', dest='fileKey', default='ntuple', required=False, help='key to match files' )
parser.add_argument( '--treeName', dest='treeName', default='UMDNTuple/EventTree', required=False, help='name of tree in files' )
parser.add_argument( '--weightBranch', dest='weightBranch', default='EventWeights', required=False, help='name of branch containing event weights' )
parser.add_argument( '--condor', dest='condor',action="store_true",help='submit condor jobs' )

options = parser.parse_args()

print '*************************FIX*********************'
#if not options.condor:
ROOT.gROOT.SetBatch(True)

def main () :

    ntuple_files = []

    for fname in os.listdir( options.directory ) :
        print fname
        if fname.count( options.fileKey ) :
            ntuple_files.append( '%s/%s' %( options.directory, fname ) )

    n_raw = []
    n_total = []
    n_weighted = []


    total_events = 0
    weighted_events = 0

    mychain = ROOT.TChain( options.treeName )
    for f in ntuple_files :
        mychain.AddFile( f )

    if True:
        #myfile = ROOT.TFile.Open( f )
        #mychain = myfile.Get( options.treeName )

        mychain.SetBranchStatus('*', 0 )
        mychain.SetBranchStatus( options.weightBranch, 1 )

        totalEvents = 0
        weightedEvents = 0

        weighthist = ROOT.TH1F( 'weighthist', 'weighthist', 2, -100000, 100000 )

        print mychain.GetEntries()
        n_raw.append(  mychain.GetEntries() )

        mychain.Draw( '%s[0] >> weighthist' %options.weightBranch )
        print "finished draw"


        neg_events  = weighthist.GetBinContent(0) + weighthist.GetBinContent(1)
        pos_events  = weighthist.GetBinContent(2) + weighthist.GetBinContent(3)

        total_events = neg_events + pos_events
        weighted_events = pos_events - neg_events 

        n_total .append( total_events )
        n_weighted.append( weighted_events)

    print 'Total Events = %d, Weighted events = %d' %( total_events, weighted_events)


    print 'Raw Events = %d, Total Events = %d, Weighted events = %d' %(sum(n_raw), sum(n_total), sum(n_weighted) ) 

    #for event in mychain :

    #    weight = getattr( mychain, options.weightBranch )

    #    totalEvents += 1

    #    if weight[0] > 0 :
    #        weightedEvents += 1
    #    if weight[0] < 0 :
    #        weightedEvents -= 1

    #print 'Total Events = %d, Weighted events = %d' %( totalEvents, weightedEvents )


rejectlist = ["failed","SingleElectron","SingleMuon","EGamma"]
includelist = ["UMDNTuple_0506_2016","UMDNTuple_0506_2017","UMDNTuple_0506_2018",]
def submitjobs():
    basepath ="/eos/cms/store/group/phys_exotica/Wgamma"

    if options.directory: basepath = options.directory
    dirlist = []
    desc_entries = ["universe = vanilla",
        "notify_user = kakw@umd.edu",
        "notification = Error",
        "getenv = True",
        "MINUTE      = 60",
        "periodic_hold = (CurrentTime - JobCurrentStartDate) >= 600 * $(MINUTE)",
        "periodic_release = NumJobStarts<5",
        "priority=0", #"Initialdir = ",
        "+jobFlavour=workday",
        "Executable = get_weighted_events.py", ]

    for b,d,f in os.walk(basepath,followlinks=True):
      if max([b.count(r) for r in rejectlist]):
        continue
      for fname in f:
         if fname.count(".root") and sum([b.count(i) for i in includelist]):
            dirlist.append(b)
            print b
            tag = os.path.relpath(b,basepath).split("/")
            makecondorjob(b,tag,desc_entries)
            break
    submitcondorjob(desc_entries)

def makecondorjob(basedir,tag,desc_entries):
    tag = tuple(tag[:3])
    tmpdir = "weighted/"+tag[0]
    if not os.path.exists(tmpdir):
        if not os.path.isdir(tmpdir):
            os.makedirs(tmpdir)
        else: 
            print tag[0], " already exists and is not directory. skipping"
            return
    desc_entries+=["",
        "output = weighted/%s/stdout$(cluster)_$(process)_%s%s.txt" %tag,
        "error = weighted/%s/stderr$(cluster)_$(process)_%s%s.txt"  %tag,
        "log = weighted/%s/condor$(cluster)_$(process)_%s%s.txt" %tag,
        "arguments = --dir %s" %basedir,
        "queue",]

def submitcondorjob(desc_entries):
    desc_name = 'job_desc_1.txt'
    descf = open(desc_name, 'w')
    descf.write('\n'.join(desc_entries))
    descf.close()
    os.system('condor_submit %s ' % desc_name)

if options.condor:
    submitjobs()
else: 
    main()
