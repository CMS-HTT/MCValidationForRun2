#!/usr/bin/env python

import ROOT
import xml.etree.ElementTree as ET
from lheObjects import Event, Particle        
from style import PlotStyle
 
PlotStyle()   

# tree = ET.parse('../MSSM_AZh_LLTauTau_MG5_aMCNLO_SusHi/madgraph5/PROC_GGH_HEFT/Events/run_04/events_h_to_A.lhe')
tree = ET.parse('../MSSM_AZh_LLTauTau_MG5_aMCNLO_2HDM4MG5/madgraph5/PROC_ggAZhlltt_mA300_HEFT/Events/run_01/events.lhe')
# tree = ET.parse('yuta_mA300.lhe')
# tree = ET.parse('yuta_gridpack.lhe')
root = tree.getroot()

# lheevents = root.findall('event')[:1]
lheevents = root.findall('event')
events = []

for ev in lheevents:
    try:
        weights = ev.find('rwgt').findall('wgt')
    except:
        weights = []
    weights_dict = {weight.attrib.values()[0] : float(weight.text) \
                    for weight in weights}
    events.append(Event(ev.text, weights_dict))


h1_a_mass   = ROOT.TH1F('h1_a_mass'  , '',100,  0  ,1000  )
h1_a_pt     = ROOT.TH1F('h1_a_pt'    , '', 50,  0  , 300  )
h1_a_eta    = ROOT.TH1F('h1_a_eta'   , '', 50, -5  ,   5  )
h1_a_phi    = ROOT.TH1F('h1_a_phi'   , '', 50, -3.5,   3.5)

h1_z_mass   = ROOT.TH1F('h1_z_mass'  , '',100,  0  , 120  )
h1_z_pt     = ROOT.TH1F('h1_z_pt'    , '', 50,  0  , 300  )
h1_z_eta    = ROOT.TH1F('h1_z_eta'   , '', 50, -5  ,   5  )
h1_z_phi    = ROOT.TH1F('h1_z_phi'   , '', 50, -3.5,   3.5)

h1_h_mass   = ROOT.TH1F('h1_h_mass'  , '',100,  0  , 200  )
h1_h_pt     = ROOT.TH1F('h1_h_pt'    , '', 50,  0  , 300  )
h1_h_eta    = ROOT.TH1F('h1_h_eta'   , '', 50, -5  ,   5  )
h1_h_phi    = ROOT.TH1F('h1_h_phi'   , '', 50, -3.5,   3.5)
# h1_weight = ROOT.TH1F('h1_weight', '', 50,  0, 300)

for ev in events:
    # A boson
    aboson = [p for p in ev.particles if p.idup == 36][0]
    # Z boson
    zboson = [p for p in ev.particles if p.idup == 23][0]
    # A boson
    hboson = [p for p in ev.particles if p.idup == 25][0]

    h1_a_mass.Fill(aboson.p4.M  ())
    h1_a_pt  .Fill(aboson.p4.Pt ())
    h1_a_eta .Fill(aboson.p4.Eta())
    h1_a_phi .Fill(aboson.p4.Phi())

    h1_z_mass.Fill(zboson.p4.M  ())
    h1_z_pt  .Fill(zboson.p4.Pt ())
    h1_z_eta .Fill(zboson.p4.Eta())
    h1_z_phi .Fill(zboson.p4.Phi())

    h1_h_mass.Fill(hboson.p4.M  ())
    h1_h_pt  .Fill(hboson.p4.Pt ())
    h1_h_eta .Fill(hboson.p4.Eta())
    h1_h_phi .Fill(hboson.p4.Phi())
    
c1 = ROOT.TCanvas('','',700,700)
for h1 in [h1_a_pt, h1_a_eta, h1_a_phi, h1_a_mass] + \
          [h1_z_pt, h1_z_eta, h1_z_phi, h1_z_mass] + \
          [h1_h_pt, h1_h_eta, h1_h_phi, h1_h_mass]:
    h1.Draw()
    c1.SaveAs(h1.GetName()+'.pdf')