import ROOT
from ROOT import gROOT, gSystem, RooIntegralMorph
from ROOT import RooRealVar, RooDataHist,RooAbsReal
from ROOT import RooFit as rf
from uncertainties import ufloat
import uuid
import re
import random
import sys
from collections import namedtuple, OrderedDict
from functools import wraps
from DrawConfig import DrawConfig
gSystem.Load("My_double_CB/RooDoubleCB_cc.so")
from ROOT import gPad, RooFit, kRed, kBlue, kViolet, kRainBow
import analysis_utils
import json

def addparser(parser):
    parser.add_argument( '--fitSignal',        action='store_true', help='Fit signal samples, generate files for fully para model' )
    parser.add_argument( '--makeWS',        action='store_true', help='makeWS' )
    parser.add_argument( '--makeplots',        action='store_true', help='makeplots' )
execfile("MakeBase.py")

inputDir = "/data/users/yihuilai/WG_Analysis/Plotting/WG_Analysis/Plotting/data_1015_afterbias_study/sigfit/2018/"
outputDir = "./"
_XSFILE   = 'cross_sections/photon16_smallsig.py'

_LUMI16   = 36000
_LUMI17   = 41000
_LUMI18   = 59740

# make parametrized signal model

_JSONLOC = "data_1015_afterbias_study/para.txt"
_JSONLOC_Fit = "data_1015_afterbias_study/para_fit.txt"
plot_outDir = "plots/MakeSignalWS_para"
data_outDir = "data_1015_afterbias_study/sigfit_para"
if plot_outDir is not None :
    if not os.path.isdir( plot_outDir ) :
        os.makedirs( plot_outDir )
if data_outDir is not None :
    if not os.path.isdir( data_outDir ) :
        os.makedirs( data_outDir )
        os.makedirs( data_outDir+'/2016' )
        os.makedirs( data_outDir+'/2017' )
        os.makedirs( data_outDir+'/2018' )

global lumi
def lumi(ibin):
    year = ibin['year']
    if year == 2016: return _LUMI16
    if year == 2017: return _LUMI17
    if year == 2018: return _LUMI18
    raise RuntimeError



# ---------------------------------------------------

def multidict_tojson(filepath, indict):
    ## expand into multidimensional dictionary
    with open(filepath, "w") as fo:
        json.dump( indict, fo)
        print "save to %s" %filepath

def import_workspace( ws , objects):
    """ import objects into workspace """

    if not isinstance( objects, list ):
        objects = [objects,]

    ## NOTE getattr is needed to escape python keyword import
    for o in objects:
        getattr( ws, "import") ( o )

# ---------------------------------------------------

def make_parametrized_signal_model( ):

    signal_widths    = ['5', '0p01']
    signal_masses    = [300, 350, 400, 450, 600, 700, 800, 900, 1000, 1200, 1400, 1600, 1800, 2000]
    Years= ['2016','2017','2018']
    CH = ['el','mu']

    weightMap,_ = analysis_utils.read_xsfile( _XSFILE, 1, print_values=True )
    sampManElG = SampleManager( options.baseDirElG, _TREENAME, filename=_FILENAME, lumi=-1)
    sampManElG.ReadSamples( _SAMPCONF )

    #Read parameters from Signal WS
    paramname = ['cb_mass_MG_Mass_Width_CHYEAR','cb_sigma_MG_Mass_Width_CHYEAR','cb_cut1_MG_Mass_Width_CHYEAR','cb_power1_MG_Mass_Width_CHYEAR','cb_cut2_MG_Mass_Width_CHYEAR','cb_power2_MG_Mass_Width_CHYEAR', 'cb_MG_Mass_Width_CHYEAR_norm']
    sighists={}
    sigModel={}
    ct=0
    leg1 = ROOT.TLegend(0.55,0.73,0.8,0.87)
    leg1.SetFillColor(ROOT.kWhite)
    leg1.SetLineColor(ROOT.kWhite)
    leg2 = ROOT.TLegend(0.65,0.73,0.86,0.87)
    leg2.SetFillColor(ROOT.kWhite)
    leg2.SetLineColor(ROOT.kWhite)
    inputdir = "data"
    from array import array
    xx={}
    yy={}
    parlist={}
    parlists = recdd()
    for ipar in paramname:
        for wid in signal_widths:
            for iyear in Years:
                for ich in CH:
                    grname = ipar.replace("YEAR",str(iyear))
                    grname = grname.replace("Width",'W'+str(wid))
                    grname = grname.replace("CH",ich)
                    parlist[grname],parlist[grname+'mass'] = array( 'd' ),array( 'd' )
                    for mass in signal_masses:
                        wsname = 'wssignal_M%s_W%s_%s' %(str(mass),wid,ich)
                        pdfname = 'cb_MG_M%s_W%s_%s%s' %(str(mass),wid,ich,iyear)
                        dataname = 'MG_M%s_W%s_%s%sdatahist' %(str(mass),wid,ich,iyear)
                        inputDir = inputdir+"/sigfit/%s/" % (iyear)
                        ifile = ROOT.TFile.Open( inputDir+wsname+'.root', 'READ' )
                        ws_in = ifile.Get( wsname )
                        #Do fitting, ignore poor fitting points
                        frame = (ws_in.var("mt_res")).frame()
                        data = ws_in.data(dataname)
                        model = ws_in.pdf(pdfname)
                        data.plotOn(frame)
                        model.plotOn(frame)
                        ##frame.Draw()
                        model.fitTo(data)
                        print('----------frame.chiSquare ',frame.chiSquare())
                        if(frame.chiSquare()>10): continue
                        if('norm' in ipar):
                            (parlist[grname]).append( ws_in.var(grname.replace("Mass",'M'+str(mass))).getVal())
                            parlists[grname][mass] = ws_in.var(grname.replace("Mass",'M'+str(mass))).getVal()
                        else:
                            (parlist[grname]).append( ws_in.var(grname.replace("Mass",'M'+str(mass))).getVal() )
                            parlists[grname][mass] = ws_in.var(grname.replace("Mass",'M'+str(mass))).getVal()
                        parlist[grname+'mass'].append(mass)
    #Finish reading
    #store param
    multidict_tojson(_JSONLOC, parlists )
# ---------------------------------------------------
    #Decide to do fitting 
    parlists_fit = recdd()
    paramname = ['cb_cut1_MG_Mass_Width_CHYEAR']
    paramname = ['cb_sigma_MG_Mass_Width_CHYEAR','cb_mass_MG_Mass_Width_CHYEAR','cb_cut1_MG_Mass_Width_CHYEAR','cb_MG_Mass_Width_CHYEAR_norm']
    for ipar in paramname:
        cpara=ROOT.TCanvas()
        gr= {}
        leg1 = ROOT.TLegend(0.25,0.33,0.8,0.87)
        leg1.SetFillColor(ROOT.kWhite)
        leg1.SetLineColor(ROOT.kWhite)
        ct=-1
        grsum=ROOT.TMultiGraph()
        if(True):
            for wid in signal_widths:
                for iyear in Years:
                    for ich in CH:
                        ct+=1
                        grname = ipar.replace("YEAR",str(iyear))
                        grname = grname.replace("Width",'W'+str(wid))
                        grname = grname.replace("CH",ich)
                        gr[grname] = ROOT.TGraph( len(parlist[grname+'mass']), parlist[grname+'mass'], parlist[grname] )
                        (gr[grname]).SetLineColor( kRainBow + ct*3 )
                        (gr[grname]).SetLineWidth( 3 )
                        (gr[grname]).SetMarkerColor( kRainBow + ct*3 )
                        (gr[grname]).SetMarkerStyle( 21 )
                        (gr[grname]).GetXaxis().SetTitle( 'X title' )
                        (gr[grname]).GetYaxis().SetTitle( 'Y title' )
                        if 'norm' in ipar:
                            a= ROOT.TF1("a","[0] - [1]*TMath::Exp(-x/[2])",0,2500);
                            a.SetParameters(0.1, 0.05, 1000)
                            gr[grname].Fit("a")
                            parlists_fit[grname]['func'] = 'expnorm'
                            parlists_fit[grname][0] = a.GetParameter(0)
                            parlists_fit[grname][1] = a.GetParameter(1)
                            parlists_fit[grname][2] = a.GetParameter(2)
                            parlists_fit[grname+'err'][0] = a.GetParError(0)
                            parlists_fit[grname+'err'][1] = a.GetParError(1)
                            parlists_fit[grname+'err'][2] = a.GetParError(2)
                        elif 'cut1' in ipar:
                           # a= ROOT.TF1("a","[0] + [1]*TMath::Exp(-x/[2])",0,2500);
                           # if wid == '5':
                           #     a.SetParameters(0.37, 3, 239)
                           # if wid == '0p01':
                           #     a.SetParameters(0.3, 9, 137)
                           # gr[grname].Fit("a","R")
                           # parlists_fit[grname]['func'] = 'expcut1'
                           # parlists_fit[grname][0] = a.GetParameter(0)
                           # parlists_fit[grname][1] = a.GetParameter(1)
                           # parlists_fit[grname][2] = a.GetParameter(2)
                           # parlists_fit[grname+'err'][0] = a.GetParError(0)
                           # parlists_fit[grname+'err'][1] = a.GetParError(1)
                           # parlists_fit[grname+'err'][2] = a.GetParError(2)
                            a= ROOT.TF1("a","[0] + [1]/(x-[2])",0,2500);
                            if wid == '5':
                                a.SetParameters(0.263351,153.581,151.212)
                            if wid == '0p01':
                                a.SetParameters(0.174413,106.189,210.706)
                            gr[grname].Fit("a","R")
                            parlists_fit[grname]['func'] = 'inv'
                            parlists_fit[grname][0] = a.GetParameter(0)
                            parlists_fit[grname][1] = a.GetParameter(1)
                            parlists_fit[grname][2] = a.GetParameter(2)
                            parlists_fit[grname+'err'][0] = a.GetParError(0)
                            parlists_fit[grname+'err'][1] = a.GetParError(1)
                            parlists_fit[grname+'err'][2] = a.GetParError(2)

                        elif 'sigma' in ipar or 'cb_mass_MG' in ipar:
                            gr[grname].Fit("pol1")
                            print(wid, iyear, ich)
                            a=gr[grname].GetFunction("pol1")
                            print(a.GetNumberFreeParameters(), " free parameters")
                            print(a.GetParameter(0),a.GetParameter(1))
                            parlists_fit[grname]['func'] = 'pol1'
                            parlists_fit[grname][0] = a.GetParameter(0)
                            parlists_fit[grname][1] = a.GetParameter(1)
                            parlists_fit[grname+'err'][0] = a.GetParError(0)
                            parlists_fit[grname+'err'][1] = a.GetParError(1)
                        else:
                            gr[grname].Fit("pol2")
                            print(wid, iyear, ich)
                            a=gr[grname].GetFunction("pol2")
                            print(a.GetNumberFreeParameters(), " free parameters")
                            print(a.GetParameter(0),a.GetParameter(1),a.GetParameter(2))
                            parlists_fit[grname]['func'] = 'pol2'
                            parlists_fit[grname][0] = a.GetParameter(0)
                            parlists_fit[grname][1] = a.GetParameter(1)
                            parlists_fit[grname][2] = a.GetParameter(2)
                            parlists_fit[grname+'err'][0] = a.GetParError(0)
                            parlists_fit[grname+'err'][1] = a.GetParError(1)
                            parlists_fit[grname+'err'][2] = a.GetParError(2)
                        gr[grname].Draw( 'ACP' )
                        a.SetLineColor( kRainBow + ct*3 )
                        grsum.Add(gr[grname])
                        entry = leg1.AddEntry(gr[grname],grname,"L")
                        entry.SetFillStyle(1001)
                        entry.SetLineStyle(1)
                        entry.SetLineWidth(1)
                        entry.SetTextFont(42)
                        entry.SetTextSize(0.04)
                        entry.SetLineColor(kRainBow+ct*3)
            grsum.Draw("ACP")
            grsum.GetXaxis().SetTitle( 'm_{reso} (GeV)' )
            grsum.GetYaxis().SetTitle( ipar )
            leg1.Draw()
            cpara.SaveAs("gr"+ipar+".C")
            input("")
    multidict_tojson(_JSONLOC_Fit, parlists_fit )

#-------------------------------------------------

def prepare_signal_functions_helper( mass, width,  iyear, ich , Use_scaleError=False) :

    sigpar = "_".join(['M'+str(mass), 'W'+str(width), '%s_%s' %( ich,str(iyear) )])
    inpar = "_".join(['M'+str(mass), 'W'+str(width), ich])

    fname= 'data_1015_afterbias_study/sigfit/%i/ws%s_%s.root' %( iyear, 'signal', inpar )
    wsname = "wssignal" + '_' + inpar
    print fname, " : ", wsname
    ifile = ROOT.TFile.Open( fname, 'READ' )
    if not ifile:
        return
    ws_in = ifile.Get( wsname )

    pdfname = 'cb_MG_M%s_W%s_%s%s' %(str(mass),width,ich,iyear)
    dataname = 'MG_M%s_W%s_%s%sdatahist' %(str(mass),width,ich,iyear)
    sighists = ws_in.data(dataname)
    sigModel = ws_in.pdf(pdfname)
    print pdfname, " ; ", dataname

    #create new WS
    ws_out = ROOT.RooWorkspace( "wssignal_M%s_W%s_%s"%(str(mass),width,ich) )

    f = open (_JSONLOC_Fit, "r")
    sigfitparams = json.loads(f.read())
    paramname = ['cb_sigma_MG_Mass_Width_CHYEAR','cb_mass_MG_Mass_Width_CHYEAR','cb_cut1_MG_Mass_Width_CHYEAR','cb_MG_Mass_Width_CHYEAR_norm']
    Allparamname = ['cb_mass_MG_Mass_Width_CHYEAR','cb_sigma_MG_Mass_Width_CHYEAR','cb_cut1_MG_Mass_Width_CHYEAR','cb_power1_MG_Mass_Width_CHYEAR','cb_cut2_MG_Mass_Width_CHYEAR','cb_power2_MG_Mass_Width_CHYEAR', 'cb_MG_Mass_Width_CHYEAR_norm']
    #Get parameter value
    for ipar in Allparamname:
        print(ipar)
        iipar = ipar.replace("YEAR",str(iyear))
        iipar = iipar.replace("CH",str(ich))
        iipar = iipar.replace("idth",str(width))
        if ipar not in paramname:
            var = ws_in.var( iipar.replace("Mass",'M'+str(mass)) )
            import_workspace( ws_out, var)
        else:
            var = ws_in.var( iipar.replace("Mass",'M'+str(mass)) )
            if sigfitparams[iipar]['func'] == 'expnorm':
                func = ROOT.TF1('func', '[0] - [1]*TMath::Exp(-x/[2])', 0, 3000)
                func.SetParameters(sigfitparams[iipar]['0'],sigfitparams[iipar]['1'],sigfitparams[iipar]['2'])
            elif sigfitparams[iipar]['func'] == 'expcut1':
                func = ROOT.TF1('func', '[0] + [1]*TMath::Exp(-x/[2])', 0, 3000)
                func.SetParameters(sigfitparams[iipar]['0'],sigfitparams[iipar]['1'],sigfitparams[iipar]['2'])
            elif sigfitparams[iipar]['func'] == 'inv':
                func = ROOT.TF1('func', "[0] + [1]/(x-[2])", 0, 3000)
                func.SetParameters(sigfitparams[iipar]['0'],sigfitparams[iipar]['1'],sigfitparams[iipar]['2'])
            elif sigfitparams[iipar]['func'] == 'pol1':
                func = ROOT.TF1('func', 'pol1', 0, 3000)
                func.SetParameters(sigfitparams[iipar]['0'],sigfitparams[iipar]['1'])
            else:
                func = ROOT.TF1('func', 'pol2', 0, 3000)
                func.SetParameters(sigfitparams[iipar]['0'],sigfitparams[iipar]['1'],sigfitparams[iipar]['2'])
            print("set ",var.getVal()," to ", func.Eval(int(mass)))
            print('original error, ', var.getError())
            if Use_scaleError:
                #scale original error
                #FIXME for wrong fittings, we can not rely on the original error
                var.setError( var.getError()*func.Eval(int(mass))/var.getVal() )
                var.setVal( func.Eval(int(mass)) )
            else:
                #Use new error from the fitting
                varmean = func.Eval(int(mass))
                if sigfitparams[iipar]['func'] == 'pol1':
                    func.SetParameters(sigfitparams[iipar]['0']+sigfitparams[iipar+'err']['0'],sigfitparams[iipar]['1']+sigfitparams[iipar+'err']['1'])
                    varup = func.Eval(int(mass))
                    func.SetParameters(sigfitparams[iipar]['0']-sigfitparams[iipar+'err']['0'],sigfitparams[iipar]['1']-sigfitparams[iipar+'err']['1'])
                    vardown = func.Eval(int(mass))
                else:
                    func.SetParameters(sigfitparams[iipar]['0']+sigfitparams[iipar+'err']['0'],sigfitparams[iipar]['1']+sigfitparams[iipar+'err']['1'],sigfitparams[iipar]['2']+sigfitparams[iipar+'err']['2'])
                    varup = func.Eval(int(mass))
                    func.SetParameters(sigfitparams[iipar]['0']-sigfitparams[iipar+'err']['0'],sigfitparams[iipar]['1']-sigfitparams[iipar+'err']['1'],sigfitparams[iipar]['2']-sigfitparams[iipar+'err']['2'])
                    vardown = func.Eval(int(mass))
                print('varup,',varup, 'vardown,',vardown,' new error',max(abs(varmean-varup),abs(varmean-vardown)) )
                var.setError( varmean*0.0001 )
                #var.setError( max(abs(varmean-varup),abs(varmean-vardown)) )
                var.setVal( varmean )
            import_workspace( ws_out, var)

    var = ws_in.var( "mt_res" )
    import_workspace( ws_out, var)
    pdffit = ws_in.pdf( pdfname )
    import_workspace( ws_out, pdffit )
    datafit = ws_in.data( dataname )
    import_workspace( ws_out, datafit )
    outputfile = '%s/%s/%s.root' %( data_outDir, str(iyear),ws_out.GetName() )
    ws_out.writeToFile( outputfile )
    ifile.Close()

def prepare_signal_functions_helper_extra( mass, width,  iyear, ich) :
    #Define parameters
    label = 'MG_Mass_Width_CHYEAR'
    label =label.replace("ass",str(mass))
    label =label.replace("CH",str(ich))
    label =label.replace("YEAR",str(iyear))
    label =label.replace("idth",str(width))
    cut1_vals   = (  0.3,       0.1,      2.0  )
    sigma_vals  = ( 28. ,       1. ,      200. ) if width==0.01 else ( 58. ,       1. ,      200.)
    power1_vals = (  2.0,       1.4,      6.  )
    mass_vals   = ( mass,  0.5*mass,  1.1*mass )
    cut2_vals   = (  1.5,       1.,       2.5  )
    power2_vals = (  4.0,       0.,       10.0  )
    cb_cut1   = ROOT.RooRealVar('cb_cut1_%s'   %label,   'Cut1'  ,
                               cut1_vals[0],   cut1_vals[1],   cut1_vals[2],   '')
    cb_sigma  = ROOT.RooRealVar('cb_sigma_%s'  %label,   'Width' ,
                               sigma_vals[0],  sigma_vals[1],  sigma_vals[2],  'GeV')
    cb_power1 = ROOT.RooRealVar('cb_power1_%s' %label,   'Power' ,
                               power1_vals[0], power1_vals[1], power1_vals[2], '')
    cb_m0     = ROOT.RooRealVar('cb_mass_%s'   %label,   'mass'  ,
                               mass_vals[0],   mass_vals[1],   mass_vals[2],   'GeV')
    cb_cut2   = ROOT.RooRealVar('cb_cut2_%s'   %label,   'Cut2'  ,
                               cut2_vals[0],   cut2_vals[1],   cut2_vals[2],   '')
    cb_power2 = ROOT.RooRealVar('cb_power2_%s' %label,   'Power' ,
                               power2_vals[0], power2_vals[1], power2_vals[2], '')
    # fix a few params in the signal fit
    cb_cut2.setConstant()
    cb_cut2.setError(0.0)
    cb_power2.setConstant()
    cb_power2.setError(0.0)
    cb_power1.setConstant()
    cb_power1.setError(0.0)

    #create new WS
    ws_out = ROOT.RooWorkspace( "wssignal_M%s_W%s_%s"%(str(mass),width,ich) )

    f = open (_JSONLOC_Fit, "r")
    sigfitparams = json.loads(f.read())
    paramname = ['cb_sigma_MG_Mass_Width_CHYEAR','cb_mass_MG_Mass_Width_CHYEAR','cb_cut1_MG_Mass_Width_CHYEAR','cb_MG_Mass_Width_CHYEAR_norm']
    Allparamname = ['cb_mass_MG_Mass_Width_CHYEAR','cb_sigma_MG_Mass_Width_CHYEAR','cb_cut1_MG_Mass_Width_CHYEAR','cb_power1_MG_Mass_Width_CHYEAR','cb_cut2_MG_Mass_Width_CHYEAR','cb_power2_MG_Mass_Width_CHYEAR', 'cb_MG_Mass_Width_CHYEAR_norm']
    #Get parameter value
    for ipar in paramname:
        print(ipar)
        iipar = ipar.replace("YEAR",str(iyear))
        iipar = iipar.replace("CH",str(ich))
        iipar = iipar.replace("idth",str(width))

        if sigfitparams[iipar]['func'] == 'expnorm':
            func = ROOT.TF1('func', '[0] - [1]*TMath::Exp(-x/[2])', 0, 3000)
            func.SetParameters(sigfitparams[iipar]['0'],sigfitparams[iipar]['1'],sigfitparams[iipar]['2'])
        elif sigfitparams[iipar]['func'] == 'expcut1':
            func = ROOT.TF1('func', '[0] + [1]*TMath::Exp(-x/[2])', 0, 3000)
            func.SetParameters(sigfitparams[iipar]['0'],sigfitparams[iipar]['1'],sigfitparams[iipar]['2'])
        elif sigfitparams[iipar]['func'] == 'inv':
            func = ROOT.TF1('func', "[0] + [1]/(x-[2])", 0, 3000)
            func.SetParameters(sigfitparams[iipar]['0'],sigfitparams[iipar]['1'],sigfitparams[iipar]['2'])
        elif sigfitparams[iipar]['func'] == 'pol1':
            func = ROOT.TF1('func', 'pol1', 0, 3000)
            func.SetParameters(sigfitparams[iipar]['0'],sigfitparams[iipar]['1'])
        else:
            func = ROOT.TF1('func', 'pol2', 0, 3000)
            func.SetParameters(sigfitparams[iipar]['0'],sigfitparams[iipar]['1'],sigfitparams[iipar]['2'])
        varmean = func.Eval(int(mass))
        if sigfitparams[iipar]['func'] == 'pol1':
            func.SetParameters(sigfitparams[iipar]['0']+sigfitparams[iipar+'err']['0'],sigfitparams[iipar]['1']+sigfitparams[iipar+'err']['1'])
            varup = func.Eval(int(mass))
            func.SetParameters(sigfitparams[iipar]['0']-sigfitparams[iipar+'err']['0'],sigfitparams[iipar]['1']-sigfitparams[iipar+'err']['1'])
            vardown = func.Eval(int(mass))
        else:
            func.SetParameters(sigfitparams[iipar]['0']+sigfitparams[iipar+'err']['0'],sigfitparams[iipar]['1']+sigfitparams[iipar+'err']['1'],sigfitparams[iipar]['2']+sigfitparams[iipar+'err']['2'])
            varup = func.Eval(int(mass))
            func.SetParameters(sigfitparams[iipar]['0']-sigfitparams[iipar+'err']['0'],sigfitparams[iipar]['1']-sigfitparams[iipar+'err']['1'],sigfitparams[iipar]['2']-sigfitparams[iipar+'err']['2'])
            vardown = func.Eval(int(mass))
        print('varmean ', varmean, ' varup,',varup, 'vardown,',vardown,' new error',max(abs(varmean-varup),abs(varmean-vardown)) )
        if 'cut1' in iipar:
            cb_cut1.setError( max(abs(varmean-vardown), abs(varmean-varup)) )
            #cb_cut1.setAsymError( abs(varmean-vardown), abs(varmean-varup) )
            cb_cut1.setVal( varmean )
            import_workspace( ws_out, cb_cut1)
            print('varmean ', cb_cut1.getVal(), ' varup,',cb_cut1.getVal()+cb_cut1.getErrorHi(), 'vardown,',cb_cut1.getVal()-cb_cut1.getErrorLo())
        if 'sigma' in iipar:
            cb_sigma.setError( max(abs(varmean-vardown), abs(varmean-varup)) )
            #cb_sigma.setAsymError( abs(varmean-vardown), abs(varmean-varup) )
            cb_sigma.setVal( varmean )
            import_workspace( ws_out, cb_sigma)
            print('varmean ', cb_sigma.getVal(), ' varup,',cb_sigma.getVal()+cb_sigma.getErrorHi(), 'vardown,',cb_sigma.getVal()-cb_sigma.getErrorLo())
        if 'cb_mass_MG' in iipar:
            cb_m0.setError( max(abs(varmean-vardown), abs(varmean-varup)) )
            #cb_m0.setAsymError( abs(varmean-vardown), abs(varmean-varup) )
            cb_m0.setVal( varmean )
            import_workspace( ws_out, cb_m0)
            print('varmean ', cb_m0.getVal(), ' varup,',cb_m0.getVal()+cb_m0.getErrorHi(), 'vardown,',cb_m0.getVal()-cb_m0.getErrorLo())
        if '_norm' in iipar:
            var = ROOT.RooRealVar('cb_MG_M%s_W%s_%s%s_norm' %(str(mass),str(width),str(ich),str(iyear)), 'Norm',
                                 varmean, varmean*0.5, varmean*1.5 )
            import_workspace( ws_out, var)
    import_workspace( ws_out, cb_cut2)
    import_workspace( ws_out, cb_power1)
    import_workspace( ws_out, cb_power2)
    mt_res = ROOT.RooRealVar("mt_res","mt_res", mass,  0.5*mass,  1.1*mass+40) 
    import_workspace( ws_out, mt_res)

    #create pdf
    pdfname = 'cb_MG_M%s_W%s_%s%s' %(str(mass),width,ich,iyear)
    sigModel = ROOT.RooDoubleCB( pdfname, 'Double Sided Crystal Ball Lineshape', mt_res, cb_m0, cb_sigma, cb_cut1, cb_power1, cb_cut2, cb_power2)
    import_workspace( ws_out, sigModel)
    outputfile = '%s/%s/%s.root' %( data_outDir, str(iyear),ws_out.GetName() )
    ws_out.writeToFile( outputfile )

def make_comparison_plots( mass, width,  iyear, ich ) :

    sigpar = "_".join(['M'+str(mass), 'W'+str(width), '%s_%s' %( ich,str(iyear) )])
    inpar = "_".join(['M'+str(mass), 'W'+str(width), ich])

    inputfile0 = 'data_1015_afterbias_study/sigfit/%i/ws%s_%s.root' %( iyear, 'signal', inpar )
    wsname = "wssignal" + '_' + inpar
    print inputfile0, " : ", wsname
    ifile0 = ROOT.TFile.Open( inputfile0, 'READ' )
    if not ifile0:
        return
    ws_in0 = ifile0.Get( wsname )

    inputfile = '%s/%s/%s.root' %( data_outDir,str(iyear), "wssignal_M%s_W%s_%s"%(str(mass),width,ich) )
    wsname = "wssignal" + '_' + inpar
    print inputfile, " : ", wsname
    ifile = ROOT.TFile.Open( inputfile, 'READ' )
    if not ifile:
        return
    ws_in = ifile.Get( wsname )

    pdfname = 'cb_MG_M%s_W%s_%s%s' %(str(mass),width,ich,iyear)
    dataname = 'MG_M%s_W%s_%s%sdatahist' %(str(mass),width,ich,iyear)
    sighists0 = ws_in0.data(dataname)
    sigModel0 = ws_in0.pdf(pdfname)
    sigModel = ws_in.pdf(pdfname)

    #make plots
    c=ROOT.TCanvas()
    leg1 = ROOT.TLegend(0.15,0.73,0.4,0.87)
    leg1.SetFillColor(ROOT.kWhite)
    leg1.SetLineColor(ROOT.kWhite)
    va = ws_in0.var("mt_res")
    frame = va.frame()
    sighists0.plotOn(frame, RooFit.MarkerColor(ROOT.kBlack),  RooFit.MarkerStyle(2), RooFit.LineColor(ROOT.kBlack))
    sigModel0.plotOn(frame, RooFit.LineColor(ROOT.kRed), RooFit.LineStyle(2))
    sigModel.plotOn(frame, RooFit.LineColor(ROOT.kGreen), RooFit.LineStyle(2))
    entry = leg1.AddEntry(sigModel0,"%sGeV_width%s_%s_%s" %(str(mass),width,ich,iyear),"L")
    entry.SetFillStyle(1001)
    entry.SetLineStyle(1)
    entry.SetLineWidth(1)
    entry.SetTextFont(42)
    entry.SetTextSize(0.04)
    entry.SetLineColor(ROOT.kRed)
    entry = leg1.AddEntry(sigModel,"%sGeV_width%s_%s_%s_fit" %(str(mass),width,ich,iyear),"L")
    entry.SetFillStyle(1001)
    entry.SetLineStyle(1)
    entry.SetLineWidth(1)
    entry.SetTextFont(42)
    entry.SetTextSize(0.04)
    entry.SetLineColor(ROOT.kGreen)
    frame.Draw()
    leg1.Draw()
    c.SaveAs(plot_outDir+'/new_signal_M%s_W%s_%s_%s.png'%(str(mass),width,ich,iyear))
    ifile.Close()


if options.fitSignal:
    make_parametrized_signal_model()


#Prepare Parameterized signal model
widthpoints    = ['5','0p01']
yearpoints = [2016,2017,2018]
chpoints = ['el','mu']
masspoints = [300, 350, 400, 450, 600, 700, 800, 900, 1000, 1200, 1400, 1600, 1800, 2000]
for mass in masspoints:
    for width in widthpoints:
        for iyear in yearpoints :
            for ich in chpoints :
                print(mass, width, iyear, ich)
                #######prepare_signal_functions_helper_extra( mass, width, iyear, ich)  # Don't use
                if options.makeWS:
                    prepare_signal_functions_helper( mass, width, iyear, ich)
                if options.makeplots:
                    make_comparison_plots( mass, width, iyear, ich )
                    #make_comparison_plots( mass, width, options.year, ich )















