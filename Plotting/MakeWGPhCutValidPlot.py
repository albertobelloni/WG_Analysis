#!/usr/bin/env python
execfile("MakeBase.py")
year = options.year
hlist = []
sampManElG.ReadSamples( _SAMPCONF )
sampManMuG.ReadSamples( _SAMPCONF )
samples = sampManElG
ROOT.gStyle.SetPalette(ROOT.kViridis)


slist = ["WGToLNuG-amcatnloFXFX","WGToLNuG_PtG-130-amcatnloFXFX","WGToLNuG_PtG-500-amcatnloFXFX"]
slist1 = [s+"PhCut" for s in slist]
lconf = {"labelStyle":str(year),"extra_label":"%i Electron Channel" %year, "extra_label_loc":(.17,.82)}
#lgconf = {'legendLoc':"Double","legendTranslateX":0.35, "legendCompress":.9, "fillalpha":.5}
lgconf={"legendWiden":1.5,"fillapha":.5}
#hconf = {"logy":True,"colors":[2,4,6], "weight":"PUWeight*NLOWeight"}
hconf = {"colors":[2,4,6],"logy":True,"doratio":True,"rlabel":"ratio to inclusive","reverseratio":True, "xlabel":"gen photon p_{T}", "weight":weight}

## the selection needs Max$ so that event is filled on an event basis, otherwise duplicate values of MaxIf will be filled.
## form for conditional max is: MaxIf$(var, particle_selection):Max/Min$(particle_selection)==0/1
## easier to just do Max$(var*(condition)):1 so if an event does not fit the selection, a zero is returned
samples.Draw2D("Max$(trueph_pt*(trueph_status==23)):Max$(trueph_pt*(trueph_isPromptFS))",["1*NLOWeight"],["WGToLNuG_PtG-500-amcatnloFXFX"],
                    (120,0,1200,120,0,1200),"COLZ",logz=True)
samples.SaveStack("truephpt_%ielg_isPromptFSVSstatus23_PtG500.pdf" %year, options.outputDir, "base0")
samples.Draw2D("Max$(trueph_pt*(trueph_status==23)):Max$(trueph_pt*(trueph_isPromptFS))",["1*NLOWeight"],["WGToLNuG_PtG-130-amcatnloFXFX"],
                    (120,0,1200,120,0,1200),"COLZ",logz=True)
samples.SaveStack("truephpt_%ielg_isPromptFSVSstatus23_PtG130.pdf" %year, options.outputDir, "base0")
samples.Draw2D("Max$(trueph_pt*(trueph_status==23)):Max$(trueph_pt*(trueph_isPromptFS))",["1*NLOWeight"],["WGToLNuG-amcatnloFXFX"],
                    (120,0,1200,120,0,1200),"COLZ",logz=True)
samples.SaveStack("truephpt_%ielg_isPromptFSVSstatus23_PtGincl.pdf" %year, options.outputDir, "base0")

### highest pT gen photon that is prompt final state
samples.CompareSelections("Max$(trueph_pt*(trueph_isPromptFS))",["1"]*3, slist ,(100,0,1000), hconf, lconf, lgconf)
samples.SaveStack("truephpt_%ielg_MaxIfisPromptFS.pdf" %year, options.outputDir, "base")
#samples.CompareSelections("MaxIf$(trueph_pt,trueph_isPromptFS)",["Max$(trueph_isPromptFS)"]*3, slist1 ,(100,0,1000),hconf,lconf, lgconf)
#samples.SaveStack("truephpt_%ielg_MaxIfisPromptFSPhCut.pdf" %year, options.outputDir, "base")

### highest pT gen photon in events without ispromptfs photon
samples.CompareSelections("trueph_pt[0]",["Max$(trueph_isPromptFS)==0"]*3,slist,(100,0,1000),hconf,lconf, lgconf)
samples.SaveStack("truephpt_%ielg_NoPromptFS.pdf" %year, options.outputDir, "base")
#samples.CompareSelections("trueph_pt[0]",["Max$(trueph_isPromptFS)==0"]*3,slist1,(100,0,1000),hconf,lconf, lgconf)
#samples.SaveStack("truephpt_%ielg_NoPromptFSPhCut.pdf" %year, options.outputDir, "base")

### highest pT gen photon with status 23
samples.CompareSelections("Max$(trueph_pt*(trueph_status==23))",["1"]*3,slist,(100,0,1000),hconf,lconf, lgconf)
samples.SaveStack("truephpt_%ielg_status23.pdf" %year, options.outputDir, "base")

### highest pT gen photon with W+/- mother in events without a status 23 photon
samples.CompareSelections("Max$(trueph_pt*(abs(trueph_motherPID)==24))",["Max$(trueph_status==23)==0"]*3,slist,
                            (100,0,1000),hconf,lconf, lgconf)
samples.SaveStack("truephpt_%ielg_mother24_nostatus23.pdf" %year, options.outputDir, "base")

### highest pT gen photon passing either status == 23 or FSR from W+/-
samples.CompareSelections("Max$(trueph_pt*(trueph_status==23||(abs(trueph_motherPID)==24&&trueph_isPromptFS)))",
                            ["1"]*3,slist,(100,0,1000),hconf, lconf, lgconf)
samples.SaveStack("truephpt_%ielg_status23OR24ispromptfs.pdf" %year, options.outputDir, "base")
samples.clear_all()


samples = sampManMuG
lconf = {"labelStyle":str(year),"extra_label":"%i Muon Channel" %year, "extra_label_loc":(.17,.82)}
hconf = {"colors":[2,4,6],"logy":True,"doratio":True,"rlabel":"ratio to inclusive","reverseratio":True, "xlabel ":"gen photon p_{T}","weight":weight}

#samples.CompareSelections("MaxIf$(trueph_pt,trueph_isPromptFS)",["Max$(trueph_isPromptFS)"]*3, slist ,(100,0,1000),hconf, lconf, lgconf)
#samples.SaveStack("truephpt_%imug_MaxIfisPromptFS.pdf" %year, options.outputDir, "base")
##samples.CompareSelections("MaxIf$(trueph_pt,trueph_isPromptFS)",["Max$(trueph_isPromptFS)"]*3, slist1 ,(100,0,1000),hconf,lconf, lgconf)
##samples.SaveStack("truephpt_%imug_MaxIfisPromptFSPhCut.pdf" %year, options.outputDir, "base")
#
#samples.CompareSelections("trueph_pt[0]",["Max$(trueph_isPromptFS)==0"]*3,slist,(100,0,1000),hconf,lconf, lgconf)
#samples.SaveStack("truephpt_%imug_NoPromptFS.pdf" %year, options.outputDir, "base")
##samples.CompareSelections("trueph_pt[0]",["Max$(trueph_isPromptFS)==0"]*3,slist1,(100,0,1000),hconf,lconf, lgconf)
##samples.SaveStack("truephpt_%imug_NoPromptFSPhCut.pdf" %year, options.outputDir, "base")
#samples.CompareSelections("MaxIf$(trueph_pt,trueph_status==23)",["1"]*3,slist,(100,0,1000),hconf,lconf, lgconf)
#samples.SaveStack("truephpt_%imug_status23.pdf" %year, options.outputDir, "base")
samples.Draw2D("Max$(trueph_pt*(trueph_status==23)):Max$(trueph_pt*(trueph_isPromptFS))",["1*NLOWeight"],["WGToLNuG_PtG-500-amcatnloFXFX"],
                    (150,0,1500,150,0,1500),"COLZ",logz=True)
samples.SaveStack("truephpt_%imug_isPromptFSVSstatus23_PtG500.pdf" %year, options.outputDir, "base0")
samples.Draw2D("Max$(trueph_pt*(trueph_status==23)):Max$(trueph_pt*(trueph_isPromptFS))",["1*NLOWeight"],["WGToLNuG_PtG-130-amcatnloFXFX"],
                    (150,0,1500,150,0,1500),"COLZ",logz=True)
samples.SaveStack("truephpt_%imug_isPromptFSVSstatus23_PtG130.pdf" %year, options.outputDir, "base0")
samples.Draw2D("Max$(trueph_pt*(trueph_status==23)):Max$(trueph_pt*(trueph_isPromptFS))",["1*NLOWeight"],["WGToLNuG-amcatnloFXFX"],
                    (150,0,1500,150,0,1500),"COLZ",logz=True)
samples.SaveStack("truephpt_%imug_isPromptFSVSstatus23_PtGincl.pdf" %year, options.outputDir, "base0")

### highest pT gen photon that is prompt final state
samples.CompareSelections("Max$(trueph_pt*(trueph_isPromptFS))",["1"]*3, slist ,(100,0,1000),hconf, lconf, lgconf)
samples.SaveStack("truephpt_%imug_MaxIfisPromptFS.pdf" %year, options.outputDir, "base")

### highest pT gen photon in events without ispromptfs photon
samples.CompareSelections("trueph_pt[0]",["Max$(trueph_isPromptFS)==0"]*3,slist,(100,0,1000),hconf,lconf, lgconf)
samples.SaveStack("truephpt_%imug_NoPromptFS.pdf" %year, options.outputDir, "base")

### highest pT gen photon with status 23
samples.CompareSelections("Max$(trueph_pt*(trueph_status==23))",["1"]*3,slist,(100,0,1000),hconf,lconf, lgconf)
samples.SaveStack("truephpt_%imug_status23.pdf" %year, options.outputDir, "base")

### highest pT gen photon with W+/- mother in events without a status 23 photon
samples.CompareSelections("Max$(trueph_pt*(abs(trueph_motherPID)==24))",["Max$(trueph_status==23)==0"]*3,slist,
                            (100,0,1000),hconf,lconf, lgconf)
samples.SaveStack("truephpt_%imug_mother24_nostatus23.pdf" %year, options.outputDir, "base")

### highest pT gen photon passing either status == 23 or FSR from W+/-
samples.CompareSelections("Max$(trueph_pt*(trueph_status==23||(abs(trueph_motherPID)==24&&trueph_isPromptFS)))",
                            ["1"]*3,slist,(100,0,1000),hconf, lconf, lgconf)
samples.SaveStack("truephpt_%imug_status23OR24ispromptfs.pdf" %year, options.outputDir, "base")


## NOTE correct stitching
samples.CompareSelections("Max$(trueph_pt*(trueph_status==23||(abs(trueph_motherPID)==24&&trueph_isPromptFS)))",
                            ["1"]*3,slist1,(100,0,1000),hconf, lconf, lgconf)
samples.SaveStack("truephpt_%imug_status23OR24ispromptfs_final.pdf" %year, options.outputDir, "base")
