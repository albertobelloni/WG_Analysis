#!/usr/bin/env python

execfile("MakeBase.py")

def main() :
    #if options.outputDir: f1 = ROOT.TFile("%s/output.root"%(options.outputDir),"RECREATE")

    sampManElG, sampManMuG = None, None
    sampManMuG= SampleManager( options.baseDirMuG, _TREENAME, filename=_FILENAME, xsFile=_XSFILE, lumi=_LUMI*lumiratio, readHists=False , weightHistName = "weighthist")
    sampManMuG.ReadSamples( _SAMPCONF )
    sampManElG= SampleManager( options.baseDirElG, _TREENAME, filename=_FILENAME, xsFile=_XSFILE, lumi=_LUMI*lumiratio ,readHists=False , weightHistName = "weighthist")
    sampManElG.ReadSamples( _SAMPCONF )
    plotvarsbase = [ ("mt_lep_met_ph",(100,0,2000)),
                 ("p_{T}(#gamma)","ph_pt[0]"     ,(100,50,550)),
                 ("#eta(#gamma)","ph_eta[0]"    ,(100,-3,3)),
                 ("#phi(#gamma)","ph_phi[0]"    ,(100,-pi,pi)),
                 ("MET"         ,"met_pt"       ,(100,0,500)),
                 ("MET #phi"    ,"met_phi"      ,(100,-pi,pi)),
                ]
    plotvarsel=[ ("p_{T}(e)"    ,"el_pt[0]"     ,(100,0,500)),
                 ("#eta(e)"     ,"el_eta[0]"    ,(100,-3,3)),
                 ("#phi(e)"     ,"el_phi[0]"    ,(100,-pi,pi)),
                 ]
    plotvarsmu=[ ("p_{T}(#mu)"  ,"mu_pt[0]"     ,(100,0,500)),
                 ("#eta(#mu)"   ,"mu_eta[0]"    ,(100,-3,3)),
                 ("#phi(#mu)"   ,"mu_phi[0]"    ,(100,-pi,pi)),
                 ]

    for ch, samples in zip(["mu","el"],[sampManMuG,sampManElG]):
        labelname = "%i Muon Channel" %options.year if ch == "mu" else "%i Electron Channel" %options.year
        lepname = "e" if ch == "el" else "#mu"
        #labelname+=" scaled to 2016 luminosity"
        #if ch == "el": selection = baseel + ph_eb + metgt40 + invZ + passpix + phpt80 + "&&el_passTight[0] && ph_passTight[0]" + elpt40 + el_eb
        ##if ch == "mu": selection = basemu + ph_eb + metgt40  + passpix + phpt80 + "&& mu_passTight[0] && ph_passTight[0]"
        #selection , weight = defs.makeselstring(ch, 210, 35, 160)
        selection , weight = defs.makeselstring(ch,  80, 35,  40)


        ## prepare config
        hist_config   = {"xlabel":"m_{T}(%s,#gamma,p^{miss}_{T})" %(lepname),"logy":1,"ymin":.05,"weight":weight, "ymax_scale":1.5} ## "unblind":False
        label_config  = {"extra_label":labelname, "extra_label_loc":(.17,.82), "labelStyle":str(options.year)}
        legend_config = {'legendLoc':"Double","legendTranslateX":0.3, "legendCompress":1, "fillalpha":.5, "legendWiden":.9}

        ### MT_LEP_MET_PH
        samples.Draw("mt_res", selection, (50,0,2000), hist_config,legend_config,label_config)

        ## save histogram
        samples.SaveStack("moneymtres_cut2_%i%s.pdf" %(options.year, ch), options.outputDir, "base")
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



