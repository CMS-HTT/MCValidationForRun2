#!/usr/bin/env python

import ROOT
import xml.etree.ElementTree as ET
from lheObjects import Event, Particle        
from style import PlotStyle
 
PlotStyle()   

# tree = ET.parse('../MSSM_AZh_LLTauTau_MG5_aMCNLO_SusHi/madgraph5/PROC_GGH_HEFT/Events/run_04/events_h_to_A.lhe')
tree = ET.parse('../MSSM_AZh_LLTauTau_MG5_aMCNLO_2HDM4MG5/madgraph5/PROC_ggAZhlltt_mA300_HEFT/Events/run_01/events.lhe')
root = tree.getroot()

lheevents = root.findall('event')[:1]
events = []

for ev in lheevents:
    try:
        weights = ev.find('rwgt').findall('wgt')
    except:
        weights = []
    weights_dict = {weight.attrib.values()[0] : float(weight.text) \
                    for weight in weights}
    events.append(Event(ev.text, weights_dict))


h1_pt     = ROOT.TH1F('h1_pt'    , '', 50,  0  , 300  )
h1_eta    = ROOT.TH1F('h1_eta'   , '', 50, -5  ,   5  )
h1_phi    = ROOT.TH1F('h1_phi'   , '', 50, -3.5,   3.5)
# h1_weight = ROOT.TH1F('h1_weight', '', 50,  0, 300)

for ev in events:
    aboson = [p for p in ev.particles if p.idup == 36][0]
    h1_pt .Fill(aboson.p4.Pt ())
    h1_eta.Fill(aboson.p4.Eta())
    h1_phi.Fill(aboson.p4.Phi())
    
c1 = ROOT.TCanvas('','',700,700)
for h1 in [h1_pt, h1_eta, h1_phi]:
    h1.Draw()
    c1.SaveAs(h1.GetName()+'.pdf')