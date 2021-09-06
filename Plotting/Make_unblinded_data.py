import ROOT
from array import array
#execfile("MakeBase.py")

MIN_ = 200
MAX_ = 2000
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
Date = '2021_08_27'
for year in ['2016','2017','2018']:
    for ch in ['el','mu']:
        if ch == 'el':
            FileMap[year+ch] = glob.glob('/data2/users/kakw/Resonances'+year+'/LepGamma_elg_'+Date+'/WithSF/SingleElectron/Job*/tree.root')
            if(year=='2018'): FileMap[year+ch] = glob.glob('/data2/users/kakw/Resonances'+year+'/LepGamma_elg_'+Date+'/WithSF/EGamma/Job*/tree.root')
        if ch == 'mu':
            FileMap[year+ch] = glob.glob('/data2/users/kakw/Resonances'+year+'/LepGamma_mug_'+Date+'/WithSF/SingleMuon/Job*/tree.root')
            
print('Loaded FileMap')

# ---------------------------------------------------

def import_workspace( ws , objects):
    """ import objects into workspace """

    if not isinstance( objects, list ):
        objects = [objects,]

    ## NOTE getattr is needed to escape python keyword import
    for o in objects:
        getattr( ws, "import") ( o )

# ---------------------------------------------------

def prepare_data(frac, year, ch, skimtree, skimfile):
    #Prepare skimed data
    names = ROOT.std.vector('string')()
    for n in FileMap[year+ch]: names.push_back(n)
    d = ROOT.RDataFrame(treeIn, names)
    #hardcoded selections
    if ch=='el':
        myfilter = d.Filter("el_n==1&& mu_n==0 && ph_n==1&&  fabs( el_eta[0] ) < 2.1&& el_pt[0] > 35  &&  el_passTight[0] == 1 && met_pt > 40 && fabs(m_lep_ph-91)>20.0 && jet_CSVMedium_n==0 && ph_IsEB[0] && ph_passTight[0] && ph_pt[0] > 0.50*mt_res - 40 && ph_pt[0] < 0.50*mt_res + 40&& !ph_hasPixSeed[0]").Range(0,0,frac)
    elif ch=='mu':
        myfilter = d.Filter("mu_n==1 && el_n==0 && ph_n==1 && met_pt > 40 && mu_pt_rc[0] > 35  && jet_CSVMedium_n==0 && ph_IsEB[0] && ph_passTight[0] && ph_pt[0] > 0.50*mt_res - 40 && ph_pt[0] < 0.50*mt_res + 40 && !ph_hasPixSeed[0]").Range(0,0,frac)
    else:
        print("use el or mu")
        exit()
    Hmt = myfilter.Histo1D("mt_res")
    Hmt.Draw()
    myfilter.Snapshot(skimtree, skimfile)

def prepareWS(year,baseDir,skimtree,skimfile):

    #prepare Working Space with Roofit
    #Readin Data
    mt_res = ROOT.RooRealVar("mt_res", "mt_res", 0, 2000);
    mt_res.setRange( MIN_ ,MAX_)
    F=ROOT.TFile(baseDir+'/el'+year+'_'+skimfile)
    tree=F.Get(skimtree)
    print('read ',baseDir+'/el'+year+'_'+skimfile)
    print('tot:',tree.GetEntries())
    dse = ROOT.RooDataSet('data_elA'+year+'_mt_res_base', "dse", ROOT.RooArgSet(mt_res), ROOT.RooFit.Import(tree));
    F=ROOT.TFile(baseDir+'/mu'+year+'_'+skimfile)
    tree=F.Get(skimtree)
    print('read ',baseDir+'/mu'+year+'_'+skimfile)
    print('tot:',tree.GetEntries())
    dsm = ROOT.RooDataSet('data_muA'+year+'_mt_res_base', "dsm", ROOT.RooArgSet(mt_res), ROOT.RooFit.Import(tree));
    #dijet_elA2016_all_dijet_norm,dijet_muA2016_all_dijet_norm
    ne = dse.sumEntries("mt_res>200")
    nm = dsm.sumEntries("mt_res>200")
    
    integral_var_e = ROOT.RooRealVar('%s_norm' %( 'dijet_elA'+year+'_all_dijet' ),
                        'normalization', ne )
    integral_var_m = ROOT.RooRealVar('%s_norm' %( 'dijet_muA'+year+'_all_dijet' ),
                        'normalization', nm )
    #dijet_order1_elA2016_all_dijet,dijet_order1_muA2016_all_dijet,dijet_order2_elA2016_all_dijet,dijet_order2_muA2016_all_dijet
    dijet_order1_e = ROOT.RooRealVar('dijet_order1_elA'+year+'_all_dijet', "power1", -9.1155748, -50.0, 0.0)
    dijet_order1_m = ROOT.RooRealVar('dijet_order1_muA'+year+'_all_dijet', "power1", -9, -50.0, 0.0)
    dijet_order2_e = ROOT.RooRealVar('dijet_order2_elA'+year+'_all_dijet', "power2", -1.4998414, -10.0, 0.0)
    dijet_order2_m = ROOT.RooRealVar('dijet_order2_muA'+year+'_all_dijet', "power2", -1, -10.0, 0.0)
    #p.d.f
    function = ''
    func_name = 'dijet'
    if func_name == 'dijet' :
        order_entries = []
        log_str = 'TMath::Log10(@0/13000)'
        for i in range( 1, 2) :
            order_entries.append('@'+str(i+1)+'*' + '*'.join( [log_str]*i))
        function = 'TMath::Power( @0/13000., @1 + ' + '+'.join( order_entries) + ')'
        print "function: ", function
        func_pdf_e = ROOT.RooGenericPdf( '%s_%s'%(func_name, 'elA'+year+'_all_dijet'), func_name, function, ROOT.RooArgList(mt_res,dijet_order1_e,dijet_order2_e))
        func_pdf_m = ROOT.RooGenericPdf( '%s_%s'%(func_name, 'muA'+year+'_all_dijet'), func_name, function, ROOT.RooArgList(mt_res,dijet_order1_m,dijet_order2_m))
    #Fit to model
    resu_e = func_pdf_e.fitTo(dse,ROOT.RooFit.Save(),ROOT.RooFit.SumW2Error(ROOT.kTRUE))
    resu_m = func_pdf_m.fitTo(dsm,ROOT.RooFit.Save(),ROOT.RooFit.SumW2Error(ROOT.kTRUE))
    frame_e = mt_res.frame(ROOT.RooFit.Title("Unbinned ML fit, el"))
    frame_m = mt_res.frame(ROOT.RooFit.Title("Unbinned ML fit, mu"))
    dse.plotOn(frame_e,ROOT.RooFit.DataError(ROOT.RooAbsData.SumW2)) ;
    func_pdf_e.plotOn(frame_e)
    dsm.plotOn(frame_m,ROOT.RooFit.DataError(ROOT.RooAbsData.SumW2)) ;
    func_pdf_m.plotOn(frame_m)
    print("===> fit result")
    resu_e.Print()
    print("===> fit result")
    resu_m.Print()
    c = ROOT.TCanvas("c","c",600,600) ;
    ROOT.gPad.SetLeftMargin(0.15)
    frame_e.GetYaxis().SetTitleOffset(1.8)
    ROOT.gPad.SetLogy()
    frame_e.Draw()
    c.SaveAs('%s/%s/el.C' %( data_outDir,year))
    c.SaveAs('%s/%s/el.root' %( data_outDir,year))
    c.SaveAs('%s/%s/el.png' %( data_outDir,year))
    c = ROOT.TCanvas("c","c",600,600) ;
    ROOT.gPad.SetLeftMargin(0.15)
    ROOT.gPad.SetLogy()
    frame_m.GetYaxis().SetTitleOffset(1.8)
    frame_m.Draw()
    c.SaveAs('%s/%s/mu.C' %( data_outDir,year))
    c.SaveAs('%s/%s/mu.root' %( data_outDir,year))
    c.SaveAs('%s/%s/mu.png' %( data_outDir,year))
    #Work space
    ws_out  = ROOT.RooWorkspace( "workspace_all" )
    rootfilename = '%s/%s/%s.root' %( data_outDir,year,ws_out.GetName() )
    import_workspace( ws_out, mt_res)
    import_workspace( ws_out, dse)
    import_workspace( ws_out, dsm)
    import_workspace( ws_out, dijet_order1_e )
    import_workspace( ws_out, dijet_order1_m )
    import_workspace( ws_out, dijet_order2_e )
    import_workspace( ws_out, dijet_order2_m )
    import_workspace( ws_out, func_pdf_e )
    import_workspace( ws_out, func_pdf_m )
    import_workspace( ws_out, integral_var_e )
    import_workspace( ws_out, integral_var_m )
    ws_out.writeToFile( rootfilename )


def foodnessOfFit(year,baseDir,skimtree,skimfile):

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
   



skimtree   =  "outputTree"
skimfile     =  "skim.root"

for year in ['2018']:#,'2017','2018']:
    foodnessOfFit(year,data_outDir,skimtree,skimfile)
    #prepareWS(year,data_outDir,skimtree,skimfile)
    #for ch in ['el','mu']:
        #prepare_data(1, year, ch, skimtree, data_outDir+'/'+ch+year+'_'+skimfile)







