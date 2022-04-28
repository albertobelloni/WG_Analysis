#!/usr/bin/env python3
exec(compile(open("MakeBase.py", "rb").read(), "MakeBase.py", 'exec'))

###
### This script makes N-1/ final selection distribution plots
###

year = options.year
lconf = {"labelStyle":str(year),"extra_label":"%i Electron Channel" %year, "extra_label_loc":(.17,.82)}
lgconf = {'legendLoc':"Double","legendTranslateX":0.33, "legendCompress":.8, "fillalpha":.5, "legendWiden":.95}
hlist = []


sampManElG.ReadSamples( _SAMPCONF )
samples = sampManElG

selection = "el_n==1 && ph_n==1"
sf = samples.SetFilter(selection)
hlist=[]


def print_chi2(h1, h2, index, color = None):
    l2 = ROOT.TLatex()
    l2.SetNDC()
    l2.SetText(0.75,0.5-index*0.1,"Chi^{2}/ndf = %.3g" %h1.Chi2Test(h2,"WWCHI2/NDF"))
    l2.SetTextSize(0.07)
    if color: l2.SetTextColor(color)
    l2.Draw()
    return l2

sellist, weight =  defs.makeselstringlist( ch = "el", phpt = 40, leppt = 35, met = 40 )
#sellist, weight =  defs.makeselstringlist( ch = "el", phpt = 0, leppt = 0, met = 0 )
#sellist +=["mt_res>500"]
selfull = " && ".join(sellist) ## full signal selection

sel,w = defs.makeselstring("el")
mlist = [0,100,160,200,225,250,275,300,350,400,450,500,600,700,720]
#samplelist =  ["WGamma", "AllTop", "Zgamma","TopW"]
samplelist =  ["WGamma", "Top+X", "Others"]

hconf = {"weight":w,"doratio":1,"logy":1,"normalize":True,"bywidth":True,"rlabel":"ratio to W#gamma","xlabel":"m_{T}^{res}(e, #gamma, #slash{E}_{T})","reverseratio":1}
lconf = {"labelStyle":str(year),"extra_label":["%i Electron Channel" %year,"p_{T}^{e}>35GeV, MET>40GeV","Tight barrel #gamma p_{T}^{#gamma}>80GeV"], "extra_label_loc":(.17,.82)}
#samples.CompareSelections("mt_res",[sel+"&&mt_res>200"]*len(samplelist),samplelist,mlist, hconf, lconf)
samples.CompareSelections("mt_res",[sel+"&&jet_CSVMedium_n==0"]*len(samplelist),samplelist,mlist, hconf, lconf)

samples.curr_canvases["bottom"].cd()
harray = [ samples[name+"_mt_res*"] for name in samplelist ]
larray= []
for i, h in enumerate(harray[1:]):
    l = print_chi2(harray[0].hist, h.hist, i, color = h.color)
    larray.append(l)


samples.SaveStack("mtres_elg%i_sigsel_bkgdcomp.pdf" %year,options.outputDir,"base")

