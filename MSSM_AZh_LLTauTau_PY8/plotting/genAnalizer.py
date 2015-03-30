#! /usr/bin/env python

import ROOT
import sys
import os
from itertools import product
from DataFormats.FWLite import Events, Handle
from style import PlotStyle
from cmsTitle import CMS_lumi
from histograms import histograms


mass = '350'
histograms['h1_A_mass'] = ROOT.TH1F('h1_A_mass', '',  40,  int(mass)*0.95, int(mass)*1.05)
histograms['h1_A_mass'].SetMinimum(0.)
histograms['h1_A_mass'].SetLineWidth(2)
histograms['h1_A_mass'].SetLineColor(ROOT.kBlack)
histograms['h1_A_mass'].SetFillColor(ROOT.kOrange)
histograms['h1_A_mass'].SetMarkerStyle(8)
histograms['h1_A_mass'].SetFillStyle(3344)
histograms['h1_A_mass'].GetYaxis().SetTitle('events')
histograms['h1_A_mass'].GetYaxis().SetTitleOffset(1.6)
histograms['h1_A_mass'].GetXaxis().SetTitle('m_{A} [GeV]')
histograms['h1_A_mass'].GetXaxis().SetTitleOffset(1.3)

PlotStyle()
ROOT.gStyle.SetOptStat(1)
ROOT.gStyle.SetStatBorderSize(0)
ROOT.gStyle.SetOptStat('emr')


folder = 'mA'+mass
os.system('mkdir ' + folder)

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
                  '../{MASS}/first2k_1of20/HIG-RunIIWinter15GS-00003_1of20.root'  .format(MASS = mass),
                  '../{MASS}/first2k_2of20/HIG-RunIIWinter15GS-00003_2of20.root'  .format(MASS = mass),
                  '../{MASS}/first2k_3of20/HIG-RunIIWinter15GS-00003_3of20.root'  .format(MASS = mass),
                  '../{MASS}/first2k_4of20/HIG-RunIIWinter15GS-00003_4of20.root'  .format(MASS = mass),
                  '../{MASS}/first2k_5of20/HIG-RunIIWinter15GS-00003_5of20.root'  .format(MASS = mass),
                  '../{MASS}/first2k_6of20/HIG-RunIIWinter15GS-00003_6of20.root'  .format(MASS = mass),
                  '../{MASS}/first2k_7of20/HIG-RunIIWinter15GS-00003_7of20.root'  .format(MASS = mass),
                  '../{MASS}/first2k_8of20/HIG-RunIIWinter15GS-00003_8of20.root'  .format(MASS = mass),
                  '../{MASS}/first2k_9of20/HIG-RunIIWinter15GS-00003_9of20.root'  .format(MASS = mass),
                  '../{MASS}/first2k_10of20/HIG-RunIIWinter15GS-00003_10of20.root'.format(MASS = mass),
                  '../{MASS}/first2k_11of20/HIG-RunIIWinter15GS-00003_11of20.root'.format(MASS = mass),
                  '../{MASS}/first2k_12of20/HIG-RunIIWinter15GS-00003_12of20.root'.format(MASS = mass),
                  '../{MASS}/first2k_13of20/HIG-RunIIWinter15GS-00003_13of20.root'.format(MASS = mass),
                  '../{MASS}/first2k_14of20/HIG-RunIIWinter15GS-00003_14of20.root'.format(MASS = mass),
                  '../{MASS}/first2k_15of20/HIG-RunIIWinter15GS-00003_15of20.root'.format(MASS = mass),
                  '../{MASS}/first2k_16of20/HIG-RunIIWinter15GS-00003_16of20.root'.format(MASS = mass),
                  '../{MASS}/first2k_17of20/HIG-RunIIWinter15GS-00003_17of20.root'.format(MASS = mass),
                  '../{MASS}/first2k_18of20/HIG-RunIIWinter15GS-00003_18of20.root'.format(MASS = mass),
                  '../{MASS}/first2k_19of20/HIG-RunIIWinter15GS-00003_19of20.root'.format(MASS = mass),
                  '../{MASS}/first2k_20of20/HIG-RunIIWinter15GS-00003_20of20.root'.format(MASS = mass),
                  ])

handles = {}
handles['genParticles'] = [Handle('std::vector<reco::GenParticle>'), 'genParticles']
handles['ak4GenJets']   = [Handle('vector<reco::GenJet>'          ), 'ak4GenJets']

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

def tauDecayMode(tau):

    unstable = True

    dm = 'tau'
    final_daughter = tau

    while unstable:
        nod = tau.numberOfDaughters()
        for i in range(nod):
            dau = tau.daughter(i)
            if abs(dau.pdgId()) == 11 and dau.status() == 1:
                dm = 'ele'
                final_daughter = dau
                unstable = False
                break
            elif abs(dau.pdgId()) == 13 and dau.status() == 1:
                dm = 'muon'
                final_daughter = dau
                unstable = False
                break
            elif abs(dau.pdgId()) == 15: #taus may do bremsstrahlung
                dm = 'tau'
                final_daughter = dau
                tau = dau # check its daughters
                break
            elif abs(dau.pdgId()) not in (12, 14, 16):
                unstable = False
                break
            else:
                pass

    return dm, final_daughter

def deltaR(p1, p2):
    p1_vec = ROOT.TLorentzVector()
    p2_vec = ROOT.TLorentzVector()
    p1_vec.SetPtEtaPhiE(p1.p4().pt() ,
                        p1.p4().eta(),
                        p1.p4().phi(),
                        p1.p4().e()  )
    p2_vec.SetPtEtaPhiE(p2.p4().pt() ,
                        p2.p4().eta(),
                        p2.p4().phi(),
                        p2.p4().e()  )
    return p1_vec.DeltaR(p2_vec)

def deltaPhi(p1, p2):
    p1_vec = ROOT.TLorentzVector()
    p2_vec = ROOT.TLorentzVector()
    p1_vec.SetPtEtaPhiE(p1.p4().pt() ,
                        p1.p4().eta(),
                        p1.p4().phi(),
                        p1.p4().e()  )
    p2_vec.SetPtEtaPhiE(p2.p4().pt() ,
                        p2.p4().eta(),
                        p2.p4().phi(),
                        p2.p4().e()  )
    return p1_vec.DeltaPhi(p2_vec)

def cleanCollection(toBeCleaned, otherCollection, dR = 0.3, match = False):
    '''
    match returns a subset of elements of toBeCleaned that match
    with at least one element of otherCollection
    '''
    cleanedColl      = []
    jetsToRemove     = []
    matchedParticles = []
    for pair in product(toBeCleaned, otherCollection):
        if pair[0] in jetsToRemove or pair[1] in matchedParticles:
            continue
        p1_vec = ROOT.TLorentzVector()
        p2_vec = ROOT.TLorentzVector()
        p1_vec.SetPtEtaPhiE(pair[0].p4().pt() ,
                            pair[0].p4().eta(),
                            pair[0].p4().phi(),
                            pair[0].p4().e()  )
        p2_vec.SetPtEtaPhiE(pair[1].p4().pt() ,
                            pair[1].p4().eta(),
                            pair[1].p4().phi(),
                            pair[1].p4().e()  )
        if p1_vec.DeltaR(p2_vec) <= dR:
            jetsToRemove    .append(pair[0])
            matchedParticles.append(pair[1])
    if match:
        for jet in jetsToRemove:
            cleanedColl.append(jet)
    else:
        for jet in toBeCleaned:
            if jet in jetsToRemove:
                continue
            else:
                cleanedColl.append(jet)
    return list(set(cleanedColl))

def cosmetics():
    CMS_lumi(ROOT.gPad, 4, 0)
    stats = ROOT.gPad.GetPrimitive('stats')
    stats.SetY1NDC(0.82)
    stats.SetY2NDC(0.92)
    stats.SetX1NDC(0.72)
    stats.SetX2NDC(0.92)

for i, event in enumerate(events):

    #if i+1 > 5: break
    print i,']'

    event.getByLabel(handles['genParticles'][1], handles['genParticles'][0])
    genparticles = handles['genParticles'][0].product()

    event.getByLabel(handles['ak4GenJets'][1], handles['ak4GenJets'][0])
    genjets = handles['ak4GenJets'][0].product()

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
        raise

    for index in range(genZ[0].numberOfDaughters()):
        dau = genZ[0].daughter(index)
        if abs(dau.pdgId()) not in (11,13,15):
            import pdb ; pdb.set_trace()

    fill4vector(genA[0], histograms, 'h1_A_mass')
    fill4vector(genZ[0], histograms, 'h1_Z_mass')
    fill4vector(genh[0], histograms, 'h1_h_mass')

    if genA[0].daughter(0).pdgId() != 23 or \
       genA[0].daughter(1).pdgId() != 25:
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

    histograms['h1_delta_phi_ll'].Fill( deltaPhi( genh[0].daughter(0), genh[0].daughter(1) ) )
    histograms['h1_delta_eta_ll'].Fill( abs(genh[0].daughter(0).eta() - genh[0].daughter(1).eta()) )
    histograms['h1_delta_r_ll']  .Fill( deltaR  ( genh[0].daughter(0), genh[0].daughter(1) ) )

    if len(final_state_tau_into_had_from_h125) == 2 :
        histograms['h1_channel'].Fill('tt',1.)
        if final_state_tau_into_had_from_h125[0].pt() > final_state_tau_into_had_from_h125[1].pt():
            fill4vector(final_state_tau_into_had_from_h125[0], histograms, 'h1_tt_tau1_pt')
            fill4vector(final_state_tau_into_had_from_h125[1], histograms, 'h1_tt_tau2_pt')
        else:
            fill4vector(final_state_tau_into_had_from_h125[0], histograms, 'h1_tt_tau2_pt')
            fill4vector(final_state_tau_into_had_from_h125[1], histograms, 'h1_tt_tau1_pt')
    elif len(final_state_tau_into_had_from_h125) == 1 :
        if len(final_state_tau_into_mu_from_h125) == 1 :
            histograms['h1_channel'].Fill('mt',1.)
            fill4vector(final_state_tau_into_mu_from_h125 [0], histograms, 'h1_mt_mu_pt')
            fill4vector(final_state_tau_into_had_from_h125[0], histograms, 'h1_mt_tau_pt')
        elif len(final_state_tau_into_ele_from_h125) == 1 :
            histograms['h1_channel'].Fill('et',1.)
            fill4vector(final_state_tau_into_ele_from_h125[0], histograms, 'h1_et_ele_pt')
            fill4vector(final_state_tau_into_had_from_h125[0], histograms, 'h1_et_tau_pt')
    if len(final_state_tau_into_ele_from_h125) == 2 :
        histograms['h1_channel'].Fill('ee',1.)
        if final_state_tau_into_ele_from_h125[0].pt() > final_state_tau_into_ele_from_h125[1].pt():
            fill4vector(final_state_tau_into_ele_from_h125[0], histograms, 'h1_ee_ele1_pt')
            fill4vector(final_state_tau_into_ele_from_h125[1], histograms, 'h1_ee_ele2_pt')
        else:
            fill4vector(final_state_tau_into_ele_from_h125[0], histograms, 'h1_ee_ele2_pt')
            fill4vector(final_state_tau_into_ele_from_h125[1], histograms, 'h1_ee_ele1_pt')
    if len(final_state_tau_into_mu_from_h125) == 2 :
        histograms['h1_channel'].Fill('mm',1.)
        if final_state_tau_into_mu_from_h125[0].pt() > final_state_tau_into_mu_from_h125[1].pt():
            fill4vector(final_state_tau_into_mu_from_h125[0], histograms, 'h1_mm_mu1_pt')
            fill4vector(final_state_tau_into_mu_from_h125[1], histograms, 'h1_mm_mu2_pt')
        else:
            fill4vector(final_state_tau_into_mu_from_h125[0], histograms, 'h1_mm_mu2_pt')
            fill4vector(final_state_tau_into_mu_from_h125[1], histograms, 'h1_mm_mu1_pt')
    if len(final_state_tau_into_ele_from_h125) == 1 and \
       len(final_state_tau_into_mu_from_h125 ) == 1 :
        histograms['h1_channel'].Fill('em',1.)
        fill4vector(final_state_tau_into_mu_from_h125 [0], histograms, 'h1_em_mu_pt')
        fill4vector(final_state_tau_into_ele_from_h125[0], histograms, 'h1_em_ele_pt')

    genjetsel = [jet for jet in genjets if jet.pt()>30 and abs(jet.eta())<5.]
    genjetsel = cleanCollection(genjetsel, gentau + genmu + genele)

    histograms['h1_njets'].Fill(len(genjetsel))
    for i in xrange( min(len(genjetsel),2) ):
        fill4vector(genjetsel[i], histograms, 'h1_jet{I}_eta'.format(I=str(i+1)))

    if len(genjetsel) >= 2:
        histograms['h1_delta_phi_jj'].Fill( deltaPhi( genjetsel[0], genjetsel[1] ) )
        histograms['h1_delta_eta_jj'].Fill( abs( genjetsel[0].eta() - genjetsel[1].eta() ) )
        histograms['h1_delta_r_jj'  ].Fill( deltaR  ( genjetsel[0], genjetsel[1] ) )

    bquarks    = [p for p  in genparticles if abs(p.pdgId()) == 5]
    genbjetsel = [jet for jet in genjets if jet.pt()>20 and abs(jet.eta())<2.4]

    bjets = 0
    bjets = cleanCollection(genbjetsel, bquarks, match = True)
    histograms['h1_nbjets'].Fill(len(bjets))


    genmet = gennu[0].p4()
    for nu in gennu[1:]:
        genmet += nu.p4()
    histograms['h1_met_pt' ].Fill(genmet.pt() )
    histograms['h1_met_phi'].Fill(genmet.phi())


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

    histograms['h1_sumpt'].Fill(sumPt)


# make a canvas, draw, and save it
c1 = ROOT.TCanvas()

# for k in ['h1_A_mass', 'h1_Z_mass', 'h1_h_mass']:
for k in histograms.keys():
    histograms[k].Draw('HISTE')
    cosmetics()
    c1.Modified()
    c1.Update()
    c1.Print(folder+'/'+k+'.pdf')
    #c1.Print(folder+'/'+k+'.png')
