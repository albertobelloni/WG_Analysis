import itertools
from math import pi

def get_base_selection( channel ) :

    if channel == 'mu' :
        return 'mu_pt30_n==1 && mu_n==1 && el_n==0 && mu_passTight[0] '  # require 1 muon with pt > 30 and 1 muon with pt > 10 (second lepton veto) and 0 electrons with pt > 10 (second lepton veto)
    if channel == 'el' :
        return 'el_pt30_n==1 && el_n==1 && mu_n==0 && el_passTight[0] && HLT_Ele27_WPTight_Gsf ' # require 1 electron with pt > 30 and 1 electron with pt > 10 (second lepton veto) and 0 muonswith pt > 10 (second lepton veto)
    if channel == 'mumu' :
        return 'mu_pt30_n>=1 && mu_n==2 && mu_passTight[0] && mu_passTight[1] '  # require 1 muon with pt > 30 and 2 muons with pt > 10 
    if channel == 'elel' :
        return 'el_pt30_n>=1 && el_n==2 && el_pt[0]>35 && el_passTight[0] && el_hasTrigMatch[0] ' # require 1 electron with pt > 30 and 2 electrons with pt > 10
    if channel == 'muel' :
        return 'mu_pt30_n>=1 && el_n==1  '  # require 1 muon with pt > 30 and 2 muons with pt > 10 

def get_weight_str( ) :

    #return ' ( NLOWeight * PUWeight + isData ) '
    #return ' ( isData ? isData : PUWeight * NLOWeight )'
    return ' ( isData ? isData : PUWeight * NLOWeight * el_trigSF * el_idSF * el_recoSF * ph_idSF * ph_psvSF * ph_csevSF * mu_trigSF * mu_isoSF * mu_trkSF * mu_idSF * prefweight )'

def get_phid_selection( sel1, sel2='' ) :

    if sel1 == 'all' :
        return 'ph_n'
    if sel1 == 'loose' :
        return 'ph_loose_n' 
    if sel1 == 'medium' :
        return 'ph_medium_n' 
    if sel1 == 'chIso' :
        if sel2 == 'sigmaIEIE' :
            return 'ph_mediumNoSIEIENoChIso_n'
        else :
            return 'ph_mediumNoChIso_n'
    if sel1 == 'sigmaIEIE' :
        if sel2 == 'chIso' :
            return 'ph_mediumNoSIEIENoChIso_n'
        else :
            return 'ph_mediumNoSIEIE_n'

    assert( 'get_phid_selection -- Could not parse selection vars!' )

def get_phid_idx( sel1, sel2='' ) :

    if sel1 == 'all' :
        return '0'
    if sel1 == 'loose' :
        return 'ptSorted_ph_loose_idx[0]' 
    if sel1 == 'medium' :
        return 'ptSorted_ph_medium_idx[0]' 
    if sel1 == 'chIso' :
        if sel2 == 'sigmaIEIE' :
            return 'ptSorted_ph_mediumNoSIEIENoChIso_idx[0]'
        else :
            return 'ptSorted_ph_mediumNoChIso_idx[0]'
    if sel1 == 'sigmaIEIE' :
        if sel2 == 'chIso' :
            return 'ptSorted_ph_mediumNoSIEIENoChIso_idx[0]'
        else :
            return 'ptSorted_ph_mediumNoSIEIE_idx[0]'

    assert( 'get_phid_idx -- Could not parse selection vars!' )

def get_phid_cut_var( ivar ) :

    if ivar == 'chIso' :
        return 'ph_chIsoCorr'
    if ivar == 'sigmaIEIE' :
        return 'ph_sigmaIEIEFull5x5' #ph_sigmaIEIE

    assert( 'get_phid_cut_var -- Could not parse selection vars!' )



badefakesectors = {
        2016: {
            "veto" :[],
            "worst":[],
            "bad"  :[(( 13,   16  ),(-0.5, 1.0)),
                     (( 26.5, 31.5),(-1.6, 0.8)),
                     (( 16.5, 18.5),(-1.5, 1.5)),
                     (( 23,   24  ),(-0.2, 1.5)),
                     ((-18.5,-17.5),(-1.4, 1.4)),
                     ((-27  ,-25  ),( 1.2, 1.5)),
                     ((-27  ,-25  ),(-1.5,-1.2)),
                    ],
            },
        2017:{
            "veto"  :[(( 31, 36),( 1.2,1.4))],
            "worst" :[(( 31, 36),(-0.4,1.6)),
                      ((-36,-35),(-0.4,1.6)),
                      (( 17, 22),(-0.6,1.2)),
                      (( 20, 26),(-1.2,0.3)),
                      (( 10, 12),(-0.6,1. )),
                      (( 30, 31),(-1. ,0. )),
                      ],
            "bad"   :[((  0,  3),(-1. ,0.3)),
                      ((  3,  5),( 0. ,1.2)),
                      ((  5,  8),(-1.5,0. )),
                      ((-28,-26),(-0.4,0.4)),
                      ((-18,-16),(-1. ,0.4)),
                      ((-25,-23),(-1.6,0.2)),
                      ((-20,-18),(-1.6,-0.6)),
                      ((-12,-10),(-1.2,0. )),
                      ((-14,-13),(-1.,-0.4)),
                      (( 22, 25),( 0.4,0.6)),
                      (( 22, 23),( 0.2,0.4)),
                      (( 28, 32),(-1.2,0.4)),
                      (( 31, 36),(-0.8,-0.4)),
                      ],
            },
        2018:{
            "veto"  :[],
            "worst" :[((5,9),( 0.,  1.4)),
                      ((6,8),(-1.4,-0.5)),
                      ((21,23),(-1.,0.)),
                      ((6,8),(-0.2,0.)),
                      ],
            "bad"   :[((  4, 10),(-0.4,1.6)),
                      ((  5, 13),(-1.6,0.8)),
                      (( 16, 21),(-0.4,1.4)),
                      (( 20, 24),(-1. ,0.4)),
                      ((  0,  3),(-1. ,1. )),
                      (( 28, 31),(-1.6,0.4)),
                      ((-19,-15),(-1. ,0.4)),
                      ((-15,-10),(-1.2,0.4)),
                      ((-30,-23),(-0.5,1. )),
                      ((-19,-18),(-1.4,-1.)),
                      ],
            },
        }

def build_bad_efake_sector_string(year, quality):
    " generate bad efake sector substrings (quality: veto, worst, bad) "

    bstr={}
    for key, badlist in badefakesectors[year].iteritems():
        bstr[key]="||".join(itertools.starmap(photonphietastr, badlist))
    combinedstring = ""

    # veto quality
    combinedstring += bstr["veto"]
    if quality == "veto":
        return combinedstring

    # worst quality only (excludes veto)
    if quality == "worstonly":
        if not combinedstring:
            return bstr["worst"]
        return "(%s) && !(%s)" %(bstr["worst"],combinedstring)

    # worst quality
    #if combinedstring: combinedstring += "||"
    if combinedstring: combinedstring =  "(%s)||" %combinedstring
    combinedstring += bstr["worst"]
    if quality == "worst":
        return combinedstring

    # bad quality only (excludes veto and worst)
    if quality == "badonly":
        if not combinedstring:
            return bstr["bad"]
        return "(%s) && !(%s)" %(bstr["bad"],combinedstring)

    ## bad quality
    if combinedstring: combinedstring =  "(%s)||" %combinedstring
    combinedstring += bstr["bad"]
    if quality == "bad":
        return combinedstring
    if quality == "normal":
        return "!(%s)" %combinedstring
    print "ERROR do not recognise: ", quality
    raise RuntimeError

def photonphietastr(iphi, eta):
    assert eta[0]<eta[1],     "eta  order: %g %g" %eta
    assert iphi[0]<iphi[1],   "iphi order: %g %g" %iphi
    sel = (eta[0],eta[1], iphitophi(iphi[0]), iphitophi(iphi[1]))
    return "(ph_eta[0]>%g && ph_eta[0]<%g && ph_phi[0]>%g && ph_phi[0]<%g)" %sel

def iphitophi(iphi):
    assert iphi<=36 and iphi>=-36
    return pi/36*iphi




