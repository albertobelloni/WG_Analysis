#!/usr/bin/env python3
exec(compile(open("MakeBase.py", "rb").read(), "MakeBase.py", 'exec'))


year = options.year
lconf = {"labelStyle":str(year),"extra_label":"%i Muon Channel" %year, "extra_label_loc":(.17,.82)}
lgconf = {'legendLoc':"Double","legendTranslateX":0.35, "legendCompress":.9, "fillalpha":.5}
hlist = []


sampManMuMu.ReadSamples( _SAMPCONF )
samples = sampManMuMu

selection = "mu_n==2"
sf = samples.SetFilter(selection)
hlist=[]

varlist = [ ("met_pt","MET","GeV",(100,0,250)),
            ("m_ll","m(#mu, #mu)","GeV",(100,50,250)),
            ("mt_res","reco mT","GeV",(100,0,200)),
            ("ph_pt", "#gamma pT", "GeV", (100,0,200)),
            ("mu_pt[0]", "leading #mu pT", "GeV", (100,0,300)),
            ("mu_pt[1]", "subleading #mu pT", "GeV", (100,0,300)),
            ("mu_eta[0]", "leading #mu #eta",    "", (50,-3,3)),
            ("mu_eta[1]", "subleading #mu #eta", "", (50,-3,3)),
            ]

#no log
var2list = [ ("met_pt","MET","GeV",(100,0,100)),
            ("met_phi", "MET #phi", "", (72,-pie,pie)),
            ("mu_phi[0]", "leading mu #phi", "", (72, -pie, pie)),
            ("mu_phi[1]", "subleading mu #phi", "", (72, -pie, pie)),
            ]

for var in varlist:
    varname = str.translate(var[0],None,"[]_")
    save_as = ("%s_%imumu_ln.pdf" %(varname,year), options.outputDir, "base")
    hconf = {"unblind":True, "doratio":True,"xlabel":var[1],"xunit":var[2],"drawsignal":False, "logy":True,"ymin":10, "overflow":False}
    hf = sf.SetHisto1DFast(var[0], "", var[3], weight, hconf, lgconf , lconf, save_as)
    hlist.append(hf)
    #save_as = ("%s_%ielel_elselln.pdf" %(varname,year), options.outputDir, "base")
    #sel = (el_eb+elpt40).lstrip("& ")
    #hf = sf.SetHisto1DFast(var[0], sel, var[3], weight, hconf, lgconf , lconf, save_as)
    #hlist.append(hf)

for var in var2list:
    varname = str.translate(var[0],None,"[]_")
    save_as = ("%s_%imumu.pdf" %(varname,year), options.outputDir, "base")
    hconf = {"unblind":True, "doratio":True,"xlabel":var[1],"xunit":var[2],"drawsignal":False, "overflow":False}
    hf = sf.SetHisto1DFast(var[0], "", var[3], weight, hconf, lgconf , lconf, save_as)
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
