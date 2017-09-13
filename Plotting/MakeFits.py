import ROOT
ROOT.PyConfig.IgnoreCommandLineOptions = True
from argparse import ArgumentParser

parser = ArgumentParser()

parser.add_argument( '--baseDir',  dest='baseDir', required=True, help='path to workspace directory' )
parser.add_argument( '--outputCard',  dest='outputCard', required=False, help='name of output card' )

options = parser.parse_args()

_LUMI = 36000.

def main() :

    key_wgamma = 'workspace_wgamma'
    key_signal = 'workspace_signal'
    key_wjets = 'workspace_wjets'

    #make_fit_workspace( options.baseDir, key_wgamma )

    #workspace_toy = ROOT.RooWorkspace( 'workspace_toy' )
    #generate_toy_data( options.baseDir, key_wgamma, 'dijet_Wgamma_mu_EB', workspace_toy, suffix='mu_EB' )
    #workspace_toy.writeToFile( '%s/%s.root' %( options.baseDir, workspace_toy.GetName() ) )

    #workspace_toysignal = ROOT.RooWorkspace( 'workspace_toysignal' )
    #make_toy_signal( options.baseDir, workspace_toysignal )
    #workspace_toysignal.writeToFile( '%s/%s.root' %( options.baseDir, workspace_toysignal.GetName() ) )

    signal_pred = 'srhistpdf_MadGraphResonanceMass300_width0p01_mu_EB'
    #signal_pred = 'signal'

    #generate_card( options.baseDir, 'workspace_toy', 'workspace_signal', signal_pred, options.outputCard )
    #generate_card( options.baseDir, 'workspace_toy', 'workspace_toysignal', signal_pred, options.outputCard )

    run_statistical_tests( options.baseDir, key_wgamma, 'dijet_Wgamma_mu_EB', 100, options.baseDir, suffix='mu_EB' )

def make_toy_signal( baseDir, workspace ) :


    #x = ROOT.RooRealVar ('x','x',-10,10) ;
    #mean = ROOT.RooRealVar ('mean','Mean of Gaussian',0,-10,10) 
    #sigma = ROOT.RooRealVar ('sigma','Width of Gaussian',3,-10,10) 
    #gauss = ROOT.RooGaussian ('gauss','gauss(x,mean,sigma)',x,mean,sigma) 
    #frame = x.frame() 
    #gauss.plotOn(frame) 
    #frame.Draw() 
    #raw_input('cont')

    xvar = ROOT.RooRealVar( 'x', 'x', 0, 1000 )
    mean = ROOT.RooRealVar( 'mean', 'mean', 300 )
    sigma = ROOT.RooRealVar( 'sigma', 'sigma', 3 )

    #norm = ROOT.RooRealVar( 'signal_norm', 'signal_norm', 1 )

    signal = ROOT.RooGaussian( 'signal', 'signal', xvar, mean, sigma )

    frame = xvar.frame()
    signal.plotOn( frame )
    frame.Draw()
    raw_input('cont')


    getattr( workspace, 'import' ) ( signal )
    #getattr( workspace, 'import' ) ( norm )



def make_fit_workspace( baseDir, workspace_key ) :

    ofile = ROOT.TFile.Open( '%s/%s.root' %( baseDir, workspace_key ) )

    ws = ofile.Get( workspace_key )

    ws.Print()

    pdf_list = ws.allPdfs()
    print pdf_list.getSize()

    for i in range( 0, pdf_list.getSize() ) :
        print pdf_list[i]


def generate_card( baseDir, data_workspace, signal_workspace, signal_pred, outputCard ) :

    card_entries = []


    #bins = ['mu_EB', 'mu_EE', 'el_EB', 'el_EE']
    bins = ['mu_EB']
    backgrounds = [ 
        {'name' : 'Wgamma' , 'path' : '%s/workspace_wgamma.root' %( baseDir ), 'wsname' : 'workspace_wgamma' }
    ]

    section_divider = '-'*100

    card_entries.append( 'imax %d number of bins' %len( bins ) )
    card_entries.append( 'jmax %d number of backgrounds' %len( backgrounds) ) 
    card_entries.append( 'kmax * number of nuisance parameters' )

    card_entries.append( section_divider )

    max_name_len = max( [len(x['name']) for x in backgrounds ] )
    max_path_len = max( [len(x['path']) for x in backgrounds ] )

    for ibin in bins :
        for bkgdic in backgrounds :
            card_entries.append( 'shapes %s %s %s %s:dijet_%s_%s' %( bkgdic['name'].ljust( max_name_len ), ibin, bkgdic['path'].ljust( max_path_len ), bkgdic['wsname'], bkgdic['name'], ibin ) )
        card_entries.append( 'shapes Resonance %s %s/%s.root %s:%s' %( ibin, baseDir, signal_workspace, signal_workspace, signal_pred) )
        card_entries.append( 'shapes data_obs %s %s/%s.root %s:toydata%s' %( ibin, baseDir, data_workspace, data_workspace, ibin ) )

    card_entries.append( section_divider )

    card_entries.append( 'bin          ' + '    '.join( bins ) )
    card_entries.append( 'observation  ' + '    '.join( ['-1.0']*len(bins) ) )

    card_entries.append( section_divider )

    card_entries.append( 'bin      ' + '    '.join(['    '.join( [x for x in bins] )]*( len(backgrounds) + 1 ) ) ) 
    card_entries.append( 'process  ' + '    '.join( ( ['Resonance'] + [x['name'] for x in backgrounds])*len(bins) ) )
    card_entries.append( 'process  ' + '    '.join( [str(x) for x in range(0, len(backgrounds) +1 ) ]*len(bins) ) )
    card_entries.append( 'rate     ' + '    '.join( ['1.0','1.0' ]*len(bins) ) )

    card_entries.append( section_divider )

    card_entries.append( 'lumi   lnN    ' + '    '.join(['1.05']*len(backgrounds) + ['1.05'] ) )

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


def generate_toy_data( basedir, ws_key, hist_key, out_ws, suffix='' ) :

    ofile = ROOT.TFile.Open( '%s/%s.root' %( basedir, ws_key ) )

    ws = ofile.Get( ws_key )

    normalization = ws.var( 'norm_%s' %hist_key )
    pdf = ws.pdf( hist_key )
    xvar = ws.var('x')

    dataset = pdf.generate( ROOT.RooArgSet(xvar), int(normalization.getValV()), ROOT.RooCmdArg( 'Name', 0, 0, 0, 0, 'toydata%s' %suffix ) )

    # not clear why we have to rename here
    getattr( out_ws, 'import' ) ( dataset, ROOT.RooCmdArg('RenameAllNodes', 0, 0, 0, 0, 'toydata%s' %suffix ) )


def run_statistical_tests( basedir, ws_key, hist_key, niter=100, outputDir=None, suffix='' ) :

    ofile = ROOT.TFile.Open( '%s/%s.root' %( basedir, ws_key ) )

    ws = ofile.Get( ws_key )

    normalization = ws.var( 'norm_%s' %hist_key )
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


main()
