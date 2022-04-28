#!/usr/bin/env python3

def addparser(parser):
    parser.add_argument('--TT',            action="store_true",   help='Do TT bar control region')
    parser.add_argument('--ZP',            action="store_true",   help='Do Z peak control region')

exec(compile(open("MakeBase.py", "rb").read(), "MakeBase.py", 'exec'))
import re
import numpy as np
import os
import uuid
import math
import pickle
import selection_defs as defs
from uncertainties import ufloat
from FitManager import FitManager
from DrawConfig import DrawConfig
import json
#ROOT.TVirtualFitter.SetMaxIterations( 100000 )
ROOT.gStyle.SetOptStat(0)
ROOT.Math.MinimizerOptions.SetDefaultMaxFunctionCalls( 100000)

##weight = "PUWeight*NLOWeight"
weight = "NLOWeight"

ptb=None
#ptbins = [0, 30, 40, 50, 60, 80, 2000]
ptbins = [80, 2000]
ptvar = "ph_pt[0]"

doControlRegion=False
#doControlRegion="Z"
#doControlRegion="TT"
if options.ZP == True:
    doControlRegion="Z"
if options.TT == True:
    doControlRegion="TT"


_SAMPCONF = 'Modules/Resonance%i_efake.py' %options.year






def get_param(filename, ptlist=None):
    js = json.loads(open(filename).read())
    xlist = np.array(js['ptlist'])
    sig   = np.array(js['parm']['Nsig'])
    error = np.array(js['error']['Nsig'])
    return sig, error

def closure(  sampMan, sample, sel_base, eta_cut, var="ph_pt",
              varbins = list(range(0,200,25)),xtitle="photon p_{T}",
              plot_var='m_lep_ph', suffix='', workspace=None, overlaprm=1,mode=1) :
    bins = np.array(varbins,'f')
    h_sr_est= ROOT.TH1F("h_sr_est","",len(varbins)-1,bins)
    h_sr_sum= ROOT.TH1F("h_sr_sum",";%s;count" %(xtitle),len(varbins)-1,bins)
    h_sr_est2= ROOT.TH1F("h_sr_est2",";%s;count" %(xtitle),len(varbins)-1,bins)
    sr_est_sum = sr_sum_sum = 0
    sr_est2_sum = 0
    for i in range(len(varbins)-1):
        sel_base1= sel_base + "&& %s[0]>%3f && %s[0]<=%3f" %(var,varbins[i],var,varbins[i+1])
        #sel_base1= sel_base + "&& %s>%3f && %s<=%3f" %(var,varbins[i],var,varbins[i+1])

        #if (i==0): sel_base1= sel_base + "&& %s[0]<=%3f" %(var,varbins[1])
        if (i==len(varbins)-2): sel_base1= sel_base + "&& %s[0]>%3f " %(var,varbins[i])
        filename="temp/"+var+"%s_sel_%s_%i_%i_%i_" %(plot_var,var,i,varbins[i],varbins[i+1])
        if options.data:
            s= closureBin(sampMan, sample, sel_base1, eta_cut, plot_var, overlaprm,filename,mode=mode) 
            sa,sb,ss,sd=s
            zg = closureBin(sampMan,'Zgamma',sel_base1,eta_cut,plot_var,overlaprm,filename) 
            wg = closureBin(sampMan,'Wgamma',sel_base1,eta_cut,plot_var,overlaprm,filename) 
            sga=np.array(s);sga[2]=zg[2]+wg[2]+1
            zga=np.array(zg)
            wga=np.array(wg)
            sga_sub = sga-zga-wga
            print('Signal,Zg,Wg: ')
            print(s)
            print(zg)
            print(wg)
            print('pollution: ',(zga+wga)/sga)
            print('subtracted: ',sga_sub)
            sr_est, sr_est_e, _, _ = calABD(*sga_sub)
            za,zb,zs,zd = closureBin(sampMan, 'Z+jets', sel_base1, eta_cut, plot_var, overlaprm,filename) 
            sr_est2, sr_est2_e, sr_sum, sr_sum_e = calABD(za,zb,zs,zd)
            sr_est2_sum+=sr_est2
            h_sr_est.SetBinContent(i+1,sr_est)
            h_sr_est.SetBinError(i+1,sr_est_e)
            h_sr_est2.SetBinContent(i+1,sr_est2)
            h_sr_est2.SetBinError(i+1,sr_est2_e)
            h_sr_sum.SetBinContent(i+1,sr_sum)
            h_sr_sum.SetBinError(i+1,sr_sum_e)
        else:
            sa,sb,ss,sd= sampMan.closureBin( sample, sel_base1, 
                            eta_cut, plot_var, overlaprm,filename,mode=mode,doSave=1) 
            #a_fit = fitter(hist_A)
            #b_fit = fitter(hist_B)
            #s_fit = fitter(hist_sr)
            #d_fit = fitter(hist_D)
            sr_est, sr_est_e, sr_sum, sr_sum_e = calABD(sa,sb,ss,sd,mode=mode)
            h_sr_est.SetBinContent(i+1,sr_est)
            h_sr_est.SetBinError(i+1,sr_est_e)
            h_sr_sum.SetBinContent(i+1,sr_sum)
            h_sr_sum.SetBinError(i+1,sr_sum_e)
        sr_est_sum+=sr_est
        sr_sum_sum+=sr_sum
    # draw graph and formatting
    if options.data:
        print("S estimate data: ", sr_est_sum)
        print("S estimate mc: ", sr_est2_sum)
        print("S total mc: ",sr_sum_sum)
        print("difference data: ",(sr_est_sum-sr_sum_sum)/sr_sum_sum)
        print("difference mc: " ,(sr_est2_sum-sr_sum_sum)/sr_sum_sum)
    else:
        print("S estimate: ", sr_est_sum)
        print("S total: ",sr_sum_sum)
        print("difference: ",(sr_est_sum-sr_sum_sum)/sr_sum_sum)
    sampMan.create_standard_ratio_canvas()
    #c2 = ROOT.TCanvas("c2","multipads",800,700)
    #toppad = ROOT.TPad("top","top",0.01,0.35,0.99,0.99)
    #botpad = ROOT.TPad("bot","bot",0.01,0.01,0.99,0.34)
    #toppad.SetTopMargin(0.08)
    #toppad.SetBottomMargin(0.06)
    #toppad.SetLeftMargin(0.15)
    #toppad.SetRightMargin(0.05)
    #botpad.SetTopMargin(0.00)
    #botpad.SetBottomMargin(0.3)
    #botpad.SetLeftMargin(0.15)
    #botpad.SetRightMargin(0.05)
    sampMan.curr_canvases['top'].cd()
    ROOT.gPad.SetTicks(1,1)
    #toppad.Draw()
    #toppad.SetLogy(0)
    #botpad.Draw()
    #toppad.cd()
    hratio = doratio(h_sr_sum,h_sr_est)
    hformat(h_sr_est,ROOT.kBlack)
    hformat(h_sr_est2,ROOT.kBlue)
    hformat(h_sr_sum,ROOT.kRed)
    hmaxar = [h.GetMaximum() for h in (h_sr_est,h_sr_est2,h_sr_sum)]
    hmax = max(hmaxar)*1.2
    print(hmax, hmaxar)

    #h_sr_sum.SetMarkerStyle(1)
    #h_sr_est2.SetMarkerStyle(1)
    if options.data: h_sr_est.SetMarkerStyle(20)
    h_sr_est.Draw("e ")
    h_sr_est.SetMaximum(hmax)
    if options.data: h_sr_est2.Draw("e same ")
    h_sr_sum.Draw("e same")
    #h_sr_est.GetYaxis().UnZoom()
    ROOT.gPad.Modified()
    ROOT.gPad.Update()
    tl = ROOT.TLegend(0.65,0.65,0.90,0.82,"","brNDC")
    if options.data:
        tl.AddEntry("h_sr_sum","Signal Z+jets","PL")
        tl.AddEntry("h_sr_est","A/B*D data","PL")
        tl.AddEntry("h_sr_est2","A/B*D Z+jets","PL")
    elif mode==1:
        tl.AddEntry("h_sr_sum","expected fakes","PL")
        tl.AddEntry("h_sr_est","estimation","PL")
    elif mode==2:
        tl.AddEntry("h_sr_sum","C/D","PL")
        tl.AddEntry("h_sr_est","A/B","PL")
    tl.Draw()
    #tex = cmsinternal(toppad)
    draw_config = DrawConfig("","","",label_config={"dx":0,"dy":-0.03})
    labels = draw_config.get_labels()
    for lab in labels :
            lab.Draw()
            sampMan.curr_decorations.append( lab )
    # bottom pad
    sampMan.curr_canvases["bottom"].cd()
    ROOT.gPad.SetTicks(1,1)
    hratio.Draw("e")
    oneline = ratioline(hratio)
    sampMan.curr_canvases["base"].SaveAs("temp/test.pdf")
    sampMan.curr_canvases["base"].SaveAs("temp/test.png")
    return


def closureBin( sampMan, sample, sel_base, eta_cut, plot_var='m_lep_ph', overlaprm=1,filename = "m_lep_ph_default_", doSave=0,mode=1) :
    if eta_cut=="EB": sel_base += '&&abs(ph_eta[0])<=1.4'
    if sample == 'Data': 
            sel_base += ' && !(met_pt*.98>25&&ph_mediumPassCSEV_n>0)'
            print('DATA MASK')

#   passev = 'ph_mediumPassCSEV_n==1'
#   failev = 'ph_mediumFailCSEV_n==1'
#   ph_selection_sr  = 'met_pt>25 && ' + passev
#   ph_selection_B   = 'met_pt<25 && ' +failev
#   ph_selection_A   = 'met_pt<25 && ' +passev
#   ph_selection_D   = 'met_pt>25 && ' +failev 
#   varfail = '[ptSorted_ph_mediumPassEleOlapFailCSEV_idx[0]]'
#   varpass = '[ptSorted_ph_mediumPassEleOlapPassCSEV_idx[0]]'

    if overlaprm:
        #passv = "ph_passEleVeto[0]==1"
        #failv = "ph_passEleVeto[0]==0"
        passv = "ph_hasPixSeed[0]==0"
        failv = "ph_hasPixSeed[0]==1"
        ph_selection_sr  = 'met_pt*1.>25 &&'+passv
        ph_selection_B   = 'met_pt<25 && '+failv
        ph_selection_A   = 'met_pt*1.<25 &&'+passv
        ph_selection_D   = 'met_pt>25 && '+failv
    varfail=varpass=''

    full_sel_D = ' && '.join( [sel_base, ph_selection_D, ] )
    full_sel_A   = ' && '.join( [sel_base, ph_selection_A,] )
    full_sel_B   = ' && '.join( [sel_base, ph_selection_B,] )
    full_sel_sr    = ' && '.join( [sel_base, ph_selection_sr,] )
    # add event weights
#   fmet = '(0.9516-0.000143*met_pt+5.062e-5*met_pt^2)'
    #PixSeed weights
    #fmet = '(0.915919-0.00101076*met_pt+5.37366e-5*met_pt^2)' #normal fit
    #fmet = "(0.934537-7.23281e-4*met_pt+8.08238e-5*met_pt^2)"  #likelihood
    fmet = "1"
    full_sel_B = fmet+'*('+full_sel_B+')'
    full_sel_D = fmet+'*('+full_sel_D+')'

    binning = (200,0,200)
    c1 =ROOT.TCanvas()
    hist_D   = clone_sample_and_draw( sampMan, sample, plot_var+varfail , full_sel_D, binning )
    hist_D.Draw('e')
    if (doSave):c1.SaveAs(filename+"D.pdf")
    hist_A   = clone_sample_and_draw( sampMan, sample, plot_var+varpass , full_sel_A  , binning )
    hist_A.Draw('e')
    if (doSave):c1.SaveAs(filename+"A.pdf")
    hist_B   = clone_sample_and_draw( sampMan, sample, plot_var+varfail , full_sel_B  , binning )
    hist_B.Draw('e')
    if (doSave):c1.SaveAs(filename+"B.pdf")
    hist_sr  = clone_sample_and_draw( sampMan, sample, plot_var+varpass , full_sel_sr  , binning )
    hist_sr.Draw('e')
    if (doSave): c1.SaveAs(filename+"S.pdf")
    sampMan.outputs[filename+"A"] = hist_A
    sampMan.outputs[filename+"B"] = hist_B
    sampMan.outputs[filename+"S"] = hist_sr
    sampMan.outputs[filename+"D"] = hist_D
    intrange = [80,100]
    a_sum = hist_A.Integral(*intrange)
    b_sum = hist_B.Integral(*intrange)
    sr_sum = hist_sr.Integral(*intrange)
    d_sum = hist_D.Integral(*intrange)
    a_sum2 = hist_A.Integral()
    sr_sum2 = hist_sr.Integral()
    d_sum2 = hist_D.Integral()
    #print  "Region A: ", a_sum
    print("Region A: %.4f - %.4f = %.4f" %( a_sum2, a_sum, a_sum2-a_sum))
    print("Region B: ", b_sum)
    print("Region S: %.4f - %.4f = %.4f" %( sr_sum2, sr_sum, sr_sum2-sr_sum))
    print("Region D: ", d_sum)
    #print  "Region D: %.4f - %.4f = %.4f" %( d_sum2, d_sum, d_sum2-d_sum)
    #return a_sum2-a_sum, b_sum, sr_sum2-sr_sum, d_sum
    return a_sum, b_sum, sr_sum, d_sum

setattr(SampleManager,"closure",closure)
setattr(SampleManager,"closureBin",closureBin)

def fitter(h):
    hname  = h.GetName()
    f1 = ROOT.TF1("f1"+hname,"gaus(0)+expo(3)",25,180)
    f1.SetParameter(0,1e3)
    f1.SetParameter(1,90)
    f1.SetParameter(2,10)
    h1.Fit("f1")
    parm = array('d',[0]*3)
    f1.GetParameters(parm)
    f1a =  ROOT.TF1("f1a"+hname,"gaus",20,180)
    f1a.SetParameters(parm)
    return f1.Integral(70,110)

def calABD(a_sum,b_sum,sr_sum,d_sum,mode=1):
    print('A/B*D: ',a_sum/b_sum*d_sum, ' diff: ', a_sum/b_sum*d_sum-sr_sum)
    if b_sum+sr_sum>0: print("Discrepency: ", a_sum/b_sum*d_sum/sr_sum-1)
    if mode==1:
      if b_sum>0: sr_est = a_sum/b_sum*d_sum
      else: return 0,0,sr_sum,0
      if (sr_est>0): sr_err = sr_est*math.sqrt(1/a_sum+ 1/b_sum+1/d_sum)
      else: sr_err =0
      return sr_est, sr_err, sr_sum ,math.sqrt(sr_sum)
    elif mode == 2:
        if b_sum>0: r_est = a_sum/b_sum
        else: r_est = 0 
        if d_sum>0: r_sr = sr_sum/d_sum
        else: r_sr = 0 
        if (r_est>0): r_err_est = r_est*math.sqrt(1/a_sum+ 1/b_sum)  # math.sqrt(a_sum *b_sum)/(a_sum+b_sum)     
        else: r_err_est =0
        if (r_sr>0):  r_err_sr  = r_sr*math.sqrt(1/sr_sum+ 1/d_sum) #math.sqrt(sr_sum*d_sum)/(sr_sum+d_sum)   
        else: r_err_sr =0
        return r_est, r_err_est, r_sr, r_err_sr 

def doratio(h1,h2):
    hratio = h1.Clone("hratio")
    hratio.Divide(h2)
    hratio.SetMarkerStyle(20)
    hratio.SetMarkerSize(1.1)
    hratio.SetStats(0)
    hratio.SetTitle("")
    hratio.GetYaxis().SetTitle("ratio")
    hratio.SetLineColor(ROOT.kBlack)
    hratio.SetLineWidth(2)
    hratio.GetYaxis().SetTitleSize(0.10)
    hratio.GetYaxis().SetTitleOffset(0.5)
    hratio.GetYaxis().SetLabelSize(0.10)
    hratio.GetXaxis().SetLabelSize(0.10)
    hratio.GetXaxis().SetTitleSize(0.10)
    hratio.GetXaxis().SetTitleOffset(1.0)
    hratio.GetYaxis().SetRangeUser(0.5,1.5)
    #hratio.GetYaxis().UnZoom()
    hratio.GetYaxis().CenterTitle()
    hratio.GetYaxis().SetNdivisions(506, True)
    return hratio

def cmsinternal(pad):
    pad.cd()
    tex = ROOT.TLatex(0.18,0.93,"CMS Internal")
    tex.SetNDC()
    tex.SetTextSize(0.05)
    tex.SetLineWidth(2)
    tex.Draw()
    return tex

def ratioline(hratio):
    left_edge  = hratio.GetXaxis().GetXmin()
    right_edge = hratio.GetXaxis().GetXmax()
    
    oneline = ROOT.TLine(left_edge, 1, right_edge, 1)
    oneline.SetLineStyle(3)
    oneline.SetLineWidth(2)
    oneline.SetLineColor(ROOT.kBlack)
    oneline.Draw()
    return oneline

def hformat(h1,color):
    h1.SetLineColor(color)
    h1.SetMarkerColor(color)
    #h1.SetMarkerStyle(20)
    h1.SetMarkerSize(1.1)
    h1.SetStats(0)
    h1.SetLineWidth(2)
    h1.GetYaxis().SetTitleSize(0.05)
    h1.GetYaxis().SetTitleOffset(1.15)
    h1.GetYaxis().SetLabelSize(0.05)
    h1.GetXaxis().SetLabelSize(0.05)
    h1.GetXaxis().SetTitleSize(0.05)
    h1.GetXaxis().SetTitleOffset(0.8)


def zones(h1,h3,h2,h4,suffix): 
    c1 = ROOT.TCanvas("c2","multipads",900,700)
    c1.SetGridx()
    c1.SetLogy()
    ROOT.gStyle.SetOptStat(0)
    c1.Divide(2,2,0,0)
    
    c1.cd(1)
    ROOT.gPad.SetTickx(2)
    ROOT.gPad.SetGridx()
    h1.Draw()
    
    c1.cd(2)
    ROOT.gPad.SetGridx()
    ROOT.gPad.SetTickx(2)
    ROOT.gPad.SetTicky(2)
    h2.GetYaxis().SetLabelOffset(0.01)
    h2.Draw()

    c1.cd(3)
    ROOT.gPad.SetGridx()
    h3.Draw()

    c1.cd(4)
    ROOT.gPad.SetGridx()
    ROOT.gPad.SetTicky(2)
    h4.Draw()
    c1.SaveAs("hist_multi_"+suffix+".pdf")


    #make_efake( sampManElG, 'Z+jets', sel_base_el,'EB', 'ph_eta', suffix='noOvLrm', workspace=elefake, overlaprm=0)


def make_efake( sampMan, sample, sel_base, eta_cut, plot_var, suffix='', workspace=None, overlaprm=0):
    #---------------------------------------
    # Get the base selection for each region
    #---------------------------------------
    passev = 'ph_mediumPassCSEV_n==1'
    failev = 'ph_mediumFailCSEV_n==1'
    ph_selection_sr  = 'met_pt>40 && ' + passev #'%s==1' %defs.get_phid_selection('medium')
    ph_selection_B   = 'met_pt<40 && ' +failev #'%s==1'%defs.get_phid_selection( num_var, _var )
    ph_selection_A   = 'met_pt<40 && '+passev #'%s==1' %defs.get_phid_selection( num_var )
    ph_selection_D   = 'met_pt>40 && '+failev #'%s==1' %defs.get_phid_selection( _var )
    varfail = '[ptSorted_ph_mediumPassEleOlapFailCSEV_idx[0]]'
    varpass = '[ptSorted_ph_mediumPassEleOlapPassCSEV_idx[0]]'

    if overlaprm:
        ph_selection_sr  = 'met_pt>40 && ph_passEleVeto[0]==1'
        ph_selection_B   = 'met_pt<40 && ph_passEleVeto[0]==0'
        ph_selection_A   = 'met_pt<40 && ph_passEleVeto[0]==1'
        ph_selection_D   = 'met_pt>40 && ph_passEleVeto[0]==0'
        varfail=varpass=''

    full_sel_D = ' && '.join( [sel_base, ph_selection_D, ] )
    full_sel_A   = ' && '.join( [sel_base, ph_selection_A,] )
    full_sel_B   = ' && '.join( [sel_base, ph_selection_B,] )
    full_sel_sr    = ' && '.join( [sel_base, ph_selection_sr,] )


    label_D = 'd_%s_' %suffix
    label_A   = 'a_%s_' %suffix
    label_B   = 'b_%s_' %suffix
    label_S    = 's_%s_' %suffix

    if workspace is None :
        ws = ROOT.RooWorkspace( 'ws') 
    else :
        ws = workspace

    #---------------------------------------
    # draw the histograms
    #---------------------------------------
    binning = (160,-4,4)
    #binning = (200,0,200)
    hist_D   = clone_sample_and_draw( sampMan, sample, plot_var+varfail , full_sel_D, binning )
    print(hist_D)
    hist_A   = clone_sample_and_draw( sampMan, sample, plot_var+varpass , full_sel_A  , binning )
    hist_B   = clone_sample_and_draw( sampMan, sample, plot_var+varfail , full_sel_B  , binning )
    hist_sr  = clone_sample_and_draw( sampMan, sample, plot_var+varpass , full_sel_sr  , binning )
    c1  = ROOT.TCanvas('c1','c1')
    c1.SetGridx()
    #c1.SetLogy()
    hist_A.Draw()
    c1.SaveAs("hist"+label_A+plot_var+".pdf","pdf")
    hist_B.Draw()
    c1.SaveAs("hist"+label_B+plot_var+".pdf","pdf")
    hist_sr.Draw()
    c1.SaveAs("hist"+label_S+plot_var+".pdf","pdf")
    hist_D.Draw()
    c1.SaveAs("hist"+label_D+plot_var+".pdf","pdf")
    zones(hist_A,hist_B,hist_sr,hist_D,suffix+"_"+plot_var)


    print("Region A: ", hist_A.Integral(80,100))
    print("Region B: ", hist_B.Integral(80,100))
    print("full range:")
    print("Region A: ", hist_A.Integral())
    print("Region B: ", hist_B.Integral())
    print("Region Signal: ", hist_sr.Integral())
    print("Region D: ", hist_D.Integral())


def make_efake2( sampMan, sample, sel_base, eta_cut, plot_var, suffix='',  workspace=None) :

    #only single plot
    #---------------------------------------
    # Get the base selection for each region
    #---------------------------------------
    ph_selection_A   = 'met_pt<40 && ph_passEleVeto[0]==1' #'%s==1' %defs.get_phid_selection( num_var )
    full_sel_A   = ' && '.join( [sel_base, ph_selection_A,] )
    label_A   = 'a_%s_' %suffix

    #---------------------------------------
    # draw the histograms
    #---------------------------------------
    binning = (200,-5,5)
    hist_A   = clone_sample_and_draw( sampMan, sample, plot_var , full_sel_A  , binning )
    c1  = ROOT.TCanvas('c1','c1')
    hist_A.Draw()
    c1.SaveAs("hist"+label_A+plot_var+".pdf","pdf")

    print("bin 80 -100: ", hist_A.Integral(80,100))
    print("full integral: ", hist_A.Integral())



def clone_sample_and_draw( sampMan, samp, var, sel, binning ) :

    newSamp = sampMan.clone_sample( oldname=samp, newname=samp+str(uuid.uuid4()), temporary=True ) 
    sampMan.create_hist( newSamp, var, sel, binning )
    return newSamp.hist

def fillhist(hist, value, error=None ,label= None):
    for i in range(len(value)):
        if error == None:
            hist.SetBinContent(i+1, value[i].n)
            hist.SetBinError(i+1, value[i].s)
        else:
            hist.SetBinContent(i+1, value[i])
            hist.SetBinError(i+1, error[i])
        if label:
            hist.GetXaxis().SetBinLabel(i+1, label[i])

def pair(x):
    return list(zip(x[:-1], x[1:]))

def get_subselection(i):
    if i == 0:          selstr = "&& _VAR_<%g" %ptbins[i+1]
    elif i == ptsize-1: selstr = "&& _VAR_>=%g" %ptbins[i]
    else:               selstr = "&& _VAR_>=%g && _VAR_<%g" %tuple(ptbins[i:i+2])
    return selstr


def getselstring(name):

    ## get selection string
    #selstr = get_subselection(i)
    print("name", name)

    if "200" in name: selstr = "&& ph_pt[0]>200"
    if "80" in name: selstr = "&& ph_pt[0]>80"
    if "40" in name: selstr = "&& ph_pt[0]>40 && ph_pt[0]<80"
    ## replace string by bin variabke
    #selection = selbase+ selstr.replace("_VAR_", ptvar)
    selection = selbase+ selstr

    if "normal" in name:
        badstring = defs.build_bad_efake_sector_string(options.year, "normal")
    if "badonly" in name:
        badstring = defs.build_bad_efake_sector_string(options.year, "badonly")
    if "worstonly" in name:
        badstring = defs.build_bad_efake_sector_string(options.year, "worstonly")
    if "whole" in name:
        badstring = "1"
    selection+="&&(%s)"%badstring

    return selection



##################################
##           SETUP              ##
##################################


if doControlRegion=="TT":
    sampManMuG.ReadSamples( _SAMPCONF )
    samp = sampManMuG
    ch = "mu"
else:
    sampManElG.ReadSamples( _SAMPCONF )
    samp = sampManElG
    ch = "el"

##FIXME encapsulate these functions
ptname = tuple([str("%g" %x).replace('.','p') for x in ptbins])

ptname = ("normal80","badonly80","worstonly80","total80",
          "normal40","badonly40","worstonly40","total40")
ptname = ("normal200","badonly200","worstonly200","total200",
          "normal80","badonly80","worstonly80","total80",
          "normal40","badonly40","worstonly40","total40")
if options.year==2016:
    ptname = ("normal80","badonly80","whole80","total80","normal40","badonly40","whole40","total40")
    ptname = (  "normal200","badonly200","total200",
                "normal80","badonly80","total80",
                "normal40","badonly40","total40")

ptvarname = ptvar.translate(None,"[]_$")
ptsize = len(ptname)

mcexplist, mccountlist   = [0]*ptsize,[0]*ptsize
dataexplist, datacntlist = [0]*ptsize,[0]*ptsize

metcorr=0
#if options.year == 2016:
#    metcorr=1.02
#if options.year == 2017:
    #metcorr=1.04
#if options.year == 2018: #1.04
 #   metcorr=1.04


tag=""
egqual   = " && el_passTight[0] && ph_passTight[0]"
mugqual  = " && mu_passTight[0] && ph_passTight[0]"
selbase = baseel + metgt40  + egqual + elptgt%35  + invZ + ph_eb + el_eb + csvveto
selbasectrl1 = baseel + metgt40 + egqual + elptgt%35 + el_eb + massZ + ph_eb + csvveto ## Z peak CR
selbasectrl2 = basemu + mugqual + ph_eb + csvmed ### TTbar control reg

title = "electron faking photon in signal region"
if doControlRegion == "Z":
    selbase = selbasectrl1
    tag = "zpeakcr"
    title = "electron faking photon in Z peak control region"
if doControlRegion == "TT":
    selbase = selbasectrl2
    tag = "ttcr"
    title = "electron faking photon in ttbar control region"



hlist = [0]*ptsize

if options.dataFrame:
  for i in range(ptsize):
    hlist[i] = {}
    if "total" in ptname[i]: continue

    selection = getselstring(ptname[i])
    if metcorr:
          selectionfail = selection.replace("met_pt","met_pt*%g" %metcorr)
    else: selectionfail = selection

    ## configuration dicts
    hconf   = { "unblind":True, "doratio":True, "xlabel":"m(l,#gamma)"}
    hconfmc = { "xlabel":"m(l,#gamma)" }
    lconf = { "labelStyle" : "%i" %options.year,
              "extra_label": "%i Electron Channel" %options.year,
              "extra_label_loc": (.17,.82) }
    lgconf = {}

    ## output filename
    save_as = ("%s_%s_%ifailpix.pdf"            %(ptvarname,ptname[i],options.year),
                                                 options.outputDir, "base")
    save_as1 = ("%s_%s_%ifailpixphmatch.pdf"    %(ptvarname,ptname[i],options.year),
                                                 options.outputDir, "base")
    save_as2 = ("%s_%s_%ifailpixphnomatch.pdf"  %(ptvarname,ptname[i],options.year),
                                                 options.outputDir, "base")
    save_as3 = ("%s_%s_%ipasspixphnomatch.pdf"  %(ptvarname,ptname[i],options.year),
                                                 options.outputDir, "base")
    save_as4 = ("%s_%s_%ipasspix.pdf"           %(ptvarname,ptname[i],options.year),
                                                 options.outputDir, "base")
    save_as5 = ("%s_%s_%ipasspixphmatch.pdf"    %(ptvarname,ptname[i],options.year),
                                                 options.outputDir, "base")

    ### book histograms

    ## data failing pixel veto in reg D
    hlist[i]["fail"]        = samp.SetHisto1DFast("m_lep_ph",selectionfail+failpix,
                               (50,0,500), weight, hconf, lgconf, lconf, save_as)

    if doControlRegion:

      ## only relevant for data, looking at control region
      hlist[i]["pass"]      = samp.SetHisto1DFast("m_lep_ph",selection+passpix,
                               (50,0,500), weight, hconf, lgconf, lconf, save_as4)

      ## real photon in fake photon region. We need to subtract this from data
      hlist[i]["passmatch"] = samp.SetHisto1DFast("m_lep_ph",
                                selection+passpix+phmatch,       (50,0,500), weight,
                                hconfmc,lgconf, lconf, save_as5, data_exp = True)

    ## real photon events in fail pix region D
    hlist[i]["failmatch"]   = samp.SetHisto1DFast("m_lep_ph",
                                selectionfail+failpix+phmatch,   (50,0,500), weight,
                                hconfmc, lgconf, lconf, save_as1, data_exp = True)

    ## fakes in fail pix region D
    hlist[i]["failnomatch"] = samp.SetHisto1DFast("m_lep_ph",
                                selectionfail+failpix+nophmatch, (50,0,500), weight,
                                hconfmc, lgconf, lconf, save_as2, data_exp = True)

    ## true fakes
    hlist[i]["passnomatch"] = samp.SetHisto1DFast("m_lep_ph",
                                selection+passpix+nophmatch,     (50,0,500), weight,
                                hconfmc, lgconf, lconf, save_as3, data_exp = True)


for i in range(ptsize):

    if "total" in ptname[i]: continue

    ptnametag = ptname[i]
    ptnum = list(filter(str.isdigit, ptname[i]))
    if int(ptnum)>80:
        ptnametag = ptnametag.replace(ptnum, "80" )
    if "whole" in ptname[i]: ptnametag = ptnametag.lstrip("whole") ## FIXME
    filenametuple = (options.year, options.year, ptnametag)
    Na = get_param('data/efake/%i/parms_regA%i%s.txt'      %filenametuple)
    Nb = get_param('data/efake/%i/parms_regB%i%s.txt'      %filenametuple)
    Nda = get_param('data/efake/%i/parms_regA_data%i%s.txt'%filenametuple)
    Ndb = get_param('data/efake/%i/parms_regB_data%i%s.txt'%filenametuple)

    # region D
    #selstr = get_subselection(i)
    #selection = selbase+ selstr.replace("_VAR_", ptvar)

    if not options.dataFrame:

        selection = getselstring(ptname[i])
        selectionfail = selection.replace("met_pt","met_pt*%g" %metcorr)
        #selectionfail = selection

        samp.Draw("m_lep_ph",selection+failpix,           (50,0,500),
                {"weight":weight, "unblind":True, "doratio":True, "xlabel":"m(l,#gamma)"})
        count = samp.get_stack_count(includeData=True)

        samp.Draw("m_lep_ph",selection+failpix+phmatch,   (50,0,500),
                {"weight":weight, "xlabel":"m(l,#gamma)"})
        nonfakecount = samp.get_stack_count()

        samp.Draw("m_lep_ph",selection+failpix+nophmatch, (50,0,500),
                {"weight":weight, "xlabel":"m(l,#gamma)"})
        fakecount = samp.get_stack_count()

        samp.Draw("m_lep_ph",selection+passpix+nophmatch,(50,0,500),
                                {"weight":weight,  "xlabel":"m(l,#gamma)"})
        passnonfakecount = samp.get_stack_count()

    else:
        hlist[i]["fail"].DrawSave()
        count = samp.get_stack_count(includeData=True)
        samp.quiet=True

        hlist[i]["failmatch"].DrawSave()
        nonfakecount = samp.get_stack_count()

        hlist[i]["failnomatch"].DrawSave()
        fakecount = samp.get_stack_count()

        if doControlRegion:
            hlist[i]["pass"].DrawSave()
            passcount = samp.get_stack_count(includeData=True)

            hlist[i]["passmatch"].DrawSave()
            passnonfakecount = samp.get_stack_count()

        hlist[i]["passnomatch"].DrawSave()
        passfakecount = samp.get_stack_count()

    print("ALL COUNT")
    samp.print_stackresult(count)
    print("NONFAKE COUNT")
    samp.print_stackresult(nonfakecount)
    print("FAKE COUNT")
    samp.print_stackresult(fakecount)
    print("FAKE COUNT IN SR")
    samp.print_stackresult(passfakecount)

    if doControlRegion:
        print("NONFAKE COUNT in pass region")
        samp.print_stackresult(passnonfakecount)
        print("TOTAL COUNT in pass region")
        samp.print_stackresult(passcount)

    datadcount = ufloat(*count['Data'] ) -ufloat(*nonfakecount['NonEleFake'])\
                                        -ufloat(*nonfakecount['OtherEleFakeBackground'])

    datascount = 0
    if doControlRegion:
       datascount = ufloat(*passcount['Data'] ) -ufloat(*passnonfakecount['NonEleFake'])\
                                    -ufloat(*passnonfakecount['OtherEleFakeBackground'])
    mcdcount   = ufloat(*fakecount['TOTAL'])
    mcscount   = ufloat(*passfakecount['TOTAL'])

    ## calculate transfer factor and expectation value
    Na = ufloat(*Na)
    Nb = ufloat(*Nb)
    Nda = ufloat(*Nda)
    Ndb = ufloat(*Ndb)

    mcexp = mcdcount*Na/Nb
    dtexp = datadcount*Nda/Ndb
    print("MC: A {:g} B {:g} Data A {:g} B {:g} "\
                    .format(Na, Nb, Nda, Ndb))
    print("MC SR: {:g} MC EXP: {:g} Data SR: {:g} Data EXP: {:g}" \
                    .format(mcscount, mcexp, datascount, dtexp))

    factor=1.
    if "80" in ptname[i] and doControlRegion == "Z": factor=10. ## better visualization
    if "200" in ptname[i]: factor=10. ## better visualization
    mcexplist[i]   = mcexp      * factor
    mccountlist[i] = mcscount   * factor
    dataexplist[i] = dtexp      * factor
    datacntlist[i] = datascount * factor


### manually calculate total
for i in range(ptsize):
    if "total" not in ptname[i]:
        continue

    radikal = ptname[i].replace("total","")
    for j in range(ptsize):
        if radikal in ptname[j] and i != j and "whole" not in ptname[j]:
            mcexplist[i]  +=mcexplist[j]
            mccountlist[i]+=mccountlist[j]
            dataexplist[i]+=dataexplist[j]
            datacntlist[i]+=datacntlist[j]




xlabel = ["%i-%i" %r for r in pair(ptbins)]
xlabel = ptname
print(mccountlist)
if ptb:
    h1= ROOT.TH1F('h1',title,ptb[2]-1,ptb[0],ptb[1])
    h2= ROOT.TH1F('h2',title,ptb[2]-1,ptb[0],ptb[1])
    h3= ROOT.TH1F('h3',title,ptb[2]-1,ptb[0],ptb[1])
    h4= ROOT.TH1F('h4',title,ptb[2]-1,ptb[0],ptb[1])
else:
    h1= ROOT.TH1F('h1',title,ptsize,0,ptsize)
    h2= ROOT.TH1F('h2',title,ptsize,0,ptsize)
    h3= ROOT.TH1F('h3',title,ptsize,0,ptsize)
    h4= ROOT.TH1F('h4',title,ptsize,0,ptsize)

fillhist(h1, mccountlist, label=xlabel)
fillhist(h2, dataexplist, label=xlabel)
fillhist(h3, mcexplist, label=xlabel)
if doControlRegion:
    fillhist(h4, datacntlist, label=xlabel)

c1 = ROOT.TCanvas('c1','c1')
#h2.SetMarkerStyle(20)
#h2.SetMarkerSize(1.1)
#h2.SetMarkerColor(1)
#h2.SetLineColor(1)
#h2.SetLineWidth(2)

##data exp
h2.SetFillStyle(3005)
h2.SetFillColor(1)
##mc count
h1.SetLineColor(2)
h1.SetLineWidth(2)
##mc exp
h3.SetFillStyle(3004)
h3.SetFillColor(2)
##data count
h4.SetMarkerSize(1.1)
h4.SetMarkerStyle(22)
h4.SetMarkerColor(1)
h4.SetLineColor(1)

h1.GetXaxis().SetLabelSize(0.07)
h3.GetXaxis().SetTitle('photon pT and detector performance bins')

ymax = max([h.GetMaximum() for h in (h1,h2,h3,h4)])*1.3
h3.GetYaxis().SetRangeUser(0,ymax)

## drawing
h3.Draw('e2')
h2.Draw('e2 same')
h1.Draw("same")
if doControlRegion:
    h4.Draw("same")

t1 = ROOT.TLegend(0.75,0.75,0.88,0.88)
t1.AddEntry(h1,"MC Count","L")
t1.AddEntry(h3,"MC Est","f")
if doControlRegion:
    t1.AddEntry(h4,"Data Count","L")
t1.AddEntry(h2,"Data Est","f")
t1.Draw()
if doControlRegion=="Z" or options.year==2016:
    l1 = ROOT.TLatex()
    l1.SetNDC()
    l1.SetTextSize(0.04)
    l1.SetTextFont(52)
    l1.SetText(.20,.60, "10x")
    l1.Draw()

c1.SaveAs("~/public_html/fakeestimate%i%s.pdf" %(options.year, tag))
c1.SaveAs("~/public_html/fakeestimate%i%s.png" %(options.year, tag))
c1.SaveAs("~/public_html/fakeestimate%i%s.C"   %(options.year, tag))

