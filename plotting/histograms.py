from ROOT import TH1F, kOrange, kBlack
from copy import deepcopy as dc

histograms_properties = {}
histograms = {}

# name, title, nbins, xmin, xmax, xaxistitle
histograms_properties['h1_A_pt'        ] = ['h1_A_pt'        , '',  20,    0  , 500  , 'p_{T}^{A} [GeV]'                                       ,]
histograms_properties['h1_A_eta'       ] = ['h1_A_eta'       , '',  20, -  6  ,   6  , '#eta_{A}'                                              ,]
histograms_properties['h1_A_phi'       ] = ['h1_A_phi'       , '',  20, -  4  ,   4  , '#phi_{A}'                                              ,]

histograms_properties['h1_Z_mass'      ] = ['h1_Z_mass'      , '',  20,   82  , 102  , 'm_{Z} [GeV]'                                           ,]
histograms_properties['h1_Z_pt'        ] = ['h1_Z_pt'        , '',  20,    0  , 200  , 'p_{T}^{Z} [GeV]'                                       ,]
histograms_properties['h1_Z_eta'       ] = ['h1_Z_eta'       , '',  20, -  6  ,   6  , '#eta_{Z}'                                              ,]
histograms_properties['h1_Z_phi'       ] = ['h1_Z_phi'       , '',  20, -  4  ,   4  , '#phi_{Z}'                                              ,]

histograms_properties['h1_h_mass'      ] = ['h1_h_mass'      , '',  20,  122  , 128  , 'm_{h} [GeV]'                                           ,]
histograms_properties['h1_h_pt'        ] = ['h1_h_pt'        , '',  20,    0  , 300  , 'p_{T}^{h} [GeV]'                                       ,]
histograms_properties['h1_h_eta'       ] = ['h1_h_eta'       , '',  20, -  6  ,   6  , '#eta_{h}'                                              ,]
histograms_properties['h1_h_phi'       ] = ['h1_h_phi'       , '',  20, -  4  ,   4  , '#phi_{h}'                                              ,]

histograms_properties['h1_channel'     ] = ['h1_channel'     , '',   6,      0,   6  , 'h decay mode'                                          ,]
histograms_properties['h1_delta_eta_ll'] = ['h1_delta_eta_ll', '',  20,      0,   6  , '#Delta#eta(l_{1},l_{2})'                               ,]
histograms_properties['h1_delta_phi_ll'] = ['h1_delta_phi_ll', '',  20,      0,   3.5, '#Delta#phi(l_{1},l_{2})'                               ,]
histograms_properties['h1_delta_r_ll'  ] = ['h1_delta_r_ll'  , '',  20,      0,   5  , '#DeltaR(l_{1},l_{2})'                                  ,]

histograms_properties['h1_tt_tau1_pt'  ] = ['h1_tt_tau1_pt'  , '',  20,    0  , 200  , '#tau_{h}#tau_{h} channel - p_{T}^{#tau_{1}} [GeV]'     ,]
histograms_properties['h1_tt_tau1_eta' ] = ['h1_tt_tau1_eta' , '',  20, -  6  ,   6  , '#tau_{h}#tau_{h} channel - #eta_{#tau_{1}}'            ,]
histograms_properties['h1_tt_tau1_phi' ] = ['h1_tt_tau1_phi' , '',  20, -  4  ,   4  , '#tau_{h}#tau_{h} channel - #phi_{#tau_{1}}'            ,]
histograms_properties['h1_tt_tau2_pt'  ] = ['h1_tt_tau2_pt'  , '',  20,    0  , 200  , '#tau_{h}#tau_{h} channel - p_{T}^{#tau_{2}} [GeV]'     ,]
histograms_properties['h1_tt_tau2_eta' ] = ['h1_tt_tau2_eta' , '',  20, -  6  ,   6  , '#tau_{h}#tau_{h} channel - #eta_{#tau_{2}}'            ,]
histograms_properties['h1_tt_tau2_phi' ] = ['h1_tt_tau2_phi' , '',  20, -  4  ,   4  , '#tau_{h}#tau_{h} channel - #phi_{#tau_{2}}'            ,]

histograms_properties['h1_mt_mu_pt'    ] = ['h1_mt_mu_pt'    , '',  20,    0  , 200  , '#mu#tau_{h} channel - p_{T}^{#mu} [GeV]'               ,]
histograms_properties['h1_mt_mu_eta'   ] = ['h1_mt_mu_eta'   , '',  20, -  6  ,   6  , '#mu#tau_{h} channel - #eta_{#mu}'                      ,]
histograms_properties['h1_mt_mu_phi'   ] = ['h1_mt_mu_phi'   , '',  20, -  4  ,   4  , '#mu#tau_{h} channel - #phi_{#mu}'                      ,]
histograms_properties['h1_mt_tau_pt'   ] = ['h1_mt_tau_pt'   , '',  20,    0  , 200  , '#mu#tau_{h} channel - p_{T}^{#tau} [GeV]'              ,]
histograms_properties['h1_mt_tau_eta'  ] = ['h1_mt_tau_eta'  , '',  20, -  6  ,   6  , '#mu#tau_{h} channel - #eta_{#tau}'                     ,]
histograms_properties['h1_mt_tau_phi'  ] = ['h1_mt_tau_phi'  , '',  20, -  4  ,   4  , '#mu#tau_{h} channel - #phi_{#tau}'                     ,]

histograms_properties['h1_et_ele_pt'   ] = ['h1_et_ele_pt'   , '',  20,    0  , 200  , 'e#tau_{h} channel - p_{T}^{e} [GeV]'                   ,]
histograms_properties['h1_et_ele_eta'  ] = ['h1_et_ele_eta'  , '',  20, -  6  ,   6  , 'e#tau_{h} channel - #eta_{e}'                          ,]
histograms_properties['h1_et_ele_phi'  ] = ['h1_et_ele_phi'  , '',  20, -  4  ,   4  , 'e#tau_{h} channel - #phi_{e}'                          ,]
histograms_properties['h1_et_tau_pt'   ] = ['h1_et_tau_pt'   , '',  20,    0  , 200  , 'e#tau_{h} channel - p_{T}^{#tau} [GeV]'                ,]
histograms_properties['h1_et_tau_eta'  ] = ['h1_et_tau_eta'  , '',  20, -  6  ,   6  , 'e#tau_{h} channel - #eta_{#tau}'                       ,]
histograms_properties['h1_et_tau_phi'  ] = ['h1_et_tau_phi'  , '',  20, -  4  ,   4  , 'e#tau_{h} channel - #phi_{#tau}'                       ,]

histograms_properties['h1_em_mu_pt'    ] = ['h1_em_mu_pt'    , '',  20,    0  , 200  , 'e#mu channel - p_{T}^{#mu} [GeV]'                      ,]
histograms_properties['h1_em_mu_eta'   ] = ['h1_em_mu_eta'   , '',  20, -  6  ,   6  , 'e#mu channel - #eta_{#mu}'                             ,]
histograms_properties['h1_em_mu_phi'   ] = ['h1_em_mu_phi'   , '',  20, -  4  ,   4  , 'e#mu channel - #phi_{#mu}'                             ,]
histograms_properties['h1_em_ele_pt'   ] = ['h1_em_ele_pt'   , '',  20,    0  , 200  , 'e#mu channel - p_{T}^{e} [GeV]'                        ,]
histograms_properties['h1_em_ele_eta'  ] = ['h1_em_ele_eta'  , '',  20, -  6  ,   6  , 'e#mu channel - #eta_{e}'                               ,]
histograms_properties['h1_em_ele_phi'  ] = ['h1_em_ele_phi'  , '',  20, -  4  ,   4  , 'e#mu channel - #phi_{e}'                               ,]

histograms_properties['h1_mm_mu1_pt'   ] = ['h1_mm_mu1_pt'   , '',  20,    0  , 200  , '#mu#mu channel - p_{T}^{#mu_{1}} [GeV]'                ,]
histograms_properties['h1_mm_mu1_eta'  ] = ['h1_mm_mu1_eta'  , '',  20, -  6  ,   6  , '#mu#mu channel - #eta_{#mu_{1}}'                       ,]
histograms_properties['h1_mm_mu1_phi'  ] = ['h1_mm_mu1_phi'  , '',  20, -  4  ,   4  , '#mu#mu channel - #phi_{#mu_{1}}'                       ,]
histograms_properties['h1_mm_mu2_pt'   ] = ['h1_mm_mu2_pt'   , '',  20,    0  , 200  , '#mu#mu channel - p_{T}^{#mu_{2}} [GeV]'                ,]
histograms_properties['h1_mm_mu2_eta'  ] = ['h1_mm_mu2_eta'  , '',  20, -  6  ,   6  , '#mu#mu channel - #eta_{#mu_{2}}'                       ,]
histograms_properties['h1_mm_mu2_phi'  ] = ['h1_mm_mu2_phi'  , '',  20, -  4  ,   4  , '#mu#mu channel - #phi_{#mu_{2}}'                       ,]

histograms_properties['h1_ee_ele1_pt'  ] = ['h1_ee_ele1_pt'  , '',  20,    0  , 200  , 'ee channel - p_{T}^{e_{1}} [GeV]'                      ,]
histograms_properties['h1_ee_ele1_eta' ] = ['h1_ee_ele1_eta' , '',  20, -  6  ,   6  , 'ee channel - #eta_{e_{1}} [GeV]'                       ,]
histograms_properties['h1_ee_ele1_phi' ] = ['h1_ee_ele1_phi' , '',  20, -  4  ,   4  , 'ee channel - #phi_{e_{1}} [GeV]'                       ,]
histograms_properties['h1_ee_ele2_pt'  ] = ['h1_ee_ele2_pt'  , '',  20,    0  , 200  , 'ee channel - p_{T}^{e_{2}} [GeV]'                      ,]
histograms_properties['h1_ee_ele2_eta' ] = ['h1_ee_ele2_eta' , '',  20, -  6  ,   6  , 'ee channel - #eta_{e_{2}}'                             ,]
histograms_properties['h1_ee_ele2_phi' ] = ['h1_ee_ele2_phi' , '',  20, -  4  ,   4  , 'ee channel - #phi_{e_{2}}'                             ,]

histograms_properties['h1_njets'       ] = ['h1_njets'       , '',  10,    0  ,  10  , '# jets (p_{T}>30 GeV, |#eta|<5)'                       ,]
histograms_properties['h1_nbjets'      ] = ['h1_nbjets'      , '',   6,    0  ,   6  , '# b-jets (p_{T}>20 GeV, |#eta|<2.4)'                   ,]
histograms_properties['h1_delta_eta_jj'] = ['h1_delta_eta_jj', '',  20,    0  ,   6  , '#Delta#eta(j_{1},j_{2})'                               ,]
histograms_properties['h1_delta_phi_jj'] = ['h1_delta_phi_jj', '',  20,    0  ,   3.5, '#Delta#phi(j_{1},j_{2})'                               ,]
histograms_properties['h1_delta_r_jj'  ] = ['h1_delta_r_jj'  , '',  20,    0  ,   5  , '#DeltaR(j_{1},j_{2})'                                  ,]
histograms_properties['h1_sumpt'       ] = ['h1_sumpt'       , '',  20,    0  ,1000  , '#Sigmap_{T} leptons and selected jets [GeV]'           ,]

histograms_properties['h1_jet1_pt'     ] = ['h1_jet1_pt'     , '',  20,    0  , 200  , 'p_{T}^{jet_{1}} [GeV]'                                 ,]
histograms_properties['h1_jet1_eta'    ] = ['h1_jet1_eta'    , '',  20, -  6  ,   6  , '#eta_{jet_{1}}'                                        ,]
histograms_properties['h1_jet1_phi'    ] = ['h1_jet1_phi'    , '',  20, -  4  ,   4  , '#phi_{jet_{1}}'                                        ,]
histograms_properties['h1_jet2_pt'     ] = ['h1_jet2_pt'     , '',  20,    0  , 200  , 'p_{T}^{jet_{2}} [GeV]'                                 ,]
histograms_properties['h1_jet2_eta'    ] = ['h1_jet2_eta'    , '',  20, -  6  ,   6  , '#eta_{jet_{2}}'                                        ,]
histograms_properties['h1_jet2_phi'    ] = ['h1_jet2_phi'    , '',  20, -  4  ,   4  , '#phi_{jet_{2}}'                                        ,]

histograms_properties['h1_met_pt'      ] = ['h1_met_pt'      , '',  20,    0  , 200  , 'E_{T}^{miss} [GeV]'                                    ,]
histograms_properties['h1_met_phi'     ] = ['h1_met_phi'     , '',  20, -  4  ,   4  , '#phi_{E_{T}^{miss}}'                                   ,]


def _createHistos():
    for k, v in histograms_properties.items():
        histo = TH1F(v[0], v[1], v[2], v[3], v[4])
        histo.SetMinimum(0.)
        histo.SetLineWidth(2)
        histo.SetLineColor(kBlack)
        histo.SetFillColor(kOrange)
        histo.SetFillStyle(3344)
        histo.SetMarkerStyle(8)
        histo.GetYaxis().SetTitle('a.u.')
        histo.GetYaxis().SetTitleOffset(1.6)
        histo.GetXaxis().SetTitle(v[5])
        histo.GetXaxis().SetTitleOffset(1.3)

        histograms[k] = dc(histo)

def returnHistos(mass):
    histograms_properties['h1_A_mass'] = ['h1_A_mass', '',  40,  int(mass)*0.95, int(mass)*1.05  , 'm_{A} [GeV]',]
    _createHistos()
    return histograms
