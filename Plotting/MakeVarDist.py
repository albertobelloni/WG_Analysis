#!/usr/bin/env python3
import ROOT
from itertools import product
ROOT.PyConfig.IgnoreCommandLineOptions = True
import numpy as np
from math import pi

import selection_defs as defs
from FitManager import FitManager
from SampleManager import SampleManager

from argparse import ArgumentParser
parser = ArgumentParser()
parser.add_argument('--baseDirMuG',      default=None,           dest='baseDirMuG',         required=False, help='Path to muon base directory')
parser.add_argument('--baseDirElG',      default=None,           dest='baseDirElG',         required=False, help='Path to electron base directory')
parser.add_argument('--outputDir',       default=None,           dest='outputDir',          required=False, help='Output directory to write histograms')
parser.add_argument('--data',            default=False,          dest='data',               required=False, help='Use data or MC')
parser.add_argument('--batch',           default=False,          dest='batch',              required=False, help='Supress X11 output')

options = parser.parse_args()

_TREENAME = 'UMDNTuple/EventTree'
_FILENAME = 'tree.root'
_XSFILE   = 'cross_sections/photon15.py'
_LUMI     = 36000
#_BASEPATH = '/home/jkunkle/usercode/Plotting/LimitSetting/'
_SAMPCONF = 'Modules/Resonance2017.py'
#_SAMPCONF = 'Modules/Resonance.py'



if options.batch:
    ROOT.gROOT.SetBatch(True)
if options.outputDir is not None :
    if not os.path.isdir( options.outputDir ) :
        os.makedirs( options.outputDir )

ROOT.gStyle.SetOptStat(0)
ROOT.gStyle.SetOptFit(1)
#ROOT.gROOT.SetBatch(True)

# if no option is given, here are the default directories to read
if options.baseDirMuG is None: options.baseDirMuG = "/data2/users/kakw/Resonances2017/LepGamma_mug_2019_04_12/"
if options.baseDirElG is None: options.baseDirElG = "/data2/users/kakw/Resonances2017/LepGamma_elg_2019_04_12/"
#options.baseDirElG = "/data/users/friccita/WGammaNtuple/LepGamma_elg_2019_04_11/"

def main() :
    if options.outputDir: f1 = ROOT.TFile("%s/output.root"%(options.outputDir),"RECREATE")

    #sampManMuG= SampleManager( options.baseDirMuG, _TREENAME, filename=_FILENAME, xsFile=_XSFILE, lumi=_LUMI )
    sampManElG= SampleManager( options.baseDirElG, _TREENAME, filename=_FILENAME, xsFile=_XSFILE, lumi=_LUMI )

    #sampManMuG.ReadSamples( _SAMPCONF )
    sampManElG.ReadSamples( _SAMPCONF )

    selbase_mu = 'mu_pt30_n==1 && mu_n==1'
    ## with bad tracker portions excluded
    selbase_el_excludephi = 'ph_n>=1 && el_n==1 &&!( ph_eta[0]<0&&ph_phi[0]>2.3&&ph_phi[0]<2.7)&&!(ph_phi[0]>1.2&&ph_phi[0]<1.5) '
    selbase_el = 'ph_n>=1 && el_n==1' 


    ## general event selections
    nocut = ("","")
    ltmet25 = 'met_pt<25'
    gtmet25 = 'met_pt>25'
    cut_met = [nocut, (ltmet25,"ltmet25"), (gtmet25,"gtmet25")]

    phpt50 = "ph_pt[0]>50"
    phpt100 = "ph_pt[0]>100"
    cut_phpt = [nocut, (phpt50,"phpt50"), (phpt100,"phpt100")]

    ## 1 and only 1 photon with pt greater than 50, 100 GeV
    phpt30neq1 = "ph_pt[0]>%.2g && (ph_n==1 || ph_pt[1]<%.2g)" %(30,30)
    phpt50neq1 = "ph_pt[0]>%.2g && (ph_n==1 || ph_pt[1]<%.2g)" %(50,50)
    phpt100neq1 = "ph_pt[0]>%.2g && (ph_n==1 || ph_pt[1]<%.2g)" %(100,100)
    cut_phptneq1 = [nocut, (phpt30neq1,"phpt30neq1"),(phpt50neq1,"phpt50neq1"), (phpt100neq1,"phpt100neq1")]

    invZ = 'abs(m_lep_ph-91)>15' ## inverse Z resonance cut
    inZ  = 'abs(m_lep_ph-91)<15' ## Z resonance cut
    gtZ = '(m_lep_ph-91)>15'     ## greater than Z mass 
    ltZ = '(91-m_lep_ph)>15'     ## less than Z mass 
    cut_z = [nocut, (inZ, "inz"), (invZ, "invz"),(gtZ,"gtZ"), (ltZ,"ltZ")]

    ### electron selections
    selbase_el_EB = selbase_el + ' && ph_IsEB[0]' #leading photon in barrel

    passpix = 'ph_hasPixSeed[0]==0'  #Pixel seed
    failpix = 'ph_hasPixSeed[0]==1'
    cut_pix = [nocut, (passpix,"ppix"), (failpix,"fpix")]

    passcsev = 'ph_passEleVeto[0]==1' #CSEV: Conversion safe electron veto
    failcsev = 'ph_passEleVeto[0]==0' 
    cut_csev = [nocut, (passcsev,"pcsev"), (failcsev,"fcsev")]

    selarray = [[(selbase_el_EB,"basephEB"),], cut_pix, cut_met, cut_phpt ]

    ### edit here for plot variables i.e. what is on the x axis
    vararray = [ #("el_n",        (10,0,10),      "num of electrons"), ## variable name, x axis range, x axis label
                ("el_pt[0]",    (50,0,200),     "p_{T}(e, leading)"),
     #           ("ph_n",        (10,0,10),      "num of photons"), 
     #           ("ph_pt[0]",    (50,0,200),     "p_{T}(#gamma, leading)"),
     #           ("met_pt",      (50,0,400),     "MET"),
     #           ("met_phi",    (20,-pi,pi),    "MET #phi"),
                ]


#    legend_config = {'legendLoc':"Double","legendTranslateX":0.3}
    hist_config = {"logy":1,"blind":True, "weight": "NLOWeight"}
    makeplots(sampManElG,vararray, selarray, hist_config,{}, "log")

    #legend_config = {'legendLoc':"Double","legendTranslateX":0.3}
    #hist_config = {"blind":True, "weight": "PUWeight*NLOWeight"}
    #makeplots(vararray, selarray, hist_config, legend_config)
    
    if options.outputDir:
        ## write and close root file
        f1.Write()
        f1.Close()





def makeplots(samples,vararray, selprearray=None, hist_config=None, legend_config=None, extratag = "", dirname = "temp"):
    #print selprearray
    chlist ="[]{}()"
    if selprearray is None or not isinstance(selprearray,(tuple,list)):
        return
    else:
        selarray = product(*selprearray)
    
    #print selarray
    for sel in selarray:
        selection, name = makeselection(sel)
        for var in vararray:
            savename = var[0]+"_SEL_"+name+"_"+extratag+".pdf"
            for ch in chlist:
                savename = savename.replace(ch,"")
            hist_config["xlabel"] = var[2] 
            print(var[0], selection, savename)
            samples.Draw(var[0], selection, var[1], hist_config, legend_config)
            samples.print_stack_count()
            samples.SaveStack(savename, dirname, 'base')

def makeselection(sel):
    #print sel
    sel, name  = list(zip(*sel))
    sel = [s for s in sel if s != ""]
    name = [n for n in name if n != ""]
    sel  = "&&".join(sel)
    name  = "_".join(name)
    return sel, name




def doratio(h1,h2):
    hratio = h1.Clone("hratio")
    hratio.Divide(h2)
    hratio.SetMarkerStyle(20)
    hratio.SetMarkerSize(1.1)
    hratio.SetStats(0)
    hratio.SetTitle("")
    hratio.GetYaxis().SetTitle("ratio")
    hratio.SetLineColor(ROOT.kBlack)
    hratio.SetLineWidth(2)
    hratio.GetYaxis().SetTitleSize(0.10)
    hratio.GetYaxis().SetTitleOffset(0.6)
    hratio.GetYaxis().SetLabelSize(0.10)
    hratio.GetXaxis().SetLabelSize(0.10)
    hratio.GetXaxis().SetTitleSize(0.10)
    hratio.GetXaxis().SetTitleOffset(1.0)
    hratio.GetYaxis().SetRangeUser(0.5,1.5)
    #hratio.GetYaxis().UnZoom()
    hratio.GetYaxis().CenterTitle()
    hratio.GetYaxis().SetNdivisions(506, True)
    return hratio

def cmsinternal(pad):
    pad.cd()
    tex = ROOT.TLatex(0.18,0.93,"CMS Internal")
    tex.SetNDC()
    tex.SetTextSize(0.05)
    tex.SetLineWidth(2)
    tex.Draw()
    return tex

def ratioline(hratio):
    left_edge  = hratio.GetXaxis().GetXmin()
    right_edge = hratio.GetXaxis().GetXmax()
    
    oneline = ROOT.TLine(left_edge, 1, right_edge, 1)
    oneline.SetLineStyle(3)
    oneline.SetLineWidth(2)
    oneline.SetLineColor(ROOT.kBlack)
    oneline.Draw()
    return oneline

def hformat(h1,color):
    h1.SetLineColor(color)
    h1.SetMarkerColor(color)
    #h1.SetMarkerStyle(20)
    h1.SetMarkerSize(1.1)
    h1.SetStats(0)
    h1.SetLineWidth(2)
    h1.GetYaxis().SetTitleSize(0.05)
    h1.GetYaxis().SetTitleOffset(1.15)
    h1.GetYaxis().SetLabelSize(0.05)
    h1.GetXaxis().SetLabelSize(0.05)
    h1.GetXaxis().SetTitleSize(0.05)
    h1.GetXaxis().SetTitleOffset(0.8)


main()

