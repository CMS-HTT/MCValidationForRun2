from ROOT import TH1F

histograms = {}

histograms['h1_A_mass'     ] = TH1F('h1_A_mass'     , '',  20,  250, 270), 'm_{A} [GeV]'
histograms['h1_A_pt'       ] = TH1F('h1_A_pt'       , '',  20,  250, 270), 'p_{T}^{A} [GeV]'
histograms['h1_A_eta'      ] = TH1F('h1_A_eta'      , '',  20,  250, 270), '#eta_{A} [GeV]'
histograms['h1_A_phi'      ] = TH1F('h1_A_phi'      , '',  20,  250, 270), '#phi_{A} [GeV]'

histograms['h1_Z_mass'     ] = TH1F('h1_Z_mass'     , '',  20,  250, 270), 'm_{Z} [GeV]'
histograms['h1_Z_pt'       ] = TH1F('h1_Z_pt'       , '',  20,  250, 270), 'p_{T}^{Z} [GeV]'
histograms['h1_Z_eta'      ] = TH1F('h1_Z_eta'      , '',  20,  250, 270), '#eta_{Z} [GeV]'
histograms['h1_Z_phi'      ] = TH1F('h1_Z_phi'      , '',  20,  250, 270), '#phi_{Z} [GeV]'

histograms['h1_h_mass'     ] = TH1F('h1_h_mass'     , '',  20,  250, 270), 'm_{h} [GeV]'
histograms['h1_h_pt'       ] = TH1F('h1_h_pt'       , '',  20,  250, 270), 'p_{T}^{h} [GeV]'
histograms['h1_h_eta'      ] = TH1F('h1_h_eta'      , '',  20,  250, 270), '#eta_{h} [GeV]'
histograms['h1_h_phi'      ] = TH1F('h1_h_phi'      , '',  20,  250, 270), '#phi_{h} [GeV]'

histograms['h1_channel'    ] = TH1F('h1_channel'    , '',  20,  250, 270), 'm_{A} [GeV]'
histograms['h1_njets'      ] = TH1F('h1_njets'      , '',  20,  250, 270), 'm_{A} [GeV]'

histograms['h1_tt_tau1_pt' ] = TH1F('h1_tt_tau1_pt' , '',  20,  250, 270), 'p_{T}^{#tau_{1}} [GeV]'
histograms['h1_tt_tau1_eta'] = TH1F('h1_tt_tau1_eta', '',  20,  250, 270), '#eta_{#tau_{1}} [GeV]'
histograms['h1_tt_tau1_phi'] = TH1F('h1_tt_tau1_phi', '',  20,  250, 270), '#phi_{#tau_{1}} [GeV]'
histograms['h1_tt_tau2_pt' ] = TH1F('h1_tt_tau2_pt' , '',  20,  250, 270), 'p_{T}^{#tau_{2}} [GeV]'
histograms['h1_tt_tau2_eta'] = TH1F('h1_tt_tau2_eta', '',  20,  250, 270), '#eta_{#tau_{2}} [GeV]'
histograms['h1_tt_tau2_phi'] = TH1F('h1_tt_tau2_phi', '',  20,  250, 270), '#phi_{#tau_{2}} [GeV]'

histograms['h1_mt_mu_pt'   ] = TH1F('h1_mt_mu_pt'   , '',  20,  250, 270), 'p_{T}^{#mu} [GeV]'
histograms['h1_mt_mu_eta'  ] = TH1F('h1_mt_mu_eta'  , '',  20,  250, 270), '#eta_{#mu} [GeV]'
histograms['h1_mt_mu_phi'  ] = TH1F('h1_mt_mu_phi'  , '',  20,  250, 270), '#phi_{#mu} [GeV]'
histograms['h1_mt_tau_pt'  ] = TH1F('h1_mt_tau_pt'  , '',  20,  250, 270), 'p_{T}^{#tau} [GeV]'
histograms['h1_mt_tau_eta' ] = TH1F('h1_mt_tau_eta' , '',  20,  250, 270), '#eta_{#tau} [GeV]'
histograms['h1_mt_tau_phi' ] = TH1F('h1_mt_tau_phi' , '',  20,  250, 270), '#phi_{#tau} [GeV]'

histograms['h1_et_ele_pt'  ] = TH1F('h1_et_ele_pt'  , '',  20,  250, 270), 'p_{T}^{e} [GeV]'
histograms['h1_et_ele_eta' ] = TH1F('h1_et_ele_eta' , '',  20,  250, 270), '#eta_{e} [GeV]'
histograms['h1_et_ele_phi' ] = TH1F('h1_et_ele_phi' , '',  20,  250, 270), '#phi_{e} [GeV]'
histograms['h1_et_tau_pt'  ] = TH1F('h1_et_tau_pt'  , '',  20,  250, 270), 'p_{T}^{#tau} [GeV]'
histograms['h1_et_tau_eta' ] = TH1F('h1_et_tau_eta' , '',  20,  250, 270), '#eta_{#tau} [GeV]'
histograms['h1_et_tau_phi' ] = TH1F('h1_et_tau_phi' , '',  20,  250, 270), '#phi_{#tau} [GeV]'

histograms['h1_jet1_pt'    ] = TH1F('h1_jet1_pt'    , '',  20,  250, 270), 'p_{T}^{h} [GeV]'
histograms['h1_jet1_eta'   ] = TH1F('h1_jet1_eta'   , '',  20,  250, 270), '#eta_{h} [GeV]'
histograms['h1_jet1_phi'   ] = TH1F('h1_jet1_phi'   , '',  20,  250, 270), '#phi_{h} [GeV]'
histograms['h1_jet2_pt'    ] = TH1F('h1_jet2_pt'    , '',  20,  250, 270), 'p_{T}^{h} [GeV]'
histograms['h1_jet2_eta'   ] = TH1F('h1_jet2_eta'   , '',  20,  250, 270), '#eta_{h} [GeV]'
histograms['h1_jet2_phi'   ] = TH1F('h1_jet2_phi'   , '',  20,  250, 270), '#phi_{h} [GeV]'

for k, v in histograms:
    v.GetYaxis().SetTitle('events')
    v.GetXaxis().SetTitle('events')

