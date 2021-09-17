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
            FileMap[year+ch] = glob.glob('/data/users/yihuilai/Resonances'+year+'/LepGamma_elg_'+Date+'/WithSF2/SingleElectron/Job*/tree.root')
            if(year=='2018'): FileMap[year+ch] = glob.glob('/data/users/yihuilai/Resonances'+year+'/LepGamma_elg_'+Date+'/WithSF2/EGamma/Job*/tree.root')
        if ch == 'mu':
            FileMap[year+ch] = glob.glob('/data/users/yihuilai/Resonances'+year+'/LepGamma_mug_'+Date+'/WithSF2/SingleMuon/Job*/tree.root')
            
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
    #dijet_elA2016_all_dijet_norm,dijet_muA2016_all_dijet_norm
    ne = dse.sumEntries("mt_res>200")
    nm = dsm.sumEntries("mt_res>200")
    
    integral_var_e = ROOT.RooRealVar('%s_norm' %( 'dijet_elA'+year+'_all_dijet' ),
                        'normalization', ne )
    integral_var_m = ROOT.RooRealVar('%s_norm' %( 'dijet_muA'+year+'_all_dijet' ),
                        'normalization', nm )
    #dijet_order1_elA2016_all_dijet,dijet_order1_muA2016_all_dijet,dijet_order2_elA2016_all_dijet,dijet_order2_muA2016_all_dijet
    dijet_order1_e = ROOT.RooRealVar('dijet_order1_elA'+year+'_all_dijet', "power1", -9, -50.0, 0)
    dijet_order1_m = ROOT.RooRealVar('dijet_order1_muA'+year+'_all_dijet', "power1", -9, -50.0, 0)
    dijet_order2_e = ROOT.RooRealVar('dijet_order2_elA'+year+'_all_dijet', "power2", -1.5, -10.0, 0)
    dijet_order2_m = ROOT.RooRealVar('dijet_order2_muA'+year+'_all_dijet', "power2", -1.5, -10.0, 0)

    #dijet_order3_e = ROOT.RooRealVar('dijet_order3_elA'+year+'_all_dijet', "power3", -1.5, -100.0, 0)
    #dijet_order3_m = ROOT.RooRealVar('dijet_order3_muA'+year+'_all_dijet', "power3", -1.5, -100.0, 0)

    #dijet_order3_e = ROOT.RooRealVar('dijet_order3_elA'+year+'_all_dijet', "power3", 1.5, -10.0, 10)
    #dijet_order3_m = ROOT.RooRealVar('dijet_order3_muA'+year+'_all_dijet', "power3", 1.5, -10.0, 10)

    #p.d.f
    function = ''
    func_name = 'dijet'
    if func_name == 'dijet' :
        order_entries = []
        log_str = 'TMath::Log10(@0/13000)'
        for i in range( 1, 2) :
            order_entries.append('@'+str(i+1)+'*' + '*'.join( [log_str]*i))
        function = 'TMath::Power( @0/13000., @1 + ' + '+'.join( order_entries) + ')'
        #print "function: ", function
        #function = 'TMath::Power( @0/13000., @1 + @2*TMath::Log10(@0/13000)*(1+@3*TMath::Log10(@0/13000)))'
        func_pdf_e = ROOT.RooGenericPdf( '%s_%s'%(func_name, 'elA'+year+'_all_dijet'), func_name, function, ROOT.RooArgList(mt_res,dijet_order1_e,dijet_order2_e))
        func_pdf_m = ROOT.RooGenericPdf( '%s_%s'%(func_name, 'muA'+year+'_all_dijet'), func_name, function, ROOT.RooArgList(mt_res,dijet_order1_m,dijet_order2_m))
        #func_pdf_e = ROOT.RooGenericPdf( '%s_%s'%(func_name, 'elA'+year+'_all_dijet'), func_name, function, ROOT.RooArgList(mt_res,dijet_order1_e,dijet_order2_e, dijet_order3_e))
        #func_pdf_m = ROOT.RooGenericPdf( '%s_%s'%(func_name, 'muA'+year+'_all_dijet'), func_name, function, ROOT.RooArgList(mt_res,dijet_order1_m,dijet_order2_m, dijet_order3_m))

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
    #return 

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
        #input()
        c.SaveAs('fit_%s%s.png' %( year,ch))
        c.SaveAs('%s/%s/%s.C' %( data_outDir,year,ch))
        c.SaveAs('%s/%s/%s.root' %( data_outDir,year,ch))
        c.SaveAs('%s/%s/%s.png' %( data_outDir,year,ch))
        
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
    #import_workspace( ws_out, dijet_order3_e )
    #import_workspace( ws_out, dijet_order3_m )
    import_workspace( ws_out, func_pdf_e )
    import_workspace( ws_out, func_pdf_m )
    import_workspace( ws_out, integral_var_e )
    import_workspace( ws_out, integral_var_m )
    ws_out.writeToFile( rootfilename )


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



skimtree   =  "outputTree"
#skimfile     =  "skim_1in5.root"
skimfile     =  "skim.root"

for year in ['2016','2017','2018']:
    #goodnessOfFit(year,data_outDir,skimtree,skimfile)
    prepareWS(year,data_outDir,skimtree,skimfile)
    #for ch in ['el','mu']:
    #    CombineGoF(ch, year)
    #    prepare_data(1, year, ch, skimtree, data_outDir+'/'+ch+year+'_'+skimfile)







