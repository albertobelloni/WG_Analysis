import ROOT
ROOT.PyConfig.IgnoreCommandLineOptions = True
import re
import os
import uuid
import pickle

from SampleManager import SampleManager
from argparse import ArgumentParser
parser = ArgumentParser()

parser.add_argument('--baseDirMu',      default=None,           dest='baseDirMu',         required=True, help='Path to muon base directory')
parser.add_argument('--baseDirEl',      default=None,           dest='baseDirEl',         required=True, help='Path to electron base directory')
parser.add_argument('--outputDir',      default=None,           dest='outputDir',         required=False, help='Output directory to write histograms')

options = parser.parse_args()


_TREENAME = 'tupel/EventTree'
_FILENAME = 'tree.root'
_XSFILE   = 'cross_sections/photon15.py'
_LUMI     = 36000
_BASEPATH = '/home/jkunkle/usercode/Plotting/LimitSetting/'
_BKGSAMP  = 'MCBackground'
_SAMPCONF = 'Modules/Resonance.py'

ROOT.gROOT.SetBatch(False)

if options.outputDir is not None :
    ROOT.gROOT.SetBatch(True)
    if not os.path.isdir( options.outputDir ) :
        os.makedirs( options.outputDir )


def main() :

    sampManMu = SampleManager( options.baseDirMu, _TREENAME, filename=_FILENAME, xsFile=_XSFILE, lumi=_LUMI )
    sampManEl = SampleManager( options.baseDirEl, _TREENAME, filename=_FILENAME, xsFile=_XSFILE, lumi=_LUMI )

    sampManMu.ReadSamples( _SAMPCONF )
    sampManEl.ReadSamples( _SAMPCONF )

    sel_base_mu = 'mu_pt30_n==1 && mu_n==1 && ph_n==1'
    sel_base_el = 'el_pt30_n==1 && el_n==1 && ph_n==1'
    plot_var = 'mt_res'

    configs = [
                    {'tag' : 'mug', 'sampMan' : sampManMu, 'selection' : sel_base_mu },
                    {'tag' : 'elg', 'sampMan' : sampManEl, 'selection' : sel_base_el },
    ]


    sig_samples = []
    
    for samp in sampManMu.get_samples() :
        print samp.name
        if samp.name.count('ResonanceMass') > 0 :

            res = re.match('(MadGraph|Pythia)ResonanceMass(\d+)_width(\w+|\d+)', samp.name )

            sig_samples.append( ( samp.name, res.group(1), int(res.group(2)), res.group(3) ) )


    for conf in configs :

        for samp, samptype, mass, width in sig_samples :

            suffix = '_m%d_width%s' %( mass, width )

            fit_xmin = int(mass*0.6)
            xmax = mass * 1.5
            nbins = 100 

            var = ROOT.RooRealVar( 'm_res%s' %suffix, 'Transverse mass [GeV]', 0.0, xmax)
            
            var.setBins(10000,'cache')
            var.setMin('cache',-100)
            var.setMax('cache',1500)

            if width == '0p01' :
                width_factor = 0.01
            else :
                width_factor = float( width )


            #------------------------------
            # create the model
            #------------------------------

            #if width == '0p01' :
            #    #------------------------------
            #    # crystal ball, has four parameters
            #    #------------------------------
            #    cb_cut = ROOT.RooRealVar('cb_cut'      , 'Cut'  , 0.2 , 0, 2 , '')
            #    cb_sigma = ROOT.RooRealVar('cb_sigma' , 'Width', 2., 0  , 60, 'GeV')
            #    cb_power = ROOT.RooRealVar('cb_power'      , 'Power', 7.1, 0    , 100 , '')
            #    cb_m0 = ROOT.RooRealVar('cb_mass' , 'mass' , mass , mass*0.8, mass*1.2,'GeV')

            #    model = ROOT.RooCBShape('sig_model%s'%suffix, 'A  Crystal Ball Lineshape', var, cb_m0, cb_sigma,cb_cut,cb_power)
            #else :

            ##------------------------------
            ## Breit-Wigner, has two parameters, the resonance mass and the width
            #------------------------------
            bw_width_val = mass*0.01*width_factor
            #if bw_width_val < 2. :
            bw_width_val = 2.
            bw_m = ROOT.RooRealVar('bw_mass' , 'Resonance  Mass', mass, mass*0.8, mass*1.2,'GeV')
            bw_w = ROOT.RooRealVar('bw_width', 'Breit-Wigner width',bw_width_val , -100, 100,'GeV')
            bw_m.setConstant()
            bw_w.setConstant()
            bw = ROOT.RooBreitWigner('bw%s' %suffix,'A Breit-Wigner Distribution', var, bw_m,bw_w)

            ##------------------------------
            ## Gaussian, has two parameters, the resonance mass and the width
            ##------------------------------
            #gaus_width_val = mass*0.01*width_factor
            #if gaus_width_val < 2. :
            #    gaus_width_val = 2.0
            #gaus_m = ROOT.RooRealVar('bw_mass' , 'Resonance  Mass', mass, mass*0.8, mass*1.2,'GeV')
            #gaus_w = ROOT.RooRealVar('bw_width', 'Breit-Wigner width',gaus_width_val , -100, 100,'GeV')
            #gaus_m.setConstant()
            ##gaus_w.setConstant()
            #gaus = ROOT.RooGaussian('gaus%s' %suffix,'A Gaussian Distribution', var, gaus_m,gaus_w)


            #------------------------------
            # crystal ball, has four parameters
            #------------------------------
            cb_cut = ROOT.RooRealVar('cb_cut'      , 'Cut'  , 0.2 , 0, 2 , '')
            cb_sigma = ROOT.RooRealVar('cb_sigma' , 'Width', 2., 0  , 60, 'GeV')
            cb_power = ROOT.RooRealVar('cb_power'      , 'Power', 7.1, 0    , 100 , '')
            cb_m0 = ROOT.RooRealVar('cb_mass' , 'mass' , 0 , -200 , 200,'GeV')

            cb = ROOT.RooCBShape('cb%s'%suffix, 'A  Crystal Ball Lineshape', var, cb_m0, cb_sigma,cb_cut,cb_power)

            #------------------------------
            # FFT convolve them to make the model
            #------------------------------
            model = ROOT.RooFFTConvPdf('sig_model%s'%suffix,'Convolution', var, bw, cb)

            #------------------------------
            # create the data histogram
            #------------------------------
            conf['sampMan'].create_hist(samp, plot_var, conf['selection'], ( nbins, 0, xmax ) )

            hist = conf['sampMan'].get_samples(name=samp)[0].hist.Clone( 'data_muon%s' %suffix )
            data_hist = ROOT.RooDataHist( 'target_data', 'target_data', ROOT.RooArgList( var ), hist )

            model.fitTo( data_hist,ROOT.RooFit.Range(fit_xmin, mass*1.3),ROOT.RooFit.SumW2Error(True) )

            can = ROOT.TCanvas( str(uuid.uuid4()), '' )
            can.SetTitle('')

            frame = var.frame()
            frame.SetTitle('')

            data_hist.plotOn( frame )
            model.plotOn( frame )
            model.paramOn(frame, ROOT.RooFit.ShowConstants(True), ROOT.RooFit.Layout(0.1,0.5,0.9), ROOT.RooFit.Format("NEU",ROOT.RooFit.AutoPrecision(3)));

            frame.Draw()
            frame.Print()
            #if width != '0p01' :
            print 'bw_m = %f, err up = %f, err dn = %f ' %(bw_m.getValV(), bw_m.getErrorHi(), bw_m.getErrorLo() )
            print 'bw_w = %f, err up = %f, err dn = %f ' %(bw_w.getValV(), bw_w.getErrorHi(), bw_w.getErrorLo() )
            print 'cb_cut = %f, err up = %f, err dn = %f ' %(cb_cut.getValV(), cb_cut.getErrorHi(), cb_cut.getErrorLo() )
            print 'cb_sigma = %f, err up = %f, err dn = %f ' %(cb_sigma.getValV(), cb_sigma.getErrorHi(), cb_sigma.getErrorLo() )
            print 'cb_power = %f, err up = %f, err dn = %f ' %(cb_power.getValV(), cb_power.getErrorHi(), cb_power.getErrorLo() )
            print 'cb_m0 = %f, err up = %f, err dn = %f ' %(cb_m0.getValV(), cb_m0.getErrorHi(), cb_m0.getErrorLo() )

            #chi2 = frame.chiSquare( 'sig_model%s' %suffix, 'target_data', 4 )
            chi2 = frame.chiSquare(  4 )
            print 'Chi^2 = ',chi2

            chi2_text = ROOT.TLatex()
            chi2_text.SetNDC()
            chi2_text.SetText(0.12, 0.45, 'Chi^2/ndf = %.01f' %chi2 )

            chi2_text.Draw()

            result_dic = {}
            result_dic['bw_m'] = ( bw_m.getValV(), bw_m.getErrorHi(), bw_m.getErrorLo() )
            result_dic['bw_w'] = ( bw_w.getValV(), bw_w.getErrorHi(), bw_w.getErrorLo() )
            result_dic['cb_cut'] = ( cb_cut.getValV(), cb_cut.getErrorHi(), cb_cut.getErrorLo() )
            result_dic['cb_sigma'] = ( cb_sigma.getValV(), cb_sigma.getErrorHi(), cb_sigma.getErrorLo() )
            result_dic['cb_power'] = ( cb_power.getValV(), cb_power.getErrorHi(), cb_power.getErrorLo() )
            result_dic['cb_m0'] = ( cb_m0.getValV(), cb_m0.getErrorHi(), cb_m0.getErrorLo() )
            result_dic['chi2'] = chi2

            

            if options.outputDir is not None :
                name = 'SignalFit_%s_%s_M%d_width%s' %( samptype, conf['tag'], mass, width )
                can.SaveAs( '%s/%s.pdf' %( options.outputDir, name ) )
                opfile = open( '%s/%s.pickle' %(options.outputDir, name ) ,'w')
                pickle.dump( result_dic, opfile )
                opfile.close()
            else :
                raw_input("cont")





main()
