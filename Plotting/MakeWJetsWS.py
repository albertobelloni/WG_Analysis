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

parser.add_argument('--baseDirMuGNoId',      default=None,           dest='baseDirMuGNoId',         required=False, help='Path to muon base directory')
parser.add_argument('--baseDirElGNoId',      default=None,           dest='baseDirElGNoId',         required=False, help='Path to electron base directory')
parser.add_argument('--outputDir',      default=None,           dest='outputDir',         required=False, help='Output directory to write histograms')
parser.add_argument('--useRooFit',       default=False,    action='store_true',      dest='useRooFit', required=False, help='Make fits using roostats' )
parser.add_argument('--doClosure',       default=False,   action='store_true',       dest='doClosure', required=False, help='make closure tests' )

options = parser.parse_args()

_TREENAME = 'UMDNTuple/EventTree'
_FILENAME = 'tree.root'
_XSFILE   = 'cross_sections/photon15.py'
_LUMI     = 36000
_BASEPATH = '/home/friccita/WGamma/WG_Analysis/Plotting/LimitSetting/'
_SAMPCONF = 'Modules/Resonance.py'


def get_cut_defaults( shape_var, ieta ) :

    cut_defaults = {'sigmaIEIE' : { 'EB' : ( 0.012, 0.02 ), 'EE' : ( 0.0, 0.0 ) },
                    'chIso'     : { 'EB' : ( 4, 10 ),       'EE' : (4, 10) },
                   }

    return cut_defaults[shape_var][ieta]


ROOT.gROOT.SetBatch(False)
if options.outputDir is not None :
    ROOT.gROOT.SetBatch(True)
    if not os.path.isdir( options.outputDir ) :
        os.makedirs( options.outputDir )

def main() :

    sampManMuGNoId = SampleManager( options.baseDirMuGNoId, _TREENAME, filename=_FILENAME, xsFile=_XSFILE, lumi=_LUMI )
    sampManElGNoId = SampleManager( options.baseDirElGNoId, _TREENAME, filename=_FILENAME, xsFile=_XSFILE, lumi=_LUMI )

    sampManMuGNoId.ReadSamples( _SAMPCONF )
    sampManElGNoId.ReadSamples( _SAMPCONF )

    sampManMuGNoId.outputs = {}
    sampManElGNoId.outputs = {}

    sel_base_mu = 'mu_pt30_n==1 && mu_n==1'
    sel_base_el = 'el_pt30_n==1 && el_n==1'

    #eta_cuts = ['EB', 'EE']
    eta_cuts = ['EB']

    workspaces_to_save = {}

    xmin_m = 160
    xmax_m = 2000
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

    kine_vars = { #'mt_incl_lepph_z' : { 'var' : 'mt_lep_met_ph'   , 'xvar' : xvar_m  , 'binning' : binning_m},
                  #'m_incl_lepph_z'  : { 'var' : 'm_lep_met_ph'    , 'xvar' : xvar_m  , 'binning' : binning_m},
                  'mt_fulltrans'    : { 'var' : 'mt_res'          , 'xvar' : xvar_m  , 'binning' : binning_m},
                  #'mt_constrwmass'  : { 'var' : 'recoM_lep_nu_ph' , 'xvar' : xvar_m  , 'binning' : binning_m},
                  #'ph_pt'           : { 'var' : 'ph_pt[0]'        , 'xvar' : xvar_pt , 'binning' : binning_pt},
                }

    selections = { 'base'    : { 
                                'mu' : {'selection' : sel_base_mu }, 
                   #             'el' : { 'selection' : sel_base_el }, 
                               },
                   #'jetVeto' : { 'mu' : {'selection' : sel_jetveto_mu }, 
                   #              'el' : { 'selection' : sel_jetveto_el } ,
                   #            },
                 }

    workspace_signal   = ROOT.RooWorkspace( 'workspace_signal' )
    workspace_wgamma   = ROOT.RooWorkspace( 'workspace_wgamma' )
    workspace_wgammalo = ROOT.RooWorkspace( 'workspace_wgammalo' )
    workspace_top      = ROOT.RooWorkspace( 'workspace_top' )
    workspace_zgamma   = ROOT.RooWorkspace( 'workspace_zgamma' )
    wjets              = ROOT.RooWorkspace( 'workspace_wjets' )
    elefake            = ROOT.RooWorkspace( 'elefake' )

    for seltag, chdic in selections.iteritems() : 

        for ch, seldic in chdic.iteritems() : 

            for name, vardata in kine_vars.iteritems() :
                                    
                print 'WJets fit for data'
                make_wjets_fit( sampManMuGNoId, 'Data', seldic['selection'], 'EB', vardata['var'], 'chIso', 'sigmaIEIE', vardata['binning'], vardata['xvar'], suffix='wjets_%s_EB_%s_%s' %(ch,name,seltag), closure=False, workspace=wjets)

                if options.doClosure :

                    print 'WJets fit for MC: closure'
                    closure_res_mu = make_wjets_fit( sampManMuGNoId, 'Wjets', seldic['selection'], 'EB', vardata['var'], 'chIso', 'sigmaIEIE', vardata['binning'], vardata['xvar'], suffix='closure_%s_EB_%s_%s' %( ch,name,seltag ), closure=True )
                    closure_res_mu = make_wjets_fit( sampManMuGNoId, 'Wgamma', seldic['selection'], 'EB', vardata['var'], 'chIso', 'sigmaIEIE', vardata['binning'], vardata['xvar'], suffix='closure_%s_EB_%s_%s' %( ch,name,seltag ), closure=True )
                    closure_res_mu = make_wjets_fit( sampManMuGNoId, 'TTbar_SingleLep', seldic['selection'], 'EB', vardata['var'], 'chIso', 'sigmaIEIE', vardata['binning'], vardata['xvar'], suffix='closure_%s_EB_%s_%s' %( ch,name,seltag ), closure=True )


    if options.outputDir is not None :

        wjets.writeToFile( '%s/%s.root' %( options.outputDir,wjets.GetName() ) )

        for fileid, ws_list in workspaces_to_save.iteritems() :
            for idx, ws in enumerate(ws_list) :
                if idx == 0 :
                    recreate = True
                else  :
                    recreate = False

                ws.writeToFile( '%s/workspace_%s.root' %( options.outputDir, fileid ), recreate )

        outputFile = ROOT.TFile('%s/outfile_%s.root' %( options.outputDir, wjets.GetName() ),'recreate')
        for key, can in sampManMuGNoId.outputs.iteritems() :
            can.Write( '%s' %(key) )
        for can in sampManElGNoId.outputs.iteritems() :
            can.Write( '%s' %(key) )

        #for key, can in sampManMuGNoId.outputs.iteritems() :
        #    can.SaveAs('%s/%s.pdf' %( options.outputDir, key ) )
        #for key, can in sampManElGNoId.outputs.iteritems() :
        #    can.SaveAs('%s/%s.pdf' %( options.outputDir, key ) )




def make_wjets_fit( sampMan, sample, sel_base, eta_cut, plot_var, shape_var, num_var, binning, xvar, suffix='', closure=False, workspace=None) :

    #---------------------------------------
    # Get the base selection for each region
    #---------------------------------------
    ph_selection_sr    = '%s==1' %defs.get_phid_selection('medium')
    ph_selection_den   = '%s==1'%defs.get_phid_selection( num_var, shape_var )
    ph_selection_num   = '%s==1' %defs.get_phid_selection( num_var )
    ph_selection_shape = '%s==1' %defs.get_phid_selection( shape_var )
    #ph_selection_ABCD  = '%s==1' %defs.get_phid_selection('all')

    ph_idx_sr =  defs.get_phid_idx( 'medium' )
    ph_idx_den = defs.get_phid_idx( num_var, shape_var )
    ph_idx_num = defs.get_phid_idx( num_var )
    ph_idx_shape = defs.get_phid_idx( shape_var )
    #ph_idx_ABCD = defs.get_phid_idx('all')

    xmin = xvar.getMin()
    xmax = xvar.getMax()

    #---------------------------------------
    # Add eta cuts, (IsEB, IsEE)
    #---------------------------------------
    eta_str_shape = 'ph_Is%s[%s]' %( eta_cut, ph_idx_shape )
    eta_str_den = 'ph_Is%s[%s]' %( eta_cut, ph_idx_den)
    eta_str_num = 'ph_Is%s[%s]' %( eta_cut, ph_idx_num )
    eta_str_sr = 'ph_Is%s[%s]' %( eta_cut, ph_idx_sr )
    #eta_str_ABCD = 'ph_Is%s[%s]' %( eta_cut, ph_idx_ABCD )

    #---------------------------------------
    # Add additional cuts, mainly restricting
    # the fitted variable to the plotting limits
    #---------------------------------------
    addtl_cuts_sr = 'ph_pt[%s] > 50 && %s > %d && %s < %d '     %( ph_idx_sr, plot_var, xmin, plot_var, xmax )
    addtl_cuts_den = 'ph_pt[%s] > 50 && %s > %d && %s < %d  '   %( ph_idx_den, plot_var, xmin, plot_var, xmax )
    addtl_cuts_num = 'ph_pt[%s] > 50 && %s > %d && %s < %d  '   %( ph_idx_num, plot_var, xmin, plot_var, xmax )
    addtl_cuts_shape = 'ph_pt[%s] > 50 && %s > %d && %s < %d  ' %( ph_idx_shape, plot_var, xmin, plot_var, xmax )
    #addtl_cuts_ABCD = 'ph_pt[%s] > 50 && %s > %d && %s < %d  ' %( ph_idx_ABCD, plot_var, xmin, plot_var, xmax )


    #---------------------------------------
    # Get the cuts that define the photon
    # sideband regions
    #---------------------------------------
    cut_str_base = ' {var}[{idx}] > {val_low} && {var}[{idx}] < {val_high}'

    cut_var_shape = defs.get_phid_cut_var( shape_var )
    cut_var_num = defs.get_phid_cut_var( num_var )

    cut_vals_shape = get_cut_defaults( shape_var, eta_cut )
    cut_vals_num = get_cut_defaults( num_var, eta_cut )

    cut_str_shape = cut_str_base.format(var=cut_var_shape, idx=ph_idx_shape, val_low=cut_vals_shape[0], val_high=cut_vals_shape[1] )
    cut_str_num = cut_str_base.format(var=cut_var_num, idx=ph_idx_num, val_low=cut_vals_num[0], val_high=cut_vals_num[1] )

    cut_str_den_1 = cut_str_base.format(var=cut_var_shape, idx=ph_idx_den, val_low=cut_vals_shape[0], val_high=cut_vals_shape[1] )
    cut_str_den_2 = cut_str_base.format(var=cut_var_num, idx=ph_idx_den, val_low=cut_vals_num[0], val_high=cut_vals_num[1] )

    cut_str_den = cut_str_den_1 + ' && ' + cut_str_den_2

    #---------------------------------------
    # put the cuts together
    #---------------------------------------
    full_sel_shape = ' && '.join( [sel_base, ph_selection_shape, eta_str_shape, addtl_cuts_shape, cut_str_shape ] )
    full_sel_num   = ' && '.join( [sel_base, ph_selection_num, eta_str_num, addtl_cuts_num, cut_str_num] )
    full_sel_den   = ' && '.join( [sel_base, ph_selection_den, eta_str_den, addtl_cuts_den, cut_str_den] )
    full_sel_sr    = ' && '.join( [sel_base, ph_selection_sr, eta_str_sr, addtl_cuts_sr] )
    #full_sel_ABCD  = ' && '.join( [sel_base, ph_selection_ABCD, eta_str_ABCD, addtl_cuts_ABCD] )

    label_shape = 'shape_%s_%s' %(sample,suffix)
    label_num   = 'num_%s_%s' %(sample,suffix)
    label_den   = 'den_%s_%s' %(sample,suffix)
    label_sr    = 'sr_%s_%s' %(sample,suffix)

    if workspace is None :
        ws = ROOT.RooWorkspace( 'ws') 
    else :
        ws = workspace

    jet_var = 'leadjet_pt' # 0 to 640 in bins of 5
    jet_binning = (128,0.,640.)
    subjet_var = 'subljet_pt' # 0 to 380 in bins of 3.8
    subjet_binning = (100,0.,380.)
    ht_var = 'trueht' # 0 to 7000 in bins of 50
    ht_binning = (140,0.,7000.)

    ABCD_var = 'ph_sigmaIEIE:ph_chIsoCorr'
    ABCD_binning = (120,0.,12.,50,0.,0.05)

    #chIsovar   = 'ph_chIso'
    #sigIEIEvar = 'ph_sigmaIEIE'

    chIso_B_var     = 'ph_chIsoCorr[ptSorted_ph_mediumNoChIso_idx[0]]'
    sigIEIE_B_var = 'ph_sigmaIEIE[ptSorted_ph_mediumNoChIso_idx[0]]'
    chIso_C_var     = 'ph_chIsoCorr[ptSorted_ph_mediumNoSIEIE_idx[0]]'
    sigIEIE_C_var = 'ph_sigmaIEIE[ptSorted_ph_mediumNoSIEIE_idx[0]]'
    chIso_D_var     = 'ph_chIsoCorr[ptSorted_ph_mediumNoSIEIENoChIso_idx[0]]'
    sigIEIE_D_var = 'ph_sigmaIEIE[ptSorted_ph_mediumNoSIEIENoChIso_idx[0]]'

    twoD_B_var = 'ph_sigmaIEIE[ptSorted_ph_mediumNoChIso_idx[0]]:ph_chIsoCorr[ptSorted_ph_mediumNoChIso_idx[0]]'
    twoD_C_var = 'ph_sigmaIEIE[ptSorted_ph_mediumNoSIEIE_idx[0]]:ph_chIsoCorr[ptSorted_ph_mediumNoSIEIE_idx[0]]'
    twoD_D_var = 'ph_sigmaIEIE[ptSorted_ph_mediumNoSIEIENoChIso_idx[0]]:ph_chIsoCorr[ptSorted_ph_mediumNoSIEIENoChIso_idx[0]]'

    sigIEIE_binning = (50,0.,0.05)
    chIso_binning = (120,0.,12.)

    #---------------------------------------
    # draw the histograms
    #---------------------------------------
    hist_shape = clone_sample_and_draw( sampMan, sample, plot_var, full_sel_shape, binning )
    hist_num   = clone_sample_and_draw( sampMan, sample, plot_var, full_sel_num  , binning )
    hist_den   = clone_sample_and_draw( sampMan, sample, plot_var, full_sel_den  , binning )
    sampMan.outputs['%s_shapehist_%s' %(sample,suffix)] = hist_shape
    sampMan.outputs['%s_numhist_%s' %(sample,suffix)] = hist_num
    sampMan.outputs['%s_denhist_%s' %(sample,suffix)] = hist_den



    #hist_ABCD  = clone_sample_and_draw( sampMan, sample, ABCD_var, full_sel_ABCD, ABCD_binning )
    hist_B     = clone_sample_and_draw( sampMan, sample, twoD_B_var, full_sel_shape, ABCD_binning )
    hist_C     = clone_sample_and_draw( sampMan, sample, twoD_C_var, full_sel_num, ABCD_binning )
    hist_D     = clone_sample_and_draw( sampMan, sample, twoD_D_var, full_sel_den, ABCD_binning )

    hist_1d_sigmaIEIE_B  = clone_sample_and_draw( sampMan, sample, sigIEIE_B_var, full_sel_shape, sigIEIE_binning )
    hist_1d_chIso_B  = clone_sample_and_draw( sampMan, sample, chIso_B_var, full_sel_shape, chIso_binning )
    hist_1d_sigmaIEIE_C  = clone_sample_and_draw( sampMan, sample, sigIEIE_C_var, full_sel_num, sigIEIE_binning )
    hist_1d_chIso_C  = clone_sample_and_draw( sampMan, sample, chIso_C_var, full_sel_num, chIso_binning )
    hist_1d_sigmaIEIE_D  = clone_sample_and_draw( sampMan, sample, sigIEIE_D_var, full_sel_den, sigIEIE_binning )
    hist_1d_chIso_D  = clone_sample_and_draw( sampMan, sample, chIso_D_var, full_sel_den, chIso_binning )

    sampMan.outputs['%s_sigmaIEIE_B_%s' %(sample,suffix)] = hist_1d_sigmaIEIE_B
    sampMan.outputs['%s_sigmaIEIE_C_%s' %(sample,suffix)] = hist_1d_sigmaIEIE_C
    sampMan.outputs['%s_sigmaIEIE_D_%s' %(sample,suffix)] = hist_1d_sigmaIEIE_D
    sampMan.outputs['%s_chIso_B_%s' %(sample,suffix)] = hist_1d_chIso_B
    sampMan.outputs['%s_chIso_C_%s' %(sample,suffix)] = hist_1d_chIso_C
    sampMan.outputs['%s_chIso_D_%s' %(sample,suffix)] = hist_1d_chIso_D


    #---------------------------------------
    # make fit managers
    #---------------------------------------
    fitMan_shape = FitManager( 'dijet', 3, '%s_shape' %sample, hist_shape, plot_var, eta_cut, xvar, label_shape, useRooFit=False )
    fitMan_num   = FitManager( 'dijet', 3, '%s_num' %sample, hist_num, plot_var, eta_cut, xvar, label_num, useRooFit=False )
    fitMan_den   = FitManager( 'dijet', 3, '%s_den' %sample, hist_den, plot_var, eta_cut, xvar, label_den, useRooFit=False )

    #---------------------------------------
    # Do the fits
    #---------------------------------------
    result_shape= fitMan_shape.fit_histogram( ws )
    result_num = fitMan_num.fit_histogram( ws )
    result_den = fitMan_den.fit_histogram( ws )
    print 'DEBUG: results of fit manager (shape, num, den): ',result_shape,result_num,result_den

    #---------------------------------------
    # save the results
    #---------------------------------------
    fitMan_den.save_fit( sampMan, ws, logy=True )
    fitMan_shape.save_fit( sampMan, ws, logy=True )
    fitMan_num.save_fit( sampMan, ws, logy=True )

    #---------------------------------------
    # calculate the function that describes
    # the ratio of num/den
    #---------------------------------------
    _integral_num   =  ws.pdf( 'dijet_%s' %label_num ).getNormIntegral(ROOT.RooArgSet( xvar ) )
    _integral_den   =  ws.pdf( 'dijet_%s' %label_den).getNormIntegral(ROOT.RooArgSet( xvar ) )
    _integral_shape =  ws.pdf( 'dijet_%s' %label_shape).getNormIntegral(ROOT.RooArgSet( xvar ) )

    func_integral_num    = _integral_num.getValV()
    func_integral_den    = _integral_den.getValV()
    func_integral_shape  = _integral_shape.getValV()

    hist_integral_num = result_num['integral'].n
    hist_integral_den = result_den['integral'].n
    hist_integral_shape = result_shape['integral'].n

    norm_num = hist_integral_num / func_integral_num
    norm_den = hist_integral_den / func_integral_den
    norm_shape = hist_integral_shape / func_integral_shape

    print 'func integral Num = ', func_integral_num
    print 'hist integral Num = ', hist_integral_num
    print 'normalization Num = ', norm_num

    print 'func integral Den = ', func_integral_den
    print 'hist integral Den = ', hist_integral_den
    print 'normalization Den = ', norm_den

    print 'func integral Shape = ', func_integral_shape
    print 'hist integral Shape = ', hist_integral_shape
    print 'normalization Shape = ', norm_shape

    power_pred_name    = 'power_pred_%s' %suffix
    logcoef_pred_name  = 'logcoef_pred_%s' %suffix
    log2coef_pred_name  = 'log2coef_pred_%s' %suffix
    power_ratio_name   = 'power_ratio_%s' %suffix
    logcoef_ratio_name = 'logcoef_ratio_%s' %suffix


    #name_power_num     ='power' 
    #name_power_den     ='power' 
    #name_power_shape   ='power' 

    #name_logcoef_num   ='logcoef1' 
    #name_logcoef_den   ='logcoef1' 
    #name_logcoef_shape ='logcoef1' 

    name_power_num     ='dijet_order1_%s' %label_num  
    name_power_den     ='dijet_order1_%s' %label_den  
    name_power_shape   ='dijet_order1_%s' %label_shape

    name_logcoef_num   ='dijet_order2_%s' %label_num  
    name_logcoef_den   ='dijet_order2_%s' %label_den  
    name_logcoef_shape ='dijet_order2_%s' %label_shape

    name_log2coef_num   ='dijet_order3_%s' %label_num  
    name_log2coef_den   ='dijet_order3_%s' %label_den  
    name_log2coef_shape ='dijet_order3_%s' %label_shape


    val_power_num     = ws.var( name_power_num      )
    val_power_den     = ws.var( name_power_den      )
    val_power_shape   = ws.var( name_power_shape    )

    val_logcoef_num   = ws.var( name_logcoef_num    )
    val_logcoef_den   = ws.var( name_logcoef_den    )
    val_logcoef_shape = ws.var( name_logcoef_shape  )

    val_log2coef_num   = ws.var( name_log2coef_num    )
    val_log2coef_den   = ws.var( name_log2coef_den    )
    val_log2coef_shape = ws.var( name_log2coef_shape  )


    power_pred    = ROOT.RooRealVar( power_pred_name   , 'power'  , (val_power_num.getValV() + val_power_shape.getValV() - val_power_den.getValV()) , -100, 100)
    logcoef_pred  = ROOT.RooRealVar( logcoef_pred_name , 'logcoef', (val_logcoef_num.getValV() + val_logcoef_shape.getValV() - val_logcoef_den.getValV()), -10, 10 )
    log2coef_pred  = ROOT.RooRealVar( log2coef_pred_name , 'log2coef', (val_log2coef_num.getValV() + val_log2coef_shape.getValV() - val_log2coef_den.getValV()), -10, 10 )
    #power_ratio   = ROOT.RooRealVar( power_ratio_name  , 'power'  , val_power_num - val_power_den , -100, 100)
    #logcoef_ratio = ROOT.RooRealVar( logcoef_ratio_name, 'logcoef', val_logcoef_num - val_logcoef_den, -10, 10 )


    #func = 'TMath::Power(@0/13000, @1+@2*TMath::Log10(@0/13000))'  
    #prediction = ROOT.RooGenericPdf('dijet_prediction_%s' %suffix , 'prediction', func, ROOT.RooArgList(xvar,power_pred, logcoef_pred))
    func = 'TMath::Power(@0/13000, @1+@2*TMath::Log10(@0/13000)+@3*TMath::Log10(@0/13000)*TMath::Log10(@0/13000))'  
    prediction = ROOT.RooGenericPdf('dijet_prediction_%s' %suffix , 'prediction', func, ROOT.RooArgList(xvar,power_pred, logcoef_pred, log2coef_pred))
    norm_pred = ROOT.RooRealVar( 'dijet_prediction_%s_norm' %(suffix), 'prediction normalization', (hist_integral_shape * hist_integral_num) / hist_integral_den )
    getattr( ws , 'import' ) ( norm_pred )
    getattr( ws , 'import' ) ( prediction )


    #---------------------------------------
    # Save the ABCD plots
    #---------------------------------------

    #can_ABCD = ROOT.TCanvas( str(uuid.uuid4()), '' )
    #can_ABCD.SetLogz()
    #hist_ABCD.Scale(1./hist_ABCD.Integral())
    #hist_ABCD.Draw("colz")
    #print "DEBUG: ABCD integral = ",hist_ABCD.Integral()

    can_B = ROOT.TCanvas( str(uuid.uuid4()), '' )
    can_B.SetLogz()
    hist_B.Scale(1./hist_B.Integral())
    hist_B.Draw("colz")
    print "DEBUG: B integral = ",hist_B.Integral()

    can_C = ROOT.TCanvas( str(uuid.uuid4()), '' )
    hist_C.Scale(1./hist_C.Integral())
    can_C.SetLogz()
    hist_C.Draw("colz")
    print "DEBUG: C integral = ",hist_C.Integral()

    can_D = ROOT.TCanvas( str(uuid.uuid4()), '' )
    hist_D.Scale(1./hist_D.Integral())
    can_D.SetLogz()
    hist_D.Draw("colz")
    print "DEBUG: D integral = ",hist_D.Integral()

    can_1d_sig_B = ROOT.TCanvas( str(uuid.uuid4()), '' )
    can_1d_sig_B.SetLogy()
    hist_1d_sigmaIEIE_B.Draw('l')
    can_1d_iso_B = ROOT.TCanvas( str(uuid.uuid4()), '' )
    can_1d_iso_B.SetLogy()
    hist_1d_chIso_B.Draw('l')

    can_1d_sig_C = ROOT.TCanvas( str(uuid.uuid4()), '' )
    can_1d_sig_C.SetLogy()
    hist_1d_sigmaIEIE_C.Draw('l')
    can_1d_iso_C = ROOT.TCanvas( str(uuid.uuid4()), '' )
    can_1d_iso_C.SetLogy()
    hist_1d_chIso_C.Draw('l')

    can_1d_sig_D = ROOT.TCanvas( str(uuid.uuid4()), '' )
    can_1d_sig_D.SetLogy()
    hist_1d_sigmaIEIE_D.Draw('l')
    can_1d_iso_D = ROOT.TCanvas( str(uuid.uuid4()), '' )
    can_1d_iso_D.SetLogy()
    hist_1d_chIso_D.Draw('l')

    #plot sigmaIEIE in regions B, C, D
    can_1d_sig = ROOT.TCanvas( str(uuid.uuid4()), '' )
    can_1d_sig.SetLogy()

    hist_norm_1d_sigmaIEIE_B = ROOT.TH1F(str(uuid.uuid4()) , str(uuid.uuid4()), hist_1d_sigmaIEIE_B.GetNbinsX(), hist_1d_sigmaIEIE_B.GetXaxis().GetXmin(), hist_1d_sigmaIEIE_B.GetXaxis().GetXmax())
    hist_norm_1d_sigmaIEIE_C = ROOT.TH1F(str(uuid.uuid4()) , str(uuid.uuid4()), hist_1d_sigmaIEIE_C.GetNbinsX(), hist_1d_sigmaIEIE_C.GetXaxis().GetXmin(), hist_1d_sigmaIEIE_C.GetXaxis().GetXmax())
    hist_norm_1d_sigmaIEIE_D = ROOT.TH1F(str(uuid.uuid4()) , str(uuid.uuid4()), hist_1d_sigmaIEIE_D.GetNbinsX(), hist_1d_sigmaIEIE_D.GetXaxis().GetXmin(), hist_1d_sigmaIEIE_D.GetXaxis().GetXmax())

    hist_1d_sigmaIEIE_B.Copy(hist_norm_1d_sigmaIEIE_B)
    hist_1d_sigmaIEIE_C.Copy(hist_norm_1d_sigmaIEIE_C)
    hist_1d_sigmaIEIE_D.Copy(hist_norm_1d_sigmaIEIE_D)
    ROOT.SetOwnership( hist_norm_1d_sigmaIEIE_B, False )
    ROOT.SetOwnership( hist_norm_1d_sigmaIEIE_C, False )
    ROOT.SetOwnership( hist_norm_1d_sigmaIEIE_D, False )

    hist_norm_1d_sigmaIEIE_B.Scale(1./hist_norm_1d_sigmaIEIE_B.Integral())
    hist_norm_1d_sigmaIEIE_C.Scale(1./hist_norm_1d_sigmaIEIE_C.Integral())
    hist_norm_1d_sigmaIEIE_D.Scale(1./hist_norm_1d_sigmaIEIE_D.Integral())
    hist_norm_1d_sigmaIEIE_B.SetLineColor(2)
    hist_norm_1d_sigmaIEIE_C.SetLineColor(1)
    hist_norm_1d_sigmaIEIE_D.SetLineColor(4)
    hist_norm_1d_sigmaIEIE_B.SetMarkerColor(2)
    hist_norm_1d_sigmaIEIE_C.SetMarkerColor(1)
    hist_norm_1d_sigmaIEIE_D.SetMarkerColor(4)
    hist_norm_1d_sigmaIEIE_B.Draw('l')
    hist_norm_1d_sigmaIEIE_C.Draw('same')
    hist_norm_1d_sigmaIEIE_D.Draw('same')

    #plot chIso in regions B, C, D
    can_1d_iso = ROOT.TCanvas( str(uuid.uuid4()), '' )
    can_1d_iso.SetLogy()

    hist_norm_1d_chIso_B = ROOT.TH1F(str(uuid.uuid4()) , str(uuid.uuid4()), hist_1d_chIso_B.GetNbinsX(), hist_1d_chIso_B.GetXaxis().GetXmin(), hist_1d_chIso_B.GetXaxis().GetXmax())
    hist_norm_1d_chIso_C = ROOT.TH1F(str(uuid.uuid4()) , str(uuid.uuid4()), hist_1d_chIso_C.GetNbinsX(), hist_1d_chIso_C.GetXaxis().GetXmin(), hist_1d_chIso_C.GetXaxis().GetXmax())
    hist_norm_1d_chIso_D = ROOT.TH1F(str(uuid.uuid4()) , str(uuid.uuid4()), hist_1d_chIso_D.GetNbinsX(), hist_1d_chIso_D.GetXaxis().GetXmin(), hist_1d_chIso_D.GetXaxis().GetXmax())

    hist_1d_chIso_B.Copy(hist_norm_1d_chIso_B)
    hist_1d_chIso_C.Copy(hist_norm_1d_chIso_C)
    hist_1d_chIso_D.Copy(hist_norm_1d_chIso_D)
    ROOT.SetOwnership( hist_norm_1d_chIso_B, False )
    ROOT.SetOwnership( hist_norm_1d_chIso_C, False )
    ROOT.SetOwnership( hist_norm_1d_chIso_D, False )

    hist_norm_1d_chIso_B.Scale(1./hist_norm_1d_chIso_B.Integral())
    hist_norm_1d_chIso_C.Scale(1./hist_norm_1d_chIso_C.Integral())
    hist_norm_1d_chIso_D.Scale(1./hist_norm_1d_chIso_D.Integral())
    hist_norm_1d_chIso_B.SetLineColor(2)
    hist_norm_1d_chIso_C.SetLineColor(1)
    hist_norm_1d_chIso_D.SetLineColor(4)
    hist_norm_1d_chIso_B.SetMarkerColor(2)
    hist_norm_1d_chIso_C.SetMarkerColor(1)
    hist_norm_1d_chIso_D.SetMarkerColor(4)
    hist_norm_1d_chIso_C.Draw('l')
    hist_norm_1d_chIso_B.Draw('same')
    hist_norm_1d_chIso_D.Draw('same')


    #---------------------------------------
    # Save the ratio histogram
    #---------------------------------------

    # canvas for ratio histogram
    can_ratio = ROOT.TCanvas( 'canv_ratio_%s' %(plot_var), 'canv_ratio_%s' %(plot_var) )
    #ROOT.SetOwnership( can_ratio, False )

    # ratio histogram = numerator histogram/denominator histogram
    ratiohist = ROOT.TH1F( 'ratio_%s' %(plot_var), 'ratio_%s' %(plot_var), hist_num.GetNbinsX(), hist_num.GetXaxis().GetXmin(), hist_num.GetXaxis().GetXmax())
    hist_num.Copy( ratiohist)
    ROOT.SetOwnership( ratiohist, False )

    print "DEBUG: first bin of num before div = ",ratiohist.GetBinContent(1)
    print "DEBUG: first bin of den before div = ",hist_den.GetBinContent(1)

    ratiohist.Divide( hist_den )
    print "DEBUG: first bin of ratio after div = ",ratiohist.GetBinContent(1)

    ratiohist.SetMarkerStyle(20)
    ratiohist.SetMarkerSize(1)
    ratiohist.GetXaxis().SetTitle( 'Transverse Mass [GeV]' )
    ratiohist.GetYaxis().SetTitle( 'ratio of passing to failing %s' %shape_var )
    ratiohist.Draw()
    ratiohist.SetStats(0)
    ratiohist.SetMinimum( 0) 
    ratiohist.SetMaximum( 5) 

    #ratio_func = ROOT.TF1( 'ratio_func_%s'%(str(uuid.uuid4())), '( [2]*TMath::Power(x/13000, [0] + [1]*TMath::Log10(x/13000) ) ) ', xmin, xmax )
    ratio_func = ROOT.TF1( 'ratio_func', '[0]', xmin, xmax )
    print 'DEBUG: ratio function = ',ratio_func
    ROOT.SetOwnership( ratio_func, False )
    print 'DEBUG: ratio function value at 200 GeV = ',ratio_func.Eval(200.)
    print 'DEBUG: ratio of integrals = ',hist_num.Integral()/hist_den.Integral()
    ratio_func.SetParameter(0, hist_num.Integral()/hist_den.Integral())
    #ratio_func.SetParameter(0, result_num[name_power_num].n - result_den[name_power_den].n)
    #ratio_func.SetParameter(1, result_num[name_logcoef_num].n  - result_den[name_logcoef_den].n )
    #ratio_func.SetParameter(2, norm_num / norm_den )
    ratiohist.Fit("ratio_func","RL","",xmin,xmax)
    print 'xmin and xmax are ',xmin,xmax
    f = ratiohist.GetFunction("ratio_func")
    fitvalue = ratio_func.GetParameter(0)
    print 'DEBUG: fitted straight line at ',fitvalue
    print 'DEBUG: chisquare of fit = ',f.GetChisquare()
    print 'DEBUG: ndof of fit = ',f.GetNDF()
    print 'DEBUG: testing f->GetParameter(0) = ',f.GetParameter(0)
    print 'DEBUG: testing f->GetParError(0) = ',f.GetParError(0)
    ratio_func.Draw('same')

    print 'DEBUG: prediction in A from B*C/D histograms = ',hist_shape.Integral(hist_shape.FindBin( xmin ), hist_shape.FindBin( xmax ))*hist_num.Integral(hist_num.FindBin( xmin ), hist_num.FindBin( xmax ))/hist_den.Integral(hist_den.FindBin( xmin ), hist_den.FindBin( xmax ))

    #ratio_power_v = val_power_num.getValV() - val_power_den.getValV()
    #ratio_power_e = math.sqrt(val_power_num.getErrorHi()*val_power_num.getErrorHi() + val_power_den.getErrorHi()*val_power_den.getErrorHi() )
    #ratio_logcoef_v = val_logcoef_num.getValV() - val_logcoef_den.getValV()
    #ratio_logcoef_e = math.sqrt(val_logcoef_num.getErrorHi()*val_logcoef_num.getErrorHi() + val_logcoef_den.getErrorHi()*val_logcoef_den.getErrorHi() )

    #power_tex   = ROOT.TLatex(0, 0, 'power = %.01f #pm %.02f' %( ratio_power_v,  ratio_power_e ))
    #ROOT.SetOwnership( power_tex, False )
    #logcoef_tex = ROOT.TLatex(0, 0, 'logcoef = %.01f #pm %.02f' %( ratio_logcoef_v,  ratio_logcoef_e ))
    #ROOT.SetOwnership( logcoef_tex, False )

    #power_tex.SetNDC()
    #logcoef_tex.SetNDC()

    #power_tex  .SetX( 0.6 )
    #power_tex  .SetY( 0.84 )
    #logcoef_tex.SetX( 0.6 )
    #logcoef_tex.SetY( 0.78 )

    #power_tex.Draw('same')
    #logcoef_tex.Draw('same')

    #sampMan.outputs['wjets_ABCD_%s' %suffix] = can_ABCD
    sampMan.outputs['%s_B_%s' %(sample,suffix)] = can_B
    sampMan.outputs['%s_C_%s' %(sample,suffix)] = can_C
    sampMan.outputs['%s_D_%s' %(sample,suffix)] = can_D

    sampMan.outputs['%s_sigmaIEIE_B_%s' %(sample,suffix)] = can_1d_sig_B
    sampMan.outputs['%s_chIso_B_%s' %(sample,suffix)] = can_1d_iso_B
    sampMan.outputs['%s_sigmaIEIE_C_%s' %(sample,suffix)] = can_1d_sig_C
    sampMan.outputs['%s_chIso_C_%s' %(sample,suffix)] = can_1d_iso_C
    sampMan.outputs['%s_sigmaIEIE_D_%s' %(sample,suffix)] = can_1d_sig_D
    sampMan.outputs['%s_chIso_D_%s' %(sample,suffix)] = can_1d_iso_D
    sampMan.outputs['%s_sigmaIEIE_BCD_%s' %(sample,suffix)] = can_1d_sig
    sampMan.outputs['%s_chIso_BCD_%s' %(sample,suffix)] = can_1d_iso


    if closure :
 #       sampMan.outputs['wjetsclosure_ratio_%s' %suffix] = can_ratio 
        sampMan.outputs['%sclosure_ratio_hist_%s' %(sample,suffix)] = ratiohist 
        sampMan.outputs['%sclosure_ratio_func_%s' %(sample,suffix)] = ratio_func
        #sampMan.outputs['wjetsclosure_ratio_power_%s' %suffix] = power_tex
        #sampMan.outputs['wjetsclosure_ratio_logcoef_%s' %suffix] = logcoef_tex

    else :
 #       sampMan.outputs['wjets_ratio_%s' %suffix] = can_ratio 
        sampMan.outputs['%s_ratio_hist_%s' %(sample,suffix)] = ratiohist 
        sampMan.outputs['%s_ratio_func_%s' %(sample,suffix)] = ratio_func 
        #sampMan.outputs['wjets_ratio_power_%s' %suffix] = power_tex
        #sampMan.outputs['wjets_ratio_logcoef_%s' %suffix] = logcoef_tex
    
    if closure :

        # canvas for signal region predictions
        can_sr = ROOT.TCanvas( 'canv_sig_%s_%s' %(sample,plot_var), 'canv_sig_%s_%s' %(sample,plot_var) )
        ROOT.SetOwnership( can_sr, False )

        hist_sr    = clone_sample_and_draw( sampMan, sample, plot_var, full_sel_sr , binning )
        ROOT.SetOwnership( hist_sr, False )
        hist_sr.GetXaxis().SetTitle( 'Transverse Mass [GeV]' )
        #hist_sr.GetYaxis().SetTitle( 'ratio of passing to failing %s' %shape_var ) ##really?
        hist_sr.GetYaxis().SetTitle( 'Events in signal region' )

        # fit a dijet2 function to region A
        fitMan_sr = FitManager( 'dijet', 3, sample, hist_sr, plot_var, eta_cut, xvar, suffix, useRooFit=False )
        result_sr  = fitMan_sr.fit_histogram( ws )

        # from histograms in MC regions B, C, and D
        # predicted number of sr events
        pred_val = (hist_integral_shape * hist_integral_num) / hist_integral_den 

        # from histogram in MC region A
        # predicted number of sr events
        tot_sr = hist_sr.Integral( hist_sr.FindBin( xmin ), hist_sr.FindBin( xmax ) )
        print 'DEBUG: SR prediction from BCD MC = ',pred_val
        print 'DEBUG: SR MC events from A       = ',tot_sr
        print 'SR integral = ', tot_sr

        # from functions fitted to regions BCD
        # predicted number of sr events
        sr_func = ROOT.TF1( 'sr_func', '( [2]*TMath::Power(x/13000, [0] + [1]*TMath::Log10(x/13000) ) ) ', xmin, xmax )
        #sr_func = ROOT.TF1( 'sr_func', '[3]*TMath::Power(x/13000, [0]+[1]*TMath::Log10(x/13000)+[2]*TMath::Log10(x/13000)*TMath::Log10(x/13000))', xmin, xmax )

        ROOT.SetOwnership( sr_func, False )
        sr_func.SetParameter(0, result_num[name_power_num].n + result_shape[name_power_shape].n - result_den[name_power_den].n )
        sr_func.SetParameter(1, result_num[name_logcoef_num].n + result_shape[name_logcoef_shape].n - result_den[name_logcoef_den].n )
        #sr_func.SetParameter(2, result_num[name_log2coef_num].n + result_shape[name_log2coef_shape].n - result_den[name_log2coef_den].n  )
        sr_func.SetParameter(2, 1)
        sr_int = sr_func.Integral( xmin, xmax )
        print 'normalizations (shape, num, den) = ',norm_shape,norm_num,norm_den
        #print 'Normalization = ',(norm_shape*norm_num) / norm_den
        print 'func Integral SR Before = ', sr_func.Integral( xmin, xmax )
        sr_func.SetParameter(2, pred_val/sr_int )
        print 'func Integral SR After = ', sr_func.Integral( xmin, xmax )
        print 'DEBUG: closure SR fit function value at 200 GeV = ',sr_func.Eval(200.)
        hist_sr.Draw()
        sr_func.Draw('same')

        sampMan.outputs['%sclosure_sr_pred_%s' %(sample,suffix)] = can_sr
        sampMan.outputs['%sclosure_srhist_%s' %(sample,suffix)] = hist_sr

        tot_ratio = result_num['integral']/result_den['integral']
        print 'DEBUG: result_num[integral]/result_den[integral] = ',tot_ratio

        hist_jetpt        = clone_sample_and_draw( sampMan, sample, jet_var, sel_base, jet_binning )
        hist_subjetpt     = clone_sample_and_draw( sampMan, sample, subjet_var, sel_base, subjet_binning )
        hist_trueht       = clone_sample_and_draw( sampMan, sample, ht_var, sel_base, ht_binning )

        sampMan.outputs['%sclosure_jetpt_%s' %(sample,suffix)] = hist_jetpt
        sampMan.outputs['%sclosure_subjetpt_%s' %(sample,suffix)] = hist_subjetpt
        sampMan.outputs['%sclosure_trueht_%s' %(sample,suffix)] = hist_trueht


def clone_sample_and_draw( sampMan, samp, var, sel, binning ) :

    newSamp = sampMan.clone_sample( oldname=samp, newname=samp+str(uuid.uuid4()), temporary=True ) 
    sampMan.create_hist( newSamp, var, sel, binning )
    return newSamp.hist

main()

    




    
    




