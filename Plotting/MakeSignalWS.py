#!/usr/bin/env python
import matplotlib.pyplot as plt
import re
import json
import uuid
from uncertainties import ufloat
from pprint import pprint
import pdb
def addparser(parser):
   parser.add_argument('--plots',  action='store_true', help='Plot fit parameter shifts' )
   parser.add_argument('--doSpecialFits',  action='store_true', help='Fit only specific systematics' )
execfile("MakeBase.py")
ROOT.PyConfig.IgnoreCommandLineOptions = True
ROOT.Math.MinimizerOptions.SetDefaultMaxFunctionCalls( 100000)
#ROOT.gSystem.Load('My_double_CB/RooDoubleCB_cc.so')
ROOT.gROOT.SetBatch()

_XMIN_M = 0
_XMAX_M = 3000
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

def hist_binning(mass):
    return (150, max( mass * 0.97*0.3, 100), min( mass *0.97*1.6,2500))

def fit_range(mass):
    return (max( mass * 0.97*0.6, 100), min( mass *0.97*1.4,2500))

def main() :
    sampManMuG = SampleManager( options.baseDirMuG, _TREENAME, filename=_FILENAME, lumi=-1)
    sampManElG = SampleManager( options.baseDirElG, _TREENAME, filename=_FILENAME, lumi=-1)
    sampManMuG.ReadSamples( _SAMPCONF )
    sampManElG.ReadSamples( _SAMPCONF )

    workspaces_to_save = {}

    kine_vars = { 'mt_res' : { 'var' : 'mt_res' , 'signal_binning' : hist_binning }, }

    lepg_samps = { 'mu' : sampManMuG, 'el' : sampManElG }

    for ch, man in lepg_samps.iteritems() :
        ## loop channel and sample manager
        for name, vardata in kine_vars.iteritems() :
            ## variables to be fitted
            print "name",name,"vardata", vardata

            ## call fit function
            make_signal_fits( man, workspaces_to_save=workspaces_to_save,
                               suffix='%s%i'%(ch,options.year), **vardata)

    multidict_tojson2(_JSONLOC, fitted_masses )

    for fileid, ws in workspaces_to_save.iteritems() :
            ws.writeToFile( '%s/%s/%s.root' %( options.dataDir, options.year, fileid ) )





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

        ### exclude certain samples
        if samp.name.count( 'MadGraph' ) == 0:
           continue
        if mass > 2000 or mass < 300:
           continue

        ## make full suffix
        full_suffix = "_".join(['MG', "M%d"%mass, 'W%s'%wid, suffix])

        ## make full selection string
        binning = signal_binning(mass)
        addition = " (%s > %d && %s < %d )" %(var, binning[1], var ,binning[2])
        cuttag, (full_sel_sr, weight) = defs.selectcutstring( mass , ch, addition )
        print full_sel_sr
        #weight = "NLOWeight"
        if options.year == 2018:
            weight = weight.replace("*prefweight","") ## no prefiring weight in 2018
        #weight = weight.replace("*jet_btagSF","") ## Yihui -- no jet_btagSF

        ## make RooRealVar for fit variable
        ## fit range is set here
        xvar = ROOT.RooRealVar( var, var, _XMIN_M , _XMAX_M)
        xvar.setRange("signal", *fit_range(mass))

        sample_params = {'mass' : mass, 'width' : width}

        workspace  = ROOT.RooWorkspace( 'wssignal_M%d_W%s_%s'%(mass, wid, ch) )

        lconf = {"labelStyle":str(options.year),
                 "extra_label":"%i %s" %(options.year, extra_label),
                 "extra_label_loc":(.12,.82)}

        ## make histogram
        sampMan.create_hist( samp, var, "(%s)*%s" %(full_sel_sr,weight), signal_binning(mass) )
        print "Integral: ", samp.hist.Integral()

        scale_norm = 1./samp.total_events_onthefly

        #pdb.set_trace()
        ## fit histogram
        fitman = fit_sample( samp.hist, xvar, workspace, full_suffix, sample_params, lconf, scale_norm = scale_norm)

        fitvals = fitman.get_parameter_vals()

        normval = (fitvals["cb_mass"], fitvals["cb_sigma"])
        fitted_masses[(ch,mass,width,"norm")] = normval

        # test simplest signal model -- Yihui
        nosyst = True
        if not nosyst:
            if not options.doSpecialFits:
                sel_odict = make_syssellist(var, full_sel_sr, weight, ch= ch)
                for tag, (v, s, w) in sel_odict.iteritems():
                    sampMan.create_hist( samp, v, "(%s)*%s" %(s,w), signal_binning(mass) )
                    ### fit with only mean floating
                    fitman = fit_sample( samp.hist, xvar, workspace, full_suffix+"_mean_"+tag,
                                         sample_params, lconf, fitvals, "mean", scale_norm = scale_norm)
                    fitvalsnew = fitman.get_parameter_vals()
                    fitted_masses[(ch, mass, width, "mean_%s" %tag)] = (fitvalsnew["cb_mass"], fitvalsnew["cb_sigma"])
                    #### fit with mean and sigma floating
                    #fitman = fit_sample( samp.hist, xvar, workspace, full_suffix+"_sigma_"+tag,
                    #                     sample_params, lconf, fitvals, "meansigma")
                    #fitvalsnew = fitman.get_parameter_vals()
                    #fitted_masses[(ch, mass, width, "sigma_%s" %tag)] = (fitvalsnew["cb_mass"], fitvalsnew["cb_sigma"])
            else:
                ## use a reduced list specified in make_syssel()
                sel_odict = make_syssel(var, full_sel_sr, weight, ch= ch)
                for tag, (v, s, w) in sel_odict.iteritems():
                    sampMan.create_hist( samp, v, "(%s)*%s" %(s,w), signal_binning(mass) )
                    ### fit with only mean floating
                    fitman = fit_sample( samp.hist, xvar, workspace, full_suffix+"_"+tag,
                                         sample_params, lconf, fitvals, "mean", scale_norm = scale_norm )
                    fitvalsnew = fitman.get_parameter_vals()
                    fitted_masses[(ch, mass, width, "mean_%s" %tag)] = (fitvalsnew["cb_mass"], fitvalsnew["cb_sigma"])


        ## save result
        #workspaces_to_save.update( { workspace.GetName() : workspace} )
        assert workspaces_to_save.get(workspace.GetName())==None, workspace.GetName()
        workspaces_to_save[ workspace.GetName() ] = workspace


        fitted_mass =  search_multidict(fitted_masses, (ch,mass,width,None))


        print "%-30s %10s %10s %6s %10s %6s" %("Systematics Name", "Mean(GeV)", "Shift", "Shift %%", "Sig shift", "Shift %%")
        for k,v in fitted_mass.iteritems():
            print "%-30s %10.1f %10.1f %6.1f%% %10.1f %6.0f%%" %(k, v[0][0], (v[0][0]-normval[0][0]), v[0][0]/normval[0][0]*100-100, v[1][0]-normval[1][0], v[1][0]/normval[1][0]*100-100,)

        ## list of all fitted mean
        meanlist = [v[0][0]for k,v in fitted_mass.iteritems() if "mean" in k]
        if len(meanlist):
            maxmean= max(meanlist)
            minmean= min(meanlist)

            # NOTE: different format from other values, ie no sigma or fit uncertainty
            fitted_masses[(ch, mass, width, "max")] = (maxmean, maxmean/normval[0][0])
            fitted_masses[(ch, mass, width, "min")] = (minmean, minmean/normval[0][0])
            print "%-30s %10.1f %10.1f %6.1f%%" % ("Max", maxmean, maxmean - normval[0][0], maxmean/normval[0][0]*100-100)
            print "%-30s %10.1f %10.1f %6.1f%%" % ("Min", minmean, minmean - normval[0][0], minmean/normval[0][0]*100-100)

    pprint(fitted_masses.keys())



def fit_sample( hist, xvar,  workspace , suffix, sample_params, label_config, usevals=None, fittype=None, scale_norm=None):

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

    print
    print "Parameter list:"
    for k, val in fitManager.fit_params.iteritems():
        print k,
        val.Print()

    fitManager.run_fit( Range="signal", Strategy=2, Save=True, SumW2Error=True)
    fitManager.get_results( workspace, scale_norm=scale_norm )

    ## NOTE uncomment this to make a flat mass shift (default 0.5%) for all samples
    #if not fittype: fitManager.shifted_dscb( workspace )

    canv = fitManager.draw( subplot = "pull", paramlayout = (0.12,0.5,0.78),
                            useOldsetup = True, label_config = label_config)

    canv.Print("%s/%s.pdf" %(options.outputDir, suffix) )
    canv.Print("%s/%s.png" %(options.outputDir, suffix) )
    canv.Print("%s/%s.C"   %(options.outputDir, suffix) )

    print "************"
    print " RooFitResult Status: %d"%fitManager.fitresult.status()
    print "************"


    fitmlist.append(fitManager)
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

@f_Obsolete
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
        sel = selnorm.replace("mt_res", "mt_res_%s" % tag )
        
        if any(x in tag for x in ['Muon', 'Electron', 'Photon']):
            sel = sel.replace("met_pt", "met_%sByHand_pt" % tag )
        else:
            sel = sel.replace("met_pt", "met_%s_pt" % tag )

        if tag == "MuonEnUp":
            sel = sel.replace("mu_pt_rc", "mu_pt_rc_up")
        if tag == "MuonEnDown":
            sel = sel.replace("mu_pt_rc", "mu_pt_rc_down")

        if tag == "PhotonEnUp":
            sel = sel.replace("ph_pt", "ph_pt_ScaleUp")
        if tag == "PhotonEnDown":
            sel = sel.replace("ph_pt", "ph_pt_ScaleDown")

        if tag == "ElectronEnUp":
            sel = sel.replace("el_pt", "el_pt_ScaleUp")
        if tag == "ElectronEnDown":
            sel = sel.replace("el_pt", "el_pt_ScaleDown")

        var = "mt_res_%s" %tag
        selection_list[tag] = (var, sel, w)

#    ### muon and electron scale factors
#    var = "mt_res"
#    SFlist = SFlistel if ch=="el" else SFlistmu
#    sftaglist = [sfname+"SF"+shift for sfname in SFlist for shift in ["UP","DN"]]
#    for tag in sftaglist:
#        sel = selnorm
#        w = weightnorm.replace(tag[:-2], tag)
#        selection_list[tag] = (var, sel, w)

#    for shift in ["up","down"]:
#        sel=selnorm
#        w = weightnorm.replace("prefweight" , "prefweight%s" % shift )
#        selection_list["pref"+shift] = (var, sel, w)

#    #for shift in ["UP5", "UP10", "DN5", "DN10"]:
#    for shift in ["UP5", "UP10",]:
#        sel=selnorm
#        w = weightnorm.replace("PUWeight" , "PUWeight%s" % shift )
#        selection_list["PU"+shift] = (var, sel, w)
#
#    # event weights (pdf)
#    for i, shift in enumerate(eventweightlist):
#        sel=selnorm
#        w = weightnorm.replace("NLOWeight" , "NLOWeight*PDFWeights[%i]" % i )
#        selection_list[shift] = (var, sel, w)

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
        print "save to %s" %filepath


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
    syslist = [] # I don't need syst plot -- Yihui
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

            # sigma shifts
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


print "Script Sucessfully Ran"


