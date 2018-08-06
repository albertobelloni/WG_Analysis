import ROOT
ROOT.PyConfig.IgnoreCommandLineOptions = True
import re
import os
import uuid
import math
import pickle
import selection_defs as defs
from uncertainties import ufloat
from FitManager import FitManager
#ROOT.TVirtualFitter.SetMaxIterations( 100000 )
ROOT.Math.MinimizerOptions.SetDefaultMaxFunctionCalls( 100000)

from SampleManager import SampleManager
from argparse import ArgumentParser
parser = ArgumentParser()

parser.add_argument('--baseDirMuG',      default=None,           dest='baseDirMuG',         required=False, help='Path to signal samples in muon channel')
parser.add_argument('--baseDirElG',      default=None,           dest='baseDirElG',         required=False, help='Path to signal samples in muon channel')
parser.add_argument('--outputDir',      default=None,           dest='outputDir',         required=False, help='Output directory to write histograms')
parser.add_argument('--useRooFit',       default=False,    action='store_true',      dest='useRooFit', required=False, help='Make fits using roostats' )
parser.add_argument('--doSignal',       default=False,    action='store_true',      dest='doSignal', required=False, help='make signal fits' )
parser.add_argument('--doWGamma',       default=False,    action='store_true',      dest='doWGamma', required=False, help='make wgamma fits' )
parser.add_argument('--doTop',          default=False,    action='store_true',      dest='doTop', required=False, help='make top fits' )
parser.add_argument('--doZGamma',          default=False,    action='store_true',      dest='doZGamma', required=False, help='make ZGamma fits' )
parser.add_argument('--doWJets',       default=False,     action='store_true',     dest='doWJets', required=False, help='make w+jets fits' )
parser.add_argument('--doEleFake',       default=False,     action='store_true',     dest='doEleFake', required=False, help='make electron fake fits' )
parser.add_argument('--doClosure',       default=False,   action='store_true',       dest='doClosure', required=False, help='make closure tests' )

options = parser.parse_args()


_TREENAME = 'UMDNTuple/EventTree'
_FILENAME = 'tree.root'
_XSFILE   = 'cross_sections/photon15.py'
_LUMI     = 36000
_BASEPATH = '/home/jkunkle/usercode/Plotting/LimitSetting/'
_SAMPCONF = 'Modules/Resonance.py'


ROOT.gROOT.SetBatch(False)
if options.outputDir is not None :
    ROOT.gROOT.SetBatch(True)
    if not os.path.isdir( options.outputDir ) :
        os.makedirs( options.outputDir )

def main() :

    sampManMuG = SampleManager( options.baseDirMuG, _TREENAME, filename=_FILENAME, xsFile=_XSFILE, lumi=_LUMI )
    sampManElG = SampleManager( options.baseDirElG, _TREENAME, filename=_FILENAME, xsFile=_XSFILE, lumi=_LUMI )

    sampManMuG.ReadSamples( _SAMPCONF )
    sampManElG.ReadSamples( _SAMPCONF )

    sampManMuG.outputs = {}
    sampManElG.outputs = {}

    sel_base_mu = 'mu_pt30_n==1 && mu_n==1'
    sel_base_el = 'el_pt30_n==1 && el_n==1'

    sel_jetveto_mu = sel_base_mu + ' && jet_n == 0 '
    sel_jetveto_el = sel_base_el + ' && jet_n == 0 '

    #eta_cuts = ['EB', 'EE']
    eta_cuts = ['EB']

    workspaces_to_save = {}

    xmin_m = 60
    xmax_m = 4000
    bin_width_m = 20

    xmin_pt = xmin_m/2
    if xmin_pt < 50 :
        xmin_pt = 50
    xmax_pt = xmax_m/2
    bin_width_pt = bin_width_m/2.

    binning_m = ((xmax_m-xmin_m)/bin_width_m, xmin_m, xmax_m)

    binning_pt = ( (xmax_pt - xmin_pt )/bin_width_pt, xmin_pt, xmax_pt )

    xvar_m = ROOT.RooRealVar( 'x_m', 'x_m',xmin_m , xmax_m)

    xvar_pt = ROOT.RooRealVar( 'x_pt', 'x_pt', xmin_pt, xmax_pt )

    signal_binning_m = { 200 : ( (xmax_m)/3 , 0, xmax_m ),
                         250 : ( (xmax_m)/3 , 0, xmax_m ),
                         300 : ( (xmax_m)/5 , 0, xmax_m ),
                         350 : ( (xmax_m)/5 , 0, xmax_m ),
                         400 : ( (xmax_m)/5 , 0, xmax_m ),
                         450 : ( (xmax_m)/5 , 0, xmax_m ),
                         500 : ( (xmax_m)/10 , 0, xmax_m ),
                         600 : ( (xmax_m)/10, 0, xmax_m ),
                         700 : ( (xmax_m)/10, 0, xmax_m ),
                         800 : ( (xmax_m)/15, 0, xmax_m ),
                         900 : ( (xmax_m)/15, 0, xmax_m ),
                        1000 : ( (xmax_m)/15, 0, xmax_m ),
                        1200 : ( (xmax_m)/20, 0, xmax_m ),
                        1400 : ( (xmax_m)/20, 0, xmax_m ),
                        1600 : ( (xmax_m)/20, 0, xmax_m ),
                        1800 : ( (xmax_m)/20, 0, xmax_m ),
                        2000 : ( (xmax_m)/20, 0, xmax_m ),
                       }

    signal_binning_pt = {}
    for mass, binning in signal_binning_m.iteritems() :
        pt_min = binning[1]/2.
        if pt_min < 50 :
            pt_min = 50
        signal_binning_pt[mass] = ( binning[0]/2., pt_min, binning[2]/2. )



    kine_vars = { #'mt_incl_lepph_z' : { 'var' : 'mt_lep_met_ph'   , 'xvar' : xvar_m  , 'binning' : binning_m, 'signal_binning' : signal_binning_m },
                  #'m_incl_lepph_z'  : { 'var' : 'm_lep_met_ph'    , 'xvar' : xvar_m  , 'binning' : binning_m, 'signal_binning' : signal_binning_m },
                  ##'mt_rotated'      : { 'var' : 'mt_rotated'      , 'xvar' : xvar_m  , 'binning' : binning_m, 'signal_binning' : signal_binning_m },
                  'mt_fulltrans'    : { 'var' : 'mt_res'          , 'xvar' : xvar_m  , 'binning' : binning_m, 'signal_binning' : signal_binning_m },
                  #'mt_constrwmass'  : { 'var' : 'recoM_lep_nu_ph' , 'xvar' : xvar_m  , 'binning' : binning_m, 'signal_binning' : signal_binning_m },
                  #'ph_pt'           : { 'var' : 'ph_pt[0]'        , 'xvar' : xvar_pt , 'binning' : binning_pt, 'signal_binning' : signal_binning_pt },
                }

    selections = { 'base'    : { 
                                'mu' : {'selection' : sel_base_mu }, 
                                 #'el' : { 'selection' : sel_base_el }, 
                               },
                   #'jetVeto' : { 'mu' : {'selection' : sel_jetveto_mu }, 
                   #              'el' : { 'selection' : sel_jetveto_el } ,
                   #            },
                 }

    workspace_signal   = ROOT.RooWorkspace( 'workspace_signal' )

    lepg_samps = { 'mu' : sampManMuG, 'el' : sampManElG }

    for seltag, chdic in selections.iteritems() : 

        for ch, seldic in chdic.iteritems() : 
                                    
            for name, vardata in kine_vars.iteritems() :

                make_signal_fits( lepg_samps[ch], seldic['selection'], eta_cuts, vardata['var'], vardata['xvar'], vardata['signal_binning'], workspace_signal, suffix='%s_%s_%s'%(ch,name,seltag ) )

    if options.outputDir is not None :

        workspace_signal.writeToFile( '%s/%s.root' %( options.outputDir,workspace_signal.GetName() ) )

        for fileid, ws_list in workspaces_to_save.iteritems() :
            for idx, ws in enumerate(ws_list) :
                if idx == 0 :
                    recreate = True
                else  :
                    recreate = False

                ws.writeToFile( '%s/workspace_%s.root' %( options.outputDir, fileid ), recreate )

        for key, can in sampManMuG.outputs.iteritems() :
            can.SaveAs('%s/%s.pdf' %( options.outputDir, key ) )
        for key, can in sampManElG.outputs.iteritems() :
            can.SaveAs('%s/%s.pdf' %( options.outputDir, key ) )


def make_signal_fits( sampMan, sel_base, eta_cuts, plot_var, xvar, binning, workspace, suffix ) : 

    sampMan.clear_hists()

    for samp in sampMan.get_samples(isSignal=True ) :

        print 'Sample = ', samp.name


        res = re.match('(MadGraph|Pythia)ResonanceMass(\d+)_.*', samp.name )
        if res is None :
            print 'Could not interpret path ', samp.name
        else :

            mass = float(res.group(2))

            if samp.name.count( 'width0p01' ) :
                width = 0.0001
            else :
                res2 = re.match('(MadGraph|Pythia)ResonanceMass(\d+)_width(\d)', samp.name )
                width = float(res2.group(3))/100.

        if mass != 450 : 
            continue

        ph_selection_sr = '%s==1' %defs.get_phid_selection('all')
        ph_idx_sr =  defs.get_phid_idx( 'all' )
        print binning[mass]
        addtl_cuts_sr = 'ph_pt[%s] > 50  && %s > %f && %s < %f ' %(ph_idx_sr, plot_var, binning[mass][1], plot_var, binning[mass][2] )

        xvar.setBins(10000,'cache')
        xvar.setMin('cache',-100)
        xvar.setMax('cache',1500)

        for ieta in eta_cuts :

            full_suffix = '%s_%s_%s' %(samp.name, suffix, ieta)

            eta_str_sr = 'ph_Is%s[%s]' %( ieta, ph_idx_sr )

            full_sel_sr    = ' && '.join( [sel_base, ph_selection_sr, eta_str_sr, addtl_cuts_sr] )

            #hist_sr    = clone_sample_and_draw( sampMan, sampname, plot_var, full_sel_sr, binning )
            sampMan.create_hist( samp, plot_var, full_sel_sr, binning[mass] ) 

            hist_sr = samp.hist

            integral = hist_sr.Integral()

            #hist_sr.Scale( 1.0/integral )

            #datahist = ROOT.RooDataHist( 'srhist_%s' %full_suffix, 'srhist', ROOT.RooArgList(xvar), hist_sr)

            #histpdf = ROOT.RooHistPdf( 'srhistpdf_%s' %(full_suffix), 'srhistpdf' , ROOT.RooArgSet( xvar), datahist, 3 )

            fit_max = mass*1.1
            fit_min = mass/1.8
            if mass >= 1000 :
                fit_max = mass*1.05
                fit_min = mass*0.7

            xvar.setMin( fit_min )
            xvar.setMax( fit_max )


            fitManager = FitManager( 'bwxcb', 0, samp.name, hist_sr, plot_var, ieta, xvar, full_suffix, True, 
                                    sample_params={'mass' : mass, 'width' : width}, )

            fitManager.fit_histogram(workspace )
            #fitManager.save_fit( sampMan, workspace, stats_pos='left' )

            iter_managers = []
            iter_managers.append( fitManager )

            saved_result = False
            for i in range( 0, 4 ) :
            #for i in [0.5, 0.3, 0.2, 0.1, 0.05] :

                print 'GOTHERE1'
                iter_managers.append(FitManager( 'bwxcb', 0, samp.name, hist_sr, plot_var, ieta, xvar, full_suffix, True, 
                                        sample_params={'mass' : mass, 'width' : width}, ))

                print 'GOTHERE2'
                cv_sigma = iter_managers[-2].fit_params['cb_sigma'].getValV()
                lo_sigma = iter_managers[-2].fit_params['cb_sigma'].getErrorLo()
                hi_sigma = iter_managers[-2].fit_params['cb_sigma'].getErrorHi()
                cv_power = iter_managers[-2].fit_params['cb_power'].getValV()
                lo_power = iter_managers[-2].fit_params['cb_power'].getErrorLo()
                hi_power = iter_managers[-2].fit_params['cb_power'].getErrorHi()
                cv_mass  = iter_managers[-2].fit_params['cb_mass'].getValV()
                lo_mass  = iter_managers[-2].fit_params['cb_mass'].getErrorLo()
                hi_mass  = iter_managers[-2].fit_params['cb_mass'].getErrorHi()

                err_sigma = hi_sigma/cv_sigma
                err_power = hi_power/cv_power
                err_mass = hi_mass/cv_mass

                #new_lim_sigma = ( cv_sigma, cv_sigma*(1-i), cv_sigma*(1+i)) 
                #new_lim_power = ( cv_power, cv_power*(1-i), cv_power*(1+i) ) 
                #new_lim_mass  = ( cv_mass, cv_mass*(1-i), cv_mass*(1+i)    ) 

                new_lim_sigma = ( cv_sigma, cv_sigma+lo_sigma, cv_sigma+hi_sigma) 
                new_lim_power = ( cv_power, cv_power+lo_power, cv_power+hi_power ) 
                new_lim_mass  = ( cv_mass,  cv_mass+lo_mass, cv_mass+hi_mass    ) 

                #if cv_sigma < 0 :
                #    new_lim_sigma = ( new_lim_sigma[0], new_lim_sigma[2], new_lim_sigma[1]) 
                #if cv_power < 0 :
                #    new_lim_power = ( new_lim_power[0], new_lim_power[2], new_lim_power[1]) 
                #if cv_mass < 0 :
                #    new_lim_mass = ( new_lim_mass[0], new_lim_mass[2], new_lim_mass[1] ) 

                print 'NEW DEFAULTS'
                print new_lim_sigma
                print new_lim_power
                print new_lim_mass

                iter_managers[-1].set_vals('cb_sigma', mass, new_lim_sigma )
                iter_managers[-1].set_vals('cb_power', mass, new_lim_power )
                iter_managers[-1].set_vals('cb_mass',  mass, new_lim_mass  )

                print 'GOTHERE3'
                iter_managers[-1].fit_histogram(  )
                print 'GOTHERE4'

                cv_sigma_new = iter_managers[-1].fit_params['cb_sigma'].getValV()
                lo_sigma_new = iter_managers[-1].fit_params['cb_sigma'].getErrorLo()
                hi_sigma_new = iter_managers[-1].fit_params['cb_sigma'].getErrorHi()
                cv_power_new = iter_managers[-1].fit_params['cb_power'].getValV()
                lo_power_new = iter_managers[-1].fit_params['cb_power'].getErrorLo()
                hi_power_new = iter_managers[-1].fit_params['cb_power'].getErrorHi()
                cv_mass_new  = iter_managers[-1].fit_params['cb_mass'].getValV()
                lo_mass_new  = iter_managers[-1].fit_params['cb_mass'].getErrorLo()
                hi_mass_new  = iter_managers[-1].fit_params['cb_mass'].getErrorHi()

                err_sigma_new = hi_sigma_new/cv_sigma_new
                err_power_new = hi_power_new/cv_power_new
                err_mass_new = hi_mass_new/cv_mass_new

                print 'Sigma : Previous error = %f, new error = %f' %( err_sigma, err_sigma_new )
                print 'Power : Previous error = %f, new error = %f' %( err_power, err_power_new )
                print 'Mass : Previous error = %f, new error = %f' %( err_mass, err_mass_new )

                print 'GOTHERE5'
                # if we get worse results with the new fit, then use the previous one
                if math.fabs(err_sigma_new) > math.fabs(err_sigma) or math.fabs(err_power_new) > math.fabs(err_power) or math.fabs(err_mass_new) > math.fabs(err_mass) :
                    print 'GOTHERE6'
                    iter_managers[-2].save_fit( sampMan, workspace, stats_pos='left' )
                    print 'GOTHERE7'
                    saved_result = True
                    break

            # if we haven't saved the fit yet, then the best
            # version is the latest
            if not saved_result :
                print 'GOTHERE8'
                iter_managers[-1].save_fit(sampMan, workspace, stats_pos='left' )
                print 'GOTHERE9'



            #cb_sigma.setVal( cb_sigma.getValV() )
            #cb_sigma.setMin( cb_sigma.getValV() - cb_sigma.getErrorLo() )
            #cb_sigma.setMin( cb_sigma.getValV() + cb_sigma.getErrorHi() )
            #model.fitTo( datahist, ROOT.RooFit.Range( fit_min, fit_max) ,ROOT.RooFit.SumW2Error(True), ROOT.RooCmdArg( 'Strategy', 3 ) )

            ## Construct unbinned likelihood of model w.r.t. data
            #nll = model.createNLL(datahist) ;
            #raw_input('cont1')
            ##// I n t e r a c t i v e   m i n i m i z a t i o n ,   e r r o r   a n a l y s i s
            ##// -------------------------------------------------------------------------------
            ##// Create MINUIT interface object
            #m = ROOT.RooMinimizer(nll) 
            #raw_input('cont2')
            ##// Activate verbose logging of MINUIT parameter space stepping
            #m.setVerbose(ROOT.kTRUE) 
            #raw_input('cont3')
            ##// Call MIGRAD to minimize the likelihood
            #m.migrad() 
            #raw_input('cont4')
            ##// Print values of all parameters, that reflect values (and error estimates)
            ##// that are back propagated from MINUIT
            #model.getParameters(ROOT.RooArgSet(xvar)).Print("s") 
            #raw_input('cont5')
            ##// Disable verbose logging
            #m.setVerbose(ROOT.kFALSE) 
            #raw_input('cont6')
            ##// Run HESSE to calculate errors from d2L/dp2
            #m.hesse() 
            #raw_input('cont7')
            ##// Print value (and error) of sigma_g2 parameter, that reflects
            ##// value and error back propagated from MINUIT
            #cb.Print() 
            #raw_input('cont8')
            #bw.Print() 
            #raw_input('cont9')
            #cb_cut.Print()
            #raw_input('cont10')
            #cb_sigma.Print()
            #raw_input('cont11')
            #cb_power.Print()
            #raw_input('cont12')
            #cb_m0.Print()
            #raw_input('cont13')
            ##// Run MINOS on sigma_g2 parameter only
            #m.minos(ROOT.RooArgSet(cb_power)) 
            #raw_input('cont14')
            #cb_power.Print()
            #raw_input('cont15')
            ##// Print value (and error) of sigma_g2 parameter, that reflects
            ##// value and error back propagated from MINUIT
            #sigma_g2.Print() ;


            #can = ROOT.TCanvas( 'signal_can_%s' %( full_suffix ), '' )
            #frame = xvar.frame(fit_min, fit_max) 
            #datahist.plotOn(frame)
            #model.plotOn( frame )
            #model.paramOn(frame, ROOT.RooFit.ShowConstants(True), ROOT.RooFit.Layout(0.1,0.5,0.9), ROOT.RooFit.Format("NEU",ROOT.RooFit.AutoPrecision(3)));
            #frame.Draw()

            #frame = xvar.frame()

            #datahist.plotOn( frame )
            #histpdf.plotOn( frame )

            ##frame.Draw()
            #sampMan.outputs[can.GetName()] = can

            #norm_var = ROOT.RooRealVar( 'srhist_%s_norm' %( full_suffix ), 'signal normalization', integral )

            #xs_var = ROOT.RooRealVar( 'cross_section_%s' %full_suffix, 'Cross section', samp.cross_section )
            #tot_evt = ROOT.RooRealVar( 'total_events_%s' %full_suffix, 'Total Events', samp.total_events)
            #scale = ROOT.RooRealVar( 'scale_%s' %full_suffix, 'Scale', samp.scale)

            #getattr(workspace, 'import' )(model)
            #getattr(workspace, 'import' )(datahist)
            #getattr(workspace, 'import' )(norm_var)
            #getattr(workspace, 'import' )(xs_var)
            #getattr(workspace, 'import' )(tot_evt)
            #getattr(workspace, 'import' )(scale)


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

main()

    




    
    




