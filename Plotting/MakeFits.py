import ROOT
import uuid
import os
import time
import subprocess
ROOT.PyConfig.IgnoreCommandLineOptions = True
from argparse import ArgumentParser

parser = ArgumentParser()

parser.add_argument( '--baseDir',  dest='baseDir', required=True, help='path to workspace directory' )
parser.add_argument( '--outputDir',  dest='outputDir', required=False, default=None, help='name of output diretory for cards' )
parser.add_argument( '--doStatTests',  dest='doStatTests', default=False, action='store_true', help='run statistical tests of WGamma background' )
parser.add_argument( '--doWJetsTests',  dest='doWJetsTests', default=False, action='store_true', help='run tests of Wjets background' )
parser.add_argument( '--doFinalFit',  dest='doFinalFit', default=False, action='store_true', help='run fit to data and background' )
parser.add_argument( '--doVarOptimization',  dest='doVarOptimization', default=False, action='store_true', help='run variable optimization' )
parser.add_argument( '--doJetOptimization',  dest='doJetOptimization', default=False, action='store_true', help='run jet veto optimization' )
parser.add_argument( '--useHistTemplates',  dest='useHistTemplates', default=False, action='store_true', help='use histogram templates' )
parser.add_argument( '--useToySignal',  dest='useToySignal', default=False, action='store_true', help='use gaussian as signal' )
parser.add_argument( '--useToyBackground',  dest='useToyBackground', default=False, action='store_true', help='use exponential as background ' )
parser.add_argument( '--noRunCombine',  dest='noRunCombine', default=False, action='store_true', help='Dont run combine, use existing results' )
parser.add_argument( '--combineDir',  dest='combineDir', default=None, help='path to combine directory' )

options = parser.parse_args()

_LUMI = 36000.
_WLEPBR = (1.-0.6741)

def main() :

    ws_keys = { 
                'Wgamma' : 'workspace_wgamma',
                'top' : 'workspace_top',
                'signal' : 'workspace_signal',
                'wjets' : 'workspace_wjets',
                'data' : 'workspace_data',
              }


    #bins = ['mu_EB', 'mu_EE', 'el_EB', 'el_EE']
    bins = [
        {'channel' : 'mu', 'eta' : 'EB' },
        #{'channel' : 'mu', 'eta' : 'EE' },
        {'channel' : 'el', 'eta' : 'EB' },
        #{'channel' : 'el', 'eta' : 'EE' },
    ]

    if options.outputDir is not None :
        if not os.path.isdir( options.outputDir ) :
            os.makedirs( options.outputDir )


    signal_points = [200, 250, 300, 350, 400, 450, 500, 600, 700, 800, 900, 1000, 1200, 1400, 1600, 1800, 2000, 2200, 2400, 2600, 2800, 3000, 3500, 4000]
    #signal_points = [200, 250, 300, 350, 400, 450, 500, 600, 700, 800, 900, 1000, 1200, 1400, 1600, 1800, 2000, 2200, 2400, 2600, 2800]
    #signal_points = [300, 350, 400, 450, 500, 600, 700, 800, 900, 1000, 1200, 1400, 1600, 1800, 2000, 2200, 2400, 2600, 2800, 3000, 3500, 4000]
    #signal_points = [200, 250, 300, 350, 400, 450, 500]
    #signal_points = [1200, 1400, 1600, 1800]
    #signal_points = [200, 250, 300, 350, 400, 450, 500, 600, 700, 800, 900]
    #signal_points = [200, 250, 300, 350, 400, 450, 500, 600, 700, 800]

    signal_base = 'srhistpdf_MadGraphResonanceMass{pt}_width0p01' 
    if options.useHistTemplates :
        signal_base = 'srhist_MadGraphResonanceMass{pt}_width0p01' 

    #generate_card( options.baseDir, 'workspace_toy', 'workspace_signal', signal_pred, options.outputCard )
    if options.doMainLimits : 

    if options.doVarOptimization:

        var_opt = {}

        kine_vars = [ 
                     { 'name' : 'mt_incl_lepph_z', 'color' : ROOT.kBlue},
                     #{ 'name' : 'm_incl_lepph_z' , 'color' : ROOT.kRed },
                     #{ 'name' : 'mt_rotated' , 'color' : ROOT.kRed },
                     { 'name' : 'mt_fulltrans'   , 'color' : ROOT.kBlack },
                     { 'name' : 'mt_constrwmass' , 'color' : ROOT.kGreen },
                     { 'name' : 'ph_pt'          , 'color' : ROOT.kMagenta },
                   ]

        for var in kine_vars :
            var_opt[var['name']] = MakeLimits( mass_points=signal_points, 
                                              plot_var=var['name'], 
                                              backgrounds=[('Wgamma', ws_keys['Wgamma'])],
                                              signal_base=signal_base,
                                              signal_ws=ws_keys['signal'],
                                              baseDir=options.baseDir,
                                              bins=bins,
                                              outputDir='%s/%s/%s' %( options.outputDir, 'VarOpt', var['name'] ),
                                              ws_keys = ws_keys,
                                              useToySignal=options.useToySignal,
                                              useToyBackground=options.useToyBackground,
                                              useHistTemplates=options.useHistTemplates,
                                             )
                                                     

        for opt in var_opt.values() :
            opt.setup()

        combine_jobs = []
        for opt in var_opt.values() :
            combine_jobs += opt.get_combine_files() 

        if not options.noRunCombine :

            jdl_name = '%s/job_desc.jdl'  %( options.outputDir )
            make_jdl( combine_jobs, jdl_name )

            os.system( 'condor_submit %s' %jdl_name )

            wait_for_jobs( 'run_combine')

        results = {}
        for key, opt in var_opt.iteritems() :
            print key
            results[key] = opt.get_combine_results()

        print results


    #    for method in limit_methods :
    #        run_var_optimization( kine_vars, signal_points, bins, ws_keys, method, subdir='%s/Comb' %method)

    #if options.doJetOptimization : 
    #    run_jet_optimization( signal_points, bins, ws_keys )
    #if options.doStatTests :
    #    run_statistical_tests( options.baseDir, ws_keys['Wgamma'], 'dijet_Wgamma_mu_EB', 100, options.baseDir, suffix='mu_EB' )

    #if options.doFinalFit :
    #    generate_card( options.baseDir, ws_keys, etc )

    #if options.doWJetsTests :
    #    run_bkg_scale_test( options.baseDir, ws_keys['Wgamma'], 'dijet_Wgamma_mu_EB', ws_keys['wjets'] , 'dijet_prediction_wjets_mu_EB' )


    ##make_fit_workspace( options.baseDir, key_wgamma )
    ##workspace_toysignal = ROOT.RooWorkspace( 'workspace_toysignal' )
    ##make_gauss_signal( options.baseDir, workspace_toysignal )
    ##workspace_toysignal.writeToFile( '%s/%s.root' %( options.baseDir, workspace_toysignal.GetName() ) )
    ##generate_card( options.baseDir, 'workspace_toy', 'workspace_toysignal', signal_pred, options.outputCard )


def run_jet_optimization( signal_points, bins, ws_keys,method ) :

    dirname = 'JetOpt'

    tags = ['base', 'jetVeto']
    tag_colors = {'base' : ROOT.kBlack, 'jetVeto' : ROOT.kRed }
    tag_legend_entres = {'base': 'No jet veto', 'jetVeto' : 'Jet veto' }
    fit_var = 'mt_incl_lepph_z'

    output_dir = '%s/%s/%s/' %( options.outputDir, dirname, method )

    if not os.path.isdir( output_dir ):
        os.makedirs( output_dir )

        
    # -------------------------------------------------
    # Since we're blind, make toy data
    # -------------------------------------------------
    workspace_toy = ROOT.RooWorkspace( 'workspace_toy' )

    for tag in tags : 
        wgamma_entry = get_workspace_entry( 'Wgamma', 'mu', 'EB', fit_var, tag )
        top_entry  = get_workspace_entry( 'TTG', 'mu', 'EB', fit_var, tag )

        if options.useHistTemplates :
            wgamma_entry = wgamma_entry.replace( 'dijet', 'datahist' )
            top_entry    = top_entry.replace( 'dijet', 'datahist' )

        xvar_name = 'x_m'


        generate_toy_data( options.baseDir, [ws_keys['Wgamma'], ws_keys['top']], [wgamma_entry, top_entry], fit_var, workspace_toy, suffix='mu_%s_%s_EB' %(fit_var,tag) )

    workspace_toy.writeToFile( '%s/%s.root' %( output_dir, workspace_toy.GetName() ) )


    all_cards = {}
    for sig_pt in signal_points :
        for tag in tags :


            signal_base = 'srhistpdf_MadGraphResonanceMass%d_width0p01' %sig_pt
            if options.useHistTemplates :
                signal_base = 'srhist_MadGraphResonanceMass%d_width0p01' %sig_pt

            signal_dic = { 'name' : 'Resonance', 
                           'path' : '%s/%s.root' %( options.baseDir, ws_keys['signal'] ), 
                           'wsname' : ws_keys['signal'], 
                           'hist_base' : signal_base }

            data_dic = { 'path' : '%s/workspace_toy.root' %( output_dir ), 
                         'wsname' : 'workspace_toy', 
                         'hist_base' : 'toydata' }

            backgrounds = [ 
                           {'name' : 'Wgamma' , 'path' : '%s/%s.root' %( options.baseDir, ws_keys['Wgamma'] ), 'wsname' : ws_keys['Wgamma'], 'hist_base' : 'Wgamma' },
                           {'name' : 'TTG' , 'path' : '%s/%s.root' %( options.baseDir, ws_keys['top'] ), 'wsname' : ws_keys['top'], 'hist_base' : 'TTG' },
                          ]

            card_path = output_dir + 'jetopt_%s_%d.txt' %(tag, sig_pt )

            if not options.noRunCombine :

                for ibin in bins :
                    binid = '%s_%s' %( ibin['channel'], ibin['eta'] )

                    signal_entry = get_workspace_entry( signal_dic['hist_base'], ibin['channel'], ibin['eta'], fit_var, tag)
                    ofile = ROOT.TFile.Open( signal_dic['path'], 'READ' )
                    ws = ofile.Get( signal_dic['wsname'] )

                    signal_dic.setdefault('norm', {} )
                    signal_dic['norm'][binid] = ws.data( signal_entry ).sumEntries()

                    ofile.Close()

                    for bkg in backgrounds :

                        bkg_entry = get_workspace_entry( bkg['hist_base'], ibin['channel'], ibin['eta'], fit_var, tag)

                        ofile = ROOT.TFile.Open( bkg['path'], 'READ' )
                        ws = ofile.Get( bkg['wsname'] )
                        bkg.setdefault( 'norm', {} )
                        bkg['norm'][binid] = ws.data( bkg_entry.replace( 'dijet', 'datahist' )  ).sumEntries()
                        ofile.Close()
            

                generate_card( options.baseDir, card_path, data_dic, signal_dic, backgrounds, bins, fit_var, tag  )

            all_cards.setdefault(sig_pt, {})
            all_cards[sig_pt][tag] =  card_path 

    if options.combineDir is not None :

        jobs = []
        output_files = {}
        # this should be improved
        if method == 'AsymptoticLimits' or method == 'MaxLikelihoodFit' :

            for pt, tagdic in all_cards.iteritems() :

                output_files.setdefault( pt, {} )

                fname = '%s/run_combine_%d.sh' %(output_dir, pt)
                ofile = open( fname, 'w' )
                ofile.write( '#!/bin/tcsh\n' )
                ofile.write( 'cd %s \n' %options.combineDir ) 
                ofile.write( 'eval `scramv1 runtime -csh` \n' ) 
                    
                for tag, card in tagdic.iteritems() :

                    log_file = '%s/results_%s_%d.txt'%( output_dir, tag, pt )
                    if method == 'AsymptoticLimits' :
                        ofile.write( 'combine -M AsymptoticLimits -m %d -t 1 --rMin 0.1 --rMax 10 %s >& %s \n'  %( pt, card, log_file ))
                    if method == 'MaxLikelihoodFit' :
                        ofile.write( 'combine -M MaxLikelihoodFit -m %d -t -1 --expectSignal=1 %s --plots -n %s >> %s \n' %( pt, card, tag, log_file ) )
                    output_files[pt][tag] = log_file

                ofile.write( ' cd - \n' )
                ofile.write( 'echo "^.^ FINISHED ^.^" \n' )
                
                ofile.close()

                jobs.append(fname )

        #if method == 'HybridNew' :

        #    for pt, vardic in all_cards.iteritems() :

        #        output_files.setdefault( pt, {} )


        #        for var, card in vardic.iteritems() :

        #            fname = '%s/run_combine_%d_%s.sh' %(output_dir, pt, var)
        #            log_file = '%s/results_%s_%d.txt'%( output_dir, var, pt )
        #            output_files[pt][var] = log_file

        #            jobs.append(fname )

        #            if not options.noRunCombine :
        #                ofile = open( fname, 'w' )
        #                ofile.write( '#!/bin/tcsh\n' )
        #                ofile.write( 'cd %s \n' %options.combineDir ) 
        #                ofile.write( 'eval `scramv1 runtime -csh` \n' ) 
        #                
        #                ofile.write( 'combine -M HybridNew --frequentist --testStat LHC -H ProfileLikelihood --fork 1 -m %d %s > %s \n ' %( pt, card, log_file ) )

        #                ofile.write( ' cd - \n' )
        #                ofile.write( 'echo "^.^ FINISHED ^.^" \n' )
        #        
        #                os.system( 'chmod 777 %s/run_combine.sh' %(output_dir) )

        #                ofile.close()

        if not options.noRunCombine :
            jdl_name = '%s/job_desc.jdl'  %( output_dir )
            make_jdl( jobs, jdl_name )

            os.system( 'condor_submit %s' %jdl_name )

            wait_for_jobs( 'run_combine')

            os.system( '%s/run_combine.sh' %( output_dir ) )

        combine_results = {}
        for pt, tagdic in output_files.iteritems() :
            for tag, f in tagdic.iteritems() :
                result = process_combine_file( f, method )
                combine_results.setdefault(tag, {})
                if method == 'AsymptoticLimits' :
                    key = 'Expected 16.0%'
                    if key not in result :
                        print 'Could not find result key in ', f 
                        continue
                    combine_results[tag][pt] = float( result[key].split('<')[1] )

                    if options.useHistTemplates :
                        signal_entry = get_workspace_entry( 'srhist_MadGraphResonanceMass%d_width0p01' %pt, 'mu', 'EB', fit_var, tag )
                        ofile = ROOT.TFile.Open( '%s/%s.root' %( options.baseDir, ws_keys['signal']) , 'READ' ) 
                        ws = ofile.Get( 'workspace_signal' )
                        norm = ws.var( '%s_norm' %signal_entry ).getValV()
                        xs = ws.var( signal_entry.replace('srhist', 'cross_section') )

                        scale = ws.var(signal_entry.replace('srhist', 'scale' )).getValV()
                        total_events = ws.var(signal_entry.replace('srhist', 'total_events')).getValV()

                        efficiency = norm / ( scale * total_events )
                        print 'mass = %d, eff = %f ' %( pt, efficiency )

                        combine_results[tag][pt] = combine_results[tag][pt]*norm*1000*3.068/(_LUMI*efficiency)
                        print combine_results[tag][pt]

                                        
                #if method == 'HybridNew' :
                #    if result :
                #        combine_results[var][pt] = float( result['Limit'].split('<')[1].split('+')[0] )
                #    else :
                #        combine_results[var][pt] = 0

        limit_graphs = []
        limit_graphs_zoom = []
        leg = ROOT.TLegend(0.6, 0.75, 0.9, 0.9)
        for tag in tags :

            npoints = len( combine_results[tag] )
            limit_graph = ROOT.TGraph( npoints )
            limit_graph.SetTitle( '' )
            limit_graph.SetName( 'graph_%s' %tag )
            limit_graph.SetLineColor( tag_colors[tag] )
            limit_graph.SetLineWidth( 2 )
            limit_graph.SetMinimum( 0.1 )
            limit_graph.SetMaximum( 1500 )

            zoom_graph = ROOT.TGraph( 7 )
            zoom_graph.SetTitle( '' )
            zoom_graph.SetName( 'zoom_graph_%s' %tag )
            zoom_graph.SetLineColor( tag_colors[tag] )
            zoom_graph.SetLineWidth( 2 )
            zoom_graph.SetMinimum( 1 )
            zoom_graph.SetMaximum( 1500 )


            for idx, pt in enumerate(signal_points) :
                limit_graph.SetPoint( idx, pt, combine_results[tag][pt])

                if idx < 7 :
                    zoom_graph.SetPoint( idx, pt, combine_results[tag][pt])

            leg.AddEntry(limit_graph,  tag_legend_entres[tag], 'L' )
            limit_graphs.append( limit_graph )
            limit_graphs_zoom.append( zoom_graph )

        can = ROOT.TCanvas( 'limit_result' ,'Limit result' )
        can.SetTitle('')
        for idx, graph in enumerate(limit_graphs) :
            if idx == 0 :
                graph.Draw('AL')
            else :
                graph.Draw('Lsame')

            graph.GetXaxis().SetTitle( 'Resonance mass [GeV]' )
            graph.GetYaxis().SetTitle( 'Cross section limit [fb]' )

        leg.Draw()

        can.SetLogy()

        raw_input("cont")

        can.SaveAs( '%s/limit_results.pdf' %output_dir )

        can_zoom = ROOT.TCanvas( 'limit_graph_zoom', 'Limit result' )
        can_zoom.SetTitle('')
        for idx, graph in enumerate(limit_graphs_zoom) :
            if idx == 0 :
                graph.Draw('AL')
            else :
                graph.Draw('Lsame')

            graph.GetXaxis().SetTitle( 'Resonance mass [GeV]' )
            graph.GetYaxis().SetTitle( 'Cross section limit [fb]' )

        leg.Draw()
        can_zoom.SaveAs( '%s/limit_results_zoom.pdf' %output_dir )





def run_var_optimization( kine_vars, signal_points, bins, ws_keys, limit_method='AsymptoticLimits', subdir=None ) :

    dirname = 'VarOpt'
    if options.useToySignal :
        dirname += 'ToySignal'
    if options.useToyBackground :
        dirname += 'ToyBackground'


    backgrounds = [ 
        {'name' : 'Wgamma' , 'path' : '%s/%s.root' %( options.baseDir, ws_keys['Wgamma']), 'wsname' : ws_keys['Wgamma'], 'hist_base' : 'Wgamma' }
                  ]

    output_dir = '%s/%s/' %( options.outputDir, dirname )

    if subdir is not None :
        output_dir += '%s/' %subdir

    if not os.path.isdir( output_dir ):
        os.makedirs( output_dir )
        
    # -------------------------------------------------
    # Prepare workspaces
    # -------------------------------------------------
    # -------------------------------------------------
    # if testing using an exponential background, make that workspace
    # -------------------------------------------------
    if options.useToyBackground :
        make_exp_background( xvar_name, kine_vars, 50000, 
                            'workspace_exp_background', 'mu_%s_EB' %( var['name'] ), output_dir  )
        #---------------------
        # update backgrounds to use the toy distribution
        #---------------------
        backgrounds = [ 
            {'name' : 'Wgamma' , 'path' : '%s/workspace_exp_background.root' %output_dir, 'wsname' : 'workspace_exp_background', 'hist_base' : 'exp' }
                      ]

    # -------------------------------------------------
    # if testing using a gauss signal, make that workspace
    # -------------------------------------------------
    if options.useToySignal :
        make_gauss_signal( xvar_name, kine_vars, signal_points, 'workspase_gauss_signal', 'mu_EB', output_dir )

    signal_data = {}
    if options.useHistTemplates :
        # -------------------------------------------------
        # Get the normalization info from the samples
        # -------------------------------------------------
        signal_file = '%s/%s.root' %( options.baseDir, ws_keys['signal'])
        signal_data = get_signal_data( signal_file, ws_keys['signal'], signal_points, kine_vars, bins )

    else :
        # -------------------------------------------------
        # Copy the background funcitons and set variables to constant as needed
        # -------------------------------------------------
        if not options.useToyBackground :
            prepare_backround_functions( options.baseDir, ws_keys, ['Wgamma'], kine_vars, bins, output_dir )

    # -------------------------------------------------
    # Since we're blind, make toy data
    # -------------------------------------------------
    workspace_toy = ROOT.RooWorkspace( 'workspace_toy' )

    for var in kine_vars :
        for ibin in bins :
            binid = '%s_%s' %( ibin['channel'], ibin['eta'] )

            wgamma_entry = get_workspace_entry( 'Wgamma', ibin['channel'], ibin['eta'], var['name'] )
            wjets_entry  = get_workspace_entry( 'wjets', ibin['channel'], ibin['eta'], var['name'] )

            if options.useHistTemplates :
                wgamma_entry = wgamma_entry.replace( 'dijet', 'datahist' )

            # this could be improved
            if var['name'].count('pt') :
                xvar_name = 'x_pt'
            else :
                xvar_name = 'x_m'


            #generate_toy_data( options.baseDir, [ws_keys['Wgamma'], ws_keys['wjets']], [wgamma_entry, wjets_entry], xvar_name, workspace_toy, suffix='mu_EB' )
            if options.useToyBackground :
                generate_toy_data( output_dir, ['workspace_exp_background'], ['exp_%s_%s_%s' %(ibin['channel'], var['name'], ibin['eta'])], xvar_name, workspace_toy, suffix='%s_%s_base_%s' %( ibin['channel'], var['name'], ibin['eta']), data_norm=50000  )
            else :
                generate_toy_data( options.baseDir, [ws_keys['Wgamma']], [wgamma_entry], xvar_name, workspace_toy, suffix='%s_%s_base_%s' %(ibin['channel'], var['name'], ibin['eta'] ) )

    workspace_toy.writeToFile( '%s/%s.root' %( output_dir, workspace_toy.GetName() ) )

    data_dic = { 'path' : '%s/workspace_toy.root' %( output_dir ), 
                 'wsname' : 'workspace_toy', 
                 'hist_base' : 'toydata' }

    all_cards = {}

    bkg_ws_list = {}
    bkg_files = []
    for bkg in backgrounds :
        bkg_files.append(ROOT.TFile.Open( bkg['path'], 'READ' ))
        bkg_ws_list[bkg['name']] = bkg_files[-1].Get( bkg['wsname'] )

    signal_path =  '%s/%s.root' %( options.baseDir, ws_keys['signal'] )

    for sig_pt in signal_points :
        signal_base = 'srhistpdf_MadGraphResonanceMass%d_width0p01' %sig_pt
        if options.useHistTemplates :
            signal_base = 'srhist_MadGraphResonanceMass%d_width0p01' %sig_pt

        signal_dic = { 'name' : 'Resonance', 
                       'wsname' : ws_keys['signal'], 
                       'path' : signal_path,
                       'hist_base' : signal_base }

        if options.useToySignal :
            # replace the signal info with the toy info
            signal_dic = { 'name' : 'Resonance', 
                           'path' : '%s/%s.root' %( output_dir, 'workspace_gauss_signal' ), 
                           'wsname' : 'workspace_gauss_signal', 
                           'hist_base' : 'gauss_%d' %sig_pt }


        signal_dic['norm'] = {}
        for var in kine_vars :

            varname = var['name']

            card_path = output_dir + 'wgamma_test_%s_%d.txt' %(varname, sig_pt )
            for ibin in bins :

                binid = '%s_%s' %( ibin['channel'], ibin['eta'] )

                signal_dic['norm'][binid] = signal_data[signal_base][varname][binid]['norm']

                for bkg in backgrounds :

                    bkg_entry = get_workspace_entry( bkg['hist_base'], ibin['channel'], ibin['eta'], varname)

                    bkg.setdefault( 'norm', {} )
                    dist = bkg_ws_list[bkg['name']].data( bkg_entry.replace( 'dijet', 'datahist' )  )
                    bkg['norm'][binid] = dist.sumEntries()

            generate_card( options.baseDir, card_path, data_dic, signal_dic, backgrounds, bins, varname  )

            all_cards.setdefault(sig_pt, {})
            all_cards[sig_pt][varname] =  card_path 

    [b.Close() for b in bkg_files ]

    if options.combineDir is not None :

        jobs, output_files = write_combine_files(all_cards, output_dir, options.combineDir,  limit_method )

        if not options.noRunCombine :
            jdl_name = '%s/job_desc.jdl'  %( output_dir )
            make_jdl( jobs, jdl_name )

            os.system( 'condor_submit %s' %jdl_name )

            wait_for_jobs( 'run_combine')

            os.system( '%s/run_combine.sh' %( output_dir ) )

        signal_base = 'srhist_MadGraphResonanceMass{pt}_width0p01'
        combine_results = get_combine_results( output_files, signal_data, signal_base, limit_method )

        limit_graphs = []
        limit_graphs_zoom = []
        leg = ROOT.TLegend(0.6, 0.6, 0.9, 0.9)
        for var in kine_vars :

            npoints = len( combine_results[var['name']] )
            limit_graph = ROOT.TGraph( npoints )
            limit_graph.SetTitle( '' )
            limit_graph.SetName( 'graph_%s' %var['name'] )
            limit_graph.SetLineColor( var['color'] )
            limit_graph.SetLineWidth( 2 )
            limit_graph.SetMinimum( 0.1 )
            limit_graph.SetMaximum( 2000 )

            zoom_graph = ROOT.TGraph( 7 )
            zoom_graph.SetTitle( '' )
            zoom_graph.SetName( 'zoom_graph_%s' %var['name'] )
            zoom_graph.SetLineColor( var['color'] )
            zoom_graph.SetLineWidth( 2 )
            zoom_graph.SetMinimum( 1 )
            zoom_graph.SetMaximum( 2000 )


            for idx, pt in enumerate(signal_points) :
                limit_graph.SetPoint( idx, pt, combine_results[var['name']][pt])

                if idx < 7 :
                    zoom_graph.SetPoint( idx, pt, combine_results[var['name']][pt])

            leg.AddEntry(limit_graph,  var['name'], 'L' )
            limit_graphs.append( limit_graph )
            limit_graphs_zoom.append( zoom_graph )

        #eff_graph = ROOT.TGraph(len(combine_results['mt_incl_lepph_z']))
        #eff_graph.SetTitle( '' )
        #eff_graph.SetName( 'eff_graph' )
        #eff_graph.SetLineColor( ROOT.kBlack )
        #eff_graph.SetLineWidth( 2 )
        #eff_graph.SetMinimum( 0 )
        #eff_graph.SetMaximum( 0.2 )
        #for idx, pt in enumerate(signal_points) :
        #    eff_graph.SetPoint( idx, pt, signal_data['mt_incl_lepph_z'][pt]['mu_EB']['efficiency'])

        can = ROOT.TCanvas( 'limit_result' ,'Limit result' )
        can.SetTitle('')
        for idx, graph in enumerate(limit_graphs) :
            if idx == 0 :
                graph.Draw('AL')
            else :
                graph.Draw('Lsame')

            graph.GetXaxis().SetTitle( 'Resonance mass [GeV]' )
            graph.GetYaxis().SetTitle( 'Cross section limit [fb]' )

        leg.Draw()

        can.SetLogy()

        can.SaveAs( '%s/limit_results.pdf' %output_dir )

        can_zoom = ROOT.TCanvas( 'limit_graph_zoom', 'Limit result' )
        can_zoom.SetTitle('')
        for idx, graph in enumerate(limit_graphs_zoom) :
            if idx == 0 :
                graph.Draw('AL')
            else :
                graph.Draw('Lsame')

            graph.GetXaxis().SetTitle( 'Resonance mass [GeV]' )
            graph.GetYaxis().SetTitle( 'Cross section limit [fb]' )

        leg.Draw()
        can_zoom.SaveAs( '%s/limit_results_zoom.pdf' %output_dir )

        #can_eff = ROOT.TCanvas( 'eff_graph', 'Efficiency' )
        #can_eff.SetTitle('')
        #eff_graph.Draw('AL')

        #eff_graph.GetXaxis().SetTitle( 'Resonance mass [GeV]' )
        #eff_graph.GetYaxis().SetTitle( 'Selection efficiency' )

        #can_eff.SaveAs( '%s/efficiency.pdf' %output_dir )


#def get_combine_results( output_files, signal_data, signal_base, method ) : 
#
#    combine_results = {}
#    for pt, vardic in output_files.iteritems() :
#        for var, f in vardic.iteritems() :
#            result = process_combine_file( f, method )
#            combine_results.setdefault(var, {})
#            if method == 'AsymptoticLimits' :
#                key = 'Expected 16.0%'
#                if key not in result :
#                    print 'Could not find result key in ', f 
#                    continue
#                combine_results[var][pt] = float( result[key].split('<')[1] )
#
#                if options.useHistTemplates :
#
#                    signal_tag = signal_base.format(pt=pt)
#
#                    # the cross section is the same for any var and any bin, just grab one of them
#                    cross_section = signal_data[signal_tag].values()[0].values()[0]['cross_section']
#
#                    #combine_results[var][pt] = combine_results[var][pt]*signal_data[signal_base][var]['mu_EB']['norm']*1000*3.068/(_LUMI*signal_data[signal_base][var]['mu_EB']['efficiency'])
#                    combine_results[var][pt] = combine_results[var][pt]*cross_section*1000/( _WLEPBR )
#                    #combine_results[var][pt] = combine_results[var][pt]*signal_data[signal_base][var]['mu_EB']['norm']*3.068*1000/(signal_data[signal_base][var]['mu_EB']['efficiency']*_LUMI)
#                    print 'pt = %d, var = %s, result = %f' %( pt, var, combine_results[var][pt] )
#
#                                    
#            if method == 'HybridNew' :
#                if result :
#                    combine_results[var][pt] = float( result['Limit'].split('<')[1].split('+')[0] )
#                else :
#                    combine_results[var][pt] = 0
#
#    return combine_results

def write_combine_files(all_cards, output_dir, combine_dir,  method ) :

    jobs = []
    output_files = {}
    # this should be improved
    if method == 'AsymptoticLimits' or method == 'MaxLikelihoodFit' :

        for pt, vardic in all_cards.iteritems() :

            fname = '%s/run_combine_%d.sh' %(output_dir, pt)
            ofile = open( fname, 'w' )
            ofile.write( '#!/bin/tcsh\n' )
            ofile.write( 'cd %s \n' %options.combineDir ) 
            ofile.write( 'eval `scramv1 runtime -csh` \n' ) 
                
            for var, card in vardic.iteritems() :

                log_file = '%s/results_%s_%d.txt'%( output_dir, var, pt )
                if method == 'AsymptoticLimits' :
                    ofile.write( 'combine -M AsymptoticLimits -m %d -t 1 --rMin 0.1 --rMax 10 %s >& %s \n'  %( pt, card, log_file ))
                if method == 'MaxLikelihoodFit' :
                    ofile.write( 'combine -M MaxLikelihoodFit -m %d -t -1 --expectSignal=1 %s --plots -n %s >> %s \n' %( pt, card, var, log_file ) )

                output_files.setdefault( pt, {} )
                output_files[pt][var] = log_file

            ofile.write( ' cd - \n' )
            ofile.write( 'echo "^.^ FINISHED ^.^" \n' )
            
            ofile.close()

            jobs.append(fname )

    if method == 'HybridNew' :

        for pt, vardic in all_cards.iteritems() :
            for var, bindic in vardic.iteritems() :

                fname = '%s/run_combine_%s_%d.sh' %(output_dir, var, pt)
                log_file = '%s/results_%s_%d.txt'%( output_dir, var, pt)

                output_files.setdefault( pt, {} )
                output_files[pt][var] = log_file

                jobs.append(fname )

                if not options.noRunCombine :
                    ofile = open( fname, 'w' )
                    ofile.write( '#!/bin/tcsh\n' )
                    ofile.write( 'cd %s \n' %combine_dir ) 
                    ofile.write( 'eval `scramv1 runtime -csh` \n' ) 
                    
                    ofile.write( 'combine -M HybridNew --frequentist --testStat LHC -H ProfileLikelihood --fork 1 -m %d %s > %s \n ' %( pt, card, log_file ) )

                    ofile.write( ' cd - \n' )
                    ofile.write( 'echo "^.^ FINISHED ^.^" \n' )
            
                    os.system( 'chmod 777 %s/run_combine.sh' %(output_dir) )

                    ofile.close()


    return ( jobs, output_files )

#def prepare_backround_functions( baseDir, ws_keys, samp_list, kine_vars, bins, output_dir ) :
#
#    for samp in samp_list :
#
#        ofile = ROOT.TFile.Open( '%s/%s.root' %( baseDir, ws_keys[samp] ), 'READ' )
#
#        ws_in = ofile.Get( ws_keys[samp] )
#
#        ws_out = ROOT.RooWorkspace( ws_keys[samp] )
#
#        for var in kine_vars :
#            for ibin in bins :
#                ws_entry = get_workspace_entry( samp, ibin['channel'], ibin['eta'], var['name'] )
#
#                if options.useHistTemplates :
#                    datahist = ws_in.data(ws_entry.replace('dijet', 'datahist') )
#                    getattr( ws_out, 'import' ) ( datahist )
#                else :
#                    pdf = ws_in.pdf( ws_entry )
#                    power_var = ws_in.var( 'power_%s' %ws_entry )
#                    logcoef_var = ws_in.var( 'logcoef_%s' %ws_entry )
#
#                    power_var.setConstant()
#                    logcoef_var.setConstant()
#
#                    norm_var = ws_in.var( '%s_norm' %ws_entry )
#                    norm_var.setVal( norm_var.getValV() )
#                    #norm_var.setConstant()
#
#                    getattr( ws_out, 'import' ) ( pdf )
#                    getattr( ws_out, 'import' ) ( power_var )
#                    getattr( ws_out, 'import' ) ( logcoef_var )
#                    getattr( ws_out, 'import' ) ( norm_var )
#
#        ofile.Close()
#        ws_out.writeToFile( '%s/%s.root' %( output_dir, ws_keys[samp] ) )

#def get_signal_data( signal_file, ws_key, signal_points, plot_var, bins ) :
#
#    signal_data = {}
#
#    ofile = ROOT.TFile.Open( signal_file, 'READ'  )
#
#    signal_ws = ofile.Get( ws_key )
#
#    if plot_var.count('pt') :
#        xvar = signal_ws.var( 'x_pt' )
#    else :
#        xvar = signal_ws.var( 'x_m' )
#
#    for gen in ['MadGraph', 'Pythia'] :
#        for width in ['width5', 'width0p01'] :
#            for sig_pt in signal_points :
#
#                signal_base = 'srhist_%sResonanceMass%d_%s' %(gen, sig_pt, width )
#                signal_data.setdefault( signal_base, {} )
#                signal_data[signal_base].setdefault( plot_var, {} )
#                for ibin in bins :
#                    binid = '%s_%s' %( ibin['channel'], ibin['eta'] )
#
#                    signal_entry = get_workspace_entry( signal_base, ibin['channel'], ibin['eta'], plot_var)
#
#                    dist = signal_ws.data( signal_entry )
#
#                    if not dist :
#                        continue
#
#                    reco_events   = signal_ws.var( '%s_norm' %signal_entry ).getValV()
#                    scale         = signal_ws.var(signal_entry.replace('srhist', 'scale' )).getValV()
#                    total_events  = signal_ws.var(signal_entry.replace('srhist', 'total_events')).getValV()
#                    cross_section = signal_ws.var(signal_entry.replace('srhist', 'cross_section')).getValV()
#
#                    efficiency = reco_events / ( scale * total_events ) 
#                    signal_data[signal_base][plot_var].setdefault(binid,  {} )
#                    signal_data[signal_base][plot_var][binid]['norm'] = dist.sumEntries()
#                    signal_data[signal_base][plot_var][binid]['efficiency'] = efficiency
#                    signal_data[signal_base][plot_var][binid]['cross_section'] = cross_section
#
#    ofile.Close()
#    return signal_data

def get_workspace_entry( process, channel, eta, var, tag='base' ) : 

    if process == 'wjets' :
        return 'dijet_prediction_%s_%s_%s_%s_%s' %( process, channel, var, tag, eta )
    elif process == 'toydata' :
        return '%s_%s_%s_%s_%s' %( process,channel, var, tag, eta )
    elif process.count('ResonanceMass') :                        
        return '%s_%s_%s_%s_%s' %( process,channel, var, tag, eta )
    elif process.count( 'gauss') :                               
        return '%s_%s_%s_%s_%s' %( process,channel, var, tag, eta )
    elif process.count( 'exp') :                                 
        return '%s_%s_%s_%s_%s' %( process,channel, var, tag, eta )
    else :
        return 'dijet_%s_%s_%s_%s_%s' %( process,channel, var, tag, eta )

#def process_combine_file( fname, method ) :
#
#    ofile = open( fname, 'r' )
#
#    results = {}
#
#    if method == 'AsymptoticLimits' : 
#        for line in ofile :
#            if line.count(':') > 0 :
#                spline = line.split(':')
#                results[spline[0]] = spline[1].rstrip('\n')
#    if method == 'HybridNew' :
#        get_data = False
#        for line in ofile :
#            if line.count('-- Hybrid New -- ') :
#                get_data = True
#            if get_data and line.count(':') > 0 :
#                spline = line.split(':')
#                results[spline[0]] = spline[1].rstrip('\n')
#
#    ofile.close()
#
#    return results


def run_bkg_scale_test( baseDir, const_ws, const_hist, var_ws, var_hist ) :

    ofile_const = ROOT.TFile.Open( '%s/%s.root' %( baseDir, const_ws) )

    ws_const = ofile_const.Get( const_ws )

    ofile_var = ROOT.TFile.Open( '%s/%s.root' %( baseDir, var_ws) )

    ws_var = ofile_var.Get( var_ws )

    xvar = ws_const.var('x')

    norm_const = ws_const.var( '%s_norm' %const_hist)
    pdf_const = ws_const.pdf( const_hist)

    norm_var = ws_var.var( '%s_norm' %var_hist)
    pdf_var = ws_var.pdf( var_hist)

    npoints = 100

    power_res = ROOT.TGraph( npoints )
    power_res.SetName( 'power_res' )
    logcoef_res = ROOT.TGraph( npoints )
    logcoef_res.SetName( 'logcoef_res' )
    chi2_res = ROOT.TGraph( npoints )
    chi2_res.SetName( 'chi2_res' )

    power = ROOT.RooRealVar( 'power_fit', 'power', -9.9, -100, 100)
    logcoef = ROOT.RooRealVar( 'logcoef_fit', 'logcoef', -0.85, -10, 10 )
    func = 'TMath::Power(@0/13000, @1+@2*TMath::Log10(@0/13000))'  
    dijet_fit = ROOT.RooGenericPdf('dijet_fit', 'dijet', func, ROOT.RooArgList(xvar,power, logcoef))

    for i in range( 10, npoints+10 ) :

        var_frac = float(i) 

        tot  = norm_const.getValV() + var_frac*norm_var.getValV()


        vfrac = ROOT.RooRealVar( 'fraciton', 'fraciton', (var_frac*norm_var.getValV()/tot) )


        summed = ROOT.RooAddPdf( 'summed' ,'summed', ROOT.RooArgList( pdf_const, pdf_var ) , ROOT.RooArgList( vfrac ) )

        dataset_summed = summed.generate( ROOT.RooArgSet(xvar), int(tot), ROOT.RooCmdArg( 'Name', 0, 0, 0, 0, 'summed' ) )

        print 'Nevent Wgamma = %f, nevent Wjets = %f, fraction = %f, total = %f, vfrac = %g, ngenerated = %d' %( norm_const.getValV() , norm_var.getValV(), var_frac, tot, vfrac.getValV(), dataset_summed.numEntries() )

        #dijet_fit.fitTo( dataset_summed, ROOT.RooCmdArg('PrintLevel', -1 ) )
        dijet_fit.fitTo( dataset_summed )

        chi2 = dijet_fit.createChi2(dataset_summed.binnedClone(),ROOT.RooFit.Range(xvar.getMin(), xvar.getMax()) )
        chi2_res.SetPoint( i, var_frac, chi2.getVal() )
        power_res.SetPoint( i, var_frac, power.getValV() )
        logcoef_res.SetPoint( i, var_frac, logcoef.getValV() )



    chi2_res.Draw('AL')
    raw_input('cont')
    power_res.Draw('AL')
    raw_input('cont')
    logcoef_res.Draw('AL')
    raw_input('cont')
    
    #frame = xvar.frame()

    #dataset_summed.plotOn( frame )
    #pdf_const.plotOn( frame )
    #pdf_var.plotOn( frame )

    #frame.Draw()
    #raw_input('cont')



#def make_gauss_signal( xvar_name, kine_vars, masses, wsname, suffix, output_dir ) :
#
#    workspace = ROOT.RooWorkspace(wsname)
#    for var in kine_vars :
#        # this could be improved
#        if var['name'].count('pt') :
#            xvar_name = 'x_pt'
#        else :
#            xvar_name = 'x_m'
#        for mass in signal_points :
#
#            full_suffix = '%s_%d_%s' %(var['name'], mass, suffix)
#
#            xvar = ROOT.RooRealVar( xvar_name, xvar_name,  160, 1000 )
#
#            mean = ROOT.RooRealVar( 'mean_%s' %(full_suffix), 'mean', mass )
#            sigma = ROOT.RooRealVar( 'sigma_%s' %(full_suffix), 'sigma', mass*0.1 )
#            mean.setConstant()
#            sigma.setConstant()
#
#            #norm = ROOT.RooRealVar( 'gauss_%s_norm' %suffix, 'normalization', 100 )
#            #norm.setConstant()
#
#            signal = ROOT.RooGaussian( 'gauss_%s' %(full_suffix), 'signal', xvar, mean, sigma )
#
#            #getattr( workspace, 'import' ) ( dataset, ROOT.RooCmdArg('RenameAllNodes', 0, 0, 0, 0, 'gaussignal_%s' %suffix ) )
#            getattr( workspace, 'import' ) ( signal )
#            #getattr( workspace, 'import' ) ( norm )
#
#    workspace_gauss_signal.writeToFile( '%s/%s.root' %( output_dir, wsname ) )
#
#
#def make_exp_background( xvar_name, kine_vars, norm, wsname, suffix, output_dir ) :
#
#    workspace= ROOT.RooWorkspace(wsname)
#    for var in kine_vars :
#        # this could be improved
#        if var['name'].count('pt') :
#            xvar_name = 'x_pt'
#        else :
#            xvar_name = 'x_m'
#
#        xvar = ROOT.RooRealVar( xvar_name, xvar_name,  0, 1000 )
#
#        power = ROOT.RooRealVar( 'power_%s' %suffix, 'power', -0.01 )
#        power.setConstant()
#
#        background = ROOT.RooExponential( 'exp_%s' %suffix, 'background', xvar, power )
#        norm = ROOT.RooRealVar( 'exp_%s_norm' %suffix, 'background normalization', norm )
#        norm.setConstant()
#
#        #getattr( workspace, 'import' ) ( dataset, ROOT.RooCmdArg('RenameAllNodes', 0, 0, 0, 0, 'gaussignal_%s' %suffix ) )
#        getattr( workspace, 'import' ) ( background )
#        getattr( workspace, 'import' ) ( norm ) 
#
#    workspace.writeToFile( '%s/%s.root' %( output_dir, wsname ) )

def make_fit_workspace( baseDir, workspace_key ) :

    ofile = ROOT.TFile.Open( '%s/%s.root' %( baseDir, workspace_key ) )

    ws = ofile.Get( workspace_key )

    ws.Print()

    pdf_list = ws.allPdfs()
    print pdf_list.getSize()

    for i in range( 0, pdf_list.getSize() ) :
        print pdf_list[i]


#def generate_card( baseDir, outputCard, data_info, signal_info, backgrounds, bins, kine_var, tag='base' ) :
#
#    card_entries = []
#
#    section_divider = '-'*100
#
#    card_entries.append( 'imax %d number of bins' %len( bins ) )
#    card_entries.append( 'jmax %d number of backgrounds' %len( backgrounds) ) 
#    card_entries.append( 'kmax * number of nuisance parameters' )
#
#    card_entries.append( section_divider )
#
#    max_name_len = max( [len(x['name']) for x in backgrounds ] )
#    max_path_len = max( [len(x['path']) for x in backgrounds ] )
#
#    all_binids = []
#    #signal_norm = 1.0
#    for ibin in bins :
#        bin_id = '%s_%s' %( ibin['channel'], ibin['eta'] )
#        all_binids.append(bin_id)
#
#        signal_entry = get_workspace_entry( signal_info['hist_base'], ibin['channel'], ibin['eta'], kine_var, tag )
#        card_entries.append( 'shapes %s %s %s %s:%s' %( signal_info['name'], bin_id, signal_info['path'], signal_info['wsname'], signal_entry ) )
#
#        for bkgdic in backgrounds :
#            bkg_entry = get_workspace_entry( bkgdic['hist_base'], ibin['channel'], ibin['eta'], kine_var, tag )
#            if options.useHistTemplates :
#                bkg_entry = bkg_entry.replace('dijet', 'datahist' )
#            card_entries.append( 'shapes %s %s %s %s:%s' %( bkgdic['name'].ljust( max_name_len ), bin_id, bkgdic['path'].ljust( max_path_len ), bkgdic['wsname'], bkg_entry ) )
#            #card_entries.append( 'shapes %s %s %s %s:%s' %( bkgdic['name'].ljust( max_name_len ), bin_id, bkgdic['path'].ljust( max_path_len ), bkgdic['wsname'], bkg_entry.replace('dijet', 'datahist') ) )
#
#        data_entry = get_workspace_entry( data_info['hist_base'], ibin['channel'], ibin['eta'], kine_var, tag )
#        card_entries.append( 'shapes data_obs %s %s %s:%s' %( bin_id, data_info['path'], data_info['wsname'], data_entry ) )
#
#    card_entries.append( section_divider )
#
#    card_entries.append( 'bin          ' + '    '.join( all_binids ) )
#    card_entries.append( 'observation  ' + '    '.join( ['-1.0']*len(bins) ) )
#
#    card_entries.append( section_divider )
#
#    rate_entries = []
#    for ibin in bins :
#        bin_id = '%s_%s' %( ibin['channel'], ibin['eta'] )
#
#        rate_entries.append( str(signal_info['norm'][bin_id] ) )
#        for bkgdic in backgrounds :
#            rate_entries.append( str(bkgdic['norm'][bin_id]) )
#
#    bin_entries = []
#    for b in all_binids :
#        bin_entries += [b]*(len(backgrounds)+1)
#
#    card_entries.append( 'bin      ' + '    '.join(bin_entries )  )
#    card_entries.append( 'process  ' + '    '.join( ( [signal_info['name']] + [x['name'] for x in backgrounds])*len(bins) ) )
#    card_entries.append( 'process  ' + '    '.join( [str(x) for x in range(0, len(backgrounds) +1 ) ]*len(bins) ) )
#    #card_entries.append( 'rate     ' + '    '.join( [str(signal_norm), str(backgrounds[0]['norm']) ]*len(bins) ) )
#    card_entries.append( 'rate     ' + '    '.join( rate_entries )  )
#
#    card_entries.append( section_divider )
#
#    lumi_vals = ['1.05'] * (len(all_binids)*( len(backgrounds) + 1 ))
#    bkg_vals = (['-'] + ['1.05']*len(backgrounds) )*len(all_binids)
#    signal_vals = ( ['1.05'] + ['-']*len(backgrounds) )*len( all_binids) 
#
#    card_entries.append( 'lumi   lnN    ' + '    '.join(lumi_vals   ) )
#    card_entries.append( 'bkg    lnN    ' + '    '.join(bkg_vals    ) )
#    card_entries.append( 'signal lnN    ' + '    '.join(signal_vals ) )
#
#    card_entries.append( section_divider )
#
#    #for ibin in bins :
#    #    card_entries.append( 'logcoef_dijet_Wgamma_%s flatParam' %( ibin ) )
#    #    card_entries.append( 'power_dijet_Wgamma_%s flatParam' %( ibin ) )
#
#    if outputCard is not None :
#        print 'Write file ', outputCard
#        ofile = open( outputCard, 'w' ) 
#        for line in card_entries :
#            ofile.write( line + '\n' )
#        ofile.close()
#    else :
#        for ent in card_entries :
#            print ent


#def generate_toy_data( basedir, ws_key_list, hist_key_list, xvar_name, out_ws, suffix='', data_norm=None ) :
#
#    if not isinstance( ws_key_list, list ) :
#        ws_key_list = [ws_key_list]
#    if not isinstance( hist_key_list, list ) :
#        hist_key_list = [hist_key_list]
#
#    pdfs = []
#    norms = []
#    xvar = None
#    for ws_key, hist_key in zip( ws_key_list, hist_key_list ) :
#
#        full_path = '%s/%s.root' %( basedir, ws_key )
#        ofile = ROOT.TFile.Open( full_path )
#        print full_path
#
#        ws = ofile.Get( ws_key )
#
#        if options.useHistTemplates :
#            print hist_key
#            pdfs.append(ws.data( hist_key ))
#            norms.append(pdfs[-1].sumEntries())
#        else :
#            norms.append(ws.var( '%s_norm' %hist_key ).getValV())
#            pdfs.append(ws.pdf( hist_key ))
#
#        if xvar is None :
#            xvar = ws.var(xvar_name)
#
#        ofile.Close()
#
#    if len( pdfs ) == 1 :
#        if options.useHistTemplates :
#            dataset = ROOT.RooDataHist( pdfs[0], 'toydata_%s' %suffix )
#        else :
#            if data_norm is None :
#                norm = int(norms[0])
#            else :
#                norm = data_norm
#            dataset = pdfs[0].generate(ROOT.RooArgSet(xvar) , int(norm), ROOT.RooCmdArg( 'Name', 0, 0, 0, 0, 'toydata_%s' %suffix ) )
#    else :
#        total = sum( [int(x) for x in norms ] )
#
#        fractions = [ int(x)/total for x in norms ] 
#
#        if options.useHistTemplates :
#
#            dataset = ROOT.RooDataHist( pdfs[0], 'toydata_%s' %suffix )
#
#            for pdf in pdfs[1:] :
#                dataset.add( pdf )
#
#        else :
#
#            pdfList = ROOT.RooArgList()
#            for p in pdfs :
#                pdfList.add( p )
#
#            fracList = ROOT.RooArgList()
#            for f in fractions[:-1] :
#                myvar = ROOT.RooRealVar( str(uuid.uuid4()), str(uuid.uuid4()), f )
#                myvar.Print()
#                fracList.add( myvar )
#
#            summed = ROOT.RooAddPdf( 'summed' ,'summed', pdfList , fracList )
#            dataset = summed.generate( ROOT.RooArgSet(xvar), int(total), ROOT.RooCmdArg( 'Name', 0, 0, 0, 0, 'toydata_%s' %suffix ) )
#
#    # not clear why we have to rename here
#    #getattr( out_ws, 'import' ) ( dataset, ROOT.RooCmdArg('RenameAllNodes', 0, 0, 0, 0, 'toydata_%s' %suffix ) )
#    getattr( out_ws, 'import' ) ( dataset )

def run_statistical_tests( basedir, ws_key, hist_key, niter=100, outputDir=None, suffix='' ) :

    ofile = ROOT.TFile.Open( '%s/%s.root' %( basedir, ws_key ) )

    ws = ofile.Get( ws_key )

    normalization = ws.var( '%s_norm' %hist_key )
    pdf = ws.pdf( hist_key )
    xvar = ws.var('x')
    power = ws.var( 'power_%s' %hist_key )
    logcoef = ws.var( 'logcoef_%s' %hist_key )

    power_val = power.getValV()
    power_err = power.getErrorHi()
    logcoef_val = logcoef.getValV()
    logcoef_err = logcoef.getErrorHi()

    can_stat = ROOT.TCanvas( 'can_stat', '' )

    hist_stat   = ROOT.TH2F( 'hist_stat'  , 'hist_stat'  , 100, power_val - 5*power_err, power_val + 5*power_err, 100, logcoef_val - 5*logcoef_err, logcoef_val + 5*logcoef_err )

    for i in range( 0, niter ) :

        dataset = pdf.generate( ROOT.RooArgSet(xvar), normalization.getValV() )
        dataset.SetName( 'toydata%s%d' %(ws_key, i) )

        pdf.fitTo( dataset, ROOT.RooCmdArg('PrintLevel', -1 ) )

        #frame = xvar.frame()
        #dataset.plotOn(frame)
        #pdf.plotOn(frame)
        #frame.Draw()
        #raw_input('cont')

        hist_stat.Fill( power.getValV(), logcoef.getValV() )

    hist_stat.Draw('colz')
    raw_input('cont')

    prf = hist_stat.ProfileX( 'prf' )
    prf.Draw()
    raw_input('cont')

    if outputDir is not None :
        can_stat.SaveAs( '%s/wgamma_stat_%s.pdf' %( outputDir, suffix) )

def make_jdl( exe_list, output_file ) :

    base_dir = os.path.dirname( output_file )

    file_entries = []
    file_entries.append('#Use only the vanilla universe')
    file_entries.append('universe = vanilla')
    file_entries.append('# This is the executable to run.  If a script,')
    file_entries.append('#   be sure to mark it "#!<path to interp>" on the first line.')
    file_entries.append('# Filename for stdout, otherwise it is lost')
    #file_entries.append('output = stdout.txt')
    #file_entries.append('error = stderr.txt')
    file_entries.append('# Copy the submittor environment variables.  Usually required.')
    file_entries.append('getenv = True')
    file_entries.append('# Copy output files when done.  REQUIRED to run in a protected directory')
    file_entries.append('when_to_transfer_output = ON_EXIT_OR_EVICT')
    file_entries.append('priority=0')
    
    for exe in exe_list :
    
        file_entries.append('Executable = %s' %exe)
        file_entries.append('Initialdir = %s' %base_dir)
        file_entries.append('# This is the argument line to the Executable')
        file_entries.append('# Queue job')
        file_entries.append('queue')

    ofile = open( output_file, 'w' )

    for line in file_entries :
        ofile.write(  line + '\n' )

    ofile.close()

def wait_for_jobs( job_tag ) :

    while 1 :
        time.sleep(20)
        status = subprocess.Popen( ['condor_q'], stdout=subprocess.PIPE).communicate()[0]

        n_limits = 0

        for line in status.split('\n') :
            if line.count(job_tag ) :
                n_limits += 1

        if n_limits == 0 :
            return
        else :
            print '%d Jobs still running' %n_limits

class MakeLimits( ) :

    def __init__(self, **kwargs) :

        self.fail=False

        self.mass_points       = kwargs.get('mass_points', None )
        self.plot_var          = kwargs.get('plot_var'   , None )
        self.baseDir           = kwargs.get('baseDir'    , None )
        self.outputDir         = kwargs.get('outputDir'  , None )
        self.bins              = kwargs.get('bins'       , None )

        input_backgrounds = kwargs.get('backgrounds', None )
        self.signal_base  = kwargs.get('signal_base', None )
        self.signal_ws    = kwargs.get('signal_ws', None )

        self.useToySignal = kwargs.get('useToySignal', False )
        self.useToyBackground = kwargs.get('useToyBackground', False )
        self.useHistTemplates = kwargs.get('useHistTemplates', False )

        self.ws_tag = kwargs.get('wsTag', 'base' )
        self.method = kwargs.get('method', 'AsymptoticLimits' )

        if self.mass_points == None or not isinstance( self.mass_points, list ) :
            print 'Must provide a list of mass points' 
            self.fail = True;

        if self.plot_var == None or not isinstance( self.plot_var, str ) :
            print 'Must provide a plot var as a string' 
            self.fail = True

        if self.signal_base == None or not isinstance( self.signal_base, str ) :
            print 'Must provide a signal base as a string' 
            self.fail = True

        if self.signal_ws == None or not isinstance( self.signal_ws, str ) :
            print 'Must provide a signal workspace as a string' 
            self.fail = True

        if self.bins == None or not isinstance( self.bins, list ) :
            print 'Must provide a list of bins ' 
            self.fail = True

        self.backgrounds = []
        if input_backgrounds == None or not isinstance( input_backgrounds, list ) :
            print 'Must provide a list of backgrounds'
            self.fail = True
        else :
            for bkgname, wsname in input_backgrounds :
                self.backgrounds.append( {'name' : bkgname, 'path' : '%s/%s.root' %( self.baseDir, wsname ), 'wsname' : wsname, 'hist_base' : bkgname } )
        
        if self.baseDir == None or not isinstance( self.plot_var, str ) :
            print 'Must provide a base directory'
            self.fail = True

    def setup( self ):

        if self.fail :
            print 'Initialzation failed, will not setup'
            return

        if not os.path.isdir( self.outputDir ):
            os.makedirs( self.outputDir )
            
        # -------------------------------------------------
        # Prepare workspaces
        # -------------------------------------------------
        # -------------------------------------------------
        # if testing using an exponential background, make that workspace
        # -------------------------------------------------
        if options.useToyBackground :
            self.make_exp_background( xvar_name, kine_vars, 50000, 
                                'workspace_exp_background', 'mu_%s_EB' %( self.plot_var ), self.outputDir)
            #---------------------
            # update backgrounds to use the toy distribution
            #---------------------
            backgrounds = [ 
                {'name' : 'Wgamma' , 'path' : '%s/workspace_exp_background.root' %self.outputDir, 'wsname' : 'workspace_exp_background', 'hist_base' : 'exp' }
                          ]

        # -------------------------------------------------
        # if testing using a gauss signal, make that workspace
        # -------------------------------------------------
        if options.useToySignal :
            self.make_gauss_signal( xvar_name, kine_vars, self.mass_points, 'workspase_gauss_signal', 'mu_EB', self.outputDir)

        signal_data = {}
        if options.useHistTemplates :
            # -------------------------------------------------
            # Get the normalization info from the samples
            # -------------------------------------------------
            signal_file = '%s/%s.root' %( self.baseDir, self.signal_ws)
            signal_data = self.get_signal_data( signal_file, self.signal_ws,  self.mass_points, self.plot_var, self.bins )

        else :
            # -------------------------------------------------
            # Copy the background funcitons and set variables to constant as needed
            # -------------------------------------------------
            if not options.useToyBackground :
                self.prepare_backround_functions( options.baseDir, self.ws_keys, ['Wgamma'], kine_vars, bins, self.outputDir)

        # -------------------------------------------------
        # Since we're blind, make toy data
        # -------------------------------------------------
        workspace_toy = ROOT.RooWorkspace( 'workspace_toy' )

        for ibin in self.bins :
            binid = '%s_%s' %( ibin['channel'], ibin['eta'] )

            wgamma_entry = get_workspace_entry( 'Wgamma', ibin['channel'], ibin['eta'], self.plot_var )
            wjets_entry  = get_workspace_entry( 'wjets' , ibin['channel'], ibin['eta'], self.plot_var )

            if options.useHistTemplates :
                wgamma_entry = wgamma_entry.replace( 'dijet', 'datahist' )

            # this could be improved
            if self.plot_var.count('pt') :
                xvar_name = 'x_pt'
            else :
                xvar_name = 'x_m'


            #generate_toy_data( options.baseDir, [ws_keys['Wgamma'], ws_keys['wjets']], [wgamma_entry, wjets_entry], xvar_name, workspace_toy, suffix='mu_EB' )
            if options.useToyBackground :
                self.generate_toy_data( self.outputDir, ['workspace_exp_background'], ['exp_%s_%s_%s' %(ibin['channel'], self.plot_var, ibin['eta'])], xvar_name, workspace_toy, suffix='%s_%s_base_%s' %( ibin['channel'], self.plot_var, ibin['eta']), data_norm=50000  )
            else :
                self.generate_toy_data( options.baseDir, ['workspace_wgamma'], [wgamma_entry], xvar_name, workspace_toy, suffix='%s_%s_base_%s' %(ibin['channel'], self.plot_var, ibin['eta'] ) )

        workspace_toy.writeToFile( '%s/%s.root' %( self.outputDir, workspace_toy.GetName() ) )

        data_dic = { 'path' : '%s/workspace_toy.root' %( self.outputDir ), 
                     'wsname' : 'workspace_toy', 
                     'hist_base' : 'toydata' }

        self.all_cards = {}

        bkg_ws_list = {}
        bkg_files = []
        for bkg in self.backgrounds :
            bkg_files.append(ROOT.TFile.Open( bkg['path'], 'READ' ))
            bkg_ws_list[bkg['name']] = bkg_files[-1].Get( bkg['wsname'] )

        signal_path =  '%s/%s.root' %( options.baseDir, self.signal_ws )

        for sig_pt in self.mass_points :

            signal_name = self.signal_base.format(pt=sig_pt) 

            signal_dic = { 'name' : 'Resonance', 
                           'wsname' : self.signal_ws, 
                           'path' : signal_path,
                           'hist_base' : signal_name }

            if options.useToySignal :
                # replace the signal info with the toy info
                signal_dic = { 'name' : 'Resonance', 
                               'path' : '%s/%s.root' %( self.outputDir, 'workspace_gauss_signal' ), 
                               'wsname' : 'workspace_gauss_signal', 
                               'hist_base' : 'gauss_%d' %sig_pt }


            signal_dic['norm'] = {}
        
            card_path = '%s/wgamma_test_%s_%d.txt' %(self.outputDir, self.plot_var, sig_pt )
            for ibin in self.bins :

                binid = '%s_%s' %( ibin['channel'], ibin['eta'] )

                signal_dic['norm'][binid] = signal_data[signal_name][self.plot_var][binid]['norm']

                for bkg in self.backgrounds :

                    bkg_entry = get_workspace_entry( bkg['hist_base'], ibin['channel'], ibin['eta'], self.plot_var)

                    bkg.setdefault( 'norm', {} )
                    dist = bkg_ws_list[bkg['name']].data( bkg_entry.replace( 'dijet', 'datahist' )  )
                    bkg['norm'][binid] = dist.sumEntries()

            self.generate_card( options.baseDir, card_path, data_dic, signal_dic, self.backgrounds, self.bins, self.plot_var)

            self.all_cards.setdefault(sig_pt, {})
            self.all_cards[sig_pt][self.plot_var] =  card_path 

        [b.Close() for b in bkg_files ]


    def get_combine_files( self ) :

        if self.fail :
            print 'Initialzation failed, will not setup'
            return []

        print self.all_cards
        print self.method
        print self.outputDir

        jobs, output_files = write_combine_files(self.all_cards, self.outputDir, options.combineDir,  self.method )

        self.output_files = output_files

        return jobs

    def generate_card( self, baseDir, outputCard, data_info, signal_info, backgrounds, bins, kine_var, tag='base' ) :
    
        card_entries = []
    
        section_divider = '-'*100
    
        card_entries.append( 'imax %d number of bins' %len( bins ) )
        card_entries.append( 'jmax %d number of backgrounds' %len( backgrounds) ) 
        card_entries.append( 'kmax * number of nuisance parameters' )
    
        card_entries.append( section_divider )
    
        max_name_len = max( [len(x['name']) for x in backgrounds ] )
        max_path_len = max( [len(x['path']) for x in backgrounds ] )
    
        all_binids = []
        #signal_norm = 1.0
        for ibin in bins :
            bin_id = '%s_%s' %( ibin['channel'], ibin['eta'] )
            all_binids.append(bin_id)
    
            signal_entry = get_workspace_entry( signal_info['hist_base'], ibin['channel'], ibin['eta'], kine_var, tag )
            card_entries.append( 'shapes %s %s %s %s:%s' %( signal_info['name'], bin_id, signal_info['path'], signal_info['wsname'], signal_entry ) )
    
            for bkgdic in backgrounds :
                bkg_entry = get_workspace_entry( bkgdic['hist_base'], ibin['channel'], ibin['eta'], kine_var, tag )
                if options.useHistTemplates :
                    bkg_entry = bkg_entry.replace('dijet', 'datahist' )
                card_entries.append( 'shapes %s %s %s %s:%s' %( bkgdic['name'].ljust( max_name_len ), bin_id, bkgdic['path'].ljust( max_path_len ), bkgdic['wsname'], bkg_entry ) )
                #card_entries.append( 'shapes %s %s %s %s:%s' %( bkgdic['name'].ljust( max_name_len ), bin_id, bkgdic['path'].ljust( max_path_len ), bkgdic['wsname'], bkg_entry.replace('dijet', 'datahist') ) )
    
            data_entry = get_workspace_entry( data_info['hist_base'], ibin['channel'], ibin['eta'], kine_var, tag )
            card_entries.append( 'shapes data_obs %s %s %s:%s' %( bin_id, data_info['path'], data_info['wsname'], data_entry ) )
    
        card_entries.append( section_divider )
    
        card_entries.append( 'bin          ' + '    '.join( all_binids ) )
        card_entries.append( 'observation  ' + '    '.join( ['-1.0']*len(bins) ) )
    
        card_entries.append( section_divider )
    
        rate_entries = []
        for ibin in bins :
            bin_id = '%s_%s' %( ibin['channel'], ibin['eta'] )
    
            rate_entries.append( str(signal_info['norm'][bin_id] ) )
            for bkgdic in backgrounds :
                rate_entries.append( str(bkgdic['norm'][bin_id]) )
    
        bin_entries = []
        for b in all_binids :
            bin_entries += [b]*(len(backgrounds)+1)
    
        card_entries.append( 'bin      ' + '    '.join(bin_entries )  )
        card_entries.append( 'process  ' + '    '.join( ( [signal_info['name']] + [x['name'] for x in backgrounds])*len(bins) ) )
        card_entries.append( 'process  ' + '    '.join( [str(x) for x in range(0, len(backgrounds) +1 ) ]*len(bins) ) )
        #card_entries.append( 'rate     ' + '    '.join( [str(signal_norm), str(backgrounds[0]['norm']) ]*len(bins) ) )
        card_entries.append( 'rate     ' + '    '.join( rate_entries )  )
    
        card_entries.append( section_divider )
    
        lumi_vals = ['1.05'] * (len(all_binids)*( len(backgrounds) + 1 ))
        bkg_vals = (['-'] + ['1.05']*len(backgrounds) )*len(all_binids)
        signal_vals = ( ['1.05'] + ['-']*len(backgrounds) )*len( all_binids) 
    
        card_entries.append( 'lumi   lnN    ' + '    '.join(lumi_vals   ) )
        card_entries.append( 'bkg    lnN    ' + '    '.join(bkg_vals    ) )
        card_entries.append( 'signal lnN    ' + '    '.join(signal_vals ) )
    
        card_entries.append( section_divider )
    
        #for ibin in bins :
        #    card_entries.append( 'logcoef_dijet_Wgamma_%s flatParam' %( ibin ) )
        #    card_entries.append( 'power_dijet_Wgamma_%s flatParam' %( ibin ) )
    
        if outputCard is not None :
            print 'Write file ', outputCard
            ofile = open( outputCard, 'w' ) 
            for line in card_entries :
                ofile.write( line + '\n' )
            ofile.close()
        else :
            for ent in card_entries :
                print ent

    def generate_toy_data( self, basedir, ws_key_list, hist_key_list, xvar_name, out_ws, suffix='', data_norm=None ) :
    
        if not isinstance( ws_key_list, list ) :
            ws_key_list = [ws_key_list]
        if not isinstance( hist_key_list, list ) :
            hist_key_list = [hist_key_list]
    
        pdfs = []
        norms = []
        xvar = None
        for ws_key, hist_key in zip( ws_key_list, hist_key_list ) :
    
            full_path = '%s/%s.root' %( basedir, ws_key )
            ofile = ROOT.TFile.Open( full_path )
            print full_path
    
            ws = ofile.Get( ws_key )
    
            if options.useHistTemplates :
                print hist_key
                pdfs.append(ws.data( hist_key ))
                norms.append(pdfs[-1].sumEntries())
            else :
                norms.append(ws.var( '%s_norm' %hist_key ).getValV())
                pdfs.append(ws.pdf( hist_key ))
    
            if xvar is None :
                xvar = ws.var(xvar_name)
    
            ofile.Close()
    
        if len( pdfs ) == 1 :
            if options.useHistTemplates :
                dataset = ROOT.RooDataHist( pdfs[0], 'toydata_%s' %suffix )
            else :
                if data_norm is None :
                    norm = int(norms[0])
                else :
                    norm = data_norm
                dataset = pdfs[0].generate(ROOT.RooArgSet(xvar) , int(norm), ROOT.RooCmdArg( 'Name', 0, 0, 0, 0, 'toydata_%s' %suffix ) )
        else :
            total = sum( [int(x) for x in norms ] )
    
            fractions = [ int(x)/total for x in norms ] 
    
            if options.useHistTemplates :
    
                dataset = ROOT.RooDataHist( pdfs[0], 'toydata_%s' %suffix )
    
                for pdf in pdfs[1:] :
                    dataset.add( pdf )
    
            else :
    
                pdfList = ROOT.RooArgList()
                for p in pdfs :
                    pdfList.add( p )
    
                fracList = ROOT.RooArgList()
                for f in fractions[:-1] :
                    myvar = ROOT.RooRealVar( str(uuid.uuid4()), str(uuid.uuid4()), f )
                    myvar.Print()
                    fracList.add( myvar )
    
                summed = ROOT.RooAddPdf( 'summed' ,'summed', pdfList , fracList )
                dataset = summed.generate( ROOT.RooArgSet(xvar), int(total), ROOT.RooCmdArg( 'Name', 0, 0, 0, 0, 'toydata_%s' %suffix ) )
    
        # not clear why we have to rename here
        #getattr( out_ws, 'import' ) ( dataset, ROOT.RooCmdArg('RenameAllNodes', 0, 0, 0, 0, 'toydata_%s' %suffix ) )
        getattr( out_ws, 'import' ) ( dataset )

    def prepare_backround_functions( self, baseDir, ws_keys, samp_list, kine_vars, bins, output_dir ) :
    
        for samp in samp_list :
    
            ofile = ROOT.TFile.Open( '%s/%s.root' %( baseDir, ws_keys[samp] ), 'READ' )
    
            ws_in = ofile.Get( ws_keys[samp] )
    
            ws_out = ROOT.RooWorkspace( ws_keys[samp] )
    
            for var in kine_vars :
                for ibin in bins :
                    ws_entry = get_workspace_entry( samp, ibin['channel'], ibin['eta'], var['name'] )
    
                    if options.useHistTemplates :
                        datahist = ws_in.data(ws_entry.replace('dijet', 'datahist') )
                        getattr( ws_out, 'import' ) ( datahist )
                    else :
                        pdf = ws_in.pdf( ws_entry )
                        power_var = ws_in.var( 'power_%s' %ws_entry )
                        logcoef_var = ws_in.var( 'logcoef_%s' %ws_entry )
    
                        power_var.setConstant()
                        logcoef_var.setConstant()
    
                        norm_var = ws_in.var( '%s_norm' %ws_entry )
                        norm_var.setVal( norm_var.getValV() )
                        #norm_var.setConstant()
    
                        getattr( ws_out, 'import' ) ( pdf )
                        getattr( ws_out, 'import' ) ( power_var )
                        getattr( ws_out, 'import' ) ( logcoef_var )
                        getattr( ws_out, 'import' ) ( norm_var )
    
            ofile.Close()
            ws_out.writeToFile( '%s/%s.root' %( output_dir, ws_keys[samp] ) )

    def get_signal_data( self, signal_file, ws_key, signal_points, plot_var, bins ) :
    
        signal_data = {}
    
        ofile = ROOT.TFile.Open( signal_file, 'READ'  )
    
        signal_ws = ofile.Get( ws_key )
    
        if plot_var.count('pt') :
            xvar = signal_ws.var( 'x_pt' )
        else :
            xvar = signal_ws.var( 'x_m' )
    
        for gen in ['MadGraph', 'Pythia'] :
            for width in ['width5', 'width0p01'] :
                for sig_pt in signal_points :
    
                    signal_base = 'srhist_%sResonanceMass%d_%s' %(gen, sig_pt, width )
                    signal_data.setdefault( signal_base, {} )
                    signal_data[signal_base].setdefault( plot_var, {} )
                    for ibin in bins :
                        binid = '%s_%s' %( ibin['channel'], ibin['eta'] )
    
                        signal_entry = get_workspace_entry( signal_base, ibin['channel'], ibin['eta'], plot_var)
    
                        dist = signal_ws.data( signal_entry )
    
                        if not dist :
                            continue
    
                        reco_events   = signal_ws.var( '%s_norm' %signal_entry ).getValV()
                        scale         = signal_ws.var(signal_entry.replace('srhist', 'scale' )).getValV()
                        total_events  = signal_ws.var(signal_entry.replace('srhist', 'total_events')).getValV()
                        cross_section = signal_ws.var(signal_entry.replace('srhist', 'cross_section')).getValV()
    
                        efficiency = reco_events / ( scale * total_events ) 
                        signal_data[signal_base][plot_var].setdefault(binid,  {} )
                        signal_data[signal_base][plot_var][binid]['norm'] = dist.sumEntries()
                        signal_data[signal_base][plot_var][binid]['efficiency'] = efficiency
                        signal_data[signal_base][plot_var][binid]['cross_section'] = cross_section
    
        ofile.Close()
        return signal_data

    def make_gauss_signal(self, xvar_name, kine_vars, masses, wsname, suffix, output_dir ) :
    
        workspace = ROOT.RooWorkspace(wsname)
        for var in kine_vars :
            # this could be improved
            if var['name'].count('pt') :
                xvar_name = 'x_pt'
            else :
                xvar_name = 'x_m'
            for mass in signal_points :
    
                full_suffix = '%s_%d_%s' %(var['name'], mass, suffix)
    
                xvar = ROOT.RooRealVar( xvar_name, xvar_name,  160, 1000 )
    
                mean = ROOT.RooRealVar( 'mean_%s' %(full_suffix), 'mean', mass )
                sigma = ROOT.RooRealVar( 'sigma_%s' %(full_suffix), 'sigma', mass*0.1 )
                mean.setConstant()
                sigma.setConstant()
    
                #norm = ROOT.RooRealVar( 'gauss_%s_norm' %suffix, 'normalization', 100 )
                #norm.setConstant()
    
                signal = ROOT.RooGaussian( 'gauss_%s' %(full_suffix), 'signal', xvar, mean, sigma )
    
                #getattr( workspace, 'import' ) ( dataset, ROOT.RooCmdArg('RenameAllNodes', 0, 0, 0, 0, 'gaussignal_%s' %suffix ) )
                getattr( workspace, 'import' ) ( signal )
                #getattr( workspace, 'import' ) ( norm )
    
        workspace_gauss_signal.writeToFile( '%s/%s.root' %( output_dir, wsname ) )
    
    
    def make_exp_background(self, xvar_name, kine_vars, norm, wsname, suffix, output_dir ) :
    
        workspace= ROOT.RooWorkspace(wsname)
        for var in kine_vars :
            # this could be improved
            if var['name'].count('pt') :
                xvar_name = 'x_pt'
            else :
                xvar_name = 'x_m'
    
            xvar = ROOT.RooRealVar( xvar_name, xvar_name,  0, 1000 )
    
            power = ROOT.RooRealVar( 'power_%s' %suffix, 'power', -0.01 )
            power.setConstant()
    
            background = ROOT.RooExponential( 'exp_%s' %suffix, 'background', xvar, power )
            norm = ROOT.RooRealVar( 'exp_%s_norm' %suffix, 'background normalization', norm )
            norm.setConstant()
    
            #getattr( workspace, 'import' ) ( dataset, ROOT.RooCmdArg('RenameAllNodes', 0, 0, 0, 0, 'gaussignal_%s' %suffix ) )
            getattr( workspace, 'import' ) ( background )
            getattr( workspace, 'import' ) ( norm ) 
    
        workspace.writeToFile( '%s/%s.root' %( output_dir, wsname ) )

    def get_combine_results( self ) : 
    
        combine_results = {}
        for pt, vardic in self.output_files.iteritems() :
            for var, f in vardic.iteritems() :
                result = self.process_combine_file( f )
                combine_results.setdefault(var, {})
                if self.method == 'AsymptoticLimits' :
                    key = 'Expected 16.0%'
                    if key not in result :
                        print 'Could not find result key in ', f 
                        continue
                    combine_results[var][pt] = float( result[key].split('<')[1] )
    
                    if options.useHistTemplates :
    
                        signal_tag = self.signal_base.format(pt=pt)
    
                        # the cross section is the same for any var and any bin, just grab one of them
                        cross_section = signal_data[signal_tag].values()[0].values()[0]['cross_section']
    
                        #combine_results[var][pt] = combine_results[var][pt]*signal_data[signal_base][var]['mu_EB']['norm']*1000*3.068/(_LUMI*signal_data[signal_base][var]['mu_EB']['efficiency'])
                        combine_results[var][pt] = combine_results[var][pt]*cross_section*1000/( _WLEPBR )
                        #combine_results[var][pt] = combine_results[var][pt]*signal_data[signal_base][var]['mu_EB']['norm']*3.068*1000/(signal_data[signal_base][var]['mu_EB']['efficiency']*_LUMI)
                        print 'pt = %d, var = %s, result = %f' %( pt, var, combine_results[var][pt] )
    
                                        
                if self.method == 'HybridNew' :
                    if result :
                        combine_results[var][pt] = float( result['Limit'].split('<')[1].split('+')[0] )
                    else :
                        combine_results[var][pt] = 0

        return combine_results

    def process_combine_file( self, fname ) :
    
        ofile = open( fname, 'r' )
    
        results = {}
    
        if self.method == 'AsymptoticLimits' : 
            for line in ofile :
                if line.count(':') > 0 :
                    spline = line.split(':')
                    results[spline[0]] = spline[1].rstrip('\n')
        if self.method == 'HybridNew' :
            get_data = False
            for line in ofile :
                if line.count('-- Hybrid New -- ') :
                    get_data = True
                if get_data and line.count(':') > 0 :
                    spline = line.split(':')
                    results[spline[0]] = spline[1].rstrip('\n')
    
        ofile.close()
    
        return results

main()
