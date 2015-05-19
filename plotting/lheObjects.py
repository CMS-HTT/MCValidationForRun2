import ROOT

class Event(object):
    '''
    LesHouches event class.
    Based on http://arxiv.org/pdf/hep-ph/0609017v1.pdf
    '''
    def __init__(self, evtext, weights_dict):
        self.particles = []
        self._textToObj(evtext)
        self._setWeights(weights_dict)
    
    def _textToObj(self, evtext):
        
        lines = evtext.split('\n')
        lines = lines[1:]
        
        # event-wise quantities
        self.nup    = int  (lines[0].split()[0]) # number of particles
        self.idprup = float(lines[0].split()[1]) # ??
        self.xwgtup = float(lines[0].split()[2]) # event weight
        self.scalup = float(lines[0].split()[3]) # scale
        self.aqedup = float(lines[0].split()[4]) # alpha qed
        self.aqcdup = float(lines[0].split()[5]) # alpha qcd
        
        # loop on the number of partons
        for position, line in enumerate(lines[1:self.nup+1]):
            particle = Particle(line)
            particle.position = position + 1
            self.particles.append(particle)
            
    def _setWeights(self, weight_dict):
        for k, v in weight_dict.items():
            setattr(self, 'weight_'+k, v)
            
class Particle(object):
    '''
    LesHouches particle class.
    Based on http://arxiv.org/pdf/hep-ph/0609017v1.pdf
    '''
    def __init__(self, lhe_line):
        # Position in the event, useful for lineage reconstruction.
        # To be set from an Event
        lhe_line = lhe_line.replace('\n','')
        self.position = -1 
        self._textToObj(lhe_line)
        
        self.p4 = ROOT.TLorentzVector()
        self.p4.SetPxPyPzE(
          self.pup1,
          self.pup2,
          self.pup3,
          self.pup4
        )
    
    def _textToObj(self, lhe_line):
        self.idup    = int  (lhe_line.split()[ 0]) # pdgID
        self.istup   = int  (lhe_line.split()[ 1]) # ??
        self.mothup1 = int  (lhe_line.split()[ 2]) # first mother position
        self.mothup2 = int  (lhe_line.split()[ 3]) # second mother position
        self.icolup1 = float(lhe_line.split()[ 4]) # colour1
        self.icolup2 = float(lhe_line.split()[ 5]) # colour2
        self.pup1    = float(lhe_line.split()[ 6]) # px
        self.pup2    = float(lhe_line.split()[ 7]) # py
        self.pup3    = float(lhe_line.split()[ 8]) # pz
        self.pup4    = float(lhe_line.split()[ 9]) # energy
        self.pup5    = float(lhe_line.split()[10]) # mass
        self.vtimup  = float(lhe_line.split()[11]) # does produce a secondary vertex? default 0 
        self.spinup  = float(lhe_line.split()[12]) # spin. Default 9 means no spin information
