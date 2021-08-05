/*
 * =====================================================================================
 *
 *       Filename:  readTFileContent.C
 *
 *    Description:  
 *
 *        Version:  1.0
 *        Created:  02/27/18 07:39:50
 *       Revision:  none
 *       Compiler:  gcc
 *
 *         Author:  Kak Wong  
 *   Organization:  UMD
 *
 * =====================================================================================
 */
#include <stdlib.h>

#include"TFile.h"
#include"TTree.h"

void scanTFileContent(std::string c) {
	TFile* f = TFile::Open(c.c_str());
	TTree* t =  (TTree*)f->Get("UMDNTuple/EventTree");

    t->SetScanField(100);
	t->Scan("*");
}

