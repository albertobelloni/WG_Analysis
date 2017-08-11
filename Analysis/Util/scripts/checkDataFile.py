#!/usr/bin/env python

from argparse import ArgumentParser
import os

p = ArgumentParser()

p.add_argument( '--file', dest = 'file', default = None, help    = 'path to ROOT file' )

p.add_argument( '--treeName', dest = 'treeName', default = None, help    = 'name of tree ( if none given, use the first tree found in the root directory of the file)' )

p.add_argument( '--nPrint', dest = 'nPrint', type=int,  default=30, help = 'Print N largest branches' )

options = p.parse_args() 

#-------------------------------------------------------------------------
class Branch:

    def __init__(self):
        self.name  = ''
        self.names = []
        self.key   = ''
        self.bytes_zip = 0
        self.bytes_tot = 0

#-------------------------------------------------------------------------
def get_branch(rtree, parent=None, option = 'top'):

    nleaf = rtree.GetListOfLeaves().GetEntries()
    blist = []

    curr_tree = None
    if parent is None :
        curr_tree = rtree
    else :
        for leaf in rtree.GetListOfLeaves() :
            br = leaf.GetBranch()
            if br.GetName() == parent :
                curr_tree = br

    if curr_tree is None :
        print 'get_branch - parent tree not found'
        return blist

    print curr_tree

    for lf in curr_tree.GetListOfLeaves() :
        br = lf.GetBranch()

        b = Branch()
        b.name      = br.GetName()
        b.bytes_zip = br.GetZipBytes()
        b.bytes_tot = br.GetTotBytes()        

        dlist = b.name.split('.')

        b.key = b.name

        if option.count('top'):

            append = True
            for j in range(0, len(blist)):
                if blist[j].key == b.key:
                    blist[j].bytes_zip += b.bytes_zip
                    blist[j].bytes_tot += b.bytes_tot
                    blist[j].names.append(b.name)
                    append = False
            if append:
                blist.append(b)    
        else:
            blist.append(b)

    return blist


#-------------------------------------------------------------------------
def compare_branch(x, y):
        return int(y.bytes_zip - x.bytes_zip)

#-------------------------------------------------------------------------
def get_status(file, treeName, nPrint):

    import ROOT
    
    rfile = ROOT.TFile.Open(file)

    tree = rfile.Get(treeName)

    if tree is None :
        print 'Did not get tree %s' %treeName
        return

    print 'Event tree has ',tree.GetEntries(),'entries'

    if tree.GetEntries() < 1:
        return

    branches = sorted(get_branch(tree), cmp = compare_branch)

    sum_zip_size = 0.0
    sum_tot_size = 0.0
    entries      = float(tree.GetEntries())
    
    for i in range(0, len(branches)):
        sum_zip_size += branches[i].bytes_zip
        sum_tot_size += branches[i].bytes_tot

    print 'Average zip size per event: %.1f' %(sum_zip_size/entries)
    print 'Average zip size per branch:'

    sum_size = 0.0
    
    for i in range(0, min(len(branches), nPrint)):
        b = branches[i]
        s = b.bytes_zip/entries        
        sum_size += b.bytes_zip
        
        print '  %.1f %s' %(s, b.key)

    print 'Average zip size per event for top %d branches: %.1f' %(nPrint, sum_size/entries)
    rfile.Close()

###########################################################################
# Main function for command line execuation
#
if __name__ == '__main__': 

    if options.file != None :
        get_status(**vars(options))
    else:        
        p.error('Missing input ROOT file')
