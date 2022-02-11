#!/usr/bin/env python
execfile("MakeBase.py")

#import ROOT
#ROOT.PyConfig.IgnoreCommandLineOptions = True
#import re
#import numpy as np
#import os
#import uuid
#import math
#import pickle
#import selection_defs as defs
#from uncertainties import ufloat
#from FitManager import FitManager
#from DrawConfig import DrawConfig
#import json
##ROOT.TVirtualFitter.SetMaxIterations( 100000 )
#ROOT.gStyle.SetOptStat(0)
#ROOT.Math.MinimizerOptions.SetDefaultMaxFunctionCalls( 100000)
#
#from SampleManager import SampleManager
#from argparse import ArgumentParser
#parser = ArgumentParser()
#
##parser.add_argument('--baseDirMuG',      default=None,           dest='baseDirMuG',         required=False, help='Path to muon base directory')
##parser.add_argument('--baseDirElG',      default=None,           dest='baseDirElG',         required=False, help='Path to electron base directory')
#parser.add_argument('--outputDir',      default=None,           dest='outputDir',         required=False, help='Output directory to write histograms')
#parser.add_argument('--data',           default=False,          dest='data',          required=False, action='store_true', help='Use data or MC')
#parser.add_argument('--doClosure',       default=False,   action='store_true',       dest='doClosure', required=False, help='make closure tests' )
#
#options = parser.parse_args()
#ROOT.gStyle.SetPalette(ROOT.kBird) 
#ROOT.gROOT.SetBatch(True)
#if options.outputDir is None :
#    options.outputDir = "Plots/" + __file__.rstrip(".py")
#if options.outputDir is not None :
#    if not os.path.isdir( options.outputDir ) :
#        os.makedirs( options.outputDir )
#
#_TREENAME = 'UMDNTuple/EventTree'
#_FILENAME = 'tree.root'
#_XSFILE   = 'cross_sections/photon16.py'
#_LUMI     = 36000
#
#baseDirElG='/data2/users/kakw/Resonances2016/LepGamma_elg_2019_12_12'
#
#
#base = 'ph_n==1 && el_n==1'
#baseeta = base + ' && ph_IsEB[0]'# + "&& ph_pt[0]>80"
#baseel = 'ph_n==1 && el_n==1 && el_pt35_n==1 && mu_n==0 && ph_IsEB[0]'
#passpix = '&& ph_hasPixSeed[0]==0'  #Pixel seed
#failpix = '&& ph_hasPixSeed[0]==1'
#ltmet = '&&met_pt<40'
#metgt40 = '&&met_pt>40'
#phpt50 = "&&ph_pt[0]>50"
#UNBLIND = "ph_hasPixSeed[0]==1 || met_pt<40"
#phtight = "&& ph_passTight[0]"
#phmedium = "&& ph_passMedium[0]"
#elpt40 = "&&el_pt[0]>40"
#phpt80 = "&&ph_pt[0]>80"
#eleta2p1 = "&&abs(el_eta[0])<2.1"
#invZ = '&& abs(m_lep_ph-91)>15'
#selZ = '&& abs(m_lep_ph-91)<15'
#nophmatch = "&& !(ph_truthMatchPh_dr[0]<ph_truthMatchEl_dr[0])"
#phmatch = "&& (ph_truthMatchPh_dr[0]<ph_truthMatchEl_dr[0])"
#weight = "PUWeight*NLOWeight"
weight = "NLOWeight"
ptb=None
ptbins = [0, 30, 40, 50, 60, 80, 2000]
#ptbins = [80, 2000]
ptvar = "ph_pt[0]"
selbase= baseel + metgt40  + "&&el_passTight[0] && ph_passMedium[0]" + elpt40 + el_eb + invZ
#(1.12+/-0.04)e+03 (1.4+/-0.4)e+03 (2.84+/-0.09)e+03
#1150+/-16 (8.1+/-2.3)e+02 (4.67+/-0.14)e+03
#(2.48+/-0.08)e+03 (2.1+/-0.6)e+03 (4.67+/-0.14)e+03
#(8.1+/-0.5)e+02 (7.2+/-2.0)e+02 (1.37+/-0.05)e+03 latest 2016
#if options.year ==2016: norm = [839., 450.] #data, MC 2016 old
if options.year ==2016: norm = [1370, 720.] #data, MC 2016
if options.year ==2017: norm = [2840., 1440.] #data, MC 2017
if options.year ==2018: norm = [4670., 2100.] #data, MC 2018


_SAMPCONF = 'Modules/Resonance%i_efake.py' %options.year
sampManElG.ReadSamples( _SAMPCONF )
samples=sampManElG


samples.CompareSelections("mt_res",[selbase+failpix+metgt40+"&&ph_pt[0]>80"],["Data"],(50,0,1000))
h1=samples[-1].hist.Clone()
h1.SetLineWidth(2)
h1.SetLineColor(2)

samples.Draw("mt_res",selbase+failpix+metgt40+"&&ph_pt[0]>80",(50,0,1000),{"weight":"NLOWeight"})
h=samples[-1].hist.Clone()
h.SetLineWidth(2)
h.SetLineColor(4)

lconf = {"labelStyle":"%i" %options.year,"extra_label":"%i Electron Channel" %options.year, "extra_label_loc":(.17,.82)}
samples.Draw("mt_res",selbase+nophmatch+passpix+metgt40+"&&ph_pt[0]>80",(50,0,1000),{"weight":"NLOWeight","ymax":norm[0]/5, "xlabel":"Reco mass"},{},lconf)
h1.Scale(norm[0]/h1.Integral())
h.Scale(norm[1]/h.Integral())
h1.Draw("same hist")
h.Draw("same hist")

l1=ROOT.TLegend(.65,.5,.95,.68)
l1.AddEntry(h,"MC shape MC est","l")
l1.AddEntry(h1,"data shape data est","l")
l1.SetBorderSize(0)
l1.Draw()

#samples.SaveStack("mt_res_efaketemplate.pdf","~/public_html","base")
samples.SaveStack("eftemplate%i.pdf"%options.year,"~/public_html","base")
