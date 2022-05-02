import itertools
from math import pi

def get_base_selection( channel, year=2016 ) :

    if channel == 'mu' :
        return 'mu_pt30_n==1 && mu_n==1 && el_n==0 && mu_passTight[0] && mu_hasTrigMatch[0] '  # require 1 muon with pt > 30 and 1 muon with pt > 10 (second lepton veto) and 0 electrons with pt > 10 (second lepton veto)
    if channel == 'mug' :
        return 'mu_n==1 && el_n==0 && ph_n==1 && mu_pt30_n==1 && mu_passTight[0] && mu_hasTrigMatch[0]'
    if channel == 'elg' :
        return 'el_n==1 && mu_n==0 && ph_n==1 && el_pt35_n==1 && el_passTight[0] && el_hasTrigMatch[0]'
    if channel == 'el' :
        return 'el_pt35_n==1 && el_n==1 && mu_n==0 && el_passTight[0] && el_hasTrigMatch[0] '
    if channel == 'mumu' :
        return 'mu_pt30_n>=1 && mu_n==2 && mu_passTight[0] && mu_passTight[1] && (mu_hasTrigMatch[0] || mu_hasTrigMatch[1])'  # require 1 muon with pt > 30 and 2 muons with pt > 10
    if channel == 'elel' :
        return 'el_pt35_n>=1 && el_n==2 && el_pt[0]>35 && el_passTight[0] && el_passTight[1] && (el_hasTrigMatch[0] || el_hasTrigMatch[1])' # require 1 electron with pt > 30 and 2 electrons with pt > 10
    if channel == 'muel' :
        return 'mu_pt30_n>=1 && el_n==1  '  # require 1 muon with pt > 30 and 2 muons with pt > 10

def get_weight_str( ch = None ) :

    #weight_str = '(isinf(PUWeight)?1:PUWeight)*NLOWeight*prefweight*(isinf(jet_btagSF)?1:jet_btagSF)'
    weight_str = 'PUWeight*NLOWeight*prefweight*jet_btagSF'
    weight_str_mu = weight_str + '*mu_trigSF*mu_idSF*mu_isoSF*mu_trkSF*ph_idSF*ph_psvSF'
    weight_str_el = weight_str + '*el_trigSF*el_idSF*el_recoSF*ph_idSF*ph_psvSF'
    if ch == "el":
        weight = weight_str_el
    elif ch == "mu":
        weight = weight_str_mu
    elif ch == "nosf":
        weight = weight_str
    else:
        weight =' ( isData ? isData : PUWeight * NLOWeight * prefweight * el_trigSF * el_idSF * el_recoSF * ph_idSF * ph_psvSF * mu_trigSF * mu_isoSF * mu_trkSF * mu_idSF * jet_btagSF)'
        #weight =' ( isData ? isData : PUWeight * NLOWeight * prefweight * el_trigSF * el_idSF * el_recoSF * ph_idSF * ph_psvSF * mu_trigSF * mu_isoSF * mu_trkSF * mu_idSF * (isinf(jet_btagSF)?1:jet_btagSF))'
    return weight


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
            "veto"  : [],#[(( 31, 36),( 1.2,1.4))],
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
    for key, badlist in badefakesectors[year].items():
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
    print(("ERROR do not recognise: ", quality))
    raise RuntimeError

def photonphietastr(iphi, eta):
    assert eta[0]<eta[1],     "eta  order: %g %g" %eta
    assert iphi[0]<iphi[1],   "iphi order: %g %g" %iphi
    sel = (eta[0],eta[1], iphitophi(iphi[0]), iphitophi(iphi[1]))
    return "(ph_eta[0]>%g && ph_eta[0]<%g && ph_phi[0]>%g && ph_phi[0]<%g)" %sel

def iphitophi(iphi):
    assert iphi<=36 and iphi>=-36
    return pi/36*iphi




def makeselstring(ch="el", phpt = 80, leppt = 35, met = 40, year=2016, addition = ""):
    """ assemble selection strings """
    selstrlist, weight = makeselstringlist(ch,phpt,leppt,met,year)
    if addition:
        selstrlist.append(addition)
    selstr = " && ".join(selstrlist)
    return selstr, weight

def makeselstringwweight(ch="el", phpt = 80, leppt = 35, met = 40, year=2016,addition = ""):
    """ assemble selection strings. Seems not being used anywhere"""
    selstrlist, weight = makeselstringlist(ch,phpt,leppt,met,year)
    if addition:
        selstrlist.append(addition)
    selstr = " && ".join(selstrlist)
    return weight+'* ( %s )'% selstr

def makeselstringlist(ch="el", phpt = 80, leppt = 35, met = 40, year=2016):
    """ assemble selection strings
        return
            array of selections
    """
    ## NOTE met filter, prefweight, Zvtx weight

    weight = get_weight_str(ch)

    sel_base_mu = get_base_selection( 'mug' )
    sel_base_el = get_base_selection( 'elg' ) ## FIXME trigger doesn't work on 2017/HLT_Ele27_WPTight_Gsf?

    el_tight = ' el_passTight[0] == 1'
    #el_tight = ' el_passVIDTight[0] == 1'
    el_trigMatch = ' el_hasTrigMatch[0] == 1'
    el_eta   = ' fabs( el_eta[0] ) < 2.1 && !(fabs( el_eta[0] ) >1.44&&fabs( el_eta[0] ) < 1.57)'
    el_pt  = 'el_pt[0] > %i ' %leppt

    mu_pt  = 'mu_pt_rc[0] > %i ' %leppt

    ph_base = 'ph_IsEB[0]'
    ph_pt  = '(ph_pt[0] > 0.4*mt_res && ph_pt[0] < 0.55*mt_res) && (ph_pt[0] > %i)' %phpt
    ph_passpix = '!ph_hasPixSeed[0]'
    ph_tight = 'ph_passTight[0]' # already in base selection
    sel_ph =  [ph_base, ph_tight, ph_pt, ph_passpix]

    met_str = 'met_pt > %i' %met

    Zveto_str = 'fabs(m_lep_ph-91)>20.0'
    deepjetveto = "jet_DeepJetSF_n==0"
    #if str(year)=='2016': deepjetveto = '(isData ? Sum$(jet_bTagDeepb>%f)==0 : jet_DeepJetSF_n==0)'%(0.3093)
    #elif str(year)=='2017': deepjetveto = '(isData ? Sum$(jet_bTagDeepb>%f)==0 : jet_DeepJetSF_n==0)'%(0.3033)
    #elif str(year)=='2018': deepjetveto = '(isData ? Sum$(jet_bTagDeepb>%f)==0 : jet_DeepJetSF_n==0)'%(0.2770)
    #else: print('bad year !!!')

    if str(year) == '2018':
        ph_in_hem1516='(ph_phi[0] > -1.57 && ph_phi[0] < -0.87 && ph_eta[0]<-1.3)'
        el_in_hem1516='(el_phi[0] > -1.57 && el_phi[0] < -0.87 && el_eta[0]<-1.3)'
        met_in_hem1516='(met_phi > -1.57 && met_phi < -0.87)'
        sel_base_hem1516_e = '(isData ? !( ('+ph_in_hem1516+'||'+el_in_hem1516+'||'+met_in_hem1516+') && runNumber>=319077):1)'
        sel_base_hem1516_m = '(isData ? !( ('+ph_in_hem1516+'||'+met_in_hem1516+') && runNumber>=319077):1)'
        run319077LumiRatio = '0.345'
        if ch=="el":
            weight=weight+'*(isData ? 1: '+'1-0.655*( '+ph_in_hem1516+'||'+el_in_hem1516+'||'+met_in_hem1516+' ) )'
        if ch=="mu":
            weight=weight+'*(isData ? 1: '+'1-0.655*( '+ph_in_hem1516+'||'+met_in_hem1516+' ) )'
        sel_mu_nominal      = [sel_base_mu,  met_str, mu_pt, deepjetveto,sel_base_hem1516_m ] +  sel_ph
        sel_el_nominal      = [sel_base_el, el_eta, el_pt, el_tight, met_str, Zveto_str, deepjetveto,sel_base_hem1516_e] + sel_ph
    else:
        sel_mu_nominal      = [sel_base_mu,  met_str, mu_pt, deepjetveto ] +  sel_ph
        sel_el_nominal      = [sel_base_el, el_eta, el_pt, el_tight, met_str, Zveto_str, deepjetveto] + sel_ph

    if ch=="mu":
        return sel_mu_nominal, weight
    if ch=="el":
        return sel_el_nominal, weight


def selectcuttag( mass ,year=2016):
    return selectcutstring( mass, "mu",year )[0]

def bkgfitlowbin( cuttag ):
    """ low range of bin content (the upper range is set to 2000 by default) """
    if cuttag == "A":
        return 220

def kinedictgen( ch, year=2016,addition = "" ):
    """ define here cut-sets and tag as function of mass """
    leppt = 35
    if ch=='mu': leppt = 30
    cutsetdict = {
               "A": dict( phpt = 80, leppt = leppt, met = 40, year=year,addition = addition),
            }
    return cutsetdict

def selectcutdictgen( ch, year=2016, addition = "" ):
    """ define here cut-sets and tag as function of mass """
    kinedict = kinedictgen( ch ,year, addition )
    cutsetdict = { k: makeselstring(ch, **w) for k,w in kinedict.iteritems()}
    return cutsetdict

def selectcutstring( mass, ch,year=2016, addition = "" ):
    """ define here cut-sets and tag as function of mass """
    cutsetdict = selectcutdictgen( ch, year,addition )
    returner = lambda d: (d, cutsetdict[d])
    return returner("A")
