#!/usr/bin/env python
execfile("MakeBase.py")
###
### This script makes N-1/ final selection distribution plots
###


year = options.year
lconf = {"labelStyle":str(year),"extra_label":"%i Muon Channel" %year, "extra_label_loc":(.17,.82)}
lgconf = {'legendLoc':"Double","legendTranslateX":0.32, "legendCompress":.8, "fillalpha":.5, "legendWiden":.95}
hlist = []


sampManMuG.ReadSamples( _SAMPCONF )
samples = sampManMuG

selection = "mu_n==1 && ph_n==1"
sf = samples.SetFilter(selection)
hlist=[]

varlistsys=[
    ("prefweight",None,"",(40,0.8,1.2)),
    ("prefweightup/prefweight",None,"",(40,0.8,1.2)),
    ("prefweightdown/prefweight",None,"",(40,0.8,1.2)),
    ("PUWeight",None,"",             (40,0.9,1.2)),
    ("PUWeightUP5/PUWeight",None,"", (40,0.8,1.2)),
    ("PUWeightDN5/PUWeight",None,"", (40,0.8,1.2)),
    ("PUWeightUP5",None,"",          (40,0.8,1.2)),
    ("PUWeightDN5",None,"",          (40,0.8,1.2)),
    ("PUWeightUP10",None,"",         (40,0.8,1.2)),
    ("PUWeightDN10",None,"",         (40,0.8,1.2)),
    ("PDFWeights",    None, "", (50,0.8,1.2)),
    ("PDFWeights[0]", None, "", (50,0.8,1.2)),
    ("PDFWeights[1]", None, "", (50,0.8,1.2)),
    ("PDFWeights[2]", None, "", (50,0.8,1.2)),
    ("PDFWeights[3]", None, "", (50,0.8,1.2)),
    ("PDFWeights[4]", None, "", (50,0.8,1.2)),
    ("PDFWeights[5]", None, "", (50,0.8,1.2)),
#    ("EventWeights[1]/EventWeights[0]",None,"",(40,0.8,1.2)),
#    ("EventWeights[2]/EventWeights[0]",None,"",(40,0.8,1.2)),
#    ("EventWeights[3]/EventWeights[0]",None,"",(40,0.8,1.2)),
#    ("EventWeights[4]/EventWeights[0]",None,"",(40,0.8,1.2)),
#    ("EventWeights[6]/EventWeights[0]",None,"",(40,0.8,1.2)),
#    ("EventWeights[8]/EventWeights[0]",None,"",(40,0.8,1.2)),
    ("met_JetResUp_pt/met_pt",None,"",(100,0.8,1.2)),
    ("met_JetEnUp_pt/met_pt",None,"",(100,0.8,1.2)),
    ("met_MuonEnUp_pt/met_pt",None,"",(100,0.8,1.2)),
    ("met_ElectronEnUp_pt/met_pt",None,"",(100,0.8,1.2)),
    ("met_PhotonEnUp_pt/met_pt",None,"",(100,0.8,1.2)),
    ("met_UnclusteredEnUp_pt/met_pt",None,"",(100,0.8,1.2)),
    ("met_JetResDown_pt/met_pt",None,"",(100,0.8,1.2)),
    ("met_JetEnDown_pt/met_pt",None,"",(100,0.8,1.2)),
    ("met_MuonEnDown_pt/met_pt",None,"",(100,0.8,1.2)),
    ("met_ElectronEnDown_pt/met_pt",None,"",(100,0.8,1.2)),
    ("met_PhotonEnDown_pt/met_pt",None,"",(100,0.8,1.2)),
    ("met_UnclusteredEnDown_pt/met_pt",None,"",(100,0.8,1.2)),
    #("el_trigSF",None,"",(40,0.8,1.2)),
    #("el_trigSFUP",None,"",(40,0.8,1.2)),
    #("el_trigSFDN",None,"",(40,0.8,1.2)),
    #("el_idSF",None,"",(40,0.8,1.2)),
    #("el_idSFUP",None,"",(40,0.8,1.2)),
    #("el_idSFDN",None,"",(40,0.8,1.2)),
    #("el_recoSF",None,"",(40,0.8,1.2)),
    #("el_recoSFUP",None,"",(40,0.8,1.2)),
    #("el_recoSFDN",None,"",(40,0.8,1.2)),
    ("ph_idSF",None,"",(40,0.8,1.2)),
    ("ph_idSFUP",None,"",(40,0.8,1.2)),
    ("ph_idSFDN",None,"",(40,0.8,1.2)),
    ("ph_psvSF",None,"",(40,0.8,1.2)),
    ("ph_psvSFUP",None,"",(40,0.8,1.2)),
    ("ph_psvSFDN",None,"",(40,0.8,1.2)),
    ("ph_csevSF",None,"",(40,0.8,1.2)),
    ("ph_csevSFUP",None,"",(40,0.8,1.2)),
    ("ph_csevSFDN",None,"",(40,0.8,1.2)),
    ("mu_pt_rc","","GeV",(100,0,500)),
    ("mu_pt_rc_up/mu_pt_rc",None,"",(40,0.8,1.2)),
    ("mu_pt_rc_down/mu_pt_rc",None,"",(40,0.8,1.2)),
    ("mu_trigSF",None,"",(40,0.8,1.2)),
    ("mu_trigSFUP",None,"",(40,0.8,1.2)),
    ("mu_trigSFDN",None,"",(40,0.8,1.2)),
    ("mu_isoSF",None,"",(40,0.8,1.2)),
    ("mu_isoSFUP",None,"",(40,0.8,1.2)),
    ("mu_isoSFDN",None,"",(40,0.8,1.2)),
    ("mu_trkSF",None,"",(40,0.8,1.2)),
    ("mu_trkSFUP",None,"",(40,0.8,1.2)),
    ("mu_trkSFDN",None,"",(40,0.8,1.2)),
    ("mu_idSF",None,"",(40,0.8,1.2)),
    ("mu_idSFUP",None,"",(40,0.8,1.2)),
    ("mu_idSFDN",None,"",(40,0.8,1.2)),

    ("met_Type1SmearXY_pt/met_pt",None,"",(100,0,3)),
    ]


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
    ("jet_CSVMedium_n","jet_CSVMedium_n","",(5,0,5)),
    ("jet_CSVLoose_n","jet_CSVLoose_n","",(5,0,5))
    ]

varlist = [ ("met_pt","MET","GeV",(80,0,400)),
            ("m_lep_ph","m(#mu, #gamma)","GeV",(80,0,400)),
            ("mt_res","Resonance Mass m_{T}","GeV",(100,0,1000)),
            ("ph_pt[0]", "leading #gamma pT", "GeV", (80,0,400)),
            ("mu_pt[0]", "leading #mu pT", "GeV", (80,0,400)),
            ("ph_phi[0]", "leading #gamma #phi", "", (72, -pie, pie)),
            ("ph_eta[0]", "leading #gamma #eta", "", (50 ,-3, 3)),
            ("mu_phi[0]", "leading mu #phi", "", (72, -pie, pie)),
            ("mu_eta[0]", "leading #mu #eta",    "", (50,-3,3)),
            ]

#no log
var2list = [ ("met_pt","MET","GeV",(100,0,200)),
            ("mu_eta[0]", "leading #mu #eta",    "", (50,-3,3)),
            ("met_phi", "MET #phi", "", (72,-pie,pie)),
            ("mu_phi[0]", "leading mu #phi", "", (72, -pie, pie)),
            ("ph_phi[0]", "leading #gamma #phi", "", (72, -pie, pie)),
            ("ph_eta[0]", "leading #gamma #eta", "", (50, -3, 3)),
            ("mu_phi[1]", "subleading mu #phi", "", (72, -pie, pie)),
            ]


#sellist, weight =  defs.makeselstringlist( ch = "mu", phpt = 40, leppt = 35, met = 40 )
sellist, weight =  defs.makeselstringlist( ch = "mu", phpt = 100, leppt = 35, met = 80 )
selfull = " && ".join(sellist) ## full signal selection

for var in varlistsys:
    varname = str.translate(var[0],None,"[]_/")
    sel = " && ".join([s for s in sellist if var[0] not in s ])
    save_as = ("%s_%ielg_sys.pdf" %(varname,year), options.outputDir, "base")
    hconf = { "xlabel": var[0] if var[1] == None else var[1],"xunit":var[2],"drawsignal":True, "logy":True, "normalize":1}
    #if "phi" in var[0] or "eta" in var[0] or "dr" in var[0]:
    #    hconf["ymax_scale"]=2.
    hf = sf.SetHisto1DFast(var[0], sel, var[3], weight, hconf, lgconf , lconf, save_as, data_exp = True)
    hlist.append(hf)

for var in varlistadditional:
    ## for additional plots. always draw signal distributions
    varname = str.translate(var[0],None,"[]_")
    sel = " && ".join([s for s in sellist if var[0] not in s ])
    save_as = ("%s_%imug_ln_addtl.pdf" %(varname,year), options.outputDir, "base")
    hconf = { "xlabel":var[1],"xunit":var[2],"drawsignal":True, "logy":True,"ymin":.1}
    if "phi" in var[0] or "eta" in var[0] or "dr" in var[0]:
        hconf["ymax_scale"]=2.
    hf = sf.SetHisto1DFast(var[0], sel, var[3], weight, hconf, lgconf , lconf, save_as, data_exp = True)
    hlist.append(hf)

for var in varlist:
    varname = str.translate(var[0],None,"[]_")
    sel = " && ".join([s for s in sellist if var[0] not in s ])
    save_as = ("%s_%imug_ln.pdf" %(varname,year), options.outputDir, "base")
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
    save_as = ("%s_%imug.pdf" %(varname,year), options.outputDir, "base")
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

