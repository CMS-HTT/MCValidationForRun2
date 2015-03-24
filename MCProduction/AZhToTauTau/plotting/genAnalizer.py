#! /usr/bin/env python

import ROOT
import sys
from DataFormats.FWLite import Events, Handle
from style import PlotStyle
from cmsTitle import CMS_lumi

PlotStyle()

# Make VarParsing object
# https://twiki.cern.ch/twiki/bin/view/CMS/SWGuideAboutPythonConfigFile#VarParsing_Example
from FWCore.ParameterSet.VarParsing import VarParsing
options = VarParsing ('python')
options.parseArguments()

# Events takes either
# - single file name
# - list of file names
# - VarParsing options

# use Varparsing object
# events = Events (options)
events = Events (['../260/stuff/HIG-RunIIWinter15GS-00003-primi-eventi.root',
                  '../260/stuff/HIG-RunIIWinter15GS-00003-primi-eventi-2.root',
                  '../260/stuff/HIG-RunIIWinter15GS-00003-new.root',
                  '../260/stuff/HIG-RunIIWinter15GS-00003-new2.root',
                  '../260/stuff/prod_test2_1of20/HIG-RunIIWinter15GS-00003_1of20.root',
                  '../260/stuff/prod_test2_2of20/HIG-RunIIWinter15GS-00003_2of20.root',
                  '../260/stuff/prod_test2_3of20/HIG-RunIIWinter15GS-00003_3of20.root',
                  #'260/stuff/prod_test2_4of20/HIG-RunIIWinter15GS-00003_4of20.root',
                  '../260/stuff/prod_test2_5of20/HIG-RunIIWinter15GS-00003_5of20.root',
                  '../260/stuff/prod_test2_6of20/HIG-RunIIWinter15GS-00003_6of20.root',
                  #'260/stuff/prod_test2_7of20/HIG-RunIIWinter15GS-00003_7of20.root',
                  #'260/stuff/prod_test2_8of20/HIG-RunIIWinter15GS-00003_8of20.root',
                  '../260/stuff/prod_test2_9of20/HIG-RunIIWinter15GS-00003_9of20.root',
                  '../260/stuff/prod_test2_10of20/HIG-RunIIWinter15GS-00003_10of20.root',
                  '../260/stuff/prod_test2_11of20/HIG-RunIIWinter15GS-00003_11of20.root',
                  '../260/stuff/prod_test2_12of20/HIG-RunIIWinter15GS-00003_12of20.root',
                  '../260/stuff/prod_test2_13of20/HIG-RunIIWinter15GS-00003_13of20.root',
                  '../260/stuff/prod_test2_14of20/HIG-RunIIWinter15GS-00003_14of20.root',
                  '../260/stuff/prod_test2_15of20/HIG-RunIIWinter15GS-00003_15of20.root',
                  '../260/stuff/prod_test2_16of20/HIG-RunIIWinter15GS-00003_16of20.root',
                  '../260/stuff/prod_test2_17of20/HIG-RunIIWinter15GS-00003_17of20.root',
                  '../260/stuff/prod_test2_18of20/HIG-RunIIWinter15GS-00003_18of20.root',
                  '../260/stuff/prod_test2_19of20/HIG-RunIIWinter15GS-00003_19of20.root',
                  '../260/stuff/prod_test2_20of20/HIG-RunIIWinter15GS-00003_20of20.root',
                  ])

# create handle outside of loop
handle  = Handle ('std::vector<reco::GenParticle>')
label = ('genParticles')

# Create histograms, etc.
ROOT.gROOT.SetBatch()
ROOT.gROOT.SetStyle('Plain')
h1_pdgid = ROOT.TH1F ('h1_pdgid', '', 100, - 50,  50)
h1_massA = ROOT.TH1F ('h1_massA', '',  20,  258, 262)
h1_massZ = ROOT.TH1F ('h1_massZ', '',  20,   85,  99)
h1_massh = ROOT.TH1F ('h1_massh', '',  20,  124.5, 125.5)

for i, event in enumerate(events):
    print i,']'
    event.getByLabel(label, handle)
    genparticles = handle.product()
    gentau = [p for p in genparticles if abs(p.pdgId()) == 15                             ]
    genmu  = [p for p in genparticles if abs(p.pdgId()) == 13                             ]
    genele = [p for p in genparticles if abs(p.pdgId()) == 11                             ]
    gennu  = [p for p in genparticles if abs(p.pdgId()) in [12,14,16]                     ]
    genA   = [p for p in genparticles if abs(p.pdgId()) == 36         and p.status() == 62]
    genZ   = [p for p in genparticles if abs(p.pdgId()) == 23                             ]
    genh   = [p for p in genparticles if abs(p.pdgId()) == 25                             ]

    h1_massA.Fill(genA[0].mass())
    h1_massZ.Fill(genZ[0].mass())
    h1_massh.Fill(genh[0].mass())

#     if len(genZ) > 1 or len(genh) > 1 or len(genA) > 1:
#         import pdb ; pdb.set_trace()
#         if genZ[0].mother() != genA[0] or genh[0].mother() != genA[0]:
#             import pdb ; pdb.set_trace()

#     for p in genparticles:
#         h1_pdgid.Fill(p.pdgId())

# make a canvas, draw, and save it
c1 = ROOT.TCanvas()
CMS_lumi(ROOT.gPad, 2, 0)


h1_massA.Draw()
c1.Print ('h1_massA.pdf')

h1_massZ.Draw()
c1.Print ('h1_massZ.pdf')

h1_massh.Draw()
c1.Print ('h1_massh.pdf')
