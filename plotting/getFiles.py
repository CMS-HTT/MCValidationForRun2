import glob
import os
import subprocess


def eos_command():

  shell = os.getenv('SHELL')
  cmd = subprocess.Popen(shell+' -c "which eos"', shell=True, stdout=subprocess.PIPE)

  for i, line in enumerate(cmd.stdout):
      if i > 0 : break
      eos = line.split(' ')[-1].rstrip()

  return eos


def get_eos_files(path):

    eos = eos_command()
    list_files_cmd = '{EOS} ls {PATH}'.format(EOS = eos, PATH = path)
    cmd = subprocess.Popen(list_files_cmd, shell = True,
                           stdout = subprocess.PIPE)
    files = []

    for i, line in enumerate(cmd.stdout):
        file = line.split(' ')[-1].rstrip()
        if '.root' not in file :
            continue
        files.append('/'.join([path, file]))

    return files


def get_afs_files(path):
    '''
    accepts wildcards too, e.g.
    PATH1/*PATH2*/CommonString*.root
    '''
    allfiles = glob.glob(path)
    files = []
    for f in allfiles:
        if f.endswith('.root'):
            files.append(f)
    return files


def get_files(path):

    if path.startswith('/store'):
        return get_eos_files(path)
    else:
        return get_afs_files(path)

if __name__ == '__main__':
    for file in get_files('/store/relval/CMSSW_7_3_0/RelValQQH1352T_Tauola_13/GEN-SIM-DIGI-RAW-HLTDEBUG/PU25ns_MCRUN2_73_V7-v1/00000/'):
        print file

