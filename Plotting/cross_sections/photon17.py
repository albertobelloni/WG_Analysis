[
 #Cross sections are in pb
 # Some are taken from 
 # https://twiki.cern.ch/twiki/bin/viewauth/CMS/StandardModelCrossSectionsat13TeV 
 # TTBar total cros section is 815.96 pb, taken from https://twiki.cern.ch/twiki/bin/view/LHCPhysics/TtbarNNLO
 # https://twiki.cern.ch/twiki/bin/view/LHCPhysics/SingleTopRefXsec
( 'DYJetsToLL_M-50'               , { 'n_evt' : 46294554, 'cross_section' : 6077.22, 'gen_eff' : 1.0 , 'k_factor' : 1.0 }), # NNLO cross section from https://twiki.cern.ch/twiki/bin/viewauth/CMS/StandardModelCrossSectionsat13TeV
( 'DYJetsToLL_M-50-amcatnloFXFX'  , { 'n_evt' : 123584524, 'cross_section' : 6077.22, 'gen_eff' : 1.0 , 'k_factor' : 1.0 }), # NNLO cross section from [1] 122055288  6225.42 ## from friccita
( 'ZGTo2LG'                       , { 'n_evt' : 19282022, 'cross_section' : 55.5, 'gen_eff' : 1.0 , 'k_factor' : 1.0 }), # NNLO cross section from  total events = 13626718
( 'tW_top'                        , { 'n_evt' : 4974435, 'cross_section' : 38.09, 'gen_eff' : 1.0 , 'k_factor' : 1.0 }), # NLO from XSDB
( 'tW_antitop'                    , { 'n_evt' : 5375230, 'cross_section' : 38.06, 'gen_eff' : 1.0 , 'k_factor' : 1.0 }), # NLO from XSDB
( 'TTJets_DiLept'                 , { 'n_evt' : 27924233, 'cross_section'  :  815*.105, 'gen_eff' : 1.0, 'k_factor' : 1.0 }), # TTbar cross section times dilepton branching fraction
( 'TTJets_SingleLeptFromT'        , { 'n_evt' : 61761347, 'cross_section' : 815.96*0.438*0.5, 'gen_eff' : 1.0, 'k_factor' : 1.0 }), # TTbar cross section times semileptonic branching fraction divided by 2 for charge
( 'TTJets_SingleLeptFromTbar'     , { 'n_evt' : 56705550, 'cross_section' : 815.96*0.438*0.5, 'gen_eff' : 1.0, 'k_factor' : 1.0 }), # TTbar cross section times semileptonic branching fraction divided by 2 for charge
( 'TTGJets'                       , { 'n_evt' : 4623345, 'cross_section' : 3.697, 'gen_eff' : 1.0, 'k_factor' : 1.0 }), # cross section taken from McM
( 'WWTo2L2Nu'                     , { 'n_evt' : 1, 'cross_section' : (118.7-3.974)*0.1086*0.1086*9, 'gen_eff' : 1.0, 'k_factor' : 1.0 }), # cross section taken from WW AN
( 'WGToLNuG-amcatnloFXFX'         , { 'n_evt' : 25296567, 'cross_section' : 170, 'gen_eff' : 1.0, 'k_factor' : 1.0 }), # cross section taken from McM (489.0) from gridpack, 8.217e+02 .  #total events = 5048470
( 'WGToLNuG-madgraphMLM'          , { 'n_evt' : 5035722, 'cross_section' : 405.271, 'gen_eff' : 1.0, 'k_factor' : 1.0 }), # cross section taken from McM (405.271, from gridpack 1025.9
( 'WGToLNuG_PtG-130-amcatnloFXFX' , { 'n_evt' : 841701, 'cross_section' : 2.563*0.79, 'gen_eff' : 1.0, 'k_factor' : 1.0 }), # cross section taken from McM, from gridpack, 2.563e+00 # total events = 1561571
( 'WGToLNuG_PtG-130-madgraphMLM'  , { 'n_evt' : 1645059, 'cross_section' : 0.6261*1.27, 'gen_eff' : 1.0, 'k_factor' : 1.0 }), # cross section taken from gridpack
( 'WGToLNuG_PtG-500-amcatnloFXFX' , { 'n_evt' : 827560, 'cross_section' : 0.02948*0.76*0.79, 'gen_eff' : 1.0, 'k_factor' : 1.0 }), # cross section taken from McM (0.007945) from gridpack, 2.948e-02 # total events = 1609694
( 'WGToLNuG_PtG-500-madgraphMLM'  , { 'n_evt' : 1393505, 'cross_section' : 0.0117887*0.72, 'gen_eff' : 1.0, 'k_factor' : 1.0 }), # cross section taken from gridpack
( 'WWG'                           , { 'n_evt' : 827630, 'cross_section' : 0.2147, 'gen_eff' : 1.0, 'k_factor' : 1.0 }), # cross section taken from McM.  # total events = 999400
( 'WJetsToLNu-madgraphMLM'        , { 'n_evt' : 31488746, 'cross_section' : 20508.9*3, 'gen_eff' : 1.0 , 'k_factor' : 1.0 }),# NNLO cross section from 
( 'WJetsToLNu-amcatnloFXFX'       , { 'n_evt' : 1, 'cross_section' : 20508.9*3, 'gen_eff' : 1.0 , 'k_factor' : 1.0 }), # total events = 24120319
 #'WJetsToLNu_HT-100To200'       ,: { 'n_evt' : 10235198, 'cross_section' : 1345., 'gen_eff' : 1.0 , 'k_factor' : 1.0 }),
 #'WJetsToLNu_HT-200To400'       ,: { 'n_evt' : 4950373, 'cross_section' :  359.7, 'gen_eff' : 1.0 , 'k_factor' : 1.0 }),
( 'WJetsToLNu_HT-100To200'        , { 'n_evt' : 35283801, 'cross_section' : 1325.3, 'gen_eff' : 1.0 , 'k_factor' : 1.0 }),
( 'WJetsToLNu_HT-200To400'        , { 'n_evt' : 21250517, 'cross_section' :  427.75, 'gen_eff' : 1.0 , 'k_factor' : 1.0 }),
( 'WJetsToLNu_HT-400To600'        , { 'n_evt' : 14112190, 'cross_section' :  63.861, 'gen_eff' : 1.0 , 'k_factor' : 1.0 }),
( 'WJetsToLNu_HT-600To800'        , { 'n_evt' : 21709087, 'cross_section' :  16.288, 'gen_eff' : 1.0 , 'k_factor' : 1.0 }),
( 'WJetsToLNu_HT-800To1200'       , { 'n_evt' : 20432728, 'cross_section' :  7.4843, 'gen_eff' : 1.0 , 'k_factor' : 1.0 }),
( 'WJetsToLNu_HT-1200To2500'      , { 'n_evt' : 19673102, 'cross_section' :  1.7937, 'gen_eff' : 1.0 , 'k_factor' : 1.0 }),
( 'WJetsToLNu_HT-2500ToInf'       , { 'n_evt' : 21495421, 'cross_section' :  0.040381, 'gen_eff' : 1.0 , 'k_factor' : 1.0 }),
( 'WJetsToLNu_Pt-100To250'        , { 'n_evt' : 1, 'cross_section' : 676.3, 'gen_eff' : 1.0 , 'k_factor' : 1.0 }), # total events = 10089661
( 'GJets_HT-40To100'              , { 'n_evt' : 5570866, 'cross_section' : 18700., 'gen_eff' : 1.0, 'k_factor' : 1.0 }),
( 'GJets_HT-100To200'             , { 'n_evt' : 9959190, 'cross_section' : 8640., 'gen_eff' : 1.0, 'k_factor' : 1.0 }),
( 'GJets_HT-200To400'             , { 'n_evt' : 16995110, 'cross_section' : 2300, 'gen_eff' : 1.0, 'k_factor' : 1.0 }),
( 'GJets_HT-400To600'             , { 'n_evt' : 4646958, 'cross_section' : 277.4, 'gen_eff' : 1.0, 'k_factor' : 1.0 }),
( 'GJets_HT-600ToInf'             , { 'n_evt' : 3108230, 'cross_section' : 85.31, 'gen_eff' : 1.0, 'k_factor' : 1.0 }),
( 'DiPhoton'                      , { 'n_evt' : 1533189, 'cross_section' : 135., 'gen_eff' : 1.0, 'k_factor' : 1.0 }), # cross section from HGG AN, total events = 35505641 # kak: changed 248 to 84


 ('ResonanceMass200'        , { 'n_evt' : 50000, 'cross_section' : 75.00    , 'gen_eff' : 1.0 , 'k_factor' : 10.0 }), #FIXME no datapoint
 ('ResonanceMass250'        , { 'n_evt' : 50000, 'cross_section' : 50.00    , 'gen_eff' : 1.0 , 'k_factor' : 10.0 }), #FIXME no datapoint
 ('ResonanceMass300'        , { 'n_evt' : 50000, 'cross_section' : 30.00    , 'gen_eff' : 1.0 , 'k_factor' : 10.0 }), #FIXME no datapoint
 ('ResonanceMass350'        , { 'n_evt' : 50000, 'cross_section' : 20.00    , 'gen_eff' : 1.0 , 'k_factor' : 10.0 }), #FIXME no datapoint
 ('ResonanceMass400'        , { 'n_evt' : 50000, 'cross_section' : 13.46    , 'gen_eff' : 1.0 , 'k_factor' : 10.0 }),
 ('ResonanceMass450'        , { 'n_evt' : 50000, 'cross_section' : 9.00     , 'gen_eff' : 1.0 , 'k_factor' : 10.0 }), #FIXME no datapoint
 ('ResonanceMass500'        , { 'n_evt' : 50000, 'cross_section' : 5.755    , 'gen_eff' : 1.0 , 'k_factor' : 10.0 }),
 ('ResonanceMass600'        , { 'n_evt' : 50000, 'cross_section' : 2.785    , 'gen_eff' : 1.0 , 'k_factor' : 10.0 }),
 ('ResonanceMass700'        , { 'n_evt' : 50000, 'cross_section' : 1.481    , 'gen_eff' : 1.0 , 'k_factor' : 10.0 }),
 ('ResonanceMass800'        , { 'n_evt' : 50000, 'cross_section' : 0.836    , 'gen_eff' : 1.0 , 'k_factor' : 10.0 }),
 ('ResonanceMass900'        , { 'n_evt' : 50000, 'cross_section' : 0.4973   , 'gen_eff' : 1.0 , 'k_factor' : 10.0 }),
 ('ResonanceMass1000'       , { 'n_evt' : 50000, 'cross_section' : 0.3075   , 'gen_eff' : 1.0 , 'k_factor' : 10.0 }),
 ('ResonanceMass1200'       , { 'n_evt' : 50000, 'cross_section' : 0.1283   , 'gen_eff' : 1.0 , 'k_factor' : 10.0 }),
 ('ResonanceMass1400'       , { 'n_evt' : 50000, 'cross_section' : 0.0580   , 'gen_eff' : 1.0 , 'k_factor' : 10.0 }),
 ('ResonanceMass1600'       , { 'n_evt' : 50000, 'cross_section' : 0.0281   , 'gen_eff' : 1.0 , 'k_factor' : 10.0 }),
 ('ResonanceMass1800'       , { 'n_evt' : 50000, 'cross_section' : 0.01422  , 'gen_eff' : 1.0 , 'k_factor' : 10.0 }),
 ('ResonanceMass2000'       , { 'n_evt' : 50000, 'cross_section' : 0.00746  , 'gen_eff' : 1.0 , 'k_factor' : 10.0 }),
 ('ResonanceMass2200'       , { 'n_evt' : 50000, 'cross_section' : 0.00402  , 'gen_eff' : 1.0 , 'k_factor' : 10.0 }),
 ('ResonanceMass2400'       , { 'n_evt' : 50000, 'cross_section' : 0.002225 , 'gen_eff' : 1.0 , 'k_factor' : 10.0 }),
 ('ResonanceMass2600'       , { 'n_evt' : 50000, 'cross_section' : 0.001249 , 'gen_eff' : 1.0 , 'k_factor' : 10.0 }),
 ('ResonanceMass2800'       , { 'n_evt' : 50000, 'cross_section' : 0.000711 , 'gen_eff' : 1.0 , 'k_factor' : 10.0 }),
 ('ResonanceMass3000'       , { 'n_evt' : 50000, 'cross_section' : 0.000409 , 'gen_eff' : 1.0 , 'k_factor' : 10.0 }),
 ('ResonanceMass3500'       , { 'n_evt' : 50000, 'cross_section' : 0.0001   , 'gen_eff' : 1.0 , 'k_factor' : 10.0 }),  #FIXME no datapoint
 ('ResonanceMass4000'       , { 'n_evt' : 50000, 'cross_section' : 0.00003  , 'gen_eff' : 1.0 , 'k_factor' : 10.0 }),  #FIXME no datapoint
                #  ('Zg'                     , { 'n_evt' : 3044343, 'cross_section' : 124.5 , 'gen_eff' : 1.0 , 'k_factor' : 1.0 }),
                #  ('Wg'                     , { 'n_evt' : 2183649, 'cross_section' : 505.8 , 'gen_eff' : 1.0 , 'k_factor' : 1.0 }),
                #  ('WgPt500'                , { 'n_evt' : 1393505, 'cross_section' : 0.0117887 , 'gen_eff' : 1.0 , 'k_factor' : 1.0 }),
                #  ('TTbar'                  , { 'n_evt' : 96584653, 'cross_section' : 831.76, 'gen_eff' : 1.0 , 'k_factor' : 1.0 }),
                #  ('GJets'                  , { 'n_evt' : 1972730, 'cross_section' : 693300.0, 'gen_eff' : 1.0 , 'k_factor' : 1.0 }),
                #  ('WW'                     , { 'n_evt' : 1965200, 'cross_section' : 12.178, 'gen_eff' : 1.0 , 'k_factor' : 1.0 }),
                #  ('ZZ'                     , { 'n_evt' : 996944, 'cross_section' : 16.523, 'gen_eff' : 1.0 , 'k_factor' : 1.0 }),
                #  ('WZ3LNLO'                , { 'n_evt' : 8260201, 'cross_section' : 5.26, 'gen_eff' : 1.0 , 'k_factor' : 1.0 }),
                #  ('ST_TW'                  , { 'n_evt' : 995600, 'cross_section' : 35.6, 'gen_eff' : 1.0 , 'k_factor' : 1.0 }),
                #  ('ST_TbarW'               , { 'n_evt' : 988500, 'cross_section' : 35.6, 'gen_eff' : 1.0 , 'k_factor' : 1.0 }),
                #  ('STtCh'                  , { 'n_evt' : 1, 'cross_section' : 70.69, 'gen_eff' : 1.0 , 'k_factor' : 1.0 }),
                #  ('STsCh'                  , { 'n_evt' : 984400, 'cross_section' : 10.32, 'gen_eff' : 1.0 , 'k_factor' : 1.0 }),
                #  ('DiPhoton_M40_80'        , { 'n_evt' : 4878862, 'cross_section' : 84.0*2.5, 'gen_eff' : 1.0 , 'k_factor' : 1.0 }),
                #  ('DiPhoton_M80toInf'      , { 'n_evt' : 13200226, 'cross_section' : 84.0, 'gen_eff' : 1.0 , 'k_factor' : 1.0 })
                  #'ResonanceMass400Width10' : {'n_evt' : 10000, 'cross_section' : 0.4, 'gen_eff' : 1.0 , 'k_factor' : 1.0 }),
                  #'ResonanceMass2000Width10' : {'n_evt' : 10000, 'cross_section' : 0.004, 'gen_eff' : 1.0 , 'k_factor' : 1.0 }),
]

