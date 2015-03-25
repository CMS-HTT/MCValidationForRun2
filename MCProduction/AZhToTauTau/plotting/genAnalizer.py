#! /usr/bin/env python

import ROOT
import sys
from DataFormats.FWLite import Events, Handle
from style import PlotStyle
from cmsTitle import CMS_lumi
from histograms import histograms

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
events = Events ([
                  '../300/first2k_1of20/HIG-RunIIWinter15GS-00003_1of20.root'  ,
                  '../300/first2k_2of20/HIG-RunIIWinter15GS-00003_2of20.root'  ,
                  '../300/first2k_3of20/HIG-RunIIWinter15GS-00003_3of20.root'  ,
                  '../300/first2k_4of20/HIG-RunIIWinter15GS-00003_4of20.root'  ,
                  '../300/first2k_5of20/HIG-RunIIWinter15GS-00003_5of20.root'  ,
                  '../300/first2k_6of20/HIG-RunIIWinter15GS-00003_6of20.root'  ,
                  '../300/first2k_7of20/HIG-RunIIWinter15GS-00003_7of20.root'  ,
                  '../300/first2k_8of20/HIG-RunIIWinter15GS-00003_8of20.root'  ,
                  '../300/first2k_9of20/HIG-RunIIWinter15GS-00003_9of20.root'  ,
                  '../300/first2k_10of20/HIG-RunIIWinter15GS-00003_10of20.root',
                  '../300/first2k_11of20/HIG-RunIIWinter15GS-00003_11of20.root',
                  '../300/first2k_12of20/HIG-RunIIWinter15GS-00003_12of20.root',
                  '../300/first2k_13of20/HIG-RunIIWinter15GS-00003_13of20.root',
                  '../300/first2k_14of20/HIG-RunIIWinter15GS-00003_14of20.root',
                  '../300/first2k_15of20/HIG-RunIIWinter15GS-00003_15of20.root',
                  '../300/first2k_16of20/HIG-RunIIWinter15GS-00003_16of20.root',
                  '../300/first2k_17of20/HIG-RunIIWinter15GS-00003_17of20.root',
                  '../300/first2k_18of20/HIG-RunIIWinter15GS-00003_18of20.root',
                  '../300/first2k_19of20/HIG-RunIIWinter15GS-00003_19of20.root',
                  '../300/first2k_20of20/HIG-RunIIWinter15GS-00003_20of20.root',
                  ])

# create handle outside of loop
handle  = Handle ('std::vector<reco::GenParticle>')
label = ('genParticles')

# Create histograms, etc.
ROOT.gROOT.SetBatch()
ROOT.gROOT.SetStyle('Plain')


def fill4vector(particle, histograms, key):
    key_parts = key.split('_')
    try: histograms['_'.join(key_parts[:-1]+['mass'])].Fill(particle.mass())
    except: pass
    histograms['_'.join(key_parts[:-1]+['pt'  ])].Fill(particle.pt()  )
    histograms['_'.join(key_parts[:-1]+['eta' ])].Fill(particle.eta() )
    histograms['_'.join(key_parts[:-1]+['phi' ])].Fill(particle.phi() )

for i, event in enumerate(events):
    #if i > 100: break
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

    fill4vector(genA[0], histograms, 'h1_A_mass')
    fill4vector(genZ[0], histograms, 'h1_Z_mass')
    fill4vector(genh[0], histograms, 'h1_h_mass')


# make a canvas, draw, and save it
c1 = ROOT.TCanvas()
CMS_lumi(ROOT.gPad, 2, 0)

# for k in ['h1_A_mass', 'h1_Z_mass', 'h1_h_mass']:
for k in histograms.keys():
    histograms[k].Draw('HIST')
    c1.Print (k+'.pdf')
