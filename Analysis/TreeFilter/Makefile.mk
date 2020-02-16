###############################################################################
# 
# Makefile 
#
# Author : Josh Kunkle jkunkle@cern.ch
#
# Compile the local package and link to the Core package
#
################################################################################
#
#CXX     = g++
#LD      = g++
#
#BIN_DIR = .
#OBJ_DIR = obj
#SRC_DIR = src
#INC_DIR = include
#
#ROOTCINT     = rootcling
#ROOTCONFIG   = root-config
#
#BOOST_VER    = 1.57.0-ikhhed
#
#ROOTCXXFLAGS = $(shell $(ROOTCONFIG) --cflags)
#BOOSTFLAGS   = \
#	-I/cvmfs/cms.cern.ch/$(SCRAM_ARCH)/external/boost/$(BOOST_VER)/include\
#	-L/cvmfs/cms.cern.ch/$(SCRAM_ARCH)/external/boost/$(BOOST_VER)/lib
#
#ROOTLIBS     = $(shell $(ROOTCONFIG) --libs) -lTreePlayer -lTMVA -lRooFit
#LIBS         = $(ROOTLIBS) $(BOOSTFLAGS) -lboost_filesystem -lboost_system
#
#
#DEBUG        = false
#INCLUDE      = $(ROOTCXXFLAGS) $(BOOSTFLAGS)
#
## Activate debug compilation with:
## %> make DEBUG=true
#ifeq ($(DEBUG),true)
#	CXXFLAGS     = -O0 -Wall -ggdb -fPIC -I$(INC_DIR) $(INCLUDE)
#	LDFLAGS      = -O0 -Wall -ggdb -I$(INC_DIR) $(INCLUDE) 
#else
#	CXXFLAGS     = -O2 -Wall -fPIC -I$(INC_DIR) $(INCLUDE)
#	LDFLAGS      = -O2 -I$(INC_DIR) $(INCLUDE) $(LIBS)
#endif
#
#.SECONDEXPANSION:
## Main targets
#all : $$(OBJECT_BASE)
#
#$(OBJ_DIR)/%.o : $(SRC_DIR)/%.cxx
#	$(CXX) $(CXXFLAGS) -c $^ -o $@ $(INC_ADDTL)
#
#clean:
#	@echo -e "\n\n===> cleaning directories"
#	rm -f $(OBJ_DIR)/*.o 
#
include ../MakefileBase.mk
WORK_AREA = ${WorkArea}

PKG_DIR = $(WORK_AREA)/TreeFilter/$(PACKAGE)/
EXE_DIR = ""
#$(PKG_DIR)
#OBJ_DIR = $(PKG_DIR)/obj/
#SRC_DIR = $(PKG_DIR)/src
#INC_DIR = $(PKG_DIR)/include

MKDIR_P = mkdir -p

COMMON_DIR = $(WORK_AREA)/TreeFilter/Common

INCLUDE      = $(ROOTCXXFLAGS) $(BOOSTFLAGS) $(COREINC) $(COMMONINC)\
	-I$(PKG_DIR)


COREINC = -I$(WORK_AREA)/TreeFilter/Core/include
COMMONINC = -I$(WORK_AREA)/TreeFilter/Common/include
COREOBJ = $(WORK_AREA)/TreeFilter/Core/obj/AnalysisBase.o\
	$(WORK_AREA)/TreeFilter/Core/obj/Util.o


OBJECT_INIT = $(OBJ_DIR)/BranchInit.o
OBJECT_RUN = $(OBJ_DIR)/RunAnalysis.o

SRC_INIT = $(SRC_DIR)/BranchInit.cxx
SRC_RUN = $(SRC_DIR)/RunAnalysis.cxx

OBJECT_ANA = $(OBJECT_INIT) $(OBJECT_RUN)
LINKDEF = $(OBJ_DIR)/cintLib.so

ifneq  ($(ADDTL_OBJ),) 
	OBJECT_ADDTL = $(OBJ_DIR)/$(ADDTL_OBJ)
endif

ifneq  ($(ADDTL_INC),) 
	INC_ADDTL = -I$(ADDTL_INC)
endif

ifneq  ($(ADDTL_LIB),) 
	LIB_ADDTL = -L$(ADDTL_LIB)
endif

ifneq  ($(EXTERN_OBJ),) 
	OBJ_EXTERN = $(EXTERN_OBJ)
endif


NEWEXENAME=$(EXENAME)
ifeq ($(strip $(EXENAME) ), )
	NEWEXENAME=RunAnalysis.exe
endif

OBJECT_BASE = check objdir $(EXE) 
EXE = $(EXE_DIR)$(NEWEXENAME)

# Main targets

objdir: ${OBJ_DIR}

linkdef: $(SRC_DIR)/Dict.cxx

${OBJ_DIR}:
	${MKDIR_P} ${OBJ_DIR}

$(SRC_DIR)/Dict.cxx: $(PKG_DIR)/include/LinkDef.h
	$(ROOTCINT) -f $@ -c -p $^

$(LINKDEF): $(SRC_DIR)/Dict.cxx
	$(CXX) -shared -o$@ `root-config --ldflags` $(CXXFLAGS)\
	-I$(ROOTSYS)/include $^


$(EXE): $$(OBJECT_ANA) $(OBJECT_ADDTL) $(LINKDEF) 
	$(CXX) $(CXXFLAGS) -o $@ -g $^ $(COREOBJ) $(OBJ_EXTERN) $(LIBS)\
	$(LIB_ADDTL)


veryclean : 
	rm -f $(OBJ_DIR)/*.o 
	rm -f $(SRC_DIR)/Dict.cxx
	rm -f $(SRC_DIR)/BranchInit.cxx
	rm -f $(INC_DIR)/BranchDefs.h
	rm -f $(INC_DIR)/BranchInit.h
	rm -f *.exe

vvclean : 
	rm -f $(OBJ_DIR)/*.o 
	rm -f $(SRC_DIR)/Dict.cxx
	rm -f $(SRC_DIR)/BranchInit.cxx
	rm -f $(INC_DIR)/LinkDef.h
	rm -f $(INC_DIR)/BranchDefs.h
	rm -f $(INC_DIR)/BranchInit.h
	rm -f *.exe

check :
	@if [ ! -f $(WORK_AREA)/TreeFilter/Core/obj/AnalysisBase.o ] ; \
	    then \
	    echo "**************************************" ; \
	    echo "WARNING : CORE NOT COMPILED.  YOUR COMPLIATION WILL FAIL" ; \
	    echo "Simply enter the Core package and type make" ; \
	    echo "cd ../Core ; make ; cd -" ; \
	    echo "**************************************" ; \
	fi;
	         

