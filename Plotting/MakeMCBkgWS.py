#!/usr/bin/env python
import re
import uuid
import pickle
from uncertainties import ufloat
from collections import OrderedDict
from IPython.core.debugger import Tracer
import sys
print sys.version

def addparser(parser):
    parser.add_argument('--useRooFit',       default=False,     action='store_true',      dest='useRooFit',    required=False, help='Make fits using roostats' )
    parser.add_argument('--process',         default="WGamma"   , help="set which process to be fitted, default is WGamma only")
    parser.add_argument('--channel',         default=""         , help="set channel to use")

execfile("MakeBase.py")

from FitManager import FitManager
ROOT.Math.MinimizerOptions.SetDefaultMaxFunctionCalls( 100000)

_XMIN_M = 200
_XMAX_M = 2000
_BIN_WIDTH_M = 20
_DEFAULTDATADIR = 'data/bkgfit/'

if options.dataDir is None :
    options.dataDir = _DEFAULTDATADIR
if options.dataDir is not None :
    if not os.path.isdir( options.dataDir ) :
        os.makedirs( options.dataDir )
        os.makedirs( options.dataDir+ "/2016" )
        os.makedirs( options.dataDir+ "/2017" )
        os.makedirs( options.dataDir+ "/2018" )


def main() :

    if options.channel != "el": sampManMuG.ReadSamples( _SAMPCONF )
    if options.channel != "mu": sampManElG.ReadSamples( _SAMPCONF )

    #binning_m  = ((_XMAX_M-200)/_BIN_WIDTH_M, 200, _XMAX_M)
    #binning_m1 = ((_XMAX_M-300)/_BIN_WIDTH_M, 300, _XMAX_M)
    #binning_m2 = ((_XMAX_M-600)/_BIN_WIDTH_M, 600, _XMAX_M)

    binner = lambda xmin: ((_XMAX_M-xmin)/_BIN_WIDTH_M, xmin, _XMAX_M)


    kine_vars = {
                    'mt_res'    : { tag: binner(defs.bkgfitlowbin(tag)) for tag in "ABC"}
                }

    cutsetdict = {}
    if options.channel!="el": cutsetdict["mu"] =  (sampManMuG, defs.selectcutdictgen( "mu" ))
    if options.channel!="mu": cutsetdict["el"] =  (sampManElG, defs.selectcutdictgen( "el" ))

    #sampnames, protag = checkprocname()
    sampnames=[""]
    protag = "all"


    fitfunc = ["dijet","expow","atlas"] 
    #fitfunc = ["atlas"] 
    #fitfunc = "dijet"

    ## instantiate workspace
    workspace            = ROOT.RooWorkspace( "workspace_%s" %(protag) )

    rootfilename = '%s/%i/%s_hist.root' %( options.dataDir,options.year,workspace.GetName() )

    histarray = []
    for ch, (sampMan, selections) in cutsetdict.iteritems() :
        for seltag, (sel, weight) in selections.iteritems():
            for var, binning in kine_vars.iteritems() :
                #histarray[ch+seltag+var]= makehistall_rdf(var, binning[seltag],  sampMan, sel, weight)

                #hist = makehist(var, binning[seltag], sampnames, sampMan, sel, weight = "NLOWeight")
                if options.year ==2018: weight = weight.replace("prefweight","1")
                #weight = weight.replace("*jet_btagSF","") ## Yihui -- no jet_btagSF
                hist = makehistall(var, binning[seltag],  sampMan, sel, weight)
                #histarray[ch+seltag+var].DrawSave()
                #hist = sampMan['__AllStack__'].hist.Clone()
                #c1 = ROOT.TCanvas()
                #c1.SetLogy()
                #hist.Draw()
                #savecanv(c1,"test")

                ## FIXME
                print " **** sampname %s number of total events %f ****"\
                                    %(protag, hist.Integral(0, 100000))
                print " **** sampname %s number of events %f **********"\
                                    %(protag, hist.Integral())

                for ff in fitfunc:
                    suffix = "%s%s%i_%s_%s"%(ch,seltag,options.year,protag, ff)
                    #suffix = "%s%s%i_%s"%(ch,seltag,options.year,protag)
                    print """
                    *********************
                    calling get_mc_fit for %s
                    *********************\n """ %tPurple %(ff)
                    #raw_input("cont...")
                    hist1 = get_mc_fit( hist, var , ff, workspace, suffix)

                    histarray.append(hist1)
                    #histarray.append(canv)

    rootfile = ROOT.TFile(rootfilename, "RECREATE")
    for h in histarray:
        h.Write()
    rootfile.Write()
    ## write workspace file
    if options.outputDir is not None :
        workspace.writeToFile( '%s/%i/%s.root' \
                    %( options.dataDir,options.year,workspace.GetName() ) )




def makehistall(var, binning, sampman, selection, weight = "NLOWeight"):
    """ use Draw method instead of create_hist """
    sampman.Draw( var, selection, binning,
            { "weight": weight, "overflow":False ,"drawsignal":False} )
    h1 = sampman['__AllStack__'].hist.Clone()
    return h1

def makehistall_rdf(var, binning, sampman, selection, weight = "NLOWeight", skipdata=True):
    hf = sampman.SetHisto1DFast( var, selection, binning, weight,
            {"overflow":False ,"drawsignal":False})
            #, data_exp=skipdata,)
    return hf


def makehist(var, binning, sampnames, sampman, selection):
    ## check that samplenames is not empty
    if not sampnames: return None

    ## first make a list of histograms
    histar = [clone_sample_and_draw( sampman, s, var, selection, binning ) for s in sampnames]

    ## then reduce by an inline function to return added histogram
    return reduce(lambda h1,h2: h1 if h1.Add(h2) else None, histar)



def get_mc_fit( hist ,var, fitfunc, workspace, suffix='') :


    if 'mu' in suffix:
       ch, extra_label = "mu", "Muon Channel"
    elif 'el' in suffix:
       ch, extra_label = "el", "Electron Channel"


    xvar = ROOT.RooRealVar( var, var, _XMIN_M , _XMAX_M)


    #full_sel_sr = sel_base.replace("ADDITION", " (%s > %d && %s < %d )"%(var, xmin, var , xmax))
    #print full_sel_sr

    #label = '%s_%s_%s'%(protag, suffix,  fitfunc)


    ## power, expow, vvdijet, atlas, dijet
    norders=2
    if fitfunc == "expow" or fitfunc == "atlas":
        norders=1
    fitManager = FitManager( fitfunc , hist , xvar, suffix, norders =norders)
    #fitManager.addhist(hist, "datahist"+fitfunc)
    canv = fitManager.draw( paramlayout = (0.7,0.5,0.82),
                            useOldsetup = True, logy=1, yrange=(5e-3, 2e4) )

    #fitManager.setup_fit()
    fitManager.setup_rootfit( xvar )
    fitManager.func.Draw("same")
    savecanv(canv,"%sbefore_%s" %(suffix,fitfunc) )
    fitManager.run_rootfit()

    #fit_distribution( fitManager, sampMan, workspace, logy=True )
    #fitManager.make_func_pdf()
    #fitManager.fit_histogram( workspace )

    print """ cast it from TF1 to RooGenericPdf """
    fitManager.calculate_func_pdf()
    fitManager.get_results( workspace, False )
    outhist = fitManager.get_pdf_histogram( xbins = hist.GetNbinsX() )

    #results[ieta] = save_distribution( fitManager, sampMan, workspace, logy=True )
    #fitManager.save_fit( sampMan, workspace, logy = True, stats_pos='right', extra_label = extra_label)

    canv = fitManager.draw( subplot = "pull", paramlayout = (0.7,0.5,0.82), useOldsetup = True, logy=1, yrange=(5e-3, 2e4) )
    savecanv(canv,"%s_%s"%(suffix,fitfunc))

    return outhist


def savecanv(canv, name):
    canv.Print("%s/%s.root" %(options.outputDir, name) )
    canv.Print("%s/%s.pdf" %(options.outputDir, name) )
    canv.Print("%s/%s.png" %(options.outputDir, name) )
    canv.Print("%s/%s.C"   %(options.outputDir, name) )


def clone_sample_and_draw( sampMan, samp, var, sel, binning ) :

    #newSamp = sampMan.clone_sample( oldname=samp, newname=samp+str(uuid.uuid4()), temporary=True )
    #print "newsample:", newSamp
    newSamp = sampMan.get_samples( name = samp )[0]
    sampMan.create_hist( newSamp, var, sel, binning, overflow=False)
    return newSamp.hist.Clone()

@f_Obsolete
def checkprocname():
    ## FIXME: use sample manager function to search for named samples instead
    proclist = ["WGamma", "Top", "TopW", "AllTop", "TopGamma",
                "Zgamma", "Z+jets", "All", "NonMajor"]
    proclistlower = map(lambda x: x.lower(), proclist)
    protag = options.process.lower()
    assert protag in proclistlower, "process not listed: %s" %options.process

    ## make compound lists (FIXME This is non standard: better use Module)
    process_list = [ p for p in proclist if p.lower() == protag ][0]
    if process_list == "All":
        process_list = ["WGamma", "AllTop", "Zgamma","GammaGamma", "TopW", "ZJets", 'WJets']
                #[ 'WGamma', 'TTG', 'TTbar', 'Zgamma', 'Wjets', 'GammaGamma']
    elif process_list == "NonMajor": pass ## FIXME
    elif isinstance(process_list, str):
        process_list = [process_list,]
    return process_list, protag

main()

