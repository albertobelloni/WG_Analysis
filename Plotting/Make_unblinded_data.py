import ROOT
from array import array
#execfile("MakeBase.py")
from ROOT import gSystem
gSystem.Load('../../../combine/CMSSW_11_0_0/lib/slc7_amd64_gcc820/libHiggsAnalysisCombinedLimit.so')

from ROOT import RooMultiPdf

MIN_ = 200
MAX_ = 2000
treeIn      = "UMDNTuple/EventTree"
import os
data_outDir = "data_1015_afterbias_study/bkgfit_data"
if data_outDir is not None :
    if not os.path.isdir( data_outDir ) :
        os.makedirs( data_outDir )
        os.makedirs( data_outDir+'/2016' )
        os.makedirs( data_outDir+'/2017' )
        os.makedirs( data_outDir+'/2018' )
import glob
FileMap = {}
Date = '2021_09_17'
#Date = '2021_08_27'
for year in ['2016','2017','2018']:
    for ch in ['el','mu']:
        if ch == 'el':
            FileMap[year+ch] = glob.glob('/data/users/yihuilai/Resonances'+year+'/LepGamma_elg_'+Date+'/WithSF/SingleElectron/Job*/tree.root')
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

def prepare_data(frac, year, ch, skimtree, skimfile):
    #Prepare skimed data
    names = ROOT.std.vector('string')()
    for n in FileMap[year+ch]: names.push_back(n)
    d = ROOT.RDataFrame(treeIn, names)
    #hardcoded selections
    print('hardcoded selections')
    if ch=='el':
        myfilter = d.Filter("el_n==1&& mu_n==0 && ph_n==1&&  fabs( el_eta[0] ) < 2.1&& el_pt[0] > 35  &&  el_passTight[0] == 1 && met_pt > 40 && fabs(m_lep_ph-91)>20.0 && jet_CSVMedium_n==0 && ph_IsEB[0] && ph_passTight[0] && ph_pt[0] > 0.4*mt_res && ph_pt[0] < 0.55*mt_res && !ph_hasPixSeed[0]").Range(1,0,frac)
        #myfilter = d.Filter("el_n==1&& mu_n==0 && ph_n==1&&  fabs( el_eta[0] ) < 2.1&& el_pt[0] > 35  &&  el_passTight[0] == 1 && met_pt > 40 && fabs(m_lep_ph-91)>20.0 && jet_CSVMedium_n==0 && ph_IsEB[0] && ph_passTight[0] && ph_pt[0] > 0.4*mt_res && ph_pt[0] < 0.55*mt_res && !ph_hasPixSeed[0]")
    elif ch=='mu':
        myfilter = d.Filter("mu_n==1 && el_n==0 && ph_n==1 && met_pt > 40 && mu_pt_rc[0] > 35  && jet_CSVMedium_n==0 && ph_IsEB[0] && ph_passTight[0] && ph_pt[0] > 0.4*mt_res && ph_pt[0] < 0.55*mt_res && !ph_hasPixSeed[0]").Range(1,0,frac)
        #myfilter = d.Filter("mu_n==1 && el_n==0 && ph_n==1 && met_pt > 40 && mu_pt_rc[0] > 35  && jet_CSVMedium_n==0 && ph_IsEB[0] && ph_passTight[0] && ph_pt[0] > 0.4*mt_res && ph_pt[0] < 0.55*mt_res && !ph_hasPixSeed[0]")
    else:
        print("use el or mu")
        exit()
    print('make histo')
    Hmt = myfilter.Histo1D("mt_res")
    Hmt.Draw()
    myfilter.Snapshot(skimtree, skimfile)

def prepareWS(year,baseDir,skimtree,skimfile):

    #prepare Working Space with Roofit
    #Reading Data
    mt_res = ROOT.RooRealVar("mt_res", "mt_res", 0, 2000);
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


    dijet_order1_e = ROOT.RooRealVar('dijet_order1_A'+year+'_all_dijet', "power1", -9, -50.0, 0)
    dijet_order1_m = ROOT.RooRealVar('dijet_order1_A'+year+'_all_dijet', "power1", -9, -50.0, 0)
    dijet_order2_e = ROOT.RooRealVar('dijet_order2_A'+year+'_all_dijet', "power2", -2, -10.0, 0)
    dijet_order2_m = ROOT.RooRealVar('dijet_order2_A'+year+'_all_dijet', "power2", -2, -10.0, 0)

    #Work space
    ws_out  = ROOT.RooWorkspace( "workspace_all" )
    rootfilename = '%s/%s/%s.root' %( data_outDir,year,ws_out.GetName() )


    toy1 = ROOT.RooRealVar('power1', "power1", -72, -200, 200)
    toy2 = ROOT.RooRealVar('power2', "power2", 22, -200, 200)
    toy3 = ROOT.RooRealVar('power3', "power3", 5, -200, 200)
    toy1.setError(0.001)
    toy2.setError(0.001)
    toy3.setError(0.001)
    func_toy_e = ROOT.RooGenericPdf( 'toy', 'toy', 'TMath::Power( (1-@0/13000.), @1 ) / ( TMath::Power( @0/13000. , @2+ @3*TMath::Power(TMath::Log10( @0/13000.),1) ))', ROOT.RooArgList(mt_res,toy1,toy2,toy3))
    toydatae = func_toy_e.generate(ROOT.RooArgSet(mt_res),ne)
    toydatam = func_toy_e.generate(ROOT.RooArgSet(mt_res),nm)
    toydatae.SetName ('data_elA'+year+'_mt_res_base')
    toydatam.SetName ('data_muA'+year+'_mt_res_base')
    #import_workspace( ws_out, toydatae)
    #import_workspace( ws_out, toydatam)

    import_workspace( ws_out, dse)
    import_workspace( ws_out, dsm)

    #p.d.f
    do_dijet=False
    if do_dijet:

        #dijet_order4_e = ROOT.RooRealVar('dijet_order4_elA'+year+'_all_dijet', "power4", -1.5, -100.0, 0)
        #dijet_order4_m = ROOT.RooRealVar('dijet_order4_muA'+year+'_all_dijet', "power4", -1.5, -100.0, 0)
        function = ''
        func_name = 'dijet'
        if func_name == 'dijet' :
            order_entries = []
            log_str = 'TMath::Log10(@0/13000)'
            for i in range( 1, 2) :
                order_entries.append('@'+str(i+1)+'*' + '*'.join( [log_str]*i))
            function = 'TMath::Power( @0/13000., @1 + ' + '+'.join( order_entries) + ')'
            print "function: ", function
            #function = 'TMath::Power( @0/13000., @1 + @2*TMath::Log10(@0/13000)*(1+@3*TMath::Log10(@0/13000)))'
            func_pdf_e = ROOT.RooGenericPdf( '%s_%s'%(func_name, 'elA'+year+'_all_dijet'), func_name, function, ROOT.RooArgList(mt_res,dijet_order1_e,dijet_order2_e))
            func_pdf_m = ROOT.RooGenericPdf( '%s_%s'%(func_name, 'muA'+year+'_all_dijet'), func_name, function, ROOT.RooArgList(mt_res,dijet_order1_m,dijet_order2_m))

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
        #import_workspace( ws_out, dse)
        #import_workspace( ws_out, dsm)
        import_workspace( ws_out, dijet_order1_e )
        import_workspace( ws_out, dijet_order1_m )
        import_workspace( ws_out, dijet_order2_e )
        import_workspace( ws_out, dijet_order2_m )
        #import_workspace( ws_out, dijet_order3_e )
        #import_workspace( ws_out, dijet_order3_m )
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

        vvdijet_order1_e = ROOT.RooRealVar( 'vvdijet_order1_A_all_vvdijet', "power1", 90 ,      0,  200)
        vvdijet_order2_e = ROOT.RooRealVar( 'vvdijet_order2_A_all_vvdijet', "power2", -6 ,     -100,   0)
        vvdijet_order3_e = ROOT.RooRealVar( 'vvdijet_order3_A_all_vvdijet', "power3", -2 ,       -100,    0)
        vvdijet_order1_m = ROOT.RooRealVar( 'vvdijet_order1_A_all_vvdijet', "power1", 90 ,      0,  200)
        vvdijet_order2_m = ROOT.RooRealVar( 'vvdijet_order2_A_all_vvdijet', "power2", -6 ,     -100,   0)
        vvdijet_order3_m = ROOT.RooRealVar( 'vvdijet_order3_A_all_vvdijet', "power3", -2 ,       -100,    0)

        #vvdijet_order1_e = ROOT.RooRealVar( 'vvdijet_order1_A_all_vvdijet', "power1", -10 ,      -100,  0)
        #vvdijet_order2_e = ROOT.RooRealVar( 'vvdijet_order2_A_all_vvdijet', "power2", 10 ,     0,   40)
        #vvdijet_order3_e = ROOT.RooRealVar( 'vvdijet_order3_A_all_vvdijet', "power3", 3 ,       0,    20)
        #vvdijet_order1_m = ROOT.RooRealVar( 'vvdijet_order1_A_all_vvdijet', "power1", -10 ,      -100,  0)
        #vvdijet_order2_m = ROOT.RooRealVar( 'vvdijet_order2_A_all_vvdijet', "power2", 10 ,     0,   40)
        #vvdijet_order3_m = ROOT.RooRealVar( 'vvdijet_order3_A_all_vvdijet', "power3", 3 ,       0,    20)


        #vvdijet_order1_e = ROOT.RooRealVar( 'vvdijet_order1_A_all_vvdijet', "power1", -90 ,      -200,  200)
        #vvdijet_order2_e = ROOT.RooRealVar( 'vvdijet_order2_A_all_vvdijet', "power2", 6 ,     -200,   200)
        #vvdijet_order3_e = ROOT.RooRealVar( 'vvdijet_order3_A_all_vvdijet', "power3", 2 ,       -200,    200)
        #vvdijet_order1_m = ROOT.RooRealVar( 'vvdijet_order1_A_all_vvdijet', "power1", -90 ,      -200,  200)
        #vvdijet_order2_m = ROOT.RooRealVar( 'vvdijet_order2_A_all_vvdijet', "power2", 6 ,     -200,   200)
        #vvdijet_order3_m = ROOT.RooRealVar( 'vvdijet_order3_A_all_vvdijet', "power3", 2 ,       -200,    200)


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
        func_vvdi_m = ROOT.RooGenericPdf( '%s_%s'%(func_name, 'muA'+year+'_all_vvdijet'), '%s_%s'%(func_name, 'muA'+year+'_all_vvdijet'), function, ROOT.RooArgList(mt_res, vvdijet_order1_m, vvdijet_order2_m, vvdijet_order3_m))
        func_vvdi_e = ROOT.RooGenericPdf( '%s_%s'%(func_name, 'elA'+year+'_all_vvdijet'), '%s_%s'%(func_name, 'elA'+year+'_all_vvdijet'), function, ROOT.RooArgList(mt_res, vvdijet_order1_e, vvdijet_order2_e, vvdijet_order3_e))
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

        #atlas_order1_e = ROOT.RooRealVar( 'atlas_order1_elA'+year+'_all_atlas', "power1", 0 ,      -100,  100)
        #atlas_order2_e = ROOT.RooRealVar( 'atlas_order2_elA'+year+'_all_atlas', "power2", 9 ,     -100,   100)
        #atlas_order3_e = ROOT.RooRealVar( 'atlas_order3_elA'+year+'_all_atlas', "power3", 1 ,       -100,    100)
        #atlas_order1_m = ROOT.RooRealVar( 'atlas_order1_muA'+year+'_all_atlas', "power1", 0 ,      -100,  100)
        #atlas_order2_m = ROOT.RooRealVar( 'atlas_order2_muA'+year+'_all_atlas', "power2", 9 ,     -100,   100)
        #atlas_order3_m = ROOT.RooRealVar( 'atlas_order3_muA'+year+'_all_atlas', "power3", 1 ,       -100,    100)
        #atlas_order4_e = ROOT.RooRealVar( 'atlas_order4_elA'+year+'_all_atlas', "power4", 1 ,       -100,    100)
        #atlas_order4_m = ROOT.RooRealVar( 'atlas_order4_muA'+year+'_all_atlas', "power4", 1 ,       -100,    100)

        atlas_order1_e = ROOT.RooRealVar( 'atlas_order1_A'+year+'_all_atlas', "power1", 0 ,      -100,  100)
        atlas_order2_e = ROOT.RooRealVar( 'atlas_order2_A'+year+'_all_atlas', "power2", 9 ,     -100,   100)
        atlas_order3_e = ROOT.RooRealVar( 'atlas_order3_A'+year+'_all_atlas', "power3", 1 ,       -100,    100)
        atlas_order1_m = ROOT.RooRealVar( 'atlas_order1_A'+year+'_all_atlas', "power1", 0 ,      -100,  100)
        atlas_order2_m = ROOT.RooRealVar( 'atlas_order2_A'+year+'_all_atlas', "power2", 9 ,     -100,   100)
        atlas_order3_m = ROOT.RooRealVar( 'atlas_order3_A'+year+'_all_atlas', "power3", 1 ,       -100,    100)

        integral_atl_e = ROOT.RooRealVar('%s_norm' %( 'atlas_elA'+year+'_all_atlas' ),
                            'normalization', ne )
        integral_atl_m = ROOT.RooRealVar('%s_norm' %( 'atlas_muA'+year+'_all_atlas' ),
                            'normalization', nm )

        function = 'TMath::Power( (1-TMath::Power(@0/13000., 1./3)), @1 ) / ( TMath::Power( @0/13000. , @2+ %s ))'
        order_entries = []
        for i in range( 0, 1 ) :
            order_entries.append( '@%d*TMath::Power' %(i+3)+
                                  '(TMath::Log10( @0/13000.),%d)'  %(i+1 ) )
        function = function % (' + '.join( order_entries ))
        #function = 'TMath::Power( (1-TMath::Power(@0/13000., 1./3)), @1 ) / ( TMath::Power( @0/13000. , @2))'
        func_atl_m = ROOT.RooGenericPdf( '%s_%s'%(func_name, 'muA'+year+'_all_atlas'), '%s_%s'%(func_name, 'muA'+year+'_all_atlas'), function, ROOT.RooArgList(mt_res, atlas_order1_m, atlas_order2_m, atlas_order3_m))
        func_atl_e = ROOT.RooGenericPdf( '%s_%s'%(func_name, 'elA'+year+'_all_atlas'), '%s_%s'%(func_name, 'elA'+year+'_all_atlas'), function, ROOT.RooArgList(mt_res, atlas_order1_e, atlas_order2_e, atlas_order3_e))
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
        #import_workspace( ws_out, atlas_order4_e)
        #import_workspace( ws_out, atlas_order4_m)
        import_workspace( ws_out, func_atl_e)
        import_workspace( ws_out, func_atl_m)
        import_workspace( ws_out, integral_atl_e )
        import_workspace( ws_out, integral_atl_m )

    #mypdfse = ROOT.RooArgList("store")
    #mypdfse.add(func_vvdi_e)
    #mypdfse.add(func_atl_e)
    #mypdfse.add(func_pdf_e)
    #catIndexe = ROOT.RooCategory('pdf_index_A'+year,'c')
    #catIndexe.setIndex(1)
    #pdfe = RooMultiPdf('MultiPdf_elA'+year+'_all_MultiPdf',"All Pdfs e",catIndexe,mypdfse)
    #import_workspace( ws_out, catIndexe )
    ##import_workspace( ws_out, mypdfse )
    #getattr( ws_out , "import")( pdfe, ROOT.RooFit.RecycleConflictNodes() )

    #mypdfsm = ROOT.RooArgList("store")
    #mypdfsm.add(func_vvdi_m)
    #mypdfsm.add(func_atl_m)
    #mypdfsm.add(func_pdf_m)
    ##catIndexm = ROOT.RooCategory('pdf_index_muA'+year,'c')
    #pdfm = RooMultiPdf('MultiPdf_muA'+year+'_all_MultiPdf',"All Pdfs m",catIndexe,mypdfsm)
    ##import_workspace( ws_out, catIndexm )
    ##import_workspace( ws_out, mypdfsm )
    #getattr( ws_out , "import")(pdfm, ROOT.RooFit.RecycleConflictNodes() )
    ws_out.writeToFile( rootfilename )


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
        htmp.SetFillColor(ROOT.kOrange)
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
    rootfilename = 'data/higgs/Width5/all/Mass%s/higgsCombine.saturated.GoodnessOfFit.mH120.root'%(mass)
    #rootfilename = 'data/higgs/Width5/%s%s/Mass%s/higgsCombine.saturated.GoodnessOfFit.mH120.root' %( ch,year ,mass)
    ifile = ROOT.TFile.Open( rootfilename, 'READ' )
    tree = ifile.Get( 'limit' )
    for e in tree:
        print e.limit
        datalimit =  e.limit
    #rootfilename = 'data/higgs/Width5/%s%s/Mass%s/higgsCombine.saturated.GoodnessOfFit.mH120.1234.root' %( ch,year ,mass)
    rootfilename = 'data/higgs/Width5/all/Mass%s/higgsCombine.saturated.GoodnessOfFit.mH120.1234.root'%(mass)
    ifile = ROOT.TFile.Open( rootfilename, 'READ' )
    tree = ifile.Get( 'limit' )
    tree.Show(0)
    hlimit = ROOT.TH1D("hlimit", "Goodness of Fit (%s %s);limit;"%(ch,year), 60, 0, 600);
    tree.Draw("limit>>hlimit")
    hlimit.SetLineColor(ROOT.kRed)
    ln = ROOT.TLine(datalimit, 0, datalimit, 0.9*hlimit.GetMaximum())
    ln.SetLineStyle(10)
    ln.SetLineWidth(3)
    tot = 0
    for i in range(1,hlimit.GetNbinsX()):
        if hlimit.GetBinCenter(i)<=datalimit:
            tot+=hlimit.GetBinContent(i)
        else:
            break
    print(1-tot/500.0)
    hlimit.Draw("HIST")
    ln.Draw("same")

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
    #rsignal = {
    #         '0' : (0, 0, 5)
    #        '0.1': (0.1, -2,2),
    #        '1': (1, -2,2),
    #        '10': (10, -2,2),
    #        '50': (50, -2,2),
    #        '100': (100, -2,2),
    #}
    rsignalr = [ '10']#,'10','50', '100']

    mean_collection = {}
    sigma_collection = {}
    mean_collection_e = {}
    sigma_collection_e = {}
    masslist = [2000]
    #masslist    = [300, 350, 400, 450, 700, 800, 900, 1000, 1200, 1400, 1600, 1800, 2000]
    masslist    = [300, 350, 400,450, 600, 700, 800,900, 1000, 1200, 1400, 1600, 1800, 2000]
    widlist = ['0p01']
    colorb = [ROOT.kRed,ROOT.kBlue,ROOT.kGreen,ROOT.kCyan,ROOT.kOrange,ROOT.kPink,ROOT.kGray]
    for wid in widlist:
        for im in masslist:
            for ir in rsignalr:
                c = ROOT.TCanvas()
                ROOT.gStyle.SetOptStat(0)
                #filename = 'higgs_atlas2_atlas_r'+ir
                #filename = 'higgs_expow2_expow_r'+ir
                #filename = 'higgs_dijet2_dijet_r'+ir
                #filename = 'higgs_dijet2_atlas_r'+ir
                #filename = 'higgs_dijet2_expow_r'+ir
                #filename = 'higgs_atlas2_expow_r'+ir
                #filename = 'higgs_expow2_atlas_r'+ir
                #filename = 'higgs_atlas2_dijet_r'+ir
                #filename = 'higgs_atlas2_vvdijet_r'+ir
                #filename = 'higgs_dijet2_vvdijet_r'+ir
                #filename = 'higgs_vvdijet2_dijet_r'+ir
                #filename = 'higgs_vvdijet2_atlas_r'+ir
                #filename = 'higgs_narrow_vvdijet2_dijet_r'+ir
                #filename = 'higgs_narrow_dijet2_vvdijet_r'+ir
                #filename = 'higgs_narrow_dijet2_atlas_r'+ir
                #filename = 'higgs_narrow_atlas2_dijet_r'+ir
                filename = 'higgs_narrow_atlas2_vvdijet_r'+ir
                #filename = 'higgs_vvdijet2_vvdijet_r'+ir
                #rootfilename = 'data/'+filename+'/Width%s/all/Mass%s/higgsCombine.Test.MultiDimFit.mH125.123456.root'%(wid,str(im))
                #rootfilename = 'data/'+filename+'/Width%s/all/Mass%s/fitDiagnostics.Test.root'%(wid,str(im))
                #ifile['r'+ir+'W'+wid+'m'+str(im)] = ROOT.TFile.Open( rootfilename, 'READ' )
                #tree = ifile['r'+ir+'W'+wid+'m'+str(im)].Get( 'limit' )
                #tree = ifile['r'+ir+'W'+wid+'m'+str(im)].Get( 'tree_fit_sb' )
                #hlimit = ROOT.TH1D("hlimit", "Bias Study (Width=%s Mass%s);(r - r_{inject})/#sigma_{r};"%(wid,str(im)), 80, rsignal[ir][1],rsignal[ir][2]);
                tree = ROOT.TChain("tree_fit_sb")
                #tree.Add('data/'+filename+'/Width%s/all/Mass%s/fitDiagnostics*.root'%(wid,str(im)))
                tree.Add('data_1015_afterbias_study/'+filename+'/Width%s/all/Mass%s/fitDiagnostics*.root'%(wid,str(im)))
                #hlimit = ROOT.TH1D("hlimit", "Bias Study (Width=%s Mass%s);(r - r_{inject})/#sigma_{r};"%(wid,str(im)), 80, -5,5);
                hlimit = ROOT.TH1D("hlimit", "Bias Study (Width=%s Mass%s);(r - r_{inject})/#sigma_{r};"%(wid,str(im)), 60, -3,3);
                #hlimit = ROOT.TH1D("hlimit", "Bias Study (Width=%s Mass%s);(r - r_{inject})/#sigma_{r};"%(wid,str(im)), 60, 0,3);
                #tree.Draw("r>>hlimit","r!=0")
                tree.Draw("(r-%s)/rErr>>hlimit"%(ir),"fit_status==0")
                hlimit.SetLineColor(ROOT.kRed)
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
                leg = ROOT.TLegend(0.21,0.6,0.35,0.85);
                leg.SetBorderSize(0);
                leg.SetLineStyle(1);
                leg.SetLineWidth(2);
                entry=leg.AddEntry('r'+ir+'W'+wid+'m'+str(im),"toy-data","l");
                entry.SetFillStyle(1001);
                entry.SetLineStyle(1);
                entry.SetLineWidth(3);
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
                c.SaveAs('gr_bias_Width'+wid+'_Mass'+str(im)+'_r'+ir+".C")
                c.SaveAs('gr_bias_Width'+wid+'_Mass'+str(im)+'_r'+ir+".png")
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



skimtree   =  "outputTree"
skimfile     =  "skim_1in5.root"
skimfile     =  "skim.root"

for year in ['2016','2017','2018']:
    #goodnessOfFit(year,data_outDir,skimtree,skimfile)
    prepareWS(year,data_outDir,skimtree,skimfile)
    #for ch in ['el','mu']:
    #    CombineGoF(ch, year)
    #    prepare_data(5, year, ch, skimtree, data_outDir+'/'+ch+year+'_'+skimfile)

#testBias()
#pltToyFit()


