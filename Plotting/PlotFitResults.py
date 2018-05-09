import ROOT
ROOT.PyConfig.IgnoreCommandLineOptions = True
import sys, os
import re
import math
import selection_defs as defs
from SampleManager import SampleManager
from argparse import ArgumentParser
sys.path.append('/data/users/fengyb/CMSPLOTS')
from Plotter.myFunction import DrawGraphs

parser = ArgumentParser()

parser.add_argument( '--baseDir'       ,  dest='baseDir'       , default=None, help='Path to the fitted workspace')
parser.add_argument( '--outputDir'     ,  dest='outputDir'     , default=None, help='Path to the output file')
parser.add_argument( '--makeBkgTruth'  ,  dest='makeBkgTruth'  , default=False, action='store_true', help='Make background truth plots')

options = parser.parse_args()

ROOT.gROOT.SetBatch(False)
if options.outputDir is not None :
    ROOT.gROOT.SetBatch(True)
    if not os.path.isdir( options.outputDir ) :
        os.makedirs( options.outputDir )

_FILENAME = 'workspace_signal.root'
_OUTFILE = 'result.root'


def MakeParDistribution(doFit = True) :
     # fitted resonance mass, width, generator and parameter names
     LResMass   = [300, 350, 400, 450, 500, 600, 700, 800, 900, 1000, 1200, 1400, 1600, 1800, 2000]
     LResWidth  = ['0p01', '5']
     LGenerator = ['MadGraph', 'Pythia'] 
     LParName   = ['cb_mass', 'cb_sigma', 'cb_power1', 'cb_cut1', 'cb_power2', 'cb_cut2']

     GColor = {}
     GColor["0p01"]  = 2
     GColor["5"]     = 3

     GMStyle = {}
     GMStyle["0p01"] = 21
     GMStyle["5"]    = 22

     FuncFit = {}
     FuncFit["cb_mass"]  = "[0] + [1]*x"
     FuncFit["cb_sigma"] = "[0] + [1]*x"
     FuncFit["cb_cut1"]  = "[0] + [1]/x"

     FColor = {}
     FColor["0p01"] = 6
     FColor["5"]    = 7

     ifile = ROOT.TFile.Open( "%s/%s"%(options.baseDir, _FILENAME) ) 
     iws = ifile.Get("workspace_signal")
     print iws
     ofile = ROOT.TFile.Open( "%s/%s"%(options.outputDir, _OUTFILE), 'RECREATE')

     for igen in LGenerator:
          for iwidth in LResWidth:
              for ipar in LParName:
                  hvar = ROOT.TGraphErrors( len(LResMass) )
                  hvar.SetName('%s_%s_%s'%(ipar, iwidth, igen))
                  hvar.SetTitle('%s_%s_%s'%(ipar, iwidth, igen))

                  ipoint = 0
                  for imass in LResMass:
                      ipoint += 1
                      ivar = iws.var("%s_%sResonanceMass%s_width%s_mu_mt_fulltrans_base_EB"%(ipar, igen, imass, iwidth))
                      if ivar:
                         print ivar
                         hvar.SetPoint(ipoint, imass, ivar.getValV())
                         hvar.SetPointError(ipoint, 0, ivar.getError())
                      else:
                         print "can not find %s_%sResonanceMass%s_width%s_mu_mt_fulltrans_base_EB"%(ipar, igen, imass, iwidth)

                  #hvar.SetDirectory(ofile)
                  hvar.SetLineColor(int(GColor[iwidth]))
                  hvar.SetMarkerColor(int(GColor[iwidth]))
                  hvar.SetMarkerStyle(int(GMStyle[iwidth]))
                  hvar.SetMarkerSize(1)
                  hvar.Write()
         
                  # do fit
                  if ipar in FuncFit:
                     func = ROOT.TF1(ipar+iwidth, FuncFit[ipar], 150, 4000)
                     func.SetName('func_%s_%s_%s'%(ipar, iwidth, igen))
                     func.SetTitle('func_%s_%s_%s'%(ipar, iwidth, igen))
                     func.SetLineColor(int(FColor[iwidth]))
                     hvar.Fit(func)
                     func.Write()


def PlotParDistribution():
     ifile = ROOT.TFile.Open( "%s/%s"%(options.outputDir, _OUTFILE) )
     
     LGenerator = ['MadGraph', 'Pythia']
     for igen in LGenerator:
         
         g_mass1 = ifile.Get("cb_mass_0p01_%s"%igen)
         g_mass2 = ifile.Get("cb_mass_5_%s"%igen)   
         f_mass1 = ifile.Get("func_cb_mass_0p01_%s"%igen)
         f_mass2 = ifile.Get("func_cb_mass_5_%s"%igen)
         DrawGraphs([g_mass1, g_mass2], ["width0p01_%s"%igen, "width5_%s"%igen], 200, 2500, "gen_mass", 200, 2500, "cb_mass", "cb_mass_%s"%igen, dology = False, myfuncs= [f_mass1, f_mass2])

         g_width1 = ifile.Get("cb_sigma_0p01_%s"%igen)
         g_width2 = ifile.Get("cb_sigma_5_%s"%igen)
         f_width1 = ifile.Get("func_cb_sigma_0p01_%s"%igen)
         f_width2 = ifile.Get("func_cb_sigma_5_%s"%igen)
         DrawGraphs([g_width1, g_width2], ["width0p01_%s"%igen, "width5_%s"%igen], 200, 2500, "gen_mass", 0, 110, "cb_sigma", "cb_sigma_%s"%igen, dology = False, myfuncs = [f_width1, f_width2])

         g_cut11 = ifile.Get("cb_cut1_0p01_%s"%igen)
         g_cut12 = ifile.Get("cb_cut1_5_%s"%igen)
         f_cut11 = ifile.Get("func_cb_cut1_0p01_%s"%igen) 
         f_cut12 = ifile.Get("func_cb_cut1_5_%s"%igen)
         DrawGraphs([g_cut11, g_cut12], ["width0p01_%s"%igen, "width5_%s"%igen], 200, 2500, "gen_mass", 0,  1.0, "cb_cut1", "cb_cut1_%s"%igen, dology = False, myfuncs = [f_cut11, f_cut12])         

         g_power11 = ifile.Get("cb_power1_0p01_%s"%igen)
         g_power12 = ifile.Get("cb_power1_5_%s"%igen)
         DrawGraphs([g_power11, g_power12], ["width0p01_%s"%igen, "width5_%s"%igen], 200, 2500, "gen_mass", 0,  10.0, "cb_power1", "cb_power1_%s"%igen, dology = False)

         g_cut21 = ifile.Get("cb_cut2_0p01_%s"%igen)
         g_cut22 = ifile.Get("cb_cut2_5_%s"%igen)
         DrawGraphs([g_cut21, g_cut22], ["width0p01_%s"%igen, "width5_%s"%igen], 200, 2500, "gen_mass", 0,  4.0, "cb_cut2", "cb_cut2_%s"%igen, dology = False)

         g_power21 = ifile.Get("cb_power2_0p01_%s"%igen)
         g_power22 = ifile.Get("cb_power2_5_%s"%igen)
         DrawGraphs([g_power21, g_power22], ["width0p01_%s"%igen, "width5_%s"%igen], 200, 2500, "gen_mass", 0,  10.0, "cb_power2", "cb_power2_%s"%igen, dology = False)

if __name__ == "__main__":
     MakeParDistribution();
     PlotParDistribution();
