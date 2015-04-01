#!/usr/bin/env python

import ROOT
import sys
import os

from cmsTitle                       import CMS_header
from histograms                     import returnHistos
from style                          import PlotStyle
from utils                          import cleanCollection, cosmetics, deltaPhi, deltaR, fill4vector, tauDecayMode
from DataFormats.FWLite             import Events, Handle
from FWCore.ParameterSet.VarParsing import VarParsing

class genAnalyzer( object ):

    def __init__(self, mass, extraTitle = '', maxEvents = -1):

        self.mass       = str(mass)
        self.maxEvents  = maxEvents
        self.extraTitle = extraTitle
        self.histograms = returnHistos(self.mass)

        self._iniStyle()
        self._iniFolder()
        self._iniHandles()
        self._getEvents()

        # Make VarParsing object
        # https://twiki.cern.ch/twiki/bin/view/CMS/SWGuideAboutPythonConfigFile#VarParsing_Example
        self.options = VarParsing('python')
        self.options.parseArguments()

        # Events takes either
        # - single file name
        # - list of file names
        # - VarParsing options

        # use Varparsing object
        # events = Events (options)

    def _iniStyle(self):
        ROOT.gROOT.SetBatch()
        ROOT.gROOT.SetStyle('Plain')
        PlotStyle()

    def _iniFolder(self):
        self.folder = 'mA'+self.mass
        os.system('mkdir ' + self.folder)

    def _iniHandles(self):
        self.handles = {}
        self.handles['genParticles'] = [Handle('std::vector<reco::GenParticle>'), 'genParticles']
        self.handles['ak4GenJets']   = [Handle('vector<reco::GenJet>'          ), 'ak4GenJets'  ]

    def _getEvents(self):
        '''
        file location is hard coded.
        FIXME!
        '''
        self.events = Events ([
                               '/afs/cern.ch/work/m/manzoni/mc-generation/CMSSW_7_1_13/src/MSSM_AZh_LLTauTau_MG5_aMCNLO/PROC_MSSM_AZH/Events/run_02/EDM2GEN_PY8.root',
                              ])

    def loop(self):

        for i, event in enumerate(self.events):
            if i+1 > self.maxEvents: break
            print i,']'
            self.process(event)

    def process(self, event):
        pass

    def saveHistos(self, png = False):
        # make a canvas, draw, and save it
        c1 = ROOT.TCanvas()
        header = CMS_header(self.extraTitle)

        for k in self.histograms.keys():
            self.histograms[k].Draw('HISTE')
            cosmetics(header)
            c1.Modified()
            c1.Update()
            c1.Print(self.folder+'/'+k+'.pdf')
            if png:
                c1.Print(self.folder+'/'+k+'.png')

if __name__ == '__main__':

    analyzer = genAnalyzer(mass = 400,
        extraTitle = 'PYTHIA8 A#rightarrowZh, h#rightarrow#tau#tau, m_{A}= 400 GeV, tan#beta = 2',
        maxEvents = 10)
    analyzer.loop()
    analyzer.saveHistos()

