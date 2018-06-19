
import ROOT
ROOT.PyConfig.IgnoreCommandLineOptions = True
# -----------------------------------------------------
# Setup CMSSW first, CMSSW_5_3_22_patch1 works
# -----------------------------------------------------
#ROOT.gSystem.Load( '/afs/cern.ch/user/j/jkunkle/Programs/MG5_aMC_v2_4_3/ExRootAnalysis/libExRootAnalysis.so')
ROOT.gSystem.Load( '/afs/cern.ch/user/j/jkunkle/Programs/MG5_aMC_v2_4_3/ExRootAnalysis/ExRootClasses_cc.so')
from ROOT import TSortableObject
from ROOT import TRootLHEFEvent
from ROOT import TRootLHEFParticle

import math

from argparse import ArgumentParser

parser = ArgumentParser()

parser.add_argument( '--input', dest='input', default=None, help='Path to input file' )
parser.add_argument( '--output', dest='output', default=None, help='Path to output file' )

options = parser.parse_args()

_m_w = 80.385

def main() :

    ifile = ROOT.TFile.Open( options.input, 'READ' )

    tree = ifile.Get('LHEF')

    ptleadph_hist = ROOT.TH1F( 'ptleadph_hist', 'ptleadph_hist', 500, 0, 1000 )
    ptleadlep_hist = ROOT.TH1F( 'ptleadlep_hist', 'ptleadlep_hist', 500, 0, 1000 )
    ptleadnu_hist = ROOT.TH1F( 'ptleadnu_hist', 'ptleadnu_hist', 500, 0, 1000 )

    mlepnu_hist = ROOT.TH1F( 'mlepnu_hist', 'mlepnu_hist', 500, 0, 1000 )
    mlepnu_hist = ROOT.TH1F( 'mlepnu_hist', 'mlepnu_hist', 500, 0, 1000 )
    mlepnuph_hist = ROOT.TH1F( 'mlepnuph_hist', 'mlepnuph_hist', 500, 0, 1000 )

    #outtree = ROOT.TTree( 'events', 'events' )

    #br_m_lep_nu_ph = array( 'f', [0] )
    #outtree.Branch( 'm_lep_nu_ph', br_m_lep_nu_ph, 'm_lep_nu_ph/F' )

    ph_n                    = ROOT.TH1F( "ph_n"                   , "ph_n"                    , 10 , 0, 10  )
    lep_n                   = ROOT.TH1F( "lep_n"                  , "lep_n"                   , 10 , 0, 10  )
    nu_n                    = ROOT.TH1F( "nu_n"                   , "nu_n"                    , 10 , 0, 10  )
    qk_n                    = ROOT.TH1F( "qk_n"                   , "qk_n"                    , 10 , 0, 10  )
    ph_pt                   = ROOT.TH1F( "ph_pt"                  , "ph_pt"                   , 100, 0, 400 )
    lep_pt                  = ROOT.TH1F( "lep_pt"                 , "lep_pt"                  , 100, 0, 400 )
    nu_pt                   = ROOT.TH1F( "nu_pt"                  , "nu_pt"                   , 100, 0, 400 )
    m_lep_nu                = ROOT.TH1F( "m_lep_nu"               , "m_lep_nu"                , 100, 0, 400 )
    mt_lep_nu               = ROOT.TH1F( "mt_lep_nu"              , "mt_lep_nu"               , 100, 0, 400 )
    mt_lep_nu_ph            = ROOT.TH1F( "mt_lep_nu_ph"           , "mt_lep_nu_ph"            , 1000, 0, 4000 )
    m_lep_nuNoZ             = ROOT.TH1F( "m_lep_nuNoZ"            , "m_lep_nuNoZ"             , 100, 0, 400 )
    m_lep_nuNoZ_success     = ROOT.TH1F( "m_lep_nuNoZ_success"    , "m_lep_nuNoZ_success"     , 100, 0, 400 )
    m_lep_nuNoZ_fail        = ROOT.TH1F( "m_lep_nuNoZ_fail"       , "m_lep_nuNoZ_fail"        , 100, 0, 400 )
    m_lep_nuReco_success    = ROOT.TH1F( "m_lep_nuReco_success"   , "m_lep_nuReco_success"    , 100, 0, 400 )
    m_lep_nuReco_fail       = ROOT.TH1F( "m_lep_nuReco_fail"      , "m_lep_nuReco_fail"       , 100, 0, 400 )
    m_lep_nuReco            = ROOT.TH1F( "m_lep_nuReco"           , "m_lep_nuReco"            , 100, 0, 400 )
    m_lep_nuReco_ph_success = ROOT.TH1F( "m_lep_nuReco_ph_success", "m_lep_nuReco_ph_success" , 1000, 0, 4000 )
    m_lep_nuReco_ph_fail    = ROOT.TH1F( "m_lep_nuReco_ph_fail"   , "m_lep_nuReco_ph_fail"    , 1000, 0, 4000 )
    m_lep_nuReco_ph         = ROOT.TH1F( "m_lep_nuReco_ph"        , "m_lep_nuReco_ph"         , 1000, 0, 4000 )
    m_lep_nu_ph             = ROOT.TH1F( "m_lep_nu_ph"            , "m_lep_nu_ph"             , 1000, 0, 4000 )
    m_q_q                   = ROOT.TH1F( "m_q_q"                  , "m_q_q"                   , 100, 0, 400 )
    m_q_q_ph                = ROOT.TH1F( "m_q_q_ph"               , "m_q_q_ph"                , 1000, 0, 4000 )
    dphi_lep_ph             = ROOT.TH1F( "dphi_lep_ph"            , "dphi_lep_ph"             , 50, 0, 3.2 )
    dphi_lepnu_ph           = ROOT.TH1F( "dphi_lepnu_ph"          , "dphi_lepnu_ph"           , 50, 0, 3.2 )

    check_ph = [22]
    check_lep = [11, -11, 13, -13, 15, -15]
    check_nu = [12, -12, 14, -14, 16, -16]
    check_qk = [1, -1, 2, -2, 3, -3, 4, -4, 5, -5]


    for evt in tree :
        npart = tree.Event[0].Nparticles

        nulvs = []
        leplvs = []
        gamlvs = [] 
        qklvs = []
        for parti in range(0, npart) :
            apid = tree.Particle[parti].PID
            if apid in check_ph :
                gamlv = ROOT.TLorentzVector()
                gamlv.SetPxPyPzE( tree.Particle[parti].Px, tree.Particle[parti].Py,tree.Particle[parti].Pz, tree.Particle[parti].E )
                gamlvs.append( gamlv)

            if apid in check_lep :
                leplv = ROOT.TLorentzVector()
                leplv.SetPxPyPzE( tree.Particle[parti].Px, tree.Particle[parti].Py,tree.Particle[parti].Pz, tree.Particle[parti].E )
                leplvs.append( leplv )

            if apid in check_nu :
                nulv = ROOT.TLorentzVector()
                nulv.SetPxPyPzE( tree.Particle[parti].Px, tree.Particle[parti].Py,tree.Particle[parti].Pz, tree.Particle[parti].E )
                nulvs.append( nulv )

            if apid in check_qk :
                if tree.Particle[parti].Mother1 > 0 :
                    qklv = ROOT.TLorentzVector()
                    qklv.SetPxPyPzE( tree.Particle[parti].Px, tree.Particle[parti].Py,tree.Particle[parti].Pz, tree.Particle[parti].E )
                    qklvs.append( qklv )

        ph_n .Fill( len( gamlvs ) )
        lep_n.Fill( len( leplvs ) )
        nu_n .Fill( len( nulvs ) )
        qk_n .Fill( len( qklvs ) )

        if len( gamlvs ) == 1 :

            ph_pt.Fill( gamlvs[0].Pt()) 

        if len( leplvs ) == 1 :
            lep_pt.Fill( leplvs[0].Pt()) 

        if len( nulvs ) == 1 :
            nu_pt.Fill( nulvs[0].Pt() )


        if len( gamlvs ) == 1 and len( leplvs ) == 1 and len( nulvs ) == 1 :

            m_lep_nu.Fill( (leplvs[0] + nulvs[0]).M())
            m_lep_nu_ph.Fill( (leplvs[0] + nulvs[0] + gamlvs[0]).M() )
            dphi_lep_ph.Fill( (leplvs[0].DeltaPhi( gamlvs[0] ) )  )
            dphi_lepnu_ph.Fill( (( leplvs[0] + nulvs[0] ).DeltaPhi( gamlvs[0] ) )  )
            #br_m_lep_nu_ph[0] = (leplvs[0] + nulvs[0] + gamlvs[0]).M()

            met = ROOT.TLorentzVector()
            met.SetPtEtaPhiM( nulvs[0].Pt(), 0.0, nulvs[0].Phi(), 0.0,  )
            met_orig = ROOT.TLorentzVector( met )

            mt_lep_nu.Fill( calc_mt( leplvs[0] , met ) )
            mt_lep_nu_ph.Fill( calc_mt( leplvs[0]+met , gamlvs[0] ) ) 

            m_lep_nuNoZ.Fill( ( leplvs[0] + met ).M() )  

            success = get_wgamma_nu_pz( leplvs[0], met )

            m_lep_nuReco.Fill( ( leplvs[0] + met ).M() )
            m_lep_nuReco_ph .Fill( (leplvs[0] + gamlvs[0] + met ).M() )

            if success :
                m_lep_nuNoZ_success     .Fill( ( leplvs[0] + met_orig ).M() )  
                m_lep_nuReco_success    .Fill( ( leplvs[0] + met ).M() )
                m_lep_nuReco_ph_success .Fill( (leplvs[0] + gamlvs[0] + met ).M() )

            else :
                m_lep_nuNoZ_fail     .Fill( ( leplvs[0] + met_orig ).M() )  
                m_lep_nuReco_fail    .Fill( ( leplvs[0] + met ).M() )
                m_lep_nuReco_ph_fail .Fill( (leplvs[0] + gamlvs[0] + met ).M() )


        if len( gamlvs ) == 1 and len( qklvs ) == 2 :

            m_q_q.Fill( ( qklvs[0] + qklvs[1] ).M() )
            m_q_q_ph.Fill( ( qklvs[0] + qklvs[1] + gamlvs[0] ).M() )


        #outtree.Fill()


    outFile = ROOT.TFile.Open( options.output, 'RECREATE' )
    outFile.cd()

    ph_n.Write()
    lep_n.Write()
    nu_n.Write()
    qk_n.Write()
    ph_pt.Write()
    lep_pt.Write()
    nu_pt.Write()
    m_lep_nu.Write()
    mt_lep_nu.Write()
    mt_lep_nu_ph.Write()
    m_lep_nuNoZ.Write()
    m_lep_nuNoZ_success.Write()
    m_lep_nuNoZ_fail.Write()
    m_lep_nuReco_success.Write()
    m_lep_nuReco_fail.Write()
    m_lep_nuReco.Write()
    m_lep_nuReco_ph_success.Write()
    m_lep_nuReco_ph_fail.Write()
    m_lep_nuReco_ph.Write()
    m_lep_nu_ph.Write()
    m_q_q.Write()
    m_q_q_ph.Write()
    dphi_lep_ph.Write()
    dphi_lepnu_ph.Write()


    outFile.Close()



def get_wgamma_nu_pz( lepton, metlv ) :

    solved_pz = -1;

    desc_pos = calc_constrained_nu_momentum( lepton, metlv, solved_pz )
    if desc_pos :
        metlv.SetPz( solved_pz )

    else :

        alpha = ( lepton.Px()*metlv.Px() + lepton.Py()*metlv.Py() )/ metlv.Pt()
        delta = ( _m_w*_m_w - lepton.M()*lepton.M() )

        Aval = 4*lepton.Pz()*lepton.Pz() - 4*lepton.E()*lepton.E() +4*alpha*alpha
        Bval = 4*alpha*delta
        Cval = delta*delta

        solution1=-1;
        solution2=-1;

        success2 = solve_quadratic( Aval, Bval, Cval, solution1, solution2 )

        if not success2 :
            print "SECOND FAILURE"

        scale1 = solution1/metlv.Pt()
        scale2 = solution2/metlv.Pt()

        metlv_sol1 = ROOT.TLorentzVector()
        metlv_sol2 = ROOT.TLorentzVector ()
        metlv_sol1.SetPtEtaPhiM( metlv.Pt()*scale1, 0.0, metlv.Phi(), 0.0 )
        metlv_sol2.SetPtEtaPhiM( metlv.Pt()*scale2, 0.0, metlv.Phi(), 0.0 )

        pz_sol1 = -1
        pz_sol2 = -1
        success_sol1 = calc_constrained_nu_momentum( lepton, metlv_sol1, pz_sol1 )
        success_sol2 = calc_constrained_nu_momentum( lepton, metlv_sol2, pz_sol2 )

        if not success_sol1  :
            print "FAILURE SOLUTION 1"
            metlv.SetPtEtaPhiM(-1, 0, 0, 0)
            return False

        if not success_sol2 :
            print "FAILURE SOLUTION 2" 
            metlv.SetPtEtaPhiM(-1, 0, 0, 0)
            return False

        solved_met3v_sol1 = ROOT.TVector3()
        solved_met3v_sol2 = ROOT.TVector3()
        solved_met3v_sol1.SetXYZ(metlv_sol1.Px(), metlv_sol1.Py(), pz_sol1)
        solved_met3v_sol2.SetXYZ(metlv_sol2.Px(), metlv_sol2.Py(), pz_sol2)
        solved_metlv_sol1 = ROOT.TLorentzVector ()
        solved_metlv_sol2 = ROOT.TLorentzVector ()
        solved_metlv_sol1.SetVectM( solved_met3v_sol1 , 0.0 )
        solved_metlv_sol2.SetVectM( solved_met3v_sol2 , 0.0 )

        wmass_sol1 = ( lepton + solved_metlv_sol1 ).M()
        wmass_sol2 = ( lepton + solved_metlv_sol2 ).M()

        if math.fabs( wmass_sol1 - _m_w ) < math.fabs( wmass_sol2 - _m_w ) :
            solved_pz = pz_sol1
            metlv = metlv_sol1
        else  :
            solved_pz = pz_sol2
            metlv = metlv_sol2
        
    return desc_pos;

def calc_constrained_nu_momentum( lepton, met, result ) :

    little_a = _m_w*_m_w - lepton.M()*lepton.M() + 2*( lepton.Px()*met.Px() + lepton.Py()*met.Py() )

    Aval = ( 4*lepton.E()*lepton.E() ) - ( 4*lepton.Pz()*lepton.Pz() )
    Bval = -4 * little_a * lepton.Pz()

    Cval = 4*lepton.E()*lepton.E()*met.Pt()*met.Pt() - little_a*little_a

    solution1=-1
    solution2=-1
    success = solve_quadratic( Aval, Bval, Cval, solution1, solution2 )

    if  success :
       if math.fabs(solution1 - lepton.Pz() ) < math.fabs( solution2 - lepton.Pz() )  :
           result = solution1
       else :
           result = solution2
    return success

def solve_quadratic( Aval, Bval, Cval, solution1, solution2 ) :

    discriminant = Bval*Bval - 4*Aval*Cval

    if discriminant >= 0 :
       solution1 = ( -1*Bval + math.sqrt( discriminant ) ) / ( 2 * Aval ) 
       solution2 = ( -1*Bval - math.sqrt( discriminant ) ) / ( 2 * Aval )  
       return True;
    else :
        return False;

def calc_mt( obj, nu ) :

     return math.sqrt( 2*obj.Pt()*nu.Pt() * ( 1 - math.cos( obj.DeltaPhi(nu) ) ) )


main()
