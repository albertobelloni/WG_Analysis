#!/usr/bin/env python
import itertools
execfile("MakeBase.py")


year = options.year
lconf = {"labelStyle":str(year),"extra_label":"%i Muon Channel" %year, "extra_label_loc":(.17,.82)}
lgconf = {'legendLoc':"Double","legendTranslateX":0.35, "legendCompress":.9, "fillalpha":.5}
hlist = []


sampManMuMu.ReadSamples( _SAMPCONF )
samples = sampManMuMu

selection = "mu_n==2"
sf = samples.SetFilter(selection)
hlist=[]

varlist = [ ("met_pt","MET","GeV",(100,0,250)),
            ("m_ll","m(e,e)","GeV",(100,0,200)),
            ("mt_res","reco mT","GeV",(100,0,200)),
            ("ph_pt", "#gamma pT", "GeV", (100,0,200)),
            ("mu_pt[0]", "leading #mu pT", "GeV", (100,0,300)),
            ("mu_pt[1]", "subleading #mu pT", "GeV", (100,0,300)),
            ("mu_eta[0]", "leading #mu #eta",    "", (50,-3,3)),
            ("mu_eta[1]", "subleading #mu #eta", "", (50,-3,3)),
            ]

#no log
var2list = [ ("met_pt","MET","GeV",(100,0,100)),
            ("met_phi", "MET #phi", "", (72,-pie,pie)),
            ("mu_phi[0]", "leading e #phi", "", (72, -pie, pie)),
            ("mu_phi[1]", "subleading e #phi", "", (72, -pie, pie)),
            ]


seldict = {
        ("met",metgt):      [25,30,40,50,60,75,90,100,120,140,
                             160,180,200,250,300,450,500,600],
        ("phpt",phptgt):    [10,15,20,25,30,35,40,45,50,60,70,
                             80,90,100,120,140,160,180,200,220,250,300],
        ("elpt",elptgt):    [30,35,40,45,50,60,70,80,90,100,120,
                             140,160,180,200,220,250,300],## elch only ##FIXME
        ("mupt",muptgt):    [30,35,40,45,50,60,70,80,90,100,120,
                             140,160,180,200,220,250,300],
        ("invz",invzlt):    [10,15,20,30,50,75,100,150,200,250,300],
        ("phid", "&&ph_passVID%s[0]==1"): ["Medium","Tight"],
        ("elid", "&&el_passVID%s[0]==1"): ["Medium","Tight"],
        ("muid", "&&mu_passVID%s[0]==1"): ["Medium","Tight"],
        ("eleta", elaetalt): [1.4,1.6,2.1,3]
            }



def quickcounter(sf, var, selection, weight, tag=""):
    sf = sf.SkipData().SetFilter(selection)
                      .SetDefine("weight",weight)
                      .SetCount(weight="weight")
    sf.selection_string=selection
    sf.tag = tag
    return sf

def selstringbuilder(seldict={}):
    """
        {"met_pt<%i": [20,30,40], "abs(m_lep_ph-91)>%i":[20,30,40]}
    """
    ## format single selection string with numbers in value array
    sellist = [ map(lambda i: k%i, v ) for k,v in seldict.iteritems()]

    # make full product of all combinations
    selfulllist=itertools.product(**sellist)

    # make sure they are properly joint together
    selstrs = [" ".join(s) for s in slist]

    print "number of selections generated: " len(selstrs)

    return selstrs
