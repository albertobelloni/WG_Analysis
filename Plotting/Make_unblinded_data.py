import ROOT
from array import array
#execfile("MakeBase.py")
from ROOT import gSystem
gSystem.Load('../../../combine/CMSSW_11_0_0/lib/slc7_amd64_gcc820/libHiggsAnalysisCombinedLimit.so')
import numpy as np
from ROOT import RooMultiPdf

MIN_ = 230
MAX_ = 2500
treeIn      = "UMDNTuple/EventTree"
import os
data_outDir = "data/bkgfit_data"
if data_outDir is not None :
    if not os.path.isdir( data_outDir ) :
        os.makedirs( data_outDir )
        os.makedirs( data_outDir+'/2016' )
        os.makedirs( data_outDir+'/2017' )
        os.makedirs( data_outDir+'/2018' )
import glob
FileMap = {}
Date = '2022_01_27'
for year in ['2016','2017','2018']:
    for ch in ['el','mu']:
        if ch == 'el':
            FileMap[year+ch] = glob.glob('/data/users/yihuilai/Resonances'+year+'/LepGamma_elg_'+Date+'/WithSF/Single*/Job*/tree.root')
            if(year=='2018'): FileMap[year+ch] = glob.glob('/data/users/yihuilai/Resonances'+year+'/LepGamma_elg_'+Date+'/WithSF/EGamma/Job*/tree.root')
        if ch == 'mu':
            FileMap[year+ch] = glob.glob('/data/users/yihuilai/Resonances'+year+'/LepGamma_mug_'+Date+'/WithSF/SingleMuon/Job*/tree.root')
            
print('Loaded FileMap')

# ---------------------------------------------------

def import_workspace( ws , objects):
    """ import objects into workspace """

    if not isinstance( objects, list ):
        objects = [objects,]

    ## NOTE getattr is needed to escape python keyword import
    for o in objects:
        getattr( ws, "import") ( o )

### sets up the margins of the canvas ###
def canvas_margin(c1, c1_up, c1_down):
  c1_up.SetTopMargin( 0.07 )
  c1_up.SetBottomMargin( 0.02 )
  c1_up.SetLeftMargin( 0.15 )
  c1_up.SetRightMargin( 0.03 )

  c1_down.SetTopMargin( 0.03 )
  c1_down.SetBottomMargin( 0.4 )
  c1_down.SetLeftMargin( 0.15 )
  c1_down.SetRightMargin( 0.03 )

  c1.SetTopMargin( 0.05 )
  c1.SetBottomMargin( 0.13 )
  c1.SetRightMargin( 0.05 )
  c1.SetLeftMargin( 0.16 )

# ---------------------------------------------------
import selection_defs as defs

def prepare_data(frac, year, ch, skimtree, skimfile):
    #Prepare skimed data
    names = ROOT.std.vector('string')()
    for n in FileMap[year+ch]: names.push_back(n)
    d = ROOT.RDataFrame(treeIn, names)
    selection , weight = defs.makeselstring('el',  80, 35,  40)
    if ch=='mu':
        selection , weight = defs.makeselstring('mu',  80, 30,  40)
    #myfilter = d.Filter(selection).Range(1,0,frac)
    myfilter = d.Filter(selection)
    #print(selection)
    #print('make histo')
    Hmt = myfilter.Histo1D("mt_res")
    Hmt.Draw()
    myfilter.Snapshot(skimtree, skimfile)


def ShowSignalInjection():
    toyfile = '/data/users/yihuilai/test_code/WG_Analysis/Plotting/data_env/test_Dec20_testsignal_inject/Width5/all/Mass600/higgsCombine_test7.GenerateOnly.mH600.9024.root'
    fitpara = '/data/users/yihuilai/test_code/WG_Analysis/Plotting/data_env/test_Dec20_testsignal_inject/Width5/all/Mass600/fitDiagnostics_test7.root'
    # 1000 5%
    signalyield={'el2016':55.7951, 'mu2016':61.6212, 'el2017':61.4791, 'mu2017':67.3945, 'el2018':92.9473, 'mu2018':102.755}
    # 600 5%
    signalyield={'el2016':150.106, 'mu2016':177.152, 'el2017':170.551, 'mu2017':199.071, 'el2018':254.791, 'mu2018':302.308}
    injects = 1
    mass = '600'
    width = '5'

    year ='ALL'
    MIN_=220
    MAX_=2200
    NBIN_=100
    mt_res = ROOT.RooRealVar("mt_res", "mt_res", MIN_, MAX_)
    mt_res.setBins(NBIN_)

    # Get toy data
    F=ROOT.TFile(toyfile)
    toydata=F.Get("toys/toy_1")
    ne = toydata.sumEntries()
    print(ne)

    # Fit function
    fit_para={}
    year='2016'
    fit_para['vvdijet_order1_elA'+year+'_all_vvdijet'] = ROOT.RooRealVar('vvdijet_order1_elA'+year+'_all_vvdijet', "power1", -9, -1000, 1000)
    fit_para['vvdijet_order2_elA'+year+'_all_vvdijet'] = ROOT.RooRealVar('vvdijet_order2_elA'+year+'_all_vvdijet', "power2", -2, -1000, 1000)
    fit_para['vvdijet_order1_muA'+year+'_all_vvdijet'] = ROOT.RooRealVar('vvdijet_order1_muA'+year+'_all_vvdijet', "power1", -9, -1000, 1000)
    fit_para['vvdijet_order2_muA'+year+'_all_vvdijet'] = ROOT.RooRealVar('vvdijet_order2_muA'+year+'_all_vvdijet', "power2", -2, -1000, 1000)
    year='2017'
    fit_para['vvdijet_order1_elA'+year+'_all_vvdijet'] = ROOT.RooRealVar('vvdijet_order1_elA'+year+'_all_vvdijet', "power1", -9, -1000, 1000)
    fit_para['vvdijet_order2_elA'+year+'_all_vvdijet'] = ROOT.RooRealVar('vvdijet_order2_elA'+year+'_all_vvdijet', "power2", -2, -1000, 1000)
    fit_para['vvdijet_order1_muA'+year+'_all_vvdijet'] = ROOT.RooRealVar('vvdijet_order1_muA'+year+'_all_vvdijet', "power1", -9, -1000, 1000)
    fit_para['vvdijet_order2_muA'+year+'_all_vvdijet'] = ROOT.RooRealVar('vvdijet_order2_muA'+year+'_all_vvdijet', "power2", -2, -1000, 1000)
    year='2018'
    fit_para['vvdijet_order1_elA'+year+'_all_vvdijet'] = ROOT.RooRealVar('vvdijet_order1_elA'+year+'_all_vvdijet', "power1", -9, -1000, 1000)
    fit_para['vvdijet_order2_elA'+year+'_all_vvdijet'] = ROOT.RooRealVar('vvdijet_order2_elA'+year+'_all_vvdijet', "power2", -2, -1000, 1000)
    fit_para['vvdijet_order1_muA'+year+'_all_vvdijet'] = ROOT.RooRealVar('vvdijet_order1_muA'+year+'_all_vvdijet', "power1", -9, -1000, 1000)
    fit_para['vvdijet_order2_muA'+year+'_all_vvdijet'] = ROOT.RooRealVar('vvdijet_order2_muA'+year+'_all_vvdijet', "power2", -2, -1000, 1000)

    # generate function
    gen_para={}
    year='2016'
    gen_para['dijet_order1_elA'+year+'_all_dijet'] = ROOT.RooRealVar('dijet_order1_elA'+year+'_all_dijet', "power1", -9, -1000, 1000)
    gen_para['dijet_order2_elA'+year+'_all_dijet'] = ROOT.RooRealVar('dijet_order2_elA'+year+'_all_dijet', "power2", -2, -1000, 1000)
    gen_para['dijet_order1_muA'+year+'_all_dijet'] = ROOT.RooRealVar('dijet_order1_muA'+year+'_all_dijet', "power1", -9, -1000, 1000)
    gen_para['dijet_order2_muA'+year+'_all_dijet'] = ROOT.RooRealVar('dijet_order2_muA'+year+'_all_dijet', "power2", -2, -1000, 1000)
    year='2017'
    gen_para['dijet_order1_elA'+year+'_all_dijet'] = ROOT.RooRealVar('dijet_order1_elA'+year+'_all_dijet', "power1", -9, -1000, 1000)
    gen_para['dijet_order2_elA'+year+'_all_dijet'] = ROOT.RooRealVar('dijet_order2_elA'+year+'_all_dijet', "power2", -2, -1000, 1000)
    gen_para['dijet_order1_muA'+year+'_all_dijet'] = ROOT.RooRealVar('dijet_order1_muA'+year+'_all_dijet', "power1", -9, -1000, 1000)
    gen_para['dijet_order2_muA'+year+'_all_dijet'] = ROOT.RooRealVar('dijet_order2_muA'+year+'_all_dijet', "power2", -2, -1000, 1000)
    year='2018'
    gen_para['dijet_order1_elA'+year+'_all_dijet'] = ROOT.RooRealVar('dijet_order1_elA'+year+'_all_dijet', "power1", -9, -1000, 1000)
    gen_para['dijet_order2_elA'+year+'_all_dijet'] = ROOT.RooRealVar('dijet_order2_elA'+year+'_all_dijet', "power2", -2, -1000, 1000)
    gen_para['dijet_order1_muA'+year+'_all_dijet'] = ROOT.RooRealVar('dijet_order1_muA'+year+'_all_dijet', "power1", -9, -1000, 1000)
    gen_para['dijet_order2_muA'+year+'_all_dijet'] = ROOT.RooRealVar('dijet_order2_muA'+year+'_all_dijet', "power2", -2, -1000, 1000)

    bkg_norm = {}
    bkg_norm['r_gen'] = ROOT.RooRealVar('r_gen','r_gen',0,100000)
    bkg_norm['r_gen'].setVal(injects)
    bkg_norm['r_gen'].setConstant()
    bkg_norm['r_gen'].setError(0)
    bkgyield={'el2016':1479, 'mu2016':1777, 'el2017':2248, 'mu2017':2237, 'el2018':3433, 'mu2018':3302}
    for ich in ['el2016', 'el2017', 'el2018', 'mu2016', 'mu2017', 'mu2018']:
        bkg_norm['shapeBkg_genAll_'+ich+'__norm'] = ROOT.RooRealVar('shapeBkg_genAll_'+ich+'__norm','N_'+ich,0,100000)
        bkg_norm['shapeBkg_genAll_'+ich+'__norm'].setVal(bkgyield[ich])
        bkg_norm['shapeBkg_genAll_'+ich+'__norm'].setConstant()
        bkg_norm['shapeBkg_All_'+ich+'__norm'] = ROOT.RooRealVar('shapeBkg_genAll_'+ich+'__norm','N_'+ich,0,100000)

    bkg_norm['r'] = ROOT.RooRealVar('r','r',0,100000)

    # Signal
    signal_para = {}
    signal_para['cb_cut2_MG'] = ROOT.RooRealVar('cb_cut2_MG','cb_cut2_MG',-100,100)
    signal_para['cb_cut2_MG'].setVal(1.6)
    signal_para['cb_cut2_MG'].setConstant()
    signal_para['cb_pow1_MG'] = ROOT.RooRealVar('cb_powe1_MG','cb_power1_MG',-100,100)
    signal_para['cb_pow1_MG'].setVal(2.2)
    signal_para['cb_pow1_MG'].setConstant()
    signal_para['cb_pow2_MG'] = ROOT.RooRealVar('cb_powe2_MG','cb_power2_MG',-100,100)
    signal_para['cb_pow2_MG'].setVal(1.4)
    signal_para['cb_pow2_MG'].setConstant()
    for ich in ['el2016', 'el2017', 'el2018', 'mu2016', 'mu2017', 'mu2018']:
        signal_para['cb_cut1_MG_M'+mass+'_W'+width+'_'+ich] = ROOT.RooRealVar('cb_cut1_MG_M'+mass+'_W'+width+'_'+ich,'cb_cut1_MG_M'+mass+'_W'+width+'_'+ich,-100,10000)
        signal_para['cb_mass_MG_M'+mass+'_W'+width+'_'+ich] = ROOT.RooRealVar('cb_mass_MG_M'+mass+'_W'+width+'_'+ich,'cb_mass_MG_M'+mass+'_W'+width+'_'+ich,-100,10000)
        signal_para['cb_sigma_MG_M'+mass+'_W'+width+'_'+ich] = ROOT.RooRealVar('cb_sigma_MG_M'+mass+'_W'+width+'_'+ich,'cb_sigma_MG_M'+mass+'_W'+width+'_'+ich,-100,10000)
        signal_para['cb_MG_M'+mass+'_W'+width+'_'+ich] = ROOT.RooDoubleCB('cb_MG_M'+mass+'_W'+width+'_'+ich, 'Double Sided Crystal Ball Lineshape', mt_res, signal_para['cb_mass_MG_M'+mass+'_W'+width+'_'+ich], signal_para['cb_sigma_MG_M'+mass+'_W'+width+'_'+ich], signal_para['cb_cut1_MG_M'+mass+'_W'+width+'_'+ich], signal_para['cb_pow1_MG'], signal_para['cb_cut2_MG'],  signal_para['cb_pow2_MG'])

    print(fit_para.keys())
    print(gen_para.keys())
    # Get fit function
    f=ROOT.TFile(fitpara)
    res = f.Get("fit_s")
    fitargs=res.floatParsFinal()
    iter = fitargs.createIterator()
    a=iter.Next()
    while not a == 0:
        print(a.GetName())
        print(a.getVal())
        #print(a.getError())
        for ipa in fit_para.keys():
            if a.GetName()== ipa:
                fit_para[ipa].setVal(a.getVal())
                fit_para[ipa].setConstant()
                fit_para[ipa].setError(a.getError())
        for ipa in gen_para.keys():
            if a.GetName()== ipa:
                gen_para[ipa].setVal(a.getVal())
                gen_para[ipa].setConstant()
                gen_para[ipa].setError(a.getError())
        for ipa in bkg_norm.keys():
            if a.GetName()== ipa:
                bkg_norm[ipa].setVal(a.getVal())
                bkg_norm[ipa].setConstant()
                bkg_norm[ipa].setError(a.getError())
        for ipa in signal_para.keys():
            if a.GetName()== ipa:
                print('get ', ipa, a.getVal())
                signal_para[ipa].setVal(a.getVal())
                signal_para[ipa].setConstant()
                signal_para[ipa].setError(a.getError())
        if a.GetName()=='r':
            print('========> get r ', a.getVal())
            bkg_norm['r'].setVal(a.getVal())
            bkg_norm['r'].setConstant()
        if a.GetName()=='vvdijet_order2_muA2018_all_vvdijet':
            break
        else:
            a=iter.Next()

    # vvdijet
    frame = mt_res.frame(ROOT.RooFit.Title("Unbinned ML fit"))
    toydata.plotOn(frame)
    func_name = 'vvdijet'
    function = str(bkg_norm['shapeBkg_genAll_el2016__norm'].getVal()) + '*TMath::Power( (1-@0/13000.), '+ str(fit_para['vvdijet_order1_elA2016_all_vvdijet'].getVal())  +' ) / ( TMath::Power( @0/13000. , '+ str(fit_para['vvdijet_order2_elA2016_all_vvdijet'].getVal())  +'))'
    function += '+'+str(bkg_norm['shapeBkg_genAll_el2017__norm'].getVal()) + '*TMath::Power( (1-@0/13000.), '+ str(fit_para['vvdijet_order1_elA2017_all_vvdijet'].getVal())  +' ) / ( TMath::Power( @0/13000. , '+ str(fit_para['vvdijet_order2_elA2017_all_vvdijet'].getVal())  +'))'
    function += '+'+str(bkg_norm['shapeBkg_genAll_el2018__norm'].getVal()) + '*TMath::Power( (1-@0/13000.), '+ str(fit_para['vvdijet_order1_elA2018_all_vvdijet'].getVal())  +' ) / ( TMath::Power( @0/13000. , '+ str(fit_para['vvdijet_order2_elA2018_all_vvdijet'].getVal())  +'))'
    function += '+'+str(bkg_norm['shapeBkg_genAll_mu2016__norm'].getVal()) + '*TMath::Power( (1-@0/13000.), '+ str(fit_para['vvdijet_order1_muA2016_all_vvdijet'].getVal())  +' ) / ( TMath::Power( @0/13000. , '+ str(fit_para['vvdijet_order2_muA2016_all_vvdijet'].getVal())  +'))'
    function += '+'+str(bkg_norm['shapeBkg_genAll_mu2017__norm'].getVal()) + '*TMath::Power( (1-@0/13000.), '+ str(fit_para['vvdijet_order1_muA2017_all_vvdijet'].getVal())  +' ) / ( TMath::Power( @0/13000. , '+ str(fit_para['vvdijet_order2_muA2017_all_vvdijet'].getVal())  +'))'
    function += '+'+str(bkg_norm['shapeBkg_genAll_mu2018__norm'].getVal()) + '*TMath::Power( (1-@0/13000.), '+ str(fit_para['vvdijet_order1_muA2018_all_vvdijet'].getVal())  +' ) / ( TMath::Power( @0/13000. , '+ str(fit_para['vvdijet_order2_muA2018_all_vvdijet'].getVal())  +'))'
    print(function)
    func_vvdijet = ROOT.RooGenericPdf( '%s_%s'%(func_name, '_all_vvdijet'), func_name, function, ROOT.RooArgList(mt_res))
    func_vvdijet.plotOn(frame,ROOT.RooFit.LineColor(ROOT.kBlue),ROOT.RooFit.LineStyle(2))
    hpull_vvdijet2 = frame.pullHist()
    hpull_vvdijet2.SetLineColor(ROOT.kBlue)
    hpull_vvdijet2.SetMarkerColor(ROOT.kBlue)

    norm_totb = ROOT.RooRealVar("norm_vvdijetb","norm_vvdijetb",0,100000);
    norm_totb.setVal(bkg_norm['shapeBkg_All_el2016__norm'].getVal()+bkg_norm['shapeBkg_All_mu2016__norm'].getVal()+bkg_norm['shapeBkg_All_el2017__norm'].getVal()+bkg_norm['shapeBkg_All_mu2017__norm'].getVal()+bkg_norm['shapeBkg_All_el2018__norm'].getVal()+bkg_norm['shapeBkg_All_mu2018__norm'].getVal())
    norm_totb.setConstant()

    signal_norm={}

    for ich in ['el2016', 'el2017', 'el2018', 'mu2016', 'mu2017', 'mu2018']:
        signal_norm[ich] = ROOT.RooRealVar("signal_norm_"+ich,"signal_norm_"+ich,0,100000)
        signal_norm[ich].setVal(bkg_norm['r_gen'].getVal()*signalyield[ich])
        signal_norm[ich].setConstant()

    components_vvdijet = ROOT.RooArgList(func_vvdijet, signal_para['cb_MG_M'+mass+'_W'+width+'_el2016'], signal_para['cb_MG_M'+mass+'_W'+width+'_el2017'], signal_para['cb_MG_M'+mass+'_W'+width+'_el2018'], signal_para['cb_MG_M'+mass+'_W'+width+'_mu2016'], signal_para['cb_MG_M'+mass+'_W'+width+'_mu2017'], signal_para['cb_MG_M'+mass+'_W'+width+'_mu2018'])
    coeffs_vvdijet = ROOT.RooArgList(norm_totb,signal_norm['el2016'],signal_norm['el2017'],signal_norm['el2018'],signal_norm['mu2016'],signal_norm['mu2017'],signal_norm['mu2018'] )
    model_vvdijet = ROOT.RooAddPdf("model_vvdijet","f_all",components_vvdijet,coeffs_vvdijet)
    model_vvdijet.plotOn(frame,ROOT.RooFit.LineColor(ROOT.kBlue),ROOT.RooFit.LineStyle(1))
    hpull_vvdijet = frame.pullHist()
    hpull_vvdijet.SetLineColor(ROOT.kBlue)
    hpull_vvdijet.SetMarkerColor(ROOT.kBlue)

    # dijet
    func_name = 'dijet'
    function = str(bkg_norm['shapeBkg_All_el2016__norm'].getVal()) + ' *TMath::Power( @0/13000., '+ str(gen_para['dijet_order1_elA2016_all_dijet'].getVal())  +' + '+ str(gen_para['dijet_order2_elA2016_all_dijet'].getVal())  +'*TMath::Log10(@0/13000) ) '
    function += ' +'+str(bkg_norm['shapeBkg_All_el2017__norm'].getVal()) +'*TMath::Power( @0/13000., '+ str(gen_para['dijet_order1_elA2017_all_dijet'].getVal())  +' + '+ str(gen_para['dijet_order2_elA2017_all_dijet'].getVal())  +'*TMath::Log10(@0/13000) ) '
    function += ' +'+str(bkg_norm['shapeBkg_All_el2018__norm'].getVal()) +'*TMath::Power( @0/13000., '+ str(gen_para['dijet_order1_elA2018_all_dijet'].getVal())  +' + '+ str(gen_para['dijet_order2_elA2018_all_dijet'].getVal())  +'*TMath::Log10(@0/13000) ) '
    function += '+'+str(bkg_norm['shapeBkg_All_mu2016__norm'].getVal()) + ' *TMath::Power( @0/13000., '+ str(gen_para['dijet_order1_muA2016_all_dijet'].getVal())  +' + '+ str(gen_para['dijet_order2_muA2016_all_dijet'].getVal())  +'*TMath::Log10(@0/13000) ) '
    function += ' +'+str(bkg_norm['shapeBkg_All_mu2017__norm'].getVal()) +'*TMath::Power( @0/13000., '+ str(gen_para['dijet_order1_muA2017_all_dijet'].getVal())  +' + '+ str(gen_para['dijet_order2_muA2017_all_dijet'].getVal())  +'*TMath::Log10(@0/13000) ) '
    function += ' +'+str(bkg_norm['shapeBkg_All_mu2018__norm'].getVal()) +'*TMath::Power( @0/13000., '+ str(gen_para['dijet_order1_muA2018_all_dijet'].getVal())  +' + '+ str(gen_para['dijet_order2_muA2018_all_dijet'].getVal())  +'*TMath::Log10(@0/13000) ) '
    print(function)
    func_dijet = ROOT.RooGenericPdf( '%s_%s'%(func_name, '_all_dijet'), func_name, function, ROOT.RooArgList(mt_res))
    func_dijet.plotOn(frame,ROOT.RooFit.LineColor(ROOT.kRed),ROOT.RooFit.LineStyle(2))
    hpull_dijet2 = frame.pullHist()
    hpull_dijet2.SetLineColor(ROOT.kRed)
    hpull_dijet2.SetMarkerColor(ROOT.kRed)
    signal_norm2={}
    for ich in ['el2016', 'el2017', 'el2018', 'mu2016', 'mu2017', 'mu2018']:
        signal_norm2[ich] = ROOT.RooRealVar("signal_norm2_"+ich,"signal_norm_"+ich,0,100000)
        signal_norm2[ich].setVal(bkg_norm['r'].getVal()*signalyield[ich])
        signal_norm2[ich].setConstant()

    components_dijet = ROOT.RooArgList(func_dijet, signal_para['cb_MG_M'+mass+'_W'+width+'_el2016'], signal_para['cb_MG_M'+mass+'_W'+width+'_el2017'], signal_para['cb_MG_M'+mass+'_W'+width+'_el2018'], signal_para['cb_MG_M'+mass+'_W'+width+'_mu2016'], signal_para['cb_MG_M'+mass+'_W'+width+'_mu2017'], signal_para['cb_MG_M'+mass+'_W'+width+'_mu2018'])
    coeffs_dijet = ROOT.RooArgList(norm_totb,signal_norm2['el2016'],signal_norm2['el2017'],signal_norm2['el2018'],signal_norm2['mu2016'],signal_norm2['mu2017'],signal_norm2['mu2018'] )
    model_dijet = ROOT.RooAddPdf("model_dijet","f_all",components_dijet,coeffs_dijet)
    model_dijet.plotOn(frame,ROOT.RooFit.LineColor(ROOT.kRed),ROOT.RooFit.LineStyle(1))
    hpull_dijet = frame.pullHist()
    hpull_dijet.SetLineColor(ROOT.kRed)
    hpull_dijet.SetMarkerColor(ROOT.kRed)

    #add signals to the plot
    c = ROOT.TCanvas("c","c",0,53,800,740)
    ROOT.gStyle.SetOptStat(0)
    c.SetHighLightColor(2);
    c.Range(0,0,1,1);
    c.SetFillColor(0);
    c.SetBorderMode(0);
    c.SetBorderSize(2);
    c.SetTickx(1);
    c.SetTicky(1);
    c.SetLeftMargin(0.12);
    c.SetRightMargin(0.02);
    c.SetTopMargin(0.055);
    c.SetFrameFillStyle(0);
    c.SetFrameBorderMode(0);
    #------------>Primitives in pad: toppad
    toppad = ROOT.TPad('toppad','toppad',0,0.5 ,1.0,1.0)
    toppad.SetTickx(1);
    toppad.SetTicky(1);
    bottompad = ROOT.TPad('bottompad','bottompad',0,0.0,1.0,0.32)
    bottompad.SetTickx(1);
    bottompad.SetTicky(1);
    canvas_margin(c,toppad,bottompad)
    middlepad = ROOT.TPad('middlepad','middlepad',0,0.18,1.0,0.5)
    middlepad.SetTickx(1);
    middlepad.SetTicky(1);
    middlepad.SetTopMargin( 0.03 )
    middlepad.SetBottomMargin( 0.4 )
    middlepad.SetLeftMargin( 0.15 )
    middlepad.SetRightMargin( 0.03 )

    toppad.SetFillStyle(4000)
    toppad.SetFrameFillStyle(1000)
    toppad.SetFrameFillColor(0)
    toppad.SetFillColor(0)
    toppad.SetBorderMode(0)
    toppad.SetBorderSize(2)
    toppad.SetLogy()
    toppad.SetFrameBorderMode(0)
    toppad.SetFrameBorderMode(0)
    toppad.SetLeftMargin(0.15)
    bottompad.SetFillStyle(4000)
    bottompad.SetFrameFillStyle(1000)
    bottompad.SetFrameFillColor(0)
    bottompad.SetFillColor(0)
    bottompad.SetBorderMode(0)
    bottompad.SetBorderSize(2)
    bottompad.SetFrameBorderMode(0)
    bottompad.SetFrameBorderMode(0)
    middlepad.SetFillStyle(4000)
    middlepad.SetFrameFillStyle(1000)
    middlepad.SetFrameFillColor(0)
    middlepad.SetFillColor(0)
    middlepad.SetBorderMode(0)
    middlepad.SetBorderSize(2)
    middlepad.SetFrameBorderMode(0)
    middlepad.SetFrameBorderMode(0)
    toppad.Draw()
    middlepad.Draw()
    bottompad.Draw()

    c.cd()
    c.Update()
    c.RedrawAxis()
    cframe = c.GetFrame()
    cframe.Draw()
    toppad.cd()
    frame_4fa51a0__1 = ROOT.TH1D("frame_4fa51a0__1","Unbinned ML fit, %s %s"%(ch,year),NBIN_,MIN_,MAX_)
    frame_4fa51a0__1.GetXaxis().SetTitle("m_{T}^{l#nu#gamma} [GeV]");
    frame_4fa51a0__1.GetXaxis().SetLabelFont(42);
    frame_4fa51a0__1.GetXaxis().SetLabelSize(0.05);
    frame_4fa51a0__1.GetXaxis().SetTitleSize(0.05);
    frame_4fa51a0__1.GetXaxis().SetTitleOffset(1);
    frame_4fa51a0__1.GetXaxis().SetTitleFont(42);
    frame_4fa51a0__1.GetYaxis().SetTitle("Events / "+str((MAX_-MIN_)/NBIN_)+" GeV");
    frame_4fa51a0__1.GetYaxis().SetLabelFont(42);
    frame_4fa51a0__1.GetYaxis().SetLabelSize(0.05);
    frame_4fa51a0__1.GetYaxis().SetTitleSize(0.05);
    frame_4fa51a0__1.GetYaxis().SetTitleFont(42);
    frame_4fa51a0__1.GetYaxis().SetRangeUser(0.8e-2,1e4)
    frame_4fa51a0__1.GetXaxis().SetLabelOffset(999)
    frame_4fa51a0__1.GetXaxis().SetLabelSize(0)
    frame_4fa51a0__1.Draw("AXISSAME");
    frame.Draw("same E")
    frame_4fa51a0__1.Draw("AXISSAME");

    frame3 = mt_res.frame(ROOT.RooFit.Title("Pull Distribution"))
    frame3.addPlotable(hpull_dijet, "P")
    frame4 = mt_res.frame(ROOT.RooFit.Title("Pull Distribution"))
    frame4.addPlotable(hpull_vvdijet, "P")

    frame5 = mt_res.frame(ROOT.RooFit.Title("Pull Distribution"))
    frame5.addPlotable(hpull_dijet2, "P")
    frame6 = mt_res.frame(ROOT.RooFit.Title("Pull Distribution"))
    frame6.addPlotable(hpull_vvdijet2, "P")

    leg = ROOT.TLegend(0.25,0.73,0.6,0.85);
    leg.SetBorderSize(0);
    leg.SetLineStyle(1);
    leg.SetLineWidth(1);
    entry=leg.AddEntry(frame,"ToyData from Vvdijet-2","pe");
    entry.SetFillStyle(1001);
    entry.SetMarkerStyle(8);
    entry.SetMarkerSize(1.5);
    entry.SetLineStyle(1);
    entry.SetLineWidth(2);
    entry.SetTextFont(42);
    entry.SetTextSize(0.04);
    leg.Draw()


    leg2 = ROOT.TLegend(0.55,0.6,0.9,0.9);
    leg2.SetBorderSize(0);
    leg2.SetLineStyle(1);
    leg2.SetLineWidth(1);
    entry=leg2.AddEntry("","Dijet-2 + signal@600GeV (#Gamma_{X}/m_{X}=5%)","l");
    entry.SetFillStyle(1001);
    entry.SetLineStyle(1)
    entry.SetLineWidth(2)
    entry.SetLineColor(ROOT.kRed);
    entry.SetTextFont(42)
    entry.SetTextSize(0.04)
    entry=leg2.AddEntry("","Dijet-2","l");
    entry.SetFillStyle(1001);
    entry.SetLineStyle(9)
    entry.SetLineWidth(2)
    entry.SetLineColor(ROOT.kRed);
    entry.SetTextFont(42)
    entry.SetTextSize(0.04)
    entry=leg2.AddEntry("","Vvdijet-2 + signal@600GeV (#Gamma_{X}/m_{X}=5%)","l");
    entry.SetFillStyle(1001);
    entry.SetLineStyle(1)
    entry.SetLineWidth(2)
    entry.SetLineColor(ROOT.kAzure);
    entry.SetTextFont(42)
    entry.SetTextSize(0.04)
    entry=leg2.AddEntry("","Vvdijet-2","l");
    entry.SetFillStyle(1001);
    entry.SetLineStyle(9)
    entry.SetLineWidth(2)
    entry.SetLineColor(ROOT.kAzure);
    entry.SetTextFont(42)
    entry.SetTextSize(0.04)
    leg2.Draw()
    tex = ROOT.TLatex(0.98,0.94,"137 fb^{-1} (13 TeV)");
    tex.SetNDC();
    tex.SetTextAlign(31);
    tex.SetTextFont(42);
    tex.SetTextSize(0.05);
    tex.SetLineWidth(2);
    tex.Draw();
    tex2 = ROOT.TLatex(0.18,0.9,"CMS");
    tex2.SetNDC();
    tex2.SetTextAlign(13);
    tex2.SetTextFont(61);
    tex2.SetTextSize(0.06);
    tex2.SetLineWidth(2);
    tex2.Draw();
    bottompad.cd()
    frame_4fa51a0__2 = ROOT.TH1D("frame_4fa51a0__2","",NBIN_,MIN_,MAX_)
    frame_4fa51a0__2.GetXaxis().SetTitle("m_{T}^{l#nu#gamma} [GeV]");
    frame_4fa51a0__2.GetXaxis().SetLabelFont(42);
    frame_4fa51a0__2.GetXaxis().SetLabelSize(0.1);
    frame_4fa51a0__2.GetXaxis().SetTitleSize(0.1);
    frame_4fa51a0__2.GetXaxis().SetTitleOffset(1);
    frame_4fa51a0__2.GetXaxis().SetTitleFont(42);
    frame_4fa51a0__2.GetYaxis().SetTitle("#frac{Data-Fit}{#sigma_{Stat.}}");
    frame_4fa51a0__2.GetYaxis().CenterTitle()
    frame_4fa51a0__2.GetYaxis().SetLabelFont(42);
    frame_4fa51a0__2.GetYaxis().SetLabelSize(0.1);
    frame_4fa51a0__2.GetYaxis().SetTitleSize(0.1);
    frame_4fa51a0__2.GetYaxis().SetTitleFont(42);
    frame_4fa51a0__2.GetYaxis().SetRangeUser(-10,10)
    frame_4fa51a0__2.GetYaxis().SetNdivisions(5, 2, 0, ROOT.kTRUE)
    frame_4fa51a0__2.GetYaxis().SetTitleOffset(0.4)
    frame_4fa51a0__2.Draw("AXISSAME")
    frame3.Draw("same")
    frame4.Draw("same")
    frame_4fa51a0__2.Draw("AXISSAME")
    line = ROOT.TLine(200,0,2000,0);
    line.SetLineStyle(2)
    line.SetLineWidth(2)
    line.Draw()
    middlepad.cd()
    frame_4fa51a0__3 = ROOT.TH1D("frame_4fa51a0__3","",NBIN_,MIN_,MAX_)
    frame_4fa51a0__3.GetXaxis().SetTitle("m_{T}^{l#nu#gamma} [GeV]");
    frame_4fa51a0__3.GetXaxis().SetLabelFont(42);
    frame_4fa51a0__3.GetXaxis().SetLabelSize(0.01);
    frame_4fa51a0__3.GetXaxis().SetTitleSize(0.1);
    frame_4fa51a0__3.GetXaxis().SetTitleOffset(1);
    frame_4fa51a0__3.GetXaxis().SetTitleFont(42);
    frame_4fa51a0__3.GetYaxis().SetTitle("#frac{Data-BkgFit}{#sigma_{Stat.}}");
    frame_4fa51a0__3.GetYaxis().CenterTitle()
    frame_4fa51a0__3.GetYaxis().SetLabelFont(42);
    frame_4fa51a0__3.GetYaxis().SetLabelSize(0.1);
    frame_4fa51a0__3.GetYaxis().SetTitleSize(0.1);
    frame_4fa51a0__3.GetYaxis().SetTitleFont(42);
    frame_4fa51a0__3.GetYaxis().SetRangeUser(-10,10)
    frame_4fa51a0__3.GetYaxis().SetNdivisions(5, 2, 0, ROOT.kTRUE)
    frame_4fa51a0__3.GetYaxis().SetTitleOffset(0.4)
    frame_4fa51a0__3.Draw("AXISSAME")
    frame5.Draw("same")
    frame6.Draw("same")
    frame_4fa51a0__3.Draw("AXISSAME")
    line2 = ROOT.TLine(200,0,2000,0);
    line2.SetLineStyle(2)
    line2.SetLineWidth(2)
    line2.Draw()

    input('wait..')
    #c.SaveAs('fit_ALL%s.C' %(ch))



def makeFinalplots(baseDir,skimtree):

    #Reading Data, merge 3 years
    year ='ALL'
    MIN_=200
    MAX_=400
    NBIN_=100
    mt_res = ROOT.RooRealVar("mt_res", "mt_res", 200, 2200)
    mt_res.setBins(400)
    #mt_res.setRange( MIN_ ,MAX_)
    F=ROOT.TFile(baseDir+'/elALL_skim.root')
    tree=F.Get(skimtree)
    netot = tree.GetEntries()
    dse = ROOT.RooDataSet('data_elA'+year+'_mt_res_base', "dse", ROOT.RooArgSet(mt_res), ROOT.RooFit.Import(tree))
    F=ROOT.TFile(baseDir+'/muALL_skim.root')
    tree=F.Get(skimtree)
    nmtot = tree.GetEntries()
    dsm = ROOT.RooDataSet('data_muA'+year+'_mt_res_base', "dsm", ROOT.RooArgSet(mt_res), ROOT.RooFit.Import(tree))
    ne = dse.sumEntries("mt_res>"+str(MIN_))
    nm = dsm.sumEntries("mt_res>"+str(MIN_))

    #prepare Working Space with Roofit
    #ws_out  = ROOT.RooWorkspace( "workspace_all" )
    #rootfilename = '%s/%s/%s.root' %( data_outDir,year,ws_out.GetName() )


    #create 3 background pdfs
    func_name = 'dijet'
    function = 'TMath::Power( @0/13000., @1 + @2*TMath::Log10(@0/13000) )'
    dijet_order1_e = ROOT.RooRealVar('dijet_order1_elA'+year+'_all_dijet', "power1", -9, -100.0, -0.001)
    dijet_order2_e = ROOT.RooRealVar('dijet_order2_elA'+year+'_all_dijet', "power2", -2, -5.0, -0.01)
    dijet_order1_m = ROOT.RooRealVar('dijet_order1_muA'+year+'_all_dijet', "power1", -9, -100.0, -0.001)
    dijet_order2_m = ROOT.RooRealVar('dijet_order2_muA'+year+'_all_dijet', "power2", -2, -5.0, -0.01)
#    dijet_order1_e = ROOT.RooRealVar('dijet_order1_elA'+year+'_all_dijet', "power1", -9, -100.0, -0.001)
#    dijet_order2_e = ROOT.RooRealVar('dijet_order2_elA'+year+'_all_dijet', "power2", -2, -5.0, 10)
#    dijet_order1_m = ROOT.RooRealVar('dijet_order1_muA'+year+'_all_dijet', "power1", -9, -100.0, -0.001)
#    dijet_order2_m = ROOT.RooRealVar('dijet_order2_muA'+year+'_all_dijet', "power2", -2, -5.0, 10)

    func_dijet_e = ROOT.RooGenericPdf( '%s_%s'%(func_name, 'elA'+year+'_all_dijet'), func_name, function, ROOT.RooArgList(mt_res,dijet_order1_e,dijet_order2_e))
    func_dijet_m = ROOT.RooGenericPdf( '%s_%s'%(func_name, 'muA'+year+'_all_dijet'), func_name, function, ROOT.RooArgList(mt_res,dijet_order1_m,dijet_order2_m))

    func_name = 'vvdijet'
    function = 'TMath::Power( (1-@0/13000.), @1 ) / ( TMath::Power( @0/13000. , @2))'
    vvdijet_order1_e = ROOT.RooRealVar( 'vvdijet_order1_elA'+year+'_all_vvdijet', "power1", 40 ,      -50,  200)
    vvdijet_order2_e = ROOT.RooRealVar( 'vvdijet_order2_elA'+year+'_all_vvdijet', "power2", 2 ,     -10,   30)
    vvdijet_order1_m = ROOT.RooRealVar( 'vvdijet_order1_muA'+year+'_all_vvdijet', "power1", 40 ,      -50,  200)
    vvdijet_order2_m = ROOT.RooRealVar( 'vvdijet_order2_muA'+year+'_all_vvdijet', "power2", 2 ,     -10,   30)
    #vvdijet_order3_e = ROOT.RooRealVar( 'vvdijet_order3_elA'+year+'_all_vvdijet', "power3", 2 ,     -10,   30)
    #vvdijet_order3_m = ROOT.RooRealVar( 'vvdijet_order3_muA'+year+'_all_vvdijet', "power3", 2 ,     -10,   30)
    func_vvdijet_m = ROOT.RooGenericPdf( '%s_%s'%(func_name, 'muA'+year+'_all_vvdijet'), '%s_%s'%(func_name, 'muA'+year+'_all_vvdijet'), function, ROOT.RooArgList(mt_res, vvdijet_order1_m, vvdijet_order2_m))
    func_vvdijet_e = ROOT.RooGenericPdf( '%s_%s'%(func_name, 'elA'+year+'_all_vvdijet'), '%s_%s'%(func_name, 'elA'+year+'_all_vvdijet'), function, ROOT.RooArgList(mt_res, vvdijet_order1_e, vvdijet_order2_e))
 
    func_name = 'expow'
    function = 'TMath::Power( @0/13000., @2 ) * TMath::Exp( @1*@0/13000.)'

    expow_order2_e = ROOT.RooRealVar( 'expow_order2_elA'+year+'_all_expow', "power2", -2 ,      -100,  20)
    expow_order1_e = ROOT.RooRealVar( 'expow_order1_elA'+year+'_all_expow', "power1", -50 ,     -200,   50)
    expow_order2_m = ROOT.RooRealVar( 'expow_order2_muA'+year+'_all_expow', "power2", -2 ,      -100,  20)
    expow_order1_m = ROOT.RooRealVar( 'expow_order1_muA'+year+'_all_expow', "power1", -50 ,     -200,   50)
    func_expow_m = ROOT.RooGenericPdf( '%s_%s'%(func_name, 'muA'+year+'_all_expow'), '%s_%s'%(func_name, 'muA'+year+'_all_expow'), function, ROOT.RooArgList(mt_res, expow_order1_m, expow_order2_m))
    func_expow_e = ROOT.RooGenericPdf( '%s_%s'%(func_name, 'elA'+year+'_all_expow'), '%s_%s'%(func_name, 'elA'+year+'_all_expow'), function, ROOT.RooArgList(mt_res, expow_order1_e, expow_order2_e))

    # First we fit the pdfs to the data
    resu_dijet_e = func_dijet_e.fitTo(dse,ROOT.RooFit.Save(),ROOT.RooFit.SumW2Error(ROOT.kTRUE))
    resu_dijet_m = func_dijet_m.fitTo(dsm,ROOT.RooFit.Save(),ROOT.RooFit.SumW2Error(ROOT.kTRUE))
    resu_vvdijet_e = func_vvdijet_e.fitTo(dse,ROOT.RooFit.Save(),ROOT.RooFit.SumW2Error(ROOT.kTRUE))
    resu_vvdijet_m = func_vvdijet_m.fitTo(dsm,ROOT.RooFit.Save(),ROOT.RooFit.SumW2Error(ROOT.kTRUE))
    resu_expow_e = func_expow_e.fitTo(dse,ROOT.RooFit.Save(),ROOT.RooFit.SumW2Error(ROOT.kTRUE))
    resu_expow_m = func_expow_m.fitTo(dsm,ROOT.RooFit.Save(),ROOT.RooFit.SumW2Error(ROOT.kTRUE))
    print("===> fit result")
    resu_dijet_e.Print()
    print("===> fit result")
    resu_dijet_m.Print()
    print("===> fit result")
    resu_vvdijet_e.Print()
    print("===> fit result")
    resu_vvdijet_m.Print()
    print("===> fit result")
    resu_expow_e.Print()
    print("===> fit result")
    resu_expow_m.Print()


    catIndexe = ROOT.RooCategory('pdf_index_el'+year,'Index of Pdf which is active')
    mypdfse = ROOT.RooArgList("store")
    mypdfse.add(func_dijet_e)
    mypdfse.add(func_vvdijet_e)
    mypdfse.add(func_expow_e)
    catIndexm = ROOT.RooCategory('pdf_index_mu'+year,'Index of Pdf which is active')
    mypdfsm = ROOT.RooArgList("store")
    mypdfsm.add(func_dijet_m)
    mypdfsm.add(func_vvdijet_m)
    mypdfsm.add(func_expow_m)

    multipdfe = RooMultiPdf('MultiPdf_elA'+year+'_all_MultiPdf',"All Pdfs e",catIndexe, mypdfse)
    norm_MultiPdf_e = ROOT.RooRealVar('%s_norm' %( 'MultiPdf_elA'+year+'_all_MultiPdf' ),'normalization_e', ne,0,1000000 )
    multipdfm = RooMultiPdf('MultiPdf_muA'+year+'_all_MultiPdf',"All Pdfs m",catIndexm, mypdfsm)
    norm_MultiPdf_m = ROOT.RooRealVar('%s_norm' %( 'MultiPdf_muA'+year+'_all_MultiPdf' ),'normalization_m', nm,0,1000000 )

    #Generate toy with a specific function 
    singlefunc=False
    if singlefunc:
        func_name = 'toy'
        function = 'TMath::Power( (1-@0/13000.), @1 ) / ( TMath::Power( @0/13000. , @2+ @3*TMath::Log10(@0/13000)))'
        toy_vvdijet_order1_e = ROOT.RooRealVar( 'toy_vvdijet_order1_elA'+year+'_all_vvdijet', "power1", 40 ,      -100,  100)
        toy_vvdijet_order2_e = ROOT.RooRealVar( 'toy_vvdijet_order2_elA'+year+'_all_vvdijet', "power2", 2 ,     -50,   50)
        toy_vvdijet_order3_e = ROOT.RooRealVar( 'toy_vvdijet_order3_elA'+year+'_all_vvdijet', "power3", 2 ,     -50,   50)
        func_toy_vvdijet = ROOT.RooGenericPdf( 'toy_%s_%s'%(func_name, 'muA'+year+'_all_vvdijet'), '%s_%s'%(func_name, 'muA'+year+'_all_vvdijet'), function, ROOT.RooArgList(mt_res, toy_vvdijet_order1_e, toy_vvdijet_order2_e,toy_vvdijet_order3_e))
        func_toy_vvdijet.fitTo(dse,ROOT.RooFit.Save(),ROOT.RooFit.SumW2Error(ROOT.kTRUE)) 
        toydatae = func_toy_vvdijet.generate(ROOT.RooArgSet(mt_res),ne)
        func_toy_vvdijet.fitTo(dsm,ROOT.RooFit.Save(),ROOT.RooFit.SumW2Error(ROOT.kTRUE))
        toydatam = func_toy_vvdijet.generate(ROOT.RooArgSet(mt_res),nm)
        toydatae.SetName ('data_elA'+year+'_mt_res_base')
        toydatam.SetName ('data_muA'+year+'_mt_res_base')
        #import_workspace( ws_out, dse)
        #import_workspace( ws_out, dsm)
    else:
        frame_toy = mt_res.frame(ROOT.RooFit.Title("Unbinned ML fit, el"))
        dse.plotOn(frame_toy,ROOT.RooFit.DataError(ROOT.RooAbsData.SumW2))
        chi2score_e=[]
        multipdfse=[func_dijet_e,func_vvdijet_e,func_expow_e]
        multiresultse=[resu_dijet_e,resu_vvdijet_e,resu_expow_e]
        for toypdf in multipdfse:
            toypdf.plotOn(frame_toy)
            chi2score_e.append((frame_toy.chiSquare()))

        framm_toy = mt_res.frame(ROOT.RooFit.Title("Unbinned ML fit, el"))
        dsm.plotOn(framm_toy,ROOT.RooFit.DataError(ROOT.RooAbsData.SumW2))
        chi2score_m=[]
        multipdfsm=[func_dijet_m,func_vvdijet_m,func_expow_m]
        multiresultsm=[resu_dijet_m,resu_vvdijet_m,resu_expow_m]
        for toypdf in multipdfsm:
            toypdf.plotOn(framm_toy)
            chi2score_m.append((framm_toy.chiSquare()))
        rseed = ROOT.RooRandom.randomGenerator()
        rseed.SetSeed(123)
        toydatae = multipdfse[np.argmin(np.abs(chi2score_e))].generate(ROOT.RooArgSet(mt_res),ne)
        toydatam = multipdfsm[np.argmin(np.abs(chi2score_m))].generate(ROOT.RooArgSet(mt_res),nm)
        print('------> score: ', chi2score_e, chi2score_m)
        print('------------> set index to e: ', np.argmin(np.abs(chi2score_e)), ' m: ', np.argmin(np.abs(chi2score_m)))
        catIndexe.setIndex(np.argmin(np.abs(chi2score_e)))
        catIndexm.setIndex(np.argmin(np.abs(chi2score_m)))
        toydatae.SetName ('data_elA'+year+'_mt_res_base')
        toydatam.SetName ('data_muA'+year+'_mt_res_base')
        #import_workspace( ws_out, toydatae)
        #import_workspace( ws_out, toydatam)
        #import_workspace( ws_out, dse)
        #import_workspace( ws_out, dsm)

    frame_e = mt_res.frame(ROOT.RooFit.Title("Unbinned ML fit, el"))
    frame_m = mt_res.frame(ROOT.RooFit.Title("Unbinned ML fit, mu"))

    #add signals to the plot
    widthlist=['5','0p01']
    masslist=['600', '1000', '1600']
    normalizationlist = {
        "el":{
            "5":{
                "600":{"norm":100,"linecolor":ROOT.kRed,"linestyle":9,
                },
                "1000":{"norm":100,"linecolor":ROOT.kViolet,"linestyle":9,
                },
                "1600":{"norm":100,"linecolor":ROOT.kAzure,"linestyle":9,
                },
            },
            "0p01":{
                "600":{"norm":100,"linecolor":ROOT.kRed,"linestyle":1,
                },
                "1000":{"norm":100,"linecolor":ROOT.kViolet,"linestyle":1,
                },
                "1600":{"norm":100,"linecolor":ROOT.kAzure,"linestyle":1,
                },
            }
        },
        "mu":{
            "5":{
                "600":{"norm":100,"linecolor":ROOT.kRed,"linestyle":9,
                },
                "1000":{"norm":100,"linecolor":ROOT.kViolet,"linestyle":9,
                },
                "1600":{"norm":100,"linecolor":ROOT.kAzure,"linestyle":9,
                },
            },
            "0p01":{
                "600":{"norm":100,"linecolor":ROOT.kRed,"linestyle":1,
                },
                "1000":{"norm":100,"linecolor":ROOT.kViolet,"linestyle":1,
                },
                "1600":{"norm":100,"linecolor":ROOT.kAzure,"linestyle":1,
                },
            }
        }
    }
    for ch in ["el","mu"]:
        for iwid in widthlist:
            for imass in masslist:
                year='2018'
                inputfile0 = 'data_env/sigfit/'+year+'/wssignal_M'+imass+'_W'+iwid+'_'+ch+'.root'
                wsname = "wssignal_M"+imass+"_W"+iwid+"_"+ch
                print(inputfile0, " : ", wsname)
                ifile0 = ROOT.TFile.Open( inputfile0, 'READ' )
                if not ifile0:
                    return
                ws_in0 = ifile0.Get( wsname )
                pdfname = 'cb_MG_M%s_W%s_%s%s' %(imass,iwid,ch,year)
                sigModel0 = ws_in0.pdf(pdfname)
                print(normalizationlist[ch][iwid][imass])
                if 'el' in ch:
                    sigModel0.plotOn(frame_e,ROOT.RooFit.DataError(ROOT.RooAbsData.Poisson),ROOT.RooFit.LineColor(normalizationlist[ch][iwid][imass]['linecolor']),ROOT.RooFit.LineStyle(normalizationlist[ch][iwid][imass]['linestyle']), ROOT.RooFit.Normalization(normalizationlist[ch][iwid][imass]['norm'],ROOT.RooAbsReal.NumEvent))#,ROOT.RooFit.LineColor(normalizationlist[ch][iwid][imass]['linecolor']),ROOT.RooFit.LineStyle(ROOT.RooFit.LineColor(normalizationlist[ch][iwid][imass]['linestyle']) ))
                if 'mu' in ch:
                    sigModel0.plotOn(frame_m,ROOT.RooFit.DataError(ROOT.RooAbsData.Poisson),ROOT.RooFit.LineColor(normalizationlist[ch][iwid][imass]['linecolor']),ROOT.RooFit.LineStyle(normalizationlist[ch][iwid][imass]['linestyle']), ROOT.RooFit.Normalization(normalizationlist[ch][iwid][imass]['norm'],ROOT.RooAbsReal.NumEvent))

    dse.plotOn(frame_e,ROOT.RooFit.DataError(ROOT.RooAbsData.SumW2))
    dsm.plotOn(frame_m,ROOT.RooFit.DataError(ROOT.RooAbsData.SumW2))
#    toydatae.plotOn(frame_e,ROOT.RooFit.DataError(ROOT.RooAbsData.Poisson))
#    toydatam.plotOn(frame_m,ROOT.RooFit.DataError(ROOT.RooAbsData.Poisson))
    multipdfse[np.argmin(np.abs(chi2score_e))].plotOn(frame_e, ROOT.RooFit.VisualizeError(multiresultse[np.argmin(np.abs(chi2score_e))], 2), ROOT.RooFit.FillColor(ROOT.kYellow))
    multipdfsm[np.argmin(np.abs(chi2score_m))].plotOn(frame_m, ROOT.RooFit.VisualizeError(multiresultsm[np.argmin(np.abs(chi2score_m))], 2), ROOT.RooFit.FillColor(ROOT.kYellow))
    multipdfse[np.argmin(np.abs(chi2score_e))].plotOn(frame_e, ROOT.RooFit.VisualizeError(multiresultse[np.argmin(np.abs(chi2score_e))], 1), ROOT.RooFit.FillColor(ROOT.kGreen))
    multipdfsm[np.argmin(np.abs(chi2score_m))].plotOn(frame_m, ROOT.RooFit.VisualizeError(multiresultsm[np.argmin(np.abs(chi2score_m))], 1), ROOT.RooFit.FillColor(ROOT.kGreen))
    multipdfse[np.argmin(np.abs(chi2score_e))].plotOn(frame_e)
    multipdfsm[np.argmin(np.abs(chi2score_m))].plotOn(frame_m)
    dse.plotOn(frame_e,ROOT.RooFit.DataError(ROOT.RooAbsData.SumW2))
    dsm.plotOn(frame_m,ROOT.RooFit.DataError(ROOT.RooAbsData.SumW2))
#    toydatae.plotOn(frame_e,ROOT.RooFit.DataError(ROOT.RooAbsData.Poisson))
#    toydatam.plotOn(frame_m,ROOT.RooFit.DataError(ROOT.RooAbsData.Poisson))

    print("sum Entries: ", toydatae.sumEntries(), toydatam.sumEntries())

    for ch, frame in zip(["el","mu"],[frame_e, frame_m]):
        c = ROOT.TCanvas("c","c",0,53,800,740)
        ROOT.gStyle.SetOptStat(0)
        c.SetHighLightColor(2);
        c.Range(0,0,1,1);
        c.SetFillColor(0);
        c.SetBorderMode(0);
        c.SetBorderSize(2);
        c.SetTickx(1);
        c.SetTicky(1);
        c.SetLeftMargin(0.12);
        c.SetRightMargin(0.02);
        c.SetTopMargin(0.055);
        c.SetFrameFillStyle(0);
        c.SetFrameBorderMode(0);
        #------------>Primitives in pad: toppad
        toppad = ROOT.TPad('toppad','toppad',0,0.3 ,1.0,1.0)
        toppad.SetTickx(1);
        toppad.SetTicky(1);
        bottompad = ROOT.TPad('bottompad','bottompad',0,0.0,1.0,0.32)
        bottompad.SetTickx(1);
        bottompad.SetTicky(1);
        canvas_margin(c,toppad,bottompad)
        toppad.SetFillStyle(4000)
        toppad.SetFrameFillStyle(1000)
        toppad.SetFrameFillColor(0)
        toppad.SetFillColor(0)
        toppad.SetBorderMode(0)
        toppad.SetBorderSize(2)
        #toppad.SetLogy()
        toppad.SetFrameBorderMode(0)
        toppad.SetFrameBorderMode(0)
        toppad.SetLeftMargin(0.15)
        bottompad.SetFillStyle(4000)
        bottompad.SetFrameFillStyle(1000)
        bottompad.SetFrameFillColor(0)
        bottompad.SetFillColor(0)
        bottompad.SetBorderMode(0)
        bottompad.SetBorderSize(2)
        bottompad.SetFrameBorderMode(0)
        bottompad.SetFrameBorderMode(0)
        toppad.Draw()
        bottompad.Draw()

        c.cd()
        c.Update()
        c.RedrawAxis()
        cframe = c.GetFrame()
        cframe.Draw()
        toppad.cd()
        frame_4fa51a0__1 = ROOT.TH1D("frame_4fa51a0__1","Unbinned ML fit, %s %s"%(ch,year),NBIN_,MIN_,MAX_)
        frame_4fa51a0__1.GetXaxis().SetTitle("m_{T}^{l#nu#gamma} [GeV]");
        frame_4fa51a0__1.GetXaxis().SetLabelFont(42);
        frame_4fa51a0__1.GetXaxis().SetLabelSize(0.05);
        frame_4fa51a0__1.GetXaxis().SetTitleSize(0.05);
        frame_4fa51a0__1.GetXaxis().SetTitleOffset(1);
        frame_4fa51a0__1.GetXaxis().SetTitleFont(42);
        frame_4fa51a0__1.GetYaxis().SetTitle("Events / 20 GeV");
        frame_4fa51a0__1.GetYaxis().SetLabelFont(42);
        frame_4fa51a0__1.GetYaxis().SetLabelSize(0.05);
        frame_4fa51a0__1.GetYaxis().SetTitleSize(0.05);
        frame_4fa51a0__1.GetYaxis().SetTitleFont(42);
        frame_4fa51a0__1.GetYaxis().SetRangeUser(0.8e-2,1e4)
        frame_4fa51a0__1.GetXaxis().SetLabelOffset(999)
        frame_4fa51a0__1.GetXaxis().SetLabelSize(0)
        frame_4fa51a0__1.Draw("AXISSAME");
        frame.Draw("same E")

        hpull = frame.pullHist()
        frame3 = mt_res.frame(ROOT.RooFit.Title("Pull Distribution"))
        frame3.addPlotable(hpull, "P")

        leg = ROOT.TLegend(0.25,0.7,0.65,0.9);
        leg.SetBorderSize(0);
        leg.SetLineStyle(1);
        leg.SetLineWidth(1);
        entry=leg.AddEntry(frame,"ToyData","pe");
        entry.SetFillStyle(1001);
        entry.SetMarkerStyle(8);
        entry.SetMarkerSize(1.5);
        entry.SetLineStyle(1);
        entry.SetLineWidth(2);
        entry.SetTextFont(42);
        entry.SetTextSize(0.03);
        entry=leg.AddEntry("","Data fit","l");
        entry.SetFillStyle(1001);
        entry.SetLineStyle(1)
        entry.SetLineWidth(2)
        entry.SetLineColor(ROOT.kBlue);
        entry.SetMarkerStyle(20)
        entry.SetTextFont(42)
        entry.SetTextSize(0.03)
        htmp=ROOT.TH1F("htmp","htmp",10,0,1)
        htmp.SetFillColor(ROOT.kGreen)
        entry=leg.AddEntry(htmp,"Fit uncert. 68% CL","f");
        entry.SetFillStyle(1001)
        entry.SetLineStyle(1)
        entry.SetLineWidth(2)
        entry.SetMarkerStyle(20)
        entry.SetTextFont(42)
        entry.SetTextSize(0.03)
        htmp2=ROOT.TH1F("htmp2","htmp2",10,0,1)
        htmp2.SetFillColor(ROOT.kYellow)
        entry=leg.AddEntry(htmp2,"Fit uncert. 95% CL","f");
        entry.SetFillStyle(1001)
        entry.SetLineStyle(1)
        entry.SetLineWidth(2)
        entry.SetMarkerStyle(20)
        entry.SetTextFont(42)
        entry.SetTextSize(0.03)
        leg.Draw()


        leg2 = ROOT.TLegend(0.55,0.5,0.9,0.9);
        leg2.SetBorderSize(0);
        leg2.SetLineStyle(1);
        leg2.SetLineWidth(1);
        entry=leg2.AddEntry("","Signal 600GeV, narrow","l");
        entry.SetFillStyle(1001);
        entry.SetLineStyle(1)
        entry.SetLineWidth(2)
    print(selection)
    exit()
    print('make histo')
    Hmt = myfilter.Histo1D("mt_res")
    Hmt.Draw()
    myfilter.Snapshot(skimtree, skimfile)


def ShowSignalInjection():
    toyfile = '/data/users/yihuilai/test_code/WG_Analysis/Plotting/data_env/test_Dec20_testsignal_inject/Width5/all/Mass600/higgsCombine_test7.GenerateOnly.mH600.9024.root'
    fitpara = '/data/users/yihuilai/test_code/WG_Analysis/Plotting/data_env/test_Dec20_testsignal_inject/Width5/all/Mass600/fitDiagnostics_test7.root'
    # 1000 5%
    signalyield={'el2016':55.7951, 'mu2016':61.6212, 'el2017':61.4791, 'mu2017':67.3945, 'el2018':92.9473, 'mu2018':102.755}
    # 600 5%
    signalyield={'el2016':150.106, 'mu2016':177.152, 'el2017':170.551, 'mu2017':199.071, 'el2018':254.791, 'mu2018':302.308}
    injects = 1
    mass = '600'
    width = '5'

    year ='ALL'
    MIN_=220
    MAX_=2200
    NBIN_=100
    mt_res = ROOT.RooRealVar("mt_res", "mt_res", MIN_, MAX_)
    mt_res.setBins(NBIN_)

    # Get toy data
    F=ROOT.TFile(toyfile)
    toydata=F.Get("toys/toy_1")
    ne = toydata.sumEntries()
    print(ne)

    # Fit function
    fit_para={}
    year='2016'
    fit_para['vvdijet_order1_elA'+year+'_all_vvdijet'] = ROOT.RooRealVar('vvdijet_order1_elA'+year+'_all_vvdijet', "power1", -9, -1000, 1000)
    fit_para['vvdijet_order2_elA'+year+'_all_vvdijet'] = ROOT.RooRealVar('vvdijet_order2_elA'+year+'_all_vvdijet', "power2", -2, -1000, 1000)
    fit_para['vvdijet_order1_muA'+year+'_all_vvdijet'] = ROOT.RooRealVar('vvdijet_order1_muA'+year+'_all_vvdijet', "power1", -9, -1000, 1000)
    fit_para['vvdijet_order2_muA'+year+'_all_vvdijet'] = ROOT.RooRealVar('vvdijet_order2_muA'+year+'_all_vvdijet', "power2", -2, -1000, 1000)
    year='2017'
    fit_para['vvdijet_order1_elA'+year+'_all_vvdijet'] = ROOT.RooRealVar('vvdijet_order1_elA'+year+'_all_vvdijet', "power1", -9, -1000, 1000)
    fit_para['vvdijet_order2_elA'+year+'_all_vvdijet'] = ROOT.RooRealVar('vvdijet_order2_elA'+year+'_all_vvdijet', "power2", -2, -1000, 1000)
    fit_para['vvdijet_order1_muA'+year+'_all_vvdijet'] = ROOT.RooRealVar('vvdijet_order1_muA'+year+'_all_vvdijet', "power1", -9, -1000, 1000)
    fit_para['vvdijet_order2_muA'+year+'_all_vvdijet'] = ROOT.RooRealVar('vvdijet_order2_muA'+year+'_all_vvdijet', "power2", -2, -1000, 1000)
    year='2018'
    fit_para['vvdijet_order1_elA'+year+'_all_vvdijet'] = ROOT.RooRealVar('vvdijet_order1_elA'+year+'_all_vvdijet', "power1", -9, -1000, 1000)
    fit_para['vvdijet_order2_elA'+year+'_all_vvdijet'] = ROOT.RooRealVar('vvdijet_order2_elA'+year+'_all_vvdijet', "power2", -2, -1000, 1000)
    fit_para['vvdijet_order1_muA'+year+'_all_vvdijet'] = ROOT.RooRealVar('vvdijet_order1_muA'+year+'_all_vvdijet', "power1", -9, -1000, 1000)
    fit_para['vvdijet_order2_muA'+year+'_all_vvdijet'] = ROOT.RooRealVar('vvdijet_order2_muA'+year+'_all_vvdijet', "power2", -2, -1000, 1000)

    # generate function
    gen_para={}
    year='2016'
    gen_para['dijet_order1_elA'+year+'_all_dijet'] = ROOT.RooRealVar('dijet_order1_elA'+year+'_all_dijet', "power1", -9, -1000, 1000)
    gen_para['dijet_order2_elA'+year+'_all_dijet'] = ROOT.RooRealVar('dijet_order2_elA'+year+'_all_dijet', "power2", -2, -1000, 1000)
    gen_para['dijet_order1_muA'+year+'_all_dijet'] = ROOT.RooRealVar('dijet_order1_muA'+year+'_all_dijet', "power1", -9, -1000, 1000)
    gen_para['dijet_order2_muA'+year+'_all_dijet'] = ROOT.RooRealVar('dijet_order2_muA'+year+'_all_dijet', "power2", -2, -1000, 1000)
    year='2017'
    gen_para['dijet_order1_elA'+year+'_all_dijet'] = ROOT.RooRealVar('dijet_order1_elA'+year+'_all_dijet', "power1", -9, -1000, 1000)
    gen_para['dijet_order2_elA'+year+'_all_dijet'] = ROOT.RooRealVar('dijet_order2_elA'+year+'_all_dijet', "power2", -2, -1000, 1000)
    gen_para['dijet_order1_muA'+year+'_all_dijet'] = ROOT.RooRealVar('dijet_order1_muA'+year+'_all_dijet', "power1", -9, -1000, 1000)
    gen_para['dijet_order2_muA'+year+'_all_dijet'] = ROOT.RooRealVar('dijet_order2_muA'+year+'_all_dijet', "power2", -2, -1000, 1000)
    year='2018'
    gen_para['dijet_order1_elA'+year+'_all_dijet'] = ROOT.RooRealVar('dijet_order1_elA'+year+'_all_dijet', "power1", -9, -1000, 1000)
    gen_para['dijet_order2_elA'+year+'_all_dijet'] = ROOT.RooRealVar('dijet_order2_elA'+year+'_all_dijet', "power2", -2, -1000, 1000)
    gen_para['dijet_order1_muA'+year+'_all_dijet'] = ROOT.RooRealVar('dijet_order1_muA'+year+'_all_dijet', "power1", -9, -1000, 1000)
    gen_para['dijet_order2_muA'+year+'_all_dijet'] = ROOT.RooRealVar('dijet_order2_muA'+year+'_all_dijet', "power2", -2, -1000, 1000)

    bkg_norm = {}
    bkg_norm['r_gen'] = ROOT.RooRealVar('r_gen','r_gen',0,100000)
    bkg_norm['r_gen'].setVal(injects)
    bkg_norm['r_gen'].setConstant()
    bkg_norm['r_gen'].setError(0)
    bkgyield={'el2016':1479, 'mu2016':1777, 'el2017':2248, 'mu2017':2237, 'el2018':3433, 'mu2018':3302}
    for ich in ['el2016', 'el2017', 'el2018', 'mu2016', 'mu2017', 'mu2018']:
        bkg_norm['shapeBkg_genAll_'+ich+'__norm'] = ROOT.RooRealVar('shapeBkg_genAll_'+ich+'__norm','N_'+ich,0,100000)
        bkg_norm['shapeBkg_genAll_'+ich+'__norm'].setVal(bkgyield[ich])
        bkg_norm['shapeBkg_genAll_'+ich+'__norm'].setConstant()
        bkg_norm['shapeBkg_All_'+ich+'__norm'] = ROOT.RooRealVar('shapeBkg_genAll_'+ich+'__norm','N_'+ich,0,100000)

    bkg_norm['r'] = ROOT.RooRealVar('r','r',0,100000)

    # Signal
    signal_para = {}
    signal_para['cb_cut2_MG'] = ROOT.RooRealVar('cb_cut2_MG','cb_cut2_MG',-100,100)
    signal_para['cb_cut2_MG'].setVal(1.6)
    signal_para['cb_cut2_MG'].setConstant()
    signal_para['cb_pow1_MG'] = ROOT.RooRealVar('cb_powe1_MG','cb_power1_MG',-100,100)
    signal_para['cb_pow1_MG'].setVal(2.2)
    signal_para['cb_pow1_MG'].setConstant()
    signal_para['cb_pow2_MG'] = ROOT.RooRealVar('cb_powe2_MG','cb_power2_MG',-100,100)
    signal_para['cb_pow2_MG'].setVal(1.4)
    signal_para['cb_pow2_MG'].setConstant()
    for ich in ['el2016', 'el2017', 'el2018', 'mu2016', 'mu2017', 'mu2018']:
        signal_para['cb_cut1_MG_M'+mass+'_W'+width+'_'+ich] = ROOT.RooRealVar('cb_cut1_MG_M'+mass+'_W'+width+'_'+ich,'cb_cut1_MG_M'+mass+'_W'+width+'_'+ich,-100,10000)
        signal_para['cb_mass_MG_M'+mass+'_W'+width+'_'+ich] = ROOT.RooRealVar('cb_mass_MG_M'+mass+'_W'+width+'_'+ich,'cb_mass_MG_M'+mass+'_W'+width+'_'+ich,-100,10000)
        signal_para['cb_sigma_MG_M'+mass+'_W'+width+'_'+ich] = ROOT.RooRealVar('cb_sigma_MG_M'+mass+'_W'+width+'_'+ich,'cb_sigma_MG_M'+mass+'_W'+width+'_'+ich,-100,10000)
        signal_para['cb_MG_M'+mass+'_W'+width+'_'+ich] = ROOT.RooDoubleCB('cb_MG_M'+mass+'_W'+width+'_'+ich, 'Double Sided Crystal Ball Lineshape', mt_res, signal_para['cb_mass_MG_M'+mass+'_W'+width+'_'+ich], signal_para['cb_sigma_MG_M'+mass+'_W'+width+'_'+ich], signal_para['cb_cut1_MG_M'+mass+'_W'+width+'_'+ich], signal_para['cb_pow1_MG'], signal_para['cb_cut2_MG'],  signal_para['cb_pow2_MG'])

    print(fit_para.keys())
    print(gen_para.keys())
    # Get fit function
    f=ROOT.TFile(fitpara)
    res = f.Get("fit_s")
    fitargs=res.floatParsFinal()
    iter = fitargs.createIterator()
    a=iter.Next()
    while not a == 0:
        print(a.GetName())
        print(a.getVal())
        #print(a.getError())
        for ipa in fit_para.keys():
            if a.GetName()== ipa:
                fit_para[ipa].setVal(a.getVal())
                fit_para[ipa].setConstant()
                fit_para[ipa].setError(a.getError())
        for ipa in gen_para.keys():
            if a.GetName()== ipa:
                gen_para[ipa].setVal(a.getVal())
                gen_para[ipa].setConstant()
                gen_para[ipa].setError(a.getError())
        for ipa in bkg_norm.keys():
            if a.GetName()== ipa:
                bkg_norm[ipa].setVal(a.getVal())
                bkg_norm[ipa].setConstant()
                bkg_norm[ipa].setError(a.getError())
        for ipa in signal_para.keys():
            if a.GetName()== ipa:
                print('get ', ipa, a.getVal())
                signal_para[ipa].setVal(a.getVal())
                signal_para[ipa].setConstant()
                signal_para[ipa].setError(a.getError())
        if a.GetName()=='r':
            print('========> get r ', a.getVal())
            bkg_norm['r'].setVal(a.getVal())
            bkg_norm['r'].setConstant()
        if a.GetName()=='vvdijet_order2_muA2018_all_vvdijet':
            break
        else:
            a=iter.Next()

    # vvdijet
    frame = mt_res.frame(ROOT.RooFit.Title("Unbinned ML fit"))
    toydata.plotOn(frame)
    func_name = 'vvdijet'
    function = str(bkg_norm['shapeBkg_genAll_el2016__norm'].getVal()) + '*TMath::Power( (1-@0/13000.), '+ str(fit_para['vvdijet_order1_elA2016_all_vvdijet'].getVal())  +' ) / ( TMath::Power( @0/13000. , '+ str(fit_para['vvdijet_order2_elA2016_all_vvdijet'].getVal())  +'))'
    function += '+'+str(bkg_norm['shapeBkg_genAll_el2017__norm'].getVal()) + '*TMath::Power( (1-@0/13000.), '+ str(fit_para['vvdijet_order1_elA2017_all_vvdijet'].getVal())  +' ) / ( TMath::Power( @0/13000. , '+ str(fit_para['vvdijet_order2_elA2017_all_vvdijet'].getVal())  +'))'
    function += '+'+str(bkg_norm['shapeBkg_genAll_el2018__norm'].getVal()) + '*TMath::Power( (1-@0/13000.), '+ str(fit_para['vvdijet_order1_elA2018_all_vvdijet'].getVal())  +' ) / ( TMath::Power( @0/13000. , '+ str(fit_para['vvdijet_order2_elA2018_all_vvdijet'].getVal())  +'))'
    function += '+'+str(bkg_norm['shapeBkg_genAll_mu2016__norm'].getVal()) + '*TMath::Power( (1-@0/13000.), '+ str(fit_para['vvdijet_order1_muA2016_all_vvdijet'].getVal())  +' ) / ( TMath::Power( @0/13000. , '+ str(fit_para['vvdijet_order2_muA2016_all_vvdijet'].getVal())  +'))'
    function += '+'+str(bkg_norm['shapeBkg_genAll_mu2017__norm'].getVal()) + '*TMath::Power( (1-@0/13000.), '+ str(fit_para['vvdijet_order1_muA2017_all_vvdijet'].getVal())  +' ) / ( TMath::Power( @0/13000. , '+ str(fit_para['vvdijet_order2_muA2017_all_vvdijet'].getVal())  +'))'
    function += '+'+str(bkg_norm['shapeBkg_genAll_mu2018__norm'].getVal()) + '*TMath::Power( (1-@0/13000.), '+ str(fit_para['vvdijet_order1_muA2018_all_vvdijet'].getVal())  +' ) / ( TMath::Power( @0/13000. , '+ str(fit_para['vvdijet_order2_muA2018_all_vvdijet'].getVal())  +'))'
    print(function)
    func_vvdijet = ROOT.RooGenericPdf( '%s_%s'%(func_name, '_all_vvdijet'), func_name, function, ROOT.RooArgList(mt_res))
    func_vvdijet.plotOn(frame,ROOT.RooFit.LineColor(ROOT.kBlue),ROOT.RooFit.LineStyle(2))
    hpull_vvdijet2 = frame.pullHist()
    hpull_vvdijet2.SetLineColor(ROOT.kBlue)
    hpull_vvdijet2.SetMarkerColor(ROOT.kBlue)

    norm_totb = ROOT.RooRealVar("norm_vvdijetb","norm_vvdijetb",0,100000);
    norm_totb.setVal(bkg_norm['shapeBkg_All_el2016__norm'].getVal()+bkg_norm['shapeBkg_All_mu2016__norm'].getVal()+bkg_norm['shapeBkg_All_el2017__norm'].getVal()+bkg_norm['shapeBkg_All_mu2017__norm'].getVal()+bkg_norm['shapeBkg_All_el2018__norm'].getVal()+bkg_norm['shapeBkg_All_mu2018__norm'].getVal())
    norm_totb.setConstant()

    signal_norm={}

    for ich in ['el2016', 'el2017', 'el2018', 'mu2016', 'mu2017', 'mu2018']:
        signal_norm[ich] = ROOT.RooRealVar("signal_norm_"+ich,"signal_norm_"+ich,0,100000)
        signal_norm[ich].setVal(bkg_norm['r_gen'].getVal()*signalyield[ich])
        signal_norm[ich].setConstant()

    components_vvdijet = ROOT.RooArgList(func_vvdijet, signal_para['cb_MG_M'+mass+'_W'+width+'_el2016'], signal_para['cb_MG_M'+mass+'_W'+width+'_el2017'], signal_para['cb_MG_M'+mass+'_W'+width+'_el2018'], signal_para['cb_MG_M'+mass+'_W'+width+'_mu2016'], signal_para['cb_MG_M'+mass+'_W'+width+'_mu2017'], signal_para['cb_MG_M'+mass+'_W'+width+'_mu2018'])
    coeffs_vvdijet = ROOT.RooArgList(norm_totb,signal_norm['el2016'],signal_norm['el2017'],signal_norm['el2018'],signal_norm['mu2016'],signal_norm['mu2017'],signal_norm['mu2018'] )
    model_vvdijet = ROOT.RooAddPdf("model_vvdijet","f_all",components_vvdijet,coeffs_vvdijet)
    model_vvdijet.plotOn(frame,ROOT.RooFit.LineColor(ROOT.kBlue),ROOT.RooFit.LineStyle(1))
    hpull_vvdijet = frame.pullHist()
    hpull_vvdijet.SetLineColor(ROOT.kBlue)
    hpull_vvdijet.SetMarkerColor(ROOT.kBlue)

    # dijet
    func_name = 'dijet'
    function = str(bkg_norm['shapeBkg_All_el2016__norm'].getVal()) + ' *TMath::Power( @0/13000., '+ str(gen_para['dijet_order1_elA2016_all_dijet'].getVal())  +' + '+ str(gen_para['dijet_order2_elA2016_all_dijet'].getVal())  +'*TMath::Log10(@0/13000) ) '
    function += ' +'+str(bkg_norm['shapeBkg_All_el2017__norm'].getVal()) +'*TMath::Power( @0/13000., '+ str(gen_para['dijet_order1_elA2017_all_dijet'].getVal())  +' + '+ str(gen_para['dijet_order2_elA2017_all_dijet'].getVal())  +'*TMath::Log10(@0/13000) ) '
    function += ' +'+str(bkg_norm['shapeBkg_All_el2018__norm'].getVal()) +'*TMath::Power( @0/13000., '+ str(gen_para['dijet_order1_elA2018_all_dijet'].getVal())  +' + '+ str(gen_para['dijet_order2_elA2018_all_dijet'].getVal())  +'*TMath::Log10(@0/13000) ) '
    function += '+'+str(bkg_norm['shapeBkg_All_mu2016__norm'].getVal()) + ' *TMath::Power( @0/13000., '+ str(gen_para['dijet_order1_muA2016_all_dijet'].getVal())  +' + '+ str(gen_para['dijet_order2_muA2016_all_dijet'].getVal())  +'*TMath::Log10(@0/13000) ) '
    function += ' +'+str(bkg_norm['shapeBkg_All_mu2017__norm'].getVal()) +'*TMath::Power( @0/13000., '+ str(gen_para['dijet_order1_muA2017_all_dijet'].getVal())  +' + '+ str(gen_para['dijet_order2_muA2017_all_dijet'].getVal())  +'*TMath::Log10(@0/13000) ) '
    function += ' +'+str(bkg_norm['shapeBkg_All_mu2018__norm'].getVal()) +'*TMath::Power( @0/13000., '+ str(gen_para['dijet_order1_muA2018_all_dijet'].getVal())  +' + '+ str(gen_para['dijet_order2_muA2018_all_dijet'].getVal())  +'*TMath::Log10(@0/13000) ) '
    print(function)
    func_dijet = ROOT.RooGenericPdf( '%s_%s'%(func_name, '_all_dijet'), func_name, function, ROOT.RooArgList(mt_res))
    func_dijet.plotOn(frame,ROOT.RooFit.LineColor(ROOT.kRed),ROOT.RooFit.LineStyle(2))
    hpull_dijet2 = frame.pullHist()
    hpull_dijet2.SetLineColor(ROOT.kRed)
    hpull_dijet2.SetMarkerColor(ROOT.kRed)
    signal_norm2={}
    for ich in ['el2016', 'el2017', 'el2018', 'mu2016', 'mu2017', 'mu2018']:
        signal_norm2[ich] = ROOT.RooRealVar("signal_norm2_"+ich,"signal_norm_"+ich,0,100000)
        signal_norm2[ich].setVal(bkg_norm['r'].getVal()*signalyield[ich])
        signal_norm2[ich].setConstant()

    components_dijet = ROOT.RooArgList(func_dijet, signal_para['cb_MG_M'+mass+'_W'+width+'_el2016'], signal_para['cb_MG_M'+mass+'_W'+width+'_el2017'], signal_para['cb_MG_M'+mass+'_W'+width+'_el2018'], signal_para['cb_MG_M'+mass+'_W'+width+'_mu2016'], signal_para['cb_MG_M'+mass+'_W'+width+'_mu2017'], signal_para['cb_MG_M'+mass+'_W'+width+'_mu2018'])
    coeffs_dijet = ROOT.RooArgList(norm_totb,signal_norm2['el2016'],signal_norm2['el2017'],signal_norm2['el2018'],signal_norm2['mu2016'],signal_norm2['mu2017'],signal_norm2['mu2018'] )
    model_dijet = ROOT.RooAddPdf("model_dijet","f_all",components_dijet,coeffs_dijet)
    model_dijet.plotOn(frame,ROOT.RooFit.LineColor(ROOT.kRed),ROOT.RooFit.LineStyle(1))
    hpull_dijet = frame.pullHist()
    hpull_dijet.SetLineColor(ROOT.kRed)
    hpull_dijet.SetMarkerColor(ROOT.kRed)

    #add signals to the plot
    c = ROOT.TCanvas("c","c",0,53,800,740)
    ROOT.gStyle.SetOptStat(0)
    c.SetHighLightColor(2);
    c.Range(0,0,1,1);
    c.SetFillColor(0);
    c.SetBorderMode(0);
    c.SetBorderSize(2);
    c.SetTickx(1);
    c.SetTicky(1);
    c.SetLeftMargin(0.12);
    c.SetRightMargin(0.02);
    c.SetTopMargin(0.055);
    c.SetFrameFillStyle(0);
    c.SetFrameBorderMode(0);
    #------------>Primitives in pad: toppad
    toppad = ROOT.TPad('toppad','toppad',0,0.5 ,1.0,1.0)
    toppad.SetTickx(1);
    toppad.SetTicky(1);
    bottompad = ROOT.TPad('bottompad','bottompad',0,0.0,1.0,0.32)
    bottompad.SetTickx(1);
    bottompad.SetTicky(1);
    canvas_margin(c,toppad,bottompad)
    middlepad = ROOT.TPad('middlepad','middlepad',0,0.18,1.0,0.5)
    middlepad.SetTickx(1);
    middlepad.SetTicky(1);
    middlepad.SetTopMargin( 0.03 )
    middlepad.SetBottomMargin( 0.4 )
    middlepad.SetLeftMargin( 0.15 )
    middlepad.SetRightMargin( 0.03 )

    toppad.SetFillStyle(4000)
    toppad.SetFrameFillStyle(1000)
    toppad.SetFrameFillColor(0)
    toppad.SetFillColor(0)
    toppad.SetBorderMode(0)
    toppad.SetBorderSize(2)
    toppad.SetLogy()
    toppad.SetFrameBorderMode(0)
    toppad.SetFrameBorderMode(0)
    toppad.SetLeftMargin(0.15)
    bottompad.SetFillStyle(4000)
    bottompad.SetFrameFillStyle(1000)
    bottompad.SetFrameFillColor(0)
    bottompad.SetFillColor(0)
    bottompad.SetBorderMode(0)
    bottompad.SetBorderSize(2)
    bottompad.SetFrameBorderMode(0)
    bottompad.SetFrameBorderMode(0)
    middlepad.SetFillStyle(4000)
    middlepad.SetFrameFillStyle(1000)
    middlepad.SetFrameFillColor(0)
    middlepad.SetFillColor(0)
    middlepad.SetBorderMode(0)
    middlepad.SetBorderSize(2)
    middlepad.SetFrameBorderMode(0)
    middlepad.SetFrameBorderMode(0)
    toppad.Draw()
    middlepad.Draw()
    bottompad.Draw()

    c.cd()
    c.Update()
    c.RedrawAxis()
    cframe = c.GetFrame()
    cframe.Draw()
    toppad.cd()
    frame_4fa51a0__1 = ROOT.TH1D("frame_4fa51a0__1","Unbinned ML fit, %s %s"%(ch,year),NBIN_,MIN_,MAX_)
    frame_4fa51a0__1.GetXaxis().SetTitle("m_{T}^{l#nu#gamma} [GeV]");
    frame_4fa51a0__1.GetXaxis().SetLabelFont(42);
    frame_4fa51a0__1.GetXaxis().SetLabelSize(0.05);
    frame_4fa51a0__1.GetXaxis().SetTitleSize(0.05);
    frame_4fa51a0__1.GetXaxis().SetTitleOffset(1);
    frame_4fa51a0__1.GetXaxis().SetTitleFont(42);
    frame_4fa51a0__1.GetYaxis().SetTitle("Events / "+str((MAX_-MIN_)/NBIN_)+" GeV");
    frame_4fa51a0__1.GetYaxis().SetLabelFont(42);
    frame_4fa51a0__1.GetYaxis().SetLabelSize(0.05);
    frame_4fa51a0__1.GetYaxis().SetTitleSize(0.05);
    frame_4fa51a0__1.GetYaxis().SetTitleFont(42);
    frame_4fa51a0__1.GetYaxis().SetRangeUser(0.8e-2,1e4)
    frame_4fa51a0__1.GetXaxis().SetLabelOffset(999)
    frame_4fa51a0__1.GetXaxis().SetLabelSize(0)
    frame_4fa51a0__1.Draw("AXISSAME");
    frame.Draw("same E")
    frame_4fa51a0__1.Draw("AXISSAME");

    frame3 = mt_res.frame(ROOT.RooFit.Title("Pull Distribution"))
    frame3.addPlotable(hpull_dijet, "P")
    frame4 = mt_res.frame(ROOT.RooFit.Title("Pull Distribution"))
    frame4.addPlotable(hpull_vvdijet, "P")

    frame5 = mt_res.frame(ROOT.RooFit.Title("Pull Distribution"))
    frame5.addPlotable(hpull_dijet2, "P")
    frame6 = mt_res.frame(ROOT.RooFit.Title("Pull Distribution"))
    frame6.addPlotable(hpull_vvdijet2, "P")

    leg = ROOT.TLegend(0.25,0.73,0.6,0.85);
    leg.SetBorderSize(0);
    leg.SetLineStyle(1);
    leg.SetLineWidth(1);
    entry=leg.AddEntry(frame,"ToyData from Vvdijet-2","pe");
    entry.SetFillStyle(1001);
    entry.SetMarkerStyle(8);
    entry.SetMarkerSize(1.5);
    entry.SetLineStyle(1);
    entry.SetLineWidth(2);
    entry.SetTextFont(42);
    entry.SetTextSize(0.04);
    leg.Draw()


    leg2 = ROOT.TLegend(0.55,0.6,0.9,0.9);
    leg2.SetBorderSize(0);
    leg2.SetLineStyle(1);
    leg2.SetLineWidth(1);
    entry=leg2.AddEntry("","Dijet-2 + signal@600GeV (#Gamma_{X}/m_{X}=5%)","l");
    entry.SetFillStyle(1001);
    entry.SetLineStyle(1)
    entry.SetLineWidth(2)
    entry.SetLineColor(ROOT.kRed);
    entry.SetTextFont(42)
    entry.SetTextSize(0.04)
    entry=leg2.AddEntry("","Dijet-2","l");
    entry.SetFillStyle(1001);
    entry.SetLineStyle(9)
    entry.SetLineWidth(2)
    entry.SetLineColor(ROOT.kRed);
    entry.SetTextFont(42)
    entry.SetTextSize(0.04)
    entry=leg2.AddEntry("","Vvdijet-2 + signal@600GeV (#Gamma_{X}/m_{X}=5%)","l");
    entry.SetFillStyle(1001);
    entry.SetLineStyle(1)
    entry.SetLineWidth(2)
    entry.SetLineColor(ROOT.kAzure);
    entry.SetTextFont(42)
    entry.SetTextSize(0.04)
    entry=leg2.AddEntry("","Vvdijet-2","l");
    entry.SetFillStyle(1001);
    entry.SetLineStyle(9)
    entry.SetLineWidth(2)
    entry.SetLineColor(ROOT.kAzure);
    entry.SetTextFont(42)
    entry.SetTextSize(0.04)
    leg2.Draw()
    tex = ROOT.TLatex(0.98,0.94,"137 fb^{-1} (13 TeV)");
    tex.SetNDC();
    tex.SetTextAlign(31);
    tex.SetTextFont(42);
    tex.SetTextSize(0.05);
    tex.SetLineWidth(2);
    tex.Draw();
    tex2 = ROOT.TLatex(0.18,0.9,"CMS");
    tex2.SetNDC();
    tex2.SetTextAlign(13);
    tex2.SetTextFont(61);
    tex2.SetTextSize(0.06);
    tex2.SetLineWidth(2);
    tex2.Draw();
    bottompad.cd()
    frame_4fa51a0__2 = ROOT.TH1D("frame_4fa51a0__2","",NBIN_,MIN_,MAX_)
    frame_4fa51a0__2.GetXaxis().SetTitle("m_{T}^{l#nu#gamma} [GeV]");
    frame_4fa51a0__2.GetXaxis().SetLabelFont(42);
    frame_4fa51a0__2.GetXaxis().SetLabelSize(0.1);
    frame_4fa51a0__2.GetXaxis().SetTitleSize(0.1);
    frame_4fa51a0__2.GetXaxis().SetTitleOffset(1);
    frame_4fa51a0__2.GetXaxis().SetTitleFont(42);
    frame_4fa51a0__2.GetYaxis().SetTitle("#frac{Data-Fit}{#sigma_{Stat.}}");
    frame_4fa51a0__2.GetYaxis().CenterTitle()
    frame_4fa51a0__2.GetYaxis().SetLabelFont(42);
    frame_4fa51a0__2.GetYaxis().SetLabelSize(0.1);
    frame_4fa51a0__2.GetYaxis().SetTitleSize(0.1);
    frame_4fa51a0__2.GetYaxis().SetTitleFont(42);
    frame_4fa51a0__2.GetYaxis().SetRangeUser(-10,10)
    frame_4fa51a0__2.GetYaxis().SetNdivisions(5, 2, 0, ROOT.kTRUE)
    frame_4fa51a0__2.GetYaxis().SetTitleOffset(0.4)
    frame_4fa51a0__2.Draw("AXISSAME")
    frame3.Draw("same")
    frame4.Draw("same")
    frame_4fa51a0__2.Draw("AXISSAME")
    line = ROOT.TLine(200,0,2000,0);
    line.SetLineStyle(2)
    line.SetLineWidth(2)
    line.Draw()
    middlepad.cd()
    frame_4fa51a0__3 = ROOT.TH1D("frame_4fa51a0__3","",NBIN_,MIN_,MAX_)
    frame_4fa51a0__3.GetXaxis().SetTitle("m_{T}^{l#nu#gamma} [GeV]");
    frame_4fa51a0__3.GetXaxis().SetLabelFont(42);
    frame_4fa51a0__3.GetXaxis().SetLabelSize(0.01);
    frame_4fa51a0__3.GetXaxis().SetTitleSize(0.1);
    frame_4fa51a0__3.GetXaxis().SetTitleOffset(1);
    frame_4fa51a0__3.GetXaxis().SetTitleFont(42);
    frame_4fa51a0__3.GetYaxis().SetTitle("#frac{Data-BkgFit}{#sigma_{Stat.}}");
    frame_4fa51a0__3.GetYaxis().CenterTitle()
    frame_4fa51a0__3.GetYaxis().SetLabelFont(42);
    frame_4fa51a0__3.GetYaxis().SetLabelSize(0.1);
    frame_4fa51a0__3.GetYaxis().SetTitleSize(0.1);
    frame_4fa51a0__3.GetYaxis().SetTitleFont(42);
    frame_4fa51a0__3.GetYaxis().SetRangeUser(-10,10)
    frame_4fa51a0__3.GetYaxis().SetNdivisions(5, 2, 0, ROOT.kTRUE)
    frame_4fa51a0__3.GetYaxis().SetTitleOffset(0.4)
    frame_4fa51a0__3.Draw("AXISSAME")
    frame5.Draw("same")
    frame6.Draw("same")
    frame_4fa51a0__3.Draw("AXISSAME")
    line2 = ROOT.TLine(200,0,2000,0);
    line2.SetLineStyle(2)
    line2.SetLineWidth(2)
    line2.Draw()

    input('wait..')
    #c.SaveAs('fit_ALL%s.C' %(ch))



def makeFinalplots(baseDir,skimtree):

    #Reading Data, merge 3 years
    year ='ALL'
    MIN_=200
    MAX_=400
    NBIN_=100
    mt_res = ROOT.RooRealVar("mt_res", "mt_res", 200, 2200)
    mt_res.setBins(400)
    #mt_res.setRange( MIN_ ,MAX_)
    F=ROOT.TFile(baseDir+'/elALL_skim.root')
    tree=F.Get(skimtree)
    netot = tree.GetEntries()
    dse = ROOT.RooDataSet('data_elA'+year+'_mt_res_base', "dse", ROOT.RooArgSet(mt_res), ROOT.RooFit.Import(tree))
    F=ROOT.TFile(baseDir+'/muALL_skim.root')
    tree=F.Get(skimtree)
    nmtot = tree.GetEntries()
    dsm = ROOT.RooDataSet('data_muA'+year+'_mt_res_base', "dsm", ROOT.RooArgSet(mt_res), ROOT.RooFit.Import(tree))
    ne = dse.sumEntries("mt_res>"+str(MIN_))
    nm = dsm.sumEntries("mt_res>"+str(MIN_))

    #prepare Working Space with Roofit
    #ws_out  = ROOT.RooWorkspace( "workspace_all" )
    #rootfilename = '%s/%s/%s.root' %( data_outDir,year,ws_out.GetName() )


    #create 3 background pdfs
    func_name = 'dijet'
    function = 'TMath::Power( @0/13000., @1 + @2*TMath::Log10(@0/13000) )'
    dijet_order1_e = ROOT.RooRealVar('dijet_order1_elA'+year+'_all_dijet', "power1", -9, -100.0, -0.001)
    dijet_order2_e = ROOT.RooRealVar('dijet_order2_elA'+year+'_all_dijet', "power2", -2, -5.0, -0.01)
    dijet_order1_m = ROOT.RooRealVar('dijet_order1_muA'+year+'_all_dijet', "power1", -9, -100.0, -0.001)
    dijet_order2_m = ROOT.RooRealVar('dijet_order2_muA'+year+'_all_dijet', "power2", -2, -5.0, -0.01)
#    dijet_order1_e = ROOT.RooRealVar('dijet_order1_elA'+year+'_all_dijet', "power1", -9, -100.0, -0.001)
#    dijet_order2_e = ROOT.RooRealVar('dijet_order2_elA'+year+'_all_dijet', "power2", -2, -5.0, 10)
#    dijet_order1_m = ROOT.RooRealVar('dijet_order1_muA'+year+'_all_dijet', "power1", -9, -100.0, -0.001)
#    dijet_order2_m = ROOT.RooRealVar('dijet_order2_muA'+year+'_all_dijet', "power2", -2, -5.0, 10)

    func_dijet_e = ROOT.RooGenericPdf( '%s_%s'%(func_name, 'elA'+year+'_all_dijet'), func_name, function, ROOT.RooArgList(mt_res,dijet_order1_e,dijet_order2_e))
    func_dijet_m = ROOT.RooGenericPdf( '%s_%s'%(func_name, 'muA'+year+'_all_dijet'), func_name, function, ROOT.RooArgList(mt_res,dijet_order1_m,dijet_order2_m))

    func_name = 'vvdijet'
    function = 'TMath::Power( (1-@0/13000.), @1 ) / ( TMath::Power( @0/13000. , @2))'
    vvdijet_order1_e = ROOT.RooRealVar( 'vvdijet_order1_elA'+year+'_all_vvdijet', "power1", 40 ,      -50,  200)
    vvdijet_order2_e = ROOT.RooRealVar( 'vvdijet_order2_elA'+year+'_all_vvdijet', "power2", 2 ,     -10,   30)
    vvdijet_order1_m = ROOT.RooRealVar( 'vvdijet_order1_muA'+year+'_all_vvdijet', "power1", 40 ,      -50,  200)
    vvdijet_order2_m = ROOT.RooRealVar( 'vvdijet_order2_muA'+year+'_all_vvdijet', "power2", 2 ,     -10,   30)
    #vvdijet_order3_e = ROOT.RooRealVar( 'vvdijet_order3_elA'+year+'_all_vvdijet', "power3", 2 ,     -10,   30)
    #vvdijet_order3_m = ROOT.RooRealVar( 'vvdijet_order3_muA'+year+'_all_vvdijet', "power3", 2 ,     -10,   30)
    func_vvdijet_m = ROOT.RooGenericPdf( '%s_%s'%(func_name, 'muA'+year+'_all_vvdijet'), '%s_%s'%(func_name, 'muA'+year+'_all_vvdijet'), function, ROOT.RooArgList(mt_res, vvdijet_order1_m, vvdijet_order2_m))
    func_vvdijet_e = ROOT.RooGenericPdf( '%s_%s'%(func_name, 'elA'+year+'_all_vvdijet'), '%s_%s'%(func_name, 'elA'+year+'_all_vvdijet'), function, ROOT.RooArgList(mt_res, vvdijet_order1_e, vvdijet_order2_e))
 
    func_name = 'expow'
    function = 'TMath::Power( @0/13000., @2 ) * TMath::Exp( @1*@0/13000.)'

    expow_order2_e = ROOT.RooRealVar( 'expow_order2_elA'+year+'_all_expow', "power2", -2 ,      -100,  20)
    expow_order1_e = ROOT.RooRealVar( 'expow_order1_elA'+year+'_all_expow', "power1", -50 ,     -200,   50)
    expow_order2_m = ROOT.RooRealVar( 'expow_order2_muA'+year+'_all_expow', "power2", -2 ,      -100,  20)
    expow_order1_m = ROOT.RooRealVar( 'expow_order1_muA'+year+'_all_expow', "power1", -50 ,     -200,   50)
    func_expow_m = ROOT.RooGenericPdf( '%s_%s'%(func_name, 'muA'+year+'_all_expow'), '%s_%s'%(func_name, 'muA'+year+'_all_expow'), function, ROOT.RooArgList(mt_res, expow_order1_m, expow_order2_m))
    func_expow_e = ROOT.RooGenericPdf( '%s_%s'%(func_name, 'elA'+year+'_all_expow'), '%s_%s'%(func_name, 'elA'+year+'_all_expow'), function, ROOT.RooArgList(mt_res, expow_order1_e, expow_order2_e))

    # First we fit the pdfs to the data
    resu_dijet_e = func_dijet_e.fitTo(dse,ROOT.RooFit.Save(),ROOT.RooFit.SumW2Error(ROOT.kTRUE))
    resu_dijet_m = func_dijet_m.fitTo(dsm,ROOT.RooFit.Save(),ROOT.RooFit.SumW2Error(ROOT.kTRUE))
    resu_vvdijet_e = func_vvdijet_e.fitTo(dse,ROOT.RooFit.Save(),ROOT.RooFit.SumW2Error(ROOT.kTRUE))
    resu_vvdijet_m = func_vvdijet_m.fitTo(dsm,ROOT.RooFit.Save(),ROOT.RooFit.SumW2Error(ROOT.kTRUE))
    resu_expow_e = func_expow_e.fitTo(dse,ROOT.RooFit.Save(),ROOT.RooFit.SumW2Error(ROOT.kTRUE))
    resu_expow_m = func_expow_m.fitTo(dsm,ROOT.RooFit.Save(),ROOT.RooFit.SumW2Error(ROOT.kTRUE))
    print("===> fit result")
    resu_dijet_e.Print()
    print("===> fit result")
    resu_dijet_m.Print()
    print("===> fit result")
    resu_vvdijet_e.Print()
    print("===> fit result")
    resu_vvdijet_m.Print()
    print("===> fit result")
    resu_expow_e.Print()
    print("===> fit result")
    resu_expow_m.Print()


    catIndexe = ROOT.RooCategory('pdf_index_el'+year,'Index of Pdf which is active')
    mypdfse = ROOT.RooArgList("store")
    mypdfse.add(func_dijet_e)
    mypdfse.add(func_vvdijet_e)
    mypdfse.add(func_expow_e)
    catIndexm = ROOT.RooCategory('pdf_index_mu'+year,'Index of Pdf which is active')
    mypdfsm = ROOT.RooArgList("store")
    mypdfsm.add(func_dijet_m)
    mypdfsm.add(func_vvdijet_m)
    mypdfsm.add(func_expow_m)

    multipdfe = RooMultiPdf('MultiPdf_elA'+year+'_all_MultiPdf',"All Pdfs e",catIndexe, mypdfse)
    norm_MultiPdf_e = ROOT.RooRealVar('%s_norm' %( 'MultiPdf_elA'+year+'_all_MultiPdf' ),'normalization_e', ne,0,1000000 )
    multipdfm = RooMultiPdf('MultiPdf_muA'+year+'_all_MultiPdf',"All Pdfs m",catIndexm, mypdfsm)
    norm_MultiPdf_m = ROOT.RooRealVar('%s_norm' %( 'MultiPdf_muA'+year+'_all_MultiPdf' ),'normalization_m', nm,0,1000000 )

    #Generate toy with a specific function 
    singlefunc=False
    if singlefunc:
        func_name = 'toy'
        function = 'TMath::Power( (1-@0/13000.), @1 ) / ( TMath::Power( @0/13000. , @2+ @3*TMath::Log10(@0/13000)))'
        toy_vvdijet_order1_e = ROOT.RooRealVar( 'toy_vvdijet_order1_elA'+year+'_all_vvdijet', "power1", 40 ,      -100,  100)
        toy_vvdijet_order2_e = ROOT.RooRealVar( 'toy_vvdijet_order2_elA'+year+'_all_vvdijet', "power2", 2 ,     -50,   50)
        toy_vvdijet_order3_e = ROOT.RooRealVar( 'toy_vvdijet_order3_elA'+year+'_all_vvdijet', "power3", 2 ,     -50,   50)
        func_toy_vvdijet = ROOT.RooGenericPdf( 'toy_%s_%s'%(func_name, 'muA'+year+'_all_vvdijet'), '%s_%s'%(func_name, 'muA'+year+'_all_vvdijet'), function, ROOT.RooArgList(mt_res, toy_vvdijet_order1_e, toy_vvdijet_order2_e,toy_vvdijet_order3_e))
        func_toy_vvdijet.fitTo(dse,ROOT.RooFit.Save(),ROOT.RooFit.SumW2Error(ROOT.kTRUE)) 
        toydatae = func_toy_vvdijet.generate(ROOT.RooArgSet(mt_res),ne)
        func_toy_vvdijet.fitTo(dsm,ROOT.RooFit.Save(),ROOT.RooFit.SumW2Error(ROOT.kTRUE))
        toydatam = func_toy_vvdijet.generate(ROOT.RooArgSet(mt_res),nm)
        toydatae.SetName ('data_elA'+year+'_mt_res_base')
        toydatam.SetName ('data_muA'+year+'_mt_res_base')
        #import_workspace( ws_out, dse)
        #import_workspace( ws_out, dsm)
    else:
        frame_toy = mt_res.frame(ROOT.RooFit.Title("Unbinned ML fit, el"))
        dse.plotOn(frame_toy,ROOT.RooFit.DataError(ROOT.RooAbsData.SumW2))
        chi2score_e=[]
        multipdfse=[func_dijet_e,func_vvdijet_e,func_expow_e]
        multiresultse=[resu_dijet_e,resu_vvdijet_e,resu_expow_e]
        for toypdf in multipdfse:
            toypdf.plotOn(frame_toy)
            chi2score_e.append((frame_toy.chiSquare()))

        framm_toy = mt_res.frame(ROOT.RooFit.Title("Unbinned ML fit, el"))
        dsm.plotOn(framm_toy,ROOT.RooFit.DataError(ROOT.RooAbsData.SumW2))
        chi2score_m=[]
        multipdfsm=[func_dijet_m,func_vvdijet_m,func_expow_m]
        multiresultsm=[resu_dijet_m,resu_vvdijet_m,resu_expow_m]
        for toypdf in multipdfsm:
            toypdf.plotOn(framm_toy)
            chi2score_m.append((framm_toy.chiSquare()))
        rseed = ROOT.RooRandom.randomGenerator()
        rseed.SetSeed(123)
        toydatae = multipdfse[np.argmin(np.abs(chi2score_e))].generate(ROOT.RooArgSet(mt_res),ne)
        toydatam = multipdfsm[np.argmin(np.abs(chi2score_m))].generate(ROOT.RooArgSet(mt_res),nm)
        print('------> score: ', chi2score_e, chi2score_m)
        print('------------> set index to e: ', np.argmin(np.abs(chi2score_e)), ' m: ', np.argmin(np.abs(chi2score_m)))
        catIndexe.setIndex(np.argmin(np.abs(chi2score_e)))
        catIndexm.setIndex(np.argmin(np.abs(chi2score_m)))
        toydatae.SetName ('data_elA'+year+'_mt_res_base')
        toydatam.SetName ('data_muA'+year+'_mt_res_base')
        #import_workspace( ws_out, toydatae)
        #import_workspace( ws_out, toydatam)
        #import_workspace( ws_out, dse)
        #import_workspace( ws_out, dsm)

    frame_e = mt_res.frame(ROOT.RooFit.Title("Unbinned ML fit, el"))
    frame_m = mt_res.frame(ROOT.RooFit.Title("Unbinned ML fit, mu"))

    #add signals to the plot
    widthlist=['5','0p01']
    masslist=['600', '1000', '1600']
    normalizationlist = {
        "el":{
            "5":{
                "600":{"norm":100,"linecolor":ROOT.kRed,"linestyle":9,
                },
                "1000":{"norm":100,"linecolor":ROOT.kViolet,"linestyle":9,
                },
                "1600":{"norm":100,"linecolor":ROOT.kAzure,"linestyle":9,
                },
            },
            "0p01":{
                "600":{"norm":100,"linecolor":ROOT.kRed,"linestyle":1,
                },
                "1000":{"norm":100,"linecolor":ROOT.kViolet,"linestyle":1,
                },
                "1600":{"norm":100,"linecolor":ROOT.kAzure,"linestyle":1,
                },
            }
        },
        "mu":{
            "5":{
                "600":{"norm":100,"linecolor":ROOT.kRed,"linestyle":9,
                },
                "1000":{"norm":100,"linecolor":ROOT.kViolet,"linestyle":9,
                },
                "1600":{"norm":100,"linecolor":ROOT.kAzure,"linestyle":9,
                },
            },
            "0p01":{
                "600":{"norm":100,"linecolor":ROOT.kRed,"linestyle":1,
                },
                "1000":{"norm":100,"linecolor":ROOT.kViolet,"linestyle":1,
                },
                "1600":{"norm":100,"linecolor":ROOT.kAzure,"linestyle":1,
                },
            }
        }
    }
    for ch in ["el","mu"]:
        for iwid in widthlist:
            for imass in masslist:
                year='2018'
                inputfile0 = 'data_env/sigfit/'+year+'/wssignal_M'+imass+'_W'+iwid+'_'+ch+'.root'
                wsname = "wssignal_M"+imass+"_W"+iwid+"_"+ch
                print(inputfile0, " : ", wsname)
                ifile0 = ROOT.TFile.Open( inputfile0, 'READ' )
                if not ifile0:
                    return
                ws_in0 = ifile0.Get( wsname )
                pdfname = 'cb_MG_M%s_W%s_%s%s' %(imass,iwid,ch,year)
                sigModel0 = ws_in0.pdf(pdfname)
                print(normalizationlist[ch][iwid][imass])
                if 'el' in ch:
                    sigModel0.plotOn(frame_e,ROOT.RooFit.DataError(ROOT.RooAbsData.Poisson),ROOT.RooFit.LineColor(normalizationlist[ch][iwid][imass]['linecolor']),ROOT.RooFit.LineStyle(normalizationlist[ch][iwid][imass]['linestyle']), ROOT.RooFit.Normalization(normalizationlist[ch][iwid][imass]['norm'],ROOT.RooAbsReal.NumEvent))#,ROOT.RooFit.LineColor(normalizationlist[ch][iwid][imass]['linecolor']),ROOT.RooFit.LineStyle(ROOT.RooFit.LineColor(normalizationlist[ch][iwid][imass]['linestyle']) ))
                if 'mu' in ch:
                    sigModel0.plotOn(frame_m,ROOT.RooFit.DataError(ROOT.RooAbsData.Poisson),ROOT.RooFit.LineColor(normalizationlist[ch][iwid][imass]['linecolor']),ROOT.RooFit.LineStyle(normalizationlist[ch][iwid][imass]['linestyle']), ROOT.RooFit.Normalization(normalizationlist[ch][iwid][imass]['norm'],ROOT.RooAbsReal.NumEvent))

    dse.plotOn(frame_e,ROOT.RooFit.DataError(ROOT.RooAbsData.SumW2))
    dsm.plotOn(frame_m,ROOT.RooFit.DataError(ROOT.RooAbsData.SumW2))
#    toydatae.plotOn(frame_e,ROOT.RooFit.DataError(ROOT.RooAbsData.Poisson))
#    toydatam.plotOn(frame_m,ROOT.RooFit.DataError(ROOT.RooAbsData.Poisson))
    multipdfse[np.argmin(np.abs(chi2score_e))].plotOn(frame_e, ROOT.RooFit.VisualizeError(multiresultse[np.argmin(np.abs(chi2score_e))], 2), ROOT.RooFit.FillColor(ROOT.kYellow))
    multipdfsm[np.argmin(np.abs(chi2score_m))].plotOn(frame_m, ROOT.RooFit.VisualizeError(multiresultsm[np.argmin(np.abs(chi2score_m))], 2), ROOT.RooFit.FillColor(ROOT.kYellow))
    multipdfse[np.argmin(np.abs(chi2score_e))].plotOn(frame_e, ROOT.RooFit.VisualizeError(multiresultse[np.argmin(np.abs(chi2score_e))], 1), ROOT.RooFit.FillColor(ROOT.kGreen))
    multipdfsm[np.argmin(np.abs(chi2score_m))].plotOn(frame_m, ROOT.RooFit.VisualizeError(multiresultsm[np.argmin(np.abs(chi2score_m))], 1), ROOT.RooFit.FillColor(ROOT.kGreen))
    multipdfse[np.argmin(np.abs(chi2score_e))].plotOn(frame_e)
    multipdfsm[np.argmin(np.abs(chi2score_m))].plotOn(frame_m)
    dse.plotOn(frame_e,ROOT.RooFit.DataError(ROOT.RooAbsData.SumW2))
    dsm.plotOn(frame_m,ROOT.RooFit.DataError(ROOT.RooAbsData.SumW2))
#    toydatae.plotOn(frame_e,ROOT.RooFit.DataError(ROOT.RooAbsData.Poisson))
#    toydatam.plotOn(frame_m,ROOT.RooFit.DataError(ROOT.RooAbsData.Poisson))

    print("sum Entries: ", toydatae.sumEntries(), toydatam.sumEntries())

    for ch, frame in zip(["el","mu"],[frame_e, frame_m]):
        c = ROOT.TCanvas("c","c",0,53,800,740)
        ROOT.gStyle.SetOptStat(0)
        c.SetHighLightColor(2);
        c.Range(0,0,1,1);
        c.SetFillColor(0);
        c.SetBorderMode(0);
        c.SetBorderSize(2);
        c.SetTickx(1);
        c.SetTicky(1);
        c.SetLeftMargin(0.12);
        c.SetRightMargin(0.02);
        c.SetTopMargin(0.055);
        c.SetFrameFillStyle(0);
        c.SetFrameBorderMode(0);
        #------------>Primitives in pad: toppad
        toppad = ROOT.TPad('toppad','toppad',0,0.3 ,1.0,1.0)
        toppad.SetTickx(1);
        toppad.SetTicky(1);
        bottompad = ROOT.TPad('bottompad','bottompad',0,0.0,1.0,0.32)
        bottompad.SetTickx(1);
        bottompad.SetTicky(1);
        canvas_margin(c,toppad,bottompad)
        toppad.SetFillStyle(4000)
        toppad.SetFrameFillStyle(1000)
        toppad.SetFrameFillColor(0)
        toppad.SetFillColor(0)
        toppad.SetBorderMode(0)
        toppad.SetBorderSize(2)
        #toppad.SetLogy()
        toppad.SetFrameBorderMode(0)
        toppad.SetFrameBorderMode(0)
        toppad.SetLeftMargin(0.15)
        bottompad.SetFillStyle(4000)
        bottompad.SetFrameFillStyle(1000)
        bottompad.SetFrameFillColor(0)
        bottompad.SetFillColor(0)
        bottompad.SetBorderMode(0)
        bottompad.SetBorderSize(2)
        bottompad.SetFrameBorderMode(0)
        bottompad.SetFrameBorderMode(0)
        toppad.Draw()
        bottompad.Draw()

        c.cd()
        c.Update()
        c.RedrawAxis()
        cframe = c.GetFrame()
        cframe.Draw()
        toppad.cd()
        frame_4fa51a0__1 = ROOT.TH1D("frame_4fa51a0__1","Unbinned ML fit, %s %s"%(ch,year),NBIN_,MIN_,MAX_)
        frame_4fa51a0__1.GetXaxis().SetTitle("m_{T}^{l#nu#gamma} [GeV]");
        frame_4fa51a0__1.GetXaxis().SetLabelFont(42);
        frame_4fa51a0__1.GetXaxis().SetLabelSize(0.05);
        frame_4fa51a0__1.GetXaxis().SetTitleSize(0.05);
        frame_4fa51a0__1.GetXaxis().SetTitleOffset(1);
        frame_4fa51a0__1.GetXaxis().SetTitleFont(42);
        frame_4fa51a0__1.GetYaxis().SetTitle("Events / 20 GeV");
        frame_4fa51a0__1.GetYaxis().SetLabelFont(42);
        frame_4fa51a0__1.GetYaxis().SetLabelSize(0.05);
        frame_4fa51a0__1.GetYaxis().SetTitleSize(0.05);
        frame_4fa51a0__1.GetYaxis().SetTitleFont(42);
        frame_4fa51a0__1.GetYaxis().SetRangeUser(0.8e-2,1e4)
        frame_4fa51a0__1.GetXaxis().SetLabelOffset(999)
        frame_4fa51a0__1.GetXaxis().SetLabelSize(0)
        frame_4fa51a0__1.Draw("AXISSAME");
        frame.Draw("same E")

        hpull = frame.pullHist()
        frame3 = mt_res.frame(ROOT.RooFit.Title("Pull Distribution"))
        frame3.addPlotable(hpull, "P")

        leg = ROOT.TLegend(0.25,0.7,0.65,0.9);
        leg.SetBorderSize(0);
        leg.SetLineStyle(1);
        leg.SetLineWidth(1);
        entry=leg.AddEntry(frame,"ToyData","pe");
        entry.SetFillStyle(1001);
        entry.SetMarkerStyle(8);
        entry.SetMarkerSize(1.5);
        entry.SetLineStyle(1);
        entry.SetLineWidth(2);
        entry.SetTextFont(42);
        entry.SetTextSize(0.03);
        entry=leg.AddEntry("","Data fit","l");
        entry.SetFillStyle(1001);
        entry.SetLineStyle(1)
        entry.SetLineWidth(2)
        entry.SetLineColor(ROOT.kBlue);
        entry.SetMarkerStyle(20)
        entry.SetTextFont(42)
        entry.SetTextSize(0.03)
        htmp=ROOT.TH1F("htmp","htmp",10,0,1)
        htmp.SetFillColor(ROOT.kGreen)
        entry=leg.AddEntry(htmp,"Fit uncert. 68% CL","f");
        entry.SetFillStyle(1001)
        entry.SetLineStyle(1)
        entry.SetLineWidth(2)
        entry.SetMarkerStyle(20)
        entry.SetTextFont(42)
        entry.SetTextSize(0.03)
        htmp2=ROOT.TH1F("htmp2","htmp2",10,0,1)
        htmp2.SetFillColor(ROOT.kYellow)
        entry=leg.AddEntry(htmp2,"Fit uncert. 95% CL","f");
        entry.SetFillStyle(1001)
        entry.SetLineStyle(1)
        entry.SetLineWidth(2)
        entry.SetMarkerStyle(20)
        entry.SetTextFont(42)
        entry.SetTextSize(0.03)
        leg.Draw()


        leg2 = ROOT.TLegend(0.55,0.5,0.9,0.9);
        leg2.SetBorderSize(0);
        leg2.SetLineStyle(1);
        leg2.SetLineWidth(1);
        entry=leg2.AddEntry("","Signal 600GeV, narrow","l");
        entry.SetFillStyle(1001);
        entry.SetLineStyle(1)
        entry.SetLineWidth(2)
        entry.SetLineColor(ROOT.kRed);
        entry.SetTextFont(42)
        entry.SetTextSize(0.03)
        entry=leg2.AddEntry("","Signal 600GeV, #Gamma_{X}/m_{X}=5%","l");
        entry.SetFillStyle(1001);
        entry.SetLineStyle(9)
        entry.SetLineWidth(2)
        entry.SetLineColor(ROOT.kRed);
        entry.SetTextFont(42)
        entry.SetTextSize(0.03)
        entry=leg2.AddEntry("","Signal 1000GeV, narrow","l");
        entry.SetFillStyle(1001);
        entry.SetLineStyle(1)
        entry.SetLineWidth(2)
        entry.SetLineColor(ROOT.kViolet);
        entry.SetTextFont(42)
        entry.SetTextSize(0.03)
        entry=leg2.AddEntry("","Signal 1000GeV, #Gamma_{X}/m_{X}=5%","l");
        entry.SetFillStyle(1001);
        entry.SetLineStyle(9)
        entry.SetLineWidth(2)
        entry.SetLineColor(ROOT.kViolet);
        entry.SetTextFont(42)
        entry.SetTextSize(0.03)
        entry=leg2.AddEntry("","Signal 1600GeV, narrow","l");
        entry.SetFillStyle(1001);
        entry.SetLineStyle(1)
        entry.SetLineWidth(2)
        entry.SetLineColor(ROOT.kAzure);
        entry.SetTextFont(42)
        entry.SetTextSize(0.03)
        entry=leg2.AddEntry("","Signal 1600GeV, #Gamma_{X}/m_{X}=5%","l");
        entry.SetFillStyle(1001);
        entry.SetLineStyle(9)
        entry.SetLineWidth(2)
        entry.SetLineColor(ROOT.kAzure);
        entry.SetTextFont(42)
        entry.SetTextSize(0.03)
        leg2.Draw()

        tex = ROOT.TLatex(0.98,0.94,"137 fb^{-1} (13 TeV)");
        tex.SetNDC();
        tex.SetTextAlign(31);
        tex.SetTextFont(42);
        tex.SetTextSize(0.05);
        tex.SetLineWidth(2);
        tex.Draw();
        tex2 = ROOT.TLatex(0.18,0.9,"CMS");
        tex2.SetNDC();
        tex2.SetTextAlign(13);
        tex2.SetTextFont(61);
        tex2.SetTextSize(0.06);
        tex2.SetLineWidth(2);
        tex2.Draw();
#        tex3 = ROOT.TLatex(0.18,0.8,"Preliminary");
#        tex3.SetNDC();
#        tex3.SetTextAlign(13);
#        tex3.SetTextFont(52);
#        tex3.SetTextSize(0.06);
#        tex3.SetLineWidth(2);
#        tex3.Draw();

        bottompad.cd()
        frame_4fa51a0__2 = ROOT.TH1D("frame_4fa51a0__2","",NBIN_,MIN_,MAX_)
        frame_4fa51a0__2.GetXaxis().SetTitle("m_{T}^{l#nu#gamma} [GeV]");
        frame_4fa51a0__2.GetXaxis().SetLabelFont(42);
        frame_4fa51a0__2.GetXaxis().SetLabelSize(0.1);
        frame_4fa51a0__2.GetXaxis().SetTitleSize(0.1);
        frame_4fa51a0__2.GetXaxis().SetTitleOffset(1);
        frame_4fa51a0__2.GetXaxis().SetTitleFont(42);
        frame_4fa51a0__2.GetYaxis().SetTitle("#frac{Data-Fit}{#sigma_{Stat.}}");
        frame_4fa51a0__2.GetYaxis().CenterTitle()
        frame_4fa51a0__2.GetYaxis().SetLabelFont(42);
        frame_4fa51a0__2.GetYaxis().SetLabelSize(0.1);
        frame_4fa51a0__2.GetYaxis().SetTitleSize(0.1);
        frame_4fa51a0__2.GetYaxis().SetTitleFont(42);
        frame_4fa51a0__2.GetYaxis().SetRangeUser(-5,5)
        frame_4fa51a0__2.GetYaxis().SetNdivisions(5, 2, 0, ROOT.kTRUE)
        frame_4fa51a0__2.GetYaxis().SetTitleOffset(0.4)
        frame_4fa51a0__2.Draw("AXISSAME")
        frame3.Draw("same")
        line = ROOT.TLine(200,0,2000,0);
        line.SetLineStyle(2)
        line.SetLineWidth(2)
        line.Draw()
        input('wait..')
        #c.SaveAs('fit_ALL%s.C' %(ch))
        #c.SaveAs('fit_ALL%s.pdf' %(ch))


def makeRooMultiPdfWorkspace(year,baseDir,skimtree,skimfile):

    #prepare Working Space with Roofit
    #Reading Data
    mt_res = ROOT.RooRealVar("mt_res", "mt_res", 230, 2200)
    mt_res.setRange( MIN_ ,MAX_)
    F=ROOT.TFile(baseDir+'/el'+year+'_'+skimfile)
    tree=F.Get(skimtree)
    print('read ',baseDir+'/el'+year+'_'+skimfile)
    netot = tree.GetEntries()
    dse = ROOT.RooDataSet('data_elA'+year+'_mt_res_base', "dse", ROOT.RooArgSet(mt_res), ROOT.RooFit.Import(tree))
    F=ROOT.TFile(baseDir+'/mu'+year+'_'+skimfile)
    tree=F.Get(skimtree)
    print('read ',baseDir+'/mu'+year+'_'+skimfile)
    nmtot = tree.GetEntries()
    dsm = ROOT.RooDataSet('data_muA'+year+'_mt_res_base', "dsm", ROOT.RooArgSet(mt_res), ROOT.RooFit.Import(tree))
    ne = dse.sumEntries("mt_res>"+str(MIN_))
    nm = dsm.sumEntries("mt_res>"+str(MIN_))

    #Work space
    ws_out  = ROOT.RooWorkspace( "workspace_all" )
    rootfilename = '%s/%s/%s.root' %( data_outDir,year,ws_out.GetName() )
    #import_workspace( ws_out, dse)
    #import_workspace( ws_out, dsm)


    #create 3 background pdfs
 
    func_name = 'dijet'
    function = 'TMath::Power( @0/13000., @1 + @2*TMath::Log10(@0/13000) )'
    #function = 'TMath::Power( @0/13000., @1 + @2*TMath::Log10(@0/13000) +  @3*TMath::Log10(@0/13000)*TMath::Log10(@0/13000) )'
    #function = 'TMath::Power( @0/13000., @1 + @2*TMath::Log10(@0/13000) +  @3*TMath::Log10(@0/13000)*TMath::Log10(@0/13000) +@4*TMath::Log10(@0/13000)*TMath::Log10(@0/13000)*TMath::Log10(@0/13000) )'
    #norm_dijet_e = ROOT.RooRealVar('%s_norm' %( 'dijet_elA'+year+'_all_dijet' ),'normalization_e', ne,0,1000000 )
    #norm_dijet_m = ROOT.RooRealVar('%s_norm' %( 'dijet_muA'+year+'_all_dijet' ),'normalization_m', nm,0,1000000 )
    dijet_order1_e = ROOT.RooRealVar('dijet_order1_elA'+year+'_all_dijet', "power1", -9, -100.0, 10)
    dijet_order2_e = ROOT.RooRealVar('dijet_order2_elA'+year+'_all_dijet', "power2", -2, -10.0, 20)
    #dijet_order3_e = ROOT.RooRealVar('dijet_order3_elA'+year+'_all_dijet', "power3", 0.2, -20, 20)
    dijet_order1_m = ROOT.RooRealVar('dijet_order1_muA'+year+'_all_dijet', "power1", -9, -100.0, 10)
    dijet_order2_m = ROOT.RooRealVar('dijet_order2_muA'+year+'_all_dijet', "power2", -2, -10.0, 20)
    #dijet_order3_m = ROOT.RooRealVar('dijet_order3_muA'+year+'_all_dijet', "power3", 0.2, -20, 20)
    #dijet_order4_e = ROOT.RooRealVar('dijet_order4_elA'+year+'_all_dijet', "power4", 0.2, -20, 20)
    #dijet_order4_m = ROOT.RooRealVar('dijet_order4_muA'+year+'_all_dijet', "power4", 0.2, -20, 20)
    func_dijet_e = ROOT.RooGenericPdf( '%s_%s'%(func_name, 'elA'+year+'_all_dijet'), func_name, function, ROOT.RooArgList(mt_res,dijet_order1_e,dijet_order2_e))#,dijet_order3_e,dijet_order4_e))
    func_dijet_m = ROOT.RooGenericPdf( '%s_%s'%(func_name, 'muA'+year+'_all_dijet'), func_name, function, ROOT.RooArgList(mt_res,dijet_order1_m,dijet_order2_m))#,dijet_order3_m,dijet_order4_m))

    func_name = 'vvdijet'
    function = 'TMath::Power( (1-@0/13000.), @1 ) / ( TMath::Power( @0/13000. , @2))'
    #function = 'TMath::Power( (1-@0/13000.), @1 ) / ( TMath::Power( @0/13000. , @2+ @3*TMath::Log10(@0/13000)))'
    #function = 'TMath::Power( (1-@0/13000.), @1 ) / ( TMath::Power( @0/13000. , @2+ @3*TMath::Log10(@0/13000) +@4*TMath::Log10(@0/13000)*TMath::Log10(@0/13000) )   )'
    #norm_vvdijet_e = ROOT.RooRealVar('%s_norm' %( 'vvdijet_elA'+year+'_all_vvdijet' ),'normalization_e', ne,0,1000000 )
    #norm_vvdijet_m = ROOT.RooRealVar('%s_norm' %( 'vvdijet_muA'+year+'_all_vvdijet' ),'normalization_m', nm,0,1000000 )
    vvdijet_order1_e = ROOT.RooRealVar( 'vvdijet_order1_elA'+year+'_all_vvdijet', "power1", 40 ,      -50,  300)
    vvdijet_order2_e = ROOT.RooRealVar( 'vvdijet_order2_elA'+year+'_all_vvdijet', "power2", 2 ,     -20,   50)
    vvdijet_order1_m = ROOT.RooRealVar( 'vvdijet_order1_muA'+year+'_all_vvdijet', "power1", 40 ,      -50,  300)
    vvdijet_order2_m = ROOT.RooRealVar( 'vvdijet_order2_muA'+year+'_all_vvdijet', "power2", 2 ,     -20,   50)
    #vvdijet_order3_e = ROOT.RooRealVar( 'vvdijet_order3_elA'+year+'_all_vvdijet', "power3", 2 ,     -30,   20)
    #vvdijet_order3_m = ROOT.RooRealVar( 'vvdijet_order3_muA'+year+'_all_vvdijet', "power3", 2 ,     -30,   20)
    #vvdijet_order4_e = ROOT.RooRealVar( 'vvdijet_order4_elA'+year+'_all_vvdijet', "power4", 0 ,     -10,   30)
    #vvdijet_order4_m = ROOT.RooRealVar( 'vvdijet_order4_muA'+year+'_all_vvdijet', "power4", 0 ,     -10,   30)
    func_vvdijet_m = ROOT.RooGenericPdf( '%s_%s'%(func_name, 'muA'+year+'_all_vvdijet'), '%s_%s'%(func_name, 'muA'+year+'_all_vvdijet'), function, ROOT.RooArgList(mt_res, vvdijet_order1_m, vvdijet_order2_m))#,vvdijet_order3_m))#,vvdijet_order4_m))
    func_vvdijet_e = ROOT.RooGenericPdf( '%s_%s'%(func_name, 'elA'+year+'_all_vvdijet'), '%s_%s'%(func_name, 'elA'+year+'_all_vvdijet'), function, ROOT.RooArgList(mt_res, vvdijet_order1_e, vvdijet_order2_e))#,vvdijet_order3_e,vvdijet_order4_e))
 
    #if year=='2016' or year=='2018':
    #    function = 'TMath::Power( (1-@0/13000.), @1 ) / ( TMath::Power( @0/13000. , @2))'
    #    func_vvdijet_e = ROOT.RooGenericPdf( '%s_%s'%(func_name, 'elA'+year+'_all_vvdijet'), '%s_%s'%(func_name, 'elA'+year+'_all_vvdijet'), function, ROOT.RooArgList(mt_res, vvdijet_order1_e, vvdijet_order2_e))
    #else:
    #    func_vvdijet_e = ROOT.RooGenericPdf( '%s_%s'%(func_name, 'elA'+year+'_all_vvdijet'), '%s_%s'%(func_name, 'elA'+year+'_all_vvdijet'), function, ROOT.RooArgList(mt_res, vvdijet_order1_e, vvdijet_order2_e,vvdijet_order3_e))

    #func_name = 'atlas'
    #function = 'TMath::Power( (1- TMath::Power(@0/13000.,1/3.0) ), @1 ) / ( TMath::Power( @0/13000. , @2))'
    ##norm_atlas_e = ROOT.RooRealVar('%s_norm' %( 'atlas_elA'+year+'_all_atlas' ),'normalization_e', ne,0,1000000 )
    ##norm_atlas_m = ROOT.RooRealVar('%s_norm' %( 'atlas_muA'+year+'_all_atlas' ),'normalization_m', nm,0,1000000 )
    #atlas_order1_e = ROOT.RooRealVar( 'atlas_order1_elA'+year+'_all_atlas', "power1", 40 ,      0.01,  100)
    #atlas_order2_e = ROOT.RooRealVar( 'atlas_order2_elA'+year+'_all_atlas', "power2", 2 ,     0.01,   50)
    #atlas_order1_m = ROOT.RooRealVar( 'atlas_order1_muA'+year+'_all_atlas', "power1", 40 ,      0.01,  100)
    #atlas_order2_m = ROOT.RooRealVar( 'atlas_order2_muA'+year+'_all_atlas', "power2", 2 ,     0.01,   50)
    #func_atlas_m = ROOT.RooGenericPdf( '%s_%s'%(func_name, 'muA'+year+'_all_atlas'), '%s_%s'%(func_name, 'muA'+year+'_all_atlas'), function, ROOT.RooArgList(mt_res, atlas_order1_m, atlas_order2_m))
    #func_atlas_e = ROOT.RooGenericPdf( '%s_%s'%(func_name, 'elA'+year+'_all_atlas'), '%s_%s'%(func_name, 'elA'+year+'_all_atlas'), function, ROOT.RooArgList(mt_res, atlas_order1_e, atlas_order2_e))
 
    func_name = 'expow'
    function = 'TMath::Power( @0/13000., @2 ) * TMath::Exp( @1*@0/13000.)'
    #function = 'TMath::Power( @0/13000., @2 +  @3*TMath::Log10(@0/13000) ) * TMath::Exp( @1*@0/13000.)'
    #function = 'TMath::Power( @0/13000., @2 +  @3*TMath::Log10(@0/13000)+@4*TMath::Log10(@0/13000)*TMath::Log10(@0/13000) ) * TMath::Exp( @1*@0/13000.)'
    expow_order2_e = ROOT.RooRealVar( 'expow_order2_elA'+year+'_all_expow', "power2", -2 ,      -100,  20)
    expow_order1_e = ROOT.RooRealVar( 'expow_order1_elA'+year+'_all_expow', "power1", 20 ,     -300,   50)
    expow_order2_m = ROOT.RooRealVar( 'expow_order2_muA'+year+'_all_expow', "power2", -2 ,      -100,  20)
    expow_order1_m = ROOT.RooRealVar( 'expow_order1_muA'+year+'_all_expow', "power1", 20 ,     -300,   50)
    #expow_order3_e = ROOT.RooRealVar( 'expow_order3_elA'+year+'_all_expow', "power3", -5 ,     -50,   50)
    #expow_order3_m = ROOT.RooRealVar( 'expow_order3_muA'+year+'_all_expow', "power3", -5 ,     -50,   50)
    #expow_order4_e = ROOT.RooRealVar( 'expow_order4_elA'+year+'_all_expow', "power4", -5 ,     -50,   50)
    #expow_order4_m = ROOT.RooRealVar( 'expow_order4_muA'+year+'_all_expow', "power4", -5 ,     -50,   50)
    func_expow_m = ROOT.RooGenericPdf( '%s_%s'%(func_name, 'muA'+year+'_all_expow'), '%s_%s'%(func_name, 'muA'+year+'_all_expow'), function, ROOT.RooArgList(mt_res, expow_order1_m, expow_order2_m))#,expow_order3_m))#,expow_order4_m))
    func_expow_e = ROOT.RooGenericPdf( '%s_%s'%(func_name, 'elA'+year+'_all_expow'), '%s_%s'%(func_name, 'elA'+year+'_all_expow'), function, ROOT.RooArgList(mt_res, expow_order1_e, expow_order2_e))#,expow_order3_e,expow_order4_e))

    #if year=='2016' or year=='2018':
    #    function = 'TMath::Power( @0/13000., @2 ) * TMath::Exp( @1*@0/13000.)'
    #    func_expow_e = ROOT.RooGenericPdf( '%s_%s'%(func_name, 'elA'+year+'_all_expow'), '%s_%s'%(func_name, 'elA'+year+'_all_vvdijet'), function, ROOT.RooArgList(mt_res, expow_order1_e, expow_order2_e))
    #else:
    #    func_expow_e = ROOT.RooGenericPdf( '%s_%s'%(func_name, 'elA'+year+'_all_expow'), '%s_%s'%(func_name, 'elA'+year+'_all_vvdijet'), function, ROOT.RooArgList(mt_res, expow_order1_e, expow_order2_e,expow_order3_e))



    # First we fit the pdfs to the data
    resu_dijet_e = func_dijet_e.fitTo(dse,ROOT.RooFit.Save(),ROOT.RooFit.SumW2Error(ROOT.kTRUE))
    resu_dijet_m = func_dijet_m.fitTo(dsm,ROOT.RooFit.Save(),ROOT.RooFit.SumW2Error(ROOT.kTRUE))
    resu_vvdijet_e = func_vvdijet_e.fitTo(dse,ROOT.RooFit.Save(),ROOT.RooFit.SumW2Error(ROOT.kTRUE))
    resu_vvdijet_m = func_vvdijet_m.fitTo(dsm,ROOT.RooFit.Save(),ROOT.RooFit.SumW2Error(ROOT.kTRUE))
    #resu_atlas_e = func_atlas_e.fitTo(dse,ROOT.RooFit.Save(),ROOT.RooFit.SumW2Error(ROOT.kTRUE))
    #resu_atlas_m = func_atlas_m.fitTo(dsm,ROOT.RooFit.Save(),ROOT.RooFit.SumW2Error(ROOT.kTRUE))
    resu_expow_e = func_expow_e.fitTo(dse,ROOT.RooFit.Save(),ROOT.RooFit.SumW2Error(ROOT.kTRUE))
    resu_expow_m = func_expow_m.fitTo(dsm,ROOT.RooFit.Save(),ROOT.RooFit.SumW2Error(ROOT.kTRUE))
    print("===> fit result")
    resu_dijet_e.Print()
    print("===> fit result")
    resu_dijet_m.Print()
    print("===> fit result")
    resu_vvdijet_e.Print()
    print("===> fit result")
    resu_vvdijet_m.Print()
    #print("===> fit result")
    #resu_atlas_e.Print()
    #print("===> fit result")
    #resu_atlas_m.Print()
    catIndexe = ROOT.RooCategory('pdf_index_el'+year,'Index of Pdf which is active')
    #catIndexe = ROOT.RooCategory('pdf_index','Index of Pdf which is active')
    mypdfse = ROOT.RooArgList("store")
    mypdfse.add(func_dijet_e)
    mypdfse.add(func_vvdijet_e)
    #mypdfse.add(func_atlas_e)
    mypdfse.add(func_expow_e)
    #catIndexm = ROOT.RooCategory('pdf_index','Index of Pdf which is active')
    catIndexm = ROOT.RooCategory('pdf_index_mu'+year,'Index of Pdf which is active')
    mypdfsm = ROOT.RooArgList("store")
    mypdfsm.add(func_dijet_m)
    mypdfsm.add(func_vvdijet_m)
    #mypdfsm.add(func_atlas_m)
    mypdfsm.add(func_expow_m)

    multipdfe = RooMultiPdf('MultiPdf_elA'+year+'_all_MultiPdf',"All Pdfs e",catIndexe, mypdfse)
    norm_MultiPdf_e = ROOT.RooRealVar('%s_norm' %( 'MultiPdf_elA'+year+'_all_MultiPdf' ),'normalization_e', ne,0,1000000 )
    multipdfm = RooMultiPdf('MultiPdf_muA'+year+'_all_MultiPdf',"All Pdfs m",catIndexm, mypdfsm)
    norm_MultiPdf_m = ROOT.RooRealVar('%s_norm' %( 'MultiPdf_muA'+year+'_all_MultiPdf' ),'normalization_m', nm,0,1000000 )

    #Generate toy with a specific function 
    singlefunc=False
    if singlefunc:
        func_name = 'toy'
        function = 'TMath::Power( (1-@0/13000.), @1 ) / ( TMath::Power( @0/13000. , @2+ @3*TMath::Log10(@0/13000)))'
        toy_vvdijet_order1_e = ROOT.RooRealVar( 'toy_vvdijet_order1_elA'+year+'_all_vvdijet', "power1", 40 ,      -100,  100)
        toy_vvdijet_order2_e = ROOT.RooRealVar( 'toy_vvdijet_order2_elA'+year+'_all_vvdijet', "power2", 2 ,     -50,   50)
        toy_vvdijet_order3_e = ROOT.RooRealVar( 'toy_vvdijet_order3_elA'+year+'_all_vvdijet', "power3", 2 ,     -50,   50)
        func_toy_vvdijet = ROOT.RooGenericPdf( 'toy_%s_%s'%(func_name, 'muA'+year+'_all_vvdijet'), '%s_%s'%(func_name, 'muA'+year+'_all_vvdijet'), function, ROOT.RooArgList(mt_res, toy_vvdijet_order1_e, toy_vvdijet_order2_e,toy_vvdijet_order3_e))
        func_toy_vvdijet.fitTo(dse,ROOT.RooFit.Save(),ROOT.RooFit.SumW2Error(ROOT.kTRUE)) 
        toydatae = func_toy_vvdijet.generate(ROOT.RooArgSet(mt_res),ne)
        func_toy_vvdijet.fitTo(dsm,ROOT.RooFit.Save(),ROOT.RooFit.SumW2Error(ROOT.kTRUE))
        toydatam = func_toy_vvdijet.generate(ROOT.RooArgSet(mt_res),nm)
        toydatae.SetName ('data_elA'+year+'_mt_res_base')
        toydatam.SetName ('data_muA'+year+'_mt_res_base')
        import_workspace( ws_out, dse)
        import_workspace( ws_out, dsm)
    else:
        frame_toy = mt_res.frame(ROOT.RooFit.Title("Unbinned ML fit, el"))
        dse.plotOn(frame_toy,ROOT.RooFit.DataError(ROOT.RooAbsData.SumW2))
        chi2score_e=[]
        multipdfse=[func_dijet_e,func_vvdijet_e,func_expow_e]
        for toypdf in multipdfse:
            toypdf.plotOn(frame_toy)
            chi2score_e.append((frame_toy.chiSquare()-1))
        chi2score_m=[]
        multipdfsm=[func_dijet_m,func_vvdijet_m,func_expow_m]
        for toypdf in multipdfsm:
            toypdf.plotOn(frame_toy)
            chi2score_m.append((frame_toy.chiSquare()-1))
        rseed = ROOT.RooRandom.randomGenerator()
        rseed.SetSeed(100)
        toydatae = multipdfse[np.argmin(np.abs(chi2score_e))].generate(ROOT.RooArgSet(mt_res),ne)
        toydatam = multipdfsm[np.argmin(np.abs(chi2score_m))].generate(ROOT.RooArgSet(mt_res),nm)
        print('------------> set index to e: ', np.argmin(np.abs(chi2score_e)), ' m: ', np.argmin(np.abs(chi2score_m)))
        catIndexe.setIndex(np.argmin(np.abs(chi2score_e)))
        catIndexm.setIndex(np.argmin(np.abs(chi2score_m)))
        toydatae.SetName ('data_elA'+year+'_mt_res_base')
        toydatam.SetName ('data_muA'+year+'_mt_res_base')
        #import_workspace( ws_out, toydatae)
        #import_workspace( ws_out, toydatam)
        import_workspace( ws_out, dse)
        import_workspace( ws_out, dsm)

    import_workspace( ws_out, norm_MultiPdf_e )
    import_workspace( ws_out, norm_MultiPdf_m )
    import_workspace( ws_out, catIndexe )
    import_workspace( ws_out, catIndexm )
    getattr( ws_out , "import")( multipdfe, ROOT.RooFit.RecycleConflictNodes() )
    getattr( ws_out , "import")( multipdfm, ROOT.RooFit.RecycleConflictNodes() )
    ws_out.writeToFile( rootfilename )
    return
    frame_e = mt_res.frame(ROOT.RooFit.Title("Unbinned ML fit, el"))
    frame_m = mt_res.frame(ROOT.RooFit.Title("Unbinned ML fit, mu"))
    toydatae.plotOn(frame_e,ROOT.RooFit.DataError(ROOT.RooAbsData.SumW2))
    toydatam.plotOn(frame_m,ROOT.RooFit.DataError(ROOT.RooAbsData.SumW2))
    func_dijet_e.plotOn(frame_e)
    func_dijet_m.plotOn(frame_m)
    func_vvdijet_e.plotOn(frame_e)
    func_vvdijet_m.plotOn(frame_m)
    #func_atlas_e.plotOn(frame_e)
    #func_atlas_m.plotOn(frame_m)
    func_expow_e.plotOn(frame_e)
    func_expow_m.plotOn(frame_m)

    for ch, frame in zip(["el","mu"],[frame_e, frame_m]):
        c = ROOT.TCanvas("c","c",600,600) ;
        ROOT.gStyle.SetOptStat(0)
        c.SetFillColor(0)
        c.SetBorderMode(0)
        c.SetBorderSize(2)
        c.SetFrameBorderMode(0)
        #------------>Primitives in pad: toppad
        toppad = ROOT.TPad('toppad','toppad',0,0.3 ,1.0,1.0)
        bottompad = ROOT.TPad('bottompad','bottompad',0,0.0,1.0,0.32)
        canvas_margin(c,toppad,bottompad)
        toppad.SetFillStyle(4000)
        toppad.SetFrameFillStyle(1000)
        toppad.SetFrameFillColor(0)
        toppad.SetFillColor(0)
        toppad.SetBorderMode(0)
        toppad.SetBorderSize(2)
        #toppad.SetLogy()
        toppad.SetFrameBorderMode(0)
        toppad.SetFrameBorderMode(0)
        toppad.SetLeftMargin(0.15)
        bottompad.SetFillStyle(4000)
        bottompad.SetFrameFillStyle(1000)
        bottompad.SetFrameFillColor(0)
        bottompad.SetFillColor(0)
        bottompad.SetBorderMode(0)
        bottompad.SetBorderSize(2)
        bottompad.SetFrameBorderMode(0)
        bottompad.SetFrameBorderMode(0)
        toppad.Draw()
        bottompad.Draw()

        c.cd()
        c.Update()
        c.RedrawAxis()
        cframe = c.GetFrame()
        cframe.Draw()
        toppad.cd()
        frame_4fa51a0__1 = ROOT.TH1D("frame_4fa51a0__1","Unbinned ML fit, %s %s"%(ch,year),100,200,1000)
        frame_4fa51a0__1.GetXaxis().SetTitle("mt_res");
        frame_4fa51a0__1.GetXaxis().SetLabelFont(42);
        frame_4fa51a0__1.GetXaxis().SetLabelSize(0.05);
        frame_4fa51a0__1.GetXaxis().SetTitleSize(0.05);
        frame_4fa51a0__1.GetXaxis().SetTitleOffset(1);
        frame_4fa51a0__1.GetXaxis().SetTitleFont(42);
        frame_4fa51a0__1.GetYaxis().SetTitle("Events / ( 18 )");
        frame_4fa51a0__1.GetYaxis().SetLabelFont(42);
        frame_4fa51a0__1.GetYaxis().SetLabelSize(0.05);
        frame_4fa51a0__1.GetYaxis().SetTitleSize(0.05);
        frame_4fa51a0__1.GetYaxis().SetTitleFont(42);
        frame_4fa51a0__1.GetYaxis().SetRangeUser(0.1,1e3)
        frame_4fa51a0__1.GetXaxis().SetLabelOffset(999)
        frame_4fa51a0__1.GetXaxis().SetLabelSize(0)
        frame_4fa51a0__1.Draw("AXISSAME");
        frame.Draw("same")

        hpull = frame.pullHist()
        frame3 = mt_res.frame(ROOT.RooFit.Title("Pull Distribution"))
        frame3.addPlotable(hpull, "P")

        leg = ROOT.TLegend(0.55,0.6,0.95,0.85);
        leg.SetBorderSize(0);
        leg.SetLineStyle(1);
        leg.SetLineWidth(1);
        entry=leg.AddEntry(frame,"data","lp");
        entry.SetFillStyle(1001);
        entry.SetMarkerStyle(8);
        entry.SetMarkerSize(1.5);
        entry.SetLineStyle(1);
        entry.SetLineWidth(2);
        entry.SetTextFont(42);
        entry.SetTextSize(0.06);
        entry=leg.AddEntry("","Fit","l");
        entry.SetFillStyle(1001);
        entry.SetLineStyle(1);
        entry.SetLineWidth(2);
        entry.SetLineColor(ROOT.kBlue);
        entry.SetMarkerStyle(20);
        entry.SetTextFont(42);
        entry.SetTextSize(0.06);
        htmp=ROOT.TH1F("htmp","htmp",10,0,1)
        htmp.SetFillColor(ROOT.kGreen)
        entry=leg.AddEntry(htmp,"1-sigma error band","f");
        entry.SetFillStyle(1001);
        entry.SetLineStyle(1);
        entry.SetLineWidth(2);
        entry.SetMarkerStyle(20);
        entry.SetTextFont(42);
        entry.SetTextSize(0.06);
        leg.Draw()

        bottompad.cd()
        frame_4fa51a0__2 = ROOT.TH1D("frame_4fa51a0__2","",100,200,1000)
        frame_4fa51a0__2.GetXaxis().SetTitle("mt_res [GeV]");
        frame_4fa51a0__2.GetXaxis().SetLabelFont(42);
        frame_4fa51a0__2.GetXaxis().SetLabelSize(0.1);
        frame_4fa51a0__2.GetXaxis().SetTitleSize(0.1);
        frame_4fa51a0__2.GetXaxis().SetTitleOffset(1);
        frame_4fa51a0__2.GetXaxis().SetTitleFont(42);
        frame_4fa51a0__2.GetYaxis().SetTitle("Pull");
        frame_4fa51a0__2.GetYaxis().SetLabelFont(42);
        frame_4fa51a0__2.GetYaxis().SetLabelSize(0.15);
        frame_4fa51a0__2.GetYaxis().SetTitleSize(0.15);
        frame_4fa51a0__2.GetYaxis().SetTitleFont(42);
        frame_4fa51a0__2.GetYaxis().SetNdivisions(4)
        frame_4fa51a0__2.GetYaxis().SetRangeUser(-3,3)
        frame_4fa51a0__2.GetYaxis().SetTitleOffset(0.4)
        frame_4fa51a0__2.Draw("AXISSAME")
        frame3.Draw("same")
        input('wait..')
        c.SaveAs('fit_%s%s.png' %( year,ch))


def prepareWS(year,baseDir,skimtree,skimfile):

    #prepare Working Space with Roofit
    #Reading Data
    mt_res = ROOT.RooRealVar("mt_res", "mt_res", 0, 3000);
    mt_res.setRange( MIN_ ,MAX_)
    F=ROOT.TFile(baseDir+'/el'+year+'_'+skimfile)
    tree=F.Get(skimtree)
    print('read ',baseDir+'/el'+year+'_'+skimfile)
    #print('tot:',tree.GetEntries())
    netot = tree.GetEntries()
    dse = ROOT.RooDataSet('data_elA'+year+'_mt_res_base', "dse", ROOT.RooArgSet(mt_res), ROOT.RooFit.Import(tree));
    F=ROOT.TFile(baseDir+'/mu'+year+'_'+skimfile)
    tree=F.Get(skimtree)
    print('read ',baseDir+'/mu'+year+'_'+skimfile)
    #print('tot:',tree.GetEntries())
    nmtot = tree.GetEntries()
    dsm = ROOT.RooDataSet('data_muA'+year+'_mt_res_base', "dsm", ROOT.RooArgSet(mt_res), ROOT.RooFit.Import(tree));


    ne = dse.sumEntries("mt_res>"+str(MIN_))
    nm = dsm.sumEntries("mt_res>"+str(MIN_))
    
    integral_var_e = ROOT.RooRealVar('%s_norm' %( 'dijet_elA'+year+'_all_dijet' ),
                        'normalization', ne )
    integral_var_m = ROOT.RooRealVar('%s_norm' %( 'dijet_muA'+year+'_all_dijet' ),
                        'normalization', nm )
    #dijet_order1_e = ROOT.RooRealVar('dijet_order1_elA'+year+'_all_dijet', "power1", -9, -50.0, 0)
    #dijet_order1_m = ROOT.RooRealVar('dijet_order1_muA'+year+'_all_dijet', "power1", -9, -50.0, 0)
    #dijet_order2_e = ROOT.RooRealVar('dijet_order2_elA'+year+'_all_dijet', "power2", -2, -10.0, 0)
    #dijet_order2_m = ROOT.RooRealVar('dijet_order2_muA'+year+'_all_dijet', "power2", -2, -10.0, 0)
    #dijet_order3_e = ROOT.RooRealVar('dijet_order3_elA'+year+'_all_dijet', "power3", -1.5, -100.0, 0)
    #dijet_order3_m = ROOT.RooRealVar('dijet_order3_muA'+year+'_all_dijet', "power3", -1.5, -100.0, 0)

    #dijet_order1_e = ROOT.RooRealVar('dijet_order1_A'+year+'_all_dijet', "power1", -9, -50.0, 0)
    #dijet_order1_m = ROOT.RooRealVar('dijet_order1_A'+year+'_all_dijet', "power1", -9, -50.0, 0)
    #dijet_order2_e = ROOT.RooRealVar('dijet_order2_A'+year+'_all_dijet', "power2", -2, -10.0, 0)
    #dijet_order2_m = ROOT.RooRealVar('dijet_order2_A'+year+'_all_dijet', "power2", -2, -10.0, 0)

    dijet_order1_e = ROOT.RooRealVar('dijet_order1_A_all_dijet', "power1", -9, -50.0, -0.01)
    dijet_order1_m = ROOT.RooRealVar('dijet_order1_A_all_dijet', "power1", -9, -50.0, -0.01)
    dijet_order2_e = ROOT.RooRealVar('dijet_order2_A_all_dijet', "power2", -2, -10.0, -0.01)
    dijet_order2_m = ROOT.RooRealVar('dijet_order2_A_all_dijet', "power2", -2, -10.0, -0.01)
    dijet_order3_e = ROOT.RooRealVar('dijet_order3_A_all_dijet', "power3", 0, -5.0, 5)
    dijet_order3_m = ROOT.RooRealVar('dijet_order3_A_all_dijet', "power3", 0, -5.0, 5)
    #dijet_order4_e = ROOT.RooRealVar('dijet_order4_A_all_dijet', "power4", -2, -10.0, -0.01)
    #dijet_order4_m = ROOT.RooRealVar('dijet_order4_A_all_dijet', "power4", -2, -10.0, -0.01)

    #Work space
    ws_out  = ROOT.RooWorkspace( "workspace_all" )
    rootfilename = '%s/%s/%s.root' %( data_outDir,year,ws_out.GetName() )

   # toy1 = ROOT.RooRealVar('power1', "power1", -72, -200, 200)
   # toy2 = ROOT.RooRealVar('power2', "power2", 22, -200, 200)
   # toy3 = ROOT.RooRealVar('power3', "power3", 5, -200, 200)
   # toy1.setError(0.001)
   # toy2.setError(0.001)
   # toy3.setError(0.001)
   # func_toy_e = ROOT.RooGenericPdf( 'toy', 'toy', 'TMath::Power( (1-@0/13000.), @1 ) / ( TMath::Power( @0/13000. , @2+ @3*TMath::Power(TMath::Log10( @0/13000.),1) ))', ROOT.RooArgList(mt_res,toy1,toy2,toy3))
   # toydatae = func_toy_e.generate(ROOT.RooArgSet(mt_res),ne)
   # toydatam = func_toy_e.generate(ROOT.RooArgSet(mt_res),nm)
   # toydatae.SetName ('data_elA'+year+'_mt_res_base')
   # toydatam.SetName ('data_muA'+year+'_mt_res_base')
   # import_workspace( ws_out, toydatae)
   # import_workspace( ws_out, toydatam)

    import_workspace( ws_out, dse)
    import_workspace( ws_out, dsm)

    #p.d.f
    do_dijet=True
    if do_dijet:
        function = ''
        func_name = 'dijet'
        if func_name == 'dijet' :
            order_entries = []
            log_str = 'TMath::Log10(@0/13000)'
            for i in range( 1, 3) :
                order_entries.append('@'+str(i+1)+'*' + '*'.join( [log_str]*i))
            function = 'TMath::Power( @0/13000., @1 + ' + '+'.join( order_entries) + ')'
            print "function: ", function
            #function = 'TMath::Power( @0/13000., @1 + @2*TMath::Log10(@0/13000)*(1+@3*TMath::Log10(@0/13000)))'
            func_pdf_e = ROOT.RooGenericPdf( '%s_%s'%(func_name, 'elA'+year+'_all_dijet'), func_name, function, ROOT.RooArgList(mt_res,dijet_order1_e,dijet_order2_e,dijet_order3_e))
            func_pdf_m = ROOT.RooGenericPdf( '%s_%s'%(func_name, 'muA'+year+'_all_dijet'), func_name, function, ROOT.RooArgList(mt_res,dijet_order1_m,dijet_order2_m,dijet_order3_m))

        #Fit to model
        resu_e = func_pdf_e.fitTo(dse,ROOT.RooFit.Save(),ROOT.RooFit.SumW2Error(ROOT.kTRUE))
        resu_m = func_pdf_m.fitTo(dsm,ROOT.RooFit.Save(),ROOT.RooFit.SumW2Error(ROOT.kTRUE))

        frame_e = mt_res.frame(ROOT.RooFit.Title("Unbinned ML fit, el"))
        frame_m = mt_res.frame(ROOT.RooFit.Title("Unbinned ML fit, mu"))
        dse.plotOn(frame_e,ROOT.RooFit.DataError(ROOT.RooAbsData.SumW2))
        dsm.plotOn(frame_m,ROOT.RooFit.DataError(ROOT.RooAbsData.SumW2))
        func_pdf_m.plotOn(frame_m, ROOT.RooFit.VisualizeError(resu_m, 1),ROOT.RooFit.FillColor(ROOT.kOrange))
        func_pdf_e.plotOn(frame_e, ROOT.RooFit.VisualizeError(resu_e, 1), ROOT.RooFit.FillColor(ROOT.kOrange))
        func_pdf_e.plotOn(frame_e)
        func_pdf_m.plotOn(frame_m)
        dse.plotOn(frame_e,ROOT.RooFit.DataError(ROOT.RooAbsData.SumW2))
        dsm.plotOn(frame_m,ROOT.RooFit.DataError(ROOT.RooAbsData.SumW2)) 
        print("===> fit result")
        resu_e.Print()
        print("chi^2 = ", frame_e.chiSquare())
        print("netot:", netot)
        print("===> fit result")
        resu_m.Print()
        print "function: ", function
        print("chi^2 = ", frame_m.chiSquare())
        print("nmtot:", nmtot)
        print(func_pdf_e.Print())
        print(func_pdf_m.Print())

        import_workspace( ws_out, mt_res)
        import_workspace( ws_out, dijet_order1_e )
        import_workspace( ws_out, dijet_order1_m )
        import_workspace( ws_out, dijet_order2_e )
        import_workspace( ws_out, dijet_order2_m )
        import_workspace( ws_out, dijet_order3_e )
        import_workspace( ws_out, dijet_order3_m )
        #import_workspace( ws_out, dijet_order4_e )
        #import_workspace( ws_out, dijet_order4_m )
        import_workspace( ws_out, func_pdf_e )
        import_workspace( ws_out, func_pdf_m )
        import_workspace( ws_out, integral_var_e )
        import_workspace( ws_out, integral_var_m )

    do_expow=False
    if do_expow:
        function = ''
        func_name = 'expow'
        expow_order0_e = ROOT.RooRealVar( 'expow_order1_elA'+year+'_all_expow', "power0", -5,       -100,   100)
        expow_order1_e = ROOT.RooRealVar( 'expow_order2_elA'+year+'_all_expow', "power1", -10,    -200,   100)
        expow_order0_m = ROOT.RooRealVar( 'expow_order1_muA'+year+'_all_expow', "power0", -5,       -100,   100)
        expow_order1_m = ROOT.RooRealVar( 'expow_order2_muA'+year+'_all_expow', "power1", -10,    -200,   100)
        #expow_order2_e = ROOT.RooRealVar( 'expow_order3_elA'+year+'_all_expow', "power2", 0,        -200,    0)
        #expow_order2_m = ROOT.RooRealVar( 'expow_order3_muA'+year+'_all_expow', "power2", 0,        -200,    0)

        #expow_order3_e = ROOT.RooRealVar( 'expow_order3_elA'+year+'_all_expow', "power3", 5,        -200,    200)
        #expow_order3_m = ROOT.RooRealVar( 'expow_order3_muA'+year+'_all_expow', "power3", 5,        -200,    200)

        integral_exp_e = ROOT.RooRealVar('%s_norm' %( 'expow_elA'+year+'_all_expow' ),
                            'normalization', ne )
        integral_exp_m = ROOT.RooRealVar('%s_norm' %( 'expow_muA'+year+'_all_expow' ),
                            'normalization', nm )

        order_entries = []
        function =  'TMath::Power( @0 / 13000., @1 ) * TMath::Exp(%s)'
        for i in range( 0, 2 ) :
            order_entries.append( ('@%d' %(i+2)) + "*@0/13000."*(i+1) )

        function = function %("+".join(order_entries))
        print(function)
        exit()
        func_exp_m = ROOT.RooGenericPdf( '%s_%s'%(func_name, 'muA'+year+'_all_expow'), '%s_%s'%(func_name, 'muA'+year+'_all_expow'), function, ROOT.RooArgList(mt_res, expow_order0_m, expow_order1_m,expow_order2_m))
        func_exp_e = ROOT.RooGenericPdf( '%s_%s'%(func_name, 'elA'+year+'_all_expow'), '%s_%s'%(func_name, 'elA'+year+'_all_expow'), function, ROOT.RooArgList(mt_res, expow_order0_e, expow_order1_e,expow_order2_e))
        resu_exp_e = func_exp_e.fitTo(dse,ROOT.RooFit.Save(),ROOT.RooFit.SumW2Error(ROOT.kTRUE))
        resu_exp_m = func_exp_m.fitTo(dsm,ROOT.RooFit.Save(),ROOT.RooFit.SumW2Error(ROOT.kTRUE))

        frame_e = mt_res.frame(ROOT.RooFit.Title("Unbinned ML fit, el"))
        frame_m = mt_res.frame(ROOT.RooFit.Title("Unbinned ML fit, mu"))
        dse.plotOn(frame_e,ROOT.RooFit.DataError(ROOT.RooAbsData.SumW2))
        dsm.plotOn(frame_m,ROOT.RooFit.DataError(ROOT.RooAbsData.SumW2))
        func_exp_m.plotOn(frame_m, ROOT.RooFit.VisualizeError(resu_exp_m, 1),ROOT.RooFit.FillColor(ROOT.kOrange))
        func_exp_e.plotOn(frame_e, ROOT.RooFit.VisualizeError(resu_exp_e, 1), ROOT.RooFit.FillColor(ROOT.kOrange))
        func_exp_e.plotOn(frame_e)
        func_exp_m.plotOn(frame_m)
        dse.plotOn(frame_e,ROOT.RooFit.DataError(ROOT.RooAbsData.SumW2))
        dsm.plotOn(frame_m,ROOT.RooFit.DataError(ROOT.RooAbsData.SumW2))
        print("===> fit result")
        resu_exp_e.Print()
        print("chi^2 = ", frame_e.chiSquare())
        print("netot:", netot)
        print("===> fit result")
        resu_exp_m.Print()
        print "function: ", function
        print("chi^2 = ", frame_m.chiSquare())
        print("nmtot:", nmtot)
        print(func_exp_e.Print())
        print(func_exp_m.Print())
        
        import_workspace( ws_out, expow_order0_e)
        import_workspace( ws_out, expow_order1_e)
        #import_workspace( ws_out, expow_order2_e)
        import_workspace( ws_out, expow_order0_m)
        import_workspace( ws_out, expow_order1_m)
        #import_workspace( ws_out, expow_order2_m)
        #import_workspace( ws_out, expow_order3_e)
        #import_workspace( ws_out, expow_order3_m)
        import_workspace( ws_out, func_exp_e)
        import_workspace( ws_out, func_exp_m)
        import_workspace( ws_out, integral_exp_e )
        import_workspace( ws_out, integral_exp_m )

    do_vvdijet=True
    if do_vvdijet:
        function = ''
        func_name = 'vvdijet'
        #vvdijet_order1_e = ROOT.RooRealVar( 'vvdijet_order1_elA'+year+'_all_vvdijet', "power1", 40 ,      0,  100)
        #vvdijet_order2_e = ROOT.RooRealVar( 'vvdijet_order2_elA'+year+'_all_vvdijet', "power2", 2.5 ,     0,   100)
        #vvdijet_order3_e = ROOT.RooRealVar( 'vvdijet_order3_elA'+year+'_all_vvdijet', "power3", 1 ,       0,    100)
        #vvdijet_order1_m = ROOT.RooRealVar( 'vvdijet_order1_muA'+year+'_all_vvdijet', "power1", 40 ,      0,  100)
        #vvdijet_order2_m = ROOT.RooRealVar( 'vvdijet_order2_muA'+year+'_all_vvdijet', "power2", 2.5 ,     0,   100)
        #vvdijet_order3_m = ROOT.RooRealVar( 'vvdijet_order3_muA'+year+'_all_vvdijet', "power3", 1 ,       0,    100)

        #vvdijet_order1_e = ROOT.RooRealVar( 'vvdijet_order1_elA'+year+'_all_vvdijet', "power1", 40 ,      -100,  100)
        #vvdijet_order2_e = ROOT.RooRealVar( 'vvdijet_order2_elA'+year+'_all_vvdijet', "power2", 2.5 ,     -100,   100)
        #vvdijet_order3_e = ROOT.RooRealVar( 'vvdijet_order3_elA'+year+'_all_vvdijet', "power3", 1 ,       -100,    100)
        #vvdijet_order1_m = ROOT.RooRealVar( 'vvdijet_order1_muA'+year+'_all_vvdijet', "power1", 40 ,      -100,  100)
        #vvdijet_order2_m = ROOT.RooRealVar( 'vvdijet_order2_muA'+year+'_all_vvdijet', "power2", 2.5 ,     -100,   100)
        #vvdijet_order3_m = ROOT.RooRealVar( 'vvdijet_order3_muA'+year+'_all_vvdijet', "power3", 1 ,       -100,    100)

        #vvdijet_order1_e = ROOT.RooRealVar( 'vvdijet_order1_A'+year+'_all_vvdijet', "power1", 90 ,      0,  100)
        #vvdijet_order2_e = ROOT.RooRealVar( 'vvdijet_order2_A'+year+'_all_vvdijet', "power2", -6 ,     -100,   0)
        #vvdijet_order3_e = ROOT.RooRealVar( 'vvdijet_order3_A'+year+'_all_vvdijet', "power3", -2 ,       -100,    0)
        #vvdijet_order1_m = ROOT.RooRealVar( 'vvdijet_order1_A'+year+'_all_vvdijet', "power1", 90 ,      0,  100)
        #vvdijet_order2_m = ROOT.RooRealVar( 'vvdijet_order2_A'+year+'_all_vvdijet', "power2", -6 ,     -100,   0)
        #vvdijet_order3_m = ROOT.RooRealVar( 'vvdijet_order3_A'+year+'_all_vvdijet', "power3", -2 ,       -100,    0)        

        #vvdijet_order1_e = ROOT.RooRealVar( 'vvdijet_order1_A_all_vvdijet', "power1", 90 ,      0,  200)
        #vvdijet_order2_e = ROOT.RooRealVar( 'vvdijet_order2_A_all_vvdijet', "power2", -6 ,     -100,   0)
        #vvdijet_order3_e = ROOT.RooRealVar( 'vvdijet_order3_A_all_vvdijet', "power3", -2 ,       -100,    0)
        #vvdijet_order1_m = ROOT.RooRealVar( 'vvdijet_order1_A_all_vvdijet', "power1", 90 ,      0,  200)
        #vvdijet_order2_m = ROOT.RooRealVar( 'vvdijet_order2_A_all_vvdijet', "power2", -6 ,     -100,   0)
        #vvdijet_order3_m = ROOT.RooRealVar( 'vvdijet_order3_A_all_vvdijet', "power3", -2 ,       -100,    0)

        #vvdijet_order1_e = ROOT.RooRealVar( 'vvdijet_order1_A_all_vvdijet', "power1", -10 ,      -100,  0)
        #vvdijet_order2_e = ROOT.RooRealVar( 'vvdijet_order2_A_all_vvdijet', "power2", 10 ,     0,   40)
        #vvdijet_order3_e = ROOT.RooRealVar( 'vvdijet_order3_A_all_vvdijet', "power3", 3 ,       0,    20)
        #vvdijet_order1_m = ROOT.RooRealVar( 'vvdijet_order1_A_all_vvdijet', "power1", -10 ,      -100,  0)
        #vvdijet_order2_m = ROOT.RooRealVar( 'vvdijet_order2_A_all_vvdijet', "power2", 10 ,     0,   40)
        #vvdijet_order3_m = ROOT.RooRealVar( 'vvdijet_order3_A_all_vvdijet', "power3", 3 ,       0,    20)


        #vvdijet_order1_e = ROOT.RooRealVar( 'vvdijet_order1_elA'+year+'_all_vvdijet', "power1", 70 ,      0,  200)
        #vvdijet_order2_e = ROOT.RooRealVar( 'vvdijet_order2_elA'+year+'_all_vvdijet', "power2", -30 ,     -200,   200)
        #vvdijet_order3_e = ROOT.RooRealVar( 'vvdijet_order3_elA'+year+'_all_vvdijet', "power3", -2 ,       -200,    0)
        #vvdijet_order1_m = ROOT.RooRealVar( 'vvdijet_order1_muA'+year+'_all_vvdijet', "power1", 70 ,      0,  200)
        #vvdijet_order2_m = ROOT.RooRealVar( 'vvdijet_order2_muA'+year+'_all_vvdijet', "power2", -30 ,     -200,   200)
        #vvdijet_order3_m = ROOT.RooRealVar( 'vvdijet_order3_muA'+year+'_all_vvdijet', "power3", -2 ,       -200,    0)

        vvdijet_order1_e = ROOT.RooRealVar( 'vvdijet_order1_A_all_vvdijet', "power1", 40 ,      0.01,  50)
        vvdijet_order2_e = ROOT.RooRealVar( 'vvdijet_order2_A_all_vvdijet', "power2", 2 ,     0.01,   10)
        vvdijet_order3_e = ROOT.RooRealVar( 'vvdijet_order3_A_all_vvdijet', "power3", 0 ,       -20,    20)
        #vvdijet_order4_e = ROOT.RooRealVar( 'vvdijet_order4_A_all_vvdijet', "power4", -2 ,       -200,    0)
        vvdijet_order1_m = ROOT.RooRealVar( 'vvdijet_order1_A_all_vvdijet', "power1", 40 ,      0.01,  50)
        vvdijet_order2_m = ROOT.RooRealVar( 'vvdijet_order2_A_all_vvdijet', "power2", 2 ,     0.01,   10)
        vvdijet_order3_m = ROOT.RooRealVar( 'vvdijet_order3_A_all_vvdijet', "power3", 0 ,       -20,    20)
        #vvdijet_order4_m = ROOT.RooRealVar( 'vvdijet_order4_A_all_vvdijet', "power4", -2 ,       -200,    0)

        #if str(year) == '2016':
        #    vvdijet_order1_e = ROOT.RooRealVar( 'vvdijet_order1_elA'+year+'_all_vvdijet', "power1", 52.5 ,      0,  100)
        #    vvdijet_order2_e = ROOT.RooRealVar( 'vvdijet_order2_elA'+year+'_all_vvdijet', "power2", 0 ,     -100,   0)
        #    vvdijet_order3_e = ROOT.RooRealVar( 'vvdijet_order3_elA'+year+'_all_vvdijet', "power3", -0.6 ,       -100,    0)
        #    vvdijet_order1_m = ROOT.RooRealVar( 'vvdijet_order1_muA'+year+'_all_vvdijet', "power1", -15 ,      -100,  0)
        #    vvdijet_order2_m = ROOT.RooRealVar( 'vvdijet_order2_muA'+year+'_all_vvdijet', "power2", 13.4 ,     0,   100)
        #    vvdijet_order3_m = ROOT.RooRealVar( 'vvdijet_order3_muA'+year+'_all_vvdijet', "power3", 2.9 ,       0,    100)
        #    #vvdijet_order1_m = ROOT.RooRealVar( 'vvdijet_order1_muA'+year+'_all_vvdijet', "power1", 67.7 ,      0,  100)
        #    #vvdijet_order2_m = ROOT.RooRealVar( 'vvdijet_order2_muA'+year+'_all_vvdijet', "power2", 0 ,     -100,   0)
        #    #vvdijet_order3_m = ROOT.RooRealVar( 'vvdijet_order3_muA'+year+'_all_vvdijet', "power3", -0.5 ,       -100,    0)
        #if str(year) == '2017':
        #    vvdijet_order1_e = ROOT.RooRealVar( 'vvdijet_order1_elA'+year+'_all_vvdijet', "power1", -9 ,      -100,  0)
        #    vvdijet_order2_e = ROOT.RooRealVar( 'vvdijet_order2_elA'+year+'_all_vvdijet', "power2", 10.2 ,     0,   100)
        #    vvdijet_order3_e = ROOT.RooRealVar( 'vvdijet_order3_elA'+year+'_all_vvdijet', "power3", 2.1 ,       0,    100)
        #    vvdijet_order1_m = ROOT.RooRealVar( 'vvdijet_order1_muA'+year+'_all_vvdijet', "power1", -37 ,      -100,  0)
        #    vvdijet_order2_m = ROOT.RooRealVar( 'vvdijet_order2_muA'+year+'_all_vvdijet', "power2", 16 ,     0,   100)
        #    vvdijet_order3_m = ROOT.RooRealVar( 'vvdijet_order3_muA'+year+'_all_vvdijet', "power3", 3.5 ,       0,    100)
        #if str(year) == '2018':
        #    vvdijet_order1_e = ROOT.RooRealVar( 'vvdijet_order1_elA'+year+'_all_vvdijet', "power1", 75 ,      0,  100)
        #    vvdijet_order2_e = ROOT.RooRealVar( 'vvdijet_order2_elA'+year+'_all_vvdijet', "power2", -32 ,     -100,   0)
        #    vvdijet_order3_e = ROOT.RooRealVar( 'vvdijet_order3_elA'+year+'_all_vvdijet', "power3", -2 ,       -100,    0)
        #    vvdijet_order1_m = ROOT.RooRealVar( 'vvdijet_order1_muA'+year+'_all_vvdijet', "power1", -72 ,      -100,  0)
        #    vvdijet_order2_m = ROOT.RooRealVar( 'vvdijet_order2_muA'+year+'_all_vvdijet', "power2", 20 ,     0,   100)
        #    vvdijet_order3_m = ROOT.RooRealVar( 'vvdijet_order3_muA'+year+'_all_vvdijet', "power3", 5 ,       0,    100)


        integral_vvdi_e = ROOT.RooRealVar('%s_norm' %( 'vvdijet_elA'+year+'_all_vvdijet' ),
                            'normalization', ne )
        integral_vvdi_m = ROOT.RooRealVar('%s_norm' %( 'vvdijet_muA'+year+'_all_vvdijet' ),
                            'normalization', nm )

        function = 'TMath::Power( (1-@0/13000.), @1 ) / ( TMath::Power( @0/13000. , @2+ %s ))'
        order_entries = []
        for i in range( 0, 1 ) :
            order_entries.append( '@%d*TMath::Power' %(i+3)+
                                  '(TMath::Log10( @0/13000.),%d)'  %(i+1 ) )
        function = function % (' + '.join( order_entries ))
        print(function)
        #function = 'TMath::Power( (1-@0/13000.), @1 ) / ( TMath::Power( @0/13000. , @2))'
        func_vvdi_m = ROOT.RooGenericPdf( '%s_%s'%(func_name, 'muA'+year+'_all_vvdijet'), '%s_%s'%(func_name, 'muA'+year+'_all_vvdijet'), function, ROOT.RooArgList(mt_res, vvdijet_order1_m, vvdijet_order2_m,vvdijet_order3_m))
        func_vvdi_e = ROOT.RooGenericPdf( '%s_%s'%(func_name, 'elA'+year+'_all_vvdijet'), '%s_%s'%(func_name, 'elA'+year+'_all_vvdijet'), function, ROOT.RooArgList(mt_res, vvdijet_order1_e, vvdijet_order2_e,vvdijet_order3_e))
        resu_vvdi_e = func_vvdi_e.fitTo(dse,ROOT.RooFit.Save(),ROOT.RooFit.SumW2Error(ROOT.kTRUE))
        resu_vvdi_m = func_vvdi_m.fitTo(dsm,ROOT.RooFit.Save(),ROOT.RooFit.SumW2Error(ROOT.kTRUE))
        frame_e = mt_res.frame(ROOT.RooFit.Title("Unbinned ML fit, el"))
        frame_m = mt_res.frame(ROOT.RooFit.Title("Unbinned ML fit, mu"))
        dse.plotOn(frame_e,ROOT.RooFit.DataError(ROOT.RooAbsData.SumW2))
        dsm.plotOn(frame_m,ROOT.RooFit.DataError(ROOT.RooAbsData.SumW2))
        func_vvdi_m.plotOn(frame_m, ROOT.RooFit.VisualizeError(resu_vvdi_m, 2),ROOT.RooFit.FillColor(ROOT.kOrange))
        func_vvdi_e.plotOn(frame_e, ROOT.RooFit.VisualizeError(resu_vvdi_e, 2), ROOT.RooFit.FillColor(ROOT.kOrange))
        func_vvdi_m.plotOn(frame_m, ROOT.RooFit.VisualizeError(resu_vvdi_m, 1),ROOT.RooFit.FillColor(ROOT.kGreen))
        func_vvdi_e.plotOn(frame_e, ROOT.RooFit.VisualizeError(resu_vvdi_e, 1), ROOT.RooFit.FillColor(ROOT.kGreen))
        func_vvdi_e.plotOn(frame_e)
        func_vvdi_m.plotOn(frame_m)
        dse.plotOn(frame_e,ROOT.RooFit.DataError(ROOT.RooAbsData.SumW2))
        dsm.plotOn(frame_m,ROOT.RooFit.DataError(ROOT.RooAbsData.SumW2))
        print("===> fit result")
        resu_vvdi_e.Print()
        print("chi^2 = ", frame_e.chiSquare())
        print("netot:", netot)
        print("===> fit result")
        resu_vvdi_m.Print()
        print "function: ", function
        print("chi^2 = ", frame_m.chiSquare())
        print("nmtot:", nmtot)
        print(func_vvdi_e.Print())
        print(func_vvdi_m.Print())

        #vvdijet_order1_e.setVal(74.7572)
        #vvdijet_order2_e.setVal(-3.18609)
        #vvdijet_order3_e.setVal(-1.3619)
        #vvdijet_order1_m.setVal(74.7572)
        #vvdijet_order2_m.setVal(-3.18609)
        #vvdijet_order3_m.setVal(-1.3619)

        import_workspace( ws_out, vvdijet_order1_e)
        import_workspace( ws_out, vvdijet_order2_e)
        import_workspace( ws_out, vvdijet_order1_m)
        import_workspace( ws_out, vvdijet_order2_m)
        import_workspace( ws_out, vvdijet_order3_e)
        import_workspace( ws_out, vvdijet_order3_m)
        #import_workspace( ws_out, vvdijet_order4_e)
        #import_workspace( ws_out, vvdijet_order4_m)
        import_workspace( ws_out, func_vvdi_e)
        import_workspace( ws_out, func_vvdi_m)
        import_workspace( ws_out, integral_vvdi_e )
        import_workspace( ws_out, integral_vvdi_m )    

    do_atlas=False
    if do_atlas:
        function = ''
        func_name = 'atlas'

        atlas_order1_e = ROOT.RooRealVar( 'atlas_order1_A_all_atlas', "power1", 0 ,      0,  100)
        atlas_order2_e = ROOT.RooRealVar( 'atlas_order2_A_all_atlas', "power2", 9 ,     -100,   0)
        atlas_order3_e = ROOT.RooRealVar( 'atlas_order3_A_all_atlas', "power3", 1 ,       -100,    0)
        atlas_order1_m = ROOT.RooRealVar( 'atlas_order1_A_all_atlas', "power1", 0 ,      0,  100)
        atlas_order2_m = ROOT.RooRealVar( 'atlas_order2_A_all_atlas', "power2", 9 ,     -100,   0)
        atlas_order3_m = ROOT.RooRealVar( 'atlas_order3_A_all_atlas', "power3", 1 ,       -100,    0)
        atlas_order4_e = ROOT.RooRealVar( 'atlas_order4_A_all_atlas', "power4", 1 ,       -100,    100)
        atlas_order4_m = ROOT.RooRealVar( 'atlas_order4_A_all_atlas', "power4", 1 ,       -100,    100)


        integral_atl_e = ROOT.RooRealVar('%s_norm' %( 'atlas_elA'+year+'_all_atlas' ),
                            'normalization', ne )
        integral_atl_m = ROOT.RooRealVar('%s_norm' %( 'atlas_muA'+year+'_all_atlas' ),
                            'normalization', nm )

        function = 'TMath::Power( (1-TMath::Power(@0/13000., 1./3)), @1 ) / ( TMath::Power( @0/13000. , @2+ %s ))'
        order_entries = []
        for i in range( 0, 2 ) :
            order_entries.append( '@%d*TMath::Power' %(i+3)+
                                  '(TMath::Log10( @0/13000.),%d)'  %(i+1 ) )
        function = function % (' + '.join( order_entries ))
        #function = 'TMath::Power( (1-TMath::Power(@0/13000., 1./3)), @1 ) / ( TMath::Power( @0/13000. , @2))'
        func_atl_m = ROOT.RooGenericPdf( '%s_%s'%(func_name, 'muA'+year+'_all_atlas'), '%s_%s'%(func_name, 'muA'+year+'_all_atlas'), function, ROOT.RooArgList(mt_res, atlas_order1_m, atlas_order2_m, atlas_order3_m,atlas_order4_m))
        func_atl_e = ROOT.RooGenericPdf( '%s_%s'%(func_name, 'elA'+year+'_all_atlas'), '%s_%s'%(func_name, 'elA'+year+'_all_atlas'), function, ROOT.RooArgList(mt_res, atlas_order1_e, atlas_order2_e, atlas_order3_e,atlas_order4_e))
        resu_atl_e = func_atl_e.fitTo(dse,ROOT.RooFit.Save(),ROOT.RooFit.SumW2Error(ROOT.kTRUE))
        resu_atl_m = func_atl_m.fitTo(dsm,ROOT.RooFit.Save(),ROOT.RooFit.SumW2Error(ROOT.kTRUE))

        frame_e = mt_res.frame(ROOT.RooFit.Title("Unbinned ML fit, el"))
        frame_m = mt_res.frame(ROOT.RooFit.Title("Unbinned ML fit, mu"))
        dse.plotOn(frame_e,ROOT.RooFit.DataError(ROOT.RooAbsData.SumW2))
        dsm.plotOn(frame_m,ROOT.RooFit.DataError(ROOT.RooAbsData.SumW2))
        func_atl_m.plotOn(frame_m, ROOT.RooFit.VisualizeError(resu_atl_m, 1),ROOT.RooFit.FillColor(ROOT.kOrange))
        func_atl_e.plotOn(frame_e, ROOT.RooFit.VisualizeError(resu_atl_e, 1), ROOT.RooFit.FillColor(ROOT.kOrange))
        func_atl_e.plotOn(frame_e)
        func_atl_m.plotOn(frame_m)
        dse.plotOn(frame_e,ROOT.RooFit.DataError(ROOT.RooAbsData.SumW2))
        dsm.plotOn(frame_m,ROOT.RooFit.DataError(ROOT.RooAbsData.SumW2))
        print("===> fit result")
        resu_atl_e.Print()
        print("chi^2 = ", frame_e.chiSquare())
        print("netot:", netot)
        print("===> fit result")
        resu_atl_m.Print()
        print "function: ", function
        print("chi^2 = ", frame_m.chiSquare())
        print("nmtot:", nmtot)
        print(func_atl_e.Print())
        print(func_atl_m.Print())
        import_workspace( ws_out, atlas_order1_e)
        import_workspace( ws_out, atlas_order2_e)
        import_workspace( ws_out, atlas_order1_m)
        import_workspace( ws_out, atlas_order2_m)
        import_workspace( ws_out, atlas_order3_e)
        import_workspace( ws_out, atlas_order3_m)
        import_workspace( ws_out, atlas_order4_e)
        import_workspace( ws_out, atlas_order4_m)
        import_workspace( ws_out, func_atl_e)
        import_workspace( ws_out, func_atl_m)
        import_workspace( ws_out, integral_atl_e )
        import_workspace( ws_out, integral_atl_m )

    #mypdfse = ROOT.RooArgList("store")
    #mypdfse.add(func_vvdi_e)
    #mypdfse.add(func_atl_e)
    #mypdfse.add(func_pdf_e)
    #catIndexe = ROOT.RooCategory('pdf_index_elA'+year,'c')
    #catIndexe.setIndex(1)
    #pdfe = RooMultiPdf('MultiPdf_elA'+year+'_all_MultiPdf',"All Pdfs e",catIndexe,mypdfse)
    #import_workspace( ws_out, catIndexe )
    ##import_workspace( ws_out, mypdfse )
    #getattr( ws_out , "import")( pdfe, ROOT.RooFit.RecycleConflictNodes() )

    #mypdfsm = ROOT.RooArgList("store")
    #mypdfsm.add(func_vvdi_m)
    #mypdfsm.add(func_atl_m)
    #mypdfsm.add(func_pdf_m)
    #catIndexm = ROOT.RooCategory('pdf_index_muA'+year,'c')
    #pdfm = RooMultiPdf('MultiPdf_muA'+year+'_all_MultiPdf',"All Pdfs m",catIndexm,mypdfsm)
    #import_workspace( ws_out, catIndexm )
    ##import_workspace( ws_out, mypdfsm )
    #getattr( ws_out , "import")(pdfm, ROOT.RooFit.RecycleConflictNodes() )
    ws_out.writeToFile( rootfilename )
    return 
    #plot
    for ch, frame in zip(["el","mu"],[frame_e, frame_m]):
        c = ROOT.TCanvas("c","c",600,600) ;
        ROOT.gStyle.SetOptStat(0)
        c.SetFillColor(0)
        c.SetBorderMode(0)
        c.SetBorderSize(2)
        c.SetFrameBorderMode(0)
        #------------>Primitives in pad: toppad
        toppad = ROOT.TPad('toppad','toppad',0,0.3 ,1.0,1.0)
        bottompad = ROOT.TPad('bottompad','bottompad',0,0.0,1.0,0.32)
        canvas_margin(c,toppad,bottompad)
        toppad.SetFillStyle(4000)
        toppad.SetFrameFillStyle(1000)
        toppad.SetFrameFillColor(0)
        toppad.SetFillColor(0)
        toppad.SetBorderMode(0)
        toppad.SetBorderSize(2)
        toppad.SetLogy()
        toppad.SetFrameBorderMode(0)
        toppad.SetFrameBorderMode(0)
        toppad.SetLeftMargin(0.15)
        bottompad.SetFillStyle(4000)
        bottompad.SetFrameFillStyle(1000)
        bottompad.SetFrameFillColor(0)
        bottompad.SetFillColor(0)
        bottompad.SetBorderMode(0)
        bottompad.SetBorderSize(2)
        bottompad.SetFrameBorderMode(0)
        bottompad.SetFrameBorderMode(0)
        toppad.Draw()
        bottompad.Draw()

        c.cd()
        c.Update()
        c.RedrawAxis()
        cframe = c.GetFrame()
        cframe.Draw()
        toppad.cd()
        frame_4fa51a0__1 = ROOT.TH1D("frame_4fa51a0__1","Unbinned ML fit, %s %s"%(ch,year),100,200,MAX_)
        frame_4fa51a0__1.GetXaxis().SetTitle("mt_res");
        frame_4fa51a0__1.GetXaxis().SetLabelFont(42);
        frame_4fa51a0__1.GetXaxis().SetLabelSize(0.05);
        frame_4fa51a0__1.GetXaxis().SetTitleSize(0.05);
        frame_4fa51a0__1.GetXaxis().SetTitleOffset(1);
        frame_4fa51a0__1.GetXaxis().SetTitleFont(42);
        frame_4fa51a0__1.GetYaxis().SetTitle("Events / ( 18 )");
        frame_4fa51a0__1.GetYaxis().SetLabelFont(42);
        frame_4fa51a0__1.GetYaxis().SetLabelSize(0.05);
        frame_4fa51a0__1.GetYaxis().SetTitleSize(0.05);
        frame_4fa51a0__1.GetYaxis().SetTitleFont(42);
        frame_4fa51a0__1.GetYaxis().SetRangeUser(0.1,1e3)
        frame_4fa51a0__1.GetXaxis().SetLabelOffset(999)
        frame_4fa51a0__1.GetXaxis().SetLabelSize(0)
        frame_4fa51a0__1.Draw("AXISSAME");
        frame.Draw("same")

        hpull = frame.pullHist()
        frame3 = mt_res.frame(ROOT.RooFit.Title("Pull Distribution"))
        frame3.addPlotable(hpull, "P")

        leg = ROOT.TLegend(0.55,0.6,0.95,0.85);
        leg.SetBorderSize(0);
        leg.SetLineStyle(1);
        leg.SetLineWidth(1);
        entry=leg.AddEntry(frame,"data","lp");
        entry.SetFillStyle(1001);
        entry.SetMarkerStyle(8);
        entry.SetMarkerSize(1.5);
        entry.SetLineStyle(1);
        entry.SetLineWidth(2);
        entry.SetTextFont(42);
        entry.SetTextSize(0.06);
        entry=leg.AddEntry("","Fit","l");
        entry.SetFillStyle(1001);
        entry.SetLineStyle(1);
        entry.SetLineWidth(2);
        entry.SetLineColor(ROOT.kBlue);
        entry.SetMarkerStyle(20);
        entry.SetTextFont(42);
        entry.SetTextSize(0.06);
        htmp=ROOT.TH1F("htmp","htmp",10,0,1)
        htmp.SetFillColor(ROOT.kGreen)
        entry=leg.AddEntry(htmp,"1-sigma error band","f");
        entry.SetFillStyle(1001);
        entry.SetLineStyle(1);
        entry.SetLineWidth(2);
        entry.SetMarkerStyle(20);
        entry.SetTextFont(42);
        entry.SetTextSize(0.06);
        leg.Draw()

        bottompad.cd()
        frame_4fa51a0__2 = ROOT.TH1D("frame_4fa51a0__2","",100,200,MAX_)
        frame_4fa51a0__2.GetXaxis().SetTitle("mt_res [GeV]");
        frame_4fa51a0__2.GetXaxis().SetLabelFont(42);
        frame_4fa51a0__2.GetXaxis().SetLabelSize(0.1);
        frame_4fa51a0__2.GetXaxis().SetTitleSize(0.1);
        frame_4fa51a0__2.GetXaxis().SetTitleOffset(1);
        frame_4fa51a0__2.GetXaxis().SetTitleFont(42);
        frame_4fa51a0__2.GetYaxis().SetTitle("Pull");
        frame_4fa51a0__2.GetYaxis().SetLabelFont(42);
        frame_4fa51a0__2.GetYaxis().SetLabelSize(0.15);
        frame_4fa51a0__2.GetYaxis().SetTitleSize(0.15);
        frame_4fa51a0__2.GetYaxis().SetTitleFont(42);
        frame_4fa51a0__2.GetYaxis().SetNdivisions(4)
        frame_4fa51a0__2.GetYaxis().SetRangeUser(-3,3)
        frame_4fa51a0__2.GetYaxis().SetTitleOffset(0.4)
        frame_4fa51a0__2.Draw("AXISSAME");
        frame3.Draw("same")
        #input()
        c.SaveAs('fit_%s%s.png' %( year,ch))
        c.SaveAs('%s/%s/%s.C' %( data_outDir,year,ch))
        #c.SaveAs('%s/%s/%s.root' %( data_outDir,year,ch))
        #c.SaveAs('%s/%s/%s.png' %( data_outDir,year,ch))

def pltToyFit():#toyfile,f1file, f2file):
    #filen = 'higgs_expow2dijet_r1'
    filen = 'higgs_atlas2dijet_r10'
    mass='300'
    Ftoy=ROOT.TFile("data/"+filen+"/Width5/el2016/Mass"+mass+"/higgsCombine.Test.GenerateOnly.mH125.123456.root")
    toy=Ftoy.Get('toys/toy_1')
    toy.Print()
    #ROOT.gSystem.Load('My_double_CB/RooDoubleCB_cc.so')
    #dijet
    Ff1 = ROOT.TFile("data/"+filen+"/Width5/el2016/Mass"+mass+"/inital_fit.root")
    #Ff1 = ROOT.TFile("data/"+filen+"/Width5/el2016/Mass"+mass+"/higgsCombine.Test.MultiDimFit.mH125.root")
    ws1 = Ff1.Get('w')
    Ff2 = ROOT.TFile("data/"+filen+"/Width5/el2016/Mass"+mass+"/higgsCombine.Test.MultiDimFit.mH125.123456.root")
    ws2 = Ff2.Get('w')
    ws2.loadSnapshot("MultiDimFit")
    #ws2.loadSnapshot("toyGenSnapshot")

    #ws1.Print()
    func_pdf_e1 = ws1.pdf("shapeBkg_All_el2016")
    func_pdf_e2 = ws2.pdf("shapeBkg_All_el2016")
    func_sig_e = ws2.pdf("shapeSig_Resonance_el2016")
    components = ROOT.RooArgList(func_sig_e,func_pdf_e2)
    bkg_norm1 = ws1.var("n_exp_binel2016_proc_All")
    bkg_norm2 = ws2.var("n_exp_binel2016_proc_All")
    sig_norm = ws2.var("shapeSig_Resonance_el2016__norm")
    sig_norm.setVal(sig_norm.getVal()*ws2.var("r").getVal()*536.617)
    #sig_norm.setVal(sig_norm.getVal()*ws2.var("r").getVal()*4121.13)
    #sig_norm.setVal(sig_norm.getVal()*ws2.var("r").getVal()*1891.44)
    coeffs = ROOT.RooArgList(sig_norm,bkg_norm2)
    model = ROOT.RooAddPdf("model","f_{s+b}",components,coeffs);
    #model.Print("v")
    #print(bkg_norm2.getVal(),sig_norm.getVal()*ws2.var("r").getVal()*1891.44)
    mt_res = ws1.var("mt_res")
    frame = mt_res.frame(ROOT.RooFit.Title("toy fit"))
    toy.plotOn(frame,ROOT.RooFit.DataError(ROOT.RooAbsData.SumW2))
    print(toy.sumEntries())
    func_pdf_e1.plotOn(frame,ROOT.RooFit.LineColor(ROOT.kRed), ROOT.RooFit.Normalization(toy.sumEntries(),ROOT.RooAbsReal.NumEvent))
    model.plotOn(frame,ROOT.RooFit.LineColor(ROOT.kOrange), ROOT.RooFit.Normalization(toy.sumEntries(),ROOT.RooAbsReal.NumEvent))
    #func_pdf_e.plotOn(frame,ROOT.RooFit.FillColor(ROOT.kRed), ROOT.RooFit.Normalization(bkg_norm.getVal(), ROOT.RooAbsReal.NumEvent))
#Norm(ROOT.RooAbsReal.NumEvent,bkg_norm.getVal()))
    #func_sig_e.plotOn(frame,ROOT.RooFit.FillColor(ROOT.kOrange),Norm(ROOT.RooAbsReal.NumEvent,sig_norm.getVal()))
    #toy.plotOn(frame,ROOT.RooFit.DataError(ROOT.RooAbsData.SumW2))
    #frame.Draw()
    #input()


    c = ROOT.TCanvas("c","c",600,600) ;
    ROOT.gStyle.SetOptStat(0)
    c.SetFillColor(0)
    c.SetBorderMode(0)
    c.SetBorderSize(2)
    c.SetFrameBorderMode(0)
    #------------>Primitives in pad: toppad
    toppad = ROOT.TPad('toppad','toppad',0,0.3 ,1.0,1.0)
    bottompad = ROOT.TPad('bottompad','bottompad',0,0.0,1.0,0.32)
    canvas_margin(c,toppad,bottompad)
    toppad.SetFillStyle(4000)
    toppad.SetFrameFillStyle(1000)
    toppad.SetFrameFillColor(0)
    toppad.SetFillColor(0)
    toppad.SetBorderMode(0)
    toppad.SetBorderSize(2)
    toppad.SetLogy()
    toppad.SetFrameBorderMode(0)
    toppad.SetFrameBorderMode(0)
    toppad.SetLeftMargin(0.15)
    bottompad.SetFillStyle(4000)
    bottompad.SetFrameFillStyle(1000)
    bottompad.SetFrameFillColor(0)
    bottompad.SetFillColor(0)
    bottompad.SetBorderMode(0)
    bottompad.SetBorderSize(2)
    bottompad.SetFrameBorderMode(0)
    bottompad.SetFrameBorderMode(0)
    toppad.Draw()
    bottompad.Draw()

    c.cd()
    c.Update()
    c.RedrawAxis()
    cframe = c.GetFrame()
    cframe.Draw()
    toppad.cd()
    frame_4fa51a0__1 = ROOT.TH1D("frame_4fa51a0__1","Unbinned ML fit, %s %s"%(ch,year),100,200,2000)
    frame_4fa51a0__1.GetXaxis().SetTitle("mt_res");
    frame_4fa51a0__1.GetXaxis().SetLabelFont(42);
    frame_4fa51a0__1.GetXaxis().SetLabelSize(0.05);
    frame_4fa51a0__1.GetXaxis().SetTitleSize(0.05);
    frame_4fa51a0__1.GetXaxis().SetTitleOffset(1);
    frame_4fa51a0__1.GetXaxis().SetTitleFont(42);
    frame_4fa51a0__1.GetYaxis().SetTitle("Events / ( 18 )");
    frame_4fa51a0__1.GetYaxis().SetLabelFont(42);
    frame_4fa51a0__1.GetYaxis().SetLabelSize(0.05);
    frame_4fa51a0__1.GetYaxis().SetTitleSize(0.05);
    frame_4fa51a0__1.GetYaxis().SetTitleFont(42);
    frame_4fa51a0__1.GetYaxis().SetRangeUser(0.1,1e3)
    frame_4fa51a0__1.GetXaxis().SetLabelOffset(999)
    frame_4fa51a0__1.GetXaxis().SetLabelSize(0)
    frame_4fa51a0__1.Draw("AXISSAME");
    frame.Draw("same")

    hpull = frame.pullHist()
    frame3 = mt_res.frame(ROOT.RooFit.Title("Pull Distribution"))
    frame3.addPlotable(hpull, "P")

    leg = ROOT.TLegend(0.55,0.6,0.95,0.85);
    leg.SetBorderSize(0);
    leg.SetLineStyle(1);
    leg.SetLineWidth(1);
    entry=leg.AddEntry(frame,"toy data","lp");
    entry.SetFillStyle(1001);
    entry.SetMarkerStyle(8);
    entry.SetMarkerSize(1.5);
    entry.SetLineStyle(1);
    entry.SetLineWidth(2);
    entry.SetTextFont(42);
    entry.SetTextSize(0.06);
    entry=leg.AddEntry("","initial bkg Func","l");
    entry.SetFillStyle(1001);
    entry.SetLineStyle(1);
    entry.SetLineWidth(2);
    entry.SetLineColor(ROOT.kRed);
    entry.SetMarkerStyle(20);
    entry.SetTextFont(42);
    entry.SetTextSize(0.06);
    entry=leg.AddEntry("","final bkg+signal fit","l");
    entry.SetFillStyle(1001);
    entry.SetLineStyle(1);
    entry.SetLineWidth(2);
    entry.SetMarkerStyle(20);
    entry.SetLineColor(ROOT.kOrange);
    entry.SetTextFont(42);
    entry.SetTextSize(0.06);
    leg.Draw()
    
    bottompad.cd()
    frame_4fa51a0__2 = ROOT.TH1D("frame_4fa51a0__2","",100,200,2000)
    frame_4fa51a0__2.GetXaxis().SetTitle("mt_res [GeV]");
    frame_4fa51a0__2.GetXaxis().SetLabelFont(42);
    frame_4fa51a0__2.GetXaxis().SetLabelSize(0.1);
    frame_4fa51a0__2.GetXaxis().SetTitleSize(0.1);
    frame_4fa51a0__2.GetXaxis().SetTitleOffset(1);
    frame_4fa51a0__2.GetXaxis().SetTitleFont(42);
    frame_4fa51a0__2.GetYaxis().SetTitle("Pull");
    frame_4fa51a0__2.GetYaxis().SetLabelFont(42);
    frame_4fa51a0__2.GetYaxis().SetLabelSize(0.15);
    frame_4fa51a0__2.GetYaxis().SetTitleSize(0.15);
    frame_4fa51a0__2.GetYaxis().SetTitleFont(42);
    frame_4fa51a0__2.GetYaxis().SetNdivisions(4)
    frame_4fa51a0__2.GetYaxis().SetRangeUser(-3,3)
    frame_4fa51a0__2.GetYaxis().SetTitleOffset(0.4)
    frame_4fa51a0__2.Draw("AXISSAME");
    frame3.Draw("same")
    input()
    #c.SaveAs('fit_%s%s.png' %( year,ch))
    #c.SaveAs('%s/%s/%s.C' %( data_outDir,year,ch))
    #c.SaveAs('%s/%s/%s.root' %( data_outDir,year,ch))
    #c.SaveAs('%s/%s/%s.png' %( data_outDir,year,ch))


def goodnessOfFit(year,baseDir,skimtree,skimfile):

    rootfilename = '%s/%s/%s.root' %( data_outDir,year,'workspace_all' )
    ifile = ROOT.TFile.Open( rootfilename, 'READ' )
    ws = ifile.Get( 'workspace_all' ) 
    mt_res = ws.var("mt_res")
    datae = ws.data('data_elA'+year+'_mt_res_base')
    datam = ws.data('data_muA'+year+'_mt_res_base')
    pdfe  = ws.pdf('%s_%s'%('dijet','elA'+year+'_all_dijet'))
    pdfm  = ws.pdf('%s_%s'%('dijet','muA'+year+'_all_dijet'))
    nllDatae = pdfe.createNLL(datae)
    nllDatam = pdfm.createNLL(datam)
    print('nllDatae nllDatam',nllDatae.getVal(),nllDatam.getVal())
    ne = ws.var('%s_norm' %( 'dijet_elA'+year+'_all_dijet' )).getVal()
    nm = ws.var('%s_norm' %( 'dijet_muA'+year+'_all_dijet' )).getVal()
    print('ne nm :',ne,nm)
    #pdfMc = ROOT.RooHistPdf("pdf1", "pdf1", x, mcHist, 0);
    #tse = ROOT.TH1D("MC-likelihood-Dist", "MC-likelihood-Dist", 200, 2500, 4500);
    #tsm = ROOT.TH1D("MC-likelihood-Dist", "MC-likelihood-Dist", 200, 2500, 4500);
    #tse = ROOT.TH1D("MC-likelihood-Dist", "MC-likelihood-Dist", 200, 4500, 6000);
    #tsm = ROOT.TH1D("MC-likelihood-Dist", "MC-likelihood-Dist", 200, 4500, 6000);
    tse = ROOT.TH1D("MC-likelihood-Dist", "MC-likelihood-Dist", 200, 7000, 7500);
    tsm = ROOT.TH1D("MC-likelihood-Dist", "MC-likelihood-Dist", 200, 7000, 7500);
    tempNlle = 0
    tempNllm = 0
    for i in range(1,1000):
        toyMCDataGen = pdfe.generate(ROOT.RooArgSet(mt_res),ne)  #generateBinned(mt_res, ne)
        nlle = pdfe.createNLL(toyMCDataGen)
        tempNlle = nlle.getVal()
        if (ROOT.TMath.Finite(tempNlle) == 1):
            tse.Fill(tempNlle)
        toyMCDataGen.Clear()
        toyMCDataGen = pdfm.generate(ROOT.RooArgSet(mt_res),nm)  #generateBinned(mt_res, nm)
        nllm = pdfm.createNLL(toyMCDataGen)
        tempNllm = nllm.getVal()
        if (ROOT.TMath.Finite(tempNllm) == 1):
            tsm.Fill(tempNllm)
        toyMCDataGen.Clear()
        print('tempNlle,tempNllm ',tempNlle,tempNllm)
    tse.Draw("HIST")
    tsm.SetLineColor(ROOT.kRed)
    tsm.Draw("same HIST")
    tse.SaveAs('year'+year+"tse.C")
    tsm.SaveAs('year'+year+"tsm.C")
    print('nllDatae nllDatam',nllDatae.getVal(),nllDatam.getVal())
    input()
   

def CombineGoF(ch, year):
    mass = '300'
    c = ROOT.TCanvas()
    ROOT.gStyle.SetOptStat(0)
    print('=========>',ch,year)
    rootfilename = 'data_env/decideOrderwithdata_GOF3/higgsCombine%s%s_dijet3.GoodnessOfFit.mH120.root'%(ch,year)
    #rootfilename = 'data/higgs/Width5/%s%s/Mass%s/higgsCombine.saturated.GoodnessOfFit.mH120.root' %( ch,year ,mass)
    ifile = ROOT.TFile.Open( rootfilename, 'READ' )
    tree = ifile.Get( 'limit' )
    for e in tree:
        print("=========> ", e.limit)
        datalimit =  e.limit
    #rootfilename = 'data/higgs/Width5/%s%s/Mass%s/higgsCombine.saturated.GoodnessOfFit.mH120.1234.root' %( ch,year ,mass)
    rootfilename = 'data_env/decideOrderwithdata_GOF3/higgsCombine%s%s_dijet3.GoodnessOfFit.mH120.123.root'%(ch,year)
    ifile = ROOT.TFile.Open( rootfilename, 'READ' )
    tree = ifile.Get( 'limit' )
    #tree.Show(0)
    hlimit = ROOT.TH1D("hlimit", "Goodness of Fit (%s %s);limit;"%(ch,year), 60, 0, 0.3);
    tree.Draw("limit>>hlimit")
    hlimit.SetLineColor(ROOT.kRed)
    hlimit.Fit("gaus")
    #ln = ROOT.TLine(datalimit, 0, datalimit, 0.9*hlimit.GetMaximum())
    #ln.SetLineStyle(10)
    #ln.SetLineWidth(3)
    #tot = 0
    #for i in range(1,hlimit.GetNbinsX()):
    #    if hlimit.GetBinCenter(i)<=datalimit:
    #        tot+=hlimit.GetBinContent(i)
    #    else:
    #        break
    #print(1-tot/500.0)
    #hlimit.Draw("HIST")
    #ln.Draw("same")
    return
    leg = ROOT.TLegend(0.11,0.6,0.3,0.85);
    leg.SetBorderSize(0);
    leg.SetLineStyle(1);
    leg.SetLineWidth(1);
    entry=leg.AddEntry("hlimit","toy-data","l");
    entry.SetFillStyle(1001);
    entry.SetLineStyle(1);
    entry.SetLineWidth(3);
    entry.SetTextFont(42);
    entry.SetTextSize(0.1);
    entry=leg.AddEntry("ln","Data","l");
    entry.SetFillStyle(1001);
    entry.SetLineStyle(10);
    entry.SetLineWidth(3);
    entry.SetMarkerStyle(20);
    entry.SetTextFont(42);
    entry.SetTextSize(0.1);
    entry=leg.AddEntry("","P=%0.2f"%(1-tot/500.0),"l");
    entry.SetFillStyle(1001);
    entry.SetLineStyle(1);
    entry.SetLineWidth(0);
    entry.SetMarkerStyle(20);
    entry.SetTextFont(42);
    entry.SetTextSize(0.1);
    leg.Draw()
    input()
    c.SaveAs('year'+ch+year+"_Mass"+mass+"_hlimit.C")
    c.SaveAs('year'+ch+year+"_Mass"+mass+"_hlimit.png")


def testBias():

    hbias = {}
    ifile = {}
    rsignalr = [ '0.1']
    #leg1 = 'dijet -> vvdijet'
    #leg1 = 'dijet -> vvdijet'
    #leg1 = 'expow -> envelope'
    leg1 = 'expow -> envelope'
    #leg1 = 'vvdijet -> envelope'
    mean_collection = {}
    sigma_collection = {}
    mean_collection_e = {}
    sigma_collection_e = {}
    masslist    = [300, 350, 400,450, 600, 700, 800,900, 1000, 1200, 1400, 1600, 1800, 2000]
    #masslist    = [300, 600, 900, 1200, 1600, 2000]
    widlist = ['5','0p01']
    colorb = [ROOT.kRed,ROOT.kBlue,ROOT.kGreen,ROOT.kCyan,ROOT.kOrange,ROOT.kPink,ROOT.kGray]
    for wid in widlist:
        for im in masslist:
            for ir in rsignalr:
                c = ROOT.TCanvas("basecan", "basecan",0,0,800,750)
                ROOT.gStyle.SetOptStat(0)
                c.SetHighLightColor(2);
                c.Range(0,0.2,1,1);
                c.SetFillColor(0);
                c.SetBorderMode(0);
                c.SetBorderSize(2);
                c.SetFrameBorderMode(0);
                c.SetBottomMargin(0.2);

                #filename = 'data_env/higgs_1112_o2_toydata__expow2envelop_biastest'
                tree = ROOT.TChain("tree_fit_sb")
                tree.Add('data_env/test_bias_Dec17_expow_multi_r1//Width%s/all/Mass%s/fitDiagnostics*.root'%(wid,str(im)))
                #tree.Add('data_env/test_bias_Dec16_expow_multi_r1//Width%s/all/Mass%s/fitDiagnostics*.root'%(wid,str(im)))
                #tree.Add('data_env/test_bias_Dec17_dijet_vvdijet_r1//Width%s/all/Mass%s/fitDiagnostics*.root'%(wid,str(im)))
                #tree.Add('data_env/test_bias_Dec17_dijet_vvdijet_r1//Width%s/all/Mass%s/fitDiagnostics*.root'%(wid,str(im)))
                #tree.Add('data_env/test_bias_Dec16_vvdijet_dijet_r1//Width%s/all/Mass%s/fitDiagnostics*.root'%(wid,str(im)))
                #tree.Add('data_env/test_bias_Dec16_dijet_vvdijet_r1//Width%s/all/Mass%s/fitDiagnostics*.root'%(wid,str(im)))
                if wid=='0p01':
                    hlimit = ROOT.TH1D("hlimit", "Bias Study (#Gamma_{X}/m_{X}=0.01%, m_{X}="+str(im)+"GeV);(r - r_{inject})/#sigma_{r};", 60, -5,5);
                else:
                    hlimit = ROOT.TH1D("hlimit", "Bias Study (#Gamma_{X}/m_{X}="+wid+"%, m_{X}="+str(im)+"GeV);(r - r_{inject})/#sigma_{r};", 60, -5,5);
                tree.Draw("(r-%s)*2/(rLoErr+rHiErr)>>hlimit"%(ir),"fit_status>0 && rLoErr<9")
                hlimit.SetLineColor(ROOT.kRed)
                hlimit.GetXaxis().SetLabelFont(42)
                hlimit.GetXaxis().SetLabelSize(0.05)
                hlimit.GetXaxis().SetTitleSize(0.05)
                hlimit.GetXaxis().SetTitleFont(42)
                hlimit.GetXaxis().SetTitleOffset(1)
                func = ROOT.TF1("func","gaus",hlimit.GetMean()-2*hlimit.GetRMS(),hlimit.GetMean()+2*hlimit.GetRMS())
                hlimit.Fit(func,"R")
                hlimit.GetYaxis().SetRangeUser(0,2*hlimit.GetMaximum())
                #hbias['r'+ir+'W'+wid+'m'+str(im)] = ROOT.TH1D('r'+ir+'W'+wid+'m'+str(im), "Bias Study (Width=%s Mass%s);(r-r_{inject})/#sigma_{r};"%(wid,str(im)),100,-5,5)
                #htemplate= ROOT.TH1D('htemplate', "Bias Study (Width=%s Mass%s);r;"%(wid,str(im)),100,-5,5)
                #tree.Draw("(r-"+str(rsignal[ir][0])+")/"+str(func.GetParameter(2))+">>htemplate")
                #nbins = htemplate.GetNbinsX()
                #xlow = htemplate.GetBinLowEdge(1)
                #xup = htemplate.GetBinLowEdge(nbins + 1)
                #print('r'+ir+'W'+wid+'m'+str(im))
                #for bin in range(nbins+1):
                #    hbias['r'+ir+'W'+wid+'m'+str(im)].SetBinContent(bin, htemplate.GetBinContent(bin) )
                #    hbias['r'+ir+'W'+wid+'m'+str(im)].SetBinError(bin, htemplate.GetBinError(bin) )
                #hbias['r'+ir+'W'+wid+'m'+str(im)].Draw("hist")
                #hbias['r'+ir+'W'+wid+'m'+str(im)].GetYaxis().SetRangeUser(0,2*hbias['r'+ir+'W'+wid+'m'+str(im)].GetMaximum())
                #hbias['r'+ir+'W'+wid+'m'+str(im)].SetLineColor(ROOT.kRed)
                #func = ROOT.TF1("func","gaus",hbias['r'+ir+'W'+wid+'m'+str(im)].GetMean()-2*hbias['r'+ir+'W'+wid+'m'+str(im)].GetRMS(),hbias['r'+ir+'W'+wid+'m'+str(im)].GetMean()+2*hbias['r'+ir+'W'+wid+'m'+str(im)].GetRMS())
                #htemplate.Fit(func,"R")
                #hbias['r'+ir+'W'+wid+'m'+str(im)].Draw("hist")
                #func.Draw("same")
                sigma_collection['r'+ir+'W'+wid+'m'+str(im)]= func.GetParameter(2)
                mean_collection['r'+ir+'W'+wid+'m'+str(im)]= func.GetParameter(1)
                sigma_collection_e['r'+ir+'W'+wid+'m'+str(im)]= func.GetParError(2)
                mean_collection_e['r'+ir+'W'+wid+'m'+str(im)]= func.GetParError(1)
                leg = ROOT.TLegend(0.15,0.6,0.35,0.85);
                leg.SetBorderSize(0);
                leg.SetLineStyle(1);
                leg.SetLineWidth(2);
                entry=leg.AddEntry("",leg1,"l");
                entry.SetFillStyle(1001);
                entry.SetLineStyle(1);
                entry.SetLineWidth(0);
                entry.SetTextFont(42);
                entry.SetTextSize(0.08);
                entry=leg.AddEntry("","Mean=%0.2f +/- %0.2f"%(func.GetParameter(1), func.GetParError(1)),"l");
                entry.SetFillStyle(1001);
                entry.SetLineStyle(1);
                entry.SetLineWidth(0);
                entry.SetMarkerStyle(20);
                entry.SetTextFont(42);
                entry.SetTextSize(0.08);
                entry=leg.AddEntry("","#sigma=%0.2f +/- %0.2f "%(func.GetParameter(2), func.GetParError(2)),"l");
                entry.SetFillStyle(1001);
                entry.SetLineStyle(1);
                entry.SetLineWidth(0);
                entry.SetMarkerStyle(20);
                entry.SetTextFont(42);
                entry.SetTextSize(0.08);
                leg.Draw()
                irr='1'
                c.SaveAs('gr_bias_Width'+wid+'_Mass'+str(im)+'_r'+irr+".C")
                c.SaveAs('gr_bias_Width'+wid+'_Mass'+str(im)+'_r'+irr+".png")
                #input('wait')
    cc = ROOT.TCanvas()
    ROOT.gStyle.SetOptStat(0)
    leg = ROOT.TLegend(0.21,0.6,0.35,0.85);
    leg.SetBorderSize(0);
    leg.SetLineStyle(1);
    leg.SetLineWidth(2);
    i=1

    for wid in widlist:
        for im in masslist:
            for ir in rsignalr:
                print(mean_collection['r'+ir+'W'+wid+'m'+str(im)])
    print('-')    
    for wid in widlist:
        for im in masslist:
            for ir in rsignalr:
                print(mean_collection_e['r'+ir+'W'+wid+'m'+str(im)])

    print('-')
    for wid in widlist:
        for im in masslist:
            for ir in rsignalr:
                print(sigma_collection['r'+ir+'W'+wid+'m'+str(im)])
    print('-')
    for wid in widlist:
        for im in masslist:
            for ir in rsignalr:
                print(sigma_collection_e['r'+ir+'W'+wid+'m'+str(im)])
    #for wid in widlist:
    #    for im in masslist:
            #print('wid ',wid, ' im ', im)
    #        for ir in rsignalr:
                #print('mean: r'+ir+'W'+wid+'m'+str(im), mean_collection['r'+ir+'W'+wid+'m'+str(im)])
    #            print('mean error: r'+ir+'W'+wid+'m'+str(im), mean_collection_e['r'+ir+'W'+wid+'m'+str(im)])
                #print('sigma: r'+ir+'W'+wid+'m'+str(im), sigma_collection['r'+ir+'W'+wid+'m'+str(im)])
                #print('sigma error: r'+ir+'W'+wid+'m'+str(im), sigma_collection_e['r'+ir+'W'+wid+'m'+str(im)])
    #            i=i+1
    #            hbias['r'+ir+'W'+wid+'m'+str(im)].SetName('r'+ir+'W'+wid+'m'+str(im))
    #            hbias['r'+ir+'W'+wid+'m'+str(im)].SetTitle('r'+ir+'W'+wid+'m'+str(im))
    #            hbias['r'+ir+'W'+wid+'m'+str(im)].Draw("same e")
    #            hbias['r'+ir+'W'+wid+'m'+str(im)].SetLineColor(i)
    #            entry=leg.AddEntry('r'+ir+'W'+wid+'m'+str(im),'r='+ir+' Wid'+wid+'_Mass'+str(im),"l");
    #            entry.SetFillStyle(1001);
    #            entry.SetLineStyle(1);
    #            entry.SetLineWidth(3);
    #            entry.SetTextFont(42);
    #            entry.SetTextSize(0.04);
    #            i=i+1
    #leg.Draw()
    #cc.SaveAs('gr_all_bias.C')
    #cc.SaveAs('gr_all_bias.png')

def checkenv():

    masslist = ['300','350','400','450','600','800','1000','1200','1400','1600','1800','2000']
    for mass in masslist:
        inputfile = 'data_env/higgs_1112_o2_toydata_envelop/Width5/all/Mass'+mass+'/'
        #inputfile = 'data_env/higgs_o2_env_4funcs_differentParams_correcto2/Width5/all/Mass400/'
        #f_all=ROOT.TFile(inputfile+"higgsCombinefixed_pdf_0.MultiDimFit.mH"+mass+".root")
        f_all=ROOT.TFile(inputfile+"higgsCombineEnvelope.MultiDimFit.mH"+mass+".root")
        t_all=f_all.Get("limit")
        ymin = 202000
        ymax = 204000
        h_all=ROOT.TH2F("h_all","envelope",50,-1,5,2000,ymin, ymax)
        t_all.Draw("2*(deltaNLL+nll+nll0):r>>h_all")
        hp_all = h_all.ProfileX()
        ymin_=hp_all.GetMinimum()
        ymax_=hp_all.GetMaximum()
        if ymin_==0: ymin_ = ymax_
        hp={}
        h={}
        f={}
        t={}
        colorbar=[1,2,3,4,6,7,8,9]
        comb=['0','1','2','111000']#'011000','101000','110000','111000','100000','010000','001000']
        tt=['dijet_2','vvdijet_2','expow_2','best_fit']#'011000','101000','110000','111000','100000','010000','001000']
        for i in range(len(comb)):
            f[i]=ROOT.TFile(inputfile+"higgsCombinefixed_pdf_"+str(comb[i])+".MultiDimFit.mH"+mass+".root")
            t[i]=f[i].Get("limit")
            h[i]=ROOT.TH2F("h"+str(i),"",500,-1,5,2000,ymin, ymax)
            t[i].Draw("2*(deltaNLL+nll+nll0):r>>h"+str(i))
            hp[i] = h[i].ProfileX()
            for j in range(hp[i].GetNbinsX()):
                binc = hp[i].GetBinContent(j)
                if ymin_>binc and binc>0: ymin_=binc
                if ymax_<binc and binc>0: ymax_=binc
        if ymin_==0:
            ymin_ = ymax_-50


        #make plots
        c=ROOT.TCanvas()
        c.SetFillColor(0)
        c.SetBorderMode(0)
        ROOT.gStyle.SetOptStat(0)
        c.SetLeftMargin(0.2)
        c.SetBorderSize(2)
        c.SetFrameBorderMode(0)
        frame_4fa51a0__1 = ROOT.TH1D("frame_4fa51a0__1","",500,-1,5)
        frame_4fa51a0__1.GetXaxis().SetTitle("signal strength")
        frame_4fa51a0__1.GetXaxis().SetTitleSize(0.05)
        frame_4fa51a0__1.GetXaxis().SetTitleOffset(0.8)
        frame_4fa51a0__1.GetXaxis().SetTitleFont(42)
        frame_4fa51a0__1.GetYaxis().SetTitle("-2#Delta Log(L)")
        frame_4fa51a0__1.GetYaxis().SetLabelFont(42)
        frame_4fa51a0__1.GetYaxis().SetLabelSize(0.05)
        frame_4fa51a0__1.GetYaxis().SetTitleSize(0.05)
        frame_4fa51a0__1.GetYaxis().SetTitleFont(42)
        frame_4fa51a0__1.GetYaxis().SetRangeUser(ymin_-(ymax_-ymin_)*0.1,ymax_+(ymax_-ymin_)*0.5)
        frame_4fa51a0__1.Draw("AXISSAME")
        ROOT.gStyle.SetOptStat(0)
        leg = ROOT.TLegend(0.3,0.4,0.45,0.8)
        leg.SetBorderSize(0)
        leg.SetLineStyle(1)
        leg.SetLineWidth(1)
        for i in range(len(comb)):
            hp[i].SetTitle(tt[i])
            hp[i].SetMarkerStyle(20)
            hp[i].SetMarkerColor(colorbar[i+1])
            hp[i].SetLineColor(colorbar[i+1])
            hp[i].Draw("same p")
            hp[i].GetXaxis().SetTitle("r")
            hp[i].GetYaxis().SetTitle("-2#Delta Log(L)")
            hp[i].SetTitle(tt[i])
            hp[i].SetName(tt[i])
            entry=leg.AddEntry(tt[i],tt[i] ,"p")
            entry.SetFillStyle(1001)
            entry.SetMarkerStyle(8)
            entry.SetMarkerSize(1.5)
            entry.SetLineStyle(1)
            entry.SetLineWidth(3)
            entry.SetTextFont(42)
            entry.SetTextSize(0.06)

        hp_all.SetMarkerColor(colorbar[0])
        hp_all.SetMarkerStyle(24)
        hp_all.Draw("same p")
        hp_all.GetXaxis().SetTitle("r")
        hp_all.GetYaxis().SetTitle("-2#Delta Log(L)")
        hp_all.SetTitle("envelope")
        hp_all.SetName("envelope")
        entry=leg.AddEntry("envelope","envelope" ,"p")
        entry.SetFillStyle(1001)
        entry.SetMarkerStyle(8)
        entry.SetMarkerSize(1.5)
        entry.SetLineStyle(1)
        entry.SetLineWidth(3)
        entry.SetTextFont(42)
        entry.SetTextSize(0.06)
        leg.Draw()
        te = ROOT.TLatex(0.3,0.87,"M"+str(mass))
        te.SetNDC()
        te.SetTextAlign(13)
        te.SetTextSize(0.06)
        te.SetLineWidth(2)
        te.Draw()
        tex = ROOT.TLatex(0.3,0.95,"CMS")
        tex.SetNDC()
        tex.SetTextAlign(13)
        tex.SetTextSize(0.048)
        tex.SetLineWidth(2)
        tex.Draw()
        tex1 = ROOT.TLatex(0.37,0.95,"Simulation Work in Progress")
        tex1.SetNDC()
        tex1.SetTextAlign(13)
        tex1.SetTextFont(52)
        tex1.SetTextSize(0.03648)
        tex1.SetLineWidth(2)
        tex1.Draw()
        c.SaveAs("env"+mass+'.C')
        c.SaveAs("env"+mass+'.pdf')
        c.SaveAs("env"+mass+'.png')
        #input('wait...')

skimtree   =  "outputTree"
skimfile     =  "skim_1in5.root"
skimfile     =  "skim.root"

#testBias()

#ShowSignalInjection()
#makeFinalplots(data_outDir,skimtree)
#exit()

for year in ['2016','2017','2018']:
#for year in ['2018']:
    #goodnessOfFit(year,data_outDir,skimtree,skimfile)
    #prepareWS(year,data_outDir,skimtree,skimfile) # Old, do not use
    makeRooMultiPdfWorkspace(year,data_outDir,skimtree,skimfile)
    #for ch in ['el','mu']:
    #    CombineGoF(ch, year)
        #prepare_data(5, year, ch, skimtree, data_outDir+'/'+ch+year+'_'+skimfile)

#testBias()
#pltToyFit()
#checkenv()

