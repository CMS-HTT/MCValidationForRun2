import os

def getSLHA(mass):
    slha_file = open('SLHA-tables/mhmodp-LHCHXSWG-AZh-hTauTau-mA{MASS}-tanBeta2.slha'.format(MASS = mass))
    slha_string = ''
    for line in slha_file:
        slha_string += line.replace('\n','\\n')
    return slha_string


def modify_cfg(mass, file):
    slha_string = getSLHA(mass)
    file_cfg = open('{MASS}/{FILE}.py'    .format(MASS = mass, FILE = file.replace('.py',''))     )
    new_file = open('{MASS}/{FILE}_NEW.py'.format(MASS = mass, FILE = file.replace('.py','')), 'w')
    for line in file_cfg:
        if 'SLHATableForPythia8' in line:
            line_parts = line.rstrip().split('\'')
            new_line = '\''.join([line_parts[0], slha_string, line_parts[2]])
        elif '36:m0 = ' in line:
            line_parts = line.rstrip().split('\'')
            new_line = '\''.join([line_parts[0], '36:m0 = {MASS}'.format(MASS = mass), line_parts[2]])
        elif 'PhaseSpace:mHatMin = ' in line:
            line_parts = line.rstrip().split('\'')
            new_line = '\''.join([line_parts[0], 'PhaseSpace:mHatMin = {MASS}'.format(MASS = str(float(mass)*0.7)), line_parts[2]])
#         elif 'input = cms.untracked.int32(39)' in line:
#             new_line = line.rstrip().replace('39','1000')
#         elif 'nevts:39' in line:
#             new_line = line.rstrip().replace('39','1000')
        else:
            new_line = line.rstrip()
        print >> new_file, new_line
    file_cfg.close()
    new_file.close()
    os.system('mv {MASS}/{FILE}_NEW.py {MASS}/{FILE}.py'.format(MASS = mass, FILE = file.replace('.py','')))

folders = ['220', '240', '260', '280', '300', '320', '340', '350', '400']

for f in folders:
    os.system('cd {FOLDER} ; ln -s ../prepare-HIG-RunIIWinter15GS-00003.sh ; ln -s ../submitter.py ; bash prepare-HIG-RunIIWinter15GS-00003.sh ; rm -r CMSSW* ; cd -'.format(FOLDER = f))
    modify_cfg(f,'HIG-RunIIWinter15GS-00003_1_cfg.py')
    modify_cfg(f,'HIG-RunIIWinter15GS-00003_genvalid.py')
