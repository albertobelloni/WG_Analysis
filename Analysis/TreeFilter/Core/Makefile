###############################################################################
#
# 
# Makefile       (RPB2010088)
#
# Targets: 
# - main executables  
# - library (which can be loaded within root: gSystem->Load("lib/hwwLib.so") )
# 
#
################################################################################

CXX     = g++
LD      = g++

BIN_DIR = .
OBJ_DIR = obj
SRC_DIR = src
INC_DIR = include

ROOTCINT     = rootcint
ROOTCONFIG   = root-config

BOOST_VER    = 1.57.0-ikhhed

ROOTCXXFLAGS = $(shell $(ROOTCONFIG) --cflags)
BOOSTFLAGS   = \
	-I/cvmfs/cms.cern.ch/$(SCRAM_ARCH)/external/boost/$(BOOST_VER)/include

ROOTLIBS     = $(shell $(ROOTCONFIG) --libs) -lTreePlayer -lTMVA -lRIO
GCCLIBS      = -l$(subst bin/$(CXX),lib64,$(shell which $(CXX)))
LIBS         = $(ROOTLIBS) $(BOOSTFLAGS)

DEBUG        = false
INCLUDE      = $(ROOTCXXFLAGS) $(BOOSTFLAGS)

# Activate debug compilation with:
# %> make DEBUG=true
ifeq ($(DEBUG),true)
	CXXFLAGS     = -O0 -Wall -ggdb -fPIC -I$(INC_DIR) $(INCLUDE)
	LDFLAGS      = -O0 -Wall -ggdb -I$(INC_DIR) $(INCLUDE) 
else
	CXXFLAGS     = -O2 -Wall -fPIC -I$(INC_DIR) $(INCLUDE)
	LDFLAGS      = -O2 -I$(INC_DIR) $(INCLUDE) 
endif

OBJECT_BASE = $(OBJ_DIR)/AnalysisBase.o $(OBJ_DIR)/Util.o

# Main targets
all : $(OBJECT_BASE)

$(OBJ_DIR)/%.o : $(SRC_DIR)/%.cxx
	$(CXX) $(CXXFLAGS) -c $^ -o $@

clean:
	@echo -e "\n\n===> cleaning directories"
	rm -f $(OBJ_DIR)/*.o 
