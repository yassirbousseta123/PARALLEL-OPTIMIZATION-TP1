#!/bin/bash
set -e

echo "=== HPL Build Script for macOS Apple Silicon ==="

# Check dependencies
if ! command -v mpicc &> /dev/null; then
    echo "OpenMPI not found. Install with: brew install open-mpi"
    exit 1
fi

# Download HPL if not present
if [ ! -d "hpl-2.3" ]; then
    echo "Downloading HPL 2.3..."
    curl -LO https://www.netlib.org/benchmark/hpl/hpl-2.3.tar.gz
    tar xzf hpl-2.3.tar.gz
fi

cd hpl-2.3

# Create Make.MacOS
cat > Make.MacOS << 'MAKEFILE'
SHELL        = /bin/sh
CD           = cd
CP           = cp
LN_S         = ln -s
MKDIR        = mkdir
RM           = /bin/rm -f
TOUCH        = touch

ARCH         = MacOS
TOPdir       = $(shell pwd)
INCdir       = $(TOPdir)/include
BINdir       = $(TOPdir)/bin/$(ARCH)
LIBdir       = $(TOPdir)/lib/$(ARCH)

HPLlib       = $(LIBdir)/libhpl.a

# Use Accelerate framework (Apple's optimized BLAS/LAPACK)
LAdir        = /Library/Developer/CommandLineTools/SDKs/MacOSX.sdk/System/Library/Frameworks/Accelerate.framework
LAinc        =
LAlib        = -framework Accelerate

# MPI
MPdir        = /opt/homebrew
MPinc        = -I$(MPdir)/include
MPlib        = -L$(MPdir)/lib -lmpi

# Compiler and flags
CC           = mpicc
CCNOOPT      = $(HPL_DEFS)
CCFLAGS      = $(HPL_DEFS) -O3 -fomit-frame-pointer
LINKER       = mpicc
LINKFLAGS    = $(CCFLAGS)

ARCHIVER     = ar
ARFLAGS      = r
RANLIB       = ranlib

HPL_INCLUDES = -I$(INCdir) -I$(INCdir)/$(ARCH) $(LAinc) $(MPinc)
HPL_LIBS     = $(HPLlib) $(LAlib) $(MPlib)
HPL_OPTS     =
HPL_DEFS     = $(HPL_OPTS) $(HPL_INCLUDES)
MAKEFILE

echo "Building HPL..."
make arch=MacOS

echo ""
echo "=== Build complete! ==="
echo "HPL binary: hpl-2.3/bin/MacOS/xhpl"
