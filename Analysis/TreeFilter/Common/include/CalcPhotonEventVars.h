#include <vector>
#include <map>
#include "TLorentzVector.h"
#include "Core/Util.h"

namespace Phot {
void CalcEventVars(const std::vector<TLorentzVector> & photons, 
                                     const std::vector<TLorentzVector> & electrons,
                                     const std::vector<TLorentzVector> & muons,
                                     const TLorentzVector &metlv,
                                     std::map<std::string, float> & results,
                                     std::map<std::string, std::vector<float> > & vector_results
        );
}

void Phot::CalcEventVars(const std::vector<TLorentzVector> & photons, 
                                     const std::vector<TLorentzVector> & electrons,
                                     const std::vector<TLorentzVector> & muons,
                                     const TLorentzVector &metlv,
                                     std::map<std::string, float> & results,
                                     std::map<std::string, std::vector<float> > & vector_results
        ) {

    
    std::vector<std::pair<float, int> > sorted_photons;
    for( unsigned idx = 0; idx < photons.size() ; ++idx ) {
        sorted_photons.push_back( std::make_pair( photons[idx].Pt(), idx ) );
    }

    std::vector<std::pair<float, int> > sorted_leptons;
    std::vector<TLorentzVector> leptons;
    for( unsigned idx = 0; idx < electrons.size() ; ++idx ) {
        leptons.push_back( electrons[idx] );
        sorted_leptons.push_back( std::make_pair( electrons[idx].Pt(), idx ) );
    }
    for( unsigned idx = 0; idx < muons.size() ; ++idx ) {
        sorted_leptons.push_back( std::make_pair( muons[idx].Pt(), idx ) );
        leptons.push_back( muons[idx] );
    }

    // sort the list of photon momenta in descending order
    std::sort(sorted_photons.rbegin(), sorted_photons.rend());
    std::sort(sorted_leptons.rbegin(), sorted_leptons.rend());

    // fill variables for pT sorted photons
   
   
    vector_results["dphi_met_phot"] = std::vector<float>();
    vector_results["m_leadLep_phot"] = std::vector<float>();
    vector_results["m_sublLep_phot"] = std::vector<float>();
    vector_results["dr_leadLep_phot"] = std::vector<float>();
    vector_results["dr_sublLep_phot"] = std::vector<float>();
    vector_results["dphi_leadLep_phot"] = std::vector<float>();
    vector_results["dphi_sublLep_phot"] = std::vector<float>();
    vector_results["m_leplep_phot"] = std::vector<float>();

    vector_results["m_diphot"] = std::vector<float>();
    vector_results["dr_diphot"] = std::vector<float>();
    vector_results["dphi_diphot"] = std::vector<float>();
    vector_results["pt_diphot"] = std::vector<float>();
    vector_results["m_leplep_diphot"] = std::vector<float>();

    // fill photon event variable vectors
    for( unsigned int phidx = 0; phidx < photons.size(); ++phidx ) {
        vector_results["dphi_met_phot"].push_back(photons[phidx].DeltaPhi( metlv ));

        if( leptons.size() > 1 ) {
            vector_results["m_leadLep_phot"]    .push_back( ( photons[phidx] + leptons[0] ).M() );
            vector_results["m_sublLep_phot"]    .push_back( ( photons[phidx] + leptons[1] ).M() );
            vector_results["dr_leadLep_phot"]   .push_back( photons[phidx].DeltaR( leptons[0]) );
            vector_results["dr_sublLep_phot"]   .push_back( photons[phidx].DeltaR( leptons[1]) );
            vector_results["dphi_leadLep_phot"] .push_back( photons[phidx].DeltaPhi( leptons[0]));
            vector_results["dphi_sublLep_phot"] .push_back( photons[phidx].DeltaPhi( leptons[1]));
            vector_results["m_leplep_phot"].push_back( ( photons[phidx] + leptons[0] + leptons[1] ).M() );
        }

    }
    // fill di photon event variable vectors
    if( photons.size() > 1 ) {
        int max_idx = 10*(photons.size()-1);

        vector_results["m_diphot"]             .resize( max_idx,0 );
        vector_results["dr_diphot"]            .resize( max_idx,0 );
        vector_results["dphi_diphot"]          .resize( max_idx,0 );
        vector_results["pt_diphot"]            .resize( max_idx,0 );
        vector_results["m_leplep_diphot"]      .resize( max_idx,0 );

        for( unsigned int idx1=0; idx1 < photons.size(); ++idx1 ) {
            for( unsigned int idx2=idx1+1; idx2 < photons.size(); ++idx2 ) {
                int fill_idx = idx1*10+idx2;

                vector_results["m_diphot"]   [fill_idx] = ( photons[idx1] + photons[idx2]).M();
                vector_results["dr_diphot"]  [fill_idx] = photons[idx1].DeltaR(photons[idx2]);
                vector_results["dphi_diphot"][fill_idx] = photons[idx1].DeltaPhi(photons[idx2]);
                vector_results["pt_diphot"]  [fill_idx] = ( photons[idx1] + photons[idx2]).Pt();

                if( leptons.size() > 1 ) {
                    vector_results["m_leplep_diphot"][fill_idx] = ( photons[idx1] + photons[idx2] + leptons[0] + leptons[1] ).M();
                }
            }
        }
    }
                    

    if( leptons.size() > 0 ) {
        results["mt_lep_met"] = Utils::calc_mt( leptons[0], metlv );
        results["dphi_met_lep1"] = leptons[0].DeltaPhi( metlv );

        if( leptons.size() > 1 ) {
            results["dphi_met_lep2"] = leptons[1].DeltaPhi( metlv );
            results["m_leplep"] = ( leptons[0] + leptons[1] ).M();
        }
    }
    if( muons.size() > 1 ) {
        results["m_mumu"] = ( muons[0] + muons[1] ).M();
    }
    if( electrons.size() > 1 ) {
        results["m_elel"] = ( electrons[0] + electrons[1] ).M();
    }
    if( leptons.size() == 3 ) {
        results["m_3lep"] = ( leptons[0] + leptons[1] + leptons[2] ).M();
    }

    if( leptons.size() == 4 ) {
        results["m_4lep"] = ( leptons[0] + leptons[1] + leptons[2] + leptons[3] ).M();
    }
}

