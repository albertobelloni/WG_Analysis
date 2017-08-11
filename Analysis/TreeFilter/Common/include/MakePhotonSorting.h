namespace Wgg {
void MakePhotonSorting(const std::vector<TLorentzVector> & photons, 
                                     std::vector<float> * ph_sigmaIEIE,
                                     std::vector<float> * ph_chIsoCorr,
                                     std::vector<float> * ph_phoIsoCorr,
                                     std::vector<float> * ph_neuIsoCorr,
                                     std::vector<Bool_t> * ph_passHOverEMedium  ,
                                     std::vector<Bool_t> * ph_passSIEIEMedium,
                                     std::vector<Bool_t> * ph_passChIsoCorrMedium,
                                     std::vector<Bool_t> * ph_passNeuIsoCorrMedium,
                                     std::vector<Bool_t> * ph_passPhoIsoCorrMedium,
                                     std::vector<Bool_t> * ph_hasPixSeed,
                                     std::vector<Bool_t> * ph_eleVeto,
                                     std::map<std::string, int> & results,
                                     std::map<std::string, std::vector<int> > & vector_results
        );
}

void Wgg::MakePhotonSorting(const std::vector<TLorentzVector> & photons, 
                                     std::vector<float> * ph_sigmaIEIE,
                                     std::vector<float> * ph_chIsoCorr,
                                     std::vector<float> * ph_phoIsoCorr,
                                     std::vector<float> * ph_neuIsoCorr,
                                     std::vector<Bool_t> * ph_passHOverEMedium,
                                     std::vector<Bool_t> * ph_passSIEIEMedium,
                                     std::vector<Bool_t> * ph_passChIsoCorrMedium,
                                     std::vector<Bool_t> * ph_passNeuIsoCorrMedium,
                                     std::vector<Bool_t> * ph_passPhoIsoCorrMedium,
                                     std::vector<Bool_t> * ph_hasPixSeed,
                                     std::vector<Bool_t> * ph_eleVeto,
                                     std::map<std::string, int> & results,
                                     std::map<std::string, std::vector<int> > & vector_results
        ) {

    vector_results["ptSorted_ph_noSIEIEiso533_idx"] = std::vector<int>();
    vector_results["ptSorted_ph_noSIEIEiso855_idx"] = std::vector<int>();
    vector_results["ptSorted_ph_noSIEIEiso1077_idx"] = std::vector<int>();
    vector_results["ptSorted_ph_noSIEIEiso1299_idx"] = std::vector<int>();
    vector_results["ptSorted_ph_noSIEIEiso151111_idx"] = std::vector<int>();
    vector_results["ptSorted_ph_noSIEIEiso201616_idx"] = std::vector<int>();
    vector_results["ptSorted_ph_passSIEIEiso53None_idx"] = std::vector<int>();
    vector_results["ptSorted_ph_passSIEIEiso85None_idx"] = std::vector<int>();
    vector_results["ptSorted_ph_passSIEIEiso107None_idx"] = std::vector<int>();
    vector_results["ptSorted_ph_passSIEIEiso129None_idx"] = std::vector<int>();
    vector_results["ptSorted_ph_passSIEIEiso1511None_idx"] = std::vector<int>();
    vector_results["ptSorted_ph_passSIEIEiso2016None_idx"] = std::vector<int>();
    vector_results["ptSorted_ph_passSIEIEiso5None3_idx"] = std::vector<int>();
    vector_results["ptSorted_ph_passSIEIEiso8None5_idx"] = std::vector<int>();
    vector_results["ptSorted_ph_passSIEIEiso10None7_idx"] = std::vector<int>();
    vector_results["ptSorted_ph_passSIEIEiso12None9_idx"] = std::vector<int>();
    vector_results["ptSorted_ph_passSIEIEiso15None11_idx"] = std::vector<int>();
    vector_results["ptSorted_ph_passSIEIEiso20None16_idx"] = std::vector<int>();
    vector_results["ptSorted_ph_passSIEIEisoNone33_idx"] = std::vector<int>();
    vector_results["ptSorted_ph_passSIEIEisoNone55_idx"] = std::vector<int>();
    vector_results["ptSorted_ph_passSIEIEisoNone77_idx"] = std::vector<int>();
    vector_results["ptSorted_ph_passSIEIEisoNone99_idx"] = std::vector<int>();
    vector_results["ptSorted_ph_passSIEIEisoNone1111_idx"] = std::vector<int>();
    vector_results["ptSorted_ph_passSIEIEisoNone1616_idx"] = std::vector<int>();
    vector_results["ptSorted_ph_failSIEIEiso53None_idx"] = std::vector<int>();
    vector_results["ptSorted_ph_failSIEIEiso85None_idx"] = std::vector<int>();
    vector_results["ptSorted_ph_failSIEIEiso107None_idx"] = std::vector<int>();
    vector_results["ptSorted_ph_failSIEIEiso129None_idx"] = std::vector<int>();
    vector_results["ptSorted_ph_failSIEIEiso1511None_idx"] = std::vector<int>();
    vector_results["ptSorted_ph_failSIEIEiso2016None_idx"] = std::vector<int>();
    vector_results["ptSorted_ph_failSIEIEiso5None3_idx"] = std::vector<int>();
    vector_results["ptSorted_ph_failSIEIEiso8None5_idx"] = std::vector<int>();
    vector_results["ptSorted_ph_failSIEIEiso10None7_idx"] = std::vector<int>();
    vector_results["ptSorted_ph_failSIEIEiso12None9_idx"] = std::vector<int>();
    vector_results["ptSorted_ph_failSIEIEiso15None11_idx"] = std::vector<int>();
    vector_results["ptSorted_ph_failSIEIEiso20None16_idx"] = std::vector<int>();
    vector_results["ptSorted_ph_failSIEIEisoNone33_idx"] = std::vector<int>();
    vector_results["ptSorted_ph_failSIEIEisoNone55_idx"] = std::vector<int>();
    vector_results["ptSorted_ph_failSIEIEisoNone77_idx"] = std::vector<int>();
    vector_results["ptSorted_ph_failSIEIEisoNone99_idx"] = std::vector<int>();
    vector_results["ptSorted_ph_failSIEIEisoNone1111_idx"] = std::vector<int>();
    vector_results["ptSorted_ph_failSIEIEisoNone1616_idx"] = std::vector<int>();
    vector_results["ptSorted_ph_mediumNoNeuIsoNoPhoIso_idx"] = std::vector<int>();
    vector_results["ptSorted_ph_mediumNoChIsoNoPhoIso_idx"] = std::vector<int>();
    vector_results["ptSorted_ph_mediumNoChIsoNoNeuIso_idx"] = std::vector<int>();
    vector_results["ptSorted_ph_mediumNoSIEIENoPhoIsoNoEleVeto_idx"] = std::vector<int>();
    vector_results["ptSorted_ph_mediumNoSIEIENoNeuIsoNoEleVeto_idx"] = std::vector<int>();
    vector_results["ptSorted_ph_mediumNoSIEIENoChIsoNoEleVeto_idx"] = std::vector<int>();
    vector_results["ptSorted_ph_mediumNoSIEIENoChIso_idx"] = std::vector<int>();
    vector_results["ptSorted_ph_mediumNoSIEIENoPhoIsoPassPSV_idx"] = std::vector<int>();
    vector_results["ptSorted_ph_mediumNoSIEIENoNeuIsoPassPSV_idx"] = std::vector<int>();
    vector_results["ptSorted_ph_mediumNoSIEIENoChIsoPassPSV_idx"] = std::vector<int>();
    vector_results["ptSorted_ph_mediumNoSIEIENoPhoIsoFailPSV_idx"] = std::vector<int>();
    vector_results["ptSorted_ph_mediumNoSIEIENoNeuIsoFailPSV_idx"] = std::vector<int>();
    vector_results["ptSorted_ph_mediumNoSIEIENoChIsoFailPSV_idx"] = std::vector<int>();
    vector_results["ptSorted_ph_mediumNoSIEIENoPhoIsoPassCSEV_idx"] = std::vector<int>();
    vector_results["ptSorted_ph_mediumNoSIEIENoNeuIsoPassCSEV_idx"] = std::vector<int>();
    vector_results["ptSorted_ph_mediumNoSIEIENoChIsoPassCSEV_idx"] = std::vector<int>();
    vector_results["ptSorted_ph_mediumNoSIEIENoPhoIsoFailCSEV_idx"] = std::vector<int>();
    vector_results["ptSorted_ph_mediumNoSIEIENoNeuIsoFailCSEV_idx"] = std::vector<int>();
    vector_results["ptSorted_ph_mediumNoSIEIENoChIsoFailCSEV_idx"] = std::vector<int>();
    vector_results["ptSorted_ph_mediumNoSIEIENoEleVeto_idx"] = std::vector<int>();
    vector_results["ptSorted_ph_mediumNoSIEIEPassPSV_idx"] = std::vector<int>();
    vector_results["ptSorted_ph_mediumNoSIEIEFailPSV_idx"] = std::vector<int>();
    vector_results["ptSorted_ph_mediumNoSIEIEPassCSEV_idx"] = std::vector<int>();
    vector_results["ptSorted_ph_mediumNoSIEIEFailCSEV_idx"] = std::vector<int>();
    vector_results["ptSorted_ph_mediumNoEleVeto_idx"] = std::vector<int>();
    vector_results["ptSorted_ph_mediumPassPSV_idx"] = std::vector<int>();
    vector_results["ptSorted_ph_mediumFailPSV_idx"] = std::vector<int>();
    vector_results["ptSorted_ph_mediumPassCSEV_idx"] = std::vector<int>();
    vector_results["ptSorted_ph_mediumFailCSEV_idx"] = std::vector<int>();
    vector_results["ptSorted_ph_mediumNoChIsoNoEleVeto_idx"] = std::vector<int>();
    vector_results["ptSorted_ph_mediumNoChIsoPassPSV_idx"] = std::vector<int>();
    vector_results["ptSorted_ph_mediumNoChIsoFailPSV_idx"] = std::vector<int>();
    vector_results["ptSorted_ph_mediumNoChIsoPassCSEV_idx"] = std::vector<int>();
    vector_results["ptSorted_ph_mediumNoChIsoFailCSEV_idx"] = std::vector<int>();
    vector_results["ptSorted_ph_mediumNoNeuIsoNoEleVeto_idx"] = std::vector<int>();
    vector_results["ptSorted_ph_mediumNoNeuIsoPassPSV_idx"] = std::vector<int>();
    vector_results["ptSorted_ph_mediumNoNeuIsoFailPSV_idx"] = std::vector<int>();
    vector_results["ptSorted_ph_mediumNoNeuIsoPassCSEV_idx"] = std::vector<int>();
    vector_results["ptSorted_ph_mediumNoNeuIsoFailCSEV_idx"] = std::vector<int>();
    vector_results["ptSorted_ph_mediumNoPhoIsoNoEleVeto_idx"] = std::vector<int>();
    vector_results["ptSorted_ph_mediumNoPhoIsoPassPSV_idx"] = std::vector<int>();
    vector_results["ptSorted_ph_mediumNoPhoIsoFailPSV_idx"] = std::vector<int>();
    vector_results["ptSorted_ph_mediumNoPhoIsoPassCSEV_idx"] = std::vector<int>();
    vector_results["ptSorted_ph_mediumNoPhoIsoFailCSEV_idx"] = std::vector<int>();

    std::vector<std::pair<float, int> > sorted_photons_iso533;
    std::vector<std::pair<float, int> > sorted_photons_iso855;
    std::vector<std::pair<float, int> > sorted_photons_iso1077;
    std::vector<std::pair<float, int> > sorted_photons_iso1299;
    std::vector<std::pair<float, int> > sorted_photons_iso151111;
    std::vector<std::pair<float, int> > sorted_photons_iso201616;
    std::vector<std::pair<float, int> > sorted_photons_passSIEIEiso53None;
    std::vector<std::pair<float, int> > sorted_photons_passSIEIEiso85None;
    std::vector<std::pair<float, int> > sorted_photons_passSIEIEiso107None;
    std::vector<std::pair<float, int> > sorted_photons_passSIEIEiso129None;
    std::vector<std::pair<float, int> > sorted_photons_passSIEIEiso1511None;
    std::vector<std::pair<float, int> > sorted_photons_passSIEIEiso2016None;
    std::vector<std::pair<float, int> > sorted_photons_passSIEIEiso5None3;
    std::vector<std::pair<float, int> > sorted_photons_passSIEIEiso8None5;
    std::vector<std::pair<float, int> > sorted_photons_passSIEIEiso10None7;
    std::vector<std::pair<float, int> > sorted_photons_passSIEIEiso12None9;
    std::vector<std::pair<float, int> > sorted_photons_passSIEIEiso15None11;
    std::vector<std::pair<float, int> > sorted_photons_passSIEIEiso20None16;
    std::vector<std::pair<float, int> > sorted_photons_passSIEIEisoNone33;
    std::vector<std::pair<float, int> > sorted_photons_passSIEIEisoNone55;
    std::vector<std::pair<float, int> > sorted_photons_passSIEIEisoNone77;
    std::vector<std::pair<float, int> > sorted_photons_passSIEIEisoNone99;
    std::vector<std::pair<float, int> > sorted_photons_passSIEIEisoNone1111;
    std::vector<std::pair<float, int> > sorted_photons_passSIEIEisoNone1616;
    std::vector<std::pair<float, int> > sorted_photons_failSIEIEiso53None;
    std::vector<std::pair<float, int> > sorted_photons_failSIEIEiso85None;
    std::vector<std::pair<float, int> > sorted_photons_failSIEIEiso107None;
    std::vector<std::pair<float, int> > sorted_photons_failSIEIEiso129None;
    std::vector<std::pair<float, int> > sorted_photons_failSIEIEiso1511None;
    std::vector<std::pair<float, int> > sorted_photons_failSIEIEiso2016None;
    std::vector<std::pair<float, int> > sorted_photons_failSIEIEiso5None3;
    std::vector<std::pair<float, int> > sorted_photons_failSIEIEiso8None5;
    std::vector<std::pair<float, int> > sorted_photons_failSIEIEiso10None7;
    std::vector<std::pair<float, int> > sorted_photons_failSIEIEiso12None9;
    std::vector<std::pair<float, int> > sorted_photons_failSIEIEiso15None11;
    std::vector<std::pair<float, int> > sorted_photons_failSIEIEiso20None16;
    std::vector<std::pair<float, int> > sorted_photons_failSIEIEisoNone33;
    std::vector<std::pair<float, int> > sorted_photons_failSIEIEisoNone55;
    std::vector<std::pair<float, int> > sorted_photons_failSIEIEisoNone77;
    std::vector<std::pair<float, int> > sorted_photons_failSIEIEisoNone99;
    std::vector<std::pair<float, int> > sorted_photons_failSIEIEisoNone1111;
    std::vector<std::pair<float, int> > sorted_photons_failSIEIEisoNone1616;
    std::vector<std::pair<float, int> > sorted_photons_mediumNoNeuIsoNoPhoIso;
    std::vector<std::pair<float, int> > sorted_photons_mediumNoChIsoNoPhoIso;
    std::vector<std::pair<float, int> > sorted_photons_mediumNoChIsoNoNeuIso;
    std::vector<std::pair<float, int> > sorted_photons_mediumNoSIEIENoPhoIsoNoEleVeto;
    std::vector<std::pair<float, int> > sorted_photons_mediumNoSIEIENoNeuIsoNoEleVeto;
    std::vector<std::pair<float, int> > sorted_photons_mediumNoSIEIENoChIsoNoEleVeto;
    std::vector<std::pair<float, int> > sorted_photons_mediumNoSIEIENoPhoIsoPassPSV;
    std::vector<std::pair<float, int> > sorted_photons_mediumNoSIEIENoNeuIsoPassPSV;
    std::vector<std::pair<float, int> > sorted_photons_mediumNoSIEIENoChIsoPassPSV;
    std::vector<std::pair<float, int> > sorted_photons_mediumNoSIEIENoPhoIsoFailPSV;
    std::vector<std::pair<float, int> > sorted_photons_mediumNoSIEIENoNeuIsoFailPSV;
    std::vector<std::pair<float, int> > sorted_photons_mediumNoSIEIENoChIsoFailPSV;
    std::vector<std::pair<float, int> > sorted_photons_mediumNoSIEIENoPhoIsoPassCSEV;
    std::vector<std::pair<float, int> > sorted_photons_mediumNoSIEIENoNeuIsoPassCSEV;
    std::vector<std::pair<float, int> > sorted_photons_mediumNoSIEIENoChIsoPassCSEV;
    std::vector<std::pair<float, int> > sorted_photons_mediumNoSIEIENoPhoIsoFailCSEV;
    std::vector<std::pair<float, int> > sorted_photons_mediumNoSIEIENoNeuIsoFailCSEV;
    std::vector<std::pair<float, int> > sorted_photons_mediumNoSIEIENoChIsoFailCSEV;
    std::vector<std::pair<float, int> > sorted_photons_mediumNoSIEIENoEleVeto;
    std::vector<std::pair<float, int> > sorted_photons_mediumNoSIEIEPassPSV;
    std::vector<std::pair<float, int> > sorted_photons_mediumNoSIEIEFailPSV;
    std::vector<std::pair<float, int> > sorted_photons_mediumNoSIEIEPassCSEV;
    std::vector<std::pair<float, int> > sorted_photons_mediumNoSIEIEFailCSEV;
    std::vector<std::pair<float, int> > sorted_photons_mediumNoEleVeto;
    std::vector<std::pair<float, int> > sorted_photons_mediumPassPSV;
    std::vector<std::pair<float, int> > sorted_photons_mediumFailPSV;
    std::vector<std::pair<float, int> > sorted_photons_mediumPassCSEV;
    std::vector<std::pair<float, int> > sorted_photons_mediumFailCSEV;
    std::vector<std::pair<float, int> > sorted_photons_mediumNoChIsoNoEleVeto;
    std::vector<std::pair<float, int> > sorted_photons_mediumNoChIsoPassPSV;
    std::vector<std::pair<float, int> > sorted_photons_mediumNoChIsoFailPSV;
    std::vector<std::pair<float, int> > sorted_photons_mediumNoChIsoPassCSEV;
    std::vector<std::pair<float, int> > sorted_photons_mediumNoChIsoFailCSEV;
    std::vector<std::pair<float, int> > sorted_photons_mediumNoNeuIsoNoEleVeto;
    std::vector<std::pair<float, int> > sorted_photons_mediumNoNeuIsoPassPSV;
    std::vector<std::pair<float, int> > sorted_photons_mediumNoNeuIsoFailPSV;
    std::vector<std::pair<float, int> > sorted_photons_mediumNoNeuIsoPassCSEV;
    std::vector<std::pair<float, int> > sorted_photons_mediumNoNeuIsoFailCSEV;
    std::vector<std::pair<float, int> > sorted_photons_mediumNoPhoIsoNoEleVeto;
    std::vector<std::pair<float, int> > sorted_photons_mediumNoPhoIsoPassPSV;
    std::vector<std::pair<float, int> > sorted_photons_mediumNoPhoIsoFailPSV;
    std::vector<std::pair<float, int> > sorted_photons_mediumNoPhoIsoPassCSEV;
    std::vector<std::pair<float, int> > sorted_photons_mediumNoPhoIsoFailCSEV;

    int ph_noSIEIEiso533_n = 0;
    int ph_noSIEIEiso855_n = 0;
    int ph_noSIEIEiso1077_n = 0;
    int ph_noSIEIEiso1299_n = 0;
    int ph_noSIEIEiso151111_n = 0;
    int ph_noSIEIEiso201616_n = 0;
    int ph_passSIEIEiso53None_n = 0;
    int ph_passSIEIEiso85None_n = 0;
    int ph_passSIEIEiso107None_n = 0;
    int ph_passSIEIEiso129None_n = 0;
    int ph_passSIEIEiso1511None_n = 0;
    int ph_passSIEIEiso2016None_n = 0;
    int ph_passSIEIEiso5None3_n = 0;
    int ph_passSIEIEiso8None5_n = 0;
    int ph_passSIEIEiso10None7_n = 0;
    int ph_passSIEIEiso12None9_n = 0;
    int ph_passSIEIEiso15None11_n = 0;
    int ph_passSIEIEiso20None16_n = 0;
    int ph_passSIEIEisoNone33_n = 0;
    int ph_passSIEIEisoNone55_n = 0;
    int ph_passSIEIEisoNone77_n = 0;
    int ph_passSIEIEisoNone99_n = 0;
    int ph_passSIEIEisoNone1111_n = 0;
    int ph_passSIEIEisoNone1616_n = 0;
    int ph_failSIEIEiso53None_n = 0;
    int ph_failSIEIEiso85None_n = 0;
    int ph_failSIEIEiso107None_n = 0;
    int ph_failSIEIEiso129None_n = 0;
    int ph_failSIEIEiso1511None_n = 0;
    int ph_failSIEIEiso2016None_n = 0;
    int ph_failSIEIEiso5None3_n = 0;
    int ph_failSIEIEiso8None5_n = 0;
    int ph_failSIEIEiso10None7_n = 0;
    int ph_failSIEIEiso12None9_n = 0;
    int ph_failSIEIEiso15None11_n = 0;
    int ph_failSIEIEiso20None16_n = 0;
    int ph_failSIEIEisoNone33_n = 0;
    int ph_failSIEIEisoNone55_n = 0;
    int ph_failSIEIEisoNone77_n = 0;
    int ph_failSIEIEisoNone99_n = 0;
    int ph_failSIEIEisoNone1111_n = 0;
    int ph_failSIEIEisoNone1616_n = 0;
    int ph_mediumNoNeuIsoNoPhoIso_n = 0;
    int ph_mediumNoChIsoNoPhoIso_n = 0;
    int ph_mediumNoChIsoNoNeuIso_n = 0;
    int ph_mediumNoSIEIENoPhoIsoNoEleVeto_n = 0;
    int ph_mediumNoSIEIENoPhoIsoPassPSV_n = 0;
    int ph_mediumNoSIEIENoPhoIsoFailPSV_n = 0;
    int ph_mediumNoSIEIENoPhoIsoPassCSEV_n = 0;
    int ph_mediumNoSIEIENoPhoIsoFailCSEV_n = 0;
    int ph_mediumNoSIEIENoNeuIsoNoEleVeto_n = 0;
    int ph_mediumNoSIEIENoNeuIsoPassPSV_n = 0;
    int ph_mediumNoSIEIENoNeuIsoFailPSV_n = 0;
    int ph_mediumNoSIEIENoNeuIsoPassCSEV_n = 0;
    int ph_mediumNoSIEIENoNeuIsoFailCSEV_n = 0;
    int ph_mediumNoSIEIENoChIsoNoEleVeto_n = 0;
    int ph_mediumNoSIEIENoChIso_n = 0;
    int ph_mediumNoSIEIENoChIsoPassPSV_n = 0;
    int ph_mediumNoSIEIENoChIsoFailPSV_n = 0;
    int ph_mediumNoSIEIENoChIsoPassCSEV_n = 0;
    int ph_mediumNoSIEIENoChIsoFailCSEV_n = 0;
    int ph_mediumNoSIEIENoEleVeto_n = 0;
    int ph_mediumNoSIEIEPassPSV_n = 0;
    int ph_mediumNoSIEIEFailPSV_n = 0;
    int ph_mediumNoSIEIEPassCSEV_n = 0;
    int ph_mediumNoSIEIEFailCSEV_n = 0;
    int ph_mediumNoEleVeto_n = 0;
    int ph_mediumPassPSV_n = 0;
    int ph_mediumFailPSV_n = 0;
    int ph_mediumPassCSEV_n = 0;
    int ph_mediumFailCSEV_n = 0;
    int ph_mediumNoChIsoNoEleVeto_n = 0;
    int ph_mediumNoChIsoPassPSV_n = 0;
    int ph_mediumNoChIsoFailPSV_n = 0;
    int ph_mediumNoChIsoPassCSEV_n = 0;
    int ph_mediumNoChIsoFailCSEV_n = 0;
    int ph_mediumNoNeuIsoNoEleVeto_n = 0;
    int ph_mediumNoNeuIsoPassPSV_n = 0;
    int ph_mediumNoNeuIsoFailPSV_n = 0;
    int ph_mediumNoNeuIsoPassCSEV_n = 0;
    int ph_mediumNoNeuIsoFailCSEV_n = 0;
    int ph_mediumNoPhoIsoNoEleVeto_n = 0;
    int ph_mediumNoPhoIsoPassPSV_n = 0;
    int ph_mediumNoPhoIsoFailPSV_n = 0;
    int ph_mediumNoPhoIsoPassCSEV_n = 0;
    int ph_mediumNoPhoIsoFailCSEV_n = 0;



    for( unsigned idx = 0; idx < photons.size(); ++idx ) {

        std::pair<float, int> sort_pair = std::make_pair( photons[idx].Pt(), idx );

        if( ph_passHOverEMedium->at(idx)) {

            if( ph_chIsoCorr->at(idx) < 5   && 
                ph_neuIsoCorr->at(idx) < 3  && 
                ph_phoIsoCorr->at(idx) < 3 ) {
                ph_noSIEIEiso533_n++;
                sorted_photons_iso533.push_back( sort_pair );
            }
            
            if( ph_chIsoCorr->at(idx) < 8  && 
                ph_neuIsoCorr->at(idx) < 5 && 
                ph_phoIsoCorr->at(idx) < 5 ) {
                ph_noSIEIEiso855_n++;
                sorted_photons_iso855.push_back( sort_pair );
            }
            
            if( ph_chIsoCorr->at(idx) < 10 && 
                ph_neuIsoCorr->at(idx) < 7  && 
                ph_phoIsoCorr->at(idx) < 7 ) {
                ph_noSIEIEiso1077_n++;
                sorted_photons_iso1077.push_back( sort_pair );
            }
            
            if( ph_chIsoCorr->at(idx) < 12 && 
                ph_neuIsoCorr->at(idx) < 9  && 
                ph_phoIsoCorr->at(idx) < 9 ) {
                ph_noSIEIEiso1299_n++;
                sorted_photons_iso1299.push_back( sort_pair );
            }
            
            if( ph_chIsoCorr->at(idx) < 15 && 
                ph_neuIsoCorr->at(idx) < 11 && 
                ph_phoIsoCorr->at(idx) < 11 ) {
                ph_noSIEIEiso151111_n++;
                sorted_photons_iso151111.push_back( sort_pair );
            }
            
            if( ph_chIsoCorr->at(idx) < 20 && 
                ph_neuIsoCorr->at(idx) < 16 && 
                ph_phoIsoCorr->at(idx) < 16 ) {
                ph_noSIEIEiso201616_n++;
                sorted_photons_iso201616.push_back( sort_pair );
            }
            if( ph_passSIEIEMedium->at(idx) ) {

                // For phoIsoCorr, passing SIEIE, loosen other isolations
                if( ph_chIsoCorr->at(idx) < 5   && 
                    ph_neuIsoCorr->at(idx) < 3 ) {
                    ph_passSIEIEiso53None_n++;
                    sorted_photons_passSIEIEiso53None.push_back( sort_pair );
                }
                
                if( ph_chIsoCorr->at(idx) < 8  && 
                    ph_neuIsoCorr->at(idx) < 5 ) {
                    ph_passSIEIEiso85None_n++;
                    sorted_photons_passSIEIEiso85None.push_back( sort_pair );
                }
                
                if( ph_chIsoCorr->at(idx) < 10 && 
                    ph_neuIsoCorr->at(idx) < 7 ) {
                    ph_passSIEIEiso107None_n++;
                    sorted_photons_passSIEIEiso107None.push_back( sort_pair );
                }
                
                if( ph_chIsoCorr->at(idx) < 12 && 
                    ph_neuIsoCorr->at(idx) < 9 ) {
                    ph_passSIEIEiso129None_n++;
                    sorted_photons_passSIEIEiso129None.push_back( sort_pair );
                }
                
                if( ph_chIsoCorr->at(idx) < 15 && 
                    ph_neuIsoCorr->at(idx) < 11 ) {
                    ph_passSIEIEiso1511None_n++;
                    sorted_photons_passSIEIEiso1511None.push_back( sort_pair );
                }
                
                if( ph_chIsoCorr->at(idx) < 20 && 
                    ph_neuIsoCorr->at(idx) < 16 ) {
                    ph_passSIEIEiso2016None_n++;
                    sorted_photons_passSIEIEiso2016None.push_back( sort_pair );
                }

                // For neuIsoCorr, passing SIEIE, loosen other isolations
                if( ph_chIsoCorr->at(idx) < 5   && 
                    ph_phoIsoCorr->at(idx) < 3 ) {
                    ph_passSIEIEiso5None3_n++;
                    sorted_photons_passSIEIEiso5None3.push_back( sort_pair );
                }
                
                if( ph_chIsoCorr->at(idx) < 8  && 
                    ph_phoIsoCorr->at(idx) < 5 ) {
                    ph_passSIEIEiso8None5_n++;
                    sorted_photons_passSIEIEiso8None5.push_back( sort_pair );
                }
                
                if( ph_chIsoCorr->at(idx) < 10 && 
                    ph_phoIsoCorr->at(idx) < 7 ) {
                    ph_passSIEIEiso10None7_n++;
                    sorted_photons_passSIEIEiso10None7.push_back( sort_pair );
                }
                
                if( ph_chIsoCorr->at(idx) < 12 && 
                    ph_phoIsoCorr->at(idx) < 9 ) {
                    ph_passSIEIEiso12None9_n++;
                    sorted_photons_passSIEIEiso12None9.push_back( sort_pair );
                }
                
                if( ph_chIsoCorr->at(idx) < 15 && 
                    ph_phoIsoCorr->at(idx) < 11 ) {
                    ph_passSIEIEiso15None11_n++;
                    sorted_photons_passSIEIEiso15None11.push_back( sort_pair );
                }
                
                if( ph_chIsoCorr->at(idx) < 20 && 
                    ph_phoIsoCorr->at(idx) < 16 ) {
                    ph_passSIEIEiso20None16_n++;
                    sorted_photons_passSIEIEiso20None16.push_back( sort_pair );
                }

                // For chIsoCorr, passing SIEIE, loosen other isolations
                if( ph_neuIsoCorr->at(idx) < 3  && 
                    ph_phoIsoCorr->at(idx) < 3 ) {
                    ph_passSIEIEisoNone33_n++;
                    sorted_photons_passSIEIEisoNone33.push_back( sort_pair );
                }
                
                if( ph_neuIsoCorr->at(idx) < 5 && 
                    ph_phoIsoCorr->at(idx) < 5 ) {
                    ph_passSIEIEisoNone55_n++;
                    sorted_photons_passSIEIEisoNone55.push_back( sort_pair );
                }
                
                if( ph_neuIsoCorr->at(idx) < 7  && 
                    ph_phoIsoCorr->at(idx) < 7 ) {
                    ph_passSIEIEisoNone77_n++;
                    sorted_photons_passSIEIEisoNone77.push_back( sort_pair );
                }
                
                if( ph_neuIsoCorr->at(idx) < 9  && 
                    ph_phoIsoCorr->at(idx) < 9 ) {
                    ph_passSIEIEisoNone99_n++;
                    sorted_photons_passSIEIEisoNone99.push_back( sort_pair );
                }
                
                if( ph_neuIsoCorr->at(idx) < 11 && 
                    ph_phoIsoCorr->at(idx) < 11 ) {
                    ph_passSIEIEisoNone1111_n++;
                    sorted_photons_passSIEIEisoNone1111.push_back( sort_pair );
                }
                
                if( ph_neuIsoCorr->at(idx) < 16 && 
                    ph_phoIsoCorr->at(idx) < 16 ) {
                    ph_passSIEIEisoNone1616_n++;
                    sorted_photons_passSIEIEisoNone1616.push_back( sort_pair );
                }
            }
            else {
                // For phoIsoCorr, failing SIEIE, loosen other isolations
                if( ph_chIsoCorr->at(idx) < 5   && 
                    ph_neuIsoCorr->at(idx) < 3 ) {
                    ph_failSIEIEiso53None_n++;
                    sorted_photons_failSIEIEiso53None.push_back( sort_pair );
                }
                
                if( ph_chIsoCorr->at(idx) < 8  && 
                    ph_neuIsoCorr->at(idx) < 5 ) {
                    ph_failSIEIEiso85None_n++;
                    sorted_photons_failSIEIEiso85None.push_back( sort_pair );
                }
                
                if( ph_chIsoCorr->at(idx) < 10 && 
                    ph_neuIsoCorr->at(idx) < 7 ) {
                    ph_failSIEIEiso107None_n++;
                    sorted_photons_failSIEIEiso107None.push_back( sort_pair );
                }
                
                if( ph_chIsoCorr->at(idx) < 12 && 
                    ph_neuIsoCorr->at(idx) < 9 ) {
                    ph_failSIEIEiso129None_n++;
                    sorted_photons_failSIEIEiso129None.push_back( sort_pair );
                }
                
                if( ph_chIsoCorr->at(idx) < 15 && 
                    ph_neuIsoCorr->at(idx) < 11 ) {
                    ph_failSIEIEiso1511None_n++;
                    sorted_photons_failSIEIEiso1511None.push_back( sort_pair );
                }
                
                if( ph_chIsoCorr->at(idx) < 20 && 
                    ph_neuIsoCorr->at(idx) < 16 ) {
                    ph_failSIEIEiso2016None_n++;
                    sorted_photons_failSIEIEiso2016None.push_back( sort_pair );
                }

                // For neuIsoCorr, failing SIEIE, loosen other isolations
                if( ph_chIsoCorr->at(idx) < 5   && 
                    ph_phoIsoCorr->at(idx) < 3 ) {
                    ph_failSIEIEiso5None3_n++;
                    sorted_photons_failSIEIEiso5None3.push_back( sort_pair );
                }
                
                if( ph_chIsoCorr->at(idx) < 8  && 
                    ph_phoIsoCorr->at(idx) < 5 ) {
                    ph_failSIEIEiso8None5_n++;
                    sorted_photons_failSIEIEiso8None5.push_back( sort_pair );
                }
                
                if( ph_chIsoCorr->at(idx) < 10 && 
                    ph_phoIsoCorr->at(idx) < 7 ) {
                    ph_failSIEIEiso10None7_n++;
                    sorted_photons_failSIEIEiso10None7.push_back( sort_pair );
                }
                
                if( ph_chIsoCorr->at(idx) < 12 && 
                    ph_phoIsoCorr->at(idx) < 9 ) {
                    ph_failSIEIEiso12None9_n++;
                    sorted_photons_failSIEIEiso12None9.push_back( sort_pair );
                }
                
                if( ph_chIsoCorr->at(idx) < 15 && 
                    ph_phoIsoCorr->at(idx) < 11 ) {
                    ph_failSIEIEiso15None11_n++;
                    sorted_photons_failSIEIEiso15None11.push_back( sort_pair );
                }
                
                if( ph_chIsoCorr->at(idx) < 20 && 
                    ph_phoIsoCorr->at(idx) < 16 ) {
                    ph_failSIEIEiso20None16_n++;
                    sorted_photons_failSIEIEiso20None16.push_back( sort_pair );
                }

                // For chIsoCorr, failing SIEIE, loosen other isolations
                if( ph_neuIsoCorr->at(idx) < 3  && 
                    ph_phoIsoCorr->at(idx) < 3 ) {
                    ph_failSIEIEisoNone33_n++;
                    sorted_photons_failSIEIEisoNone33.push_back( sort_pair );
                }
                
                if( ph_neuIsoCorr->at(idx) < 5 && 
                    ph_phoIsoCorr->at(idx) < 5 ) {
                    ph_failSIEIEisoNone55_n++;
                    sorted_photons_failSIEIEisoNone55.push_back( sort_pair );
                }
                
                if( ph_neuIsoCorr->at(idx) < 7  && 
                    ph_phoIsoCorr->at(idx) < 7 ) {
                    ph_failSIEIEisoNone77_n++;
                    sorted_photons_failSIEIEisoNone77.push_back( sort_pair );
                }
                
                if( ph_neuIsoCorr->at(idx) < 9  && 
                    ph_phoIsoCorr->at(idx) < 9 ) {
                    ph_failSIEIEisoNone99_n++;
                    sorted_photons_failSIEIEisoNone99.push_back( sort_pair );
                }
                
                if( ph_neuIsoCorr->at(idx) < 11 && 
                    ph_phoIsoCorr->at(idx) < 11 ) {
                    ph_failSIEIEisoNone1111_n++;
                    sorted_photons_failSIEIEisoNone1111.push_back( sort_pair );
                }
                
                if( ph_neuIsoCorr->at(idx) < 16 && 
                    ph_phoIsoCorr->at(idx) < 16 ) {
                    ph_failSIEIEisoNone1616_n++;
                    sorted_photons_failSIEIEisoNone1616.push_back( sort_pair );
                }
            }
        }
        if( ph_passHOverEMedium->at(idx)) { 
            if( ph_passSIEIEMedium->at(idx) ) { 
                if( ph_passChIsoCorrMedium->at(idx) ) {
                    ph_mediumNoNeuIsoNoPhoIso_n++;
                    sorted_photons_mediumNoNeuIsoNoPhoIso.push_back( sort_pair );
                }
                if( ph_passNeuIsoCorrMedium->at(idx) ) {
                    ph_mediumNoChIsoNoPhoIso_n++;
                    sorted_photons_mediumNoChIsoNoPhoIso.push_back( sort_pair );
                }
                if( ph_passPhoIsoCorrMedium->at(idx) ) {
                    ph_mediumNoChIsoNoNeuIso_n++;
                    sorted_photons_mediumNoChIsoNoNeuIso.push_back( sort_pair );
                }
            }
            if( ph_passChIsoCorrMedium->at(idx) ) { 
                if( ph_passNeuIsoCorrMedium->at(idx) ) {
                    ph_mediumNoSIEIENoPhoIsoNoEleVeto_n++;
                    sorted_photons_mediumNoSIEIENoPhoIsoNoEleVeto.push_back( sort_pair );
                    if( ph_hasPixSeed->at(idx)==0 ) {
                        ph_mediumNoSIEIENoPhoIsoPassPSV_n++;
                        sorted_photons_mediumNoSIEIENoPhoIsoPassPSV.push_back( sort_pair );
                    }
                    if( ph_hasPixSeed->at(idx)==1 ) {
                        ph_mediumNoSIEIENoPhoIsoFailPSV_n++;
                        sorted_photons_mediumNoSIEIENoPhoIsoFailPSV.push_back( sort_pair );
                    }
                    if( ph_eleVeto->at(idx)==0 ) {
                        ph_mediumNoSIEIENoPhoIsoPassCSEV_n++;
                        sorted_photons_mediumNoSIEIENoPhoIsoPassCSEV.push_back( sort_pair );
                    }
                    if( ph_eleVeto->at(idx)==1 ) {
                        ph_mediumNoSIEIENoPhoIsoFailCSEV_n++;
                        sorted_photons_mediumNoSIEIENoPhoIsoFailCSEV.push_back( sort_pair );
                    }
                }
                if( ph_passPhoIsoCorrMedium->at(idx) ) {
                    ph_mediumNoSIEIENoNeuIsoNoEleVeto_n++;
                    sorted_photons_mediumNoSIEIENoNeuIsoNoEleVeto.push_back( sort_pair );
                    if( ph_hasPixSeed->at(idx)==0 ) {
                        ph_mediumNoSIEIENoNeuIsoPassPSV_n++;
                        sorted_photons_mediumNoSIEIENoNeuIsoPassPSV.push_back( sort_pair );
                    }
                    if( ph_hasPixSeed->at(idx)==1 ) {
                        ph_mediumNoSIEIENoNeuIsoFailPSV_n++;
                        sorted_photons_mediumNoSIEIENoNeuIsoFailPSV.push_back( sort_pair );
                    }
                    if( ph_eleVeto->at(idx)==0 ) {
                        ph_mediumNoSIEIENoNeuIsoPassCSEV_n++;
                        sorted_photons_mediumNoSIEIENoNeuIsoPassCSEV.push_back( sort_pair );
                    }
                    if( ph_eleVeto->at(idx)==1 ) {
                        ph_mediumNoSIEIENoNeuIsoFailCSEV_n++;
                        sorted_photons_mediumNoSIEIENoNeuIsoFailCSEV.push_back( sort_pair );
                    }
                }
            }
            if( ph_passNeuIsoCorrMedium->at(idx) ) { 
                if( ph_passPhoIsoCorrMedium->at(idx) ) {
                    ph_mediumNoSIEIENoChIsoNoEleVeto_n++;
                    // for backwards compatibility
                    ph_mediumNoSIEIENoChIso_n++;
                    sorted_photons_mediumNoSIEIENoChIsoNoEleVeto.push_back( sort_pair );
                    if( ph_hasPixSeed->at(idx)==0 ) {
                        ph_mediumNoSIEIENoChIsoPassPSV_n++;
                        sorted_photons_mediumNoSIEIENoChIsoPassPSV.push_back( sort_pair );
                    }
                    if( ph_hasPixSeed->at(idx)==1 ) {
                        ph_mediumNoSIEIENoChIsoFailPSV_n++;
                        sorted_photons_mediumNoSIEIENoChIsoFailPSV.push_back( sort_pair );
                    }
                    if( ph_eleVeto->at(idx)==0 ) {
                        ph_mediumNoSIEIENoChIsoPassCSEV_n++;
                        sorted_photons_mediumNoSIEIENoChIsoPassCSEV.push_back( sort_pair );
                    }
                    if( ph_eleVeto->at(idx)==1 ) {
                        ph_mediumNoSIEIENoChIsoFailCSEV_n++;
                        sorted_photons_mediumNoSIEIENoChIsoFailCSEV.push_back( sort_pair );
                    }
                }
            }
        }
        if( ph_passHOverEMedium->at(idx) && ph_passChIsoCorrMedium->at(idx)  && ph_passNeuIsoCorrMedium->at(idx) && ph_passPhoIsoCorrMedium->at(idx) ) {
            ph_mediumNoSIEIENoEleVeto_n++;
            sorted_photons_mediumNoSIEIENoEleVeto.push_back( sort_pair );

            if( ph_hasPixSeed->at(idx)==0 ) {
                ph_mediumNoSIEIEPassPSV_n++;
                sorted_photons_mediumNoSIEIEPassPSV.push_back( sort_pair );
            }
            if( ph_hasPixSeed->at(idx)==1 ) {
                ph_mediumNoSIEIEFailPSV_n++;
                sorted_photons_mediumNoSIEIEFailPSV.push_back( sort_pair );
            }
            if( ph_eleVeto->at(idx)==0 ) {
                ph_mediumNoSIEIEPassCSEV_n++;
                sorted_photons_mediumNoSIEIEPassCSEV.push_back( sort_pair );
            }
            if( ph_eleVeto->at(idx)==1 ) {
                ph_mediumNoSIEIEFailCSEV_n++;
                sorted_photons_mediumNoSIEIEFailCSEV.push_back( sort_pair );
            }
            if( ph_passSIEIEMedium->at(idx) ) {
                ph_mediumNoEleVeto_n++;
                sorted_photons_mediumNoEleVeto.push_back( sort_pair );
            
                if( ph_hasPixSeed->at(idx)==0 ) {
                    ph_mediumPassPSV_n++;
                    sorted_photons_mediumPassPSV.push_back( sort_pair );
                }
                if( ph_hasPixSeed->at(idx)==1 ) {
                    ph_mediumFailPSV_n++;
                    sorted_photons_mediumFailPSV.push_back( sort_pair );
                }
                if( ph_eleVeto->at(idx)==0 ) {
                    ph_mediumPassCSEV_n++;
                    sorted_photons_mediumPassCSEV.push_back( sort_pair );
                }
                if( ph_eleVeto->at(idx)==1 ) {
                    ph_mediumFailCSEV_n++;
                    sorted_photons_mediumFailCSEV.push_back( sort_pair );
                }
            }
        }
        if( ph_passHOverEMedium->at(idx) && ph_passSIEIEMedium->at(idx)  && ph_passNeuIsoCorrMedium->at(idx) && ph_passPhoIsoCorrMedium->at(idx) ) {
            ph_mediumNoChIsoNoEleVeto_n++;
            sorted_photons_mediumNoChIsoNoEleVeto.push_back( sort_pair );

            if( ph_hasPixSeed->at(idx)==0 ) {
                ph_mediumNoChIsoPassPSV_n++;
                sorted_photons_mediumNoChIsoPassPSV.push_back( sort_pair );
            }
            if( ph_hasPixSeed->at(idx)==1 ) {
                ph_mediumNoChIsoFailPSV_n++;
                sorted_photons_mediumNoChIsoFailPSV.push_back( sort_pair );
            }
            if( ph_eleVeto->at(idx)==0 ) {
                ph_mediumNoChIsoPassCSEV_n++;
                sorted_photons_mediumNoChIsoPassCSEV.push_back( sort_pair );
            }
            if( ph_eleVeto->at(idx)==1 ) {
                ph_mediumNoChIsoFailCSEV_n++;
                sorted_photons_mediumNoChIsoFailCSEV.push_back( sort_pair );
            }
        }
        if( ph_passHOverEMedium->at(idx) && ph_passSIEIEMedium->at(idx)  && ph_passChIsoCorrMedium->at(idx) && ph_passPhoIsoCorrMedium->at(idx) ) {
            ph_mediumNoNeuIsoNoEleVeto_n++;
            sorted_photons_mediumNoNeuIsoNoEleVeto.push_back( sort_pair );

            if( ph_hasPixSeed->at(idx)==0 ) {
                ph_mediumNoNeuIsoPassPSV_n++;
                sorted_photons_mediumNoNeuIsoPassPSV.push_back( sort_pair );
            }
            if( ph_hasPixSeed->at(idx)==1 ) {
                ph_mediumNoNeuIsoFailPSV_n++;
                sorted_photons_mediumNoNeuIsoFailPSV.push_back( sort_pair );
            }
            if( ph_eleVeto->at(idx)==0 ) {
                ph_mediumNoNeuIsoPassCSEV_n++;
                sorted_photons_mediumNoNeuIsoPassCSEV.push_back( sort_pair );
            }
            if( ph_eleVeto->at(idx)==1 ) {
                ph_mediumNoNeuIsoFailCSEV_n++;
                sorted_photons_mediumNoNeuIsoFailCSEV.push_back( sort_pair );
            }
        }
        if( ph_passHOverEMedium->at(idx) && ph_passSIEIEMedium->at(idx)  && ph_passChIsoCorrMedium->at(idx) && ph_passNeuIsoCorrMedium->at(idx) ) {
            ph_mediumNoPhoIsoNoEleVeto_n++;
            sorted_photons_mediumNoPhoIsoNoEleVeto.push_back( sort_pair );

            if( ph_hasPixSeed->at(idx)==0 ) {
                ph_mediumNoPhoIsoPassPSV_n++;
                sorted_photons_mediumNoPhoIsoPassPSV.push_back( sort_pair );
            }
            if( ph_hasPixSeed->at(idx)==1 ) {
                ph_mediumNoPhoIsoFailPSV_n++;
                sorted_photons_mediumNoPhoIsoFailPSV.push_back( sort_pair );
            }
            if( ph_eleVeto->at(idx)==0 ) {
                ph_mediumNoPhoIsoPassCSEV_n++;
                sorted_photons_mediumNoPhoIsoPassCSEV.push_back( sort_pair );
            }
            if( ph_eleVeto->at(idx)==1 ) {
                ph_mediumNoPhoIsoFailCSEV_n++;
                sorted_photons_mediumNoPhoIsoFailCSEV.push_back( sort_pair );
            }
        }
    }

    std::sort(sorted_photons_iso533.rbegin()                  , sorted_photons_iso533.rend());
    std::sort(sorted_photons_iso855.rbegin()                  , sorted_photons_iso855.rend());
    std::sort(sorted_photons_iso1077.rbegin()                 , sorted_photons_iso1077.rend());
    std::sort(sorted_photons_iso1299.rbegin()                 , sorted_photons_iso1299.rend());
    std::sort(sorted_photons_iso151111.rbegin()               , sorted_photons_iso151111.rend());
    std::sort(sorted_photons_iso201616.rbegin()               , sorted_photons_iso201616.rend());
    std::sort(sorted_photons_passSIEIEiso53None.rbegin()      , sorted_photons_passSIEIEiso53None.rend());
    std::sort(sorted_photons_passSIEIEiso85None.rbegin()      , sorted_photons_passSIEIEiso85None.rend());
    std::sort(sorted_photons_passSIEIEiso107None.rbegin()     , sorted_photons_passSIEIEiso107None.rend());
    std::sort(sorted_photons_passSIEIEiso129None.rbegin()     , sorted_photons_passSIEIEiso129None.rend());
    std::sort(sorted_photons_passSIEIEiso1511None.rbegin()    , sorted_photons_passSIEIEiso1511None.rend());
    std::sort(sorted_photons_passSIEIEiso2016None.rbegin()    , sorted_photons_passSIEIEiso2016None.rend());
    std::sort(sorted_photons_passSIEIEiso5None3.rbegin()       , sorted_photons_passSIEIEiso5None3.rend());
    std::sort(sorted_photons_passSIEIEiso8None5.rbegin()       , sorted_photons_passSIEIEiso8None5.rend());
    std::sort(sorted_photons_passSIEIEiso10None7.rbegin()      , sorted_photons_passSIEIEiso10None7.rend());
    std::sort(sorted_photons_passSIEIEiso12None9.rbegin()      , sorted_photons_passSIEIEiso12None9.rend());
    std::sort(sorted_photons_passSIEIEiso15None11.rbegin()    , sorted_photons_passSIEIEiso15None11.rend());
    std::sort(sorted_photons_passSIEIEiso20None16.rbegin()    , sorted_photons_passSIEIEiso20None16.rend());
    std::sort(sorted_photons_passSIEIEisoNone33.rbegin()      , sorted_photons_passSIEIEisoNone33.rend());
    std::sort(sorted_photons_passSIEIEisoNone55.rbegin()      , sorted_photons_passSIEIEisoNone55.rend());
    std::sort(sorted_photons_passSIEIEisoNone77.rbegin()      , sorted_photons_passSIEIEisoNone77.rend());
    std::sort(sorted_photons_passSIEIEisoNone99.rbegin()      , sorted_photons_passSIEIEisoNone99.rend());
    std::sort(sorted_photons_passSIEIEisoNone1111.rbegin()    , sorted_photons_passSIEIEisoNone1111.rend());
    std::sort(sorted_photons_passSIEIEisoNone1616.rbegin()    , sorted_photons_passSIEIEisoNone1616.rend());
    std::sort(sorted_photons_failSIEIEiso53None.rbegin()      , sorted_photons_failSIEIEiso53None.rend());
    std::sort(sorted_photons_failSIEIEiso85None.rbegin()      , sorted_photons_failSIEIEiso85None.rend());
    std::sort(sorted_photons_failSIEIEiso107None.rbegin()     , sorted_photons_failSIEIEiso107None.rend());
    std::sort(sorted_photons_failSIEIEiso129None.rbegin()     , sorted_photons_failSIEIEiso129None.rend());
    std::sort(sorted_photons_failSIEIEiso1511None.rbegin()    , sorted_photons_failSIEIEiso1511None.rend());
    std::sort(sorted_photons_failSIEIEiso2016None.rbegin()    , sorted_photons_failSIEIEiso2016None.rend());
    std::sort(sorted_photons_failSIEIEiso5None3.rbegin()       , sorted_photons_failSIEIEiso5None3.rend());
    std::sort(sorted_photons_failSIEIEiso8None5.rbegin()       , sorted_photons_failSIEIEiso8None5.rend());
    std::sort(sorted_photons_failSIEIEiso10None7.rbegin()      , sorted_photons_failSIEIEiso10None7.rend());
    std::sort(sorted_photons_failSIEIEiso12None9.rbegin()      , sorted_photons_failSIEIEiso12None9.rend());
    std::sort(sorted_photons_failSIEIEiso15None11.rbegin()    , sorted_photons_failSIEIEiso15None11.rend());
    std::sort(sorted_photons_failSIEIEiso20None16.rbegin()    , sorted_photons_failSIEIEiso20None16.rend());
    std::sort(sorted_photons_failSIEIEisoNone33.rbegin()      , sorted_photons_failSIEIEisoNone33.rend());
    std::sort(sorted_photons_failSIEIEisoNone55.rbegin()      , sorted_photons_failSIEIEisoNone55.rend());
    std::sort(sorted_photons_failSIEIEisoNone77.rbegin()      , sorted_photons_failSIEIEisoNone77.rend());
    std::sort(sorted_photons_failSIEIEisoNone99.rbegin()      , sorted_photons_failSIEIEisoNone99.rend());
    std::sort(sorted_photons_failSIEIEisoNone1111.rbegin()    , sorted_photons_failSIEIEisoNone1111.rend());
    std::sort(sorted_photons_failSIEIEisoNone1616.rbegin()    , sorted_photons_failSIEIEisoNone1616.rend());
    std::sort(sorted_photons_mediumNoNeuIsoNoPhoIso.rbegin()  , sorted_photons_mediumNoNeuIsoNoPhoIso.rend());
    std::sort(sorted_photons_mediumNoChIsoNoPhoIso.rbegin()   , sorted_photons_mediumNoChIsoNoPhoIso.rend());
    std::sort(sorted_photons_mediumNoChIsoNoNeuIso.rbegin()   , sorted_photons_mediumNoChIsoNoNeuIso.rend());
    std::sort(sorted_photons_mediumNoSIEIENoPhoIsoNoEleVeto.rbegin()   , sorted_photons_mediumNoSIEIENoPhoIsoNoEleVeto.rend());
    std::sort(sorted_photons_mediumNoSIEIENoNeuIsoNoEleVeto.rbegin()   , sorted_photons_mediumNoSIEIENoNeuIsoNoEleVeto.rend());
    std::sort(sorted_photons_mediumNoSIEIENoChIsoNoEleVeto.rbegin()    , sorted_photons_mediumNoSIEIENoChIsoNoEleVeto.rend());
    std::sort(sorted_photons_mediumNoSIEIENoPhoIsoPassPSV.rbegin()   , sorted_photons_mediumNoSIEIENoPhoIsoPassPSV.rend());
    std::sort(sorted_photons_mediumNoSIEIENoNeuIsoPassPSV.rbegin()   , sorted_photons_mediumNoSIEIENoNeuIsoPassPSV.rend());
    std::sort(sorted_photons_mediumNoSIEIENoChIsoPassPSV.rbegin()    , sorted_photons_mediumNoSIEIENoChIsoPassPSV.rend());
    std::sort(sorted_photons_mediumNoSIEIENoPhoIsoFailPSV.rbegin()   , sorted_photons_mediumNoSIEIENoPhoIsoFailPSV.rend());
    std::sort(sorted_photons_mediumNoSIEIENoNeuIsoFailPSV.rbegin()   , sorted_photons_mediumNoSIEIENoNeuIsoFailPSV.rend());
    std::sort(sorted_photons_mediumNoSIEIENoChIsoFailPSV.rbegin()    , sorted_photons_mediumNoSIEIENoChIsoFailPSV.rend());
    std::sort(sorted_photons_mediumNoSIEIENoPhoIsoPassCSEV.rbegin()   , sorted_photons_mediumNoSIEIENoPhoIsoPassCSEV.rend());
    std::sort(sorted_photons_mediumNoSIEIENoNeuIsoPassCSEV.rbegin()   , sorted_photons_mediumNoSIEIENoNeuIsoPassCSEV.rend());
    std::sort(sorted_photons_mediumNoSIEIENoChIsoPassCSEV.rbegin()    , sorted_photons_mediumNoSIEIENoChIsoPassCSEV.rend());
    std::sort(sorted_photons_mediumNoSIEIENoPhoIsoFailCSEV.rbegin()   , sorted_photons_mediumNoSIEIENoPhoIsoFailCSEV.rend());
    std::sort(sorted_photons_mediumNoSIEIENoNeuIsoFailCSEV.rbegin()   , sorted_photons_mediumNoSIEIENoNeuIsoFailCSEV.rend());
    std::sort(sorted_photons_mediumNoSIEIENoChIsoFailCSEV.rbegin()    , sorted_photons_mediumNoSIEIENoChIsoFailCSEV.rend());
    std::sort(sorted_photons_mediumNoSIEIENoEleVeto.rbegin()  , sorted_photons_mediumNoSIEIENoEleVeto.rend());
    std::sort(sorted_photons_mediumNoSIEIEPassPSV.rbegin()    , sorted_photons_mediumNoSIEIEPassPSV.rend());
    std::sort(sorted_photons_mediumNoSIEIEFailPSV.rbegin()    , sorted_photons_mediumNoSIEIEFailPSV.rend());
    std::sort(sorted_photons_mediumNoSIEIEPassCSEV.rbegin()   , sorted_photons_mediumNoSIEIEPassCSEV.rend());
    std::sort(sorted_photons_mediumNoSIEIEFailCSEV.rbegin()   , sorted_photons_mediumNoSIEIEFailCSEV.rend());
    std::sort(sorted_photons_mediumNoEleVeto.rbegin()         , sorted_photons_mediumNoEleVeto.rend());
    std::sort(sorted_photons_mediumPassPSV.rbegin()           , sorted_photons_mediumPassPSV.rend());
    std::sort(sorted_photons_mediumFailPSV.rbegin()           , sorted_photons_mediumFailPSV.rend());
    std::sort(sorted_photons_mediumPassCSEV.rbegin()          , sorted_photons_mediumPassCSEV.rend());
    std::sort(sorted_photons_mediumFailCSEV.rbegin()          , sorted_photons_mediumFailCSEV.rend());
    std::sort(sorted_photons_mediumNoChIsoNoEleVeto.rbegin()  , sorted_photons_mediumNoChIsoNoEleVeto.rend());
    std::sort(sorted_photons_mediumNoChIsoPassPSV.rbegin()    , sorted_photons_mediumNoChIsoPassPSV.rend());
    std::sort(sorted_photons_mediumNoChIsoFailPSV.rbegin()    , sorted_photons_mediumNoChIsoFailPSV.rend());
    std::sort(sorted_photons_mediumNoChIsoPassCSEV.rbegin()   , sorted_photons_mediumNoChIsoPassCSEV.rend());
    std::sort(sorted_photons_mediumNoChIsoFailCSEV.rbegin()   , sorted_photons_mediumNoChIsoFailCSEV.rend());
    std::sort(sorted_photons_mediumNoNeuIsoNoEleVeto.rbegin() , sorted_photons_mediumNoNeuIsoNoEleVeto.rend());
    std::sort(sorted_photons_mediumNoNeuIsoPassPSV.rbegin()   , sorted_photons_mediumNoNeuIsoPassPSV.rend());
    std::sort(sorted_photons_mediumNoNeuIsoFailPSV.rbegin()   , sorted_photons_mediumNoNeuIsoFailPSV.rend());
    std::sort(sorted_photons_mediumNoNeuIsoPassCSEV.rbegin()  , sorted_photons_mediumNoNeuIsoPassCSEV.rend());
    std::sort(sorted_photons_mediumNoNeuIsoFailCSEV.rbegin()  , sorted_photons_mediumNoNeuIsoFailCSEV.rend());
    std::sort(sorted_photons_mediumNoPhoIsoNoEleVeto.rbegin() , sorted_photons_mediumNoPhoIsoNoEleVeto.rend());
    std::sort(sorted_photons_mediumNoPhoIsoPassPSV.rbegin()   , sorted_photons_mediumNoPhoIsoPassPSV.rend());
    std::sort(sorted_photons_mediumNoPhoIsoFailPSV.rbegin()   , sorted_photons_mediumNoPhoIsoFailPSV.rend());
    std::sort(sorted_photons_mediumNoPhoIsoPassCSEV.rbegin()  , sorted_photons_mediumNoPhoIsoPassCSEV.rend());
    std::sort(sorted_photons_mediumNoPhoIsoFailCSEV.rbegin()  , sorted_photons_mediumNoPhoIsoFailCSEV.rend());


    for( std::vector<std::pair<float, int> >::const_iterator itr = sorted_photons_iso533.begin() ; itr != sorted_photons_iso533.end(); ++itr ) {
        vector_results["ptSorted_ph_noSIEIEiso533_idx"].push_back( itr->second );
    }
    for( std::vector<std::pair<float, int> >::const_iterator itr = sorted_photons_iso855.begin() ; itr != sorted_photons_iso855.end(); ++itr ) {
        vector_results["ptSorted_ph_noSIEIEiso855_idx"].push_back( itr->second );
    }
    for( std::vector<std::pair<float, int> >::const_iterator itr = sorted_photons_iso1077.begin() ; itr != sorted_photons_iso1077.end(); ++itr ) {
        vector_results["ptSorted_ph_noSIEIEiso1077_idx"].push_back( itr->second );
    }
    for( std::vector<std::pair<float, int> >::const_iterator itr = sorted_photons_iso1299.begin() ; itr != sorted_photons_iso1299.end(); ++itr ) {
        vector_results["ptSorted_ph_noSIEIEiso1299_idx"].push_back( itr->second );
    }
    for( std::vector<std::pair<float, int> >::const_iterator itr = sorted_photons_iso151111.begin() ; itr != sorted_photons_iso151111.end(); ++itr ) {
        vector_results["ptSorted_ph_noSIEIEiso151111_idx"].push_back( itr->second );
    }
    for( std::vector<std::pair<float, int> >::const_iterator itr = sorted_photons_iso201616.begin() ; itr != sorted_photons_iso201616.end(); ++itr ) {
        vector_results["ptSorted_ph_noSIEIEiso201616_idx"].push_back( itr->second );
    }
    for( std::vector<std::pair<float, int> >::const_iterator itr = sorted_photons_passSIEIEiso53None.begin() ; itr != sorted_photons_passSIEIEiso53None.end(); ++itr ) {
        vector_results["ptSorted_ph_passSIEIEiso53None_idx"].push_back( itr->second );
    }
    for( std::vector<std::pair<float, int> >::const_iterator itr = sorted_photons_passSIEIEiso85None.begin() ; itr != sorted_photons_passSIEIEiso85None.end(); ++itr ) {
        vector_results["ptSorted_ph_passSIEIEiso85None_idx"].push_back( itr->second );
    }
    for( std::vector<std::pair<float, int> >::const_iterator itr = sorted_photons_passSIEIEiso107None.begin() ; itr != sorted_photons_passSIEIEiso107None.end(); ++itr ) {
        vector_results["ptSorted_ph_passSIEIEiso107None_idx"].push_back( itr->second );
    }
    for( std::vector<std::pair<float, int> >::const_iterator itr = sorted_photons_passSIEIEiso129None.begin() ; itr != sorted_photons_passSIEIEiso129None.end(); ++itr ) {
        vector_results["ptSorted_ph_passSIEIEiso129None_idx"].push_back( itr->second );
    }
    for( std::vector<std::pair<float, int> >::const_iterator itr = sorted_photons_passSIEIEiso1511None.begin() ; itr != sorted_photons_passSIEIEiso1511None.end(); ++itr ) {
        vector_results["ptSorted_ph_passSIEIEiso1511None_idx"].push_back( itr->second );
    }
    for( std::vector<std::pair<float, int> >::const_iterator itr = sorted_photons_passSIEIEiso2016None.begin() ; itr != sorted_photons_passSIEIEiso2016None.end(); ++itr ) {
        vector_results["ptSorted_ph_passSIEIEiso2016None_idx"].push_back( itr->second );
    }
    for( std::vector<std::pair<float, int> >::const_iterator itr = sorted_photons_passSIEIEiso5None3.begin() ; itr != sorted_photons_passSIEIEiso5None3.end(); ++itr ) {
        vector_results["ptSorted_ph_passSIEIEiso5None3_idx"].push_back( itr->second );
    }
    for( std::vector<std::pair<float, int> >::const_iterator itr = sorted_photons_passSIEIEiso8None5.begin() ; itr != sorted_photons_passSIEIEiso8None5.end(); ++itr ) {
        vector_results["ptSorted_ph_passSIEIEiso8None5_idx"].push_back( itr->second );
    }
    for( std::vector<std::pair<float, int> >::const_iterator itr = sorted_photons_passSIEIEiso10None7.begin() ; itr != sorted_photons_passSIEIEiso10None7.end(); ++itr ) {
        vector_results["ptSorted_ph_passSIEIEiso10None7_idx"].push_back( itr->second );
    }
    for( std::vector<std::pair<float, int> >::const_iterator itr = sorted_photons_passSIEIEiso12None9.begin() ; itr != sorted_photons_passSIEIEiso12None9.end(); ++itr ) {
        vector_results["ptSorted_ph_passSIEIEiso12None9_idx"].push_back( itr->second );
    }
    for( std::vector<std::pair<float, int> >::const_iterator itr = sorted_photons_passSIEIEiso15None11.begin() ; itr != sorted_photons_passSIEIEiso15None11.end(); ++itr ) {
        vector_results["ptSorted_ph_passSIEIEiso15None11_idx"].push_back( itr->second );
    }
    for( std::vector<std::pair<float, int> >::const_iterator itr = sorted_photons_passSIEIEiso20None16.begin() ; itr != sorted_photons_passSIEIEiso20None16.end(); ++itr ) {
        vector_results["ptSorted_ph_passSIEIEiso20None16_idx"].push_back( itr->second );
    }
    for( std::vector<std::pair<float, int> >::const_iterator itr = sorted_photons_passSIEIEisoNone33.begin() ; itr != sorted_photons_passSIEIEisoNone33.end(); ++itr ) {
        vector_results["ptSorted_ph_passSIEIEisoNone33_idx"].push_back( itr->second );
    }
    for( std::vector<std::pair<float, int> >::const_iterator itr = sorted_photons_passSIEIEisoNone55.begin() ; itr != sorted_photons_passSIEIEisoNone55.end(); ++itr ) {
        vector_results["ptSorted_ph_passSIEIEisoNone55_idx"].push_back( itr->second );
    }
    for( std::vector<std::pair<float, int> >::const_iterator itr = sorted_photons_passSIEIEisoNone77.begin() ; itr != sorted_photons_passSIEIEisoNone77.end(); ++itr ) {
        vector_results["ptSorted_ph_passSIEIEisoNone77_idx"].push_back( itr->second );
    }
    for( std::vector<std::pair<float, int> >::const_iterator itr = sorted_photons_passSIEIEisoNone99.begin() ; itr != sorted_photons_passSIEIEisoNone99.end(); ++itr ) {
        vector_results["ptSorted_ph_passSIEIEisoNone99_idx"].push_back( itr->second );
    }
    for( std::vector<std::pair<float, int> >::const_iterator itr = sorted_photons_passSIEIEisoNone1111.begin() ; itr != sorted_photons_passSIEIEisoNone1111.end(); ++itr ) {
        vector_results["ptSorted_ph_passSIEIEisoNone1111_idx"].push_back( itr->second );
    }
    for( std::vector<std::pair<float, int> >::const_iterator itr = sorted_photons_passSIEIEisoNone1616.begin() ; itr != sorted_photons_passSIEIEisoNone1616.end(); ++itr ) {
        vector_results["ptSorted_ph_passSIEIEisoNone1616_idx"].push_back( itr->second );
    }
    for( std::vector<std::pair<float, int> >::const_iterator itr = sorted_photons_failSIEIEiso53None.begin() ; itr != sorted_photons_failSIEIEiso53None.end(); ++itr ) {
        vector_results["ptSorted_ph_failSIEIEiso53None_idx"].push_back( itr->second );
    }
    for( std::vector<std::pair<float, int> >::const_iterator itr = sorted_photons_failSIEIEiso85None.begin() ; itr != sorted_photons_failSIEIEiso85None.end(); ++itr ) {
        vector_results["ptSorted_ph_failSIEIEiso85None_idx"].push_back( itr->second );
    }
    for( std::vector<std::pair<float, int> >::const_iterator itr = sorted_photons_failSIEIEiso107None.begin() ; itr != sorted_photons_failSIEIEiso107None.end(); ++itr ) {
        vector_results["ptSorted_ph_failSIEIEiso107None_idx"].push_back( itr->second );
    }
    for( std::vector<std::pair<float, int> >::const_iterator itr = sorted_photons_failSIEIEiso129None.begin() ; itr != sorted_photons_failSIEIEiso129None.end(); ++itr ) {
        vector_results["ptSorted_ph_failSIEIEiso129None_idx"].push_back( itr->second );
    }
    for( std::vector<std::pair<float, int> >::const_iterator itr = sorted_photons_failSIEIEiso1511None.begin() ; itr != sorted_photons_failSIEIEiso1511None.end(); ++itr ) {
        vector_results["ptSorted_ph_failSIEIEiso1511None_idx"].push_back( itr->second );
    }
    for( std::vector<std::pair<float, int> >::const_iterator itr = sorted_photons_failSIEIEiso2016None.begin() ; itr != sorted_photons_failSIEIEiso2016None.end(); ++itr ) {
        vector_results["ptSorted_ph_failSIEIEiso2016None_idx"].push_back( itr->second );
    }
    for( std::vector<std::pair<float, int> >::const_iterator itr = sorted_photons_failSIEIEiso5None3.begin() ; itr != sorted_photons_failSIEIEiso5None3.end(); ++itr ) {
        vector_results["ptSorted_ph_failSIEIEiso5None3_idx"].push_back( itr->second );
    }
    for( std::vector<std::pair<float, int> >::const_iterator itr = sorted_photons_failSIEIEiso8None5.begin() ; itr != sorted_photons_failSIEIEiso8None5.end(); ++itr ) {
        vector_results["ptSorted_ph_failSIEIEiso8None5_idx"].push_back( itr->second );
    }
    for( std::vector<std::pair<float, int> >::const_iterator itr = sorted_photons_failSIEIEiso10None7.begin() ; itr != sorted_photons_failSIEIEiso10None7.end(); ++itr ) {
        vector_results["ptSorted_ph_failSIEIEiso10None7_idx"].push_back( itr->second );
    }
    for( std::vector<std::pair<float, int> >::const_iterator itr = sorted_photons_failSIEIEiso12None9.begin() ; itr != sorted_photons_failSIEIEiso12None9.end(); ++itr ) {
        vector_results["ptSorted_ph_failSIEIEiso12None9_idx"].push_back( itr->second );
    }
    for( std::vector<std::pair<float, int> >::const_iterator itr = sorted_photons_failSIEIEiso15None11.begin() ; itr != sorted_photons_failSIEIEiso15None11.end(); ++itr ) {
        vector_results["ptSorted_ph_failSIEIEiso15None11_idx"].push_back( itr->second );
    }
    for( std::vector<std::pair<float, int> >::const_iterator itr = sorted_photons_failSIEIEiso20None16.begin() ; itr != sorted_photons_failSIEIEiso20None16.end(); ++itr ) {
        vector_results["ptSorted_ph_failSIEIEiso20None16_idx"].push_back( itr->second );
    }
    for( std::vector<std::pair<float, int> >::const_iterator itr = sorted_photons_failSIEIEisoNone33.begin() ; itr != sorted_photons_failSIEIEisoNone33.end(); ++itr ) {
        vector_results["ptSorted_ph_failSIEIEisoNone33_idx"].push_back( itr->second );
    }
    for( std::vector<std::pair<float, int> >::const_iterator itr = sorted_photons_failSIEIEisoNone55.begin() ; itr != sorted_photons_failSIEIEisoNone55.end(); ++itr ) {
        vector_results["ptSorted_ph_failSIEIEisoNone55_idx"].push_back( itr->second );
    }
    for( std::vector<std::pair<float, int> >::const_iterator itr = sorted_photons_failSIEIEisoNone77.begin() ; itr != sorted_photons_failSIEIEisoNone77.end(); ++itr ) {
        vector_results["ptSorted_ph_failSIEIEisoNone77_idx"].push_back( itr->second );
    }
    for( std::vector<std::pair<float, int> >::const_iterator itr = sorted_photons_failSIEIEisoNone99.begin() ; itr != sorted_photons_failSIEIEisoNone99.end(); ++itr ) {
        vector_results["ptSorted_ph_failSIEIEisoNone99_idx"].push_back( itr->second );
    }
    for( std::vector<std::pair<float, int> >::const_iterator itr = sorted_photons_failSIEIEisoNone1111.begin() ; itr != sorted_photons_failSIEIEisoNone1111.end(); ++itr ) {
        vector_results["ptSorted_ph_failSIEIEisoNone1111_idx"].push_back( itr->second );
    }
    for( std::vector<std::pair<float, int> >::const_iterator itr = sorted_photons_failSIEIEisoNone1616.begin() ; itr != sorted_photons_failSIEIEisoNone1616.end(); ++itr ) {
        vector_results["ptSorted_ph_failSIEIEisoNone1616_idx"].push_back( itr->second );
    }
    for( std::vector<std::pair<float, int> >::const_iterator itr = sorted_photons_mediumNoNeuIsoNoPhoIso.begin() ; itr != sorted_photons_mediumNoNeuIsoNoPhoIso.end(); ++itr ) {
        vector_results["ptSorted_ph_mediumNoNeuIsoNoPhoIso_idx"].push_back( itr->second );
    }
    for( std::vector<std::pair<float, int> >::const_iterator itr = sorted_photons_mediumNoChIsoNoPhoIso.begin() ; itr != sorted_photons_mediumNoChIsoNoPhoIso.end(); ++itr ) {
        vector_results["ptSorted_ph_mediumNoChIsoNoPhoIso_idx"].push_back( itr->second );
    }
    for( std::vector<std::pair<float, int> >::const_iterator itr = sorted_photons_mediumNoChIsoNoNeuIso.begin() ; itr != sorted_photons_mediumNoChIsoNoNeuIso.end(); ++itr ) {
        vector_results["ptSorted_ph_mediumNoChIsoNoNeuIso_idx"].push_back( itr->second );
    }
    for( std::vector<std::pair<float, int> >::const_iterator itr = sorted_photons_mediumNoSIEIENoPhoIsoNoEleVeto.begin() ; itr != sorted_photons_mediumNoSIEIENoPhoIsoNoEleVeto.end(); ++itr ) {
        vector_results["ptSorted_ph_mediumNoSIEIENoPhoIsoNoEleVeto_idx"].push_back( itr->second );
    }
    for( std::vector<std::pair<float, int> >::const_iterator itr = sorted_photons_mediumNoSIEIENoNeuIsoNoEleVeto.begin() ; itr != sorted_photons_mediumNoSIEIENoNeuIsoNoEleVeto.end(); ++itr ) {
        vector_results["ptSorted_ph_mediumNoSIEIENoNeuIsoNoEleVeto_idx"].push_back( itr->second );
    }
    for( std::vector<std::pair<float, int> >::const_iterator itr = sorted_photons_mediumNoSIEIENoChIsoNoEleVeto.begin() ; itr != sorted_photons_mediumNoSIEIENoChIsoNoEleVeto.end(); ++itr ) {
        vector_results["ptSorted_ph_mediumNoSIEIENoChIsoNoEleVeto_idx"].push_back( itr->second );
        // for backwards compatibility
        vector_results["ptSorted_ph_mediumNoSIEIENoChIso_idx"].push_back( itr->second );
    }
    for( std::vector<std::pair<float, int> >::const_iterator itr = sorted_photons_mediumNoSIEIENoPhoIsoPassPSV.begin() ; itr != sorted_photons_mediumNoSIEIENoPhoIsoPassPSV.end(); ++itr ) {
        vector_results["ptSorted_ph_mediumNoSIEIENoPhoIsoPassPSV_idx"].push_back( itr->second );
    }
    for( std::vector<std::pair<float, int> >::const_iterator itr = sorted_photons_mediumNoSIEIENoNeuIsoPassPSV.begin() ; itr != sorted_photons_mediumNoSIEIENoNeuIsoPassPSV.end(); ++itr ) {
        vector_results["ptSorted_ph_mediumNoSIEIENoNeuIsoPassPSV_idx"].push_back( itr->second );
    }
    for( std::vector<std::pair<float, int> >::const_iterator itr = sorted_photons_mediumNoSIEIENoChIsoPassPSV.begin() ; itr != sorted_photons_mediumNoSIEIENoChIsoPassPSV.end(); ++itr ) {
        vector_results["ptSorted_ph_mediumNoSIEIENoChIsoPassPSV_idx"].push_back( itr->second );
    }
    for( std::vector<std::pair<float, int> >::const_iterator itr = sorted_photons_mediumNoSIEIENoPhoIsoFailPSV.begin() ; itr != sorted_photons_mediumNoSIEIENoPhoIsoFailPSV.end(); ++itr ) {
        vector_results["ptSorted_ph_mediumNoSIEIENoPhoIsoFailPSV_idx"].push_back( itr->second );
    }
    for( std::vector<std::pair<float, int> >::const_iterator itr = sorted_photons_mediumNoSIEIENoNeuIsoFailPSV.begin() ; itr != sorted_photons_mediumNoSIEIENoNeuIsoFailPSV.end(); ++itr ) {
        vector_results["ptSorted_ph_mediumNoSIEIENoNeuIsoFailPSV_idx"].push_back( itr->second );
    }
    for( std::vector<std::pair<float, int> >::const_iterator itr = sorted_photons_mediumNoSIEIENoChIsoFailPSV.begin() ; itr != sorted_photons_mediumNoSIEIENoChIsoFailPSV.end(); ++itr ) {
        vector_results["ptSorted_ph_mediumNoSIEIENoChIsoFailPSV_idx"].push_back( itr->second );
    }
    for( std::vector<std::pair<float, int> >::const_iterator itr = sorted_photons_mediumNoSIEIENoPhoIsoPassCSEV.begin() ; itr != sorted_photons_mediumNoSIEIENoPhoIsoPassCSEV.end(); ++itr ) {
        vector_results["ptSorted_ph_mediumNoSIEIENoPhoIsoPassCSEV_idx"].push_back( itr->second );
    }
    for( std::vector<std::pair<float, int> >::const_iterator itr = sorted_photons_mediumNoSIEIENoNeuIsoPassCSEV.begin() ; itr != sorted_photons_mediumNoSIEIENoNeuIsoPassCSEV.end(); ++itr ) {
        vector_results["ptSorted_ph_mediumNoSIEIENoNeuIsoPassCSEV_idx"].push_back( itr->second );
    }
    for( std::vector<std::pair<float, int> >::const_iterator itr = sorted_photons_mediumNoSIEIENoChIsoPassCSEV.begin() ; itr != sorted_photons_mediumNoSIEIENoChIsoPassCSEV.end(); ++itr ) {
        vector_results["ptSorted_ph_mediumNoSIEIENoChIsoPassCSEV_idx"].push_back( itr->second );
    }
    for( std::vector<std::pair<float, int> >::const_iterator itr = sorted_photons_mediumNoSIEIENoPhoIsoFailCSEV.begin() ; itr != sorted_photons_mediumNoSIEIENoPhoIsoFailCSEV.end(); ++itr ) {
        vector_results["ptSorted_ph_mediumNoSIEIENoPhoIsoFailCSEV_idx"].push_back( itr->second );
    }
    for( std::vector<std::pair<float, int> >::const_iterator itr = sorted_photons_mediumNoSIEIENoNeuIsoFailCSEV.begin() ; itr != sorted_photons_mediumNoSIEIENoNeuIsoFailCSEV.end(); ++itr ) {
        vector_results["ptSorted_ph_mediumNoSIEIENoNeuIsoFailCSEV_idx"].push_back( itr->second );
    }
    for( std::vector<std::pair<float, int> >::const_iterator itr = sorted_photons_mediumNoSIEIENoChIsoFailCSEV.begin() ; itr != sorted_photons_mediumNoSIEIENoChIsoFailCSEV.end(); ++itr ) {
        vector_results["ptSorted_ph_mediumNoSIEIENoChIsoFailCSEV_idx"].push_back( itr->second );
    }
    for( std::vector<std::pair<float, int> >::const_iterator itr = sorted_photons_mediumNoSIEIENoEleVeto.begin() ; itr != sorted_photons_mediumNoSIEIENoEleVeto.end(); ++itr ) {
        vector_results["ptSorted_ph_mediumNoSIEIENoEleVeto_idx"].push_back( itr->second );
    }
    for( std::vector<std::pair<float, int> >::const_iterator itr = sorted_photons_mediumNoSIEIEPassPSV.begin() ; itr != sorted_photons_mediumNoSIEIEPassPSV.end(); ++itr ) {
        vector_results["ptSorted_ph_mediumNoSIEIEPassPSV_idx"].push_back( itr->second );
    }
    for( std::vector<std::pair<float, int> >::const_iterator itr = sorted_photons_mediumNoSIEIEFailPSV.begin() ; itr != sorted_photons_mediumNoSIEIEFailPSV.end(); ++itr ) {
        vector_results["ptSorted_ph_mediumNoSIEIEFailPSV_idx"].push_back( itr->second );
    }
    for( std::vector<std::pair<float, int> >::const_iterator itr = sorted_photons_mediumNoSIEIEPassCSEV.begin() ; itr != sorted_photons_mediumNoSIEIEPassCSEV.end(); ++itr ) {
        vector_results["ptSorted_ph_mediumNoSIEIEPassCSEV_idx"].push_back( itr->second );
    }
    for( std::vector<std::pair<float, int> >::const_iterator itr = sorted_photons_mediumNoSIEIEFailCSEV.begin() ; itr != sorted_photons_mediumNoSIEIEFailCSEV.end(); ++itr ) {
        vector_results["ptSorted_ph_mediumNoSIEIEFailCSEV_idx"].push_back( itr->second );
    }
    for( std::vector<std::pair<float, int> >::const_iterator itr = sorted_photons_mediumNoEleVeto.begin() ; itr != sorted_photons_mediumNoEleVeto.end(); ++itr ) {
        vector_results["ptSorted_ph_mediumNoEleVeto_idx"].push_back( itr->second );
    }
    for( std::vector<std::pair<float, int> >::const_iterator itr = sorted_photons_mediumPassPSV.begin() ; itr != sorted_photons_mediumPassPSV.end(); ++itr ) {
        vector_results["ptSorted_ph_mediumPassPSV_idx"].push_back( itr->second );
    }
    for( std::vector<std::pair<float, int> >::const_iterator itr = sorted_photons_mediumFailPSV.begin() ; itr != sorted_photons_mediumFailPSV.end(); ++itr ) {
        vector_results["ptSorted_ph_mediumFailPSV_idx"].push_back( itr->second );
    }
    for( std::vector<std::pair<float, int> >::const_iterator itr = sorted_photons_mediumPassCSEV.begin() ; itr != sorted_photons_mediumPassCSEV.end(); ++itr ) {
        vector_results["ptSorted_ph_mediumPassCSEV_idx"].push_back( itr->second );
    }
    for( std::vector<std::pair<float, int> >::const_iterator itr = sorted_photons_mediumFailCSEV.begin() ; itr != sorted_photons_mediumFailCSEV.end(); ++itr ) {
        vector_results["ptSorted_ph_mediumFailCSEV_idx"].push_back( itr->second );
    }
    for( std::vector<std::pair<float, int> >::const_iterator itr = sorted_photons_mediumNoChIsoNoEleVeto.begin() ; itr != sorted_photons_mediumNoChIsoNoEleVeto.end(); ++itr ) {
        vector_results["ptSorted_ph_mediumNoChIsoNoEleVeto_idx"].push_back( itr->second );
    }
    for( std::vector<std::pair<float, int> >::const_iterator itr = sorted_photons_mediumNoChIsoPassPSV.begin() ; itr != sorted_photons_mediumNoChIsoPassPSV.end(); ++itr ) {
        vector_results["ptSorted_ph_mediumNoChIsoPassPSV_idx"].push_back( itr->second );
    }
    for( std::vector<std::pair<float, int> >::const_iterator itr = sorted_photons_mediumNoChIsoFailPSV.begin() ; itr != sorted_photons_mediumNoChIsoFailPSV.end(); ++itr ) {
        vector_results["ptSorted_ph_mediumNoChIsoFailPSV_idx"].push_back( itr->second );
    }
    for( std::vector<std::pair<float, int> >::const_iterator itr = sorted_photons_mediumNoChIsoPassCSEV.begin() ; itr != sorted_photons_mediumNoChIsoPassCSEV.end(); ++itr ) {
        vector_results["ptSorted_ph_mediumNoChIsoPassCSEV_idx"].push_back( itr->second );
    }
    for( std::vector<std::pair<float, int> >::const_iterator itr = sorted_photons_mediumNoChIsoFailCSEV.begin() ; itr != sorted_photons_mediumNoChIsoFailCSEV.end(); ++itr ) {
        vector_results["ptSorted_ph_mediumNoChIsoFailCSEV_idx"].push_back( itr->second );
    }
    for( std::vector<std::pair<float, int> >::const_iterator itr = sorted_photons_mediumNoNeuIsoNoEleVeto.begin() ; itr != sorted_photons_mediumNoNeuIsoNoEleVeto.end(); ++itr ) {
        vector_results["ptSorted_ph_mediumNoNeuIsoNoEleVeto_idx"].push_back( itr->second );
    }
    for( std::vector<std::pair<float, int> >::const_iterator itr = sorted_photons_mediumNoNeuIsoPassPSV.begin() ; itr != sorted_photons_mediumNoNeuIsoPassPSV.end(); ++itr ) {
        vector_results["ptSorted_ph_mediumNoNeuIsoPassPSV_idx"].push_back( itr->second );
    }
    for( std::vector<std::pair<float, int> >::const_iterator itr = sorted_photons_mediumNoNeuIsoFailPSV.begin() ; itr != sorted_photons_mediumNoNeuIsoFailPSV.end(); ++itr ) {
        vector_results["ptSorted_ph_mediumNoNeuIsoFailPSV_idx"].push_back( itr->second );
    }
    for( std::vector<std::pair<float, int> >::const_iterator itr = sorted_photons_mediumNoNeuIsoPassCSEV.begin() ; itr != sorted_photons_mediumNoNeuIsoPassCSEV.end(); ++itr ) {
        vector_results["ptSorted_ph_mediumNoNeuIsoPassCSEV_idx"].push_back( itr->second );
    }
    for( std::vector<std::pair<float, int> >::const_iterator itr = sorted_photons_mediumNoNeuIsoFailCSEV.begin() ; itr != sorted_photons_mediumNoNeuIsoFailCSEV.end(); ++itr ) {
        vector_results["ptSorted_ph_mediumNoNeuIsoFailCSEV_idx"].push_back( itr->second );
    }
    for( std::vector<std::pair<float, int> >::const_iterator itr = sorted_photons_mediumNoPhoIsoNoEleVeto.begin() ; itr != sorted_photons_mediumNoPhoIsoNoEleVeto.end(); ++itr ) {
        vector_results["ptSorted_ph_mediumNoPhoIsoNoEleVeto_idx"].push_back( itr->second );
    }
    for( std::vector<std::pair<float, int> >::const_iterator itr = sorted_photons_mediumNoPhoIsoPassPSV.begin() ; itr != sorted_photons_mediumNoPhoIsoPassPSV.end(); ++itr ) {
        vector_results["ptSorted_ph_mediumNoPhoIsoPassPSV_idx"].push_back( itr->second );
    }
    for( std::vector<std::pair<float, int> >::const_iterator itr = sorted_photons_mediumNoPhoIsoFailPSV.begin() ; itr != sorted_photons_mediumNoPhoIsoFailPSV.end(); ++itr ) {
        vector_results["ptSorted_ph_mediumNoPhoIsoFailPSV_idx"].push_back( itr->second );
    }
    for( std::vector<std::pair<float, int> >::const_iterator itr = sorted_photons_mediumNoPhoIsoPassCSEV.begin() ; itr != sorted_photons_mediumNoPhoIsoPassCSEV.end(); ++itr ) {
        vector_results["ptSorted_ph_mediumNoPhoIsoPassCSEV_idx"].push_back( itr->second );
    }
    for( std::vector<std::pair<float, int> >::const_iterator itr = sorted_photons_mediumNoPhoIsoFailCSEV.begin() ; itr != sorted_photons_mediumNoPhoIsoFailCSEV.end(); ++itr ) {
        vector_results["ptSorted_ph_mediumNoPhoIsoFailCSEV_idx"].push_back( itr->second );
    }


    results["ph_noSIEIEiso533_n"] = ph_noSIEIEiso533_n;
    results["ph_noSIEIEiso855_n"] = ph_noSIEIEiso855_n;
    results["ph_noSIEIEiso1077_n"] = ph_noSIEIEiso1077_n;
    results["ph_noSIEIEiso1299_n"] = ph_noSIEIEiso1299_n;
    results["ph_noSIEIEiso151111_n"] = ph_noSIEIEiso151111_n;
    results["ph_noSIEIEiso201616_n"] = ph_noSIEIEiso201616_n;
    results["ph_passSIEIEiso53None_n"] = ph_passSIEIEiso53None_n;
    results["ph_passSIEIEiso85None_n"] = ph_passSIEIEiso85None_n;
    results["ph_passSIEIEiso107None_n"] = ph_passSIEIEiso107None_n;
    results["ph_passSIEIEiso129None_n"] = ph_passSIEIEiso129None_n;
    results["ph_passSIEIEiso1511None_n"] = ph_passSIEIEiso1511None_n;
    results["ph_passSIEIEiso2016None_n"] = ph_passSIEIEiso2016None_n;
    results["ph_passSIEIEiso5None3_n"] = ph_passSIEIEiso5None3_n;
    results["ph_passSIEIEiso8None5_n"] = ph_passSIEIEiso8None5_n;
    results["ph_passSIEIEiso10None7_n"] = ph_passSIEIEiso10None7_n;
    results["ph_passSIEIEiso12None9_n"] = ph_passSIEIEiso12None9_n;
    results["ph_passSIEIEiso15None11_n"] = ph_passSIEIEiso15None11_n;
    results["ph_passSIEIEiso20None16_n"] = ph_passSIEIEiso20None16_n;
    results["ph_passSIEIEisoNone33_n"] = ph_passSIEIEisoNone33_n;
    results["ph_passSIEIEisoNone55_n"] = ph_passSIEIEisoNone55_n;
    results["ph_passSIEIEisoNone77_n"] = ph_passSIEIEisoNone77_n;
    results["ph_passSIEIEisoNone99_n"] = ph_passSIEIEisoNone99_n;
    results["ph_passSIEIEisoNone1111_n"] = ph_passSIEIEisoNone1111_n;
    results["ph_passSIEIEisoNone1616_n"] = ph_passSIEIEisoNone1616_n;
    results["ph_failSIEIEiso53None_n"] = ph_failSIEIEiso53None_n;
    results["ph_failSIEIEiso85None_n"] = ph_failSIEIEiso85None_n;
    results["ph_failSIEIEiso107None_n"] = ph_failSIEIEiso107None_n;
    results["ph_failSIEIEiso129None_n"] = ph_failSIEIEiso129None_n;
    results["ph_failSIEIEiso1511None_n"] = ph_failSIEIEiso1511None_n;
    results["ph_failSIEIEiso2016None_n"] = ph_failSIEIEiso2016None_n;
    results["ph_failSIEIEiso5None3_n"] = ph_failSIEIEiso5None3_n;
    results["ph_failSIEIEiso8None5_n"] = ph_failSIEIEiso8None5_n;
    results["ph_failSIEIEiso10None7_n"] = ph_failSIEIEiso10None7_n;
    results["ph_failSIEIEiso12None9_n"] = ph_failSIEIEiso12None9_n;
    results["ph_failSIEIEiso15None11_n"] = ph_failSIEIEiso15None11_n;
    results["ph_failSIEIEiso20None16_n"] = ph_failSIEIEiso20None16_n;
    results["ph_failSIEIEisoNone33_n"] = ph_failSIEIEisoNone33_n;
    results["ph_failSIEIEisoNone55_n"] = ph_failSIEIEisoNone55_n;
    results["ph_failSIEIEisoNone77_n"] = ph_failSIEIEisoNone77_n;
    results["ph_failSIEIEisoNone99_n"] = ph_failSIEIEisoNone99_n;
    results["ph_failSIEIEisoNone1111_n"] = ph_failSIEIEisoNone1111_n;
    results["ph_failSIEIEisoNone1616_n"] = ph_failSIEIEisoNone1616_n;
    results["ph_mediumNoNeuIsoNoPhoIso_n"] = ph_mediumNoNeuIsoNoPhoIso_n;
    results["ph_mediumNoChIsoNoPhoIso_n"] = ph_mediumNoChIsoNoPhoIso_n;
    results["ph_mediumNoChIsoNoNeuIso_n"] = ph_mediumNoChIsoNoNeuIso_n;
    results["ph_mediumNoSIEIENoPhoIsoNoEleVeto_n"] = ph_mediumNoSIEIENoPhoIsoNoEleVeto_n;
    results["ph_mediumNoSIEIENoPhoIsoPassPSV_n"] = ph_mediumNoSIEIENoPhoIsoPassPSV_n;
    results["ph_mediumNoSIEIENoPhoIsoFailPSV_n"] = ph_mediumNoSIEIENoPhoIsoFailPSV_n;
    results["ph_mediumNoSIEIENoPhoIsoPassCSEV_n"] = ph_mediumNoSIEIENoPhoIsoPassCSEV_n;
    results["ph_mediumNoSIEIENoPhoIsoFailCSEV_n"] = ph_mediumNoSIEIENoPhoIsoFailCSEV_n;
    results["ph_mediumNoSIEIENoNeuIsoNoEleVeto_n"] = ph_mediumNoSIEIENoNeuIsoNoEleVeto_n;
    results["ph_mediumNoSIEIENoNeuIsoPassPSV_n"] = ph_mediumNoSIEIENoNeuIsoPassPSV_n;
    results["ph_mediumNoSIEIENoNeuIsoFailPSV_n"] = ph_mediumNoSIEIENoNeuIsoFailPSV_n;
    results["ph_mediumNoSIEIENoNeuIsoPassCSEV_n"] = ph_mediumNoSIEIENoNeuIsoPassCSEV_n;
    results["ph_mediumNoSIEIENoNeuIsoFailCSEV_n"] = ph_mediumNoSIEIENoNeuIsoFailCSEV_n;
    results["ph_mediumNoSIEIENoChIsoNoEleVeto_n"] = ph_mediumNoSIEIENoChIsoNoEleVeto_n;
    results["ph_mediumNoSIEIENoChIso_n"] = ph_mediumNoSIEIENoChIso_n;
    results["ph_mediumNoSIEIENoChIsoPassPSV_n"] = ph_mediumNoSIEIENoChIsoPassPSV_n;
    results["ph_mediumNoSIEIENoChIsoFailPSV_n"] = ph_mediumNoSIEIENoChIsoFailPSV_n;
    results["ph_mediumNoSIEIENoChIsoPassCSEV_n"] = ph_mediumNoSIEIENoChIsoPassCSEV_n;
    results["ph_mediumNoSIEIENoChIsoFailCSEV_n"] = ph_mediumNoSIEIENoChIsoFailCSEV_n;
    results["ph_mediumNoSIEIENoEleVeto_n"] = ph_mediumNoSIEIENoEleVeto_n;
    results["ph_mediumNoSIEIEPassPSV_n"] = ph_mediumNoSIEIEPassPSV_n;
    results["ph_mediumNoSIEIEFailPSV_n"] = ph_mediumNoSIEIEFailPSV_n;
    results["ph_mediumNoSIEIEPassCSEV_n"] = ph_mediumNoSIEIEPassCSEV_n;
    results["ph_mediumNoSIEIEFailCSEV_n"] = ph_mediumNoSIEIEFailCSEV_n;
    results["ph_mediumNoEleVeto_n"] = ph_mediumNoEleVeto_n;
    results["ph_mediumPassPSV_n"] = ph_mediumPassPSV_n;
    results["ph_mediumFailPSV_n"] = ph_mediumFailPSV_n;
    results["ph_mediumPassCSEV_n"] = ph_mediumPassCSEV_n;
    results["ph_mediumFailCSEV_n"] = ph_mediumFailCSEV_n;
    results["ph_mediumNoChIsoNoEleVeto_n"] = ph_mediumNoChIsoNoEleVeto_n;
    results["ph_mediumNoChIsoPassPSV_n"] = ph_mediumNoChIsoPassPSV_n;
    results["ph_mediumNoChIsoFailPSV_n"] = ph_mediumNoChIsoFailPSV_n;
    results["ph_mediumNoChIsoPassCSEV_n"] = ph_mediumNoChIsoPassCSEV_n;
    results["ph_mediumNoChIsoFailCSEV_n"] = ph_mediumNoChIsoFailCSEV_n;
    results["ph_mediumNoNeuIsoNoEleVeto_n"] = ph_mediumNoNeuIsoNoEleVeto_n;
    results["ph_mediumNoNeuIsoPassPSV_n"] = ph_mediumNoNeuIsoPassPSV_n;
    results["ph_mediumNoNeuIsoFailPSV_n"] = ph_mediumNoNeuIsoFailPSV_n;
    results["ph_mediumNoNeuIsoPassCSEV_n"] = ph_mediumNoNeuIsoPassCSEV_n;
    results["ph_mediumNoNeuIsoFailCSEV_n"] = ph_mediumNoNeuIsoFailCSEV_n;
    results["ph_mediumNoPhoIsoNoEleVeto_n"] = ph_mediumNoPhoIsoNoEleVeto_n;
    results["ph_mediumNoPhoIsoPassPSV_n"] = ph_mediumNoPhoIsoPassPSV_n;
    results["ph_mediumNoPhoIsoFailPSV_n"] = ph_mediumNoPhoIsoFailPSV_n;
    results["ph_mediumNoPhoIsoPassCSEV_n"] = ph_mediumNoPhoIsoPassCSEV_n;
    results["ph_mediumNoPhoIsoFailCSEV_n"] = ph_mediumNoPhoIsoFailCSEV_n;
}

