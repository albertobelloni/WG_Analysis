from core import Filter
import os
import sys

def get_remove_filter() :

    return ['EvtWeights']

def get_keep_filter() :

    #return ['Evt.*', 'MET.*', 'GPdf.*', 'GPhotPt', 'GPhotEta', 'GPhotPhi', 'GPhotE' ,'GPhotSt', 'GPhotMotherId']
    return ['Evt.*', 'GPdf.*', 'HLTObj.*', 'GenHT']

def config_analysis( alg_list, args ) :

    isData = args.pop('isData', False)

    print 'isData = ', isData

    if str(isData) =='true' :
        workarea = os.getenv('WorkArea')
        dq_filter = Filter( 'FilterDataQuality' )
        dq_filter.add_var( 'jsonFile', '%s/TreeFilter/RecoPhoton15/data/Cert_271036-284044_13TeV_23Sep2016ReReco_Collisions16_JSON.txt' %workarea)
        alg_list.append( dq_filter )

    alg_list.append( build_truth( args ) )

    alg_list.append( build_electron( do_cutflow=False, do_hists=False, evalPID=None, applyCorrections=False ) )
    #alg_list.append( build_electron( do_cutflow=True, do_hists=False, evalPID='medium', applyCorrections=False ) )

    alg_list.append( build_muon( do_cutflow=False, do_hists=False, evalPID=None, applyCorrections=False ) )
    #alg_list.append( build_muon( do_cutflow=True, do_hists=False, evalPID='tight', applyCorrections=False ) )

    alg_list.append( build_photon( do_cutflow=False, do_hists=False, evalPID=None, doEVeto=False, applyCorrections=False ) )
    #alg_list.append( build_photon( do_cutflow=True, do_hists=True, evalPID='medium', doEVeto=False, applyCorrections=False ) )

    alg_list.append( build_jet( do_cutflow=False, do_hists=False ) )

    #alg_list.append( Filter('BuildMET') )

    #alg_list.append( weight_event(args) )

    #alg_list.append( Filter( 'BuildTriggerBits' ) )

    #gph_filt = Filter( 'FilterGenPhoton' )
    #gph_filt.cut_pt = ' > 0.1 '
    #alg_list.append(gph_filt)

    #trig_filt = Filter('FilterTrigger')
    ##trig_filt.cut_trigger = ' ==48 ' #HLT_Photon36_CaloId10_Iso50_Photon22_CaloId10_Iso50_v 
    #trig_filt.cut_trigger = '==17 | == 18 | == 19 | == 13 | == 14 | == 9 | == 22 ' # HLT_Ele27_WP80 || HLT_IsoMu24_eta2p1 || HLT_IsoMu24 || HLT_Mu17_TkMu8 || HLT_Mu17_Mu8 || HLT_Ele17_CaloIdT_CaloIsoVL_TrkIdVL_TrkIsoVL_Ele8_CaloIdT_CaloIsoVL_TrkIdVL_TrkIsoVL || HLT_Ele17_CaloIdT_TrkIdVL_CaloIsoVL_TrkIsoVL_Ele8_CaloIdT_TrkIdVL_CaloIsoVL_TrkIsoVL

    #alg_list.append(trig_filt)

def build_muon( do_cutflow=False, do_hists=False, evalPID=None, applyCorrections=False ) :

    filt = Filter('BuildMuon')

    filt.do_cutflow = do_cutflow

    filt.cut_pt         = ' > 10 '

    filt.cut_isPf_loose         = ' == True '
    filt.cut_isGlobalOrTk_loose = ' == True '

    filt.cut_isGlobal_tight   = ' == True '
    filt.cut_isPF_tight       = ' == True '
    filt.cut_abseta_tight     = ' < 2.4'
    filt.cut_chi2_tight       = ' < 10'
    filt.cut_nMuonHits_tight  = ' > 0 ' 
    filt.cut_nStations_tight  = ' > 1'
    filt.cut_nTrkLayers_tight = ' > 5 ' 
    filt.cut_nPixelHits_tight = ' > 0'
    filt.cut_d0_tight         = ' < 0.2'
    filt.cut_z0_tight         = ' < 0.5'
    filt.cut_corriso_tight    = ' < 0.25'
    filt.cut_trkiso_tight     = ' < 0.05 '

    if evalPID is not None :
        filt.add_var( 'evalPID', evalPID )

    if applyCorrections :
        filt.add_var( 'applyCorrections', 'true' )

        workarea = os.getenv('WorkArea')
        filt.add_var( 'path', '%s/TreeFilter/RecoWgg/data/MuScleFitCorrector_v4_3/MuScleFit_2012_MC_53X_smearReReco.txt' %workarea )

    if do_hists :
        filt.add_hist( 'cut_pt', 100, 0, 500 )
        filt.add_hist( 'cut_abseta', 50, 0, 5 )
        filt.add_hist( 'cut_chi2', 50, 0, 50 )
        filt.add_hist( 'cut_nTrkLayers', 20, 0, 20 )
        filt.add_hist( 'cut_nStations', 5, 0, 5 )
        filt.add_hist( 'cut_nPixelHits', 20, 0, 20 )
        filt.add_hist( 'cut_d0', 100, -0.05, 0.05 )
        filt.add_hist( 'cut_z0', 100, -0.05, 0.05 )
        filt.add_hist( 'cut_trkiso', 50, 0, 0.5 )
        filt.add_hist( 'cut_corriso', 50, 0, 0.5 )

    return filt

def build_electron( do_cutflow=False, do_hists=False, filtPID=None, evalPID=None, applyCorrections=False ) :

    filt = Filter('BuildElectron')

    filt.do_cutflow = do_cutflow

    # using values here
    #https://twiki.cern.ch/twiki/bin/view/CMS/CutBasedElectronIdentificationRun2
    # d0 and z0 cuts not recommeded
    # as of Dec 2016

    filt.cut_pt = ' > 10'
    filt.cut_abssceta       = ' <2.5 '
    #filt.cut_abssceta       = ' <1.479 '
    #filt.cut_abssceta       = ' >= 1.479 & < 2.5'
    # no crack for now
    #filt.cut_abssceta_crack = ' > 1.4442 & < 1.566 '
    #filt.invert('cut_abssceta_crack')
    #filt.invert('cut_abssceta')

    filt.cut_sigmaIEIE_barrel_tight        = ' < 0.00998 '
    filt.cut_absdEtaIn_barrel_tight        = ' < 0.00308 '
    filt.cut_absdPhiIn_barrel_tight        = ' < 0.0816 '
    filt.cut_hovere_barrel_tight           = ' < 0.0414 '
    filt.cut_isoRho_barrel_tight           = ' < 0.0588 '
    filt.cut_ooEmooP_barrel_tight          = ' < 0.0129 '
    #filt.cut_d0_barrel_tight               = ' < 0.0111 '
    #filt.cut_z0_barrel_tight               = ' < 0.0466 '
    filt.cut_misshits_barrel_tight         = ' < 1 '
    filt.cut_passConvVeto_barrel_tight     = ' == 1 '

    filt.cut_sigmaIEIE_barrel_medium       = ' < 0.00998 '
    filt.cut_absdEtaIn_barrel_medium       = ' < 0.00311 '
    filt.cut_absdPhiIn_barrel_medium       = ' < 0.103 '
    filt.cut_hovere_barrel_medium          = ' < 0.253 '
    filt.cut_isoRho_barrel_medium          = ' < 0.0695 '
    filt.cut_ooEmooP_barrel_medium         = ' < 0.134 '
    #filt.cut_d0_barrel_medium              = ' < 0.0118 '
    #filt.cut_z0_barrel_medium              = ' < 0.373 '
    filt.cut_misshits_barrel_medium        = ' < 1 '
    filt.cut_passConvVeto_barrel_medium    = ' == 1 '

    filt.cut_sigmaIEIE_barrel_loose        = ' < 0.011 '
    filt.cut_absdEtaIn_barrel_loose        = ' < 0.00477 '
    filt.cut_absdPhiIn_barrel_loose        = ' < 0.222 '
    filt.cut_hovere_barrel_loose           = ' < 0.298 '
    filt.cut_isoRho_barrel_loose           = ' < 0.0994 '
    filt.cut_ooEmooP_barrel_loose          = ' < 0.241 '
    #filt.cut_d0_barrel_loose               = ' < 0.0261 '
    #filt.cut_z0_barrel_loose               = ' < 0.41 '
    filt.cut_misshits_barrel_loose         = ' < 1 '
    filt.cut_passConvVeto_barrel_loose     = ' == 1 '

    filt.cut_sigmaIEIE_barrel_veryloose    = ' < 0.0115 '
    filt.cut_absdEtaIn_barrel_veryloose    = ' < 0.00749 '
    filt.cut_absdPhiIn_barrel_veryloose    = ' < 0.228 '
    filt.cut_hovere_barrel_veryloose       = ' < 0.356 '
    filt.cut_isoRho_barrel_veryloose       = ' < 0.175 '
    filt.cut_ooEmooP_barrel_veryloose      = ' < 0.299 '
    #filt.cut_d0_barrel_veryloose           = ' < 0.0564 '
    #filt.cut_z0_barrel_veryloose           = ' < 0.472 '
    filt.cut_misshits_barrel_veryloose     = ' < 2 '
    filt.cut_passConvVeto_barrel_veryloose = ' == 1 '

    filt.cut_sigmaIEIE_endcap_tight        = ' < 0.0292 '
    filt.cut_absdEtaIn_endcap_tight        = ' < 0.00605 '
    filt.cut_absdPhiIn_endcap_tight        = ' < 0.0394 '
    filt.cut_hovere_endcap_tight           = ' < 0.0641 '
    filt.cut_isoRho_endcap_tight           = ' < 0.0571 '
    filt.cut_ooEmooP_endcap_tight          = ' < 0.0129 '
    #filt.cut_d0_endcap_tight               = ' < 0.0351 '
    #filt.cut_z0_endcap_tight               = ' < 0.417 '
    filt.cut_misshits_endcap_tight         = ' < 1 '
    filt.cut_passConvVeto_endcap_tight     = ' == 1 '

    filt.cut_sigmaIEIE_endcap_medium       = ' < 0.0298 '
    filt.cut_absdEtaIn_endcap_medium       = ' < 0.00609 '
    filt.cut_absdPhiIn_endcap_medium       = ' < 0.045 '
    filt.cut_hovere_endcap_medium          = ' < 0.0878 '
    filt.cut_isoRho_endcap_medium          = ' < 0.0821 '
    filt.cut_ooEmooP_endcap_medium         = ' < 0.13 '
    #filt.cut_d0_endcap_medium              = ' < 0.0739 '
    #filt.cut_z0_endcap_medium              = ' < 0.602 '
    filt.cut_misshits_endcap_medium        = ' <  1 '
    filt.cut_passConvVeto_endcap_medium    = ' == 1 '

    filt.cut_sigmaIEIE_endcap_loose        = ' < 0.0314 '
    filt.cut_absdEtaIn_endcap_loose        = ' < 0.00868 '
    filt.cut_absdPhiIn_endcap_loose        = ' < 0.213 '
    filt.cut_hovere_endcap_loose           = ' < 0.101 '
    filt.cut_isoRho_endcap_loose           = ' < 0.107 '
    filt.cut_ooEmooP_endcap_loose          = ' < 0.14 '
    #filt.cut_d0_endcap_loose               = ' < 0.118 '
    #filt.cut_z0_endcap_loose               = ' < 0.822 '
    filt.cut_misshits_endcap_loose         = ' <  1 '
    filt.cut_passConvVeto_endcap_loose     = ' == 1 '

    filt.cut_sigmaIEIE_endcap_veryloose    = ' < 0.037 '
    filt.cut_absdEtaIn_endcap_veryloose    = ' < 0.00895 '
    filt.cut_absdPhiIn_endcap_veryloose    = ' < 0.213 '
    filt.cut_hovere_endcap_veryloose       = ' < 0.211 '
    filt.cut_isoRho_endcap_veryloose       = ' < 0.159 '
    filt.cut_ooEmooP_endcap_veryloose      = ' < 0.15 '
    #filt.cut_d0_endcap_veryloose           = ' < 0.222 '
    #filt.cut_z0_endcap_veryloose           = ' < 0.921 '
    filt.cut_misshits_endcap_veryloose     = ' < 3 '
    filt.cut_passConvVeto_endcap_veryloose = ' == 1 '


    if filtPID is not None :
        setattr(filt, 'cut_pid_%s' %filtPID, ' == True' )

    if evalPID is not None :
        filt.add_var( 'evalPID', evalPID )

    if applyCorrections :
        workarea = os.getenv('WorkArea')
        filt.add_var('applyCorrections', 'true' )
        filt.add_var('correctionFile', '%s/TreeFilter/RecoWgg/data/step2-invMass_SC-loose-Et_20-trigger-noPF-HggRunEtaR9.dat' %workarea )
        filt.add_var('smearingFile', '%s/TreeFilter/RecoWgg/data/outFile-step4-invMass_SC-loose-Et_20-trigger-noPF-HggRunEtaR9-smearEle.dat' %workarea )


    if do_hists :
        filt.add_hist( 'cut_pt', 100, 0, 500 )
        filt.add_hist( 'cut_abseta', 50, 0, 5 )
        filt.add_hist( 'cut_abseta_crack', 50, 0, 5 )
        filt.add_hist( 'cut_absdEtaIn_barrel_tight', 100, -0.1, 0.1 )
        filt.add_hist( 'cut_absdPhiIn_barrel_tight', 100, -0.1, 0.1 )
        filt.add_hist( 'cut_sigmaIEIE_barrel_tight', 100, 0, 0.05 )
        filt.add_hist( 'cut_hovere_barrel_tight', 100, -1, 1 )
        filt.add_hist( 'cut_d0_barrel_tight', 100, -1, 1 )
        filt.add_hist( 'cut_z0_barrel_tight', 100, -1, 1 )
        filt.add_hist( 'cut_ooEmooP_barrel_tight', 100, 0, 1 )
        filt.add_hist( 'cut_pfIso30_barrel_tight', 100, 0, 10 )
        filt.add_hist( 'cut_passConvVeto_barrel_tight', 2, 0, 2 )
        filt.add_hist( 'cut_misshits_barrel_tight', 10, 0, 10 )

    return filt

def build_photon( do_cutflow=False, do_hists=False, filtPID=None, evalPID=None, doEVeto=True, applyCorrections=False ) :

    filt = Filter('BuildPhoton')

    filt.do_cutflow = do_cutflow

    filt.cut_pt           = ' > 10 '
    filt.cut_abseta       = ' < 2.5'
    filt.cut_abseta_crack = ' > 1.44 & < 1.57 '
    filt.invert('cut_abseta_crack')

    # taken from https://twiki.cern.ch/twiki/bin/view/CMS/CutBasedPhotonIdentificationRun2#Recommended_Working_points_for_2
    # Updated Dec 2016
    filt.cut_sigmaIEIE_barrel_loose  = ' < 0.01031 '
    filt.cut_chIsoCorr_barrel_loose  = ' < 1.295 '
    filt.cut_neuIsoCorr_barrel_loose = ' < 10.910 '
    filt.cut_phoIsoCorr_barrel_loose = ' < 3.630 '
    filt.cut_hovere_barrel_loose = ' < 0.0597 '

    filt.cut_sigmaIEIE_endcap_loose  = ' < 0.03013 '
    filt.cut_chIsoCorr_endcap_loose  = ' < 1.011 '
    filt.cut_neuIsoCorr_endcap_loose = ' < 5.931 '
    filt.cut_phoIsoCorr_endcap_loose = ' < 6.641 '
    filt.cut_hovere_endcap_loose = ' < 0.0481 '

    filt.cut_sigmaIEIE_barrel_medium  = ' < 0.01022 '
    filt.cut_chIsoCorr_barrel_medium  = ' < 0.441 '
    filt.cut_neuIsoCorr_barrel_medium = ' < 2.725 '
    filt.cut_phoIsoCorr_barrel_medium = ' < 2.571 '
    filt.cut_hovere_barrel_medium = ' < 0.0396 '

    filt.cut_sigmaIEIE_endcap_medium  = ' < 0.03001 '
    filt.cut_chIsoCorr_endcap_medium  = ' < 0.442 '
    filt.cut_neuIsoCorr_endcap_medium = ' < 1.715 '
    filt.cut_phoIsoCorr_endcap_medium = ' < 3.863 '
    filt.cut_hovere_endcap_medium = ' < 0.0219 '

    filt.cut_sigmaIEIE_barrel_tight  = ' < 0.00994 '
    filt.cut_chIsoCorr_barrel_tight  = ' < 0.202 '
    filt.cut_neuIsoCorr_barrel_tight = ' < 0.264 '
    filt.cut_phoIsoCorr_barrel_tight = ' < 2.362 '
    filt.cut_hovere_barrel_tight = ' < 0.0269 '

    filt.cut_sigmaIEIE_endcap_tight  = ' < 0.0300 '
    filt.cut_chIsoCorr_endcap_tight  = ' < 0.034 '
    filt.cut_neuIsoCorr_endcap_tight = ' < 0.586 '
    filt.cut_phoIsoCorr_endcap_tight = ' < 2.617 '
    filt.cut_hovere_endcap_tight = ' < 0.0213 '

    if filtPID is not None :
        setattr(filt, 'cut_pid_%s' %filtPID, ' == True' )

    if evalPID is not None :
        filt.add_var( 'evalPID', evalPID )

    if do_hists :
        filt.add_hist( 'cut_pt', 100, 0, 500 )
        filt.add_hist( 'cut_abseta', 50, 0, 5 )
        filt.add_hist( 'cut_abseta_crack', 50, 0, 5 )
        filt.add_hist( 'cut_hovere', 50, 0, 0.1 )
        filt.add_hist( 'cut_eveto', 2, 0, 2 )
        filt.add_hist( 'cut_sigmaIEIE_barrel_medium', 50, 0, 0.05 )
        filt.add_hist( 'cut_chIsoCorr_barrel_medium', 50, 0, 5 )
        filt.add_hist( 'cut_neuIsoCorr_barrel_medium', 50, 0, 5 )
        filt.add_hist( 'cut_phoIsoCorr_barrel_medium', 50, 0, 5 )
        filt.add_hist( 'cut_sigmaIEIE_endcap_medium', 50, 0, 0.05 )
        filt.add_hist( 'cut_chIsoCorr_endcap_medium', 50, 0, 5 )
        filt.add_hist( 'cut_neuIsoCorr_endcap_medium', 50, 0, 5 )
        filt.add_hist( 'cut_phoIsoCorr_endcap_medium', 50, 0, 5 )

        filt.add_hist( 'cut_sigmaIEIE_barrel_loose', 50, 0, 0.05 )
        filt.add_hist( 'cut_chIsoCorr_barrel_loose', 50, 0, 5 )
        filt.add_hist( 'cut_neuIsoCorr_barrel_loose', 100, -5, 5 )
        filt.add_hist( 'cut_phoIsoCorr_barrel_loose', 50, 0, 5 )
        filt.add_hist( 'cut_sigmaIEIE_endcap_loose', 50, 0, 0.05 )
        filt.add_hist( 'cut_chIsoCorr_endcap_loose', 50, 0, 5 )
        filt.add_hist( 'cut_neuIsoCorr_endcap_loose', 100, -5, 5 )
        filt.add_hist( 'cut_phoIsoCorr_endcap_loose', 50, 0, 5 )

    return filt

def build_jet( do_cutflow=False, do_hists=False ) :

    filt = Filter('BuildJet')
    filt.do_cutflow = do_cutflow

    filt.cut_pt = ' > 30 '
    filt.cut_abseta = ' < 4.5 '
    #filt.cut_idloose = ' == True '

    filt.cut_jet_nhf_central_loose = ' < 0.99 '
    filt.cut_jet_nemf_central_loose = ' < 0.99 '
    filt.cut_jet_nconst_central_loose = ' > 1'
    filt.cut_jet_nhf_central_tight = ' < 0.90 '
    filt.cut_jet_nemf_central_tight = ' < 0.90 '
    filt.cut_jet_nconst_central_tight = ' > 1'
    filt.cut_jet_nhf_central_tightlep = ' < 0.9 '
    filt.cut_jet_nemf_central_tightlep = ' < 0.9 '
    filt.cut_jet_nconst_central_tightlep = '> 1 '
    filt.cut_jet_muf_central_tightlep = '< 0.8 '
    filt.cut_jet_chf_central_loose = ' > 0'
    filt.cut_jet_cmult_central_loose = ' > 0 '
    filt.cut_jet_cemf_central_loose = ' < 0.99 '
    filt.cut_jet_chf_central_tight = ' > 0 '
    filt.cut_jet_cmult_central_tight = ' > 0'
    filt.cut_jet_cemf_central_tight = ' < 0.99 '
    filt.cut_jet_chf_central_tightlep = ' > 0'
    filt.cut_jet_cmult_central_tightlep = ' > 0'
    filt.cut_jet_cemf_central_tightlep = ' < 0.90'
    filt.cut_jet_nhf_transition_loose = ' > 0.01 '
    filt.cut_jet_nemf_transition_loose = ' < 0.98 '
    filt.cut_jet_nmult_transition_loose = ' > 2 '
    filt.cut_jet_nhf_transition_tight = ' > 0.01 '
    filt.cut_jet_nemf_transition_tight = ' < 0.98 '
    filt.cut_jet_nmult_transition_tight = ' > 2 '
    filt.cut_jet_nemf_forward_loose = ' < 0.90 '
    filt.cut_jet_nmult_forward_loose = '> 10 '
    filt.cut_jet_nemf_forward_tight = ' < 0.90 '
    filt.cut_jet_nmult_forward_tight = ' > 10 '

    #filt.cut_jet_el_dr = ' > 0.4 '
    #filt.cut_jet_ph_dr = ' > 0.4 '

    if do_hists :
        filt.add_hist( 'cut_pt', 100, 0, 500 )
        filt.add_hist( 'cut_abseta', 50, 0, 5 )

    return filt

def build_truth( args ) :

    truth_filt = Filter('BuildTruth') 

    truth_filt.cut_lep_mother = ' == 24 || == -24 ||  == 11 || == -11 || == 12 || == -12 || == 13 || == -13 || == 14 || == -14 || == 15 || == -15 || == 16 || == -16 '

    truth_filt.cut_ph_pt = ' > 5 '
    truth_filt.cut_ph_IsPromptFinalState = ' == True '

    doFHPFS = args.get( 'doFHPFS', False )
    if doFHPFS == 'true' :
        truth_filt.cut_ph_FromHardProcessFinalState = ' == True '

    return truth_filt 

def weight_event( args ) :

    filt = Filter( 'WeightEvent' )

    filt_str = args.get( 'ApplyNLOWeight', 'false' )

    filt.add_var( 'ApplyNLOWeight', filt_str )

    if 'sampleFile' in args :

        workarea = os.getenv('WorkArea')
        filt.add_var( 'sample_file', args['sampleFile'])
        filt.add_var( 'data_file', '%s/TreeFilter/RecoPhoton15/data/MyDataPileupHistogram.root' %workarea )
        filt.add_var( 'sample_hist', 'pileup_true' )
        filt.add_var('data_hist', 'pileup')
    else :
        print 'weight_event requires as a command line argument like --moduleArgs " { \'sampleFile\' : \'/path/histograms.root\'} "'

    return filt

