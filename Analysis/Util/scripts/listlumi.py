#!/usr/bin/env python
"""
Make lumi list of Data ntuple output
Produce two json outputs, for two different lumi formats
"""
from argparse import ArgumentParser,RawDescriptionHelpFormatter
parser = ArgumentParser(description=__doc__,
        formatter_class=RawDescriptionHelpFormatter)
parser.add_argument('--outputDir',       default=None,          help='Output directory to write histograms')
parser.add_argument('--dataDir',         default=None,          help='IO directory to data')
parser.add_argument('--batch',           action="store_true",   help='Supress X11 output')
parser.add_argument('--year',            default=2016,          type=int,            help='Set run year')
parser.add_argument('--ch',              default="el",          help='Set channel')
parser.add_argument('--era',             default="A",           help='Set era')
parser.add_argument('--condor',          action="store_true",   help='run on condor')
options = parser.parse_args()
import ROOT
from pprint import pprint
from operator import itemgetter
from itertools import groupby
import json
import sys
import pdb
import os

ROOT.PyConfig.IgnoreCommandLineOptions = True
ROOT.gStyle.SetOptStat(110011)

## copied from /cvmfs/cms.cern.ch/$SCRAM_ARCH/cms/cmssw/CMSSW_11_1_0/src/FWCore/PythonUtilities/python/LumiList.py
"""
    Deal with lists of lumis in several different forms:
    Compact list:
        {
        '1': [[1, 33], [35, 35], [37, 47], [49, 75], [77, 130], [133, 136]],
        '2':[[1,45],[50,80]]
        }
        where the first key is the run number, subsequent pairs are
        ranges of lumis within that run that are desired
    Runs and lumis:
        {
        '1': [1,2,3,4,6,7,8,9,10],
        '2': [1,4,5,20]
        }
        where the first key is the run number and the list is a list of
        individual lumi sections. This form also takes a list of these objects
        which can be much faster than LumiList += LumiList
    Run  lumi pairs:
        [[1,1], [1,2],[1,4], [2,1], [2,5], [1,10]]
        where each pair in the list is an individual run&lumi
    CMSSW representation:
        '1:1-1:33,1:35,1:37-1:47,2:1-2:45,2:50-2:80'
        The string used by CMSSW in lumisToProcess or lumisToSkip
        is a subset of the compactList example above
    """

if options.batch:
    ROOT.gROOT.SetBatch(True)

channeldict = {
        (2016,"el"): "SingleElectron",
        (2017,"el"): "SingleElectron",
        (2018,"el"): "EGamma",
        (2016,"mu"): "SingleMuon",
        (2017,"mu"): "SingleMuon",
        (2018,"mu"): "SingleMuon",
        }

runrangedict = {
    2016:
        {
        ## upper range of runNumber is incremented by 1
        "B":    {"runrange":(272007, 275377), "tasknum":{"mu": "201229_170559", "el": "201229_170452"}},
        "C":    {"runrange":(275657, 276284), "tasknum":{"mu": "201229_170550", "el": "201229_170443"}},
        "D":    {"runrange":(276315, 276812), "tasknum":{"mu": "201229_170540", "el": "201229_170434"}},
        "E":    {"runrange":(276831, 277421), "tasknum":{"mu": "201229_170531", "el": "201229_170425"}},
        "F":    {"runrange":(277772, 278809), "tasknum":{"mu": "201229_170522", "el": "201229_170416"}},
        "G":    {"runrange":(278820, 280386), "tasknum":{"mu": "201229_170512", "el": "201229_170405"}},
        "H":    {"runrange":(280919, 284045), "tasknum":{"mu": "201229_170502", "el": "201229_170356"}},
        },
    2017:
       {
        "B":    {"runrange":(297046, 299330), "tasknum":{"mu": "201228_024055", "el": "201228_024143"}},
        "C":    {"runrange":(299368, 302030), "tasknum":{"mu": "201228_024105", "el": "201228_024152"}},
        "D":    {"runrange":(302030, 303435), "tasknum":{"mu": "201228_024113", "el": "201228_024202"}},
        "E":    {"runrange":(303824, 304798), "tasknum":{"mu": "201228_024123", "el": "201228_024211"}},
        "F":    {"runrange":(305040, 306463), "tasknum":{"mu": "201228_024132", "el": "201228_024221"}},
    },
    2018:
        {
        "A":    {"runrange":(315252, 316996), "tasknum":{"mu": "201208_085319", "el": "201208_085345"}},
        "B":    {"runrange":(317080, 319311), "tasknum":{"mu": "201208_085328", "el": "201208_085354"}},
        "C":    {"runrange":(319337, 320066), "tasknum":{"mu": "201208_085337", "el": "201208_085402"}},
        "D":    {"runrange":(320673, 325176), "tasknum":{"mu": "201214_133233", "el": "201214_133243"}},
        }
}

year, ch, era = options.year, options.ch, options.era
yechera = (options.year, options.ch, options.era)

def main():
    rundict = {}

    c1 = ROOT.TCanvas()
    c = ROOT.TChain("UMDNTuple/EventTree")
    #c.Add("/store/group/WGAMMA/SingleMuon/UMDNTuple_0902_2018/201208_085319/0000/*.root")
    c.Add("/store/group/WGAMMA/{channel}/UMDNTuple_0902_{year}/{tasknum}/0000/*.root".format(year = year, channel = channeldict[(year,ch)], tasknum=runrangedict[year][era]["tasknum"][ch]))
    print "/store/group/WGAMMA/{channel}/UMDNTuple_0902_{year}/{tasknum}/0000/*.root".format(year = year, channel = channeldict[(year,ch)], tasknum=runrangedict[year][era]["tasknum"][ch])
    if os.path.isdir("/store/group/WGAMMA/{channel}/UMDNTuple_0902_{year}/{tasknum}/0001/".format(year = year, channel = channeldict[(year,ch)], tasknum=runrangedict[year][era]["tasknum"][ch])):
        c.Add("/store/group/WGAMMA/{channel}/UMDNTuple_0902_{year}/{tasknum}/0001/*.root".format(year = year, channel = channeldict[(year,ch)], tasknum=runrangedict[year][era]["tasknum"][ch]))

    runrange = runrangedict[year][era]["runrange"]
    histrange = (runrange[1]-runrange[0], runrange[0],runrange[1])
    c.Draw("runNumber:lumiSection>>h1(4000,0,4000,%i,%i,%i)" %histrange,"","COLZ")
    c1.SaveAs("processedruns%i%s%s.pdf" %yechera)
    c1.SaveAs("processedruns%i%s%s.png" %yechera)
    h1 = ROOT.gDirectory.Get("h1")
    for runnum in range(*runrange):
        for i in range(3001):
            if h1.GetBinContent(i, runnum-runrange[0]+1):
                #pdb.set_trace()
                if not rundict.get(str(runnum)):
                    rundict[str(runnum)] = []
                rundict[str(runnum)].append(i-1)

    filepath = "processedruns%i%s%s.json" %yechera
    with open(filepath, "w") as fo:
        json.dump( rundict , fo)

    rundictgrouped = { k: groupnumbers(v) for k,v in rundict.viewitems()}
    filepath = "processedrunsgrouped%i%s%s.json" %yechera
    with open(filepath, "w") as fo:
        json.dump( rundictgrouped , fo)
    print "entries", c.GetEntriesFast()


def groupnumbers(data):
    ranges = []
    for k, g in groupby(enumerate(data), lambda (i,x):i-x):
        group = map(itemgetter(1), g)
        ranges.append((group[0], group[-1]))
    return ranges

if options.condor :
    working_dir = os.getcwd()
    filename = __file__.rstrip(".py").split("/")[-1]
    condor_script = ['getenv=True',
                     'universe = vanilla',
                     'Executable = {workd}/{thisfile}.py',
                     'should_transfer_files = NO',
                     'Requirements = TARGET.FileSystemDomain == "privnet" && (TARGET.OpSysMajorVer == 7)',
                     'Output = {workd}/log/{thisfile}_$(cluster)_$(process).stdout',
                     'Error =  {workd}/log/{thisfile}_$(cluster)_$(process).stderr',
                     'Log =    {workd}/log/{thisfile}_$(cluster)_$(process).condor',
                     'Minute = 60',
                     'on_exit_hold =  (ExitCode != 0)',
                     'periodic_release = NumJobStarts<2 && (CurrentTime - JobCurrentStartDate) >= 10 * $(MINUTE)',
                     ]

    for iyear in [2016,2017,2018]:
        for iera in runrangedict[iyear]:
            for ich in ["mu","el"]:
                condor_script +=[ "Arguments = --batch --ch {ch} --year {year} --era {era}".format(era=iera, ch=ich, year=iyear), "Queue",""]
    condor_script = "\n".join(condor_script)
    condor_script = condor_script.format(thisfile = filename, workd = working_dir)
    job_desc_file = "{workd}/{thisfile}.jdl".format(thisfile = filename, workd = working_dir)
    print condor_script
    with open(job_desc_file, "w") as fo:
        fo.write(condor_script)
    condor_command = "condor_submit %s" %job_desc_file
    print condor_command
    os.system(condor_command)
    sys.exit()

main()
