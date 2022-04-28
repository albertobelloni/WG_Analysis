#!/usr/bin/env python3
import matplotlib.pyplot as plt
import sys, json
from collections import OrderedDict, defaultdict

def addparser(parser):
    parser.add_argument('--ch',         default="el",        help='Choose muon or electron channel [mu/el]' )
    parser.add_argument('--plot',       action="store_true", help='Save plots' )

exec(compile(open("MakeBase.py", "rb").read(), "MakeBase.py", 'exec'))
from DrawConfig import DrawConfig


###
### This script makes efficiency map for b tagging SF
###
print(os.getcwd())

year = options.year
ch = options.ch
chname = "Electron" if ch=="el" else "Muon"
leplatex = "e" if ch=="el" else "#mu"

lconf = {"labelStyle":str(year),"extra_label":["%i %s Channel" %(year,chname),
                                               "p_{T}^{%s}>35GeV, MET>40GeV" %leplatex,
                                               "Tight barrel #gamma p_{T}^{#gamma}>80GeV"],
                                               "extra_label_loc":(.17,.82)}
lgconf = { 'legendLoc':"Double","legendTranslateX":0.33, "legendCompress":.8,
           "fillalpha":.5, "legendWiden":.95 }

ptbin = [0,20,30,50,70,100,140,200,300,600,1000]
etabin = [-2.5,-2.,-1.5,-1.,-0.5,0.,0.5,1.,1.5,2.,2.5]

def makeplots(year, ch):
    f1 = ROOT.TFile("data/btag/btageff%i%s.root"%(year,ch))
    heffb = f1.Get("heffb")
    heffc = f1.Get("heffc")
    heffl = f1.Get("heffl")
    c1 =  ROOT.TCanvas("c1","c1",800,500)
    c1.SetLogx(1)
    heffb.GetZaxis().SetRangeUser(0.,1.)
    heffb.Draw("COLZ TEXT")
    c1.SaveAs("%s/heffb%i%s.pdf" %(options.outputDir, year, ch))
    c1.SaveAs("%s/heffb%i%s.png" %(options.outputDir, year, ch))
    c1.SaveAs("%s/heffb%i%s.C" %(options.outputDir, year, ch))
    heffc.GetZaxis().SetRangeUser(0.,.5)
    heffc.Draw("COLZ TEXT")
    c1.SaveAs("%s/heffc%i%s.pdf" %(options.outputDir, year, ch))
    c1.SaveAs("%s/heffc%i%s.png" %(options.outputDir, year, ch))
    c1.SaveAs("%s/heffc%i%s.C" %(options.outputDir, year, ch))

    heffl.GetZaxis().SetRangeUser(0.,.2)
    heffl.Draw("COLZ TEXT")
    c1.SaveAs("%s/heffl%i%s.pdf" %(options.outputDir, year, ch))
    c1.SaveAs("%s/heffl%i%s.png" %(options.outputDir, year, ch))
    c1.SaveAs("%s/heffl%i%s.C" %(options.outputDir, year, ch))

if options.plot:
    for year in [2016,2017,2018]:
        for ch in ["mu","el"]:
            makeplots(year,ch)
    sys.exit()


if ch=="mu":

    ## read MuG samples
    sampManMuG= SampleManager( options.baseDirMuG, _TREENAME, filename=_FILENAME, xsFile=_XSFILE, lumi=_LUMI*lumiratio,
                               readHists=False , weightHistName = "weighthist", dataFrame = False, quiet = options.quiet)

    sampManMuG.ReadSamples( _SAMPCONF )
    samples = sampManMuG

if ch=="el":

    ## read ElG samples
    sampManElG= SampleManager( options.baseDirElG, _TREENAME, filename=_FILENAME, xsFile=_XSFILE, lumi=_LUMI*lumiratio ,
                               readHists=False , weightHistName = "weighthist", dataFrame = False, quiet = options.quiet)

    sampManElG.ReadSamples( _SAMPCONF )
    samples = sampManElG



kinedict = defs.kinedictgen(ch)
cutsetdict = {k: defs.makeselstring(ch=ch, **w ) for k,w in kinedict.items()}

if year==2016:
    bcutvalue=0.3093
if year==2017:
    bcutvalue=0.3033
if year==2018:
    bcutvalue=0.2770

ROOT.gStyle.SetPalette(ROOT.kBird)

teststr='mu_n==1 && el_n==0 && ph_n==1 && met_pt > 40 && mu_pt_rc[0] > 35  && ph_IsEB[0] && ph_passTight[0] && ph_pt[0] > 200  && !ph_hasPixSeed[0]'
if ch == "el":
    teststr = "el_n==1 && mu_n==0 && ph_n==1 &&  fabs( el_eta[0] ) < 2.1  && el_pt[0] > 35  &&  el_passTight[0] == 1 && met_pt > 40 && fabs(m_lep_ph-91)>20.0 && ph_IsEB[0] && ph_passTight[0] && ph_pt[0] > 80  && !ph_hasPixSeed[0]"

if not os.path.isdir( "data/btag") :
    os.makedirs( "data/btag" )
f1 = ROOT.TFile("data/btag/btageff%i%s.root"%(year,ch),"RECREATE")
## cutsets
for key, (selfull, weight) in cutsetdict.items():
    print(key)
    print(selfull)
    print(weight)

hconf = {"drawopt":"COLZ TEXT", "xlabel":"jet pT", "ylabel":"jet eta"}


### light jet eff
samples.Draw("jet_eta:jet_pt",teststr + "&& jet_flav==0",(ptbin,etabin),hconf)
#samples.SaveStack("hbasel%i%s.pdf" %(year,ch), options.outputDir, "base")
hbasel = samples["__AllStack__"].hist.Clone("hbasel")

samples.Draw("jet_eta:jet_pt",teststr + "&& jet_flav==0 && jet_bTagDeepb > %g" %bcutvalue ,(ptbin,etabin),hconf)
#samples.SaveStack("hnuml%i%s.pdf" %(year,ch), options.outputDir, "base")
hnuml = samples["__AllStack__"].hist.Clone("hnuml")
heffl = samples["__AllStack__"].hist.Clone("heffl")
heffl.Divide(hnuml,hbasel,1,1,"B")
#heffl.Draw("COLZ TEXT")
#samples.SaveStack("heffl%i%s.pdf" %(year,ch), options.outputDir, "base")

### c jet eff
samples.Draw("jet_eta:jet_pt",teststr + "&& jet_flav==4",(ptbin,etabin),hconf)
#samples.SaveStack("hbasec%i%s.pdf" %(year,ch), options.outputDir, "base")
hbasec = samples["__AllStack__"].hist.Clone("hbasec")

samples.Draw("jet_eta:jet_pt",teststr + "&& jet_flav==4 && jet_bTagDeepb > %g" %bcutvalue ,(ptbin,etabin),hconf)
#samples.SaveStack("hnumc%i%s.pdf" %(year,ch), options.outputDir, "base")
hnumc = samples["__AllStack__"].hist.Clone("hnumc")
heffc = samples["__AllStack__"].hist.Clone("heffc")
heffc.Divide(hnumc,hbasec,1,1,"B")
#heffc.Draw("COLZ TEXT")
#samples.SaveStack("heffc%i%s.pdf" %(year,ch), options.outputDir, "base")


### b jets eff
samples.Draw("jet_eta:jet_pt",teststr + "&& jet_flav==5",(ptbin,etabin),hconf)
#samples.SaveStack("hbaseb%i%s.pdf" %(year,ch), options.outputDir, "base")
hbaseb = samples["__AllStack__"].hist.Clone("hbaseb")

samples.Draw("jet_eta:jet_pt",teststr + "&& jet_flav==5 && jet_bTagDeepb > %g" %bcutvalue ,(ptbin,etabin),hconf)
#samples.SaveStack("hnumb%i%s.pdf" %(year,ch), options.outputDir, "base")
hnumb = samples["__AllStack__"].hist.Clone("hnumb")
heffb = samples["__AllStack__"].hist.Clone("heffb")
heffb.Divide(hnumb,hbaseb,1,1,"B")
#heffb.Draw("COLZ TEXT")
#samples.SaveStack("heffb%i%s.pdf" %(year,ch), options.outputDir, "base")

for h in (hbasel,hnuml,heffl,
          hbasec,hnumc,heffc,
          hbaseb,hnumb,heffb):
    h.Write()
f1.Close()

