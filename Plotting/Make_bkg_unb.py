#!/usr/bin/env python3

exec(compile(open("MakeBase.py", "rb").read(), "MakeBase.py", 'exec'))

def main() :
    sampManElG, sampManMuG = None, None
    sampManMuG= SampleManager( options.baseDirMuG, _TREENAME, filename=_FILENAME, xsFile=_XSFILE, lumi=_LUMI*lumiratio, readHists=False , weightHistName = "weighthist")
    sampManMuG.ReadSamples( _SAMPCONF )
    sampManElG= SampleManager( options.baseDirElG, _TREENAME, filename=_FILENAME, xsFile=_XSFILE, lumi=_LUMI*lumiratio ,readHists=False , weightHistName = "weighthist")
    sampManElG.ReadSamples( _SAMPCONF )

    plotvarsbase = [ 
                 ("m_{T}^{l#nu#gamma}","mt_res", 'GeV',(50,0,2500)),
                 #("p_{T}(#gamma)","ph_pt[0]"    , 'GeV' ,(20,50,800)),
                 #("#eta(#gamma)","ph_eta[0]"    , '' ,(20,-2,2)),
                 #("#phi(#gamma)","ph_phi[0]"    , '' ,(20,-3.14,3.14)),
                 #("MET"         ,"met_pt"     , 'GeV'  ,(20,0,500)),
                 #("#phi(MET)"         ,"met_phi"    , ''   ,(20,-3.14,3.14)),
                ]
    plotvarsel=[ 
                 ("p_{T}(e)","el_pt[0]"  , 'GeV'   ,(20,0,800)),
                 ("#eta(e)","el_eta[0]"  , '', (20,-3,3)),
                 ("#phi(e)","el_phi[0]"  , ''   ,(20,-3.14,3.14)),
               ]
    plotvarsmu=[ 
                 ("p_{T}(#mu)","mu_pt[0]"   ,'GeV'  ,(20,0,800)),
                 ("#eta(#mu)","mu_eta[0]"   , ''  ,(20,-3,3)),
                 ("#phi(#mu)","mu_phi[0]"  , ''   ,(20,-3.14,3.14)),
               ]
    plotvarsel=[]
    plotvarsmu=[]
    plotvarsbase=[]
    plotvarsel=[("m_{T}^{l#nu#gamma}","mt_res", 'GeV',[0, 150, 200, 250, 300, 350, 400, 500, 750, 1000, 2500]),]
    plotvarsmu=[("m_{T}^{l#nu#gamma}","mt_res", 'GeV',[0, 150, 200, 250, 300, 350, 400, 500, 750, 1000, 2500]),]
    #for ch, samples in zip(["mu","el"],[sampManMuG,sampManElG]):
    #for ch, samples in zip(["el","mu"],[sampManElG,sampManMuG]):
    for ch, samples in zip(["el"],[sampManElG]):
        labelname = "%i Muon Channel" %options.year if ch == "mu" else "%i Electron Channel" %options.year
        lepname = "e" if ch == "el" else "#mu"
        #labelname+=" scaled to 2016 luminosity"
        if ch == "el":
            selection , weight = defs.makeselstring(ch,  80, 35,  40)
        else:
            selection , weight = defs.makeselstring(ch,  80, 30,  40)
        if options.year == 2018:
            weight = weight.replace("prefweight","1")
        print(ch, samples)
        weight =weight.replace("PUWeight","PUWeight*0.2")
        print(selection ,weight)
        ## prepare config
        #hist_config   = {"xlabel":"m_{T}(%s,#gamma,p^{miss}_{T})" %(lepname),"logy":1,"ymin":1e-3,"ymax":1e12,"weight":weight, "ymax_scale":1.5,"unblind":False, "bywidth":False}# "unblind":"eventNumber%5==0", "bywidth":False} ## "unblind":False 
        hist_config   = {"xlabel":"m_{T}(%s,#gamma,p^{miss}_{T})" %(lepname),"logy":1,"ymin":1e-7,"ymax":1e3,"weight":weight, "ymax_scale":1.5, "unblind":"eventNumber%5==0", "bywidth":True} 
        #hist_config   = {"xlabel":"m_{T}(%s,#gamma,p^{miss}_{T})" %(lepname),"logy":1,"ymin":1e-3,"ymax":1e8,"weight":weight, "ymax_scale":1.5, "unblind":"eventNumber%5==0", "bywidth":False} 

        label_config  = {"extra_label":labelname, "extra_label_loc":(.17,.82), "labelStyle":str(options.year)}
        legend_config = {'legendLoc':"Double","legendTranslateX":0.3, "legendCompress":1, "fillalpha":.5, "legendWiden":.9}

        if ch == "el":
            plotvars = plotvarsbase+plotvarsel
        if ch == "mu":
            plotvars = plotvarsbase+plotvarsmu
        print('plotvars',plotvars)

        for xlabel, var, unit, vrange in plotvars:
            print('xlabel, var, vrange', xlabel, var, vrange)
            hist_config["xlabel"] = xlabel
            hist_config["doratio"] = True
            hist_config["drawsignal"] = True
            hist_config["xunit"] = unit
            samples.Draw(var, selection,vrange , hist_config,legend_config,label_config)
            ## save histogram
            varname = var.replace("[","").replace("]","").replace(":","_")
            samples.SaveStack("%s_%i%s.pdf" %(varname,options.year, ch), options.outputDir, "base")
    return sampManMuG, sampManElG


sampmu,sampel = main()



