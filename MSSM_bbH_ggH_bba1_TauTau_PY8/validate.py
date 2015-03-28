from subprocess import call
import sys


def reshape(filename):
    f = open(filename, 'r')
    wfile = open('tmp', 'w')

    for line in f:
        
        str = line
        
        if str.find('nothing')!=-1:
            continue

        if str.find('step2')!=-1:
            continue
        
        str = str.replace('GEN,SIM','GEN')

        if str.find('no_exec')!=-1:

            chunk = str.split()
#            print chunk

            index = -1
            for ii, ichunk in enumerate(chunk):
                if ichunk == '-n':
                    index = ii

            nevt = chunk[index+1]
            print 'Check', index, nevt
            str = str.replace('-n ' + nevt, '-n 1000')
            
        wfile.write(str)

        
    f.close()

    cmd = 'mv tmp ' + filename
    call(cmd, shell=True)




argvs = sys.argv
argc = len(argvs)

if argc != 2:
    print 'Please specify the ID : python validate.py <e.g. : HIG-RunIIWinter15GS-00006>'
    sys.exit(0)


id = argvs[1]
cmd = 'wget https://cms-pdmv.cern.ch/mcm/public/restapi/requests/get_setup/' + id
call(cmd, shell=True)

script = id + '.sh'
call('mv ' + id + ' ' + script, shell=True)
reshape(script)
call('mkdir ' + id, shell=True)
call('mv ' + script + ' ' + id + '/', shell=True)
#call('cd ' + id, shell=True)
#call('source ' + id + '/' + script)
#call('cmsRun ' + id + '_1_cfg.py')
