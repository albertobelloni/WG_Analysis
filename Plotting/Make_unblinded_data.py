import ROOT
from array import array
#execfile("MakeBase.py")
from ROOT import gSystem
gSystem.Load('../../../combine/CMSSW_11_0_0/lib/slc7_amd64_gcc820/libHiggsAnalysisCombinedLimit.so')
import numpy as np
from ROOT import RooMultiPdf

MIN_ = 230
MAX_ = 2300
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
            FileMap[year+ch] = glob.glob('/data/users/mseidel/Resonances'+year+'/LepGamma_elg_'+Date+'/WithSF/SingleElectron/Job*/tree.root')
            FileMap[year+'ph'] = glob.glob('/data/users/mseidel/Resonances'+year+'/LepGamma_elg_'+Date+'/WithSF/SinglePhotonHltOlap/Job*/tree.root')
            if(year=='2018'): FileMap[year+ch] = glob.glob('/data/users/mseidel/Resonances'+year+'/LepGamma_elg_'+Date+'/WithSF/EGamma/Job*/tree.root')
        if ch == 'mu':
            FileMap[year+ch] = glob.glob('/data/users/mseidel/Resonances'+year+'/LepGamma_mug_'+Date+'/WithSF/SingleMuon/Job*/tree.root')
            
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
    if ch=='el': 
        for n in FileMap[year+'ph']: names.push_back(n)
    d = ROOT.RDataFrame(treeIn, names)
    selection , weight = defs.makeselstring('el',  80, 35,  40,year)
    if ch=='mu':
        selection , weight = defs.makeselstring('mu',  80, 30,  40,year)
    myfilter = d.Filter(selection).Range(1,0,frac)
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



def fit_range(mass):
    return (max( mass * 0.97*0.6, 100), min( mass *0.97*1.4,2500))

def makeFinalplots(baseDir,skimtree):

    #Reading Data, merge 3 years
    year ='2016'
    MIN_=230
    MAX_=2330
    NBIN_=105
    mt_res = ROOT.RooRealVar("mt_res", "mt_res", MIN_, MAX_)
    mt_res.setBins(NBIN_) 
    #mt_res.setRange( MIN_ ,MAX_)
    print('get ', skimtree, ' from ',baseDir+'/el'+year+'_'+skimfile)
    F=ROOT.TFile(baseDir+'/el'+year+'_'+skimfile)
    tree=F.Get(skimtree)
    netot = tree.GetEntries()
    dse = ROOT.RooDataSet('data_elA'+year+'_mt_res_base', "dse", ROOT.RooArgSet(mt_res), ROOT.RooFit.Import(tree))

    print('get ', skimtree, ' from ',baseDir+'/mu'+year+'_'+skimfile)
    F=ROOT.TFile(baseDir+'/mu'+year+'_'+skimfile)
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

    # First we fit the pdfs to the data, so we reasonable initial values for parameters
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
    # Create MultiPDF containing dijet, vvdijet, expow
    multipdfe = RooMultiPdf('MultiPdf_elA'+year+'_all_MultiPdf',"All Pdfs e",catIndexe, mypdfse)
    norm_MultiPdf_e = ROOT.RooRealVar('%s_norm' %( 'MultiPdf_elA'+year+'_all_MultiPdf' ),'normalization_e', ne,0,1000000 )
    multipdfm = RooMultiPdf('MultiPdf_muA'+year+'_all_MultiPdf',"All Pdfs m",catIndexm, mypdfsm)
    norm_MultiPdf_m = ROOT.RooRealVar('%s_norm' %( 'MultiPdf_muA'+year+'_all_MultiPdf' ),'normalization_m', nm,0,1000000 )

    singlefunc=False
    if singlefunc:
        #Generate toy with a specific function
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
        # Get chiSquare use data from Workspace
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
        # generate toydata with the best bkg function
        rseed = ROOT.RooRandom.randomGenerator()
        rseed.SetSeed(321)
        toydatae = multipdfse[np.argmin(np.abs(chi2score_e))].generate(ROOT.RooArgSet(mt_res),ne)
        toydatam = multipdfsm[np.argmin(np.abs(chi2score_m))].generate(ROOT.RooArgSet(mt_res),nm)
        catIndexe.setIndex(np.argmin(np.abs(chi2score_e)))
        catIndexm.setIndex(np.argmin(np.abs(chi2score_m)))
        toydatae.SetName ('data_elA'+year+'_mt_res_base')
        toydatam.SetName ('data_muA'+year+'_mt_res_base')

    frame_e = mt_res.frame(ROOT.RooFit.Title("Unbinned ML fit, el"))
    frame_m = mt_res.frame(ROOT.RooFit.Title("Unbinned ML fit, mu"))
    # plot fit line and error band
    dse.plotOn(frame_e,ROOT.RooFit.DataError(ROOT.RooAbsData.Poisson))
    dsm.plotOn(frame_m,ROOT.RooFit.DataError(ROOT.RooAbsData.Poisson))
    minimpdf=False
    if minimpdf:
        multipdfse[np.argmin(np.abs(chi2score_e))].plotOn(frame_e, ROOT.RooFit.VisualizeError(multiresultse[np.argmin(np.abs(chi2score_e))], 2), ROOT.RooFit.FillColor(ROOT.kYellow))
        multipdfsm[np.argmin(np.abs(chi2score_m))].plotOn(frame_m, ROOT.RooFit.VisualizeError(multiresultsm[np.argmin(np.abs(chi2score_m))], 2), ROOT.RooFit.FillColor(ROOT.kYellow))
        multipdfse[np.argmin(np.abs(chi2score_e))].plotOn(frame_e, ROOT.RooFit.VisualizeError(multiresultse[np.argmin(np.abs(chi2score_e))], 1), ROOT.RooFit.FillColor(ROOT.kGreen))
        multipdfsm[np.argmin(np.abs(chi2score_m))].plotOn(frame_m, ROOT.RooFit.VisualizeError(multiresultsm[np.argmin(np.abs(chi2score_m))], 1), ROOT.RooFit.FillColor(ROOT.kGreen))
        multipdfse[np.argmin(np.abs(chi2score_e))].plotOn(frame_e)
        multipdfsm[np.argmin(np.abs(chi2score_m))].plotOn(frame_m)
    else:
        multipdfse[1].plotOn(frame_e, ROOT.RooFit.VisualizeError(multiresultse[1], 2), ROOT.RooFit.FillColor(ROOT.kYellow))
        multipdfsm[1].plotOn(frame_m, ROOT.RooFit.VisualizeError(multiresultsm[1], 2), ROOT.RooFit.FillColor(ROOT.kYellow))
        multipdfse[1].plotOn(frame_e, ROOT.RooFit.VisualizeError(multiresultse[1], 1), ROOT.RooFit.FillColor(ROOT.kGreen))
        multipdfsm[1].plotOn(frame_m, ROOT.RooFit.VisualizeError(multiresultsm[1], 1), ROOT.RooFit.FillColor(ROOT.kGreen))
        multipdfse[1].plotOn(frame_e)
        multipdfsm[1].plotOn(frame_m)
    # Add toy signals
    dse.plotOn(frame_e,ROOT.RooFit.DataError(ROOT.RooAbsData.Poisson))
    dsm.plotOn(frame_m,ROOT.RooFit.DataError(ROOT.RooAbsData.Poisson))

    hpulle = frame_e.pullHist()
    framepull_e = mt_res.frame(ROOT.RooFit.Title("Pull Distribution"))
    framepull_e.addPlotable(hpulle, "P")
    hpullm = frame_m.pullHist()
    framepull_m = mt_res.frame(ROOT.RooFit.Title("Pull Distribution"))
    framepull_m.addPlotable(hpullm, "P")

    #add signals to the plot
    widthlist=['5','0p01']
    masslist=['600', '1000', '1600']
    normalizationlist = {
        "el":{
            "5":{
                "600":{"norm":10,"linecolor":ROOT.kRed,"linestyle":9,
                },
                "1000":{"norm":10,"linecolor":ROOT.kViolet,"linestyle":9,
                },
                "1600":{"norm":10,"linecolor":ROOT.kAzure,"linestyle":9,
                },
            },
            "0p01":{
                "600":{"norm":10,"linecolor":ROOT.kRed,"linestyle":1,
                },
                "1000":{"norm":10,"linecolor":ROOT.kViolet,"linestyle":1,
                },
                "1600":{"norm":10,"linecolor":ROOT.kAzure,"linestyle":1,
                },
            }
        },
    }
    normalizationlist['mu'] = normalizationlist['el']
    hpullsig_e = {}
    framepullsig_e = {}
    for ch in ["el","mu"]:
        for iwid in widthlist:
            for imass in masslist:
                inputfile0 = 'data/sigfit_para/'+year+'/wssignal_M'+imass+'_W'+iwid+'_'+ch+'.root'
                wsname = "wssignal_M"+imass+"_W"+iwid+"_"+ch
                print(inputfile0, " : ", wsname)
                ifile0 = ROOT.TFile.Open( inputfile0, 'READ' )
                if not ifile0:
                    return
                ws_in0 = ifile0.Get( wsname )
                pdfname = 'cb_MG_M%s_W%s_%s%s' %(imass,iwid,ch,year)
                sigModel0 = ws_in0.pdf(pdfname)
                print(fit_range(int(imass)))
                mt_res.setRange(ch+iwid+imass, fit_range(int(imass))[0],fit_range(int(imass))[1])
                print(normalizationlist[ch][iwid][imass])
                if 'el' in ch:
                    sigModel0.plotOn(frame_e,ROOT.RooFit.DataError(ROOT.RooAbsData.Poisson),ROOT.RooFit.LineColor(normalizationlist[ch][iwid][imass]['linecolor']),ROOT.RooFit.LineStyle(normalizationlist[ch][iwid][imass]['linestyle']), ROOT.RooFit.Normalization(normalizationlist[ch][iwid][imass]['norm'],ROOT.RooAbsReal.NumEvent),ROOT.RooFit.Range(ch+iwid+imass))#,ROOT.RooFit.LineColor(normalizationlist[ch][iwid][imass]['linecolor']),ROOT.RooFit.LineStyle(ROOT.RooFit.LineColor(normalizationlist[ch][iwid][imass]['linestyle']) ))
                if 'mu' in ch:
                    sigModel0.plotOn(frame_m,ROOT.RooFit.DataError(ROOT.RooAbsData.Poisson),ROOT.RooFit.LineColor(normalizationlist[ch][iwid][imass]['linecolor']),ROOT.RooFit.LineStyle(normalizationlist[ch][iwid][imass]['linestyle']), ROOT.RooFit.Normalization(normalizationlist[ch][iwid][imass]['norm'],ROOT.RooAbsReal.NumEvent),ROOT.RooFit.Range(ch+iwid+imass))


    print("sum Entries: ", toydatae.sumEntries(), toydatam.sumEntries())

    for ch, frame, framepull in zip(["el","mu"],[frame_e, frame_m],[framepull_e,framepull_m]):
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

        leg = ROOT.TLegend(0.25,0.7,0.65,0.9);
        leg.SetBorderSize(0);
        leg.SetLineStyle(1);
        leg.SetLineWidth(1);
        if ch=='el': chname='Electron channel'
        else: chname='Muon channel'
        entry=leg.AddEntry(frame,"Data, "+chname,"pe");
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


        leg2 = ROOT.TLegend(0.6,0.5,0.92,0.9);
        leg2.SetBorderSize(0);
        leg2.SetLineStyle(1);
        leg2.SetLineWidth(1);
        entry=leg2.AddEntry("","Signal 600GeV, #Gamma_{X}/m_{X}=0.01%","l");
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
        entry=leg2.AddEntry("","Signal 1000GeV, #Gamma_{X}/m_{X}=0.01%","l");
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
        entry=leg2.AddEntry("","Signal 1600GeV, #Gamma_{X}/m_{X}=0.01%","l");
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

        if year=='2018': lumi='59.7*0.2'
        elif year=='2017': lumi='41.5*0.2'
        elif year=='2016': lumi='36.3*0.2'
        else:  lumi='137'
        tex = ROOT.TLatex(0.98,0.94,lumi+" fb^{-1} (13 TeV)");
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
        framepull.Draw("same")

        line = ROOT.TLine(MIN_,0,MAX_,0);
        line.SetLineStyle(2)
        line.SetLineWidth(2)
        line.Draw()
        #input('wait..')
        c.SaveAs('fit_%s%s.C' %(year,ch))
        c.SaveAs('fit_%s%s.pdf' %(year,ch))


def makeRooMultiPdfWorkspace(year,baseDir,skimtree,skimfile):

    #prepare Working Space with Roofit
    #Reading Data
    mt_res = ROOT.RooRealVar("mt_res", "mt_res", MIN_, MAX_)
    mt_res.setBins(50)

    # Read el
    F=ROOT.TFile(baseDir+'/el'+year+'_'+skimfile)
    treee=F.Get(skimtree)
    print('read ',baseDir+'/el'+year+'_'+skimfile)
    dse = ROOT.RooDataSet('data_elA'+year+'_mt_res_base', "dse", ROOT.RooArgSet(mt_res), ROOT.RooFit.Import(treee))
    hbinnedfite=ROOT.TH1D("hbinnedfite","hbinnedfite",50,MIN_, MAX_)
    treee.Draw("mt_res>>hbinnedfite","mt_res>"+str(MIN_))
    datahe=ROOT.RooDataHist("datahe","datahe",ROOT.RooArgList(mt_res),ROOT.RooFit.Import(hbinnedfite))
    # Read mu
    F=ROOT.TFile(baseDir+'/mu'+year+'_'+skimfile)
    treem=F.Get(skimtree)
    print('read ',baseDir+'/mu'+year+'_'+skimfile)
    nmtot = treem.GetEntries()
    dsm = ROOT.RooDataSet('data_muA'+year+'_mt_res_base', "dsm", ROOT.RooArgSet(mt_res), ROOT.RooFit.Import(treem))
    hbinnedfitm=ROOT.TH1D("hbinnedfitm","hbinnedfitm",50,MIN_, MAX_)
    treem.Draw("mt_res>>hbinnedfitm","mt_res>"+str(MIN_))
    datahm=ROOT.RooDataHist("datahm","datahm",ROOT.RooArgList(mt_res),ROOT.RooFit.Import(hbinnedfitm))

    ne = dse.sumEntries("mt_res>"+str(MIN_))
    nm = dsm.sumEntries("mt_res>"+str(MIN_))

    #Work space
    ws_out  = ROOT.RooWorkspace( "workspace_all" )
    rootfilename = '%s/%s/%s.root' %( data_outDir,year,ws_out.GetName() )

    #create 3 background pdfs
    func_dijet_e={}
    func_dijet_m={}
    func_vvdijet_e={}
    func_vvdijet_m={}
    func_expow_e={}
    func_expow_m={}
    dijetorder=[1]
    vvdijetorder=[1]
    expoworder=[1]
    pdfnameltchose=[0,4,8]
    dijetorder=[2]
    vvdijetorder=[2]
    expoworder=[2]
    pdfnameltchose=[1,5,9]
    dijetorder=[3]
    vvdijetorder=[3]
    expoworder=[3]
    pdfnameltchose=[2,6,10]
    #dijetorder=[1,2,3]
    #vvdijetorder=[1,2,3]
    #expoworder=[1,2,3]
    #pdfnameltchose=[0,1,2,4,5,6,8,9,10]

    inititalvalueList={
        '2018':{
            'el':{
                'dijet_1':[-3.81052],'dijet_2':[-9.3,-1.9],'dijet_3':[-6.22887,-0.0548648,0.337115],
                'vvdijet_1':[107.05],'vvdijet_2':[27.9024,2.77859],'vvdijet_3':[-4.33316,9.06652,1.71563,],
                'expow_1':[-111.309],'expow_2':[-30.7048,-2.72329],'expow_3':[8.91366,-9.78053,-1.9036],
            },
            'mu':{
                'dijet_1':[-4.22359],'dijet_2':[-11.6,-2.5],'dijet_3':[-7.00656,-0.303116,0.270375],
                'vvdijet_1':[127.769],'vvdijet_2':[28.7694,3.23388],'vvdijet_3':[-15.5714,11.4986,2.2303],
                'expow_1':[-132.407],'expow_2':[-31.7301,-3.17493],'expow_3':[20.94,-12.1652,-2.3987],
            }
        },
        '2017':{
            'el':{
                'dijet_1':[-3.81052],'dijet_2':[-8.23543,-1.48982],'dijet_3':[-6.22887,-0.0548648,0.337115],
                'vvdijet_1':[107.05],'vvdijet_2':[27.9024,2.77859],'vvdijet_3':[-4.33316,9.06652,1.71563,],
                'expow_1':[-111.309],'expow_2':[-30.7048,-2.72329],'expow_3':[8.91366,-9.78053,-1.9036],
            },
            'mu':{
                'dijet_1':[-4.22359],'dijet_2':[-8.69142,-1.47863],'dijet_3':[-7.00656,-0.303116,0.270375],
                'vvdijet_1':[127.769],'vvdijet_2':[28.7694,3.23388],'vvdijet_3':[-15.5714,11.4986,2.2303],
                'expow_1':[-132.407],'expow_2':[-31.7301,-3.17493],'expow_3':[20.94,-12.1652,-2.3987],
            }
        },
        '2016':{
            'el':{
                'dijet_1':[-3.81052],'dijet_2':[-8.23543,-1.48982],'dijet_3':[-6.22887,-0.0548648,0.337115],
                'vvdijet_1':[107.05],'vvdijet_2':[27.9024,2.77859],'vvdijet_3':[-4.33316,9.06652,1.71563,],
                'expow_1':[-111.309],'expow_2':[-30.7048,-2.72329],'expow_3':[8.91366,-9.78053,-1.9036],
            },
            'mu':{
                'dijet_1':[-4.22359],'dijet_2':[-8.69142,-1.47863],'dijet_3':[-7.00656,-0.303116,0.270375],
                'vvdijet_1':[127.769],'vvdijet_2':[28.7694,3.23388],'vvdijet_3':[-15.5714,11.4986,2.2303],
                'expow_1':[-132.407],'expow_2':[-31.7301,-3.17493],'expow_3':[20.94,-12.1652,-2.3987],
            }
        },
    }
    for i in dijetorder:
       func_name = 'dijet_'+str(i)
       #func_name = 'dijet'
       if i==1:
           dijet1_order1_e = ROOT.RooRealVar('dijet'+str(i)+'_order1_elA'+year+'_all_dijet', "power1", inititalvalueList[year]['el'][func_name][0], -100.0, 10)
           dijet1_order1_m = ROOT.RooRealVar('dijet'+str(i)+'_order1_muA'+year+'_all_dijet', "power1", inititalvalueList[year]['mu'][func_name][0], -100.0, 10)
           function = 'TMath::Power( @0/13000., @1 )'
           func_dijet_e[i] = ROOT.RooGenericPdf( '%s_%s'%(func_name, 'elA'+year+'_all_dijet'), func_name, function, ROOT.RooArgList(mt_res,dijet1_order1_e))
           func_dijet_m[i] = ROOT.RooGenericPdf( '%s_%s'%(func_name, 'muA'+year+'_all_dijet'), func_name, function, ROOT.RooArgList(mt_res,dijet1_order1_m))
       if i==2:
           dijet2_order1_e = ROOT.RooRealVar('dijet'+str(i)+'_order1_elA'+year+'_all_dijet', "power1", inititalvalueList[year]['el'][func_name][0], -50.0, -0.001)
           dijet2_order2_e = ROOT.RooRealVar('dijet'+str(i)+'_order2_elA'+year+'_all_dijet', "power2", inititalvalueList[year]['el'][func_name][1], -20.0, -0.001)
           dijet2_order1_m = ROOT.RooRealVar('dijet'+str(i)+'_order1_muA'+year+'_all_dijet', "power1", inititalvalueList[year]['mu'][func_name][0], -50.0, -0.001)
           dijet2_order2_m = ROOT.RooRealVar('dijet'+str(i)+'_order2_muA'+year+'_all_dijet', "power2", inititalvalueList[year]['mu'][func_name][1], -20.0, -0.001)
           function = 'TMath::Power( @0/13000., @1 + @2*TMath::Log10(@0/13000) )'
           func_dijet_e[i] = ROOT.RooGenericPdf( '%s_%s'%(func_name, 'elA'+year+'_all_dijet'), func_name, function, ROOT.RooArgList(mt_res,dijet2_order1_e,dijet2_order2_e))
           func_dijet_m[i] = ROOT.RooGenericPdf( '%s_%s'%(func_name, 'muA'+year+'_all_dijet'), func_name, function, ROOT.RooArgList(mt_res,dijet2_order1_m,dijet2_order2_m))
       if i==3:
           dijet3_order1_e = ROOT.RooRealVar('dijet'+str(i)+'_order1_elA'+year+'_all_dijet', "power1", inititalvalueList[year]['el'][func_name][0], -50.0, -0.001)
           dijet3_order2_e = ROOT.RooRealVar('dijet'+str(i)+'_order2_elA'+year+'_all_dijet', "power2", inititalvalueList[year]['el'][func_name][1], -20.0, -0.001)
           dijet3_order3_e = ROOT.RooRealVar('dijet'+str(i)+'_order3_elA'+year+'_all_dijet', "power3", inititalvalueList[year]['el'][func_name][2], -5, 5)
           dijet3_order1_m = ROOT.RooRealVar('dijet'+str(i)+'_order1_muA'+year+'_all_dijet', "power1", inititalvalueList[year]['mu'][func_name][0], -50.0, -0.001)
           dijet3_order2_m = ROOT.RooRealVar('dijet'+str(i)+'_order2_muA'+year+'_all_dijet', "power2", inititalvalueList[year]['mu'][func_name][1], -20.0, -0.001)
           dijet3_order3_m = ROOT.RooRealVar('dijet'+str(i)+'_order3_muA'+year+'_all_dijet', "power3", inititalvalueList[year]['mu'][func_name][2], -5, 5)
           function = 'TMath::Power( @0/13000., @1 + @2*TMath::Log10(@0/13000) +  @3*TMath::Log10(@0/13000)*TMath::Log10(@0/13000) )'
           func_dijet_e[i] = ROOT.RooGenericPdf( '%s_%s'%(func_name, 'elA'+year+'_all_dijet'), func_name, function, ROOT.RooArgList(mt_res,dijet3_order1_e,dijet3_order2_e,dijet3_order3_e))
           func_dijet_m[i] = ROOT.RooGenericPdf( '%s_%s'%(func_name, 'muA'+year+'_all_dijet'), func_name, function, ROOT.RooArgList(mt_res,dijet3_order1_m,dijet3_order2_m,dijet3_order3_m))
       if i==4:
           dijet4_order1_e = ROOT.RooRealVar('dijet'+str(i)+'_order1_elA'+year+'_all_dijet', "power1", -9, -100.0, -0.01)
           dijet4_order2_e = ROOT.RooRealVar('dijet'+str(i)+'_order2_elA'+year+'_all_dijet', "power2", -2, -20.0, -0.01)
           dijet4_order1_m = ROOT.RooRealVar('dijet'+str(i)+'_order1_muA'+year+'_all_dijet', "power1", -9, -100.0, -0.01)
           dijet4_order2_m = ROOT.RooRealVar('dijet'+str(i)+'_order2_muA'+year+'_all_dijet', "power2", -2, -20.0, -0.01)
           dijet4_order3_e = ROOT.RooRealVar('dijet'+str(i)+'_order3_elA'+year+'_all_dijet', "power3", 0.2, -20, 20)
           dijet4_order3_m = ROOT.RooRealVar('dijet'+str(i)+'_order3_muA'+year+'_all_dijet', "power3", 0.2, -20, 20)
           dijet4_order4_e = ROOT.RooRealVar('dijet'+str(i)+'_order4_elA'+year+'_all_dijet', "power4", 0.2, -20, 20)
           dijet4_order4_m = ROOT.RooRealVar('dijet'+str(i)+'_order4_muA'+year+'_all_dijet', "power4", 0.2, -20, 20)
           function = 'TMath::Power( @0/13000., @1 + @2*TMath::Log10(@0/13000) +  @3*TMath::Log10(@0/13000)*TMath::Log10(@0/13000) +@4*TMath::Log10(@0/13000)*TMath::Log10(@0/13000)*TMath::Log10(@0/13000) )'
           func_dijet_e[i] = ROOT.RooGenericPdf( '%s_%s'%(func_name, 'elA'+year+'_all_dijet'), func_name, function, ROOT.RooArgList(mt_res,dijet4_order1_e,dijet4_order2_e,dijet4_order3_e,dijet4_order4_e))
           func_dijet_m[i] = ROOT.RooGenericPdf( '%s_%s'%(func_name, 'muA'+year+'_all_dijet'), func_name, function, ROOT.RooArgList(mt_res,dijet4_order1_m,dijet4_order2_m,dijet4_order3_m,dijet4_order4_m))

    for i in vvdijetorder:
       func_name = 'vvdijet_'+str(i)
       #func_name = 'vvdijet'
       if i==1:
           vvdijet1_order1_e = ROOT.RooRealVar( 'vvdijet'+str(i)+'_order1_elA'+year+'_all_vvdijet', "power1", inititalvalueList[year]['el'][func_name][0] ,      -50,  300)
           vvdijet1_order1_m = ROOT.RooRealVar( 'vvdijet'+str(i)+'_order1_muA'+year+'_all_vvdijet', "power1", inititalvalueList[year]['mu'][func_name][0] ,      -50,  300)
           function = 'TMath::Power( (1-@0/13000.), @1 )'
           func_vvdijet_e[i] = ROOT.RooGenericPdf( '%s_%s'%(func_name, 'elA'+year+'_all_vvdijet'), '%s_%s'%(func_name, 'elA'+year+'_all_vvdijet'), function, ROOT.RooArgList(mt_res, vvdijet1_order1_e))#,vvdijet_order3_e,vvdijet_order4_e))
           func_vvdijet_m[i] = ROOT.RooGenericPdf( '%s_%s'%(func_name, 'muA'+year+'_all_vvdijet'), '%s_%s'%(func_name, 'muA'+year+'_all_vvdijet'), function, ROOT.RooArgList(mt_res, vvdijet1_order1_m))#,vvdijet_order3_m))#,vvdijet_order4_m))

       if i==2:
           vvdijet2_order1_e = ROOT.RooRealVar( 'vvdijet'+str(i)+'_order1_elA'+year+'_all_vvdijet', "power1", inititalvalueList[year]['el'][func_name][0] ,      -50,  200)
           vvdijet2_order1_m = ROOT.RooRealVar( 'vvdijet'+str(i)+'_order1_muA'+year+'_all_vvdijet', "power1", inititalvalueList[year]['mu'][func_name][0] ,      -50,  200)
           vvdijet2_order2_e = ROOT.RooRealVar( 'vvdijet'+str(i)+'_order2_elA'+year+'_all_vvdijet', "power2", inititalvalueList[year]['el'][func_name][1] ,     -20,   50)
           vvdijet2_order2_m = ROOT.RooRealVar( 'vvdijet'+str(i)+'_order2_muA'+year+'_all_vvdijet', "power2", inititalvalueList[year]['mu'][func_name][1] ,     -20,   50)
           function = 'TMath::Power( (1-@0/13000.), @1 ) / ( TMath::Power( @0/13000. , @2))'
           func_vvdijet_e[i] = ROOT.RooGenericPdf( '%s_%s'%(func_name, 'elA'+year+'_all_vvdijet'), '%s_%s'%(func_name, 'elA'+year+'_all_vvdijet'), function, ROOT.RooArgList(mt_res, vvdijet2_order1_e, vvdijet2_order2_e))#,vvdijet_order3_e,vvdijet_order4_e))
           func_vvdijet_m[i] = ROOT.RooGenericPdf( '%s_%s'%(func_name, 'muA'+year+'_all_vvdijet'), '%s_%s'%(func_name, 'muA'+year+'_all_vvdijet'), function, ROOT.RooArgList(mt_res, vvdijet2_order1_m, vvdijet2_order2_m))#,vvdijet_order3_m))#,vvdijet_order4_m))
       if i==3:
           vvdijet3_order1_e = ROOT.RooRealVar( 'vvdijet'+str(i)+'_order1_elA'+year+'_all_vvdijet', "power1", inititalvalueList[year]['el'][func_name][0] ,      -200,  300)
           vvdijet3_order1_m = ROOT.RooRealVar( 'vvdijet'+str(i)+'_order1_muA'+year+'_all_vvdijet', "power1", inititalvalueList[year]['mu'][func_name][0] ,      -200,  300)
           vvdijet3_order2_e = ROOT.RooRealVar( 'vvdijet'+str(i)+'_order2_elA'+year+'_all_vvdijet', "power2", inititalvalueList[year]['el'][func_name][1] ,     -20,   50)
           vvdijet3_order2_m = ROOT.RooRealVar( 'vvdijet'+str(i)+'_order2_muA'+year+'_all_vvdijet', "power2", inititalvalueList[year]['mu'][func_name][1] ,     -20,   50)
           vvdijet3_order3_e = ROOT.RooRealVar( 'vvdijet'+str(i)+'_order3_elA'+year+'_all_vvdijet', "power3", inititalvalueList[year]['el'][func_name][2] ,     -30,   50)
           vvdijet3_order3_m = ROOT.RooRealVar( 'vvdijet'+str(i)+'_order3_muA'+year+'_all_vvdijet', "power3", inititalvalueList[year]['mu'][func_name][2] ,     -30,   50)
           function = 'TMath::Power( (1-@0/13000.), @1 ) / ( TMath::Power( @0/13000. , @2+ @3*TMath::Log10(@0/13000)))'
           func_vvdijet_e[i] = ROOT.RooGenericPdf( '%s_%s'%(func_name, 'elA'+year+'_all_vvdijet'), '%s_%s'%(func_name, 'elA'+year+'_all_vvdijet'), function, ROOT.RooArgList(mt_res, vvdijet3_order1_e, vvdijet3_order2_e,vvdijet3_order3_e))#,vvdijet_order4_e))
           func_vvdijet_m[i] = ROOT.RooGenericPdf( '%s_%s'%(func_name, 'muA'+year+'_all_vvdijet'), '%s_%s'%(func_name, 'muA'+year+'_all_vvdijet'), function, ROOT.RooArgList(mt_res, vvdijet3_order1_m, vvdijet3_order2_m,vvdijet3_order3_m))#,vvdijet_order4_m))
       if i==4:
           vvdijet4_order1_e = ROOT.RooRealVar( 'vvdijet'+str(i)+'_order1_elA'+year+'_all_vvdijet', "power1", 40 ,      -50,  300)
           vvdijet4_order1_m = ROOT.RooRealVar( 'vvdijet'+str(i)+'_order1_muA'+year+'_all_vvdijet', "power1", 40 ,      -100,  300)
           vvdijet4_order2_e = ROOT.RooRealVar( 'vvdijet'+str(i)+'_order2_elA'+year+'_all_vvdijet', "power2", 2 ,     -20,   50)
           vvdijet4_order2_m = ROOT.RooRealVar( 'vvdijet'+str(i)+'_order2_muA'+year+'_all_vvdijet', "power2", 2 ,     -20,   50)
           vvdijet4_order3_e = ROOT.RooRealVar( 'vvdijet'+str(i)+'_order3_elA'+year+'_all_vvdijet', "power3", 2 ,     -30,   20)
           vvdijet4_order3_m = ROOT.RooRealVar( 'vvdijet'+str(i)+'_order3_muA'+year+'_all_vvdijet', "power3", 2 ,     -30,   20)
           vvdijet4_order4_e = ROOT.RooRealVar( 'vvdijet'+str(i)+'_order4_elA'+year+'_all_vvdijet', "power4", 0 ,     -10,   30)
           vvdijet4_order4_m = ROOT.RooRealVar( 'vvdijet'+str(i)+'_order4_muA'+year+'_all_vvdijet', "power4", 0 ,     -10,   30)
           function = 'TMath::Power( (1-@0/13000.), @1 ) / ( TMath::Power( @0/13000. , @2+ @3*TMath::Log10(@0/13000) +@4*TMath::Log10(@0/13000)*TMath::Log10(@0/13000) )   )'
           func_vvdijet_e[i] = ROOT.RooGenericPdf( '%s_%s'%(func_name, 'elA'+year+'_all_vvdijet'), '%s_%s'%(func_name, 'elA'+year+'_all_vvdijet'), function, ROOT.RooArgList(mt_res, vvdijet4_order1_e, vvdijet4_order2_e,vvdijet4_order3_e,vvdijet4_order4_e))
           func_vvdijet_m[i] = ROOT.RooGenericPdf( '%s_%s'%(func_name, 'muA'+year+'_all_vvdijet'), '%s_%s'%(func_name, 'muA'+year+'_all_vvdijet'), function, ROOT.RooArgList(mt_res, vvdijet4_order1_m, vvdijet4_order2_m,vvdijet4_order3_m,vvdijet4_order4_m))


    for i in expoworder:
       func_name = 'expow_'+str(i)
       #func_name = 'expow'
       if i==1:
           expow1_order1_e = ROOT.RooRealVar( 'expow'+str(i)+'_order1_elA'+year+'_all_expow', "power1", inititalvalueList[year]['el'][func_name][0] ,     -300,   50)
           expow1_order1_m = ROOT.RooRealVar( 'expow'+str(i)+'_order1_muA'+year+'_all_expow', "power1", inititalvalueList[year]['mu'][func_name][0] ,     -300,   50)
           function = 'TMath::Exp( @1*@0/13000.)'
           func_expow_e[i] = ROOT.RooGenericPdf( '%s_%s'%(func_name, 'elA'+year+'_all_expow'), '%s_%s'%(func_name, 'elA'+year+'_all_expow'), function, ROOT.RooArgList(mt_res, expow1_order1_e))#,expow_order3_e,expow_order4_e))
           func_expow_m[i] = ROOT.RooGenericPdf( '%s_%s'%(func_name, 'muA'+year+'_all_expow'), '%s_%s'%(func_name, 'muA'+year+'_all_expow'), function, ROOT.RooArgList(mt_res, expow1_order1_m))#,expow_order3_m))#,expow_order4_m))

       if i==2:
           expow2_order1_e = ROOT.RooRealVar( 'expow'+str(i)+'_order1_elA'+year+'_all_expow', "power1", inititalvalueList[year]['el'][func_name][0] ,     -300,   50)
           expow2_order1_m = ROOT.RooRealVar( 'expow'+str(i)+'_order1_muA'+year+'_all_expow', "power1", inititalvalueList[year]['mu'][func_name][0] ,     -300,   50)
           expow2_order2_e = ROOT.RooRealVar( 'expow'+str(i)+'_order2_elA'+year+'_all_expow', "power2", inititalvalueList[year]['el'][func_name][1] ,      -100,  20)
           expow2_order2_m = ROOT.RooRealVar( 'expow'+str(i)+'_order2_muA'+year+'_all_expow', "power2", inititalvalueList[year]['mu'][func_name][1] ,      -100,  20)
           function = 'TMath::Power( @0/13000., @2 ) * TMath::Exp( @1*@0/13000.)'
           func_expow_e[i] = ROOT.RooGenericPdf( '%s_%s'%(func_name, 'elA'+year+'_all_expow'), '%s_%s'%(func_name, 'elA'+year+'_all_expow'), function, ROOT.RooArgList(mt_res, expow2_order1_e, expow2_order2_e))#,expow_order3_e,expow_order4_e))
           func_expow_m[i] = ROOT.RooGenericPdf( '%s_%s'%(func_name, 'muA'+year+'_all_expow'), '%s_%s'%(func_name, 'muA'+year+'_all_expow'), function, ROOT.RooArgList(mt_res, expow2_order1_m, expow2_order2_m))#,expow_order3_m))#,expow_order4_m))
       if i==3:
           expow3_order1_e = ROOT.RooRealVar( 'expow'+str(i)+'_order1_elA'+year+'_all_expow', "power1", inititalvalueList[year]['el'][func_name][0] ,     -300,   50)
           expow3_order1_m = ROOT.RooRealVar( 'expow'+str(i)+'_order1_muA'+year+'_all_expow', "power1", inititalvalueList[year]['mu'][func_name][0] ,     -300,   100)
           expow3_order2_e = ROOT.RooRealVar( 'expow'+str(i)+'_order2_elA'+year+'_all_expow', "power2", inititalvalueList[year]['el'][func_name][1] ,      -100,  20)
           expow3_order2_m = ROOT.RooRealVar( 'expow'+str(i)+'_order2_muA'+year+'_all_expow', "power2", inititalvalueList[year]['mu'][func_name][1] ,      -100,  20)
           expow3_order3_e = ROOT.RooRealVar( 'expow'+str(i)+'_order3_elA'+year+'_all_expow', "power3", inititalvalueList[year]['el'][func_name][2] ,     -50,   50)
           expow3_order3_m = ROOT.RooRealVar( 'expow'+str(i)+'_order3_muA'+year+'_all_expow', "power3", inititalvalueList[year]['mu'][func_name][2] ,     -50,   50)
           function = 'TMath::Power( @0/13000., @2 +  @3*TMath::Log10(@0/13000) ) * TMath::Exp( @1*@0/13000.)'
           func_expow_e[i] = ROOT.RooGenericPdf( '%s_%s'%(func_name, 'elA'+year+'_all_expow'), '%s_%s'%(func_name, 'elA'+year+'_all_expow'), function, ROOT.RooArgList(mt_res, expow3_order1_e, expow3_order2_e,expow3_order3_e))#,expow_order4_e))
           func_expow_m[i] = ROOT.RooGenericPdf( '%s_%s'%(func_name, 'muA'+year+'_all_expow'), '%s_%s'%(func_name, 'muA'+year+'_all_expow'), function, ROOT.RooArgList(mt_res, expow3_order1_m, expow3_order2_m,expow3_order3_m))#,expow_order4_m))
       if i==4:
           expow4_order1_e = ROOT.RooRealVar( 'expow'+str(i)+'_order1_elA'+year+'_all_expow', "power1", 20 ,     -300,   50)
           expow4_order1_m = ROOT.RooRealVar( 'expow'+str(i)+'_order1_muA'+year+'_all_expow', "power1", 20 ,     -300,   100)
           expow4_order2_e = ROOT.RooRealVar( 'expow'+str(i)+'_order2_elA'+year+'_all_expow', "power2", -2 ,      -100,  20)
           expow4_order2_m = ROOT.RooRealVar( 'expow'+str(i)+'_order2_muA'+year+'_all_expow', "power2", -2 ,      -100,  20)
           expow4_order3_e = ROOT.RooRealVar( 'expow'+str(i)+'_order3_elA'+year+'_all_expow', "power3", -5 ,     -50,   50)
           expow4_order3_m = ROOT.RooRealVar( 'expow'+str(i)+'_order3_muA'+year+'_all_expow', "power3", -5 ,     -50,   50)
           expow4_order4_e = ROOT.RooRealVar( 'expow'+str(i)+'_order4_elA'+year+'_all_expow', "power4", -5 ,     -50,   50)
           expow4_order4_m = ROOT.RooRealVar( 'expow'+str(i)+'_order4_muA'+year+'_all_expow', "power4", -5 ,     -50,   50)
           function = 'TMath::Power( @0/13000., @2 +  @3*TMath::Log10(@0/13000)+@4*TMath::Log10(@0/13000)*TMath::Log10(@0/13000) ) * TMath::Exp( @1*@0/13000.)'
           func_expow_e[i] = ROOT.RooGenericPdf( '%s_%s'%(func_name, 'elA'+year+'_all_expow'), '%s_%s'%(func_name, 'elA'+year+'_all_expow'), function, ROOT.RooArgList(mt_res, expow4_order1_e, expow4_order2_e,expow4_order3_e,expow4_order4_e))
           func_expow_m[i] = ROOT.RooGenericPdf( '%s_%s'%(func_name, 'muA'+year+'_all_expow'), '%s_%s'%(func_name, 'muA'+year+'_all_expow'), function, ROOT.RooArgList(mt_res, expow4_order1_m, expow4_order2_m,expow4_order3_m,expow4_order4_m))

    resu_dijet_e={}
    resu_dijet_m={}
    resu_vvdijet_e={}
    resu_vvdijet_m={}
    resu_expow_e={}
    resu_expow_m={}
    # First we fit the pdfs to the data
    catIndexe = ROOT.RooCategory('pdf_index_el'+year,'Index of Pdf which is active')
    catIndexm = ROOT.RooCategory('pdf_index_mu'+year,'Index of Pdf which is active')
    mypdfse = ROOT.RooArgList("store")
    mypdfsm = ROOT.RooArgList("store")
    print("===> fit result")
    for i in dijetorder:
        # unbinned fit
        #resu_dijet_e[i] = func_dijet_e[i].fitTo(dse,ROOT.RooFit.Save(),ROOT.RooFit.SumW2Error(ROOT.kTRUE))
        #resu_dijet_m[i] = func_dijet_m[i].fitTo(dsm,ROOT.RooFit.Save(),ROOT.RooFit.SumW2Error(ROOT.kTRUE))
        # binned fit
        resu_dijet_e[i] = func_dijet_e[i].fitTo(datahe,ROOT.RooFit.Save(),ROOT.RooFit.SumW2Error(ROOT.kTRUE))
        resu_dijet_m[i] = func_dijet_m[i].fitTo(datahm,ROOT.RooFit.Save(),ROOT.RooFit.SumW2Error(ROOT.kTRUE))

        resu_dijet_e[i].Print()
        resu_dijet_m[i].Print()
        mypdfse.add(func_dijet_e[i])
        mypdfsm.add(func_dijet_m[i])
    #input()
    for i in vvdijetorder:
        # unbinned fit
        #resu_vvdijet_e[i] = func_vvdijet_e[i].fitTo(dse,ROOT.RooFit.Save(),ROOT.RooFit.SumW2Error(ROOT.kTRUE))
        #resu_vvdijet_m[i] = func_vvdijet_m[i].fitTo(dsm,ROOT.RooFit.Save(),ROOT.RooFit.SumW2Error(ROOT.kTRUE))
        # binned fit
        resu_vvdijet_e[i] = func_vvdijet_e[i].fitTo(datahe,ROOT.RooFit.Save(),ROOT.RooFit.SumW2Error(ROOT.kTRUE))
        resu_vvdijet_m[i] = func_vvdijet_m[i].fitTo(datahm,ROOT.RooFit.Save(),ROOT.RooFit.SumW2Error(ROOT.kTRUE))

        resu_vvdijet_e[i].Print()
        resu_vvdijet_m[i].Print()
        mypdfse.add(func_vvdijet_e[i])
        mypdfsm.add(func_vvdijet_m[i])
    #input()
    for i in expoworder:
        # unbinned fit
        #resu_expow_e[i] = func_expow_e[i].fitTo(dse,ROOT.RooFit.Save(),ROOT.RooFit.SumW2Error(ROOT.kTRUE))
        #resu_expow_m[i] = func_expow_m[i].fitTo(dsm,ROOT.RooFit.Save(),ROOT.RooFit.SumW2Error(ROOT.kTRUE))
        # binned fit
        resu_expow_e[i] = func_expow_e[i].fitTo(datahe,ROOT.RooFit.Save(),ROOT.RooFit.SumW2Error(ROOT.kTRUE))
        resu_expow_m[i] = func_expow_m[i].fitTo(datahm,ROOT.RooFit.Save(),ROOT.RooFit.SumW2Error(ROOT.kTRUE))

        resu_expow_e[i].Print()
        resu_expow_m[i].Print()
        mypdfse.add(func_expow_e[i])
        mypdfsm.add(func_expow_m[i])
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
        frame_toye = mt_res.frame(ROOT.RooFit.Title("Unbinned ML fit, el"))
        #dse.plotOn(frame_toye,ROOT.RooFit.DataError(ROOT.RooAbsData.SumW2))
        datahe.plotOn(frame_toye,ROOT.RooFit.DataError(ROOT.RooAbsData.SumW2))
        chi2score_e=[]
        multipdfse=[]
        multiresultse=[]
        for i in dijetorder:
            multipdfse.append(func_dijet_e[i])
            multiresultse.append(resu_dijet_e[i])
        for i in vvdijetorder:
            multipdfse.append(func_vvdijet_e[i])
            multiresultse.append(resu_vvdijet_e[i])
        for i in expoworder:
            multipdfse.append(func_expow_e[i])
            multiresultse.append(resu_expow_e[i])
        for toypdf in multipdfse:
            toypdf.plotOn(frame_toye)
            print('-------> %0.3f'%(frame_toye.chiSquare()))
            chi2score_e.append(abs(frame_toye.chiSquare()-1))
        frame_toym = mt_res.frame(ROOT.RooFit.Title("Unbinned ML fit, mu"))
        #dsm.plotOn(frame_toym,ROOT.RooFit.DataError(ROOT.RooAbsData.SumW2))
        datahm.plotOn(frame_toym,ROOT.RooFit.DataError(ROOT.RooAbsData.SumW2))
        chi2score_m=[]
        multipdfsm=[]
        multiresultsm=[]
        for i in dijetorder:
            multipdfsm.append(func_dijet_m[i])
            multiresultsm.append(resu_dijet_m[i])
        for i in vvdijetorder:
            multipdfsm.append(func_vvdijet_m[i])
            multiresultsm.append(resu_vvdijet_m[i])
        for i in expoworder:
            multipdfsm.append(func_expow_m[i])
            multiresultsm.append(resu_expow_m[i])
        for toypdf in multipdfsm:
            toypdf.plotOn(frame_toym)
            print('-------> %0.3f'%(frame_toym.chiSquare()))
            chi2score_m.append(abs(frame_toym.chiSquare()-1))
        chi2toty=False
        if chi2toty:
            he=ROOT.TH1F("he","he",100,0,20)
            hm=ROOT.TH1F("hm","hm",100,0,20)
            he_=[]
            hm_=[]
            for ifun in [1,5,9]:
                he=ROOT.TH1F("he","he",100,0,20)
                hm=ROOT.TH1F("hm","hm",100,0,20)
                for itoy in range(400):
                    toydatae = multipdfse[ifun].generate(ROOT.RooArgSet(mt_res),ne)
                    toydatam = multipdfsm[ifun].generate(ROOT.RooArgSet(mt_res),nm)
                    frame_toye = mt_res.frame(ROOT.RooFit.Title("Unbinned ML fit, el"))
                    toydatae.plotOn(frame_toye,ROOT.RooFit.DataError(ROOT.RooAbsData.SumW2))
                    frame_toym = mt_res.frame(ROOT.RooFit.Title("Unbinned ML fit, mu"))
                    toydatam.plotOn(frame_toym,ROOT.RooFit.DataError(ROOT.RooAbsData.SumW2))
                    multipdfse[ifun].plotOn(frame_toye)
                    multipdfsm[ifun].plotOn(frame_toym)
                    #print('-------> %0.3f'%(frame_toye.chiSquare()))
                    #print('-------> %0.3f'%(frame_toym.chiSquare()))  
                    he.Fill(frame_toye.chiSquare())
                    hm.Fill(frame_toym.chiSquare())     
                #print('%0.3f & %0.3f'%(he.GetMean(), he.GetStdDev()))
                #print('%0.3f & %0.3f'%(hm.GetMean(), hm.GetStdDev()))
                he_.append('%0.3f & %0.3f'%(he.GetMean(), he.GetStdDev()))
                hm_.append('%0.3f & %0.3f'%(hm.GetMean(), hm.GetStdDev()))
            print(he_,hm_)
        #exit()
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
    print("=======> Finished making files")
    #return
    # Make plots
    # dijet, vvdiijet, expow
    pdfnamelt=['dijet-1','dijet-2','dijet-3','dijet-4','vvdijet-1','vvdijet-2','vvdijet-3','vvdijet-4','expow-1','expow-2','expow-3','expow-4']
    #for ipdf in range(9):
    #for ipdf in [0,4,8]:
    for ipdf in range(len(pdfnameltchose)):
        ipdfname=pdfnamelt[pdfnameltchose[ipdf]]
        frame_e = mt_res.frame(ROOT.RooFit.Title("Unbinned ML fit, el"))
        frame_m = mt_res.frame(ROOT.RooFit.Title("Unbinned ML fit, mu"))
        #dse.plotOn(frame_e,ROOT.RooFit.DataError(ROOT.RooAbsData.SumW2))
        #dsm.plotOn(frame_m,ROOT.RooFit.DataError(ROOT.RooAbsData.SumW2))
        datahe.plotOn(frame_e,ROOT.RooFit.DataError(ROOT.RooAbsData.SumW2))
        datahm.plotOn(frame_m,ROOT.RooFit.DataError(ROOT.RooAbsData.SumW2))
        #toydatae.plotOn(frame_e,ROOT.RooFit.DataError(ROOT.RooAbsData.SumW2))
        #toydatam.plotOn(frame_m,ROOT.RooFit.DataError(ROOT.RooAbsData.SumW2))
        multipdfse[ipdf].plotOn(frame_e,ROOT.RooFit.VisualizeError(multiresultse[ipdf], 2), ROOT.RooFit.FillColor(ROOT.kYellow))
        multipdfsm[ipdf].plotOn(frame_m,ROOT.RooFit.VisualizeError(multiresultsm[ipdf], 2), ROOT.RooFit.FillColor(ROOT.kYellow))
        multipdfse[ipdf].plotOn(frame_e,ROOT.RooFit.VisualizeError(multiresultse[ipdf], 1), ROOT.RooFit.FillColor(ROOT.kGreen))
        multipdfsm[ipdf].plotOn(frame_m,ROOT.RooFit.VisualizeError(multiresultsm[ipdf], 1), ROOT.RooFit.FillColor(ROOT.kGreen))
        multipdfse[ipdf].plotOn(frame_e)
        multipdfsm[ipdf].plotOn(frame_m)
        #dse.plotOn(frame_e,ROOT.RooFit.DataError(ROOT.RooAbsData.SumW2))
        #dsm.plotOn(frame_m,ROOT.RooFit.DataError(ROOT.RooAbsData.SumW2))
        datahe.plotOn(frame_e,ROOT.RooFit.DataError(ROOT.RooAbsData.SumW2))
        datahm.plotOn(frame_m,ROOT.RooFit.DataError(ROOT.RooAbsData.SumW2))

        for ch, frame in zip(["mu","el"],[frame_m, frame_e]):
        #for ch, frame in zip(["el","mu"],[frame_e, frame_m]):
            c = ROOT.TCanvas("c","c",800,800) ;
            ROOT.gStyle.SetOptStat(0)
            c.SetFillColor(0)
            c.SetBorderMode(0)
            c.SetBorderSize(2)
            c.SetFrameBorderMode(0)
            #------------>Primitives in pad: toppad
            toppad = ROOT.TPad('toppad','toppad',0,0.32 ,1.0,1.0)
            bottompad = ROOT.TPad('bottompad','bottompad',0,0.0,1.0,0.26)
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
            NN_=10
            frame_4fa51a0__1 = ROOT.TH1D("frame_4fa51a0__1","Unbinned ML fit, %s %s"%(ch,year),NN_,MIN_,MAX_)
            frame_4fa51a0__1.GetXaxis().SetTitle("m_{T}^{l#nu}");
            frame_4fa51a0__1.GetXaxis().SetLabelFont(42);
            frame_4fa51a0__1.GetXaxis().SetLabelSize(0.05);
            frame_4fa51a0__1.GetXaxis().SetTitleSize(0.05);
            frame_4fa51a0__1.GetXaxis().SetTitleOffset(1);
            frame_4fa51a0__1.GetXaxis().SetTitleFont(42);
            frame_4fa51a0__1.GetYaxis().SetTitle("Events / 42GeV");
            frame_4fa51a0__1.GetYaxis().SetLabelFont(42);
            frame_4fa51a0__1.GetYaxis().SetLabelSize(0.05);
            frame_4fa51a0__1.GetYaxis().SetTitleSize(0.05);
            frame_4fa51a0__1.GetYaxis().SetTitleFont(42);
            frame_4fa51a0__1.GetYaxis().SetRangeUser(0.1,1e3)
            frame_4fa51a0__1.GetXaxis().SetLabelOffset(999)
            frame_4fa51a0__1.GetXaxis().SetLabelSize(0)
            frame_4fa51a0__1.Draw("AXISSAME");
            frame.Draw("same")
            frame_4fa51a0__1.Draw("AXISSAME");

            hpull = frame.pullHist()
            frame3 = mt_res.frame(ROOT.RooFit.Title("Pull Distribution"))
            frame3.addPlotable(hpull, "P")

            leg = ROOT.TLegend(0.5,0.6,0.9,0.85);
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
            htmp2=ROOT.TH1F("htmp2","htmp2",10,0,1)
            htmp2.SetFillColor(ROOT.kYellow)
            entry=leg.AddEntry(htmp2,"2-sigma error band","f");
            entry.SetFillStyle(1001);
            entry.SetLineStyle(1);
            entry.SetLineWidth(2);
            entry.SetMarkerStyle(20);
            entry.SetTextFont(42);
            entry.SetTextSize(0.06);
            leg.Draw()

            tex = ROOT.TLatex(0.38,0.84,ch+","+ipdfname);
            tex.SetNDC();
            tex.SetTextAlign(31);
            tex.SetTextFont(42);
            tex.SetTextSize(0.05);
            tex.SetLineWidth(2);
            tex.Draw();

            bottompad.cd()
            frame_4fa51a0__2 = ROOT.TH1D("frame_4fa51a0__2","",NN_,MIN_,MAX_)
            frame_4fa51a0__2.GetXaxis().SetTitle("m_{T}^{l#nu} [GeV]");
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
            frame_4fa51a0__2.Draw("AXISSAME")
            input('wait..')
            #c.SaveAs('fit_%s%s_%s.png' %( year,ch,ipdfname))
            #c.SaveAs('fit_%s%s_%s.C' %( year,ch,ipdfname))


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
    mass = '600'
    c = ROOT.TCanvas()
    ROOT.gStyle.SetOptStat(0)
    print('=========>',ch,year)
    for i in [0,4,8]:
    #for i in range(9):
        rootfilename = 'data/wg/Width5/%s%s/Mass%s/higgsCombinepdf%s.GoodnessOfFit.mH120.root'%(ch,year,mass,str(i))
        ifile = ROOT.TFile.Open( rootfilename, 'READ' )
        tree = ifile.Get( 'limit' )
        for e in tree:
            print("=========> %0.3f"%(e.limit))
            datalimit =  e.limit
        rootfilename = 'data/wg/Width5/%s%s/Mass%s/higgsCombine*pdf%s.GoodnessOfFit.mH120.12*.root'%(ch,year,mass,str(i))
        ifile = ROOT.TChain('limit')
        ifile.Add(rootfilename)
        #ifile = ROOT.TFile.Open( rootfilename, 'READ' )
        #tree = ifile.Get( 'limit' )
        hlimit = ROOT.TH1D("hlimit", "Goodness of Fit (%s %s);limit;"%(ch,year), 20, 0.1, 0.3);
        ifile.Draw("limit>>hlimit")
        hlimit.SetLineColor(ROOT.kRed)
        hlimit.Fit("gaus","Q")
        fuv=hlimit.GetFunction("gaus")
        print('%0.3f & %0.3f & %0.3f & %0.3f'%(datalimit, fuv.GetParameter(1)-fuv.GetParameter(2),fuv.GetParameter(1),fuv.GetParameter(1)+fuv.GetParameter(2)))

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
        continue
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
        #entry=leg.AddEntry("","P=%0.2f"%(1-tot/500.0),"l");
        #entry.SetFillStyle(1001);
        #entry.SetLineStyle(1);
        #entry.SetLineWidth(0);
        #entry.SetMarkerStyle(20);
        #entry.SetTextFont(42);
        #entry.SetTextSize(0.1);
        leg.Draw()
        input()
        #c.SaveAs('year'+ch+year+"_Mass"+mass+"_hlimit.C")
        #c.SaveAs('year'+ch+year+"_Mass"+mass+"_hlimit.png")


def testBias():

    hbias = {}
    ifile = {}
    rsignalr = [ '1']
    leg1 = 'dijet -> vvdijet'
    special_str='_expow2enve'
    mean_collection = {}
    sigma_collection = {}
    mean_collection_e = {}
    sigma_collection_e = {}
    masslist    = [300, 350, 400, 450, 500, 600, 700, 800,900, 1000, 1200, 1400, 1600, 1800, 2000]
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
                tree.Add('data/wg/Width%s/all/Mass%s/fitDiagnostics*%s*.root'%(wid,str(im),special_str))
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
                #c.SaveAs('gr_bias_Width'+wid+'_Mass'+str(im)+'_r'+irr+".C")
                #c.SaveAs('gr_bias_Width'+wid+'_Mass'+str(im)+'_r'+irr+".png")
                #input('wait')
    cc = ROOT.TCanvas()
    ROOT.gStyle.SetOptStat(0)
    leg = ROOT.TLegend(0.21,0.6,0.35,0.85);
    leg.SetBorderSize(0);
    leg.SetLineStyle(1);
    leg.SetLineWidth(2);
    i=1
    wide_str=''
    narr_str=''
    wide_stre=''
    narr_stre=''
    for wid in widlist:
        for im in masslist:
            for ir in rsignalr:
                print(mean_collection['r'+ir+'W'+wid+'m'+str(im)])
                if '5' in wid: 
                    wide_str+='%0.4f, '%(mean_collection['r'+ir+'W'+wid+'m'+str(im)])
                    wide_stre+='%0.4f, '%(mean_collection_e['r'+ir+'W'+wid+'m'+str(im)])
                else:
                    narr_str+='%0.4f, '%(mean_collection['r'+ir+'W'+wid+'m'+str(im)])
                    narr_stre+='%0.4f, '%(mean_collection_e['r'+ir+'W'+wid+'m'+str(im)])
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
    print('wide:',wide_str,wide_stre)
    print('narr:',narr_str,narr_stre)
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
#skimfile     =  "skim.root"

#testBias()

#ShowSignalInjection()
#makeFinalplots(data_outDir,skimtree)
#exit()

#for year in ['2016','2017','2018']:
for year in ['2018']:#,'2017','2018']:
    #goodnessOfFit(year,data_outDir,skimtree,skimfile)
    #makeRooMultiPdfWorkspace(year,data_outDir,skimtree,skimfile)
    for ch in ['el','mu']:
        #CombineGoF(ch, year)
        prepare_data(5, year, ch, skimtree, data_outDir+'/'+ch+year+'_'+skimfile)

#testBias()
#pltToyFit()
#checkenv()

