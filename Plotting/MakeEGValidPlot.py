#!/usr/bin/env python3
exec(compile(open("MakeBase.py", "rb").read(), "MakeBase.py", 'exec'))


year = options.year
lconf = {"labelStyle":str(year),"extra_label":"%i Electron Channel" %year, "extra_label_loc":(.17,.82)}
lgconf = {'legendLoc':"Double","legendTranslateX":0.35, "legendCompress":.9, "fillalpha":.5}
hlist = []
#sampManElG.ReadSamples( _SAMPCONF )
#samples = sampManElG
#
### control region (low met, Z mass)
#selection = baseel+ph_eb+el_eb+metlt40+massZ+phptgt%30+elpt40 + "&& ph_passMedium[0]"
#sf = samples.SetFilter(selection)
#
#for tag, sel in [("passpix",passpix.lstrip(" &")), ("failpix",failpix.lstrip(" &"))]:
#    ## flattened phi
#    save_as = ("flatphphi_%ielg_%s.pdf" %(year,tag), options.outputDir, "base")
#    hconf = {"unblind":True, "doratio":True,"xlabel":"flattened #phi (>6.28 for +ve #eta)","xunit":"","drawsignal":False}
#    hf = sf.SetHisto1DFast(flatphi, sel, (72,0,pi*4), weight, hconf, lgconf , lconf, save_as)
#    hlist.append(hf)
#
#    ## photon pT
#    save_as = ("phpt_%ielg_%s.pdf" %(year,tag), options.outputDir, "base")
#    hconf = {"unblind":True, "doratio":True, "xlabel":"photon pT", "drawsignal":False, "logy":True, "ymin":10}
#    hf = sf.SetHisto1DFast("ph_pt[0]",  sel, (40,0,200), weight, hconf, lgconf , lconf, save_as)
#    hlist.append(hf)
#
#    ## deta
#    save_as = ("deta_%ielg_%s.pdf" %(year,tag), options.outputDir, "base")
#    hconf = {"unblind":True, "doratio":True, "xlabel":"photon pT", "drawsignal":False, "logy":True, "ymin":10}
#    hf = sf.SetHisto1DFast("ph_eta[0]-el_eta[0]",  sel, (60,-3,3), weight, hconf, lgconf , lconf, save_as)
#    hlist.append(hf)
#
#    ## FIXME unblind, and weight in DATA
#
#for hf in hlist:
#    hf.DrawSave()
#    sc = samples.get_stack_count(includeData=True)
#    nmc = sc["TOTAL"][0]
#    ndt = sc["Data"][0]
#    print "mccount, datacount, mc/dt: ", nmc, ndt, nmc/ ndt



sampManElEl.ReadSamples( _SAMPCONF )
samples = sampManElEl

selection = "el_n==2"
sf = samples.SetFilter(selection)
hlist=[]

varlist = [ ("met_pt","MET","GeV",(100,0,250)),
            ("m_ll","m(e,e)","GeV",(100,0,200)),
            ("mt_res","reco mT","GeV",(100,0,200)),
            ("ph_pt", "#gamma pT", "GeV", (100,0,200)),
            ("el_pt[0]", "leading e pT", "GeV", (100,0,300)),
            ("el_pt[1]", "subleading e pT", "GeV", (100,0,300)),
            ("el_eta[0]", "leading e #eta",    "", (50,-3,3)),
            ("el_eta[1]", "subleading e #eta", "", (50,-3,3)),
            ]

#no log
var2list = [ ("met_pt","MET","GeV",(100,0,100)),
            ("met_phi", "MET #phi", "", (72,-pie,pie)),
            ("el_phi[0]", "leading e #phi", "", (72, -pie, pie)),
            ("el_phi[1]", "subleading e #phi", "", (72, -pie, pie)),
            ]

for var in varlist:
    varname = str.translate(var[0],None,"[]_")
    save_as = ("%s_%ielel_ln.pdf" %(varname,year), options.outputDir, "base")
    hconf = {"unblind":True, "doratio":True,"xlabel":var[1],"xunit":var[2],"drawsignal":False, "logy":True,"ymin":10}
    hf = sf.SetHisto1DFast(var[0], "", var[3], weight, hconf, lgconf , lconf, save_as)
    hlist.append(hf)
    save_as = ("%s_%ielel_elselln.pdf" %(varname,year), options.outputDir, "base")
    sel = (el_eb+elpt40).lstrip("& ")
    hf = sf.SetHisto1DFast(var[0], sel, var[3], weight, hconf, lgconf , lconf, save_as)
    hlist.append(hf)

for var in var2list:
    varname = str.translate(var[0],None,"[]_")
    save_as = ("%s_%ielel.pdf" %(varname,year), options.outputDir, "base")
    hconf = {"unblind":True, "doratio":True,"xlabel":var[1],"xunit":var[2],"drawsignal":False}
    hf = sf.SetHisto1DFast(var[0], "", var[3], weight, hconf, lgconf , lconf, save_as)
    hlist.append(hf)
    save_as = ("%s_%ielel_elsel.pdf" %(varname,year), options.outputDir, "base")
    sel = (el_eb+elpt40).lstrip("& ")
    hf = sf.SetHisto1DFast(var[0], sel, var[3], weight, hconf, lgconf , lconf, save_as)
    hlist.append(hf)

for hf in hlist:
    hf.DrawSave()
    #sc = samples.get_stack_count(includeData=True)
    #nmc = sc["TOTAL"][0]
    #ndt = sc["Data"][0]
    #print "mccount, datacount, mc/dt: ", nmc, ndt, nmc/ ndt
