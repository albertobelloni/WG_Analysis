import ROOT
from ROOT import gROOT, gSystem, RooIntegralMorph
from ROOT import RooRealVar, RooDataHist,RooAbsReal
#from ROOT import RooFit as rf
#from uncertainties import ufloat
#import uuid
#import re
#import random
#import sys
#from collections import namedtuple, OrderedDict
#from functools import wraps
#from DrawConfig import DrawConfig
#gSystem.Load("My_double_CB/RooDoubleCB_cc.so")
from ROOT import gPad, RooFit, kRed, kBlue, kViolet, kRainBow
#import analysis_utils
import json
import os
from array import array
from collections import OrderedDict,defaultdict
recdd = lambda : defaultdict(recdd) ## define recursive defaultdict
from argparse import ArgumentParser
if "parser" not in locals(): parser = ArgumentParser()
#parser.add_argument('--baseDirMuG',      default=None,          help='Path to muon base directory')
#parser.add_argument('--baseDirElG',      default=None,          help='Path to electron base directory')
#parser.add_argument('--baseDirMuMu',     default=None,          help='Path to muon base directory')
#parser.add_argument('--baseDirElEl',     default=None,          help='Path to electron base directory')
#parser.add_argument('--baseDirMu',       default=None,          help='Path to muon base directory')
#parser.add_argument('--baseDirEl',       default=None,          help='Path to electron base directory')
#parser.add_argument('--outputDir',       default=None,          help='Output directory to write histograms')
#parser.add_argument('--dataDir',         default=None,          help='IO directory to data')
#parser.add_argument('--data',            action="store_true",   help='Use data or MC')
#parser.add_argument('--batch',           action="store_true",   help='Supress X11 output')
#parser.add_argument('--condor',          action="store_true",   help='run on condor')
#parser.add_argument('--year',            default=2016,          type=int,            help='Set run year')
#parser.add_argument('--quiet',           action="store_true",   help='Quiet output')
#parser.add_argument('--nodataFrame',     dest='dataFrame',  action='store_false',    help='backwards compatibility for pre-2019 releases of ROOT')
parser.add_argument( '--fitSignal',        action='store_true', help='Fit signal samples, generate files for fully para model' )
parser.add_argument( '--makeWS',        action='store_true', help='makeWS' )
parser.add_argument( '--makeplots',        action='store_true', help='makeplots' )
parser.add_argument( '--mass',        type=int, help='' )
parser.add_argument( '--width',        type=str, help='' )
parser.add_argument( '--iyear',        type=int, help='' )
parser.add_argument( '--ich',        type=str, help='' )

options = parser.parse_args()
#execfile("MakeBase.py")

inputDir = "./data/sigfit/2017/"
outputDir = "./"
_XSFILE   = 'cross_sections/photon16_smallsig.py'

_LUMI16   = 36000
_LUMI17   = 41000
_LUMI18   = 59740

# make parametrized signal model

_JSONLOC = "data/para.txt"
_JSONLOC_Fit = "data/para_fit.txt"
plot_outDir = "plots/MakeSignalWS_para"
data_outDir = "data/sigfit_para"

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
    # Fit the signal work space and extrat the parameetrs 
    signal_widths    = ['5', '0p01']
    signal_masses    = [300, 350, 400, 450, 500, 600, 700, 800, 900, 1000, 1200, 1400, 1600, 1800, 2000]
    Years= ['2016','2017','2018']
    signal_widths    = ['5','0p01']
    #Years= ['2018']
    CH = ['mu']#,'mu']

    #weightMap,_ = analysis_utils.read_xsfile( _XSFILE, 1, print_values=True )
    #sampManElG = SampleManager( options.baseDirElG, _TREENAME, filename=_FILENAME, lumi=-1)
    #sampManElG.ReadSamples( _SAMPCONF )

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
    inputdir = "data/sigfit/"#_step2_fixpowers"
    #inputdir = "data/sigfit_step1/"#_floatall"
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
                    parlist[grname+'_err'],parlist[grname+'_errx'] = array( 'd' ),array( 'd' )
                    parlist[grname],parlist[grname+'mass'], = array( 'd' ),array( 'd' )
                    for mass in signal_masses:
                        wsname = 'wssignal_M%s_W%s_%s' %(str(mass),wid,ich)
                        pdfname = 'cb_MG_M%s_W%s_%s%s' %(str(mass),wid,ich,iyear)
                        dataname = 'MG_M%s_W%s_%s%sdatahist' %(str(mass),wid,ich,iyear)
                        inputDir = inputdir+"/%s/" % (iyear)
                        print('open ', inputDir+wsname+'.root')
                        ifile = ROOT.TFile.Open( inputDir+wsname+'.root', 'READ' )
                        ws_in = ifile.Get( wsname )
                        #Do fitting, ignore poor fitting points
                        frame = (ws_in.var("mt_res")).frame()
                        data = ws_in.data(dataname)
                        model = ws_in.pdf(pdfname)
                        data.plotOn(frame)
                        model.plotOn(frame)
                        print('----------frame.chiSquare ',frame.chiSquare())
                        #if(frame.chiSquare()>90): continue
                        if('norm' in ipar):
                            (parlist[grname]).append( ws_in.var(grname.replace("Mass",'M'+str(mass))).getVal())
                            parlists[grname][mass] = ws_in.var(grname.replace("Mass",'M'+str(mass))).getVal()
                            (parlist[grname+'_err']).append( (ws_in.var(grname.replace("Mass",'M'+str(mass))).getError() ))
                            parlists[grname][str(mass)+'_err'] = (ws_in.var(grname.replace("Mass",'M'+str(mass))).getError() )
                        else:
                            (parlist[grname]).append( ws_in.var(grname.replace("Mass",'M'+str(mass))).getVal() )
                            parlists[grname][mass] = ws_in.var(grname.replace("Mass",'M'+str(mass))).getVal()
                            (parlist[grname+'_err']).append( (ws_in.var(grname.replace("Mass",'M'+str(mass))).getAsymErrorHi()+ws_in.var(grname.replace("Mass",'M'+str(mass))).getAsymErrorLo())/2.0 )
                            parlists[grname][str(mass)+'_err'] = ((ws_in.var(grname.replace("Mass",'M'+str(mass))).getAsymErrorHi()+ws_in.var(grname.replace("Mass",'M'+str(mass))).getAsymErrorLo())/2.0 )
                        parlist[grname+'mass'].append(mass)
                        parlist[grname+'_errx'].append(0)
    #Finish reading
    #store param
    multidict_tojson(_JSONLOC, parlists )
# ---------------------------------------------------
    #Decide to do fitting 
    parlists_fit = recdd()
    paramname = ['cb_power1_MG_Mass_Width_CHYEAR','cb_cut2_MG_Mass_Width_CHYEAR','cb_power2_MG_Mass_Width_CHYEAR','cb_sigma_MG_Mass_Width_CHYEAR','cb_mass_MG_Mass_Width_CHYEAR','cb_cut1_MG_Mass_Width_CHYEAR','cb_MG_Mass_Width_CHYEAR_norm']
    paramname = ['cb_sigma_MG_Mass_Width_CHYEAR','cb_mass_MG_Mass_Width_CHYEAR','cb_cut1_MG_Mass_Width_CHYEAR','cb_MG_Mass_Width_CHYEAR_norm']
    paramname = ['cb_cut1_MG_Mass_Width_CHYEAR']#,'cb_MG_Mass_Width_CHYEAR_norm']
    #paramname = ['cb_MG_Mass_Width_CHYEAR_norm']
    nickname={'cb_cut1_MG_Mass_Width_CHYEAR':'#alpha1','cb_cut2_MG_Mass_Width_CHYEAR':'#alpha2',
              'cb_power1_MG_Mass_Width_CHYEAR':'power1 (n1)','cb_power2_MG_Mass_Width_CHYEAR':'power2 (n2)',
              'cb_mass_MG_Mass_Width_CHYEAR':'Mean Value','cb_sigma_MG_Mass_Width_CHYEAR':'#sigma',
              'cb_MG_Mass_Width_CHYEAR_norm':'Eff.'
    }
    colorbar = [ROOT.kRed,ROOT.kBlue,ROOT.kCyan,ROOT.kOrange,ROOT.kGray,ROOT.kBlack, ROOT.kRed+3,ROOT.kBlue+3,ROOT.kGreen+3]
    signal_masses_fit    = [300, 350, 400, 450, 500, 600, 700, 800, 900, 1000, 1200, 1400, 1600, 1800, 2000]
    for ipar in paramname:
        #cpara=ROOT.TCanvas("cpara", "cpara",0,0,800,600)
        cpara=ROOT.TCanvas()
        ROOT.gStyle.SetPalette(55)
        gr= {}
        grint={}
        leg1 = ROOT.TLegend(0.25,0.33,0.8,0.87)
        leg1.SetFillColor(ROOT.kWhite)
        leg1.SetLineColor(ROOT.kWhite)
        ct=-1
        grsum=ROOT.TMultiGraph()
        ctmulti=6
        if(True):
            for wid in signal_widths:
                for iyear in Years:
                    for ich in CH:
                        print(wid,iyear,ich)
                        ct+=1
                        grname = ipar.replace("YEAR",str(iyear))
                        grname = grname.replace("Width",'W'+str(wid))
                        grname = grname.replace("CH",ich)
                        gr[grname] = ROOT.TGraphErrors( len(parlist[grname+'mass']), parlist[grname+'mass'], parlist[grname],parlist[grname+'_errx'],parlist[grname+'_err'] )
                        #(gr[grname]).SetLineColor( kRainBow + ct*ctmulti )
                        (gr[grname]).SetLineColor( colorbar[ct] )
                        (gr[grname]).SetLineWidth( 3 )
                        #(gr[grname]).SetMarkerColor( kRainBow + ct*ctmulti )
                        (gr[grname]).SetMarkerColor( colorbar[ct] )
                        (gr[grname]).SetMarkerStyle( 21 )
                        (gr[grname]).GetXaxis().SetTitle( 'X title' )
                        (gr[grname]).GetYaxis().SetTitle( 'Y title' )
                        gr[grname].SetName(grname)
                        grint[grname] = ROOT.TGraphErrors(len(signal_masses_fit))
                        (grint[grname]).SetLineColor( colorbar[ct] )
                        (grint[grname]).SetLineWidth( 1 )
                        (grint[grname]).SetMarkerColor( colorbar[ct] )
                        (grint[grname]).SetMarkerStyle( 21 )
                        grint[grname].SetMarkerStyle(5)
                        grint[grname].SetFillStyle(3010)
                        grint[grname].SetMarkerSize(0.7)
                        if 'norm' in ipar :
                            a= ROOT.TF1("a","[0] - [1]*TMath::Exp(-x/[2])",0,2500);
                            a.SetParameters(0.1, 0.05, 1000)
                            result =gr[grname].Fit(a,"S")
                            a=gr[grname].GetFunction("a")
                            parlists_fit[grname]['func'] = 'expnorm'
                            parlists_fit[grname][0] = a.GetParameter(0)
                            parlists_fit[grname][1] = a.GetParameter(1)
                            parlists_fit[grname][2] = a.GetParameter(2)
                            parlists_fit[grname+'err'][0] = a.GetParError(0)
                            parlists_fit[grname+'err'][1] = a.GetParError(1)
                            parlists_fit[grname+'err'][2] = a.GetParError(2)
                            for i in range(len(signal_masses_fit)):
                                #print(i, a.Eval(signal_masses_fit[i]))
                                grint[grname].SetPoint(i, signal_masses_fit[i],0)
                            ROOT.TVirtualFitter.GetFitter().GetConfidenceIntervals(grint[grname],0.95)
                            for i in range(len(signal_masses_fit)):
                                #parlists_fit[grname+'fit'][signal_masses_fit[i]]['x'] = grint[grname].GetX()[i]
                                parlists_fit[grname+'fit'][signal_masses_fit[i]]['y'] = grint[grname].GetY()[i]
                                #parlists_fit[grname+'fit'][signal_masses_fit[i]]['xe'] = grint[grname].GetErrorX(i)
                                parlists_fit[grname+'fit'][signal_masses_fit[i]]['ye'] = grint[grname].GetErrorY(i)
                        elif 'cut1' in ipar :
                            a= ROOT.TF1("a","[0] + [1]/(x-[2])",0,2500);
                            if wid == '5':
                                a.SetParameters(0.263351,153.581,151.212)
                            if wid == '0p01':
                                a.SetParameters(0.174413,106.189,210.706)
                            result =gr[grname].Fit(a,"S")
                            a=gr[grname].GetFunction("a")
                            parlists_fit[grname]['func'] = 'inv'
                            parlists_fit[grname][0] = a.GetParameter(0)
                            parlists_fit[grname][1] = a.GetParameter(1)
                            parlists_fit[grname][2] = a.GetParameter(2)
                            parlists_fit[grname+'err'][0] = a.GetParError(0)
                            parlists_fit[grname+'err'][1] = a.GetParError(1)
                            parlists_fit[grname+'err'][2] = a.GetParError(2)
                            for i in range(len(signal_masses_fit)):
                                grint[grname].SetPoint(i, signal_masses_fit[i],0)
                            ROOT.TVirtualFitter.GetFitter().GetConfidenceIntervals(grint[grname],0.95)
                            for i in range(len(signal_masses_fit)):
                                #parlists_fit[grname+'fit'][signal_masses_fit[i]]['x'] = grint[grname].GetX()[i]
                                parlists_fit[grname+'fit'][signal_masses_fit[i]]['y'] = grint[grname].GetY()[i]
                                #parlists_fit[grname+'fit'][signal_masses_fit[i]]['xe'] = grint[grname].GetErrorX(i)
                                parlists_fit[grname+'fit'][signal_masses_fit[i]]['ye'] = grint[grname].GetErrorY(i)
                        elif 'power2' in ipar or 'power1' in ipar:
                            a= ROOT.TF1("a","[0] + [1]*x",500,2500);
                            a.SetParameters(32,-0.01)
                            result = gr[grname].Fit("a","R")
                            a=gr[grname].GetFunction("a")
                            parlists_fit[grname]['func'] = 'pol1'
                            parlists_fit[grname][0] = a.GetParameter(0)
                            parlists_fit[grname][1] = a.GetParameter(1)
                            parlists_fit[grname+'err'][0] = a.GetParError(0)
                            parlists_fit[grname+'err'][1] = a.GetParError(1)
                            for i in range(len(signal_masses_fit)):
                                #print(i, a.Eval(signal_masses_fit[i]))
                                grint[grname].SetPoint(i, signal_masses_fit[i],0)
                            ROOT.TVirtualFitter.GetFitter().GetConfidenceIntervals(grint[grname],0.95)
                            for i in range(len(signal_masses_fit)):
                                #parlists_fit[grname+'fit'][signal_masses_fit[i]]['x'] = grint[grname].GetX()[i]
                                parlists_fit[grname+'fit'][signal_masses_fit[i]]['y'] = grint[grname].GetY()[i]
                                #parlists_fit[grname+'fit'][signal_masses_fit[i]]['xe'] = grint[grname].GetErrorX(i)
                                parlists_fit[grname+'fit'][signal_masses_fit[i]]['ye'] = grint[grname].GetErrorY(i)
                        #elif 'sigma' in ipar or 'cb_mass_MG' in ipar :
                        elif 'cb_mass_MG' in ipar :
                            result = gr[grname].Fit("pol1")
                            print(wid, iyear, ich)
                            a=gr[grname].GetFunction("pol1")
                            print(a.GetNumberFreeParameters(), " free parameters")
                            print(a.GetParameter(0),a.GetParameter(1))
                            parlists_fit[grname]['func'] = 'pol1'
                            parlists_fit[grname][0] = a.GetParameter(0)
                            parlists_fit[grname][1] = a.GetParameter(1)
                            parlists_fit[grname+'err'][0] = a.GetParError(0)
                            parlists_fit[grname+'err'][1] = a.GetParError(1)
                            for i in range(len(signal_masses_fit)):
                                #print(i, a.Eval(signal_masses_fit[i]))
                                grint[grname].SetPoint(i, signal_masses_fit[i],0)
                            ROOT.TVirtualFitter.GetFitter().GetConfidenceIntervals(grint[grname],0.95)
                            for i in range(len(signal_masses_fit)):
                                #parlists_fit[grname+'fit'][signal_masses_fit[i]]['x'] = grint[grname].GetX()[i]
                                parlists_fit[grname+'fit'][signal_masses_fit[i]]['y'] = grint[grname].GetY()[i]
                                #parlists_fit[grname+'fit'][signal_masses_fit[i]]['xe'] = grint[grname].GetErrorX(i)
                                parlists_fit[grname+'fit'][signal_masses_fit[i]]['ye'] = grint[grname].GetErrorY(i)
                        else:
                            result = gr[grname].Fit("pol2")
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
                            for i in range(len(signal_masses_fit)):
                                #print(i, a.Eval(signal_masses_fit[i]))
                                grint[grname].SetPoint(i, signal_masses_fit[i],0)
                            ROOT.TVirtualFitter.GetFitter().GetConfidenceIntervals(grint[grname],0.95)
                            for i in range(len(signal_masses_fit)):
                                #parlists_fit[grname+'fit'][signal_masses_fit[i]]['x'] = grint[grname].GetX()[i]
                                parlists_fit[grname+'fit'][signal_masses_fit[i]]['y'] = grint[grname].GetY()[i]
                                #parlists_fit[grname+'fit'][signal_masses_fit[i]]['xe'] = grint[grname].GetErrorX(i)
                                parlists_fit[grname+'fit'][signal_masses_fit[i]]['ye'] = grint[grname].GetErrorY(i)
                        gr[grname].Draw( 'ACP' )
                        grint[grname].Draw('A3')
                        #a.SetLineColor( kRainBow + ct*ctmulti )
                        a.SetLineColor( colorbar[ct] )
                        grsum.Add(grint[grname])
                        grsum.Add(gr[grname])
                        entry = leg1.AddEntry(gr[grname],'#Gamma_{3}/m_{3}={0},  {1}{2}'.format('5%',ich,iyear,"{X}") if wid=='5' else '#Gamma_{3}/m_{3}={0},  {1}{2}'.format('0.01%',ich,iyear,"{X}"),"L")
                        entry.SetFillStyle(1001)
                        entry.SetLineStyle(1)
                        entry.SetLineWidth(1)
                        entry.SetTextFont(42)
                        entry.SetTextSize(0.04)
                        #entry.SetLineColor(kRainBow+ct*ctmulti)
                        entry.SetLineColor(colorbar[ct])
            grsum.Draw("AP")
            grsum.GetXaxis().SetTitle( 'm_{X} (GeV)' )
            grsum.GetYaxis().SetTitle( nickname[ipar] )
            leg1.Draw()
            cpara.SaveAs("gr"+ipar+"_"+CH[0]+".C")
            #cpara.SaveAs("gr"+ipar+"_"+Years[0]+".C")
            input("")
    multidict_tojson(_JSONLOC_Fit, parlists_fit )

#-------------------------------------------------

def prepare_signal_functions_helper( mass, width,  iyear, ich , Use_fitError=True) :
    # produce parameterized signal models according to the fit results 
    sigpar = "_".join(['M'+str(mass), 'W'+str(width), '%s_%s' %( ich,str(iyear) )])
    inpar = "_".join(['M'+str(mass), 'W'+str(width), ich])
    _JSONLOC_Fit = 'data/para_fit_'+str(iyear)+'.txt'
    fname= 'data/sigfit/%i/ws%s_%s.root' %( iyear, 'signal', inpar )
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
    #paramname = Allparamname
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
            print("set ",var.getVal()," to ", sigfitparams[iipar+'fit'][str(mass)]['y'] )
            print('original error, ', var.getError(), ' set to ', sigfitparams[iipar+'fit'][str(mass)]['ye'])
            if Use_fitError:
                var.setVal( sigfitparams[iipar+'fit'][str(mass)]['y'] )
                var.setError( sigfitparams[iipar+'fit'][str(mass)]['ye'] )
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

def make_comparison_plots( mass, width,  iyear, ich ) :

    sigpar = "_".join(['M'+str(mass), 'W'+str(width), '%s_%s' %( ich,str(iyear) )])
    inpar = "_".join(['M'+str(mass), 'W'+str(width), ich])

    inputfile0 = 'data/sigfit/%i/ws%s_%s.root' %( iyear, 'signal', inpar )
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
    print(sighists0.sumEntries())
    #make plots
    mt_res = ws_in0.var("mt_res")

    MIN_=mt_res.getMin()
    MAX_=mt_res.getMax()
    NBIN_=mt_res.getBins()

    frame = mt_res.frame()
    sighists0.plotOn(frame, RooFit.MarkerColor(ROOT.kBlack),  RooFit.MarkerStyle(2), RooFit.LineColor(ROOT.kBlack))
    sigModel0.plotOn(frame, RooFit.LineColor(ROOT.kRed), RooFit.LineStyle(2))
    chi0_=frame.chiSquare()
    print('sigModel0-> ', frame.chiSquare())
    hpull = frame.pullHist()
    hpull.SetLineColor(ROOT.kRed)
    hpull.SetMarkerColor(ROOT.kRed)
    frame0_ = mt_res.frame(ROOT.RooFit.Title("Pull Distribution"))
    frame0_.addPlotable(hpull, "P")
    sigModel.plotOn(frame, RooFit.LineColor(ROOT.kGreen), RooFit.LineStyle(2))
    chi_=frame.chiSquare()
    print('sigModel-> ', frame.chiSquare())
    hpull_ = frame.pullHist()
    hpull_.SetLineColor(ROOT.kGreen)
    hpull_.SetMarkerColor(ROOT.kGreen)
    frame_ = mt_res.frame(ROOT.RooFit.Title("Pull Distribution"))
    frame_.addPlotable(hpull_, "P")

    if frame !=0:
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
        frame_4fa51a0__1 = ROOT.TH1D("frame_4fa51a0__1","Unbinned ML fit, %s %s"%(ich,iyear),NBIN_,MIN_,MAX_)
        frame_4fa51a0__1.GetXaxis().SetTitle("m_{T}^{l#nu#gamma} [GeV]");
        frame_4fa51a0__1.GetXaxis().SetLabelFont(42);
        frame_4fa51a0__1.GetXaxis().SetLabelSize(0.05);
        frame_4fa51a0__1.GetXaxis().SetTitleSize(0.05);
        frame_4fa51a0__1.GetXaxis().SetTitleOffset(1);
        frame_4fa51a0__1.GetXaxis().SetTitleFont(42);
        frame_4fa51a0__1.GetYaxis().SetTitle("Event / %0.1f GeV"%((MAX_-MIN_)/NBIN_));
        frame_4fa51a0__1.GetYaxis().SetLabelFont(42);
        frame_4fa51a0__1.GetYaxis().SetLabelSize(0.05);
        frame_4fa51a0__1.GetYaxis().SetTitleSize(0.05);
        frame_4fa51a0__1.GetYaxis().SetTitleFont(42);
        frame_4fa51a0__1.GetYaxis().SetRangeUser(0,sighists0.sumEntries()*15/(NBIN_))
        frame_4fa51a0__1.GetXaxis().SetLabelOffset(999)
        frame_4fa51a0__1.GetXaxis().SetLabelSize(0)
        frame_4fa51a0__1.Draw("AXISSAME");
        frame.Draw("same E")

        leg2 = ROOT.TLegend(0.6,0.7,0.9,0.9);
        leg2.SetBorderSize(0);
        leg2.SetLineStyle(1);
        leg2.SetLineWidth(1);
        entry=leg2.AddEntry("","DSCB Fit","l");
        #entry=leg2.AddEntry("","Fix n1,n2","l");
        entry.SetFillStyle(1001);
        entry.SetLineStyle(9)
        entry.SetLineWidth(2)
        entry.SetLineColor(ROOT.kRed);
        entry.SetTextFont(61)
        entry.SetTextSize(0.04)
        #entry=leg2.AddEntry("","Fix n1,n2","l");
        entry=leg2.AddEntry("","Parameterized","l");
        entry.SetFillStyle(1001);
        entry.SetLineStyle(9)
        entry.SetLineWidth(2)
        entry.SetLineColor(ROOT.kGreen);
        entry.SetTextFont(61)
        entry.SetTextSize(0.04)
        leg2.Draw()

        tex2 = ROOT.TLatex(0.18,0.9,"CMS");
        tex2.SetNDC();
        tex2.SetTextAlign(13);
        tex2.SetTextFont(61);
        tex2.SetTextSize(0.06);
        tex2.SetLineWidth(2);
        tex2.Draw();
        tex1 = ROOT.TLatex(0.3,0.9,"Simulation")
        tex1.SetNDC()
        tex1.SetTextAlign(13)
        tex1.SetTextFont(52)
        tex1.SetTextSize(0.06)
        tex1.SetLineWidth(2)
        tex1.Draw()
        if width=='0p01': width='0.01'
        if ich=='el':
            ich='Electron'
        if ich=='mu':
            ich='Muon'
        tex3 = ROOT.TLatex(0.18,0.82, str(iyear)+' '+ich+' channel')
        tex3.SetNDC()
        tex3.SetTextAlign(13)
        tex3.SetTextFont(61)
        tex3.SetTextSize(0.06)
        tex3.SetLineWidth(2)
        tex3.Draw()
        T1=ROOT.TLatex();
        T1.SetTextSize(0.06);
        T1.DrawLatexNDC(0.18,0.7, "#Gamma_{x}/m_{x}="+width+"%");
        T1.SetTextAlign(13)
        T1.SetTextFont(61)
        T1.SetLineWidth(2)
        T1=ROOT.TLatex();
        #T1.DrawLatexNDC(0.78,0.825, " #chi^{2}=%0.1f"%(chi0_));
        T1.DrawLatexNDC(0.78,0.83, " #chi^{2}=%0.1f"%(chi0_));
        T1.SetLineStyle(9)
        T1.SetLineWidth(2)
        T1.SetLineColor(ROOT.kRed);
        T1.SetTextFont(61)
        T1.SetTextSize(0.03)
        T1=ROOT.TLatex();
        #T1.DrawLatexNDC(0.78,0.73, " #chi^{2}=%0.1f"%(chi_));
        T1.DrawLatexNDC(0.85,0.73, " #chi^{2}=%0.1f"%(chi_));
        T1.SetLineStyle(9)
        T1.SetLineWidth(2)
        T1.SetLineColor(ROOT.kRed);
        T1.SetTextFont(61)
        T1.SetTextSize(0.03)

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
        frame0_.Draw("same")
        frame_.Draw("same E")
        line = ROOT.TLine(MIN_,0,MAX_,0);
        line.SetLineStyle(2)
        line.SetLineWidth(2)
        line.Draw()
    #input('wait ... ')
    if width=='0.01': width='0p01'
    c.SaveAs(plot_outDir+'/new_signal_M%s_W%s_%s_%s.png'%(str(mass),width,ich,iyear))
    ifile.Close()

#if options.fitSignal:
make_parametrized_signal_model()
#prepare_signal_functions_helper( options.mass, options.width, options.iyear, options.ich )
#make_comparison_plots( options.mass, options.width, options.iyear, options.ich )

exit()


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
                if options.makeWS:
                    prepare_signal_functions_helper( mass, width, iyear, ich)
                if options.makeplots:
                    make_comparison_plots( mass, width, iyear, ich )
                    #make_comparison_plots( mass, width, options.year, ich )















