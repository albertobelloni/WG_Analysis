import ROOT
ROOT.PyConfig.IgnoreCommandLineOptions = True
import re
import os
import uuid
import math
import pickle
from AsymErrs import AsymErrs
from uncertainties import ufloat
#ROOT.TVirtualFitter.SetMaxIterations( 100000 )

from SampleManager import SampleManager
from argparse import ArgumentParser
parser = ArgumentParser()

parser.add_argument('--baseDirMu',      default=None,           dest='baseDirMu',         required=False, help='Path to muon base directory')
parser.add_argument('--baseDirEl',      default=None,           dest='baseDirEl',         required=False, help='Path to electron base directory')
parser.add_argument('--baseDirSigMu',      default=None,           dest='baseDirSigMu',         required=False, help='Path to signal samples in muon channel')
parser.add_argument('--baseDirSigEl',      default=None,           dest='baseDirSigEl',         required=False, help='Path to signal samples in muon channel')
parser.add_argument('--outputDir',      default=None,           dest='outputDir',         required=False, help='Output directory to write histograms')
parser.add_argument('--doSignal',       default=False,    action='store_true',      dest='doSignal', required=False, help='make signal fits' )
parser.add_argument('--doWGamma',       default=False,    action='store_true',      dest='doWGamma', required=False, help='make wgamma fits' )
parser.add_argument('--doWJets',       default=False,     action='store_true',     dest='doWJets', required=False, help='make w+jets fits' )
parser.add_argument('--doClosure',       default=False,   action='store_true',       dest='doClosure', required=False, help='make closure tests' )
#parser.add_argument('--doToyData',       default=False,   action='store_true',       dest='doToyData', required=False, help='make toy data' )

options = parser.parse_args()


_TREENAME = 'tupel/EventTree'
_FILENAME = 'tree.root'
_XSFILE   = 'cross_sections/photon15.py'
_LUMI     = 36000
_BASEPATH = '/home/jkunkle/usercode/Plotting/LimitSetting/'
_SAMPCONF = 'Modules/Resonance.py'


#_binning = (100, 0, 2000)

def get_ph_selection( sel1, sel2='' ) :

    if sel1 == 'all' :
        return 'ph_n'
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

    assert( 'get_ph_selection -- Could not parse selection vars!' )

def get_ph_idx( sel1, sel2='' ) :

    if sel1 == 'all' :
        return '0'
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

    assert( 'get_ph_idx -- Could not parse selection vars!' )

def get_cut_var( ivar ) :

    if ivar == 'chIso' :
        return 'ph_chIsoCorr'
    if ivar == 'sigmaIEIE' :
        return 'ph_sigmaIEIE'

    assert( 'get_cut_var -- Could not parse selection vars!' )

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

    sampManMu = SampleManager( options.baseDirMu, _TREENAME, filename=_FILENAME, xsFile=_XSFILE, lumi=_LUMI )
    sampManEl = SampleManager( options.baseDirEl, _TREENAME, filename=_FILENAME, xsFile=_XSFILE, lumi=_LUMI )
    sampManSigMu = SampleManager( options.baseDirSigMu, _TREENAME, filename=_FILENAME, xsFile=_XSFILE, lumi=_LUMI )
    sampManSigEl = SampleManager( options.baseDirSigEl, _TREENAME, filename=_FILENAME, xsFile=_XSFILE, lumi=_LUMI )

    sampManMu.ReadSamples( _SAMPCONF )
    sampManEl.ReadSamples( _SAMPCONF )
    sampManSigMu.ReadSamples( _SAMPCONF )
    sampManSigEl.ReadSamples( _SAMPCONF )

    sampManMu.outputs = {}
    sampManEl.outputs = {}
    sampManSigMu.outputs = {}
    sampManSigEl.outputs = {}

    sel_base_mu = 'mu_pt30_n==1 && mu_n==1'
    sel_base_el = 'el_pt30_n==1 && el_n==1'

    eta_cuts = ['EB', 'EE']

    workspaces_to_save = {}

    xmin = 160
    xmax = 1000

    binning = ((xmax-xmin)/20, xmin, xmax)
    xvar = ROOT.RooRealVar( 'x', 'x',xmin , xmax)

    if options.doSignal : 

        workspace_signal = ROOT.RooWorkspace( 'workspace_signal' )

        make_signal_fits( sampManSigMu, sel_base_mu, eta_cuts, 'mt_lep_met_ph', workspace_signal, suffix='mu' )
        make_signal_fits( sampManSigEl, sel_base_el, eta_cuts, 'mt_lep_met_ph', workspace_signal, suffix='el' )

        workspaces_to_save['signal'] = []
        workspaces_to_save['signal'].append(workspace_signal )

    if options.doWGamma :

        workspace_wgamma = ROOT.RooWorkspace( 'workspace_wgamma' )

        wgamma_res_mu = get_wgamma_fit( sampManMu, sel_base_mu, eta_cuts, xvar, 'mt_lep_met_ph', binning, workspace_wgamma, suffix='mu' )
        wgamma_res_el = get_wgamma_fit( sampManEl, sel_base_el, eta_cuts, xvar, 'mt_lep_met_ph', binning, workspace_wgamma, suffix='el' )

        workspaces_to_save['wgamma'] = []
        workspaces_to_save['wgamma'].append(workspace_wgamma)

    if options.doWJets :

        wjets  = ROOT.RooWorkspace( 'wjets' )
        #wjets_mu_EB  = ROOT.RooWorkspace( 'wjets_mu_EB' )
        #wjets_el_EB  = ROOT.RooWorkspace( 'wjets_el_EB' )
        #wjets_mu_EE  = ROOT.RooWorkspace( 'wjets_mu_EE' )
        #wjets_el_EE  = ROOT.RooWorkspace( 'wjets_el_EE' )

        wjets_res_mu = make_wjets_fit( sampManMu, 'Data', sel_base_mu, 'EB', 'mt_lep_met_ph', 'chIso', 'sigmaIEIE', binning, xvar, suffix='mu_EB', closure=False, workspace=wjets)
        wjets_res_el = make_wjets_fit( sampManEl, 'Data', sel_base_el, 'EB', 'mt_lep_met_ph', 'chIso', 'sigmaIEIE', binning, xvar, suffix='el_EB', closure=False, workspace=wjets)
        #wjets_res_mu = make_wjets_fit( sampManMu, 'Data', sel_base_mu, 'EE', 'mt_lep_met_ph', 'chIso', 'sigmaIEIE', binning, xvar, suffix='mu', closure=False, workspace=wjets_mu_EE )
        #wjets_res_el = make_wjets_fit( sampManEl, 'Data', sel_base_el, 'EE', 'mt_lep_met_ph', 'chIso', 'sigmaIEIE', binning, xvar, suffix='el', closure=False, workspace=wjets_el_EE )

        workspaces_to_save['wjets'] = []
        workspaces_to_save['wjets'].append( wjets )

    if options.doClosure :

        closure_res_mu = make_wjets_fit( sampManMu, 'Wjets', sel_base_mu, 'EB', 'mt_lep_met_ph', 'chIso', 'sigmaIEIE', binning, xvar, suffix='mu_EB', closure=True )
        closure_res_el = make_wjets_fit( sampManEl, 'Wjets', sel_base_el, 'EB', 'mt_lep_met_ph', 'chIso', 'sigmaIEIE', binning, xvar, suffix='el_EB', closure=True )

    if options.outputDir is not None :

        for fileid, ws_list in workspaces_to_save.iteritems() :
            for idx, ws in enumerate(ws_list) :
                if idx == 0 :
                    recreate = True
                else  :
                    recreate = False

                ws.writeToFile( '%s/workspace_%s.root' %( options.outputDir, fileid ), recreate )

        for key, can in sampManMu.outputs.iteritems() :
            print key
            can.SaveAs('%s/%s.pdf' %( options.outputDir, key ) )
        for key, can in sampManEl.outputs.iteritems() :
            can.SaveAs('%s/%s.pdf' %( options.outputDir, key ) )
        for key, can in sampManSigMu.outputs.iteritems() :
            can.SaveAs('%s/%s.pdf' %( options.outputDir, key ) )
        for key, can in sampManSigEl.outputs.iteritems() :
            can.SaveAs('%s/%s.pdf' %( options.outputDir, key ) )

#def make_toy_data( out_workspace, in_workspace, in_pdf, suffix='' ) :
#
#    in_workspace.Print()
#
#    pdf = in_workspace.pdf( in_pdf )
#
#    nevents = in_workspace.var( 'norm_%s' %in_pdf )
#
#    #dataset = pdf.generate( in_workspace.var('xvar'), Name='toydata%s' %suffix  )
#    dataset = pdf.generate( ROOT.RooArgSet(in_workspace.var('x')), nevents )
#    dataset.SetName( 'toydata%s' %suffix )
#    print dataset
#
#    getattr( out_workspace, 'import' )( dataset )



def make_signal_fits( sampMan, sel_base, eta_cuts, plot_var, workspace, suffix ) : 

    for samp in sampMan.get_samples(isSignal=True ) :

        res = re.match('(MadGraph|Pythia)ResonanceMass(\d+)_width(\d|0p01)', samp.name )
        if res is None :
            print 'Could not interpret path ', samp.name
        else :

            mass = res.group(2)
            width = res.group(3)

        ph_selection_sr = '%s==1' %get_ph_selection('all')
        ph_idx_sr =  get_ph_idx( 'all' )
        addtl_cuts_sr = 'ph_pt[%s] > 50 ' %ph_idx_sr

        xmin = 0
        xmax = int(mass)*2

        binning = ( 50, xmin, xmax )

        for ieta in eta_cuts :

            full_suffix = '%s_%s_%s' %(samp.name, suffix, ieta)

            eta_str_sr = 'ph_Is%s[%s]' %( ieta, ph_idx_sr )

            full_sel_sr    = ' && '.join( [sel_base, ph_selection_sr, eta_str_sr, addtl_cuts_sr] )

            hist_sr    = clone_sample_and_draw( sampMan, samp.name, plot_var, full_sel_sr, binning )

            xvar = ROOT.RooRealVar( 'x', 'x',xmin , xmax)
            datahist = ROOT.RooDataHist( 'srhist_%s' %full_suffix, 'srhist', ROOT.RooArgList(xvar), hist_sr)

            histpdf = ROOT.RooHistPdf( 'srhistpdf_%s' %(full_suffix), 'srhistpdf' , ROOT.RooArgSet( xvar), datahist, 3 )

            can = ROOT.TCanvas( 'signal_can_%s' %( full_suffix ), '' )
            frame = xvar.frame()

            datahist.plotOn( frame )
            histpdf.plotOn( frame )

            frame.Draw()
            sampMan.outputs[can.GetName()] = can

            getattr(workspace, 'import' )(histpdf)


def get_wgamma_fit( sampMan, sel_base, eta_cuts, xvar, plot_var, binning, workspace, suffix='' ) :

    ph_selection_sr = '%s==1' %get_ph_selection('medium')
    ph_idx_sr =  get_ph_idx( 'medium' )
    xmin = xvar.getMin()
    xmax = xvar.getMax()
    addtl_cuts_sr = 'ph_pt[%s] > 50 && %s > %d && %s < %d  ' %(ph_idx_sr, plot_var, xmin, plot_var , xmax )

    results = {}

    for ieta in eta_cuts :

        eta_str_sr = 'ph_Is%s[%s]' %( ieta, ph_idx_sr )

        full_sel_sr    = ' && '.join( [sel_base, ph_selection_sr, eta_str_sr, addtl_cuts_sr] )

        hist_sr    = clone_sample_and_draw( sampMan, 'Wgamma', plot_var, full_sel_sr   , binning )

        results[ieta] = fit_dijet( hist_sr, xvar, 'Wgamma_%s_%s'%(suffix, ieta), sampMan, workspace )

    return results

def make_wjets_fit( sampMan, sample, sel_base, eta_cut, plot_var, shape_var, num_var, binning, xvar, suffix='', closure=False, workspace=None) :

    ph_selection_sr = '%s==1' %get_ph_selection('medium')
    ph_selection_den = '%s==1'%get_ph_selection( num_var, shape_var )

    ph_selection_num = '%s==1' %get_ph_selection( num_var )
    ph_selection_shape = '%s==1' %get_ph_selection( shape_var )

    ph_idx_sr =  get_ph_idx( 'medium' )
    ph_idx_den = get_ph_idx( num_var, shape_var )
    ph_idx_num = get_ph_idx( num_var )
    ph_idx_shape = get_ph_idx( shape_var )

    xmin = xvar.getMin()
    xmax = xvar.getMax()

    addtl_cuts_sr = 'ph_pt[%s] > 50 && %s > %d && %s < %d '     %( ph_idx_sr, plot_var, xmin, plot_var, xmax )
    addtl_cuts_den = 'ph_pt[%s] > 50 && %s > %d && %s < %d  '   %( ph_idx_den, plot_var, xmin, plot_var, xmax )
    addtl_cuts_num = 'ph_pt[%s] > 50 && %s > %d && %s < %d  '   %( ph_idx_num, plot_var, xmin, plot_var, xmax )
    addtl_cuts_shape = 'ph_pt[%s] > 50 && %s > %d && %s < %d  ' %( ph_idx_shape, plot_var, xmin, plot_var, xmax )

    cut_var_shape = get_cut_var( shape_var )
    cut_var_num = get_cut_var( num_var )

    eta_str_shape = 'ph_Is%s[%s]' %( eta_cut, ph_idx_shape )
    eta_str_den = 'ph_Is%s[%s]' %( eta_cut, ph_idx_den)
    eta_str_num = 'ph_Is%s[%s]' %( eta_cut, ph_idx_num )
    eta_str_sr = 'ph_Is%s[%s]' %( eta_cut, ph_idx_sr )

    cut_vals_shape = get_cut_defaults( shape_var, eta_cut )
    cut_vals_num = get_cut_defaults( num_var, eta_cut )

    cut_str_base = ' {var}[{idx}] > {val_low} && {var}[{idx}] < {val_high}'

    cut_str_shape = cut_str_base.format(var=cut_var_shape, idx=ph_idx_shape, val_low=cut_vals_shape[0], val_high=cut_vals_shape[1] )
    cut_str_num = cut_str_base.format(var=cut_var_num, idx=ph_idx_num, val_low=cut_vals_num[0], val_high=cut_vals_num[1] )

    cut_str_den_1 = cut_str_base.format(var=cut_var_shape, idx=ph_idx_den, val_low=cut_vals_shape[0], val_high=cut_vals_shape[1] )
    cut_str_den_2 = cut_str_base.format(var=cut_var_num, idx=ph_idx_den, val_low=cut_vals_num[0], val_high=cut_vals_num[1] )

    cut_str_den = cut_str_den_1 + ' && ' + cut_str_den_2

    full_sel_shape = ' && '.join( [sel_base, ph_selection_shape, eta_str_shape, addtl_cuts_shape, cut_str_shape ] )
    full_sel_num   = ' && '.join( [sel_base, ph_selection_num, eta_str_num, addtl_cuts_num, cut_str_num] )
    full_sel_den   = ' && '.join( [sel_base, ph_selection_den, eta_str_den, addtl_cuts_den, cut_str_den] )
    full_sel_sr    = ' && '.join( [sel_base, ph_selection_sr, eta_str_sr, addtl_cuts_sr] )

    prefix = 'wjets'
    if closure :
        prefix = 'closure'

    label_shape = 'shape_%s' %suffix
    label_num   = 'num_%s' %suffix
    label_den   = 'den_%s' %suffix
    label_sr    = 'sr_%s' %suffix

    if workspace is None :
        ws = ROOT.RooWorkspace( 'ws') 
    else :
        ws = workspace

    hist_shape = clone_sample_and_draw( sampMan, sample, plot_var, full_sel_shape, binning )
    result_shape= fit_dijet( hist_shape, xvar, label_shape  , sampMan, ws  )
    hist_num   = clone_sample_and_draw( sampMan, sample, plot_var, full_sel_num  , binning )
    result_num = fit_dijet( hist_num, xvar, label_num , sampMan, ws )
    hist_den   = clone_sample_and_draw( sampMan, sample, plot_var, full_sel_den  , binning )
    result_den = fit_dijet( hist_den, xvar, label_den , sampMan, ws )

    if closure :
        hist_sr    = clone_sample_and_draw( sampMan, sample, plot_var, full_sel_sr   , binning )
        result_sr  = fit_dijet( hist_sr, xvar, label_sr, sampMan, ws )

    _integral_num =  ws.pdf( 'dijet_%s' %label_num ).getNormIntegral(ROOT.RooArgSet( xvar ) )
    func_integral_num  = _integral_num.getValV()
    _integral_den =  ws.pdf( 'dijet_%s' %label_den).getNormIntegral(ROOT.RooArgSet( xvar ) )
    func_integral_den  = _integral_den.getValV()
    _integral_shape =  ws.pdf( 'dijet_%s' %label_shape).getNormIntegral(ROOT.RooArgSet( xvar ) )
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

    if closure :
        print 'hist integral SR = ', hist_sr.Integral()

    power_pred_name    = 'power_pred_%s' %suffix
    logcoef_pred_name  = 'logcoef_pred_%s' %suffix
    #power_ratio_name   = 'power_ratio_%s' %suffix
    #logcoef_ratio_name = 'logcoef_ratio_%s' %suffix

    val_power_num   = ws.var( 'power_dijet_%s' %label_num   )
    val_power_den   = ws.var( 'power_dijet_%s' %label_den   )
    val_power_shape = ws.var( 'power_dijet_%s' %label_shape )

    val_logcoef_num   = ws.var( 'logcoef_dijet_%s' %label_num   )
    val_logcoef_den   = ws.var( 'logcoef_dijet_%s' %label_den   )
    val_logcoef_shape = ws.var( 'logcoef_dijet_%s' %label_shape )

    power_pred    = ROOT.RooRealVar( power_pred_name   , 'power'  , (val_power_num.getValV() + val_power_shape.getValV() - val_power_den.getValV()) , -100, 100)
    logcoef_pred  = ROOT.RooRealVar( logcoef_pred_name , 'logcoef', (val_logcoef_num.getValV() + val_logcoef_shape.getValV() - val_logcoef_den.getValV()), -10, 10 )
    #power_ratio   = ROOT.RooRealVar( power_ratio_name  , 'power'  , val_power_num - val_power_den , -100, 100)
    #logcoef_ratio = ROOT.RooRealVar( logcoef_ratio_name, 'logcoef', val_logcoef_num - val_logcoef_den, -10, 10 )

    func = 'pow(@0/13000, @1+@2*log(@0/13000))' 
    prediction = ROOT.RooGenericPdf('dijet_prediction' , 'dijet', func, ROOT.RooArgList(xvar,power_pred, logcoef_pred))
    ratio_func = ROOT.TF1( 'ratio_func', '( [2]*TMath::Power(x/13000, [0] + [1]*TMath::Log(x/13000) ) ) ', xmin, xmax )

    ratio_func.SetParameter(0, result_num['power'].n - result_den['power'].n)
    ratio_func.SetParameter(1, result_num['logcoef'].n  - result_den['logcoef'].n )
    ratio_func.SetParameter(2, norm_num / norm_den )

    can_ratio = ROOT.TCanvas( str(uuid.uuid4()), '' )
    ratiohist = hist_num.Clone( 'closure_ratio_%s' %(suffix) )
    ratiohist.Divide( hist_den )
    ratiohist.SetMarkerStyle(20)
    ratiohist.SetMarkerSize(1)
    ratiohist.GetXaxis().SetTitle( 'Transverse Mass [GeV]' )
    ratiohist.GetYaxis().SetTitle( 'ratio of passing to failing %s' %shape_var )
    ratiohist.Draw()
    ratiohist.SetStats(0)

    ratio_func.Draw('same')

    ratio_power_v = val_power_num.getValV() - val_power_den.getValV()
    ratio_power_e = math.sqrt(val_power_num.getErrorHi()*val_power_num.getErrorHi() + val_power_den.getErrorHi()*val_power_den.getErrorHi() )
    ratio_logcoef_v = val_logcoef_num.getValV() - val_logcoef_den.getValV()
    ratio_logcoef_e = math.sqrt(val_logcoef_num.getErrorHi()*val_logcoef_num.getErrorHi() + val_logcoef_den.getErrorHi()*val_logcoef_den.getErrorHi() )

    power_tex   = ROOT.TLatex(0, 0, 'power = %.01f #pm %.02f' %( ratio_power_v,  ratio_power_e ))
    logcoef_tex = ROOT.TLatex(0, 0, 'logcoef = %.01f #pm %.02f' %( ratio_logcoef_v,  ratio_logcoef_e ))

    power_tex.SetNDC()
    logcoef_tex.SetNDC()

    power_tex  .SetX( 0.6 )
    power_tex  .SetY( 0.84 )
    logcoef_tex.SetX( 0.6 )
    logcoef_tex.SetY( 0.78 )

    power_tex.Draw()
    logcoef_tex.Draw()

    if closure :
        sampMan.outputs['wjetsclosure_ratio_%s' %suffix] = can_ratio 
    else :
        sampMan.outputs['wjets_ratio_%s' %suffix] = can_ratio 
    
    if closure :

        can_sr = ROOT.TCanvas( str(uuid.uuid4()), '' )
        datahist = ROOT.RooDataHist( 'srhist', 'srhist', ROOT.RooArgList(xvar), hist_sr)

        tot_sr = hist_sr.Integral( hist_sr.FindBin( xmin ), hist_sr.FindBin( xmax ) )

        frame = xvar.frame()
        datahist.plotOn( frame )
        #prediction.plotOn( frame, ROOT.RooCmdArg('Normalization', 0, 0, hist_integral_shape * hist_integral_num / ( hist_integral_den * tot_sr ) ) )
        #prediction.plotOn( frame, ROOT.RooFit.Normalization( hist_integral_shape * hist_integral_num / ( hist_integral_den * tot_sr ), ROOT.RooAbsReal.NumEvent ) )
        prediction.plotOn( frame )
        frame.Draw()

        sampMan.outputs['wjetsclosure_pred_%s' %suffix] = can_sr

        raw_input('cont')



        tot_ratio = result_num['integral']/result_den['integral']


        #hist_num.Draw()
        #hist_den.Draw('same')
        #raw_input('cont')
        #hist_num.Divide(hist_den)
        #fit_pol1( hist_num, 200, 1000 )
        #hist_num.Draw()
        #raw_input('cont')

        #hist_sr.Draw()
        #raw_input('cont')



def fit_pol1( hist, xmin, xmax ) :

    lin_func = ROOT.TF1( 'lin_func', '[0] + [1]*x', xmin, xmax )

    lin_func.SetParameter( 0, 0.5 )
    lin_func.SetParameter( 1, 0 )

    hist.Fit( lin_func, 'R' )

    hist.Draw()
    lin_func.Draw('same')
    raw_input('cont')

def fit_dijet( hist, xvar, label='', sampMan=None, workspace=None ) :

    ###------------------------------
    ### Breit-Wigner, has two parameters, the resonance mass and the width
    ##------------------------------
    #bw_m = ROOT.RooRealVar('bw_mass' , 'Resonance  Mass', 100, 60, 160, 'GeV')
    #bw_w = ROOT.RooRealVar('bw_width', 'Breit-Wigner width',20, 0, 100,'GeV')
    #bw = ROOT.RooBreitWigner('bw' ,'A Breit-Wigner Distribution', xvar, bw_m,bw_w)
    #bw_m.setConstant()

    ##------------------------------
    ## crystal ball, has four parameters
    ##------------------------------
    #cb_cut = ROOT.RooRealVar('cb_cut'      , 'Cut'  , 0.2 , 0, 2 , '')
    #cb_sigma = ROOT.RooRealVar('cb_sigma' , 'Width', 2., 0  , 60, 'GeV')
    #cb_power = ROOT.RooRealVar('cb_power'      , 'Power', 7.1, 0    , 100 , '')
    #cb_m0 = ROOT.RooRealVar('cb_mass' , 'mass' , 0 , -200 , 200,'GeV')

    #cb = ROOT.RooCBShape('cb', 'A  Crystal Ball Lineshape', xvar, cb_m0, cb_sigma,cb_cut,cb_power)

    #model = ROOT.RooFFTConvPdf('sig_model','Convolution', xvar, bw, cb)

    #datahist = ROOT.RooDataHist( 'datahist', 'datahist', ROOT.RooArgList(xvar), hist )

    #model.fitTo( datahist, ROOT.RooFit.Range( 0, 1800),ROOT.RooFit.SumW2Error(True)  )

    #frame = xvar.frame() 
    #datahist.plotOn(frame)
    #model.plotOn( frame )
    #frame.Draw()
    #raw_input('cont')

    xmin = xvar.getMin()
    xmax = xvar.getMax()

    power_name = 'power_dijet_%s'  %label
    logcoef_name = 'logcoef_dijet_%s' %label

    power = ROOT.RooRealVar( 'power', 'power', -9.9, -100, 100)
    logcoef = ROOT.RooRealVar( 'logcoef', 'logcoef', -0.85, -10, 10 )
    #func = 'pow(x/13000, %s+%s*log(x/13000))' %( power_name, logcoef_name )
    func = 'pow(@0/13000, @1+@2*log(@0/13000))'  
    #func = 'pow(x/13000, %s+%s*(0.372+0.124*%s)*log(x/13000))' %( power_name, logcoef_name, power_name )
    #func = 'pow(x/13000, %s+(0.372+0.124*%s)*log(x/13000))' %( power_name, power_name )
    dijet = ROOT.RooGenericPdf('dijet_%s' %label, 'dijet', func, ROOT.RooArgList(xvar,power, logcoef))

    #datahist = ROOT.RooDataHist( 'datahist_%s' %label, 'data', ROOT.RooArgList(xvar), hist )
    datahist = ROOT.RooDataHist( 'datahist_%s' %label, 'data', ROOT.RooArgList(xvar), hist )

    dijet.fitTo( datahist, ROOT.RooFit.Range( xmin, xmax),ROOT.RooFit.SumW2Error(True)  )

    integral =  dijet.getNormIntegral(ROOT.RooArgSet( xvar ) )

    #power.setConstant()
    #logcoef.setConstant()

    if sampMan is not None :
        can = ROOT.TCanvas( str(uuid.uuid4()), '' )
        frame = xvar.frame() 
        datahist.plotOn(frame)
        dijet.plotOn( frame )
        dijet.paramOn(frame, ROOT.RooFit.ShowConstants(True), ROOT.RooFit.Layout(0.5,0.9,0.9), ROOT.RooFit.Format("NEU",ROOT.RooFit.AutoPrecision(2)));
        frame.Draw()
        ymax = frame.GetMaximum()
        frame.SetMinimum( 0.1 )
        frame.SetMaximum( ymax*5 )
        can.SetLogy()

        sampMan.outputs[label] = can

    integral = hist.Integral( hist.FindBin( xmin), hist.FindBin( xmax ) )

    power_res = ufloat( power.getValV(), power.getErrorHi() )
    log_res   = ufloat( logcoef.getValV(), logcoef.getErrorHi())
    int_res   = ufloat( integral, math.sqrt( integral ) )

    integral_var = ROOT.RooRealVar('norm_dijet_%s' %( label ), 'normalization', integral )

    power.SetName( power_name )
    logcoef.SetName( logcoef_name )

    if workspace is not None :
        getattr( workspace , 'import' ) ( datahist )
        getattr( workspace , 'import' ) ( dijet )
        getattr( workspace , 'import' ) ( integral_var )


    return {'power' : power_res, 'logcoef' : log_res, 'integral' : int_res, 'function_str' : func, 'object' : dijet }

    #dijet_func = ROOT.TF1( 'dijet_func', '[0]*pow(x/13000, [1]+[2]*log(x/13000))', xmin, xmax )
    ##dijet_func2 = ROOT.TF1( 'dijet_func2', '[0]*pow(x/13000, [1]+[2]*log(x/13000))', xmin, xmax )
    ##dijet_func3 = ROOT.TF1( 'dijet_func3', '[0]*pow(x/13000, [1]+[2]*log(x/13000))', xmin, xmax )
    ###dijet_func = ROOT.TF1( 'dijet_func', '[0]*pow(x/13000, [1])', xmin, xmax )

    #dijet_func.SetParameter(0, 8.9e-8 )
    #dijet_func.SetParameter(1, -5.6 )
    #dijet_func.SetParameter(2, 0.01 )

    ###dijet_func2.SetParameter(0, 8.9e-8 )
    ###dijet_func2.SetParameter(1, -5.6 )
    ###dijet_func2.SetParameter(2, -0.02 )

    ###dijet_func3.SetParameter(0, 8.9e-8 )
    ###dijet_func3.SetParameter(1, -5.6 )
    ###dijet_func3.SetParameter(2, 0.02 )

    #hist.Fit( dijet_func, 'R' )

    #hist.Draw()
    #dijet_func.Draw('same')
    ###dijet_func2.SetLineColor( ROOT.kMagenta )
    ###dijet_func3.SetLineColor( ROOT.kGreen)
    ###dijet_func2.Draw('same')
    ###dijet_func3.Draw('same')
    #raw_input('cont')


def clone_sample_and_draw( sampMan, samp, var, sel, binning ) :

    newSamp = sampMan.clone_sample( oldname=samp, newname=samp+str(uuid.uuid4()), temporary=True ) 
    sampMan.create_hist( newSamp, var, sel, binning )
    return newSamp.hist

main()

    




    
    




