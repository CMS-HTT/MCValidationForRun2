#!/usr/bin/env python

from DataFormats.FWLite             import Events, Handle
from FWCore.ParameterSet.VarParsing import VarParsing
from utils                          import cleanCollection, cosmetics, deltaPhi, deltaR, fill4vector, tauDecayMode
from genAnalyzer                    import genAnalyzer

class genAnalyzerHTT( genAnalyzer ):

    def process(self, event):
        '''
        To be implemented.
        FIXME!
        '''
        #event.getByLabel(self.handles['genParticles'][1], self.handles['genParticles'][0])
        #genparticles = self.handles['genParticles'][0].product()

        #event.getByLabel(self.handles['ak4GenJets'][1], self.handles['ak4GenJets'][0])
        #genjets = self.handles['ak4GenJets'][0].product()

        #gentau = [p for p in genparticles if abs(p.pdgId()) == 15        ]
        #genmu  = [p for p in genparticles if abs(p.pdgId()) == 13        ]
        #genele = [p for p in genparticles if abs(p.pdgId()) == 11        ]
        #gennu  = [p for p in genparticles if abs(p.pdgId()) in [12,14,16]]

if __name__ == '__main__':

    analyzer = genAnalyzerHTT(mass = 125,
        extraTitle = 'SM H#rightarrow#tau#tau',
        maxEvents = 10)
    analyzer.loop()
    analyzer.saveHistos()

