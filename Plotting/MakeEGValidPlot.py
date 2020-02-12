#!/usr/bin/env python
execfile("MakeBase.py")
sampManElG.ReadSamples( _SAMPCONF )
#sampManElEl.ReadSamples( _SAMPCONF )
#sampManMuG.ReadSamples( _SAMPCONF )


hlist = []
year = options.year
samples = sampManElG

ROOT.ROOT.EnableImplicitMT()

lconf = {"labelStyle":str(year),"extra_label":"%i Electron Channel" %year, "extra_label_loc":(.17,.82)}
hconf = {"unblind":True,"doratio":True,"xlabel":"flattened #phi (>6.28 for +ve #eta)","xunit":"","drawsignal":False}
#"el_n==1&&ph_n==1&&mu_n==0&& ph_IsEB[0] && abs(el_eta[0])<2.1 && met_pt<40 && ph_hasPixSeed[0]==0 && abs(m_lep_ph-91)<15
#&& ph_passMedium[0]&&ph_pt[0]>30&&el_pt[0]>40"
selection = baseel+ph_eb+el_eb+metlt40+massZ+phptgt%30+elpt40 + "&& ph_passMedium[0]"
print "1st sel"
sf = samples.SetDefine("sel1",selection).SetFilter("sel1")

save_as = ("flatphphi_%ielg_passpix.pdf" %year, options.outputDir, "base")
print "2nd sel"
hf = sf.SetHisto1DFast(flatphi,  passpix.lstrip(" &"), (72,0,pi*4), weight, hconf, {} , lconf, save_as)
hlist.append(hf)

#samples.SetDefine("selection", selection).SetFilter("selection").SetHisto1D(72, 0, pi*4, flatphi)

#samples.Draw(, "el_n==1&&ph_n==1&&mu_n==0&& ph_IsEB[0] && abs(el_eta[0])<2.1 && met_pt<40 && ph_hasPixSeed[0]==1 && abs(m_lep_ph-91)<15 && ph_passMedium[0]&&ph_pt[0]>30&&el_pt[0]>40",(72,0,3.1416*4),{"unblind":True,"doratio":True,"xlabel":"flattened #phi (>6.28 for +ve #eta)","xunit":"","drawsignal":False, "weight":"NLOWeight*PUWeight"},{} , lconf)
save_as = ("flatphphi_%ielg_failpix.pdf" %year, options.outputDir, "base")
print "3rd sel"
hf = sf.SetHisto1DFast(flatphi,  failpix.lstrip(" &"), (72,0,pi*4), weight, hconf, {} , lconf, save_as)
hlist.append(hf)


for hf in hlist:
    hf.DrawSave()
    sc = samples.get_stack_count(includeData=True)
    nmc = sc["TOTAL"][0]
    ndt = sc["Data"][0]
    print "mccount, datacount, mc/dt: ", nmc, ndt, nmc/ ndt


#get_ipython().magic(u'run interactiveStackTree.py --baseDir  /data2/users/kakw/Resonances2018/LepLep_elel_2020_01_30/ --samplesConf Modules/Resonance2018.py --xsFile cross_sections/photon18.py --lumi 59740. --treeName UMDNTuple/EventTree --fileName tree.root')


lconf = {"labelStyle":"2018","extra_label":"2018 Electron Channel", "extra_label_loc":(.17,.82)}
#
#samples.Draw("met_pt","el_n==2 && abs(el_eta[0])<2.1 && el_pt[0]>35",(100,0,200),{"unblind":True,"logy":True,"doratio":True,"xlabel":"MET","xunit":"","drawsignal":False, "weight":"NLOWeight*PUWeight","ymin":10},{} , lconf)
#samples.SaveStack("met_2016elel.pdf","~/public_html","base")
#
#samples.Draw("m_ll", "el_n==2 && abs(el_eta[0])<2.1 && el_pt[0]>35",(100,50,250),{"unblind":True,"logy":True,"doratio":True,"xlabel":"m(e,e)","xunit":"","drawsignal":False, "weight":"NLOWeight*PUWeight","ymin":10},{} , lconf)
#samples.SaveStack("mll_2018elel.pdf","~/public_html","base")
