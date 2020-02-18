#!/usr/bin/env python
execfile("MakeBase.py")
year = options.year
lconf = {"labelStyle":str(year),"extra_label":"%i Electron Channel" %year, "extra_label_loc":(.17,.82)}
lgconf = {'legendLoc':"Double","legendTranslateX":0.35, "legendCompress":.9, "fillalpha":.5}
hlist = []
sampManElG.ReadSamples( _SAMPCONF )
sampManMuG.ReadSamples( _SAMPCONF )
samples = sampManElG

#get_ipython().magic(u'run interactiveStackTree.py --baseDir  /data2/users/kakw/Resonances2017/LepGamma_elg_2019_12_12/ --samplesConf Modules/Resonance2017.py --xsFile cross_sections/photon17.py --lumi 42000. --treeName UMDNTuple/EventTree --fileName tree.root --batch')

slist = ["WGToLNuG-amcatnloFXFX","WGToLNuG_PtG-130-amcatnloFXFX","WGToLNuG_PtG-500-amcatnloFXFX"]
slist1 = [s+"PhCut" for s in slist]

samples.CompareSelections("MaxIf$(trueph_pt,trueph_isPromptFS)",["trueph_isPromptFS"]*3, slist ,(100,0,1000),{"logy":True,"colors":[2,4,6]}, lconf, lgconf)
samples.SaveStack("truephpt_%ielg_MaxIfisPromptFS.pdf" %year, options.outputDir, "base")
samples.CompareSelections("MaxIf$(trueph_pt,trueph_isPromptFS)",["trueph_isPromptFS"]*3, slist1 ,(100,0,1000),{"logy":True,"colors":[2,4,6]},lconf, lgconf)
samples.SaveStack("truephpt_%ielg_MaxIfisPromptFSPhCut.pdf" %year, options.outputDir, "base")

samples.CompareSelections("trueph_pt[0]",["Max$(trueph_isPromptFS)==0"]*3,slist,(100,0,1000),{"logy":True,"colors":[2,4,6]},lconf, lgconf)
samples.SaveStack("truephpt_%ielg_NoPromptFS.pdf" %year, options.outputDir, "base")
samples.CompareSelections("trueph_pt[0]",["Max$(trueph_isPromptFS)==0"]*3,slist1,(100,0,1000),{"logy":True,"colors":[2,4,6]},lconf, lgconf)
samples.SaveStack("truephpt_%ielg_NoPromptFSPhCut.pdf" %year, options.outputDir, "base")

samples = sampManMuG
lconf = {"labelStyle":str(year),"extra_label":"%i Muon Channel" %year, "extra_label_loc":(.17,.82)}

samples.CompareSelections("MaxIf$(trueph_pt,trueph_isPromptFS)",["trueph_isPromptFS"]*3, slist ,(100,0,1000),{"logy":True,"colors":[2,4,6]}, lconf, lgconf)
samples.SaveStack("truephpt_%imug_MaxIfisPromptFS.pdf" %year, options.outputDir, "base")
samples.CompareSelections("MaxIf$(trueph_pt,trueph_isPromptFS)",["trueph_isPromptFS"]*3, slist1 ,(100,0,1000),{"logy":True,"colors":[2,4,6]},lconf, lgconf)
samples.SaveStack("truephpt_%imug_MaxIfisPromptFSPhCut.pdf" %year, options.outputDir, "base")

samples.CompareSelections("trueph_pt[0]",["Max$(trueph_isPromptFS)==0"]*3,slist,(100,0,1000),{"logy":True,"colors":[2,4,6]},lconf, lgconf)
samples.SaveStack("truephpt_%imug_NoPromptFS.pdf" %year, options.outputDir, "base")
samples.CompareSelections("trueph_pt[0]",["Max$(trueph_isPromptFS)==0"]*3,slist1,(100,0,1000),{"logy":True,"colors":[2,4,6]},lconf, lgconf)
samples.SaveStack("truephpt_%imug_NoPromptFSPhCut.pdf" %year, options.outputDir, "base")
