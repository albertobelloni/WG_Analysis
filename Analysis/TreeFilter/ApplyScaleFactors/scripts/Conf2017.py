from core import Filter
import os
import sys
import inspect

_workarea = os.getenv( 'WorkArea' )
theyear = 2017

# integrated luminosities in microbarns
int_lumi_b = 4793969902.341
int_lumi_c = 9633143154.021
int_lumi_d = 4247792714.244
int_lumi_e = 9314581016.416
int_lumi_f = 13540062032.243

int_lumi_bcdef = int_lumi_b + int_lumi_c + int_lumi_d + int_lumi_e + int_lumi_f
int_lumi_gh = 0.0

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

    muon_sf.add_var( 'FilePathTrigBCDEF', '%s/2017/MuTrigEfficienciesAndSF_RunBtoF_Nov17Nov2017.root' %base_path )
    muon_sf.add_var( 'HistTrigBCDEF', 'IsoMu27_PtEtaBins/pt_abseta_ratio' )
    muon_sf.add_var( 'HistTrigBCDEFdata', 'IsoMu27_PtEtaBins/efficienciesDATA/pt_abseta_DATA' )
    muon_sf.add_var( 'HistTrigBCDEFmc', 'IsoMu27_PtEtaBins/efficienciesMC/pt_abseta_MC' )
    #muon_sf.add_var( 'FilePathTrigGH', '' )
    #muon_sf.add_var( 'HistTrigGH', '' )

    muon_sf.add_var( 'FilePathIdBCDEF', '%s/2017/RunBCDEF_mu_SF_ID.root' %base_path )
    muon_sf.add_var( 'HistIdBCDEF','NUM_TightID_DEN_genTracks_pt_abseta' )
    #muon_sf.add_var( 'FilePathIdGH', '' )
    #muon_sf.add_var( 'HistIdGH', '' )

    muon_sf.add_var( 'FilePathIsoBCDEF', '%s/2017/RunBCDEF_mu_SF_ISO.root' %base_path )
    muon_sf.add_var ('HistIsoBCDEF','NUM_TightRelIso_DEN_TightIDandIPCut_pt_abseta')
    #muon_sf.add_var( 'FilePathIsoGH', '' )
    #muon_sf.add_var ('HistIsoGH','')

    return muon_sf

def get_electron_sf(options) :

    base_path = '%s/TreeFilter/ApplyScaleFactors/data' %_workarea

    electron_sf = Filter( 'AddElectronSF' )

    electron_sf.add_var( 'year', theyear)

    electron_sf.add_var( 'FilePathRecoHighPt', '%s/2017/egammaEffi.txt_EGM2D_runBCDEF_passingRECO.root' %base_path)
    electron_sf.add_var( 'HistRecoHighPt', 'EGamma_SF2D')
    electron_sf.add_var( 'FilePathRecoLowPt',  '%s/2017/egammaEffi.txt_EGM2D_runBCDEF_passingRECO_lowEt.root' %base_path)
    electron_sf.add_var( 'HistRecoLowPt', 'EGamma_SF2D')
    electron_sf.add_var( 'FilePathCutID',      '%s/2017/2017_cutbasedID_ElectronTight.root' %base_path)
    electron_sf.add_var( 'HistCutID', 'EGamma_SF2D')
    electron_sf.add_var( 'FilePathTrigEl', '%s/2017/SF_HLT_Ele35_WPTight_Gsf_2017.root' %base_path )
    electron_sf.add_var( 'HistTrigEl', 'EGamma_SF2D' )
    electron_sf.add_var( 'HistTrigElData', 'EGamma_EffData2D' )
    electron_sf.add_var( 'HistTrigElMC', 'EGamma_EffMC2D' )

    return electron_sf

def get_photon_sf(options) :

    base_path = '%s/TreeFilter/ApplyScaleFactors/data' %_workarea

    photon_sf = Filter( 'AddPhotonSF' )

    photon_sf.add_var( 'year', theyear)

    photon_sf.add_var( 'FilePathId', '%s/2017/2017_cutbasedID_PhotonsMedium.root' %base_path )
    photon_sf.add_var( 'HistId', 'EGamma_SF2D' )

    photon_sf.add_var( 'FilePathPSveto', '%s/2017/PixelSeed_ScaleFactors_2017.root' %base_path )
    photon_sf.add_var( 'HistPSveto', 'Medium_ID' )
    photon_sf.add_var( 'FilePathEveto', '%s/2017/CSEV_ScaleFactors_2017.root' %base_path )
    photon_sf.add_var( 'HistCSEveto', 'Medium_ID' )
    
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



