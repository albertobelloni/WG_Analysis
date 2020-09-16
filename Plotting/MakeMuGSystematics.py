#!/usr/bin/env python
import matplotlib.pyplot as plt
import sys, json
from collections import OrderedDict

def addparser(parser):
    parser.add_argument('--massplots',  action='store_true', help='Make nuisance parameters vs mass plots' )
#alt_condor =True

execfile("MakeBase.py")
from DrawConfig import DrawConfig

###
### This script makes N-1/ final selection distribution plots
###

year = options.year
_JSONNAME = 'data/mugsys%i.json' %options.year

#lconf = {"labelStyle":str(year),"extra_label":"%i Muon Channel" %year, "extra_label_loc":(.17,.82)}
lconf = {"labelStyle":str(year),"extra_label":["%i Muon Channel" %year,
                                               "p_{T}^{#mu}>35GeV, MET>40GeV",
                                               "Tight barrel #gamma p_{T}^{#gamma}>80GeV"],
                                               "extra_label_loc":(.17,.82)}
lgconf = {'legendLoc':"Double","legendTranslateX":0.32, "legendCompress":.8, "fillalpha":.5, "legendWiden":.95}
xpoints = [300,350,400,450,500,600,700,800,900,1000,1200,1400,1600,1800,2000]



#sellist, weight =  defs.makeselstringlist( ch = "mu", phpt = 40, leppt = 35, met = 40 )
#sellist, weight =  defs.makeselstringlist( ch = "mu", phpt = 100, leppt = 35, met = 80 )
#selfull = " && ".join(sellist) ## full signal selection

def formathist(h):
    h.SetStats(0)
    h.SetLineWidth(2)

def formathratio(hratio, rrange = None):
    hratio.GetYaxis().SetNdivisions(506)
    hratio.GetYaxis().SetTitleSize(0.06)
    hratio.GetYaxis().SetLabelSize(0.06)
    hratio.GetXaxis().SetLabelSize(0.06)
    hratio.GetXaxis().SetTitleSize(0.06)
    if rrange:
        hratio.GetYaxis().SetRangeUser(*rrange)
    else:
        hratio.GetYaxis().SetRangeUser(0.5,1.5)

def makecomparisonplot( samplemanager, histograms, hist_config=None, label_config=None, legend_config=None,
                                                   savename="test.pdf", normalize = True , hist_pars = None , logy=True):

    ## input list of histograms, plot on standard ratio plot routine
    _COLOR = [ ROOT.kBlue, ROOT.kBlue+2,
               ROOT.kRed,  ROOT.kRed+2,
               ROOT.kGreen, ROOT.kGreen+2,
               ROOT.kViolet, ROOT.kViolet+2,
               ROOT.kOrange, ROOT.kOrange-1,
               ROOT.kAzure+1, ROOT.kAzure+3,
               ROOT.kViolet+6, ROOT.kViolet+7,
               ROOT.kOrange+1, ROOT.kOrange+2,
               ROOT.kAzure+8, ROOT.kAzure+9,
               ]

    hnorm=histograms.pop(0)

    ## deduce histogram binnings
    if hist_pars == None:
        nbin = histograms[0].GetNbinsX()
        xaxis = histograms[0].GetXaxis()
        hist_pars = (nbin, xaxis.GetBinLowEdge(1), xaxis.GetBinUpEdge(nbin))

    samplemanager.create_standard_ratio_canvas()
    samplemanager.curr_canvases["top"].cd()
    samplemanager.curr_canvases["top"].SetTopMargin(0.08)
    samplemanager.curr_canvases["top"].SetBottomMargin(0.08)
    samplemanager.curr_canvases["top"].SetLeftMargin(0.15)
    samplemanager.curr_canvases["top"].SetRightMargin(0.05)
    samplemanager.curr_canvases["top"].SetGrid()
    if logy: samplemanager.curr_canvases["top"].SetLogy()

    ## Draw top canvas
    formathist(hnorm)
    if normalize: hnorm.Scale(1./hnorm.Integral())
    hnorm.Draw("hist")
    for i, h in enumerate(histograms):
        formathist(h)
        if normalize: h.Scale(1./h.Integral())
        h.SetLineColor(_COLOR[i])
        h.Draw("same hist")

    ## make hratio
    hratios = [h.Clone() for h in histograms]
    rrange = hist_config.get("rrange")
    for hr in hratios:
        hr.Divide(hnorm)
        formathratio(hr, rrange)

    drawconf = DrawConfig( "mt_res", "selection", hist_pars, legend_config.get("legend_entries"),
                            hist_config, legend_config, label_config)
    # draw labels
    labels = drawconf.get_labels()
    for l in labels :
        l.Draw()

    # draw legend
    leg = samplemanager.create_standard_legend( len(histograms)+1 , drawconf )
    legend_entries = drawconf.get_legend_entries()
    leg.AddEntry( hnorm, legend_entries.pop(0) , "L" )
    for i, h in enumerate(histograms):
        leg.AddEntry( h, legend_entries[i], "L" )
    leg.Draw()

    samplemanager.curr_canvases["bottom"].cd()
    samplemanager.curr_canvases["bottom"].SetGrid()
    hratios[0].Draw("hist")
    for hr in hratios[1:]:
        hr.Draw("hist same")

    samples.SaveStack(savename, options.outputDir, "base")

    return hratios, leg, labels


def makeplots():
    #plt.style.use("seaborn-whitegrid")
    plt.style.use("fivethirtyeight")
    with open(_JSONNAME) as fo: systematic_dict = json.load(fo)
    ### FIXME !! for missing sample
    if options.year ==2017:
        for sys in systematic_dict.keys():
            systematic_dict[sys]['MadGraphResonanceMass350_width0p01'] = systematic_dict[sys]['MadGraphResonanceMass350_width5']
    if options.year ==2018:
        for sys in systematic_dict.keys():
            systematic_dict[sys]['MadGraphResonanceMass450_width0p01'] = systematic_dict[sys]['MadGraphResonanceMass450_width5']

    ### plot 1: MET and energy scale
    syslists= [  ('JetResUp',        'JetResDown'),
                 ('JetEnUp',         'JetEnDown'),
                 ('MuonEnUp',        'MuonEnDown'),
                 ('ElectronEnUp',    'ElectronEnDown'),
                 ('PhotonEnUp',      'PhotonEnDown'),
                 ('UnclusteredEnUp', 'UnclusteredEnDown'),]

    fig = plt.figure(figsize=(12,12))
    for i,syslist in enumerate(syslists):
        sysvalues = [[systematic_dict[sys]['MadGraphResonanceMass%i_width%s' %(m,w)] for m in xpoints] \
          for sys in syslist for w in ("0p01","5")]
        ax=plt.subplot(3,2,1+i)
        ax.plot(xpoints, sysvalues[0], color = 'darkblue', label = 'up width 0.01')
        ax.plot(xpoints, sysvalues[1], color = 'lightblue', label = 'up width 5')
        ax.plot(xpoints, sysvalues[2], color = 'darkred', label = 'down width 0.01')
        ax.plot(xpoints, sysvalues[3], color = 'salmon', label = 'down width 5')
        if i>3: ax.set_xlabel('Mass [GeV]')
        if i%2==0: ax.set_ylabel('normalization shift %')
        ax.set_title(syslist[0][:-2], loc='left', color = 'orange')
        if i == 5:
            handles, labels = ax.get_legend_handles_labels()
            fig.legend(handles, labels, loc='upper right')
    fig.text(0.1, 0.95, 'Muon Channel %i'%options.year, fontsize=20, fontweight='bold')
    plt.savefig("%s/mu%isys_enscale_bymass.png" %(options.outputDir,options.year))
    plt.savefig("%s/mu%isys_enscale_bymass.pdf" %(options.outputDir,options.year))

    ### plot 2: electron, photon scale factors and prefiring
    syslists = [
     ("mu_trigSFUP", "mu_trigSFDN"),
     ("mu_idSFUP", "mu_idSFDN"),
     #("mu_trkSFUP", "mu_trkSFDN"), ## all zero FIXME?
     ("mu_isoSFUP", "mu_isoSFDN"),
     ('ph_idSFUP','ph_idSFDN'),
     ('ph_psvSFUP','ph_psvSFDN'),
     ('prefup','prefdown'),]

    fig = plt.figure(figsize=(12,12))
    for i,syslist in enumerate(syslists):
        sysvalues = [[systematic_dict[sys]['MadGraphResonanceMass%i_width%s' %(m,w)] for m in xpoints] \
          for sys in syslist for w in ("0p01","5")]
        ax=plt.subplot(3,2,1+i)
        ax.plot(xpoints, sysvalues[0], color = 'darkblue', label = 'up width 0.01')
        ax.plot(xpoints, sysvalues[1], color = 'lightblue', label = 'up width 5')
        ax.plot(xpoints, sysvalues[2], color = 'darkred', label = 'down width 0.01')
        ax.plot(xpoints, sysvalues[3], color = 'salmon', label = 'down width 5')
        if i>3: ax.set_xlabel('Mass [GeV]')
        if i%2==0: ax.set_ylabel('normalization shift %')
        ax.set_title(syslist[0][:-2], loc='left', color = 'orange')
        if i == 5:
            handles, labels = ax.get_legend_handles_labels()
            fig.legend(handles, labels, loc='upper right')
    fig.text(0.1, 0.95, 'Muon Channel %i'%options.year, fontsize=20, fontweight='bold')
    plt.savefig("%s/mu%isys_sf_bymass.png" %(options.outputDir,options.year))
    plt.savefig("%s/mu%isys_sf_bymass.pdf" %(options.outputDir,options.year))

    ### plot 3: pdf scale and pu weights
    pdflist = ['muR1muF2',
     'muR1muFp5',
     'muR2muF1',
     'muR2muF2',
     'muRp5muF1',
     'muRp5muFp5',]
    pileup = ['PUUP5','PUDN5','PUUP10','PUDN10']


    sysvalues = [[systematic_dict[sys]['MadGraphResonanceMass%i_width%s' %(m,w)] for m in xpoints] \
      for sys in  pdflist for w in ("0p01","5")]
    sysnamess = [ "%s %s" %(sys,w)
      for sys in  pdflist for w in ("narrow","wide")]
    puvalues = [[systematic_dict[sys]['MadGraphResonanceMass%i_width%s' %(m,w)] for m in xpoints] \
      for sys in  pileup for w in ("0p01","5")]
    punamess = [ "%s %s" %(sys,w)
      for sys in  pileup for w in ("narrow","wide")]

    fig = plt.figure(figsize=(12,12))
    ax=fig.add_subplot(211)
    cmap = plt.get_cmap('Paired')
    for i ,v in enumerate(sysvalues):
        ax.plot(xpoints, v,   color = cmap(i), label = sysnamess[i])
    ax.set_xlabel('Mass [GeV]')
    ax.set_ylabel('normalization shift %')
    ax.set_title( "PDF weights", loc='left', color = 'orange')
    ax.legend(loc="best")
    ax=fig.add_subplot(212)
    cmap = plt.get_cmap('Paired')
    for i, v in enumerate(puvalues):
        ax.plot(xpoints, v,   color = cmap(i), label = punamess[i])
    ax.set_xlabel('Mass [GeV]')
    ax.set_ylabel('normalization shift %')
    ax.set_title( "PU weights", loc='left', color = 'orange')
    ax.legend(loc="best")
    fig.text(0.1, 0.95, 'Muon Channel 2016', fontsize=16, fontweight='bold')
    plt.savefig("%s/mu%isys_pdfpu_bymass.png" %(options.outputDir,options.year))
    plt.savefig("%s/mu%isys_pdfpu_bymass.pdf" %(options.outputDir,options.year))
    return



if options.massplots:
    makeplots()
    sys.exit()

sampManMuG.ReadSamples( _SAMPCONF )
samples = sampManMuG

selection = "mu_n==1 && ph_n==1"
sf = samples.SetFilter(selection)
hlist=[]


## (de-)activate datasets
#samples.deactivate_all_samples()
#samples.activate_sample("WGamma")
## activate all signal
#signames = [ s.name for s in samples.get_samples(isSignal = True)]
activesignames = [ s.name for s in samples.get_samples(isSignal = True, isActive=True)]
#for s in signames:
#    samples.activate_sample(s)
## activate all signal
signames = [ s.name for s in samples.get_samples(isSignal = True)]
for s in signames:
    samples.activate_sample(s)
activesignames = [ s.name for s in samples.get_samples(isSignal = True, isActive=True)]

## FIXME bjet SF to be added
SFlist = [#"el_trig", "el_id", "el_reco",
          "mu_trig", "mu_id", "mu_trk", "mu_iso", # ignore for e channel
          "ph_id",   "ph_psv"] ## SF, SFUP, SFDOWN

metlist=[
            "JetRes",
            "JetEn",
            "MuonEn",
            "ElectronEn",
            "PhotonEn",
            "UnclusteredEn", #--/Up/Down
        ]

eventweightlist = ["muR1muF2",
                   "muR1muFp5",
                   "muR2muF1",
                   "muR2muF2",
                   "muRp5muF1",
                   "muRp5muFp5"
                   ]


sellist, weight =  defs.makeselstringlist( ch = "mu", phpt = 80, leppt = 35, met = 40 )

if options.year == 2018: weight = weight.replace("*prefweight","") ## no prefiring weight in 2018
sellist +=["mt_res>200"]
selfull = " && ".join(sellist) ## full signal selection
print selfull
print weight

selection_list = OrderedDict()
selection_list["norm"] = dict( w=weight, sel=selfull)

## met uncertainty
mettaglist = [mname+shift for mname in metlist for shift in ["Up","Down"]]
for tag in mettaglist:
    w = weight.replace("mt_res", "mt_res_%s" %tag )\
              .replace("met_pt", "met_%s_pt" %tag )
    sel = selfull.replace("mt_res", "mt_res_%s" % tag )\
                 .replace("met_pt", "met_%s_pt" % tag )
    if tag == "MuonEnUp":
        sel = sel.replace("mu_pt_rc", "mu_pt_rc_up")
    if tag == "MuonEnDown":
        sel = sel.replace("mu_pt_rc", "mu_pt_rc_down")
    var = "mt_res_%s" %tag
    selection_list[tag] = dict( w = w, sel = sel, var = var)

### muon and electron scale factors
sftaglist = [sfname+"SF"+shift for sfname in SFlist for shift in ["UP","DN"]]
for tag in sftaglist:
    sel = selfull
    w = weight.replace(tag[:-2], tag)
    selection_list[tag] = dict( w=w, sel=sel )

pupreftaglist = []
for shift in ["up","down"]:
    sel=selfull
    w = weight.replace("prefweight" , "prefweight%s" % shift )
    selection_list["pref"+shift] = dict( w=w, sel=sel )
    pupreftaglist.append("pref%s"%shift)

for shift in ["UP5", "UP10", "DN5", "DN10"]:
    sel=selfull
    w = weight.replace("PUWeight" , "PUWeight%s" % shift )
    selection_list["PU"+shift] = dict( w=w, sel=sel )
    pupreftaglist.append("PU%s"%shift)

# event weights (pdf)
for i, shift in enumerate(eventweightlist):
    sel=selfull
    w = weight.replace("NLOWeight" , "NLOWeight*PDFWeights[%i]" % i )
    selection_list[shift] = dict( w=w, sel=sel )


######## booking histograms ########

for sysname, seldict in selection_list.iteritems():
    var = seldict.get("var", "mt_res")
    weight = seldict["w"]
    sel = seldict["sel"]
    save_as = ("%s_%imug.pdf" %(sysname,year), options.outputDir, "base")
    hconf = { "xlabel": "Reco Mass","xunit": "GeV" ,"drawsignal":True, "logy":True}
    hf = sf.SetHisto1DFast(var, sel, (90,200,2000), weight, hconf, lgconf , lconf, save_as, data_exp = True)
    selection_list[sysname]["hist"] = hf


print selection_list.keys()
for sysname, seldict in selection_list.iteritems():
    hf = seldict["hist"]
    hf.DrawSave()
    seldict["stackcount"] = samples.get_stack_count()
    seldict["hstack"] = samples["__AllStack__"].hist.Clone()
    seldict["hsignals"]={}
    for sname in activesignames:
        seldict["hsignals"][sname] = samples[sname].hist.Clone()

## met uncertainty
taglist = ["norm",]+ mettaglist #[mname+shift for mname in metlist for shift in ["Up","Down"]]
lgconf["legend_entries"] = taglist
histlist = [ selection_list[t]["hstack"] for t in taglist ]
hratiolist, leg, labels = makecomparisonplot( samples, histlist, hconf, lconf, lgconf, "stackcomp_metsys%i.pdf" %year )
for mname in metlist:
    taglist = ["norm",]+[mname+shift for shift in ["Up","Down"]]
    lgconf["legend_entries"] = taglist
    histlist = [ selection_list[t]["hstack"] for t in taglist ]
    hratiolist, leg, labels = makecomparisonplot( samples, histlist, hconf, lconf, lgconf, "stackcomp_%ssys%i.pdf" %(mname,year) )

## draw shape comparison plot for SF shifts
taglist = ["norm",] +sftaglist
lgconf["legend_entries"] = taglist
histlist = [ selection_list[t]["hstack"] for t in taglist ]
hratiolist, leg, labels = makecomparisonplot( samples, histlist, hconf, lconf, lgconf, "stackcomp_sfsys%i.pdf" %year )

## draw shape comparison plot for prefiring weights and PU shifts
taglist = ["norm",] +pupreftaglist
lgconf["legend_entries"] = taglist
histlist = [ selection_list[t]["hstack"] for t in taglist ]
hratiolist, leg, labels = makecomparisonplot( samples, histlist, hconf, lconf, lgconf, "stackcomp_ppusys%i.pdf" %year )

## draw shape comparison plot for PDF weight shifts
taglist = ["norm",] + eventweightlist
lgconf["legend_entries"] = taglist
histlist = [ selection_list[t]["hstack"] for t in taglist ]
hratiolist, leg, labels = makecomparisonplot( samples, histlist, hconf, lconf, lgconf, "stackcomp_pdfsys%i.pdf" %year )


for sname in activesignames:
    snameshort = sname.replace("MadGraphResonanceMass", "M")
    lconf = {"labelStyle":str(year),"extra_label":["%i Muon Channel" %year,
                                                   "p_{T}^{#mu}>35GeV, MET>40GeV",
                                                   "Tight barrel #gamma p_{T}^{#gamma}>80GeV",
                                                   "signal sample: %s" %snameshort],
                                                    "extra_label_loc":(.17,.82)}
    hconf["rrange"]=(0.85,1.15)
    ## met uncertainty
    taglist = ["norm",]+ mettaglist #[mname+shift for mname in metlist for shift in ["Up","Down"]]
    lgconf["legend_entries"] = taglist
    histlist = [ selection_list[t]["hsignals"][sname] for t in taglist ]
    savename = "shapecomp%s_metsys%i.pdf" %(snameshort,year)
    hratiolist, leg, labels = makecomparisonplot( samples, histlist, hconf, lconf, lgconf, savename, logy=False)
    for mname in metlist:
        taglist = ["norm",]+[mname+shift for shift in ["Up","Down"]]
        lgconf["legend_entries"] = taglist
        savename = "shapecomp%s_%ssys%i.pdf" %(snameshort,mname,year)
        histlist = [ selection_list[t]["hsignals"][sname] for t in taglist ]
        hratiolist, leg, labels = makecomparisonplot( samples, histlist, hconf, lconf, lgconf, savename, logy=False )

    ## draw shape comparison plot for SF shifts
    taglist = ["norm",] +sftaglist
    lgconf["legend_entries"] = taglist
    histlist = [ selection_list[t]["hsignals"][sname] for t in taglist ]
    savename = "shapecomp%s_sfsys%i.pdf" %(snameshort,year)
    hratiolist, leg, labels = makecomparisonplot( samples, histlist, hconf, lconf, lgconf, savename, logy=False)

    ## draw shape comparison plot for prefiring weights and PU shifts
    taglist = ["norm",] +pupreftaglist
    lgconf["legend_entries"] = taglist
    histlist = [ selection_list[t]["hsignals"][sname] for t in taglist ]
    savename = "shapecomp%s_ppusys%i.pdf" %(snameshort,year)
    hratiolist, leg, labels = makecomparisonplot( samples, histlist, hconf, lconf, lgconf, savename, logy=False)

    ## draw shape comparison plot for PDF weight shifts
    taglist = ["norm",] + eventweightlist
    lgconf["legend_entries"] = taglist
    histlist = [ selection_list[t]["hsignals"][sname] for t in taglist ]
    savename = "shapecomp%s_pdfsys%i.pdf" %(snameshort,year)
    hratiolist, leg, labels = makecomparisonplot( samples, histlist, hconf, lconf, lgconf, savename, logy=False)

hkeys = ["norm",]+mettaglist+sftaglist+pupreftaglist+eventweightlist
bkgcountnorm = selection_list["norm"]["stackcount"]["TOTAL"][0]
bkgcountnormerr = selection_list["norm"]["stackcount"]["TOTAL"][0]
print "MC stat error = ", bkgcountnormerr

for k in hkeys:
    bkgcount = selection_list[k]["stackcount"]["TOTAL"][0]
    #print "%.20s %.4g %.4g %.4g" %(k, bkgcount, bkgcountnorm, bkgcount/bkgcountnorm*100-100)
    print "%-20s %.2g" %(k, bkgcount/bkgcountnorm*100-100)

## systematics as function of mass
## systematic_dict[ systematic_name ][ sample_name ]
systematic_dict = dict()
for k in hkeys:
    systematic_dict[k] = dict()

for sname in activesignames:
    print
    print "signal name: ", sname
    sigcountnorm = selection_list["norm"]["stackcount"][sname][0]
    sigcountnormerr = selection_list["norm"]["stackcount"][sname][1]
    print "MC stat error = ", sigcountnormerr
    for k in hkeys:
        sigcount = selection_list[k]["stackcount"][sname][0]
        #print "%.20s %.4g %.4g %.4g" %(k, sigcount, sigcountnorm, sigcount/sigcountnorm*100-100)
        print "%-20s %.2g" %(k, sigcount/sigcountnorm*100-100)
        systematic_dict[k][sname] = sigcount/sigcountnorm*100-100

summarylist = [("TOTAL","bkg"),
               ("MadGraphResonanceMass1000_width5", "M1000w5"),
               ("MadGraphResonanceMass450_width5", "M450w5")]

print "%-15s" %"",
for sname, title in summarylist:
    print "%-8s" %title,
print

for k in hkeys:
    print "%-15s" %k,
    for sname, title in summarylist:
        count = selection_list[k]["stackcount"][sname][0]
        countnorm = selection_list["norm"]["stackcount"][sname][0]
        print "%8.2g" %(count/countnorm*100-100),
    print

with open( _JSONNAME , "w") as fw:
    json.dump(systematic_dict, fw)
