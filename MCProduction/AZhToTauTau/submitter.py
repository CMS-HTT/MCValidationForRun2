import os
from optparse import OptionParser

parser = OptionParser()

parser.add_option('-Q', '--queue' , dest = 'queue' , help = 'choose queue. Available 1nh 8nh 1nd 2nd 1nw 2nw. Default is 1nd' , default = '8nh' )
parser.add_option('-E', '--events', dest = 'events', help = 'events to produce, in hundreds, e.g. pass 20 to get 2000 events' ,                 )
parser.add_option('-P', '--prefix', dest = 'prefix', help = 'folders will start with prefix. Default empty'                   , default = ''    )
parser.add_option('-S', '--submit', dest = 'submit', help = 'if False, it only creates the folder structure. Default True'    , default = True  )

(options,args) = parser.parse_args()

for i in range(int(options.events)):

    appendix = '{I}of{TOT}'.format(I = str(i+1), TOT = str(int(options.events)))

    os.system('mkdir '+options.prefix+'_'+appendix)
    os.chdir(options.prefix+'_'+appendix)

    file_cfg = open('../HIG-RunIIWinter15GS-00003_1_cfg.py')
    new_file = open('HIG-RunIIWinter15GS-00003_1_'+appendix+'_cfg.py','w')
    for line in file_cfg:
        if 'file:HIG-RunIIWinter15GS-00003.root' in line:
            line_parts = line.rstrip().split('\'')
            new_line = line.rstrip().replace('.root','_'+appendix+'.root')
        else:
            new_line = line.rstrip()
        print >> new_file, new_line
    file_cfg.close()
    new_file.close()

    batch_script = open('batchscript.sh','w')
    print >> batch_script, '#!/bin/bash\n\
export SCRAM_ARCH=slc6_amd64_gcc481\n\
W_DIR="{CURRENT}"\n\
cd $W_DIR\n\
eval `scramv1 ru -sh`\n\
echo "running"\n\
cmsRun {NEW_CFG}'.format(CURRENT = os.getcwd(), NEW_CFG = 'HIG-RunIIWinter15GS-00003_1_'+appendix+'_cfg.py')
    batch_script.close()

    os.system('chmod 775 batchscript.sh')

    if options.submit:
        os.system('/afs/cern.ch/cms/caf/scripts/cmsbsub -q {QUEUE} -u lakjshdlaks batchscript.sh'.format(QUEUE=options.queue))

    os.chdir('..')
