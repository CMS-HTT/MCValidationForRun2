#!/usr/bin/env python

from DataFormats.FWLite             import Events, Handle
from FWCore.ParameterSet.VarParsing import VarParsing
from utils                          import cleanCollection, cosmetics, deltaPhi, deltaR, fill4vector, tauDecayMode
from genAnalyzer                    import genAnalyzer

class genAnalyzerMSSM_AZh( genAnalyzer ):

    def process(self, event):

        event.getByLabel(self.handles['genParticles'][1], 
                         self.handles['genParticles'][0])
        genparticles = self.handles['genParticles'][0].product()

        event.getByLabel(self.handles['ak4GenJets'][1], 
                         self.handles['ak4GenJets'][0])
        genjets = self.handles['ak4GenJets'][0].product()
        
        # per event weight
        event.getByLabel(self.handles['generator'][1], 
                         self.handles['generator'][0])
        geninfo = self.handles['generator'][0].product()

        weight = geninfo.weight() 

        try:
            # per event weight computed by SusHi
            event.getByLabel(self.handles['source'][1], 
                             self.handles['source'][0])
            lhesource = self.handles['source'][0].product()

            if len(lhesource.weights()):
                for w in lhesource.weights():
                    if w.id == '1009':
                        weight = w.wgt
        except:
            pass
        
        #import pdb ; pdb.set_trace()
                
        self.sumOfWeights += weight

        gentau = [p for p in genparticles if abs(p.pdgId()) == 15                             ]
        genmu  = [p for p in genparticles if abs(p.pdgId()) == 13                             ]
        genele = [p for p in genparticles if abs(p.pdgId()) == 11                             ]
        gennu  = [p for p in genparticles if abs(p.pdgId()) in [12,14,16]                     ]
        genA   = [p for p in genparticles if abs(p.pdgId()) == 36         and p.status() == 62]
        genZ   = [p for p in genparticles if abs(p.pdgId()) == 23                             ]
        genh   = [p for p in genparticles if abs(p.pdgId()) == 25                             ]

        if len(genA) != 1 or \
           len(genZ) != 1 or \
           len(genh) != 1:
            print '\nERROR'
            print 'num. of A %d, num. of Z %d, num. of h %d\n' %(len(genA), len(genZ), len(genh))
            import pdb ; pdb.set_trace()
            return
            #raise

        fill4vector(genA[0], self.histograms, 'h1_A_mass', weight)
        fill4vector(genZ[0], self.histograms, 'h1_Z_mass', weight)
        fill4vector(genh[0], self.histograms, 'h1_h_mass', weight)

        if not ( (genA[0].daughter(0).pdgId() == 23 and genA[0].daughter(1).pdgId() == 25) or \
                 (genA[0].daughter(0).pdgId() == 25 and genA[0].daughter(1).pdgId() == 23) ):
            print '\nERROR'
            print 'A does not decay into Zh!'
            print 'daughter pdgId %d, daughter pdgId %d\n' %(genA[0].daughter(0).pdgId(), genA[0].daughter(1).pdgId())
            raise

        if abs(genh[0].daughter(0).pdgId()) != 15 or \
           abs(genh[0].daughter(1).pdgId()) != 15:
            print '\nERROR'
            print 'h does not decay into taus!'
            print 'leg1 pdgId %d, leg2 pdgId %d\n' %(genh[0].daughter(0).pdgId(), genh[0].daughter(1).pdgId())
            raise

        final_state_tau_into_mu_from_h125  = []
        final_state_tau_into_ele_from_h125 = []
        final_state_tau_into_had_from_h125 = []

        for tau in [genh[0].daughter(0), genh[0].daughter(1)]:
            type, daughter = tauDecayMode(tau)
            if type == 'ele':
                final_state_tau_into_mu_from_h125.append(daughter)
            elif type == 'muon':
                final_state_tau_into_ele_from_h125.append(daughter)
            elif type == 'tau':
                final_state_tau_into_had_from_h125.append(daughter)
            else:
                print 'How the hell this tau decays?!'
                raise

        self.histograms['h1_delta_phi_ll'].Fill( deltaPhi( genh[0].daughter(0), genh[0].daughter(1) ), weight)
        self.histograms['h1_delta_eta_ll'].Fill( abs(genh[0].daughter(0).eta() - genh[0].daughter(1).eta()), weight )
        self.histograms['h1_delta_r_ll']  .Fill( deltaR  ( genh[0].daughter(0), genh[0].daughter(1) ), weight )

        if len(final_state_tau_into_had_from_h125) == 2 :
            self.histograms['h1_channel'].Fill('tt', weight)
            if final_state_tau_into_had_from_h125[0].pt() > final_state_tau_into_had_from_h125[1].pt():
                fill4vector(final_state_tau_into_had_from_h125[0], self.histograms, 'h1_tt_tau1_pt', weight)
                fill4vector(final_state_tau_into_had_from_h125[1], self.histograms, 'h1_tt_tau2_pt', weight)
            else:
                fill4vector(final_state_tau_into_had_from_h125[0], self.histograms, 'h1_tt_tau2_pt', weight)
                fill4vector(final_state_tau_into_had_from_h125[1], self.histograms, 'h1_tt_tau1_pt', weight)
        elif len(final_state_tau_into_had_from_h125) == 1 :
            if len(final_state_tau_into_mu_from_h125) == 1 :
                self.histograms['h1_channel'].Fill('mt', weight)
                fill4vector(final_state_tau_into_mu_from_h125 [0], self.histograms, 'h1_mt_mu_pt' , weight)
                fill4vector(final_state_tau_into_had_from_h125[0], self.histograms, 'h1_mt_tau_pt', weight)
            elif len(final_state_tau_into_ele_from_h125) == 1 :
                self.histograms['h1_channel'].Fill('et', weight)
                fill4vector(final_state_tau_into_ele_from_h125[0], self.histograms, 'h1_et_ele_pt', weight)
                fill4vector(final_state_tau_into_had_from_h125[0], self.histograms, 'h1_et_tau_pt', weight)
        if len(final_state_tau_into_ele_from_h125) == 2 :
            self.histograms['h1_channel'].Fill('ee', weight)
            if final_state_tau_into_ele_from_h125[0].pt() > final_state_tau_into_ele_from_h125[1].pt():
                fill4vector(final_state_tau_into_ele_from_h125[0], self.histograms, 'h1_ee_ele1_pt', weight)
                fill4vector(final_state_tau_into_ele_from_h125[1], self.histograms, 'h1_ee_ele2_pt', weight)
            else:
                fill4vector(final_state_tau_into_ele_from_h125[0], self.histograms, 'h1_ee_ele2_pt', weight)
                fill4vector(final_state_tau_into_ele_from_h125[1], self.histograms, 'h1_ee_ele1_pt', weight)
        if len(final_state_tau_into_mu_from_h125) == 2 :
            self.histograms['h1_channel'].Fill('mm', weight)
            if final_state_tau_into_mu_from_h125[0].pt() > final_state_tau_into_mu_from_h125[1].pt():
                fill4vector(final_state_tau_into_mu_from_h125[0], self.histograms, 'h1_mm_mu1_pt', weight)
                fill4vector(final_state_tau_into_mu_from_h125[1], self.histograms, 'h1_mm_mu2_pt', weight)
            else:
                fill4vector(final_state_tau_into_mu_from_h125[0], self.histograms, 'h1_mm_mu2_pt', weight)
                fill4vector(final_state_tau_into_mu_from_h125[1], self.histograms, 'h1_mm_mu1_pt', weight)
        if len(final_state_tau_into_ele_from_h125) == 1 and \
           len(final_state_tau_into_mu_from_h125 ) == 1 :
            self.histograms['h1_channel'].Fill('em', weight)
            fill4vector(final_state_tau_into_mu_from_h125 [0], self.histograms, 'h1_em_mu_pt' , weight)
            fill4vector(final_state_tau_into_ele_from_h125[0], self.histograms, 'h1_em_ele_pt', weight)

        genjetsel = [jet for jet in genjets if jet.pt()>30 and abs(jet.eta())<5.]
        genjetsel = cleanCollection(genjetsel, gentau + genmu + genele)

        self.histograms['h1_njets'].Fill(len(genjetsel), weight)
        for i in xrange( min(len(genjetsel),2) ):
            fill4vector(genjetsel[i], self.histograms, 'h1_jet{I}_eta'.format(I=str(i+1)), weight)

        if len(genjetsel) >= 2:
            self.histograms['h1_delta_phi_jj'].Fill( deltaPhi( genjetsel[0], genjetsel[1] ) , weight)
            self.histograms['h1_delta_eta_jj'].Fill( abs( genjetsel[0].eta() - genjetsel[1].eta() ) , weight)
            self.histograms['h1_delta_r_jj'  ].Fill( deltaR  ( genjetsel[0], genjetsel[1] ) , weight)

        # just consider outgoing bquarks, i.e. about to hadronise, status 71
        # http://home.thep.lu.se/~torbjorn/pythia81html/ParticleProperties.html
        bquarks    = [p for p  in genparticles if abs(p.pdgId()) == 5 and p.status() == 71]
        genbjetsel = [jet for jet in genjets if jet.pt()>20 and abs(jet.eta())<2.4]

        bjets = 0
        bjets = cleanCollection(genbjetsel, bquarks, match = True)
        self.histograms['h1_nbjets'].Fill(len(bjets), weight)

        genmet = gennu[0].p4()
        for nu in gennu[1:]:
            genmet += nu.p4()
        self.histograms['h1_met_pt' ].Fill(genmet.pt() , weight)
        self.histograms['h1_met_phi'].Fill(genmet.phi(), weight)


        genlep_fromZ = [p for p in genparticles if p.mother() and abs(p.mother().pdgId()) == 23]
        genlep_fromh = [p for p in genparticles if p.mother() and abs(p.mother().pdgId()) == 25]

        if len(genlep_fromZ) != 2 or len(genlep_fromh) != 2:
            print 'ERROR'
            print 'Z has got %d daughters and h has got %d daughters' % (len(genlep_fromZ), len(genlep_fromh))
            raise

        # sum pt
        final_state_obj = genjetsel + genlep_fromZ + genlep_fromh
        sumPt = final_state_obj[0].pt()
        for obj in final_state_obj[1:]:
            sumPt += obj.pt()

        self.histograms['h1_sumpt'].Fill(sumPt, weight)

if __name__ == '__main__':

    analyzer = genAnalyzerMSSM_AZh(mass = 300,
        pathToFiles = '/afs/cern.ch/work/m/manzoni/mc-generation/CMSSW_7_1_13/src/MSSM_AZh_LLTauTau_PY8/300/first*k_*/HIG-RunIIWinter15GS-00003*.root',
#         pathToFiles = '/afs/cern.ch/work/m/manzoni/mc-generation/CMSSW_7_1_13/src/MSSM_AZh_LLTauTau_MG5_aMCNLO_2HDM4MG5/madgraph5/PROC_ggAZhlltt_mA300_HEFT/Events/run_01/EDM2GEN_PY8.root',
#         pathToFiles = '/afs/cern.ch/work/m/manzoni/mc-generation/CMSSW_7_1_13/src/MSSM_AZh_LLTauTau_MG5_aMCNLO_SusHi/madgraph5/PROC_GGH_HEFT/Events/run_04/EDM2GEN_PY8.root',
        extraTitle = 'PYTHIA8 A#rightarrowZh, h#rightarrow#tau#tau, m_{A}= 300 GeV, tan#beta = 2',
#         extraTitle = 'MG5_aMC A#rightarrowZh, h#rightarrow#tau#tau, m_{A}= 300 GeV, tan#beta = 2',
        maxEvents = -1)
    analyzer.loop()
    analyzer.saveHistos()

