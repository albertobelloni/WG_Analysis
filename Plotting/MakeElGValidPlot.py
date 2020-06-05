#!/usr/bin/env python
execfile("MakeBase.py")

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

varlistadditional=[
    #("el_dz[0]","el_dz","",(50,-0.02,0.02)),
    #("el_d0[0]","el_d0","",(50,-0.001,0.001)),
    #("jet_bTagCisvV2[0]","jet_bTagCisvV2[0]","",(50,0,1)),
    #("jet_bTagCisvV2[0]+jet_bTagCisvV2[1]","sum of bTagCiscV2 for 2 leading jets","",(50,0,2)),
    #("mu_pt_rc","mu_pt_rc","GeV",(100,0,100)),

    ("truemt_res","truemt_res","GeV",(100,0,1000)),
    ("m_lep_ph","m_lep_ph","GeV",(100,0,1000)),
    #("m_lep_ph_comb_sublLep","m_lep_ph_comb_sublLep","GeV",(100,0,1000)),
    #("m_lep_ph_comb_leadLep","m_lep_ph_comb_leadLep","GeV",(100,0,1000)),
    ("m_lep_met_ph","m_lep_met_ph","GeV",(100,0,1000)),
    #("m_mt_lep_met_ph","m_mt_lep_met_ph","GeV",(100,0,1000)),
    ("m_mt_lep_met_ph_forcewmass","m_mt_lep_met_ph_forcewmass","GeV",(100,0,1000)),
    ("mt_w","mt_w","GeV",(100,0,1000)),
    ("mt_res","mt_res","GeV",(100,0,1000)),
    ("mt_lep_ph","mt_lep_ph","GeV",(100,0,1000)),
    ("mt_lep_met","mt_lep_met","GeV",(100,0,1000)),
    ("m_lep_met","m_lep_met","GeV",(100,0,1000)),
    ("mt_lep_met_ph","mt_lep_met_ph","GeV",(100,0,1000)),
    ("recoM_lep_nu_ph","recoM_lep_nu_ph","GeV",(100,0,1000)),
    ("massdijet_m","massdijet_m","GeV",(100,0,1000)),
    ("leaddijet_m","leaddijet_m","GeV",(100,0,1000)),
    ("pt_lep_met","pt_lep_met","GeV",(100,0,1000)),
    ("recoW_pt","recoW_pt","GeV",(100,0,1000)),

    ("dphi_lep_met","dphi_lep_met","",(72,-pie,pie)),
    ("dphi_ph_w","dphi_ph_w","",(72,-pie,pie)),
    ("dphi_lep_ph","dphi_lep_ph","",(72,-pie,pie)),
    ("dphi_ph_w","dphi_ph_w","",(72,-pie,pie)),
    ("dr_lep_ph","dr_lep_ph","",(120,0,6)),
    #("dr_lep2_ph","dr_lep2_ph","",(120,0,6)),
    #("ph_min_el_dr[0]","ph_min_el_dr","",(100,-5,5)),
    ("truelepph_dr","truelepph_dr","",(120,0,6)),
    ("jet_CSVMedium_n","jet_CSVMedium_n",(5,0,5)),
    ("jet_CSVLoose_n","jet_CSVLoose_n",(5,0,5))
    ]
varlistadditional = []

varlist = [ ("met_pt","MET","GeV",(100,0,500)),
            ("m_lep_ph","m(e, #gamma)","GeV",(100,0,400)),
            ("mt_res","Resonance Mass m_{T}","GeV",(100,0,1000)),
            ("ph_pt[0]", "leading #gamma pT", "GeV", (80,0,400)),
            ("ph_phi[0]", "leading #gamma #phi", "", (72, -pie, pie)),
            ("ph_eta[0]", "leading #gamma #eta", "", (50,-3,3)),
            ("el_pt[0]", "leading electron pT", "GeV", (80,0,400)),
            ("el_phi[0]", "leading electron #phi", "", (72, -pie, pie)),
            ("el_eta[0]", "leading electron #eta", "", (50,-3,3)),
            ]

#no log
var2list = [ #("met_pt","MET","GeV",(100,0,200)),
             ("met_phi", "MET #phi", "", (72,-pie,pie)),
            ("el_phi[0]", "leading electron #phi", "", (72, -pie, pie)),
            ("el_eta[0]", "leading electron #eta", "", (50,-3,3)),
            ("ph_phi[0]", "leading #gamma #phi", "", (72, -pie, pie)),
            ("ph_eta[0]", "leading #gamma #eta", "", (50,-3,3)),
            ]


sellist, weight =  defs.makeselstringlist( ch = "el", phpt = 40, leppt = 35, met = 40 )
#sellist +=["mt_res>500"]
selfull = " && ".join(sellist) ## full signal selection

for var in varlistadditional:
    varname = str.translate(var[0],None,"[]_")
    sel = " && ".join([s for s in sellist if var[0] not in s ])
    save_as = ("%s_%ielg_ln_addtl.pdf" %(varname,year), options.outputDir, "base")
    hconf = { "xlabel":var[1],"xunit":var[2],"drawsignal":True, "logy":True,"ymin":.1}
    if "phi" in var[0] or "eta" in var[0] or "dr" in var[0]:
        hconf["ymax_scale"]=2.
    hf = sf.SetHisto1DFast(var[0], sel, var[3], weight, hconf, lgconf , lconf, save_as, data_exp = True)
    hlist.append(hf)

for var in varlist:
    varname = str.translate(var[0],None,"[]_")
    sel = " && ".join([s for s in sellist if var[0] not in s ])
    save_as = ("%s_%ielg_ln.pdf" %(varname,year), options.outputDir, "base")
    hconf = { "xlabel":var[1],"xunit":var[2],"drawsignal":False, "logy":True,"ymin":1}
    if "pt" in var[0]:
        hconf["drawsignal"]=True
    if "phi" in var[0] or "eta" in var[0]:
        hconf["ymax_scale"]=2.
    hf = sf.SetHisto1DFast(var[0], sel, var[3], weight, hconf, lgconf , lconf, save_as, data_exp = True)
    hlist.append(hf)
    #save_as = ("%s_%ielel_elselln.pdf" %(varname,year), options.outputDir, "base")
    #sel = (el_eb+elpt40).lstrip("& ")
    #hf = sf.SetHisto1DFast(var[0], sel, var[3], weight, hconf, lgconf , lconf, save_as)
    #hlist.append(hf)

for var in var2list:
    varname = str.translate(var[0],None,"[]_")
    sel = " && ".join([s for s in sellist if var[0] not in s ])
    save_as = ("%s_%ielg.pdf" %(varname,year), options.outputDir, "base")
    hconf = {"xlabel":var[1],"xunit":var[2],"drawsignal":False}
    if "phi" in var[0] or "eta" in var[0]:
        hconf["ymax_scale"]=2.
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

sel,w = defs.makeselstring()
samplelist =  ["WGamma", "AllTop", "Zgamma","TopW"]
hconf = {"weight":w,"doratio":1,"logy":1,"normalize":True,"bywidth":True,"rlabel":"ratio to W#gamma","xlabel":"m_{T}^{res}(e, #gamma, #slash{E}_{T})","ymin":1e-6,"reverseratio":1}
lconf = {"labelStyle":str(year),"extra_label":["%i Electron Channel" %year,"p_{T}^{e}>35GeV, MET>40GeV","Tight barrel #gamma p_{T}^{#gamma}>80GeV"], "extra_label_loc":(.27,.82)}
samples.CompareSelections("mt_res",[sel+"&&mt_res>200"]*len(samplelist),samplelist,mlist, hconf, lconf)
samples.SaveStack("mtres_mug%i_sigsel_bkgdcomp.pdf" %year,options.outputDir,"base")
