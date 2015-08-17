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
                                
                block = Block(line)
                
                k = i
                                
                for j, indentline in enumerate(self.content[i+1:]):    
                    
                    if indentline.startswith((' ', '\t')) and \
                       len(indentline) > 2:

                        it = BlockItem(indentline)
                        block.blockItems += [it]

                    elif indentline.startswith('#'):
                        pass

                    elif line.startswith( ('block', 
                                           'Block',
                                           'BLOCK',
                                           'decay',
                                           'Decay',
                                           'DECAY') ):
                        break
                        
                self.blocks[block.name] = block
                                     
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
    
#     def Diff(self, paramCard):
#         '''
#         Compare the blocks and the decays between two different parameter cards.
#         '''
#         
#         our_blocks   = self     .blocks
#         their_blocks = paramCard.blocks
# 
#         our_decays   = self     .decays
#         their_decays = paramCard.decays
#         
#         blocksToModify = {}
#         decaysToModify = {}
#         
#         # First check if there's something completely missing in their param_card
#         our_blocks_set   = set( [i.lower() for our_blocks  .keys()] )
#         their_blocks_set = set( [i.lower() for their_blocks.keys()] )
#         
#         # RIC: this method is unfinished, leave it for later

    def Print(self):
        for v in self.blocks.values() + self.decays.values():
            v.Print()        

    def PrintCustom(self):
        '''
        Use this module to produce the customized card needed for the gridpack.
        '''
        # In principle it'd be better to have a diff fucntion wrt a reference param card

        for v in self.blocks.values():
            for i in v.blockItems:
                print 'set param_card {BLOCK} {ID} {VALUE}' \
                      ''.format(BLOCK = v.name, 
                                ID    = ' '.join([str(id) for id in i.id]),
                                VALUE = i.value)

        for v in self.decays.values():
            for i in v.decayModes:
                print 'set param_card {DECAY} {PDGID} {WIDTH} ' \
                      ''.format(DECAY = v.pdgId, 
                                PDGID = v.pdgId,
                                WIDTH = v.width)
        

class Block(object):
    '''
    '''
    def __init__(self, line = ''):

        self.name    = 'dummy'
        self.comment = ''
        
        if len(line):
            if len(line.split('#')[0].split()) > 2:
                self.name    = line.split()[1] + ' ' + line.split()[2]
            else:
                self.name    = line.split()[1]
            if len(line.split('#')) > 1:
                self.comment = line.split('#')[-1]
        
        self.blockItems = []
    
    def Print(self):
        print '\t'.join(['Block', self.name,'#'*(len(self.comment) > 0)+self.comment])
        for it in self.blockItems:
            it.Print()


class BlockItem(object):
    '''
    '''
    def __init__(self, line = ''):

        self.id      = tuple()
        self.value   = None
        self.comment = ''
        
        if len(line):
            brokenline = line.split('#')
            self.id      = tuple( [int(i) for i in brokenline[0].split()[:-1]] )
            self.value   = float(brokenline[0].split()[-1])
            if len(brokenline) > 1:
                self.comment = brokenline[-1]

    def Print(self):
        toPrint = [''] + ['  ' + str(id) for id in self.id] + \
                  [str(self.value), '#'*(len(self.comment) > 0) + self.comment]
        
        try:
            print '\t'.join(toPrint)
        except:
            import pdb ; pdb.set_trace()


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
        print '\t'.join(['DECAY', str(self.pdgId), str(self.width), '#'*(len(self.comment) > 0)+self.comment])
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
    defaultpc = ParamCard('../../../../CMSSW_7_1_13/src/MSSM_AZh_LLTauTau_MG5_aMCNLO_2HDM4MG5/madgraph5/PROC_ggAZhlltt_mA300_HEFT/Cards/param_card_default.dat')
#     mypc.Print()
#     mypc.PrintCustom()

