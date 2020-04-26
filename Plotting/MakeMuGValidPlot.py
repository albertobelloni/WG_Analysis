#!/usr/bin/env python
execfile("MakeBase.py")


year = options.year
lconf = {"labelStyle":str(year),"extra_label":"%i Muon Channel" %year, "extra_label_loc":(.17,.82)}
lgconf = {'legendLoc':"Double","legendTranslateX":0.35, "legendCompress":.9, "fillalpha":.5}
hlist = []


sampManMuG.ReadSamples( _SAMPCONF )
samples = sampManMuG

selection = "mu_n==1 && ph_n==1"
sf = samples.SetFilter(selection)
hlist=[]

varlist = [ ("met_pt","MET","GeV",(100,0,400)),
            ("m_lep_ph","m(#mu, #gamma)","GeV",(100,0,400)),
            ("mt_res","reco mT","GeV",(100,0,1000)),
            ("ph_pt[0]", "leading #gamma pT", "GeV", (100,0,200)),
            ("mu_pt[0]", "leading #mu pT", "GeV", (100,0,300)),
            #("mu_pt[1]", "subleading #mu pT", "GeV", (100,0,300)),
            ("mu_eta[0]", "leading #mu #eta",    "", (50,-3,3)),
            #("mu_eta[1]", "subleading #mu #eta", "", (50,-3,3)),
            ]

#no log
var2list = [ ("met_pt","MET","GeV",(100,0,200)),
            ("met_phi", "MET #phi", "", (72,-pie,pie)),
            ("mu_phi[0]", "leading mu #phi", "", (72, -pie, pie)),
            #("mu_phi[1]", "subleading mu #phi", "", (72, -pie, pie)),
            ]


sellist, weight =  defs.makeselstringlist( ch = "mu", phpt = 40, leppt = 35, met = 40 )
selfull = " && ".join(sellist) ## full signal selection

for var in varlist:
    varname = str.translate(var[0],None,"[]_")
    sel = " && ".join([s for s in sellist if var[0] not in s ])
    save_as = ("%s_%imug_ln.pdf" %(varname,year), options.outputDir, "base")
    hconf = { "xlabel":var[1],"xunit":var[2],"drawsignal":False, "logy":True,"ymin":10}
    hf = sf.SetHisto1DFast(var[0], sel, var[3], weight, hconf, lgconf , lconf, save_as, data_exp = True)
    hlist.append(hf)
    #save_as = ("%s_%ielel_elselln.pdf" %(varname,year), options.outputDir, "base")
    #sel = (el_eb+elpt40).lstrip("& ")
    #hf = sf.SetHisto1DFast(var[0], sel, var[3], weight, hconf, lgconf , lconf, save_as)
    #hlist.append(hf)

for var in var2list:
    varname = str.translate(var[0],None,"[]_")
    sel = " && ".join([s for s in sellist if var[0] not in s ])
    save_as = ("%s_%imug.pdf" %(varname,year), options.outputDir, "base")
    hconf = {"xlabel":var[1],"xunit":var[2],"drawsignal":False}
    hf = sf.SetHisto1DFast(var[0], sel, var[3], weight, hconf, lgconf , lconf, save_as, data_exp = True)
    hlist.append(hf)
    #save_as = ("%s_%ielel_elsel.pdf" %(varname,year), options.outputDir, "base")
    #sel = (el_eb+elpt40).lstrip("& ")
    #hf = sf.SetHisto1DFast(var[0], sel, var[3], weight, hconf, lgconf , lconf, save_as)
    #hlist.append(hf)

for hf in hlist:
    hf.DrawSave()
    #sc = samples.get_stack_count(includeData=True)
    #nmc = sc["TOTAL"][0]
    #ndt = sc["Data"][0]
    #print "mccount, datacount, mc/dt: ", nmc, ndt, nmc/ ndt