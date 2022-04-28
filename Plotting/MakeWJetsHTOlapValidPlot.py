#!/usr/bin/env python3
exec(compile(open("MakeBase.py", "rb").read(), "MakeBase.py", 'exec'))
year = options.year
hlist = []
sampManEl.ReadSamples( _SAMPCONF )
sampManMu.ReadSamples( _SAMPCONF )
samplesdict = {
    'el': sampManEl,
    'mu': sampManMu,
}

ROOT.gStyle.SetPalette(ROOT.kViridis)


slists = {
    'before': ['WJetsToLNu-madgraphMLMPhOlap', 'WJetsToLNu_HT-100To200', 'WJetsToLNu_HT-200To400', 'WJetsToLNu_HT-400To600', 'WJetsToLNu_HT-600To800', 'WJetsToLNu_HT-800To1200', 'WJetsToLNu_HT-1200To2500', 'WJetsToLNu_HT-2500ToInf'],
    'after':['WJetsToLNuTrueHTOlap', 'WJetsToLNu_HT-100To200', 'WJetsToLNu_HT-200To400', 'WJetsToLNu_HT-400To600', 'WJetsToLNu_HT-600To800', 'WJetsToLNu_HT-800To1200', 'WJetsToLNu_HT-1200To2500', 'WJetsToLNu_HT-2500ToInf'],
}

for channel,samples in list(samplesdict.items()):
    lconf = {"labelStyle":str(year),"extra_label":"%i %s channel" %(year,channel), "extra_label_loc":(.17,.82)}
    #lgconf = {'legendLoc':"Double","legendTranslateX":0.35, "legendCompress":.9, "fillalpha":.5}
    lgconf={"legendWiden":1.5,"fillapha":.5}
    #hconf = {"logy":True,"colors":[2,4,6], "weight":"PUWeight*NLOWeight"}
    hconf = {"colors":[1,2,3,4,6,7,8,9],"logy":True,"doratio":True,"rlabel":"ratio to inclusive","reverseratio":True, "xlabel":"HT", "weight":weight}

    ## the selection needs Max$ so that event is filled on an event basis, otherwise duplicate values of MaxIf will be filled.
    ## form for conditional max is: MaxIf$(var, particle_selection):Max/Min$(particle_selection)==0/1
    ## easier to just do Max$(var*(condition)):1 so if an event does not fit the selection, a zero is returned

    for label,slist in list(slists.items()):

        ### highest pT gen photon that is prompt final state and in ZG eta+DeltaR
        # def CompareSelections( self, varexp, selections, reqsamples, histpars, hist_config={}, label_config={}, legend_config={}, same=False, useModel=False, treeHist=None, treeSelection=None ) :
        samples.CompareSelections("trueht",["1"]*len(slist), slist ,(150,0,3000), hconf, lconf, lgconf)
        samples.SaveStack("trueht_%i%s_%s.pdf" %(year,channel,label), options.outputDir, "base")
