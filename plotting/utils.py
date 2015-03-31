import ROOT
from itertools import product

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

def cosmetics(header):
    header.CMS_lumi(ROOT.gPad, 4, 0)
    stats = ROOT.gPad.GetPrimitive('stats')
    #stats.SetY1NDC(0.82)
    #stats.SetY2NDC(0.92)
    #stats.SetX1NDC(0.72)
    #stats.SetX2NDC(0.92)
