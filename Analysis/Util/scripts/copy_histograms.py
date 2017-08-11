
import os

import ROOT
from argparse import ArgumentParser

parser = ArgumentParser(description='')
    
parser.add_argument('--file', dest='file', default=None, help='list of input files (comma separated).')

parser.add_argument('--output', dest='output', default=None, help='output file')

options = parser.parse_args()


hists = []

def main() :

    file = ROOT.TFile.Open(options.file, 'READ')

    hists = []
    for top, dirs, objs in walk_root( file ) :
        print 'TOP = ', top 
        print 'dirs'
        print dirs
        print 'Objs'
        print objs
        for objname in objs :
            obj = file.Get(top+'/'+objname)
            if isinstance( obj, ROOT.TH1 ) :
                hists.append( top+'/'+objname)

    print hists

    copy_to_eos = False
    if options.output[0:4] == '/eos' :
        copy_to_eos = True

    if copy_to_eos :
        outfile = ROOT.TFile.Open('/tmp/histograms.root', 'RECREATE')
    else :
        outfile = ROOT.TFile.Open(options.output, 'RECREATE')

    for hist in hists :
        histdirs = hist.split('/')
        dir_path = ''
        for dir in histdirs[0:-1] :
            dir_path += dir +'/'
            outfile.mkdir(dir_path)
            
        outfile.cd(dir_path)
        outhist = file.Get(hist)
        outhist.Write()

    outfile.Write()

    outfile.Close()

    if copy_to_eos :
        os.system('/afs/cern.ch/project/eos/installation/0.3.4/bin/eos.select cp /tmp/histograms.root %s/histograms.root' %options.output ) 
        




def walk_root( path ) :

    top, dirs, objs = parse_root_dir( path )

    yield top, dirs, objs
    if len(dirs) > 0 :
        for dir in dirs :
            for new_top, new_dirs, new_objs in walk_root( path.Get(dir )) :
                yield new_top, new_dirs, new_objs



def parse_root_dir( path ) :
    dirs = []
    objs = []
    top = ''
    if isinstance( path, ROOT.TFile ) or isinstance( path, ROOT.TXNetFile ) :
        top = ''
    elif isinstance(path, ROOT.TDirectory ) :
        top = path.GetName()
    
    for objkey in path.GetListOfKeys() :
        obj = objkey.ReadObj()
        if isinstance(obj, ROOT.TDirectoryFile ) :
            dirs.append(obj.GetName())
        else :
            objs.append(obj.GetName())

    return top, dirs, objs

        

main()
    
