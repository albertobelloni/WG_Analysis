"""
Interactive script to plot data-MC histograms out of a set of trees.
"""

# Parse command-line options
from argparse import ArgumentParser
p = ArgumentParser()

                                                                                       
p.add_argument('--baseDir',     default=None,  type=str ,        dest='baseDir',         help='base directory for histograms')
p.add_argument('--outputDir',     default=None,  type=str ,        dest='outputDir',         help='output directory for histograms')
p.add_argument('--pythia',     default=False,  action='store_true' ,        dest='pythia',         help='use pythia directories')

options = p.parse_args()

import sys
import os
import re
import ROOT

from SampleManager import SampleManager

if options.outputDir is not None :
    ROOT.gROOT.SetBatch(True)

def main() :

    width_colors = { '0.01' : ROOT.kRed, '1' : ROOT.kBlack, '5' : ROOT.kGreen, '10' : ROOT.kBlue, '20' : ROOT.kMagenta }

    mass_colors = { 200 : ROOT.kBlack, 250 : ROOT.kRed, 300 : ROOT.kBlue, 350 : ROOT.kGreen, 400 : ROOT.kMagenta, 450 : ROOT.kOrange, 500 : ROOT.kCyan,
                   600 : ROOT.kBlack, 700 : ROOT.kRed, 800 : ROOT.kBlue, 900 : ROOT.kGreen, 1000 : ROOT.kMagenta, 1200 : ROOT.kOrange, 1400 : ROOT.kCyan,
                   1600 : ROOT.kBlack, 1800: ROOT.kRed, 2000 : ROOT.kBlue, 2200 : ROOT.kGreen, 2400 : ROOT.kMagenta, 2600 : ROOT.kOrange, 2800 : ROOT.kCyan, 3000 : ROOT.kBlack,
                   3500 : ROOT.kRed, 4000 : ROOT.kBlue, 

                  }

    sampMan       = SampleManager(options.baseDir, filename='validation.root', readHists=True)
    sampManMass   = SampleManager(options.baseDir, filename='validation.root', readHists=True)

    samples_lepnu = []
    samples_qq = []

    dirBaseName = 'ChargedResonance'
    if options.pythia :
        dirBaseName = 'PythiaChargedResonance'



    for dirname in os.listdir( options.baseDir ) :
        res = re.match( '%s_(WGToLNu|WGToJJ)_M(\d{3,4})_width(0p01|\d{1,2})' %dirBaseName, dirname )

        if res is not None :

            mass = int( res.group(2) )
            print dirname
            print res.group(3)
            if res.group(3) == '0p01' :
                width = '0.01'
            else :
                width = res.group(3)

            if res.group(1) == 'WGToLNu' :
                samples_lepnu.append( {'name' : dirname, 'mass' : mass, 'width' :  width} )
            elif res.group(1) == 'WGToJJ'  :
                samples_qq.append( {'name' : dirname, 'mass' : mass, 'width' :  width} )


            sampMan.AddSample( dirname, path=dirname, isActive=False, isSignal=True, sigLineStyle=1, sigLineWidth=1, plotColor=width_colors[width] )
            sampManMass.AddSample( dirname, path=dirname, isActive=False, isSignal=True, sigLineStyle=1, sigLineWidth=1, plotColor=mass_colors[mass] )

    if options.pythia :
        samples_qq = samples_lepnu

    # make the list of masses unique

    #draw_width_comp_hists( sampMan, 'm_lep_nu_ph', samples_lepnu, prefix='WidthCompare_ChargedResonance_WGToLNu', xlabel='Resonance Mass [GeV]' )
    #draw_width_comp_hists( sampMan, 'm_q_q_ph', samples_qq, prefix='WidthCompare_ChargedResonance_WGToJJ', xlabel='Resonance Mass [GeV]' )
    #draw_mass_comp_hists( sampManMass, 'm_lep_nu_ph', samples_lepnu, prefix='MassCompare_ChargedResonance_WGToLNu', xlabel='Resonance Mass [GeV]' )
    draw_mass_comp_hists( sampManMass, 'm_q_q_ph', samples_qq, prefix='MassCompare_ChargedResonance_WGToJJ', xlabel='Resonance Mass [GeV]' )

def draw_mass_comp_hists( sampMan, var, samples, prefix, xlabel ) :

    ylabel = 'Events'
    logy=True

    all_widths = []

    for samp in samples :
        all_widths.append( samp['width'] ) 

    all_widths = list( set( all_widths ) )


    for width in all_widths :
        used_samples = []

        for samp in samples :
            if samp['width'] == width :
                sampMan.activate_sample( samp['name'] )
                used_samples.append( ( samp['mass'], samp['name'] ) )
            else :
                sampMan.deactivate_sample( samp['name'] )

        used_samples.sort()

        print used_samples
        
        legend_order = [ x[1] for x in used_samples]

        xmin = 0
        xmax = 4000

        ymax = 5000000

        sampMan.DrawHist( var, xlabel=xlabel,ylabel= ylabel, label_config={'labelStyle' : None, 'labelLoc' : 'topright', 'extra_label' : 'Width = %s ' %width + r'%', 'extra_label_loc' : (0.15, 0.93) }, legend_config={'legendLoc' : 'Double', 'legendWiden' : 1.4, 'legendCompress' : 0.3, 'entryWidth' : 0.05, 'legendTranslateX' : 0.03, 'legendTranslateY' : 0.05, 'legendOrder' : legend_order}, logy=logy, ymin = 0.5, ymax=ymax )

        if options.outputDir is not None :
            width_name = width.replace('.', 'p' )
            name = '%s_width%s.pdf' %(prefix, width_name )
            sampMan.SaveStack( name, options.outputDir, 'base' )
        else :
            raw_input('continue')




def draw_width_comp_hists( sampMan, var, samples, prefix, xlabel) :

    ylabel = 'Events'
    logy=True

    all_masses = []

    for samp in samples :
        all_masses.append( samp['mass'] ) 

    all_masses = list( set( all_masses ) )


    for mass in all_masses :
        used_samples = []

        for samp in samples :
            if samp['mass'] == mass :
                sampMan.activate_sample( samp['name'] )
                used_samples.append( ( samp['width'], samp['name'] ) )
            else :
                sampMan.deactivate_sample( samp['name'] )

        used_samples.sort()

        print used_samples
        
        legend_order = [ x[1] for x in used_samples]

        xmin = 0
        xmax = 4000

        xmin = mass / 2
        xmax = mass*1.5

        #if mass >= 1000 :
        #    xmin = mass/1.3
        #    xmax = mass*1.2

        #xmax = mass + 4*(mass/10)
        #xmin = mass - 5*(mass/10)

        rebin = 2
        if mass >  1400 :
            rebin = 4

        ymax = 2500000



        sampMan.DrawHist( var, xlabel=xlabel,ylabel= ylabel, label_config={'labelStyle' : None, 'labelLoc' : 'topright', 'extra_label' : 'Generated Mass = %d GeV' %mass, 'extra_label_loc' : (0.15, 0.93) }, legend_config={'legendWiden' : 2.5, 'legendCompress' : 0.7, 'entryWidth' : 0.07, 'legendTranslateX' : 0.035, 'legendOrder' : legend_order}, logy=logy, ymin = 0.5, ymax=ymax, xmin=xmin, xmax=xmax, rebin=rebin )

        if options.outputDir is not None :
            name = '%s_M%d.pdf' %(prefix, mass )
            sampMan.SaveStack( name, options.outputDir, 'base' )
        else :
            raw_input('continue')


main()
