from DataFormats.FWLite import Events, Handle
from ROOT import TFile, TH1F, TTree, gStyle, TH2F
import sys, math
import numpy as num
from DeltaR import *

gStyle.SetOptStat(11111)

argvs = sys.argv
argc = len(argvs)

if argc != 2:
    print 'Please specify the ID : python YutaTest.py <e.g. : HIG-RunIIWinter15GS-00006>'
    sys.exit(0)

rfile = argvs[1] + '/' + argvs[1] + '.root'
events = Events(rfile)
outfile = TFile(argvs[1] + '/ValidationTest_' + argvs[1] + '.root', 'recreate')
#rfile = argvs[1]
#events = Events(rfile)
#outfile = TFile(argvs[1].replace('.root','') + '_ValidationTest.root', 'recreate')

nbin = 10000

event_tree = TTree('per_event','per_event')
mother_tree = TTree('per_mother','per_mother')
decay_tree = TTree('per_decay','per_decay')
jet_tree = TTree('per_jet','per_jet')

event_nb = num.zeros(1, dtype=int)
event_nbgen = num.zeros(1, dtype=int)
event_njet = num.zeros(1, dtype=int)
event_met = num.zeros(1, dtype=float)
event_ljet = num.zeros(1, dtype=float)
event_sljet = num.zeros(1, dtype=float)

mother_inv = num.zeros(1, dtype=float)
mother_mass = num.zeros(1, dtype=float)
mother_pdg = num.zeros(1, dtype=float)
mother_pt = num.zeros(1, dtype=float)
mother_eta = num.zeros(1, dtype=float)
mother_phi = num.zeros(1, dtype=float)
mother_ndaughter = num.zeros(1, dtype=int)

decay_mother_m = num.zeros(1, dtype=float)
decay_pdgId = num.zeros(1, dtype=int)
decay_pt = num.zeros(1, dtype=float)
decay_eta = num.zeros(1, dtype=float)
decay_phi = num.zeros(1, dtype=float)

jet_pt = num.zeros(1, dtype=float)
jet_eta = num.zeros(1, dtype=float)
jet_phi = num.zeros(1, dtype=float)


event_tree.Branch('event_nb', event_nb, 'event_nb/I')
event_tree.Branch('event_nbgen', event_nbgen, 'event_nbgen/I')
event_tree.Branch('event_njet', event_njet, 'event_njet/I')
event_tree.Branch('event_met', event_met, 'event_met/D')
event_tree.Branch('event_ljet', event_ljet, 'event_ljet/D')
event_tree.Branch('event_sljet', event_sljet, 'event_sljet/D')

mother_tree.Branch('mother_pdg', mother_pdg, 'mother_pdg/D')
mother_tree.Branch('mother_pt', mother_pt, 'mother_pt/D')
mother_tree.Branch('mother_eta', mother_eta, 'mother_eta/D')
mother_tree.Branch('mother_phi', mother_phi, 'mother_phi/D')
mother_tree.Branch('mother_mass', mother_mass, 'mother_mass/D')
mother_tree.Branch('mother_inv', mother_inv, 'mother_inv/D')
mother_tree.Branch('mother_ndaughter', mother_ndaughter, 'mother_ndaughter/I')

decay_tree.Branch('decay_mother_m', decay_mother_m, 'decay_mother_m/D')
decay_tree.Branch('decay_pdgId', decay_pdgId, 'decay_pdgId/I')
decay_tree.Branch('decay_pt', decay_pt, 'decay_pt/D')
decay_tree.Branch('decay_eta', decay_eta, 'decay_eta/D')
decay_tree.Branch('decay_phi', decay_phi, 'decay_phi/D')

jet_tree.Branch('jet_pt', jet_pt, 'jet_pt/D')
jet_tree.Branch('jet_eta', jet_eta, 'jet_eta/D')
jet_tree.Branch('jet_phi', jet_phi, 'jet_phi/D')


h_decayA = TH1F("h_decayA","h_decayA",60,-30,30)
h_decayH = TH1F("h_decayH","h_decayH",60,-30,30)
h_decayh = TH1F("h_decayh","h_decayh",60,-30,30)
h_decayZ = TH1F("h_decayZ","h_decayZ",60,-30,30)


handle  = Handle ('std::vector<reco::GenParticle>')
label = ("genParticles")
handle_jet = Handle('std::vector<reco::GenJet>')
label_jet = ("ak5GenJets")
handle_met = Handle('vector<reco::GenMET>')
label_met = ("genMetTrue")

def isFinal(p):
    return not (p.numberOfDaughters() == 1 and p.daughter(0).pdgId() == p.pdgId())

def finalDaughters(particle, daughters):
    '''Fills daughters with all the daughters of particle.
    Recursive function.'''
    if particle.numberOfDaughters() == 0:
        daughters.append(particle)
    else:
        foundDaughter = False
        for i in range( particle.numberOfDaughters() ):
            dau = GenParticle(particle.daughter(i))
            if dau.status() >= 2:
                daughters = finalDaughters( dau, daughters )
                foundDaughter = True
        if not foundDaughter:
            daughters.append(particle)

    return daughters



evtid = 0

for ev in events:

    evtid += 1

    ev.getByLabel(label, handle)
    gps = handle.product()

    ev.getByLabel(label_jet, handle_jet)
    jet = handle_jet.product()

    ev.getByLabel(label_met, handle_met)
    met = handle_met.product()


    gps_mother = [p for p in gps if isFinal(p) and abs(p.pdgId()) in [23, 25, 35, 36]]
    gps_b = [p for p in gps if isFinal(p) and abs(p.pdgId())==5 and p.status()==71 and p.pt() > 20 and abs(p.eta()) < 2.5]
    gps_bgen = [p for p in gps if isFinal(p) and abs(p.pdgId())==5 and p.status()==71]
    gps_tau = [p for p in gps if isFinal(p) and abs(p.pdgId())==15]
    gps_lep = [p for p in gps if isFinal(p) and abs(p.pdgId()) in [11,13,15]]

#    print 'before = ', len(jet)
    # overlap removal between leptons
    jet, dummy = cleanObjectCollection(jet, masks = gps_lep, deltaRMin = 0.5)
#    print 'after = ', len(jet)
    

    counter_jet = 0
#    import pdb; pdb.set_trace()
    for ijet in jet:
        if ijet.pt() > 30 and abs(ijet.eta()) <5:
            jet_pt[0] = ijet.pt()
            jet_eta[0] = ijet.eta()
            jet_phi[0] = ijet.phi()
            jet_tree.Fill()
    
            counter_jet += 1

    event_nb[0] = len(gps_b)
    event_nbgen[0] = len(gps_bgen)
    event_njet[0] = counter_jet
    event_met[0] = met[0].pt()

    if(len(jet)>=2):
        event_ljet[0] = jet[0].pt()
        event_sljet[0] = jet[1].pt()    
    elif (len(jet)==1):
        event_ljet[0] = jet[0].pt()
        event_sljet[0] = -1
    else:
        event_ljet[0] = -1
        event_sljet[0] = -1


    event_tree.Fill()


    for p in gps_mother:       
        
        nother = 0
        pair = []


        for i in range(p.numberOfDaughters()):

#            if abs(p.mass()-1000) > 100: continue

            pair.append(p.daughter(i).p4())

            decay_mother_m[0] = p.mass()
            decay_pdgId[0] = p.daughter(i).pdgId()
            decay_pt[0] = p.daughter(i).pt()
            decay_eta[0] = p.daughter(i).eta()
            decay_phi[0] = p.daughter(i).phi()
            decay_tree.Fill()

            if p.pdgId()==25:
                h_decayh.Fill(p.daughter(i).pdgId())
            elif p.pdgId()==35:
                h_decayH.Fill(p.daughter(i).pdgId())
            elif p.pdgId()==36:
                h_decayA.Fill(p.daughter(i).pdgId())
            elif p.pdgId()==23:
                h_decayZ.Fill(p.daughter(i).pdgId())

        if(len(pair)==2):
            inv = (pair[0] + pair[1]).mass()
            mother_inv[0] = inv
        else:
            mother_inv[0] = -1


        mother_pdg[0] = p.pdgId()
        mother_mass[0] = p.mass()
        mother_pt[0] = p.pt()
        mother_eta[0] = p.eta()
        mother_phi[0] = p.phi()
        mother_ndaughter[0] = len(pair)

        mother_tree.Fill()
        







print evtid, 'events processed for', argvs[1]


outfile.Write()
outfile.Close()
