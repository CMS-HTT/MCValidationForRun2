#!/usr/bin/python

class ParamCard(object):
    '''
    '''
    def __init__(self, paramcard):
        
        self.blocks = {}
        self.decays = {}

        self.paramcard = paramcard
        
        with open(paramcard) as f:
            self.content = f.read().splitlines()
        
        f.close()
        
        self._readCard()
    
    def _readCard(self):
        self._readBlocks()
        self._readDecays() 
    
    def _readBlocks(self):
        
        i = j = k = -1
        
        for i, line in enumerate(self.content):
            
            if i <= k + j:
                continue
            
            if line.startswith( ('block', 'Block', 'BLOCK') ):                
                                
                k = i
                
                blockvalues = []
                
                for j, indentline in enumerate(self.content[i+1:]):    
                    
                    if indentline.startswith((' ', '\t')) and \
                       len(indentline) > 2:
                       
                        # split the line in key & value and comment
                        value   = indentline.split('#')[0]
                        comment = indentline.split('#')[1]
                        
                        blockvalues += [ (value, comment) ]

                    elif indentline.startswith('#'):
                        pass

                    elif line.startswith( ('block', 
                                           'Block',
                                           'BLOCK',
                                           'decay',
                                           'Decay',
                                           'DECAY') ):
                        break
                        
                blockType = line.split()[1]
                self.blocks[blockType] = blockvalues
                    
                        
    def _readDecays(self):
        
        i = j = k = -1
        
        for i, line in enumerate(self.content):
            
            if i <= k + j:
                continue
            
            if line.startswith( ('decay', 'Decay', 'DECAY') ):                
                
                decay = Decay(line)                
                
                k = i
                                
                for j, indentline in enumerate(self.content[i+1:]):    
                    
                    if indentline.startswith((' ', '\t')) and \
                       len(indentline) > 2:
                       
                        dm = DecayMode(indentline)
                        decay.decayModes += [dm]

                    elif indentline.startswith('#'):
                        pass

                    elif line.startswith( ('block', 
                                           'Block',
                                           'BLOCK',
                                           'decay',
                                           'Decay',
                                           'DECAY') ):
                        break
                        
                self.decays[decay.pdgId] = decay
    
    def Print(self):
        for k, v in self.blocks.items():
            print 'Block', k
            for i in v:
                print '\t', i[0], '#', i[1]

        for v in self.decays.values():
            v.Print()        
    

class Block(object):
    '''
    It would be nice if this was implemented.
    Child classes are welcome too.
    '''


class Decay(object):
    '''
    '''
    def __init__(self, line = ''):
        
        if len(line):
            self.pdgId   = int  (line.split()[1])
            self.width   = float(line.split()[2])
            self.comment = line.split('#')[1]
        
        else:
            self.pdgId   = -1
            self.width   = -1.
            self.comment = 'dummy'
        
        self.decayModes = []
    
    def Print(self):
        print '\t'.join(['DECAY', str(self.pdgId), str(self.width), '#'+str(self.comment)])
        for dm in self.decayModes:
            dm.Print()


class DecayMode(object):
    '''
    '''
    def __init__(self, line = ''):   
        
        if len(line):
            self.br  = float( line.split()[0] )
            self.nda = int  ( line.split()[1] )
            self.id1 = int  ( line.split()[2] )
            self.id2 = int  ( line.split()[3] )

        else:
            self.br  = -1.
            self.nda = -1.
            self.id1 = None
            self.id2 = None
    
    def Print(self):
        print '\t'.join(['', str(self.br), str(self.nda), str(self.id1), str(self.id2)])


if __name__ == '__main__':
    mypc = ParamCard('../param_cards/param_card_mA300.dat')
    mypc.Print()
