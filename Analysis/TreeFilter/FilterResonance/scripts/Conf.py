from core import Filter
import inspect
import sys

def get_remove_filter() :
    """ Define list of regex strings to filter input branches to remove from the output.
        Defining a non-empty list does not apply the filter, 
        you must also supply --enableRemoveFilter on the command line.
        If both filters are used, all branches in keep_filter are used
        except for those in remove_filter """

    return ['el_passVIDHEEP']

def get_keep_filter() :
    """ Define list of regex strings to filter input branches to retain in the output.  
        Defining a non-empty list does not apply the filter, 
        you must also supply --enableKeepFilter on the command line
        If both filters are used, all branches in keep_filter are used
        except for those in remove_filter """

    return ['Evt.*', 'NLOWeight', 'PUWeight', 'GPdf.*', 'GenHT', 'el_n', 'mu_n', 'el_pt', 'el_phi', 'el_eta', 'el_e', 'mu_pt', 'mu_phi', 'mu_eta', 'mu_e', 'ph.*', 'met_pt', 'met_phi', 'jet.*', 'trueph_.*', 'truelep_.*', 'isW.*', 'passTrig.*']

def config_analysis( alg_list, args ) :
    """ Configure analysis modules. Order is preserved """

    # run on the function provided through
    # the args
    for s in inspect.getmembers(sys.modules[__name__]) :
        if s[0] == args['function'] :
            print '*********************************'
            print 'RUN %s' %( args['function'] )
            print '*********************************'
            s[1]( alg_list, args )

    apply_pu_weight = Filter('ApplyPUWeight')
    apply_pu_weight.add_var( 'HistPath','/home/jkunkle/usercode/Analysis/TreeFilter/FilterResonance/data/MyDataPileupHistogram.root')
    apply_pu_weight.add_var( 'HistName','pileup')

    alg_list.append(apply_pu_weight)

def make_final_mumu( alg_list, args) :

    mu_pt = args.get( 'mu_pt', ' > 25 ' )

    # order should be muon, electron, photon, jet
    alg_list.append( filter_muon( mu_pt ) )
    alg_list.append( filter_electron( ) )
    alg_list.append( filter_photon( ) )
    alg_list.append( filter_jet( ) )

    filter_event = Filter('FilterEvent')
    filter_event.cut_mu_n = ' == 2 '
    filter_event.cut_trig_Mu24_IsoORIsoTk = ' == True '

    alg_list.append( filter_event )

    alg_list.append( Filter( 'MakePhotonCountVars' ) )
    alg_list.append( Filter( 'BuildEventVars' ) )
    alg_list.append( Filter( 'BuildTruth' ) )

def make_final_elel( alg_list, args) :

    el_pt = args.get( 'el_pt', ' > 25 ' )

    # order should be muon, electron, photon, jet
    alg_list.append( filter_muon( ) )
    alg_list.append( filter_electron( el_pt ) )
    alg_list.append( filter_photon( ) )
    alg_list.append( filter_jet( ) )

    filter_event = Filter('FilterEvent')
    filter_event.cut_el_n = ' == 2 '
    # reenable with new DYJets sample
    filter_event.cut_trig_Ele27_eta2p1_tight = ' == True '

    alg_list.append( filter_event )

    alg_list.append( Filter( 'MakePhotonCountVars' ) )
    alg_list.append( Filter( 'BuildEventVars' ) )
    alg_list.append( Filter( 'BuildTruth' ) )

def make_final_muel( alg_list, args) :

    mu_pt = args.get( 'mu_pt', ' > 25 ' )
    el_pt = args.get( 'el_pt', ' > 25 ' )

    # order should be muon, electron, photon, jet
    alg_list.append( filter_muon( mu_pt ) )
    alg_list.append( filter_electron(el_pt ) )
    alg_list.append( filter_photon( ) )
    alg_list.append( filter_jet( ) )

    filter_event = Filter('FilterEvent')
    filter_event.cut_mu_n = ' == 1 '
    filter_event.cut_el_n = ' == 1 '
    filter_event.cut_trig_Mu24_IsoORIsoTk = ' == True '

    alg_list.append( filter_event )

    alg_list.append( Filter( 'MakePhotonCountVars' ) )
    alg_list.append( Filter( 'BuildEventVars' ) )
    alg_list.append( Filter( 'BuildTruth' ) )

def make_final_mu( alg_list, args) :

    mu_pt = args.get( 'mu_pt', ' > 25 ' )
    ph_id_cut = args.get( 'ph_id_cut', 'medium' )

    # order should be muon, electron, photon, jet
    alg_list.append( filter_muon( mu_pt ) )
    alg_list.append( filter_electron( ) )
    alg_list.append( filter_photon( id_cut=ph_id_cut ) )
    alg_list.append( filter_jet( ) )

    filter_event = Filter('FilterEvent')
    filter_event.cut_mu_n = ' == 1 '
    filter_event.cut_mu_pt30_n = ' == 1 '
    filter_event.cut_trig_Mu24_IsoORIsoTk = ' == True '

    alg_list.append( filter_event )

    alg_list.append( Filter( 'MakePhotonCountVars' ) )
    alg_list.append( Filter( 'BuildEventVars' ) )
    alg_list.append( Filter( 'BuildTruth' ) )

def make_final_el( alg_list, args) :

    el_pt = args.get( 'el_pt', ' > 25 ' )
    ph_id_cut = args.get( 'ph_id_cut', 'medium' )

    # order should be muon, electron, photon, jet
    alg_list.append( filter_muon( ) )
    alg_list.append( filter_electron( el_pt ) )
    alg_list.append( filter_photon( id_cut=ph_id_cut ) )
    alg_list.append( filter_jet( ) )

    filter_event = Filter('FilterEvent')
    filter_event.cut_el_n = ' == 1 '
    filter_event.cut_el_pt30_n = ' == 1 '
    filter_event.cut_trig_Ele27_eta2p1_tight = ' == True '

    alg_list.append( filter_event )

    alg_list.append( Filter( 'MakePhotonCountVars' ) )
    alg_list.append( Filter( 'BuildEventVars' ) )
    alg_list.append( Filter( 'BuildTruth' ) )

def make_final_elg( alg_list, args) :

    mu_pt = args.get( 'mu_pt', ' > 10 ' )
    el_pt = args.get( 'el_pt', ' > 10 ' )
    ph_pt = args.get( 'ph_pt', ' > 15 ' )
    phot_vars = args.get( 'phot_vars', ' False ' )
    phot_id = args.get( 'phot_id', 'medium' )
    ph_eta = args.get( 'ph_eta', None )
    sec_lep_veto = args.get( 'sec_lep_veto', 'True' )
    unblind = args.get( 'unblind', 'False' )

    # order should be muon, electron, photon, jet
    alg_list.append( filter_muon(mu_pt ) )
    alg_list.append( filter_electron(el_pt ) )
    alg_list.append( filter_photon( ph_pt, id_cut=phot_id, ieta_cut=ph_eta ) )
    alg_list.append( filter_jet( ) )

    filter_event = Filter('FilterEvent')
    filter_event.cut_el_pt30_n = ' == 1 '
    filter_event.cut_ph_n = ' > 0 '
    filter_event.cut_trig_Ele27_eta2p1_tight = ' == True '
    if sec_lep_veto != 'False' :
        filter_event.cut_el_n = ' == 1 '
        filter_event.cut_mu_n = ' == 0 '

    alg_list.append( filter_event )

    if phot_vars == 'True' :
        alg_list.append( Filter( 'MakePhotonCountVars' ) )

    alg_list.append( Filter( 'BuildEventVars' ) )
    alg_list.append( Filter( 'BuildTruth' ) )

    if unblind is not 'True' :
        filter_blind = Filter( 'FilterBlind' )
        filter_blind.cut_ph_pt_lead = ' < 50 ' 

        filter_blind.add_var( 'isData', args.get('isData', ' == False' ) )
        alg_list.append( filter_blind )

def make_final_mug( alg_list, args) :

    el_pt = args.get( 'el_pt', ' > 10 ' )
    mu_pt = args.get( 'mu_pt', ' > 10 ' )
    ph_pt = args.get( 'ph_pt', ' > 15 ' )
    muphtrig = args.get( 'muphtrig', 'False' )
    phot_vars = args.get( 'phot_vars', ' False ' )
    phot_id = args.get( 'phot_id', 'medium' )
    ph_eta = args.get( 'ph_eta', None )
    sec_lep_veto = args.get( 'sec_lep_veto', 'True' )
    unblind = args.get( 'unblind', 'False' )

    # order should be muon, electron, photon, jet
    alg_list.append( filter_muon( mu_pt ) )
    alg_list.append( filter_electron( el_pt ) )
    alg_list.append( filter_photon( ph_pt, id_cut=phot_id, ieta_cut=ph_eta ) )
    alg_list.append( filter_jet( ) )

    filter_event = Filter('FilterEvent')
    filter_event.cut_ph_n = ' > 0 '
    
    if muphtrig == 'True' :
        filter_event.cut_mu_pt20_n = ' == 1 '
        filter_event.cut_trig_Mu17_Photon30 = ' == True '
    else :
        filter_event.cut_mu_pt30_n = ' == 1 '
        filter_event.cut_trig_Mu24_IsoORIsoTk = ' == True '

    if sec_lep_veto is not 'False' :
        filter_event.cut_mu_n = ' == 1 '
        filter_event.cut_el_n = ' == 0 '

    alg_list.append( filter_event )

    if phot_vars == 'True' :
        alg_list.append( Filter( 'MakePhotonCountVars' ) )
    alg_list.append( Filter( 'BuildEventVars' ) )
    alg_list.append( Filter( 'BuildTruth' ) )

    if unblind is not 'True' :
        filter_blind = Filter( 'FilterBlind' )
        filter_blind.cut_ph_pt_lead = ' < 50 ' 

        filter_blind.add_var( 'isData', args.get('isData', ' == False' ) )
        alg_list.append( filter_blind )

def make_final_elgjj( alg_list, args) :

    el_pt = args.get( 'el_pt', ' > 25 ' )
    ph_pt = args.get( 'ph_pt', ' > 15 ' )

    # order should be muon, electron, photon, jet
    alg_list.append( filter_muon( ) )
    alg_list.append( filter_electron(el_pt ) )
    alg_list.append( filter_photon( ph_pt ) )
    alg_list.append( filter_jet( ) )

    filter_event = Filter('FilterEvent')
    filter_event.cut_el_n = ' == 1 '
    filter_event.cut_ph_n = ' == 1 '
    filter_event.cut_jet_n = ' > 1 '
    filter_event.cut_trig_Ele27_eta2p1_tight = ' == True '

    alg_list.append( filter_event )

    alg_list.append( Filter( 'BuildEventVars' ) )
    alg_list.append( Filter( 'BuildTruth' ) )

    filter_blind = Filter( 'FilterBlind' )
    filter_blind.cut_abs_dijet_m_from_z = ' < 15 ' 

    filter_blind.add_var( 'isData', args.get('isData', ' == False' ) )
    alg_list.append( filter_blind )

def make_final_mugjj( alg_list, args) :

    mu_pt = args.get( 'mu_pt', ' > 25 ' )
    ph_pt = args.get( 'ph_pt', ' > 15 ' )

    # order should be muon, electron, photon, jet
    alg_list.append( filter_muon( mu_pt ) )
    alg_list.append( filter_electron( ph_pt ) )
    alg_list.append( filter_photon( ) )
    alg_list.append( filter_jet( ) )

    filter_event = Filter('FilterEvent')
    filter_event.cut_mu_n  = ' == 1 '
    filter_event.cut_ph_n  = ' == 1 '
    filter_event.cut_jet_n = ' > 1 '
    filter_event.cut_trig_Mu24_IsoORIsoTk = ' == True '

    alg_list.append( filter_event )

    alg_list.append( Filter( 'BuildEventVars' ) )
    alg_list.append( Filter( 'BuildTruth' ) )

    filter_blind = Filter( 'FilterBlind' )
    filter_blind.cut_abs_dijet_m_from_z = ' < 15 ' 

    filter_blind.add_var( 'isData', args.get('isData', ' == False' ) )
    alg_list.append( filter_blind )

def make_nofilt( alg_list, args ) :

    pass_lepton = args.get('pass_lepton', 'False')
    if pass_lepton == 'True' :
        alg_list.append( filter_muon( mu_pt = ' > 0 ' ) )
        alg_list.append( filter_electron( el_pt = ' > 0 ' ) )

    alg_list.append( filter_photon( ph_pt = ' > 0 ', id_cut = 'medium'   )  )
                           
    alg_list.append( Filter( 'BuildEventVars' ) )
    alg_list.append( Filter( 'BuildTruth' ) )



def filter_muon( mu_pt = ' > 25 ', do_cutflow=False, do_hists=False ) :

    filt = Filter('FilterMuon')

    filt.cut_pt           = mu_pt
    filt.cut_eta       = ' < 2.5'
    filt.cut_tight       = ' == True '
    filt.add_var( 'triggerBits', '23,31' )

    return filt

def filter_electron( el_pt = ' > 25 ', do_cutflow=False, do_hists=False ) :

    filt = Filter('FilterElectron')

    filt.cut_pt         = el_pt
    filt.cut_eta        = ' < 2.5'
    #filt.cut_tight     = ' == True '
    filt.cut_vid_medium     = ' == True '
    filt.cut_muon_dr    = ' > 0.4 '

    filt.add_var( 'triggerBits', '10' )

    return filt

def filter_photon( ph_pt = ' > 15 ', id_cut='medium', ieta_cut=None, do_cutflow=False, do_hists=False ) :

    filt = Filter('FilterPhoton')

    filt.cut_pt           = ph_pt
    filt.cut_eta       = ' < 2.5'
    filt.cut_muon_dr    = ' > 0.4 '
    filt.cut_electron_dr    = ' > 0.4 '

    if ieta_cut is not None :
        if ieta_cut == 'EB' :
            filt.cut_eb = ' == True '
        if ieta_cut == 'EE' :
            filt.cut_ee = ' == True '

    if( id_cut is not 'None' ) :
        setattr( filt, 'cut_%s' %id_cut, ' == True ' )
    return filt

def filter_jet( jet_pt = ' > 30 ' ) :

    filt = Filter( 'FilterJet' )

    filt.cut_pt = jet_pt
    filt.cut_muon_dr    = ' > 0.4 '
    filt.cut_electron_dr    = ' > 0.4 '
    filt.cut_photon_dr    = ' > 0.4 '

    filt.cut_jet_CSV_Loose = ' > 0.5426 '
    filt.cut_jet_CSV_Medium = ' > 0.8484 '
    filt.cut_jet_CSV_Tight = ' > 0.9535 '

    return filt

