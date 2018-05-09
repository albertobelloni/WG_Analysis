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
    #ROOT.gROOT.SetBatch(True)
    if not os.path.isdir( options.outputDir ) :
        os.makedirs( options.outputDir )

_FILENAME = 'workspace_signal.root'
_OUTFILE = 'result.root'

def FitParDistribution():
     ifile = ROOT.TFile.Open( "%s/%s"%(options.outputDir, _OUTFILE) )
     
     LGenerator = ['MadGraph', 'Pythia']
     for igen in LGenerator:
         
         g_mass1 = ifile.Get("cb_mass_0p01_%s"%igen)
         g_mass2 = ifile.Get("cb_mass_5_%s"%igen)   

         fit_mass1 = ROOT.TF1("fit_mass_0p01_%s"%igen, "[0]+[1]*x", 1, 4000)
         fit_mass2 = ROOT.TF1("fit_mass_5_%s"%igen,    "[0]+[1]*x", 1, 4000)

         g_mass1.Fit(fit_mass1)
         g_mass1.Draw("AP")
         print "fit wider signal"
         g_mass2.Fit(fit_mass2)

         '''
         g_width1 = ifile.Get("cb_sigma_0p01_%s"%igen)
         g_width2 = ifile.Get("cb_sigma_5_%s"%igen)
         DrawGraphs([g_width1, g_width2], ["width0p01_%s"%igen, "width5_%s"%igen], [1, 2], 200, 2500, "gen_mass", 0, 110, "cb_sigma", "cb_sigma_%s"%igen, dology = False)

         g_cut11 = ifile.Get("cb_cut1_0p01_%s"%igen)
         g_cut12 = ifile.Get("cb_cut1_5_%s"%igen)
         DrawGraphs([g_cut11, g_cut12], ["width0p01_%s"%igen, "width5_%s"%igen], [1, 2], 200, 2500, "gen_mass", 0,  1.0, "cb_cut1", "cb_cut1_%s"%igen, dology = False)         

         g_power11 = ifile.Get("cb_power1_0p01_%s"%igen)
         g_power12 = ifile.Get("cb_power1_5_%s"%igen)
         DrawGraphs([g_power11, g_power12], ["width0p01_%s"%igen, "width5_%s"%igen], [1, 2], 200, 2500, "gen_mass", 0,  10.0, "cb_power1", "cb_power1_%s"%igen, dology = False)

         g_cut21 = ifile.Get("cb_cut2_0p01_%s"%igen)
         g_cut22 = ifile.Get("cb_cut2_5_%s"%igen)
         DrawGraphs([g_cut21, g_cut22], ["width0p01_%s"%igen, "width5_%s"%igen], [1, 2], 200, 2500, "gen_mass", 0,  4.0, "cb_cut2", "cb_cut2_%s"%igen, dology = False)

         g_power21 = ifile.Get("cb_power2_0p01_%s"%igen)
         g_power22 = ifile.Get("cb_power2_5_%s"%igen)
         DrawGraphs([g_power21, g_power22], ["width0p01_%s"%igen, "width5_%s"%igen], [1, 2], 200, 2500, "gen_mass", 0,  10.0, "cb_power2", "cb_power2_%s"%igen, dology = False)
         '''

if __name__ == "__main__":
     FitParDistribution();
