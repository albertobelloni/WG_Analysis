###############################################################################
# 
# Makefile 
#
# Author : Josh Kunkle jkunkle@cern.ch
#
# Compile the local package and link to the Core package
#
################################################################################

include ../MakefileBase.mk
WORK_AREA = ${WorkArea}

PKG_DIR = $(WORK_AREA)/TreeFilter/$(PACKAGE)/

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
	mv $(SRC_DIR)/Dict_rdict.pcm $(OBJ_DIR)

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
	         

