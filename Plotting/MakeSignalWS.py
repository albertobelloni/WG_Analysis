#!/usr/bin/env python
import matplotlib.pyplot as plt
import re
import json
import uuid
from uncertainties import ufloat
def addparser(parser):
    parser.add_argument('--plots',  action='store_true', help='Plot fit parameter shifts' )
    parser.add_argument('--doAllFits',  action='store_true', help='Fit all possible systematics (do not flag for combine)' )
execfile("MakeBase.py")
ROOT.PyConfig.IgnoreCommandLineOptions = True
ROOT.Math.MinimizerOptions.SetDefaultMaxFunctionCalls( 100000)

_XMIN_M = 60
_XMAX_M = 4000
_DEFAULTDATADIR = 'data/sigfit/'

if options.dataDir is None :
    options.dataDir = _DEFAULTDATADIR
if options.dataDir is not None :
    if not os.path.isdir( options.dataDir ) :
        os.makedirs( options.dataDir )
        os.makedirs( options.dataDir+ "/2016" )
        os.makedirs( options.dataDir+ "/2017" )
        os.makedirs( options.dataDir+ "/2018" )
fitmlist = []
fitted_masses = OrderedDict()
_JSONLOC = "%s/fitted_mass%i.txt"%(options.dataDir,options.year)

def main() :
    sampManMuG = SampleManager( options.baseDirMuG, _TREENAME, filename=_FILENAME, lumi=-1)
    sampManElG = SampleManager( options.baseDirElG, _TREENAME, filename=_FILENAME, lumi=-1)
    sampManMuG.ReadSamples( _SAMPCONF )
    sampManElG.ReadSamples( _SAMPCONF )

    workspaces_to_save = {}

    bin_width_m = 20

    xmin_pt = _XMIN_M/2
    if xmin_pt < 50 :
        xmin_pt = 50
    xmax_pt = _XMAX_M/2
    bin_width_pt = bin_width_m/2.


    signal_binning_m_width1 = {
                         200 : ( (_XMAX_M)/4 , 0, _XMAX_M ),
                         250 : ( (_XMAX_M)/4 , 0, _XMAX_M ),
                         300 : ( (_XMAX_M)/4 , 0, _XMAX_M ),
                         350 : ( (_XMAX_M)/4 , 0, _XMAX_M ),
                         400 : ( (_XMAX_M)/4 , 0, _XMAX_M ),
                         450 : ( (_XMAX_M)/5 , 0, _XMAX_M ),
                         500 : ( (_XMAX_M)/8 , 0, _XMAX_M ),
                         600 : ( (_XMAX_M)/10, 0, _XMAX_M ),
                         700 : ( (_XMAX_M)/10, 0, _XMAX_M ),
                         800 : ( (_XMAX_M)/10, 0, _XMAX_M ),
                         900 : ( (_XMAX_M)/10, 0, _XMAX_M ),
                        1000 : ( (_XMAX_M)/10, 0, _XMAX_M ),
                        1200 : ( int((_XMAX_M)/15), 0, _XMAX_M ),
                        1400 : ( int((_XMAX_M)/15), 0, _XMAX_M ),
                        1600 : ( int((_XMAX_M)/15), 0, _XMAX_M ),
                        1800 : ( int((_XMAX_M)/15), 0, _XMAX_M ),
                        2000 : ( (_XMAX_M)/20, 0, _XMAX_M ),
                        2200 : ( (_XMAX_M)/20, 0, _XMAX_M ),
                        2400 : ( (_XMAX_M)/20, 0, _XMAX_M ),
                        2600 : ( (_XMAX_M)/20, 0, _XMAX_M ),
                        2800 : ( int((_XMAX_M)/25), 0, _XMAX_M ),
                        3000 : ( int((_XMAX_M)/25), 0, _XMAX_M ),
                        3500 : ( int((_XMAX_M)/40), 0, _XMAX_M ),
                        4000 : ( int((_XMAX_M)/40), 0, _XMAX_M ),
                       }

    signal_binning_m_width2 = {
                         200 : ( (_XMAX_M)/4 , 0, _XMAX_M ),
                         250 : ( (_XMAX_M)/4 , 0, _XMAX_M ),
                         300 : ( (_XMAX_M)/4 , 0, _XMAX_M ),
                         350 : ( (_XMAX_M)/5 , 0, _XMAX_M ),
                         400 : ( (_XMAX_M)/5 , 0, _XMAX_M ),
                         450 : ( (_XMAX_M)/8 , 0, _XMAX_M ),
                         500 : ( (_XMAX_M)/8 , 0, _XMAX_M ),
                         600 : ( (_XMAX_M)/8 , 0, _XMAX_M ),
                         700 : ( (_XMAX_M)/10, 0, _XMAX_M ),
                         800 : ( (_XMAX_M)/10, 0, _XMAX_M ),
                         900 : ( int((_XMAX_M)/15), 0, _XMAX_M ),
                        1000 : ( int((_XMAX_M)/15), 0, _XMAX_M ),
                        1200 : ( (_XMAX_M)/20, 0, _XMAX_M ),
                        1400 : ( (_XMAX_M)/25, 0, _XMAX_M ),
                        1600 : ( (_XMAX_M)/25, 0, _XMAX_M ),
                        1800 : ( int((_XMAX_M)/30), 0, _XMAX_M ),
                        2000 : ( int((_XMAX_M)/30), 0, _XMAX_M ),
                        2200 : ( int((_XMAX_M)/30), 0, _XMAX_M ),
                        2400 : ( int((_XMAX_M)/30), 0, _XMAX_M ),
                        2600 : ( int((_XMAX_M)/35), 0, _XMAX_M ),
                        2800 : ( int((_XMAX_M)/35), 0, _XMAX_M ),
                        3000 : ( int((_XMAX_M)/35), 0, _XMAX_M ),
                        3500 : ( int((_XMAX_M)/40), 0, _XMAX_M ),
                        4000 : ( int((_XMAX_M)/40), 0, _XMAX_M ),
                       }

    signal_binning_m = [ signal_binning_m_width1, signal_binning_m_width2 ]

    ### pT binning is just mass binning divided by two, with floor of 50 GeV
    signal_binning_pt = {}
    for mass, binning in signal_binning_m_width1.iteritems() :
        pt_min = binning[1]/2.
        if pt_min < 50 :
            pt_min = 50
        signal_binning_pt[mass] = ( binning[0]/2., pt_min, binning[2]/2. )



    kine_vars = { 'mt_res' : { 'var' : 'mt_res' , 'signal_binning' : signal_binning_m }, }

    lepg_samps = { 'mu' : sampManMuG, 'el' : sampManElG }

    for ch, man in lepg_samps.iteritems() :
        ## loop channel and sample manager
        for name, vardata in kine_vars.iteritems() :
            ## variables to be fitted
            print "name",name,"vardata", vardata

            ## call fit function
            make_signal_fits( man, workspaces_to_save=workspaces_to_save,
                               suffix='%s%i'%(ch,options.year), **vardata)

    #multidict_tojson2(_JSONLOC, fitted_masses )

    for fileid, ws in workspaces_to_save.iteritems() :
            ws.writeToFile( '%s/%s/%s.root' %( options.dataDir, options.year, fileid ) )

    sys.exit()




def parsesampname(name):
    res = re.match('(MadGraph|Pythia)ResonanceMass(\d+)_.*', name )
    if res is None :
        print 'Could not interpret path ', name
    else :

        mass = float(res.group(2))
        iwidth = 0
        if name.count( 'width0p01' ) :
            width = 0.01
            wid = "0p01"
        else :
            res2 = re.match('(MadGraph|Pythia)ResonanceMass(\d+)_width(\d)', name )
            width = float(res2.group(3))
            wid = res2.group(3)
            iwidth = 1
    return mass, width, wid, iwidth

def numtostr(num=0):
    strg = "%g" %num
    return strg.replace(".","p")



def makevar(var, mass):
    xvar = ROOT.RooRealVar( var, var, _XMIN_M , _XMAX_M)
    fit_max = mass * 1.20
    fit_min = max ( mass * 0.50,  200.0 )
    ## set the fit range
    xvar.setMin( fit_min )
    xvar.setMax( fit_max )
    return xvar


def make_signal_fits( sampMan, suffix="", workspaces_to_save=None, var="mt_res",  signal_binning=[]):

    sampMan.clear_hists()

    ## decide which channel it is
    assert "mu" in suffix or "el" in suffix, \
            "suffix %s must contain the mu or el channel" %suffix

    if 'mu' in suffix:
       extra_label = "Muon channel"
       ch="mu"
    else:
       extra_label = "Electron channel"
       ch="el"
    #raw_input(ch+" cont")


    ### now loop over all samples to fit each of them
    for samp in sampMan.get_samples(isSignal=True ) :

        print 'Sample = ', samp.name
        mass, width, wid, iwidth = parsesampname(samp.name)

        #if mass!=400: continue #FIXME test
        ### exclude certain samples
        if samp.name.count( 'MadGraph' ) == 0:
           continue
        if mass > 2000 or mass < 300:
           continue
        if iwidth >=len(signal_binning):
           print "exclude", iwidth,signal_binning
           continue
        if mass not in signal_binning[iwidth]:
           print "exclude mass", mass, signal_binning[iwidth]
           continue

        ## make full suffix
        full_suffix = "_".join(['MG', "M%d"%mass, 'W%s'%wid, suffix])

        ## make full selection string
        binning = signal_binning[iwidth][mass]
        addition = " (%s > %d && %s < %d )" %(var, binning[1], var ,binning[2])
        cuttag, (full_sel_sr, weight) = defs.selectcutstring( mass , ch, addition )
        print full_sel_sr
        #weight = "NLOWeight"
        if options.year == 2018:
            weight = weight.replace("*prefweight","") ## no prefiring weight in 2018

        ## make RooRealVar for fit variable

        xvar = makevar(var, mass)

        sample_params = {'mass' : mass, 'width' : width}

        workspace  = ROOT.RooWorkspace( 'wssignal_M%d_W%s_%s'%(mass, wid, ch) )

        lconf = {"labelStyle":str(options.year),
                 "extra_label":"%i %s" %(options.year, extra_label),
                 "extra_label_loc":(.12,.82)}

        ## make histogram
        sampMan.create_hist( samp, var, "(%s)*%s" %(full_sel_sr,weight), signal_binning[iwidth][mass] )
        print "Integral: ", samp.hist.Integral()

        ## fit histogram
        fitman = fit_sample( samp.hist, xvar, workspace, full_suffix, sample_params, lconf)

        fitvals = fitman.get_parameter_vals()

        normval = (fitvals["cb_mass"], fitvals["cb_sigma"])
        fitted_masses[(ch,mass,width,"norm")] = normval


        if options.doAllFits:
            sel_odict = make_syssellist(var, full_sel_sr, weight, ch= ch)

            for tag, (v, s, w) in sel_odict.iteritems():

                sampMan.create_hist( samp, v, "(%s)*%s" %(s,w), signal_binning[iwidth][mass] )

                ### fit with only mean floating

                fitman = fit_sample( samp.hist, xvar, workspace, full_suffix+"_mean_"+tag,
                                     sample_params, lconf, fitvals, "mean")
                fitvalsnew = fitman.get_parameter_vals()

                fitted_masses[(ch, mass, width, "mean_%s" %tag)] = (fitvalsnew["cb_mass"], fitvalsnew["cb_sigma"])

                #### fit with mean and sigma floating

                #fitman = fit_sample( samp.hist, xvar, workspace, full_suffix+"_sigma_"+tag,
                #                     sample_params, lconf, fitvals, "meansigma")
                #fitvalsnew = fitman.get_parameter_vals()

                #fitted_masses[(ch, mass, width, "sigma_%s" %tag)] = (fitvalsnew["cb_mass"], fitvalsnew["cb_sigma"])
        else:

            sel_odict = make_syssel(var, full_sel_sr, weight, ch= ch)

            for tag, (v, s, w) in sel_odict.iteritems():

                sampMan.create_hist( samp, v, "(%s)*%s" %(s,w), signal_binning[iwidth][mass] )

                ### fit with only mean floating

                fitman = fit_sample( samp.hist, xvar, workspace, full_suffix+"_"+tag,
                                     sample_params, lconf, fitvals, "mean")
                fitvalsnew = fitman.get_parameter_vals()

                fitted_masses[(ch, mass, width, "mean_%s" %tag)] = (fitvalsnew["cb_mass"], fitvalsnew["cb_sigma"])


        ## save result
        #workspaces_to_save.update( { workspace.GetName() : workspace} )
        assert workspaces_to_save.get(workspace.GetName())==None, workspace.GetName()
        workspaces_to_save[ workspace.GetName() ] = workspace

        fitted_mass =  search_multidict(fitted_masses, (mass,width,None))
        for k,v in fitted_mass.iteritems():
            print "%-30s %10.1f %6.1f%% %10.1f %6.0f%%" %(k, (v[0][0]-normval[0][0]), v[0][0]/normval[0][0]*100-100, v[1][0]-normval[1][0], v[1][0]/normval[1][0]*100-100,)
        #if "q" in raw_input("cont"):
        #   sys.exit()

    #fitted_masses_json = {"%i_%g_%s" %k: v for k,v in fitted_masses.iteritems()}
    #with open(_JSONLOC, "w") as fo:
    #    json.dump( fitted_masses_json, fo)
    print fitted_masses.keys()



def fit_sample( hist, xvar,  workspace , suffix, sample_params, label_config, usevals=None, fittype=None):

    fitManager = FitManager( 'dscb',  hist=hist,  xvardata = xvar,
                            sample_params=sample_params, label = suffix)

    fitManager.setup_fit()

    if usevals:
        fitManager.set_parameter_vals( usevals )

    if fittype=="mean":
        for k, val in fitManager.fit_params.iteritems():
            if k == "cb_mass":
                val.setConstant(False)
            else:
                val.setConstant(True)

    if fittype=="sigma":
        for k, val in fitManager.fit_params.iteritems():
            if k == "cb_sigma":
                val.setConstant(False)
            else:
                val.setConstant(True)

    if fittype=="meansigma":
        for k, val in fitManager.fit_params.iteritems():
            if k == "cb_sigma" or k == "cb_mass":
                val.setConstant(False)
            else:
                val.setConstant(True)

    for k, val in fitManager.fit_params.iteritems():
        print k
        val.Print()

    fitManager.run_fit_minuit( fitrange = xvar ) #, debug = True)
    fitManager.get_results( workspace )

    ## NOTE uncomment this to make a flat mass shift (default 0.5%) for all samples
    #if not fittype: fitManager.shifted_dscb( workspace )
    #fitManager.save_fit( sampMan, workspace, stats_pos='left',
    #                     extra_label = extra_label , plotParam =True)

    canv = fitManager.draw( subplot = "pull", paramlayout = (0.12,0.5,0.78),
                            useOldsetup = True, label_config = label_config)

    canv.Print("%s/%s.pdf" %(options.outputDir, suffix) )
    canv.Print("%s/%s.png" %(options.outputDir, suffix) )
    canv.Print("%s/%s.C"   %(options.outputDir, suffix) )

    print "************"
    print " RooFitResult Status: %d"%fitManager.fitresult.status()
    print "************"


    #fitmlist.append(fitManager)
    return fitManager


def fit_pol1( hist, xmin, xmax ) :

    lin_func = ROOT.TF1( 'lin_func', '[0] + [1]*x', xmin, xmax )

    lin_func.SetParameter( 0, 0.5 )
    lin_func.SetParameter( 1, 0 )

    hist.Fit( lin_func, 'R' )

    hist.Draw()
    lin_func.Draw('same')


def clone_sample_and_draw( sampMan, samp, var, sel, binning ) :

    newSamp = sampMan.clone_sample( oldname=samp, newname=samp+str(uuid.uuid4()), temporary=True )
    sampMan.create_hist( newSamp, var, sel, binning )
    return newSamp.hist

SFlistel = ["el_trig", "el_id", "el_reco",
          "ph_id",   "ph_psv"] ## SF, SFUP, SFDOWN
SFlistmu = [ "mu_trig", "mu_id", "mu_trk", "mu_iso",
              "ph_id",   "ph_psv"]

metlist=[
            "JetRes",
            "JetEn",
            "MuonEn",
            "ElectronEn",
            "PhotonEn",
            "UnclusteredEn", #--/Up/Down
        ]

eventweightlist = ["muR1muF2",
                   "muR1muFp5",
                   "muR2muF1",
                   "muR2muF2",
                   "muRp5muF1",
                   "muRp5muFp5"
                   ]

def make_syssel( varnorm, selnorm, weightnorm, ch = "el"):

    """ This function hard-codes the up/down shape variation
       the limit-setter takes
    """
    selection_list = OrderedDict()

    if ch == "mu":

        #up variation
        w = weightnorm.replace("mt_res", "mt_res_MuonEnUp" )\
                  .replace("met_pt", "met_MuonEnUp_pt" )
        sel = selnorm.replace("mt_res", "mt_res_MuonEnUp"  )\
                  .replace("met_pt", "met_MuonEnUp_pt"  )
        sel = sel.replace("mu_pt_rc", "mu_pt_rc_up")
        var = "mt_res_MuonEnUp"
        selection_list["up"] = (var, sel, w)

        #down variation
        w = weightnorm.replace("mt_res", "mt_res_MuonEnDown" )\
                  .replace("met_pt", "met_MuonEnDown_pt" )
        sel = selnorm.replace("mt_res", "mt_res_MuonEnDown"  )\
                  .replace("met_pt", "met_MuonEnDown_pt"  )
        sel = sel.replace("mu_pt_rc", "mu_pt_rc_down")
        var = "mt_res_MuonEnDown"
        selection_list["down"] = (var, sel, w)

    if ch == "el":
        # up variation
        w = weightnorm.replace("mt_res", "mt_res_PhotonEnUp" )\
                  .replace("met_pt", "met_PhotonEnUp_pt" )
        sel = selnorm.replace("mt_res", "mt_res_PhotonEnUp"  )\
                  .replace("met_pt", "met_PhotonEnUp_pt"  )
        var = "mt_res_PhotonEnUp"
        selection_list["up"] = (var, sel, w)

        # down variation
        w = weightnorm.replace("mt_res", "mt_res_PhotonEnDown" )\
                  .replace("met_pt", "met_PhotonEnDown_pt" )
        sel = selnorm.replace("mt_res", "mt_res_PhotonEnDown"  )\
                  .replace("met_pt", "met_PhotonEnDown_pt"  )
        var = "mt_res_PhotonEnDown"
        selection_list["down"] = (var, sel, w)
    return selection_list

def make_syssellist( varnorm, selnorm, weightnorm, ch = "el"):

    selection_list = OrderedDict()

    ## met uncertainty
    mettaglist = [mname+shift for mname in metlist for shift in ["Up","Down"]]

    for tag in mettaglist:

        w = weightnorm.replace("mt_res", "mt_res_%s" %tag )\
                  .replace("met_pt", "met_%s_pt" %tag )
        sel = selnorm.replace("mt_res", "mt_res_%s" % tag )\
                     .replace("met_pt", "met_%s_pt" % tag )

        if tag == "MuonEnUp":
            sel = sel.replace("mu_pt_rc", "mu_pt_rc_up")
        if tag == "MuonEnDown":
            sel = sel.replace("mu_pt_rc", "mu_pt_rc_down")

        var = "mt_res_%s" %tag
        selection_list[tag] = (var, sel, w)

    ### muon and electron scale factors
    var = "mt_res"
    SFlist = SFlistel if ch=="el" else SFlistmu
    sftaglist = [sfname+"SF"+shift for sfname in SFlist for shift in ["UP","DN"]]
    for tag in sftaglist:
        sel = selnorm
        w = weightnorm.replace(tag[:-2], tag)
        selection_list[tag] = (var, sel, w)

    for shift in ["up","down"]:
        sel=selnorm
        w = weightnorm.replace("prefweight" , "prefweight%s" % shift )
        selection_list["pref"+shift] = (var, sel, w)

    #for shift in ["UP5", "UP10", "DN5", "DN10"]:
    for shift in ["UP5", "UP10",]:
        sel=selnorm
        w = weightnorm.replace("PUWeight" , "PUWeight%s" % shift )
        selection_list["PU"+shift] = (var, sel, w)

    # event weights (pdf)
    for i, shift in enumerate(eventweightlist):
        sel=selnorm
        w = weightnorm.replace("NLOWeight" , "NLOWeight*PDFWeights[%i]" % i )
        selection_list[shift] = (var, sel, w)

    return selection_list

def comp_tuples(keytuple, seltuple):

    if not (isinstance(keytuple,tuple) and isinstance(seltuple, tuple)):
        return False

    if len(keytuple)<len(seltuple):
        return False

    for i in range(len(seltuple)):

        if seltuple[i]==None:
            continue

        if keytuple[i]!=seltuple[i]:
            return False

    return True

def mask(a,b):
    c = tuple(a[i] for i , ib in enumerate(b) if ib == None)
    return c[0] if len(c) == 1 else c

def search_multidict(in_dict,selkey):
    ### search dictionary with ntuple keys
    ### (None,"hello") selects all entries where the second column is Hello
    ### roughly equivalent to ~~ dict[:,"hello"]
    return OrderedDict((mask(k,selkey), w) for k,w in in_dict.iteritems() if comp_tuples(k, selkey))

def multidict_tojson(filepath, indict, keymould = "%i_%g_%s"):
    transformed_dict = {keymould %k: v for k,v in indict.iteritems()}
    with open(filepath, "w") as fo:
        json.dump( transformed_dict, fo)

def multidict_tojson2(filepath, indict):
    ## expand into multidimensional dictionary
    transformed_dict = recdd()
    for (a,b,c,d), v in indict.viewitems():
        transformed_dict[a][b][c][d] = v
    with open(filepath, "w") as fo:
        json.dump( transformed_dict, fo)


def makeplots():
    with open(_JSONLOC) as fo:
        fm = json.load(fo)
    #ph_en_el = [fm["el"][m]["5.0"]["mean_PhotonEnDown"][0][0]/fm["el"][m]["5.0"]["norm"][0][0]*100-100 for m in masses]
    # NOTE fitted_masses[ch][mass][width][sys_type]:[0:mean,1:sigma][0:value, 1:sigma]
    plt.style.use("fivethirtyeight")

    syslist = [ "PhotonEn",
                "ElectronEn",
                "MuonEn",
                "UnclusteredEn",
                ]

    masses = fm["el"].keys()
    masses.sort(lambda x,y:int(float(x)-float(y)))

    mass = [float(m) for m in masses]
    for ch in ["el","mu"]:
        for w,width in [("w5","5.0"),("w0p01","0.01")]:
            fig=plt.figure()
            for sys in syslist:
                yup = [fm[ch][m][width]["mean_%sUp"%sys][0][0]/fm[ch][m][width]["norm"][0][0]*100-100 for m in masses]
                ydn = [fm[ch][m][width]["mean_%sDown"%sys][0][0]/fm[ch][m][width]["norm"][0][0]*100-100 for m in masses]
                plt.fill_between(mass,yup,ydn,alpha=0.2,label = sys)
            plt.legend()
            plt.savefig("%s/shifts_%s%i_%s_mean.png"%(options.outputDir,ch,options.year,w))
            plt.savefig("%s/shifts_%s%i_%s_mean.pdf"%(options.outputDir,ch,options.year,w))

            ## sigma shifts
            fig=plt.figure()
            for sys in syslist:
                yup = [fm[ch][m][width]["sigma_%sUp"%sys][1][0]/fm[ch][m][width]["norm"][1][0]*100-100 for m in masses]
                ydn = [fm[ch][m][width]["sigma_%sDown"%sys][1][0]/fm[ch][m][width]["norm"][1][0]*100-100 for m in masses]
                plt.fill_between(mass,yup,ydn,alpha=0.2,label = sys)
            plt.legend()
            plt.savefig("%s/shifts_%s%i_%s_sigma.png"%(options.outputDir,ch,options.year,w))
            plt.savefig("%s/shifts_%s%i_%s_sigma.pdf"%(options.outputDir,ch,options.year,w))


if options.plots:
    makeplots()
    sys.exit()

main()









