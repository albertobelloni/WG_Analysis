#!/usr/bin/env python

execfile("MakeBase.py")

def main() :
    #if options.outputDir: f1 = ROOT.TFile("%s/output.root"%(options.outputDir),"RECREATE")

    sampManElG, sampManMuG = None, None
    sampManMuG= SampleManager( options.baseDirMuG, _TREENAME, filename=_FILENAME, xsFile=_XSFILE, lumi=_LUMI*lumiratio, readHists=False , weightHistName = "weighthist")
    sampManMuG.ReadSamples( _SAMPCONF )
    sampManElG= SampleManager( options.baseDirElG, _TREENAME, filename=_FILENAME, xsFile=_XSFILE, lumi=_LUMI*lumiratio ,readHists=False , weightHistName = "weighthist")
    sampManElG.ReadSamples( _SAMPCONF )
    #samples = sampManMuG
    plotvarsbase = [# ("mt_lep_met_ph",(100,0,2000)),
                 ("p_{T}(#gamma)","ph_pt[0]"     ,(100,50,550)),
                 #("#eta(#gamma)","ph_eta[0]"    ,(100,-3,3)),
                 #("#phi(#gamma)","ph_phi[0]"    ,(100,-pi,pi)),
                 #("MET"         ,"met_pt"       ,(100,0,500)),
                 #("MET #phi"    ,"met_phi"      ,(100,-pi,pi)),
                ]
    plotvarsel=[ #("p_{T}(e)"    ,"el_pt[0]"     ,(100,0,500)),
                 #("#eta(e)"     ,"el_eta[0]"    ,(100,-3,3)),
                 #("#phi(e)"     ,"el_phi[0]"    ,(100,-pi,pi)),
                 ]
    plotvarsmu=[ #("p_{T}(#mu)"  ,"mu_pt[0]"     ,(100,0,500)),
                 #("#eta(#mu)"   ,"mu_eta[0]"    ,(100,-3,3)),
                 #("#phi(#mu)"   ,"mu_phi[0]"    ,(100,-pi,pi)),
                 ]

    for ch, samples in zip(["mu","el"],[sampManMuG,sampManElG]):
    #for ch, samples in [("el",sampManElG),]:
    #for ch, samples in [("mu",sampManMuG),]:
        labelname = "%i Muon Channel" %options.year if ch == "mu" else "%i Electron Channel" %options.year
        #labelname+=" scaled to 2016 luminosity"
        #if ch == "el": selection = baseel + ph_eb + metgt40 + invZ + passpix + phpt80 + "&&el_passTight[0] && ph_passTight[0]" + elpt40 + el_eb
        ##if ch == "mu": selection = basemu + ph_eb + metgt40  + passpix + phpt80 + "&& mu_passTight[0] && ph_passTight[0]"
        selection = defs.makeselstring(ch, 80, 35, 40)


        ## prepare config
        hist_config   = {"xlabel":"m_{T}(e,#gamma,p^{miss}_{T})","logy":1,"ymin":.1,"weight":weight, "ymax_scale":1.5} ## "unblind":False
        label_config  = {"extra_label":labelname, "extra_label_loc":(.17,.82), "labelStyle":str(options.year)}
        legend_config = {'legendLoc':"Double","legendTranslateX":0.35, "legendCompress":.9, "fillalpha":.5}

        ### MT_LEP_MET_PH
        samples.Draw("mt_res", selection, (50,0,2000), hist_config,legend_config,label_config)

        ## save histogram
        samples.SaveStack("moneymtres%i%s.pdf" %(options.year, ch), options.outputDir, "base")
        samples.print_stack_count()
        samples.print_stack_count(doacceptance=True)
        samples.print_stack_count(dolatex=True)
        samples.print_stack_count(dolatex=True,doacceptance=True)

        if ch == "el":
            plotvars = plotvarsbase+plotvarsel
        if ch == "mu":
            plotvars = plotvarsbase+plotvarsmu
        for xlabel, var, vrange in plotvars:
            hist_config["xlabel"] = xlabel
            samples.Draw(var, selection,vrange , hist_config,legend_config,label_config)
            ## save histogram
            varname = var.replace("[","").replace("]","")
            samples.SaveStack("%sSIGSEL%i%s.pdf" %(varname,options.year, ch), options.outputDir, "base")
    return sampManMuG, sampManElG


#        ### MT_RES
#        hist_config    ={"xlabel":"Resonance Mass","logy":1,"ymin":.1,"weight":weight} ## "unblind":False
#        samples.Draw("mt_res", selection, (100,0,2000), hist_config,legend_config, label_config)
#
#        ## save histogram
#        samples.SaveStack("moneymtres%i%s.pdf" %(options.year, ch), options.outputDir, "base")
#        samples.print_stack_count()
#        samples.print_stack_count(acceptance=True)
#        samples.print_stack_count(dolatex=True)
#        samples.print_stack_count(dolatex=True,acceptance=True)


#    selbase_mu = 'mu_pt30_n==1 && mu_n==1'
#    ## with bad tracker portions excluded
#    selbase_el_excludephi = 'ph_n>=1 && el_n==1 &&!( ph_eta[0]<0&&ph_phi[0]>2.3&&ph_phi[0]<2.7)&&!(ph_phi[0]>1.2&&ph_phi[0]<1.5) '
#    selbase_el = 'ph_n>=1 && el_n==1'
#
#
#    ## general event selections
#    nocut = ("","")
#    ltmet25 = 'met_pt<25'
#    gtmet25 = 'met_pt>25'
#    cut_met = [nocut, (ltmet25,"ltmet25"), (gtmet25,"gtmet25")]
#
#    phpt50 = "ph_pt[0]>50"
#    phpt100 = "ph_pt[0]>100"
#    cut_phpt = [nocut, (phpt50,"phpt50"), (phpt100,"phpt100")]
#
#    ## 1 and only 1 photon with pt greater than 50, 100 GeV
#    phpt30neq1 = "ph_pt[0]>%.2g && (ph_n==1 || ph_pt[1]<%.2g)" %(30,30)
#    phpt50neq1 = "ph_pt[0]>%.2g && (ph_n==1 || ph_pt[1]<%.2g)" %(50,50)
#    phpt100neq1 = "ph_pt[0]>%.2g && (ph_n==1 || ph_pt[1]<%.2g)" %(100,100)
#    cut_phptneq1 = [nocut, (phpt30neq1,"phpt30neq1"),(phpt50neq1,"phpt50neq1"), (phpt100neq1,"phpt100neq1")]
#
#    invZ = 'abs(m_lep_ph-91)>15' ## inverse Z resonance cut
#    inZ  = 'abs(m_lep_ph-91)<15' ## Z resonance cut
#    gtZ = '(m_lep_ph-91)>15'     ## greater than Z mass
#    ltZ = '(91-m_lep_ph)>15'     ## less than Z mass
#    cut_z = [nocut, (inZ, "inz"), (invZ, "invz"),(gtZ,"gtZ"), (ltZ,"ltZ")]
#
#    ### electron selections
#    selbase_el_EB = selbase_el + ' && ph_IsEB[0]' #leading photon in barrel
#
#    passpix = 'ph_hasPixSeed[0]==0'  #Pixel seed
#    failpix = 'ph_hasPixSeed[0]==1'
#    cut_pix = [nocut, (passpix,"ppix"), (failpix,"fpix")]
#
#    passcsev = 'ph_passEleVeto[0]==1' #CSEV: Conversion safe electron veto
#    failcsev = 'ph_passEleVeto[0]==0'
#    cut_csev = [nocut, (passcsev,"pcsev"), (failcsev,"fcsev")]
#
#    selarray = [[(selbase_el_EB,"basephEB"),], cut_pix, cut_met, cut_phpt ]
#
#    ### edit here for plot variables i.e. what is on the x axis
#    vararray = [ #("el_n",        (10,0,10),      "num of electrons"), ## variable name, x axis range, x axis label
#                ("el_pt[0]",    (50,0,200),     "p_{T}(e, leading)"),
#     #           ("ph_n",        (10,0,10),      "num of photons"),
#     #           ("ph_pt[0]",    (50,0,200),     "p_{T}(#gamma, leading)"),
#     #           ("met_pt",      (50,0,400),     "MET"),
#     #           ("met_phi",    (20,-pi,pi),    "MET #phi"),
#                ]
#
#
##    legend_config = {'legendLoc':"Double","legendTranslateX":0.3}
#    hist_config = {"logy":1,"blind":True, "weight": "NLOWeight"}
#    makeplots(sampManElG,vararray, selarray, hist_config,{}, "log")
#
#    #legend_config = {'legendLoc':"Double","legendTranslateX":0.3}
#    #hist_config = {"blind":True, "weight": "PUWeight*NLOWeight"}
#    #makeplots(vararray, selarray, hist_config, legend_config)
#    if options.outputDir:
#        ## write and close root file
#        f1.Write()
#        f1.Close()





def makeplots(samples,vararray, selprearray=None, hist_config=None, legend_config=None, extratag = "", dirname = "temp"):
    #print selprearray
    chlist ="[]{}()"
    if selprearray is None or not isinstance(selprearray,(tuple,list)):
        return
    else:
        selarray = product(*selprearray)

    #print selarray
    for sel in selarray:
        selection, name = makeselection(sel)
        for var in vararray:
            savename = var[0]+"_SEL_"+name+"_"+extratag+".pdf"
            for ch in chlist:
                savename = savename.replace(ch,"")
            hist_config["xlabel"] = var[2]
            print var[0], selection, savename
            samples.Draw(var[0], selection, var[1], hist_config, legend_config)
            samples.print_stack_count()
            samples.SaveStack(savename, dirname, 'base')

def makeselection(sel):
    #print sel
    sel, name  = zip(*sel)
    sel = [s for s in sel if s != ""]
    name = [n for n in name if n != ""]
    sel  = "&&".join(sel)
    name  = "_".join(name)
    return sel, name




def doratio(h1,h2):
    hratio = h1.Clone("hratio")
    hratio.Divide(h2)
    hratio.SetMarkerStyle(20)
    hratio.SetMarkerSize(1.1)
    hratio.SetStats(0)
    hratio.SetTitle("")
    hratio.GetYaxis().SetTitle("ratio")
    hratio.SetLineColor(ROOT.kBlack)
    hratio.SetLineWidth(2)
    hratio.GetYaxis().SetTitleSize(0.10)
    hratio.GetYaxis().SetTitleOffset(0.6)
    hratio.GetYaxis().SetLabelSize(0.10)
    hratio.GetXaxis().SetLabelSize(0.10)
    hratio.GetXaxis().SetTitleSize(0.10)
    hratio.GetXaxis().SetTitleOffset(1.0)
    hratio.GetYaxis().SetRangeUser(0.5,1.5)
    #hratio.GetYaxis().UnZoom()
    hratio.GetYaxis().CenterTitle()
    hratio.GetYaxis().SetNdivisions(506, True)
    return hratio

def cmsinternal(pad):
    pad.cd()
    tex = ROOT.TLatex(0.18,0.93,"CMS Internal")
    tex.SetNDC()
    tex.SetTextSize(0.05)
    tex.SetLineWidth(2)
    tex.Draw()
    return tex

def ratioline(hratio):
    left_edge  = hratio.GetXaxis().GetXmin()
    right_edge = hratio.GetXaxis().GetXmax()

    oneline = ROOT.TLine(left_edge, 1, right_edge, 1)
    oneline.SetLineStyle(3)
    oneline.SetLineWidth(2)
    oneline.SetLineColor(ROOT.kBlack)
    oneline.Draw()
    return oneline

def hformat(h1,color):
    h1.SetLineColor(color)
    h1.SetMarkerColor(color)
    #h1.SetMarkerStyle(20)
    h1.SetMarkerSize(1.1)
    h1.SetStats(0)
    h1.SetLineWidth(2)
    h1.GetYaxis().SetTitleSize(0.05)
    h1.GetYaxis().SetTitleOffset(1.15)
    h1.GetYaxis().SetLabelSize(0.05)
    h1.GetXaxis().SetLabelSize(0.05)
    h1.GetXaxis().SetTitleSize(0.05)
    h1.GetXaxis().SetTitleOffset(0.8)


sampmu,sampel = main()



