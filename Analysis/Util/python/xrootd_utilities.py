import subprocess 
import os
import sys
import time
import pwd

def x509():
    "Helper function to get x509 either from env or tmp file"
    proxy = os.environ.get('X509_USER_PROXY', '')
    if  not proxy:
        proxy = '/tmp/x509up_u%s' % pwd.getpwuid( os.getuid() ).pw_uid
        if  not os.path.isfile(proxy):
            return ''
    return proxy

#---------------------------------------------------------
def copy_xrd_to_local(url, remote_path, local_path) :

    cmd = ['xrdcp', "root://%s//%s"%(url,remote_path), local_path]
    result = subprocess.Popen(cmd, stdout=subprocess.PIPE,stderr=subprocess.PIPE,shell=True).communicate()[0]

#---------------------------------------------------------
def copy_local_to_xrd(url, remote_path, local_path) :

    cmd = ['xrdcp', local_path, "root://%s//%s"%(url,remote_path)]
    result = subprocess.Popen(cmd, stdout=subprocess.PIPE,stderr=subprocess.PIPE,shell=True).communicate()[0]

#---------------------------------------------------------
def xrdrm(url, path) :

    cmd = [ 'xrdfs', url ,'rm', path]
    result = subprocess.Popen(cmd, stdout=subprocess.PIPE,stderr=subprocess.PIPE, shell=True).communicate()[0]

#---------------------------------------------------------
def walk_xrd(url,path) :

    dirs, files, sizes = parse_xrd_dir(url,path)
    yield path, dirs, files, sizes
    for d in dirs :
        for new_path, new_dirs, new_files, new_sizes in walk_xrd(url,d) :
            yield new_path, new_dirs, new_files, new_sizes
    for f,s in zip(files,sizes):
      if s<500 and s>10 and ".root" not in f and ".txt" not in f:
        ## possibly a soft link
        for new_path, new_dirs, new_files, new_sizes in walk_xrd(url,f) :
            yield new_path, new_dirs, new_files, new_sizes


#---------------------------------------------------------
def parse_xrd_dir(url, path, DEBUG=False) :
    
    # remove leading xrootd for using xrd dirlist
    #res = re.match('/xrootd/(.*)', path)
    #if res is not None :
    #    path = res.group(1)
    directories = []
    files = [] 
    sizes = []

    #print 'PATH = ', path

    #print "xrd hn.at3f dirlist "+path
    #lines = os.popen("xrd hn.at3f dirlist "+path).readlines()
    #output = str("").join(lines)


    # get directory contents
#    cmd = ['xrdfs',url, 'ls -l', path+'/']
    cmd = ['xrdfs %s ls -l %s/' %(url,path)]
    print cmd
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=None,bufsize=-1,shell=True)
    # p.wait() hangs indefinately on large directories
    # (this is a known issue https://docs.python.org/2/library/subprocess.html#subprocess.Popen.wait)
    # so instead, just use a short sleep to 
    # ensure the command has completed
    #time.sleep(2)
    #p.wait()
    result = p.communicate()[0]
    p.stdout.close()

    result_lines = result.rstrip('\n').split('\n')

    if len(result_lines) == 0 :
        return directories, files
    for line in result_lines :

        if DEBUG :
            print "Line is"
            print line

        splitline = [line[:4]]+line[24:].split()

        if len(splitline) != 3 :
            if line :
                print 'Cannot parse line :'
                print splitline
                print line
                print 'Here is the path'
                print path 
                print 'Here is the full entry'
                print result
            break
            continue

        obj = splitline[2]
        isdir = (splitline[0][0] == 'd')
        size = splitline[1]

        if isdir :
            directories.append(obj)
        else :
            files.append(obj)
            sizes.append( int(size) )
        
    return directories, files, sizes

