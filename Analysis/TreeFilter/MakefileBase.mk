###############################################################################
# 
# Makefile 
#
# Author : Josh Kunkle jkunkle@cern.ch
#
# Compile the local package and link to the Core package
#
################################################################################

CXX     = g++
LD      = g++

BIN_DIR = .
OBJ_DIR = obj
SRC_DIR = src
INC_DIR = include

ROOTCINT     = rootcling
ROOTCONFIG   = root-config

BOOST_VER    = 1.57.0-ikhhed

ROOTCXXFLAGS = $(shell $(ROOTCONFIG) --cflags)
BOOSTFLAGS   = \
	-I/cvmfs/cms.cern.ch/$(SCRAM_ARCH)/external/boost/$(BOOST_VER)/include\
	-L/cvmfs/cms.cern.ch/$(SCRAM_ARCH)/external/boost/$(BOOST_VER)/lib

ROOTLIBS     = $(shell $(ROOTCONFIG) --libs) -lTreePlayer -lTMVA -lRooFit -lTIO
LIBS         = $(ROOTLIBS) $(BOOSTFLAGS) -lboost_filesystem -lboost_system
GCCLIBS      = -l$(subst bin/$(CXX),lib64,$(shell which $(CXX)))


DEBUG        = false
INCLUDE      = $(ROOTCXXFLAGS) $(BOOSTFLAGS)

# Activate debug compilation with:
# %> make DEBUG=true
ifeq ($(DEBUG),true)
	CXXFLAGS     = -O0 -Wall -ggdb -fPIC -I$(INC_DIR) $(INCLUDE)
	LDFLAGS      = -O0 -Wall -ggdb -I$(INC_DIR)  $(INCLUDE) 
else
	CXXFLAGS     = -O2 -Wall -fPIC -I$(INC_DIR)  $(INCLUDE)
	LDFLAGS      = -O2 -I$(INC_DIR) $(INCLUDE) $(LIBS)
endif

.SECONDEXPANSION:
# Main targets
all : $$(OBJECT_BASE)

$(OBJ_DIR)/%.o : $(SRC_DIR)/%.cxx
	$(CXX) $(CXXFLAGS) -c $^ -o $@ $(INC_ADDTL)

clean:
	@echo -e "\n\n===> cleaning directories"
	rm -f $(OBJ_DIR)/*.o 
