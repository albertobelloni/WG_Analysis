#!/usr/bin/env python
execfile("MakeBase.py")
year = options.year
hlist = []
sampManElG.ReadSamples( _SAMPCONF )
sampManMuG.ReadSamples( _SAMPCONF )
samples = sampManElG
ROOT.gStyle.SetPalette(ROOT.kViridis)


def transferrate2dplotmaker(samples,var,sel,sampname,hbin,savename, weight="NLOWeight",plotopt="COLZ"):
    ## make 2D histograms
    samples.Draw2D(var,["(%s)*%s" %(sel+passpix, weight)],[sampname],hbin,"COLZ",logz=False)
    samples.SaveStack("pixpass2D_"+savename, options.outputDir, "base0")
    hratio=samples[-1].hist.Clone()
    samples.Draw2D(var,["(%s)*%s" %(sel+failpix, weight)],[sampname],hbin,"COLZ",logz=False)
    samples.SaveStack("pixfail2D_"+savename, options.outputDir, "base0")
    hfail=samples[-1].hist.Clone()

    # now divide pass by fail
    hratio.Divide(hfail)
    #samples.curr_canvases["base0"].SetLogz(0)
    hratio.GetZaxis().SetRangeUser(0,3)
    hratio.Draw(plotopt)
    samples.SaveStack("trf2D_"+savename, options.outputDir, "base0")
    return hratio

def metbias2dplotmaker(samples,var,sel,sampname,hbin,weight="NLOWeight",plotopt="COLZ"):
    ## make 2D histograms
    samples.Draw2D(var,["(%s)*%s" %(sel+ metgt%40+ passpix, weight)],[sampname],hbin,"COLZ",logz=False)
    hregs=samples[-1].hist.Clone()
    samples.Draw2D(var,["(%s)*%s" %(sel+ metlt%40+ passpix, weight)],[sampname],hbin,"COLZ",logz=False)
    hrega=samples[-1].hist.Clone()
    samples.Draw2D(var,["(%s)*%s" %(sel+ metgt%40+ failpix, weight)],[sampname],hbin,"COLZ",logz=False)
    hregd=samples[-1].hist.Clone()
    samples.Draw2D(var,["(%s)*%s" %(sel+ metlt%40+ failpix, weight)],[sampname],hbin,"COLZ",logz=False)
    hregb=samples[-1].hist.Clone()

    # now divide pass by fail
    ## this is the ratio of SR over-estimation to actual SR count
    hratio=hrega
    hratio.Multiply(hregd)
    hratio.Divide(hregb)
    hratio.Divide(hregs)
    hratio.Draw(plotopt)
    hratio.GetZaxis().SetRangeUser(.8,2)
    return hratio


lconf = {"labelStyle":str(year),"extra_label":"%i Electron Channel" %year, "extra_label_loc":(.17,.82)}
#lgconf = {'legendLoc':"Double","legendTranslateX":0.35, "legendCompress":.9, "fillalpha":.5}
lgconf={"legendWiden":1.5,"fillapha":.5}
hconf = {"colors":[2,4,6],"logy":True,"doratio":True,"rlabel":"ratio to inclusive","reverseratio":True, "xlabel ":"gen photon p_{T}", "weight":weight}


sel="ph_n==1 && el_n==1 && ph_passMedium[0] &&ph_IsEB[0] && met_pt<40 && abs(m_lep_ph-91)<15"
sel1="ph_n==1 && el_n==1 && ph_passMedium[0] &&ph_IsEB[0] && abs(m_lep_ph-91)<15"


# bad eta phi
worststr = defs.build_bad_efake_sector_string(options.year, "worst")
badstr = defs.build_bad_efake_sector_string(options.year, "bad")

for stag, samplename in [("zjet","Z+jets"), ("data","Data")]:
    ### photon pT vs phi
    hbin = (list(np.linspace(-3.1416,3.1416,73)),[20,25,30,35,40,45,50,60,80,85])
    hrate = transferrate2dplotmaker(samples, "ph_pt[0]:ph_phi[0]", sel,
                                    samplename, hbin, "ptVSphi_%ielg_%s_colz.pdf"%(year,stag))
    hrate.Draw("SURF2")
    samples.SaveStack("trf2D_ptVSphi_%ielg_%s_surf2.pdf" %(year,stag), options.outputDir, "base0")
    # met bias (A*D/B/S = est/S)
    hrate = metbias2dplotmaker(samples, "ph_pt[0]:ph_phi[0]", sel1, samplename, hbin,plotopt = "CONT4")
    samples.SaveStack("metbias2D_ptVSphi_%ielg_%s_cont4.pdf" %(year,stag), options.outputDir, "base0")

    ### photon eta vs phi
    hbin = (144,-36,36,20,-2,2)
    hrate = transferrate2dplotmaker(samples, "ph_eta[0]:ph_phi[0]/3.1415927*36", sel,
                                    samplename, hbin, "etaVSphi_%ielg_%s_colz.pdf"%(year,stag))
    hrate.Draw("SURF2")
    samples.SaveStack("trf2D_etaVSphi_%ielg_%s_surf2.pdf" %(year,stag), options.outputDir, "base0")

    ### photon eta vs phi (worst mask)
    hrate = transferrate2dplotmaker(samples, "ph_eta[0]:ph_phi[0]/3.1415927*36", "%s && !(%s)" %(sel, worststr),
                                    samplename, hbin, "etaVSphi_worst_%ielg_%s_colz.pdf"%(year,stag))
    hrate.Draw("SURF2")
    samples.SaveStack("trf2D_etaVSphi_worst_%ielg_%s_surf2.pdf" %(year,stag), options.outputDir, "base0")

    ### photon eta vs phi (bad mask)
    hrate = transferrate2dplotmaker(samples, "ph_eta[0]:ph_phi[0]/3.1415927*36", "%s && !(%s)" %(sel, badstr),
                                    samplename, hbin, "etaVSphi_bad_%ielg_%s_colz.pdf"%(year,stag))
    hrate.Draw("SURF2")
    samples.SaveStack("trf2D_etaVSphi_bad_%ielg_%s_surf2.pdf" %(year,stag), options.outputDir, "base0")

    ### photon eta vs pT
    hbin = ([20,25,30,35,40,45,50,60,80,85],list(np.linspace(-2,2,21)))
    hrate = transferrate2dplotmaker(samples, "ph_eta[0]:ph_pt[0]", sel, samplename, hbin, "ptVSeta_%ielg_%s_colz.pdf"%(year,stag))
    hrate.Draw("SURF2")
    samples.SaveStack("trf2D_ptVSeta_%ielg_%s_surf2.pdf" %(year,stag), options.outputDir, "base0")

    ### photon eta vs pT (bad mask)
    hrate = transferrate2dplotmaker(samples, "ph_eta[0]:ph_pt[0]", "%s && !(%s)" %(sel,badstr),
                                    samplename, hbin, "ptVSeta_bad_%ielg_%s_colz.pdf"%(year,stag))
    hrate.Draw("SURF2")
    samples.SaveStack("trf2D_ptVSeta_bad_%ielg_%s_surf2.pdf" %(year,stag), options.outputDir, "base0")

    ### photon eta vs pT (bad mask)
    hrate = transferrate2dplotmaker(samples, "ph_eta[0]:ph_pt[0]", "%s && (%s)" %(sel,badstr),
                                    samplename, hbin, "ptVSeta_badtag_%ielg_%s_colz.pdf"%(year,stag))
    hrate.Draw("SURF2")
    samples.SaveStack("trf2D_ptVSeta_badtag_%ielg_%s_surf2.pdf" %(year,stag), options.outputDir, "base0")

    # met bias (A*D/B/S = est/S)
    hrate = metbias2dplotmaker(samples, "ph_eta[0]:ph_pt[0]", sel1, samplename, hbin, plotopt = "CONT4")
    samples.SaveStack("metbias2D_ptVSeta_%ielg_%s_cont4.pdf" %(year,stag), options.outputDir, "base0")

lconf = {"labelStyle":str(year),"extra_label":"%i Muon Channel" %year, "extra_label_loc":(.17,.82)}
lgconf={#"legendWiden":1.5,
        "fillapha":.5}
sampManMuG.Draw("ph_phi[0]+(1+2*(ph_eta[0]>0)+4*ph_hasPixSeed[0])*3.1416", "mu_n==1 && el_n==0 && ph_n==1 && jet_CSVMedium_n>0 && ph_pt[0]>50 && ph_IsEB[0] && ph_passVIDMedium[0]", (144,0,3.1416*8), {"drawsignal":False, "unblind":True, "weight":"NLOWeight","xunit":"","xlabel":"flatten photon phi, pixVeto"},lgconf,lconf)
sampManMuG.SaveStack("phphipixveto_csvmed_%imug.pdf" %year, options.outputDir, "base")
