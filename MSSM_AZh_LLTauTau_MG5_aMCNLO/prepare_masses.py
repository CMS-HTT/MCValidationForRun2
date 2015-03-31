masses = [
          '220',
          '240',
          '260',
          '280',
          '300',
          '320',
          '340',
          '350',
          '400',
         ]

for mass in masses:
    file_dat_mass     = open('proc_card_mA{MASS}_hm.dat'.format(MASS = mass), 'w')
    file_dat_template = open('proc_card_hm.dat')
    for line in file_dat_template:
        if 'PROC_MSSM_AZH' in line:
            line = line.replace('PROC_MSSM_AZH','PROC_MSSM_AZH_'+mass) 
        line = line.rstrip()
        print >> file_dat_mass, line
    file_dat_mass     .close()
    file_dat_template.close()

