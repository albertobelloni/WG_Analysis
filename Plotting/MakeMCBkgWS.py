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

    sampManMuG.ReadSamples( _SAMPCONF )
    sampManElG.ReadSamples( _SAMPCONF )

    #sampManMuG.outputs = OrderedDict()
    #sampManElG.outputs = {}
    #sampManMuG.fitresults = OrderedDict()
    #sampManMuG.chi2= OrderedDict()
    #sampManMuG.chi2prob = OrderedDict()
    #sampManElG.fitresults = OrderedDict()
    #sampManElG.chi2= OrderedDict()
    #sampManElG.chi2prob = OrderedDict()


    eta_cuts = ['EB']

    #workspaces_to_save = {}


    binning_m  = ((_XMAX_M-200)/_BIN_WIDTH_M, 200, _XMAX_M)
    binning_m1 = ((_XMAX_M-300)/_BIN_WIDTH_M, 300, _XMAX_M)
    binning_m2 = ((_XMAX_M-600)/_BIN_WIDTH_M, 600, _XMAX_M)


    kine_vars = {
                  'mt_res'    : { 'A': binning_m ,
                                  'B': binning_m1,
                                  'C': binning_m2,
                                 },
                }

    cutsetdict = {"mu": (sampManMuG, defs.selectcutdictgen( "mu" )),
                  "el": (sampManElG, defs.selectcutdictgen( "el" ))}

    sampnames, protag = checkprocname()


    #fitfunc = "expow"
    fitfunc = "dijet"

    ## instantiate workspace
    workspace            = ROOT.RooWorkspace( "workspace_%s_%s" %(protag,fitfunc) )

    for ch, (sampMan, selections) in cutsetdict.iteritems() :
        for seltag, sel in selections.iteritems():

            for var, binning in kine_vars.iteritems() :
                hist = makehist(var, binning[seltag], sampnames, sampMan, sel)
                c1 = ROOT.TCanvas()
                c1.SetLogy()
                hist.Draw()
                savecanv(c1,"test")

                ## FIXME
                print " **** sampname %s number of total events %f ****"\
                                    %(protag, hist.Integral(0, 100000))
                print " **** sampname %s number of events %f **********"\
                                    %(protag, hist.Integral())

                suffix = "%s%s%i_%s"%(ch,seltag,options.year,protag)
                print """
                *********************
                calling get_mc_fit for %s
                *********************\n """ %tPurple %(sampnames)
                get_mc_fit( hist, var , fitfunc, workspace, suffix)


    ## write workspace file
    if options.outputDir is not None :
        workspace.writeToFile( '%s/%i/%s.root' \
                    %( options.dataDir,options.year,workspace.GetName() ) )


    #for key, canv in sampManMuG.outputs.iteritems() :
    #    savecanv(canv, key)
    #else:
    #    print "Nothing to save"
    #for key, canv in sampManElG.outputs.iteritems() :
    #    savecanv(canv, key)
    #else:
    #    print "Nothing to save"

        #for key, result in sampManMuG.fitresults.iteritems():
        #    print "sample: %50s result %d chi2 %.2f"%(key, result.status(), sampManMuG.chi2[key])
        #    result.Print()


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
    fitManager = FitManager( fitfunc , hist, xvar, suffix, norders =2)
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
    fitManager.get_results( workspace )

    #results[ieta] = save_distribution( fitManager, sampMan, workspace, logy=True )
    #fitManager.save_fit( sampMan, workspace, logy = True, stats_pos='right', extra_label = extra_label)

    canv = fitManager.draw( subplot = "pull", paramlayout = (0.7,0.5,0.82), useOldsetup = True, logy=1, yrange=(5e-3, 2e4) )
    savecanv(canv,"%s_%s"%(suffix,fitfunc))

    return


def savecanv(canv, name):
    canv.Print("%s/%s.pdf" %(options.outputDir, name) )
    canv.Print("%s/%s.png" %(options.outputDir, name) )
    canv.Print("%s/%s.C"   %(options.outputDir, name) )


def clone_sample_and_draw( sampMan, samp, var, sel, binning ) :

    #newSamp = sampMan.clone_sample( oldname=samp, newname=samp+str(uuid.uuid4()), temporary=True )
    #print "newsample:", newSamp
    newSamp = sampMan.get_samples( name = samp )[0]
    sampMan.create_hist( newSamp, var, sel, binning, overflow=False)
    return newSamp.hist.Clone()


#@f_Obsolete
#def buildselectionstr(ch=""):
#    ## FIXME combine with SigFit
#    sel_base_mu = defs.get_base_selection( 'mu' )
#    sel_base_el = defs.get_base_selection( 'el' )
#
#
#    #el_ip_str = '( fabs( el_d0[0] ) < 0.05 && fabs( el_dz[0] ) < 0.10 && fabs( el_sc_eta[0] )<= 1.479 ) || ( fabs( el_d0[0] ) < 0.10 && fabs( el_dz[0] ) < 0.20 && fabs( el_sc_eta[0] )> 1.479 )'
#
#    el_tight = ' el_passVIDTight[0] == 1'
#    el_eta   = ' fabs( el_eta[0] ) < 2.1 '
#
#    ph_str         = 'ph_n==1 && ph_IsEB[0] && ph_pt[0] > 80 && ph_passMedium[0] && !ph_hasPixSeed[0] && ph_passEleVeto[0]'
#    ph_tightpt_str = 'ph_n==1 && ph_IsEB[0] && ph_pt[0] > 80 && ph_passMedium[0] && !ph_hasPixSeed[0] && ph_passEleVeto[0]'
#
#    met_str = 'met_pt > 40'
#
#    Zveto_str = 'fabs(m_lep_ph-91)>20.0'
#
#    musellist = [sel_base_mu, ph_tightpt_str, met_str]
#    sel_mu_phpt_nominal = " && ".join( musellist )
#    elsellist = [sel_base_el, el_tight, el_eta, ph_tightpt_str, met_str, Zveto_str ]
#    sel_el_phpt_nominal = " && ".join( elsellist )
#
#    sel_base_mu = "NLOWeight*(%s)" %sel_mu_phpt_nominal
#    sel_base_el = "NLOWeight*(%s)" %sel_el_phpt_nominal
#
#    #sel_jetveto_mu = sel_base_mu + ' && jet_n == 0 '
#    #sel_jetveto_el = sel_base_el + ' && jet_n == 0 '
#    if ch=="mu": return sel_base_mu
#    if ch=="el": return sel_base_el
#    return sel_base_mu, sel_base_el


@f_Obsolete
def makebinpt():
    xmin_pt = _XMIN_M/2
    if xmin_pt < 50 :
        xmin_pt = 50
    xmax_pt = _XMAX_M/2
    bin_width_pt = _BIN_WIDTH_M/2.

    binning_pt = ( (xmax_pt - xmin_pt )/bin_width_pt, xmin_pt, xmax_pt )
    return binning_pt

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
        process_list = ["WGamma", "AllTop", "Zgamma","GammaGamma", "TopW", "Z+jets", 'Wjets']
                #[ 'WGamma', 'TTG', 'TTbar', 'Zgamma', 'Wjets', 'GammaGamma']
    elif process_list == "NonMajor": pass ## FIXME
    elif isinstance(process_list, str):
        process_list = [process_list,]
    return process_list, protag

main()

