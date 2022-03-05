#!/usr/bin/env python
execfile("MakeBase.py")
year = options.year
hlist = []
sampManElEl.ReadSamples( _SAMPCONF )
sampManMuMu.ReadSamples( _SAMPCONF )
samplesdict = {
    'elel': sampManElEl,
    'mumu': sampManMuMu,
}

ROOT.gStyle.SetPalette(ROOT.kViridis)


slists = {
    'before': ["DYJetsToLL_M-50-amcatnloFXFX","ZGTo2LG"],
    'after': ["DYJetsToLL_M-50-amcatnloFXFXPhOlap","ZGTo2LGPhOlap"],
}

for channel,samples in samplesdict.items():
    lconf = {"labelStyle":str(year),"extra_label":"%i %s channel" %(year,channel), "extra_label_loc":(.17,.82)}
    #lgconf = {'legendLoc':"Double","legendTranslateX":0.35, "legendCompress":.9, "fillalpha":.5}
    lgconf={"legendWiden":1.5,"fillapha":.5}
    #hconf = {"logy":True,"colors":[2,4,6], "weight":"PUWeight*NLOWeight"}
    hconf = {"colors":[2,4],"logy":True,"doratio":True,"rlabel":"ratio to inclusive","reverseratio":True, "xlabel":"gen photon p_{T}", "weight":weight}
    hconfdr = {"colors":[2,4],"logy":True,"doratio":True,"rlabel":"ratio to inclusive","reverseratio":True, "xlabel":"Min #DeltaR(lep,#gamma)", "xunit": "", "weight":weight}

    ## the selection needs Max$ so that event is filled on an event basis, otherwise duplicate values of MaxIf will be filled.
    ## form for conditional max is: MaxIf$(var, particle_selection):Max/Min$(particle_selection)==0/1
    ## easier to just do Max$(var*(condition)):1 so if an event does not fit the selection, a zero is returned

    for label,slist in slists.items():

        ### highest pT gen photon that is prompt final state and in ZG eta+DeltaR
        # def CompareSelections( self, varexp, selections, reqsamples, histpars, hist_config={}, label_config={}, legend_config={}, same=False, useModel=False, treeHist=None, treeSelection=None ) :
        samples.CompareSelections("Max$(trueph_pt*(trueph_isPromptFS && abs(trueph_eta)<2.6 && trueph_lep_dr>0.05))",["1"]*len(slist), slist ,(100,0,100), hconf, lconf, lgconf)
        samples.SaveStack("truephpt_%i%s_MaxIfisPromptFSEtaDr_%s.pdf" %(year,channel,label), options.outputDir, "base")

        samples.CompareSelections("trueph_lep_dr*(trueph_isPromptFS && abs(trueph_eta)<2.6 && trueph_pt>20)",["1"]*len(slist), slist ,(100,0,1), hconfdr, lconf, lgconf)
        samples.SaveStack("truephlepdr1_%i%s_isPromptFSEtaPt_%s.pdf" %(year,channel,label), options.outputDir, "base")

        samples.CompareSelections("trueph_lep_dr*(trueph_isPromptFS && abs(trueph_eta)<2.6 && trueph_pt>20)",["1"]*len(slist), slist ,(100,0,5), hconfdr, lconf, lgconf)
        samples.SaveStack("truephlepdr5_%i%s_isPromptFSEtaPt_%s.pdf" %(year,channel,label), options.outputDir, "base")