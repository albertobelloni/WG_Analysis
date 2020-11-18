from core import Filter
import os
import sys
import inspect

_workarea = os.getenv( 'WorkArea' )
theyear = 2018

# integrated luminosities in microbarns
int_lumi_a = 13977900815.135
int_lumi_b = 7063759972.048
int_lumi_c = 6898816877.984
int_lumi_d = 31747581871.050

int_lumi_abcd = int_lumi_a +int_lumi_b + int_lumi_c + int_lumi_d
int_lumi_bcd = int_lumi_b + int_lumi_c + int_lumi_d

int_lumi_bcdef =  8.950818835 # run <  316361 (BeforeMuonHLTUpdate)
int_lumi_gh    = 50.789746374 # run >= 316361 (AfterMuonHLTUpdate)


def get_remove_filter() :
    """ Define list of regex strings to filter input branches to remove from the output.
        Defining a non-empty list does not apply the filter, 
        you must also supply --enableRemoveFilter on the command line.
        If both filters are used, all branches in keep_filter are used
        except for those in remove_filter """

    return []

def get_keep_filter() :
    """ Define list of regex strings to filter input branches to retain in the output.  
        Defining a non-empty list does not apply the filter, 
        you must also supply --enableKeepFilter on the command line
        If both filters are used, all branches in keep_filter are used
        except for those in remove_filter """

    return ['.*']

def config_analysis( alg_list, args ) :
    """ Configure analysis modules. Order is preserved """

    # run on the function provided through
    # the args
    for func in args['functions'].split(',') :
        for s in inspect.getmembers(sys.modules[__name__]) :
            if s[0] == func :
                print '*********************************'
                print 'RUN %s' %( func )
                print '*********************************'
                alg_list.append( s[1]( args ) )


def get_muon_sf(options) :

    base_path = '%s/TreeFilter/ApplyScaleFactors/data' %_workarea

    muon_sf = Filter( 'AddMuonSF' )

    muon_sf.add_var( 'year', theyear)

    muon_sf.add_var( 'LumiBCDEF', int_lumi_bcdef)
    muon_sf.add_var ('LumiGH', int_lumi_gh)

    muon_sf.add_var( 'FilePathTrigBCDEF', '%s/2018/EfficienciesAndSF_2018Data_BeforeMuonHLTUpdate.root' %base_path )
    muon_sf.add_var( 'HistTrigBCDEF', 'IsoMu24_PtEtaBins/pt_abseta_ratio' )
    muon_sf.add_var( 'HistTrigBCDEFdata', 'IsoMu24_PtEtaBins/efficienciesDATA/pt_abseta_DATA' )
    muon_sf.add_var( 'HistTrigBCDEFmc', 'IsoMu24_PtEtaBins/efficienciesMC/pt_abseta_MC' )
    muon_sf.add_var( 'FilePathTrigGH', '%s/2018/EfficienciesAndSF_2018Data_AfterMuonHLTUpdate.root' %base_path )
    muon_sf.add_var( 'HistTrigGH', 'IsoMu24_PtEtaBins/pt_abseta_ratio' )
    muon_sf.add_var( 'HistTrigGHdata', 'IsoMu24_PtEtaBins/efficienciesDATA/pt_abseta_DATA' )
    muon_sf.add_var( 'HistTrigGHmc', 'IsoMu24_PtEtaBins/efficienciesMC/pt_abseta_MC' )

    muon_sf.add_var( 'FilePathIdBCDEF', '%s/2018/RunABCD_mu_SF_ID.root' %base_path )
    muon_sf.add_var( 'HistIdBCDEF','NUM_TightID_DEN_TrackerMuons_pt_abseta' )
    muon_sf.add_var( 'FilePathIdGH', '%s/2018/RunABCD_mu_SF_ID.root' %base_path )
    muon_sf.add_var( 'HistIdGH', 'NUM_TightID_DEN_TrackerMuons_pt_abseta' )

    muon_sf.add_var( 'FilePathIsoBCDEF', '%s/2018/RunABCD_mu_SF_ISO.root' %base_path )
    muon_sf.add_var ('HistIsoBCDEF','NUM_TightRelIso_DEN_TightIDandIPCut_pt_abseta')
    muon_sf.add_var( 'FilePathIsoGH', '%s/2018/RunABCD_mu_SF_ISO.root' %base_path )
    muon_sf.add_var ('HistIsoGH','NUM_TightRelIso_DEN_TightIDandIPCut_pt_abseta')

    return muon_sf

def get_electron_sf(options) :

    base_path = '%s/TreeFilter/ApplyScaleFactors/data' %_workarea

    electron_sf = Filter( 'AddElectronSF' )

    electron_sf.add_var( 'year', theyear)

    electron_sf.add_var( 'FilePathRecoHighPt', '%s/2018/egammaEffi.txt_EGM2D_updatedAll2018.root'%base_path)
    electron_sf.add_var( 'HistRecoHighPt', 'EGamma_SF2D')
    electron_sf.add_var( 'FilePathRecoLowPt',  '%s/2018/egammaEffi.txt_EGM2D_updatedAll2018.root'%base_path)
    electron_sf.add_var( 'HistRecoLowPt', 'EGamma_SF2D')
    electron_sf.add_var( 'FilePathCutID',      '%s/2018/2018_cutbased_ElectronTightID.root'%base_path)
    electron_sf.add_var( 'HistCutID', 'EGamma_SF2D')
    electron_sf.add_var( 'FilePathTrigEl', '%s/2018/SF_HLT_Ele32_WPTight_Gsf_2018.root' %base_path )
    electron_sf.add_var( 'HistTrigEl', 'EGamma_SF2D' )
    electron_sf.add_var( 'HistTrigElData', 'EGamma_EffData2D' )
    electron_sf.add_var( 'HistTrigElMC', 'EGamma_EffMC2D' )

    return electron_sf

def get_photon_sf(options) :

    base_path = '%s/TreeFilter/ApplyScaleFactors/data' %_workarea

    photon_sf = Filter( 'AddPhotonSF' )

    photon_sf.add_var( 'year', theyear)

    photon_sf.add_var( 'FilePathId', '%s/2018/2018_cutbased_PhotonsMediumID.root' %base_path )
    photon_sf.add_var( 'HistId', 'EGamma_SF2D' )
    
    # high-pt photon ID fit: https://indico.cern.ch/event/879936/#3-high-pt-photon-sfs-for-wgamm
    photon_sf.add_var( 'HiPtId_inner_const', +1.006153e+00 )
    photon_sf.add_var( 'HiPtId_inner_cov00', +2.687380e-05 )
    photon_sf.add_var( 'HiPtId_inner_cov01', +4.196722e-08 )
    photon_sf.add_var( 'HiPtId_inner_cov11', +1.953810e-09 )

    photon_sf.add_var( 'HiPtId_outer_const', +1.016154e+00 )
    photon_sf.add_var( 'HiPtId_outer_cov00', +1.971348e-05 )
    photon_sf.add_var( 'HiPtId_outer_cov01', +4.213067e-08 )
    photon_sf.add_var( 'HiPtId_outer_cov11', +4.083047e-09 )

    photon_sf.add_var( 'FilePathPSveto', '%s/2018/2018_HasPix_SF_DYJets_MCatNLO_asNominal.root' %base_path )
    photon_sf.add_var( 'HistPSveto', 'eleVeto_SF' )
    photon_sf.add_var( 'HistPSveto_err', 'eleVeto_StatUnc' )
    photon_sf.add_var( 'FilePathEveto', '%s/2018/2018_CSEV_SF_DYJets_MCatNLO_asNominal.root' %base_path )
    photon_sf.add_var( 'HistCSEveto', 'eleVeto_SF' )
    photon_sf.add_var( 'HistCSEveto_err', 'eleVeto_StatUnc' )
    
    return photon_sf

def get_pileup_sf(options) :

    base_path = '%s/TreeFilter/ApplyScaleFactors/data' %_workarea

    pileup_sf = Filter( 'AddPileupSF' )
    pileup_sf.add_var( 'DataFilePath', '%s/Data_Pileup_2012_ReReco-600bins.root' % base_path)
    pileup_sf.add_var( 'MCFilePath', options['PUDistMCFile'] )

    return pileup_sf

def vary_egamma_scale_up (options) :
    print 'GOTHERE'
    egamma_vary = Filter( 'VaryEGammaScale' )
    egamma_vary.add_var( 'Direction', 'UP' )
    return egamma_vary

def vary_egamma_scale_dn(options) :
    egamma_vary = Filter( 'VaryEGammaScale' )
    egamma_vary.add_var( 'Direction', 'DN' )
    return egamma_vary

def vary_muon_scale_up (options) :
    muon_vary = Filter( 'VaryMuonScale' )
    muon_vary.add_var( 'Direction', 'UP' )
    return muon_vary

def vary_muon_scale_dn(options) :
    muon_vary = Filter( 'VaryMuonScale' )
    muon_vary.add_var( 'Direction', 'DN' )
    return muon_vary

def vary_met_uncert(options) :
    return Filter( 'AddMETUncert' )



