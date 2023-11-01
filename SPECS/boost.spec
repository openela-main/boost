# Support for documentation installation As the %%doc macro erases the
# target directory ($RPM_BUILD_ROOT%%{_docdir}/%%{name}), manually
# installed documentation must be saved into a temporary dedicated
# directory.
# XXX note that as of rpm 4.9.1, this shouldn't be necessary anymore.
# We should be able to install directly.
%global boost_docdir __tmp_docdir
%global boost_examplesdir __tmp_examplesdir

%if 0%{?flatpak}
# For bundling in Flatpak, currently build without mpich and openmpi,
# which aren't needed and cause prefix=/app errors.
%bcond_with mpich
%bcond_with openmpi
%else
# All arches have openmpi and mpich
%bcond_without mpich
%bcond_without openmpi
%endif

%ifnarch %{ix86} x86_64 ppc64le aarch64
  %bcond_with context
%else
  %bcond_without context
%endif

%ifnarch %{ix86} x86_64
  %bcond_with quadmath
%else
  %bcond_without quadmath
%endif

Name: boost
Summary: The free peer-reviewed portable C++ source libraries
Version: 1.66.0
%global version_enc 1_66_0
Release: 13%{?dist}
License: Boost and MIT and Python

%global toplev_dirname %{name}_%{version_enc}
URL: http://www.boost.org

Source0: https://sourceforge.net/projects/boost/files/boost/%{version}/%{toplev_dirname}.tar.bz2
Source1: libboost_thread.so

# Since Fedora 13, the Boost libraries are delivered with sonames
# equal to the Boost version (e.g., 1.41.0).
%global sonamever %{version}

# boost is an "umbrella" package that pulls in all boost shared library
# components, except for MPI and Python sub-packages.  Those are special
# in that there are alternative implementations to choose from
# (Open MPI and MPICH, and Python 2 and 3), and it's not a big burden
# to have interested parties install them explicitly.
# The subpackages that don't install shared libraries are also not pulled in
# (doc, doctools, examples, jam, static).
Requires: boost-atomic%{?_isa} = %{version}-%{release}
Requires: boost-chrono%{?_isa} = %{version}-%{release}
Requires: boost-container%{?_isa} = %{version}-%{release}
%if %{with context}
Requires: boost-context%{?_isa} = %{version}-%{release}
Requires: boost-coroutine%{?_isa} = %{version}-%{release}
%endif
Requires: boost-date-time%{?_isa} = %{version}-%{release}
%if %{with context}
Requires: boost-fiber%{?_isa} = %{version}-%{release}
%endif
Requires: boost-filesystem%{?_isa} = %{version}-%{release}
Requires: boost-graph%{?_isa} = %{version}-%{release}
Requires: boost-iostreams%{?_isa} = %{version}-%{release}
Requires: boost-locale%{?_isa} = %{version}-%{release}
Requires: boost-log%{?_isa} = %{version}-%{release}
Requires: boost-math%{?_isa} = %{version}-%{release}
Requires: boost-program-options%{?_isa} = %{version}-%{release}
Requires: boost-random%{?_isa} = %{version}-%{release}
Requires: boost-regex%{?_isa} = %{version}-%{release}
Requires: boost-serialization%{?_isa} = %{version}-%{release}
Requires: boost-signals%{?_isa} = %{version}-%{release}
Requires: boost-stacktrace%{?_isa} = %{version}-%{release}
Requires: boost-system%{?_isa} = %{version}-%{release}
Requires: boost-test%{?_isa} = %{version}-%{release}
Requires: boost-thread%{?_isa} = %{version}-%{release}
Requires: boost-timer%{?_isa} = %{version}-%{release}
Requires: boost-type_erasure%{?_isa} = %{version}-%{release}
Requires: boost-wave%{?_isa} = %{version}-%{release}

BuildRequires: m4
BuildRequires: libstdc++-devel
BuildRequires: bzip2-devel
BuildRequires: zlib-devel
BuildRequires: xz-devel
BuildRequires: python3-devel
BuildRequires: python3-numpy
BuildRequires: libicu-devel
%if %{with quadmath}
BuildRequires: libquadmath-devel
%endif

# https://svn.boost.org/trac/boost/ticket/6150
Patch4: boost-1.50.0-fix-non-utf8-files.patch

# Add a manual page for bjam, based on the on-line documentation:
# http://www.boost.org/boost-build2/doc/html/bbv2/overview.html
Patch5: boost-1.48.0-add-bjam-man-page.patch

# https://bugzilla.redhat.com/show_bug.cgi?id=828856
# https://bugzilla.redhat.com/show_bug.cgi?id=828857
# https://svn.boost.org/trac/boost/ticket/6701
Patch15: boost-1.58.0-pool.patch

# https://svn.boost.org/trac/boost/ticket/5637
Patch25: boost-1.57.0-mpl-print.patch

# https://svn.boost.org/trac/boost/ticket/9038
Patch51: boost-1.58.0-pool-test_linking.patch

# https://bugzilla.redhat.com/show_bug.cgi?id=1102667
Patch61: boost-1.57.0-python-libpython_dep.patch
Patch62: boost-1.66.0-python-abi_letters.patch

# https://bugzilla.redhat.com/show_bug.cgi?id=1190039
Patch65: boost-1.66.0-build-optflags.patch

# Prevent gcc.jam from setting -m32 or -m64.
Patch68: boost-1.66.0-address-model.patch

# https://bugzilla.redhat.com/show_bug.cgi?id=1318383
Patch82: boost-1.66.0-no-rpath.patch

# https://bugzilla.redhat.com/show_bug.cgi?id=1541035
Patch83: boost-1.66.0-bjam-build-flags.patch

# https://bugzilla.redhat.com/show_bug.cgi?id=1545092
Patch84: boost-1.66.0-spirit-abs-overflow.patch

Patch85: boost-1.66.0-py3-shebang.patch

# https://bugzilla.redhat.com/show_bug.cgi?id=1596468
# https://github.com/boostorg/python/pull/218
Patch87: boost-1.66.0-numpy3.patch

# https://bugzilla.redhat.com/show_bug.cgi?id=1630552
Patch88: boost-1.66-annobin-notes.patch

# https://github.com/boostorg/build/pull/350
Patch89: boost-1.66-build-malloc-sizeof.patch

# https://github.com/boostorg/build/pull/351
Patch90: boost-1.66-build-memory-leak.patch

# https://github.com/boostorg/graph/pull/84
Patch91: boost-1.66-graph-return-local-addr.patch

%bcond_with tests
%bcond_with docs_generated

%description
Boost provides free peer-reviewed portable C++ source libraries.  The
emphasis is on libraries which work well with the C++ Standard
Library, in the hopes of establishing "existing practice" for
extensions and providing reference implementations so that the Boost
libraries are suitable for eventual standardization. (Some of the
libraries have already been included in the C++ 2011 standard and
others have been proposed to the C++ Standards Committee for inclusion
in future standards.)

%package atomic
Summary: Run-time component of boost atomic library

%description atomic

Run-time support for Boost.Atomic, a library that provides atomic data
types and operations on these data types, as well as memory ordering
constraints required for coordinating multiple threads through atomic
variables.

%package chrono
Summary: Run-time component of boost chrono library
Requires: boost-system%{?_isa} = %{version}-%{release}

%description chrono

Run-time support for Boost.Chrono, a set of useful time utilities.

%package container
Summary: Run-time component of boost container library

%description container

Boost.Container library implements several well-known containers,
including STL containers. The aim of the library is to offer advanced
features not present in standard containers or to offer the latest
standard draft features for compilers that comply with C++03.

%if %{with context}
%package context
Summary: Run-time component of boost context switching library

%description context

Run-time support for Boost.Context, a foundational library that
provides a sort of cooperative multitasking on a single thread.

%package coroutine
Summary: Run-time component of boost coroutine library
Requires: boost-chrono%{?_isa} = %{version}-%{release}
Requires: boost-context%{?_isa} = %{version}-%{release}
Requires: boost-system%{?_isa} = %{version}-%{release}
Requires: boost-thread%{?_isa} = %{version}-%{release}

%description coroutine
Run-time support for Boost.Coroutine, a library that provides
generalized subroutines which allow multiple entry points for
suspending and resuming execution.

%endif

%package date-time
Summary: Run-time component of boost date-time library

%description date-time

Run-time support for Boost Date Time, a set of date-time libraries based
on generic programming concepts.

%if %{with context}
%package fiber
Summary: Run-time component of boost fiber library
Requires: boost-context%{?_isa} = %{version}-%{release}
Requires: boost-filesystem%{?_isa} = %{version}-%{release}
Requires: boost-system%{?_isa} = %{version}-%{release}

%description fiber

Run-time support for the Boost Fiber library, a framework for
micro-/userland-threads (fibers) scheduled cooperatively.
%endif

%package filesystem
Summary: Run-time component of boost filesystem library
Requires: boost-system%{?_isa} = %{version}-%{release}

%description filesystem

Run-time support for the Boost Filesystem Library, which provides
portable facilities to query and manipulate paths, files, and
directories.

%package graph
Summary: Run-time component of boost graph library
Requires: boost-regex%{?_isa} = %{version}-%{release}

%description graph

Run-time support for the BGL graph library.  BGL interface and graph
components are generic, in the same sense as the Standard Template
Library (STL).

%package iostreams
Summary: Run-time component of boost iostreams library

%description iostreams

Run-time support for Boost.Iostreams, a framework for defining streams,
stream buffers and i/o filters.

%package locale
Summary: Run-time component of boost locale library
Requires: boost-chrono%{?_isa} = %{version}-%{release}
Requires: boost-system%{?_isa} = %{version}-%{release}
Requires: boost-thread%{?_isa} = %{version}-%{release}

%description locale

Run-time support for Boost.Locale, a set of localization and Unicode
handling tools.

%package log
Summary: Run-time component of boost logging library
Requires: boost-atomic%{?_isa} = %{version}-%{release}
Requires: boost-chrono%{?_isa} = %{version}-%{release}
Requires: boost-date-time%{?_isa} = %{version}-%{release}
Requires: boost-filesystem%{?_isa} = %{version}-%{release}
Requires: boost-regex%{?_isa} = %{version}-%{release}
Requires: boost-system%{?_isa} = %{version}-%{release}
Requires: boost-thread%{?_isa} = %{version}-%{release}

%description log

Boost.Log library aims to make logging significantly easier for the
application developer.  It provides a wide range of out-of-the-box
tools along with public interfaces for extending the library.

%package math
Summary: Math functions for boost TR1 library

%description math

Run-time support for C99 and C++ TR1 C-style Functions from the math
portion of Boost.TR1.

%package numpy3
Summary: Run-time component of boost numpy library for Python 3
Requires: boost-python3%{?_isa} = %{version}-%{release}
Requires: python3-numpy

%description numpy3

The Boost Python Library is a framework for interfacing Python and
C++. It allows you to quickly and seamlessly expose C++ classes,
functions and objects to Python, and vice versa, using no special
tools -- just your C++ compiler.  This package contains run-time
support for the NumPy extension of the Boost Python Library for Python 3.

%package program-options
Summary:  Run-time component of boost program_options library

%description program-options

Run-time support of boost program options library, which allows program
developers to obtain (name, value) pairs from the user, via
conventional methods such as command-line and configuration file.

%package python3
Summary: Run-time component of boost python library for Python 3

%description python3

The Boost Python Library is a framework for interfacing Python and
C++. It allows you to quickly and seamlessly expose C++ classes,
functions and objects to Python, and vice versa, using no special
tools -- just your C++ compiler.  This package contains run-time
support for the Boost Python Library compiled for Python 3.

%package python3-devel
Summary: Shared object symbolic links for Boost.Python 3
Requires: boost-numpy3%{?_isa} = %{version}-%{release}
Requires: boost-python3%{?_isa} = %{version}-%{release}
Requires: boost-devel%{?_isa} = %{version}-%{release}

%description python3-devel

Shared object symbolic links for Python 3 variant of Boost.Python.

%package random
Summary: Run-time component of boost random library
Requires: boost-system%{?_isa} = %{version}-%{release}

%description random

Run-time support for boost random library.

%package regex
Summary: Run-time component of boost regular expression library

%description regex

Run-time support for boost regular expression library.

%package serialization
Summary: Run-time component of boost serialization library

%description serialization

Run-time support for serialization for persistence and marshaling.

%package signals
Summary: Run-time component of boost signals and slots library

%description signals

Run-time support for managed signals & slots callback implementation.

%package stacktrace
Summary: Run-time component of boost stacktrace library

%description stacktrace

Run-time component of the Boost stacktrace library.

%package system
Summary: Run-time component of boost system support library

%description system

Run-time component of Boost operating system support library, including
the diagnostics support that is part of the C++11 standard library.

%package test
Summary: Run-time component of boost test library
Requires: boost-system%{?_isa} = %{version}-%{release}
Requires: boost-timer%{?_isa} = %{version}-%{release}

%description test

Run-time support for simple program testing, full unit testing, and for
program execution monitoring.

%package thread
Summary: Run-time component of boost thread library
Requires: boost-system%{?_isa} = %{version}-%{release}

%description thread

Run-time component Boost.Thread library, which provides classes and
functions for managing multiple threads of execution, and for
synchronizing data between the threads or providing separate copies of
data specific to individual threads.

%package timer
Summary: Run-time component of boost timer library
Requires: boost-chrono%{?_isa} = %{version}-%{release}
Requires: boost-system%{?_isa} = %{version}-%{release}

%description timer

"How long does my C++ code take to run?"
The Boost Timer library answers that question and does so portably,
with as little as one #include and one additional line of code.

%package type_erasure
Summary: Run-time component of boost type erasure library
Requires: boost-chrono%{?_isa} = %{version}-%{release}
Requires: boost-system%{?_isa} = %{version}-%{release}
Requires: boost-thread%{?_isa} = %{version}-%{release}

%description type_erasure

The Boost.TypeErasure library provides runtime polymorphism in C++
that is more flexible than that provided by the core language.

%package wave
Summary: Run-time component of boost C99/C++ preprocessing library
Requires: boost-chrono%{?_isa} = %{version}-%{release}
Requires: boost-date-time%{?_isa} = %{version}-%{release}
Requires: boost-filesystem%{?_isa} = %{version}-%{release}
Requires: boost-system%{?_isa} = %{version}-%{release}
Requires: boost-thread%{?_isa} = %{version}-%{release}

%description wave

Run-time support for the Boost.Wave library, a Standards conforming,
and highly configurable implementation of the mandated C99/C++
preprocessor functionality.

%package devel
Summary: The Boost C++ headers and shared development libraries
Requires: boost%{?_isa} = %{version}-%{release}
Requires: libicu-devel%{?_isa}
%if %{with quadmath}
Requires: libquadmath-devel%{?_isa}
%endif

%description devel
Headers and shared object symbolic links for the Boost C++ libraries.

%package static
Summary: The Boost C++ static development libraries
Requires: boost-devel%{?_isa} = %{version}-%{release}

%description static
Static Boost C++ libraries.

%package doc
Summary: HTML documentation for the Boost C++ libraries
%if 0%{?rhel} >= 6
BuildArch: noarch
%endif

%description doc
This package contains the documentation in the HTML format of the Boost C++
libraries. The documentation provides the same content as that on the Boost
web page (http://www.boost.org/doc/libs/%{version_enc}).

%package examples
Summary: Source examples for the Boost C++ libraries
%if 0%{?rhel} >= 6
BuildArch: noarch
%endif
Requires: boost-devel = %{version}-%{release}

%description examples
This package contains example source files distributed with boost.


%if %{with openmpi}

%package openmpi
Summary: Run-time component of Boost.MPI library
BuildRequires: openmpi-devel
Requires: boost-serialization%{?_isa} = %{version}-%{release}

%description openmpi

Run-time support for Boost.MPI-OpenMPI, a library providing a clean C++
API over the OpenMPI implementation of MPI.

%package openmpi-devel
Summary: Shared library symbolic links for Boost.MPI
Requires: boost-devel%{?_isa} = %{version}-%{release}
Requires: boost-openmpi%{?_isa} = %{version}-%{release}
Requires: boost-graph-openmpi%{?_isa} = %{version}-%{release}

%description openmpi-devel

Devel package for Boost.MPI-OpenMPI, a library providing a clean C++
API over the OpenMPI implementation of MPI.

%package openmpi-python3
Summary: Python 3 run-time component of Boost.MPI library
Requires: boost-openmpi%{?_isa} = %{version}-%{release}
Requires: boost-python3%{?_isa} = %{version}-%{release}
Requires: boost-serialization%{?_isa} = %{version}-%{release}
Requires: python3-openmpi%{?_isa}

%description openmpi-python3

Python 3 support for Boost.MPI-OpenMPI, a library providing a clean C++
API over the OpenMPI implementation of MPI.

%package openmpi-python3-devel
Summary: Shared library symbolic links for Boost.MPI Python 3 component
Requires: boost-devel%{?_isa} = %{version}-%{release}
Requires: boost-python3-devel%{?_isa} = %{version}-%{release}
Requires: boost-openmpi-devel%{?_isa} = %{version}-%{release}
Requires: boost-openmpi-python3%{?_isa} = %{version}-%{release}

%description openmpi-python3-devel

Devel package for the Python 3 interface of Boost.MPI-OpenMPI, a library
providing a clean C++ API over the OpenMPI implementation of MPI.

%package graph-openmpi
Summary: Run-time component of parallel boost graph library
Requires: boost-openmpi%{?_isa} = %{version}-%{release}
Requires: boost-serialization%{?_isa} = %{version}-%{release}

%description graph-openmpi

Run-time support for the Parallel BGL graph library.  The interface and
graph components are generic, in the same sense as the Standard
Template Library (STL).  This libraries in this package use OpenMPI
back-end to do the parallel work.

%endif


%if %{with mpich}

%package mpich
Summary: Run-time component of Boost.MPI library
BuildRequires: mpich-devel
Requires: boost-serialization%{?_isa} = %{version}-%{release}

%description mpich

Run-time support for Boost.MPI-MPICH, a library providing a clean C++
API over the MPICH implementation of MPI.

%package mpich-devel
Summary: Shared library symbolic links for Boost.MPI
Requires: boost-devel%{?_isa} = %{version}-%{release}
Requires: boost-mpich%{?_isa} = %{version}-%{release}
Requires: boost-graph-mpich%{?_isa} = %{version}-%{release}

%description mpich-devel

Devel package for Boost.MPI-MPICH, a library providing a clean C++
API over the MPICH implementation of MPI.

%package mpich-python3
Summary: Python 3 run-time component of Boost.MPI library
Requires: boost-mpich%{?_isa} = %{version}-%{release}
Requires: boost-python3%{?_isa} = %{version}-%{release}
Requires: boost-serialization%{?_isa} = %{version}-%{release}
Requires: python3-mpich%{?_isa}

%description mpich-python3

Python 3 support for Boost.MPI-MPICH, a library providing a clean C++
API over the MPICH implementation of MPI.

%package mpich-python3-devel
Summary: Shared library symbolic links for Boost.MPI Python 3 component
Requires: boost-devel%{?_isa} = %{version}-%{release}
Requires: boost-python3-devel%{?_isa} = %{version}-%{release}
Requires: boost-mpich-devel%{?_isa} = %{version}-%{release}
Requires: boost-mpich-python3%{?_isa} = %{version}-%{release}

%description mpich-python3-devel

Devel package for the Python 3 interface of Boost.MPI-MPICH, a library
providing a clean C++ API over the MPICH implementation of MPI.

%package graph-mpich
Summary: Run-time component of parallel boost graph library
Requires: boost-mpich%{?_isa} = %{version}-%{release}
Requires: boost-serialization%{?_isa} = %{version}-%{release}

%description graph-mpich

Run-time support for the Parallel BGL graph library.  The interface and
graph components are generic, in the same sense as the Standard
Template Library (STL).  This libraries in this package use MPICH
back-end to do the parallel work.

%endif

%package build
Summary: Cross platform build system for C++ projects
Requires: boost-jam
BuildArch: noarch

%description build
Boost.Build is an easy way to build C++ projects, everywhere. You name
your pieces of executable and libraries and list their sources.  Boost.Build
takes care about compiling your sources with the right options,
creating static and shared libraries, making pieces of executable, and other
chores -- whether you're using GCC, MSVC, or a dozen more supported
C++ compilers -- on Windows, OSX, Linux and commercial UNIX systems.

%package doctools
Summary: Tools for working with Boost documentation
Requires: docbook-dtds
Requires: docbook-style-xsl

%description doctools

Tools for working with Boost documentation in BoostBook or QuickBook format.

%package jam
Summary: A low-level build tool

%description jam
Boost.Jam (BJam) is the low-level build engine tool for Boost.Build.
Historically, Boost.Jam is based on on FTJam and on Perforce Jam but has grown
a number of significant features and is now developed independently.

%prep
%setup -q -n %{toplev_dirname}
find ./boost -name '*.hpp' -perm /111 | xargs chmod a-x

%patch4 -p1
%patch5 -p1
%patch15 -p0
%patch25 -p1
%patch51 -p1
%patch61 -p1
%patch62 -p1
%patch65 -p1
%patch68 -p1
%patch82 -p1
%patch83 -p1
%patch84 -p1
%patch85 -p1
%patch87 -p1
%patch88 -p1
%patch89 -p1
%patch90 -p1
%patch91 -p2

%build
PYTHON3_ABIFLAGS=$(/usr/bin/python3-config --abiflags)

# There are many strict aliasing warnings, and it's not feasible to go
# through them all at this time.
# There are also lots of noisy but harmless unused local typedef warnings.
export RPM_OPT_FLAGS="$RPM_OPT_FLAGS -fno-strict-aliasing -Wno-unused-local-typedefs -Wno-deprecated-declarations"

cat > ./tools/build/src/user-config.jam << "EOF"
import os ;
local RPM_OPT_FLAGS = [ os.environ RPM_OPT_FLAGS ] ;
local RPM_LD_FLAGS = [ os.environ RPM_LD_FLAGS ] ;

using gcc : : : <compileflags>$(RPM_OPT_FLAGS) <linkflags>$(RPM_LD_FLAGS) ;
%if %{with openmpi} || %{with mpich}
using mpi ;
%endif
EOF

cat >> ./tools/build/src/user-config.jam << EOF
using python : %{python3_version} : /usr/bin/python3 : /usr/include/python%{python3_version}${PYTHON3_ABIFLAGS} : : : : ${PYTHON3_ABIFLAGS} ;
EOF

./bootstrap.sh --with-toolset=gcc --with-icu

# N.B. When we build the following with PCH, parts of boost (math
# library in particular) end up being built second time during
# installation.  Unsure why that is, but all sub-builds need to be
# built with pch=off to avoid this.

echo ============================= build serial ==================
./b2 -d+2 -q %{?_smp_mflags} \
	--without-mpi --without-graph_parallel --build-dir=serial \
%if !%{with context}
	--without-context --without-coroutine \
	--without-fiber \
%endif
	variant=release threading=multi debug-symbols=on pch=off \
	python=%{python3_version} stage

# See libs/thread/build/Jamfile.v2 for where this file comes from.
if [ $(find serial -type f -name has_atomic_flag_lockfree \
		-print -quit | wc -l) -ne 0 ]; then
	DEF=D
else
	DEF=U
fi

m4 -${DEF}HAS_ATOMIC_FLAG_LOCKFREE -DVERSION=%{version} \
	%{SOURCE1} > $(basename %{SOURCE1})

# Build MPI parts of Boost with OpenMPI support

%if %{with openmpi} || %{with mpich}
# First, purge all modules so that user environment doesn't conflict
# with the build.
module purge ||:
%endif

%if %{with openmpi}
%{_openmpi_load}
echo ============================= build $MPI_COMPILER ==================
./b2 -d+2 -q %{?_smp_mflags} \
	--with-mpi --with-graph_parallel --build-dir=$MPI_COMPILER \
	variant=release threading=multi debug-symbols=on pch=off \
	python=%{python3_version} stage

%{_openmpi_unload}
export PATH=/bin${PATH:+:}$PATH
%endif

# Build MPI parts of Boost with MPICH support
%if %{with mpich}
%{_mpich_load}
echo ============================= build $MPI_COMPILER ==================
./b2 -d+2 -q %{?_smp_mflags} \
	--with-mpi --with-graph_parallel --build-dir=$MPI_COMPILER \
	variant=release threading=multi debug-symbols=on pch=off \
	python=%{python3_version} stage

%{_mpich_unload}
export PATH=/bin${PATH:+:}$PATH
%endif

echo ============================= build Boost.Build ==================
(cd tools/build
 ./bootstrap.sh --with-toolset=gcc)

%check
:


%install
cd %{_builddir}/%{toplev_dirname}

%if %{with openmpi} || %{with mpich}
# First, purge all modules so that user environment doesn't conflict
# with the build.
module purge ||:
%endif

%if %{with openmpi}
%{_openmpi_load}
# XXX We want to extract this from RPM flags
# b2 instruction-set=i686 etc.
echo ============================= install $MPI_COMPILER ==================
./b2 -q %{?_smp_mflags} \
	--with-mpi --with-graph_parallel --build-dir=$MPI_COMPILER \
	--stagedir=${RPM_BUILD_ROOT}${MPI_HOME} \
	variant=release threading=multi debug-symbols=on pch=off \
	python=%{python3_version} stage

# Move Python module to proper location for automatic loading
mkdir -p ${RPM_BUILD_ROOT}%{python3_sitearch}/openmpi/boost
touch ${RPM_BUILD_ROOT}%{python3_sitearch}/openmpi/boost/__init__.py
mv ${RPM_BUILD_ROOT}${MPI_HOME}/lib/mpi.so \
   ${RPM_BUILD_ROOT}%{python3_sitearch}/openmpi/boost/

# Remove generic parts of boost that were built for dependencies.
rm -f ${RPM_BUILD_ROOT}${MPI_HOME}/lib/libboost_{python,{w,}serialization}*

%{_openmpi_unload}
export PATH=/bin${PATH:+:}$PATH
%endif

%if %{with mpich}
%{_mpich_load}
echo ============================= install $MPI_COMPILER ==================
./b2 -q %{?_smp_mflags} \
	--with-mpi --with-graph_parallel --build-dir=$MPI_COMPILER \
	--stagedir=${RPM_BUILD_ROOT}${MPI_HOME} \
	variant=release threading=multi debug-symbols=on pch=off \
	python=%{python3_version} stage

# Move Python module to proper location for automatic loading
mkdir -p ${RPM_BUILD_ROOT}%{python3_sitearch}/mpich/boost
touch ${RPM_BUILD_ROOT}%{python3_sitearch}/mpich/boost/__init__.py
mv ${RPM_BUILD_ROOT}${MPI_HOME}/lib/mpi.so \
   ${RPM_BUILD_ROOT}%{python3_sitearch}/mpich/boost/

# Remove generic parts of boost that were built for dependencies.
rm -f ${RPM_BUILD_ROOT}${MPI_HOME}/lib/libboost_{python,{w,}serialization}*

%{_mpich_unload}
export PATH=/bin${PATH:+:}$PATH
%endif

echo ============================= install serial ==================
./b2 -d+2 -q %{?_smp_mflags} \
	--without-mpi --without-graph_parallel --build-dir=serial \
%if !%{with context}
	--without-context --without-coroutine \
	--without-fiber \
%endif
	--prefix=$RPM_BUILD_ROOT%{_prefix} \
	--libdir=$RPM_BUILD_ROOT%{_libdir} \
	variant=release threading=multi debug-symbols=on pch=off \
	python=%{python3_version} install

# Override DSO symlink with a linker script.  See the linker script
# itself for details of why we need to do this.
[ -f $RPM_BUILD_ROOT%{_libdir}/libboost_thread.so ] # Must be present
rm -f $RPM_BUILD_ROOT%{_libdir}/libboost_thread.so
install -p -m 644 $(basename %{SOURCE1}) $RPM_BUILD_ROOT%{_libdir}/

echo ============================= install Boost.Build ==================
(cd tools/build
 ./b2 --prefix=$RPM_BUILD_ROOT%{_prefix} install
 # Fix some permissions
 chmod -x $RPM_BUILD_ROOT%{_datadir}/boost-build/src/build/alias.py
 chmod +x $RPM_BUILD_ROOT%{_datadir}/boost-build/src/tools/doxproc.py
 # We don't want to distribute this
 rm -f $RPM_BUILD_ROOT%{_bindir}/b2
 # Not a real file
 rm -f $RPM_BUILD_ROOT%{_datadir}/boost-build/src/build/project.ann.py
 # Empty file
 rm -f $RPM_BUILD_ROOT%{_datadir}/boost-build/src/tools/doxygen/windows-paths-check.hpp
 # Install the manual page
 %{__install} -p -m 644 v2/doc/bjam.1 -D $RPM_BUILD_ROOT%{_mandir}/man1/bjam.1
)

echo ============================= install Boost.QuickBook ==================
(cd tools/quickbook
 ../build/b2 --prefix=$RPM_BUILD_ROOT%{_prefix}
 %{__install} -p -m 755 ../../dist/bin/quickbook $RPM_BUILD_ROOT%{_bindir}/
 cd ../boostbook
 find dtd -type f -name '*.dtd' | while read tobeinstalledfiles; do
   install -p -m 644 $tobeinstalledfiles -D $RPM_BUILD_ROOT%{_datadir}/boostbook/$tobeinstalledfiles
 done
 find xsl -type f | while read tobeinstalledfiles; do
   install -p -m 644 $tobeinstalledfiles -D $RPM_BUILD_ROOT%{_datadir}/boostbook/$tobeinstalledfiles
 done
)

# Install documentation files (HTML pages) within the temporary place
echo ============================= install documentation ==================
# Prepare the place to temporarily store the generated documentation
rm -rf %{boost_docdir} && %{__mkdir_p} %{boost_docdir}/html
DOCPATH=%{boost_docdir}
DOCREGEX='.*\.\(html?\|css\|png\|gif\)'

find libs doc more -type f -regex $DOCREGEX \
    | sed -n '/\//{s,/[^/]*$,,;p}' \
    | sort -u > tmp-doc-directories

sed "s:^:$DOCPATH/:" tmp-doc-directories \
    | xargs -P 0 --no-run-if-empty %{__install} -d

cat tmp-doc-directories | while read tobeinstalleddocdir; do
    find $tobeinstalleddocdir -mindepth 1 -maxdepth 1 -regex $DOCREGEX -print0 \
    | xargs -P 0 -0 %{__install} -p -m 644 -t $DOCPATH/$tobeinstalleddocdir
done
rm -f tmp-doc-directories
%{__install} -p -m 644 -t $DOCPATH LICENSE_1_0.txt index.htm index.html boost.png rst.css boost.css

echo ============================= install examples ==================
# Fix a few non-standard issues (DOS and/or non-UTF8 files)
sed -i -e 's/\r//g' libs/geometry/example/ml02_distance_strategy.cpp
for tmp_doc_file in flyweight/example/Jamfile.v2 \
 format/example/sample_new_features.cpp multi_index/example/Jamfile.v2 \
 multi_index/example/hashed.cpp serialization/example/demo_output.txt
do
  mv libs/${tmp_doc_file} libs/${tmp_doc_file}.iso8859
  iconv -f ISO8859-1 -t UTF8 < libs/${tmp_doc_file}.iso8859 > libs/${tmp_doc_file}
  touch -r libs/${tmp_doc_file}.iso8859 libs/${tmp_doc_file}
  rm -f libs/${tmp_doc_file}.iso8859
done

# Prepare the place to temporarily store the examples
rm -rf %{boost_examplesdir} && mkdir -p %{boost_examplesdir}/html
EXAMPLESPATH=%{boost_examplesdir}
find libs -type d -name example -exec find {} -type f \; \
    | sed -n '/\//{s,/[^/]*$,,;p}' \
    | sort -u > tmp-doc-directories
sed "s:^:$EXAMPLESPATH/:" tmp-doc-directories \
    | xargs -P 0 --no-run-if-empty %{__install} -d
rm -f tmp-doc-files-to-be-installed && touch tmp-doc-files-to-be-installed
cat tmp-doc-directories | while read tobeinstalleddocdir
do
  find $tobeinstalleddocdir -mindepth 1 -maxdepth 1 -type f \
    >> tmp-doc-files-to-be-installed
done
cat tmp-doc-files-to-be-installed | while read tobeinstalledfiles
do
  if test -s $tobeinstalledfiles
  then
    tobeinstalleddocdir=`dirname $tobeinstalledfiles`
    %{__install} -p -m 644 -t $EXAMPLESPATH/$tobeinstalleddocdir $tobeinstalledfiles
  fi
done
rm -f tmp-doc-files-to-be-installed
rm -f tmp-doc-directories
%{__install} -p -m 644 -t $EXAMPLESPATH LICENSE_1_0.txt


# MPI subpackages don't need the ldconfig magic.  They are hidden by
# default, in MPI back-end-specific directory, and only show to the
# user after the relevant environment module has been loaded.
# rpmlint will report that as errors, but it is fine.

%post atomic -p /sbin/ldconfig

%postun atomic -p /sbin/ldconfig

%post chrono -p /sbin/ldconfig

%postun chrono -p /sbin/ldconfig

%post container -p /sbin/ldconfig

%postun container -p /sbin/ldconfig

%if %{with context}
%post context -p /sbin/ldconfig

%postun context -p /sbin/ldconfig

%post coroutine -p /sbin/ldconfig

%postun coroutine -p /sbin/ldconfig
%endif

%post date-time -p /sbin/ldconfig

%postun date-time -p /sbin/ldconfig

%if %{with context}
%post fiber -p /sbin/ldconfig

%postun fiber -p /sbin/ldconfig
%endif

%post filesystem -p /sbin/ldconfig

%postun filesystem -p /sbin/ldconfig

%post graph -p /sbin/ldconfig

%postun graph -p /sbin/ldconfig

%post iostreams -p /sbin/ldconfig

%postun iostreams -p /sbin/ldconfig

%post locale -p /sbin/ldconfig

%postun locale -p /sbin/ldconfig

%post log -p /sbin/ldconfig

%postun log -p /sbin/ldconfig

%post math -p /sbin/ldconfig

%postun math -p /sbin/ldconfig

%post numpy3 -p /sbin/ldconfig

%postun numpy3 -p /sbin/ldconfig

%post program-options -p /sbin/ldconfig

%postun program-options -p /sbin/ldconfig

%post python3 -p /sbin/ldconfig

%postun python3 -p /sbin/ldconfig

%post random -p /sbin/ldconfig

%postun random -p /sbin/ldconfig

%post regex -p /sbin/ldconfig

%postun regex -p /sbin/ldconfig

%post serialization -p /sbin/ldconfig

%postun serialization -p /sbin/ldconfig

%post signals -p /sbin/ldconfig

%postun signals -p /sbin/ldconfig

%post stacktrace -p /sbin/ldconfig

%postun stacktrace -p /sbin/ldconfig

%post system -p /sbin/ldconfig

%postun system -p /sbin/ldconfig

%post test -p /sbin/ldconfig

%postun test -p /sbin/ldconfig

%post thread -p /sbin/ldconfig

%postun thread -p /sbin/ldconfig

%post timer -p /sbin/ldconfig

%postun timer -p /sbin/ldconfig

%post type_erasure -p /sbin/ldconfig

%postun type_erasure -p /sbin/ldconfig

%post wave -p /sbin/ldconfig

%postun wave -p /sbin/ldconfig

%post doctools
CATALOG=%{_sysconfdir}/xml/catalog
%{_bindir}/xmlcatalog --noout --add "rewriteSystem" \
 "http://www.boost.org/tools/boostbook/dtd" \
 "file://%{_datadir}/boostbook/dtd" $CATALOG
%{_bindir}/xmlcatalog --noout --add "rewriteURI" \
 "http://www.boost.org/tools/boostbook/dtd" \
 "file://%{_datadir}/boostbook/dtd" $CATALOG
%{_bindir}/xmlcatalog --noout --add "rewriteSystem" \
 "http://www.boost.org/tools/boostbook/xsl" \
 "file://%{_datadir}/boostbook/xsl" $CATALOG
%{_bindir}/xmlcatalog --noout --add "rewriteURI" \
 "http://www.boost.org/tools/boostbook/xsl" \
 "file://%{_datadir}/boostbook/xsl" $CATALOG

%postun doctools
# remove entries only on removal of package
if [ "$1" = 0 ]; then
  CATALOG=%{_sysconfdir}/xml/catalog
  %{_bindir}/xmlcatalog --noout --del \
    "file://%{_datadir}/boostbook/dtd" $CATALOG
  %{_bindir}/xmlcatalog --noout --del \
    "file://%{_datadir}/boostbook/xsl" $CATALOG
fi


%files
%license LICENSE_1_0.txt

%files atomic
%license LICENSE_1_0.txt
%{_libdir}/libboost_atomic.so.%{sonamever}

%files chrono
%license LICENSE_1_0.txt
%{_libdir}/libboost_chrono.so.%{sonamever}

%files container
%license LICENSE_1_0.txt
%{_libdir}/libboost_container.so.%{sonamever}

%if %{with context}

%files context
%license LICENSE_1_0.txt
%{_libdir}/libboost_context.so.%{sonamever}

%files coroutine
%license LICENSE_1_0.txt
%{_libdir}/libboost_coroutine.so.%{sonamever}

%endif

%files date-time
%license LICENSE_1_0.txt
%{_libdir}/libboost_date_time.so.%{sonamever}

%if %{with context}
%files fiber
%license LICENSE_1_0.txt
%{_libdir}/libboost_fiber.so.%{sonamever}
%endif

%files filesystem
%license LICENSE_1_0.txt
%{_libdir}/libboost_filesystem.so.%{sonamever}

%files graph
%license LICENSE_1_0.txt
%{_libdir}/libboost_graph.so.%{sonamever}

%files iostreams
%license LICENSE_1_0.txt
%{_libdir}/libboost_iostreams.so.%{sonamever}

%files locale
%license LICENSE_1_0.txt
%{_libdir}/libboost_locale.so.%{sonamever}

%files log
%license LICENSE_1_0.txt
%{_libdir}/libboost_log.so.%{sonamever}
%{_libdir}/libboost_log_setup.so.%{sonamever}

%files math
%license LICENSE_1_0.txt
%{_libdir}/libboost_math_c99.so.%{sonamever}
%{_libdir}/libboost_math_c99f.so.%{sonamever}
%{_libdir}/libboost_math_c99l.so.%{sonamever}
%{_libdir}/libboost_math_tr1.so.%{sonamever}
%{_libdir}/libboost_math_tr1f.so.%{sonamever}
%{_libdir}/libboost_math_tr1l.so.%{sonamever}

%files numpy3
%license LICENSE_1_0.txt
%{_libdir}/libboost_numpy3.so.%{sonamever}

%files test
%license LICENSE_1_0.txt
%{_libdir}/libboost_prg_exec_monitor.so.%{sonamever}
%{_libdir}/libboost_unit_test_framework.so.%{sonamever}

%files program-options
%license LICENSE_1_0.txt
%{_libdir}/libboost_program_options.so.%{sonamever}

%files python3
%license LICENSE_1_0.txt
%{_libdir}/libboost_python3.so.%{sonamever}

%files python3-devel
%license LICENSE_1_0.txt
%{_libdir}/libboost_numpy3.so
%{_libdir}/libboost_python3.so

%files random
%license LICENSE_1_0.txt
%{_libdir}/libboost_random.so.%{sonamever}

%files regex
%license LICENSE_1_0.txt
%{_libdir}/libboost_regex.so.%{sonamever}

%files serialization
%license LICENSE_1_0.txt
%{_libdir}/libboost_serialization.so.%{sonamever}
%{_libdir}/libboost_wserialization.so.%{sonamever}

%files signals
%license LICENSE_1_0.txt
%{_libdir}/libboost_signals.so.%{sonamever}

%files stacktrace
%license LICENSE_1_0.txt
%{_libdir}/libboost_stacktrace_addr2line.so.%{sonamever}
%{_libdir}/libboost_stacktrace_basic.so.%{sonamever}
%{_libdir}/libboost_stacktrace_noop.so.%{sonamever}

%files system
%license LICENSE_1_0.txt
%{_libdir}/libboost_system.so.%{sonamever}

%files thread
%license LICENSE_1_0.txt
%{_libdir}/libboost_thread.so.%{sonamever}

%files timer
%license LICENSE_1_0.txt
%{_libdir}/libboost_timer.so.%{sonamever}

%files type_erasure
%license LICENSE_1_0.txt
%{_libdir}/libboost_type_erasure.so.%{sonamever}

%files wave
%license LICENSE_1_0.txt
%{_libdir}/libboost_wave.so.%{sonamever}

%files doc
%doc %{boost_docdir}/*

%files examples
%doc %{boost_examplesdir}/*

%files devel
%license LICENSE_1_0.txt
%{_includedir}/%{name}
%{_libdir}/libboost_atomic.so
%{_libdir}/libboost_chrono.so
%{_libdir}/libboost_container.so
%if %{with context}
%{_libdir}/libboost_context.so
%{_libdir}/libboost_coroutine.so
%endif
%{_libdir}/libboost_date_time.so
%if %{with context}
%{_libdir}/libboost_fiber.so
%endif
%{_libdir}/libboost_filesystem.so
%{_libdir}/libboost_graph.so
%{_libdir}/libboost_iostreams.so
%{_libdir}/libboost_locale.so
%{_libdir}/libboost_log.so
%{_libdir}/libboost_log_setup.so
%{_libdir}/libboost_math_tr1.so
%{_libdir}/libboost_math_tr1f.so
%{_libdir}/libboost_math_tr1l.so
%{_libdir}/libboost_math_c99.so
%{_libdir}/libboost_math_c99f.so
%{_libdir}/libboost_math_c99l.so
%{_libdir}/libboost_prg_exec_monitor.so
%{_libdir}/libboost_unit_test_framework.so
%{_libdir}/libboost_program_options.so
%{_libdir}/libboost_random.so
%{_libdir}/libboost_regex.so
%{_libdir}/libboost_serialization.so
%{_libdir}/libboost_wserialization.so
%{_libdir}/libboost_signals.so
%{_libdir}/libboost_stacktrace_addr2line.so
%{_libdir}/libboost_stacktrace_basic.so
%{_libdir}/libboost_stacktrace_noop.so
%{_libdir}/libboost_system.so
%{_libdir}/libboost_thread.so
%{_libdir}/libboost_timer.so
%{_libdir}/libboost_type_erasure.so
%{_libdir}/libboost_wave.so

%files static
%license LICENSE_1_0.txt
%{_libdir}/*.a
%if %{with mpich}
%{_libdir}/mpich/lib/*.a
%endif
%if %{with openmpi}
%{_libdir}/openmpi/lib/*.a
%endif

# OpenMPI packages
%if %{with openmpi}

%files openmpi
%license LICENSE_1_0.txt
%{_libdir}/openmpi/lib/libboost_mpi.so.%{sonamever}

%files openmpi-devel
%license LICENSE_1_0.txt
%{_libdir}/openmpi/lib/libboost_mpi.so
%{_libdir}/openmpi/lib/libboost_graph_parallel.so

%files openmpi-python3
%license LICENSE_1_0.txt
%{_libdir}/openmpi/lib/libboost_mpi_python3.so.%{sonamever}
%{python3_sitearch}/openmpi/boost/

%files openmpi-python3-devel
%license LICENSE_1_0.txt
%{_libdir}/openmpi/lib/libboost_mpi_python3.so

%files graph-openmpi
%license LICENSE_1_0.txt
%{_libdir}/openmpi/lib/libboost_graph_parallel.so.%{sonamever}

%endif

# MPICH packages
%if %{with mpich}

%files mpich
%license LICENSE_1_0.txt
%{_libdir}/mpich/lib/libboost_mpi.so.%{sonamever}

%files mpich-devel
%license LICENSE_1_0.txt
%{_libdir}/mpich/lib/libboost_mpi.so
%{_libdir}/mpich/lib/libboost_graph_parallel.so

%files mpich-python3
%license LICENSE_1_0.txt
%{_libdir}/mpich/lib/libboost_mpi_python3.so.%{sonamever}
%{python3_sitearch}/mpich/boost/

%files mpich-python3-devel
%license LICENSE_1_0.txt
%{_libdir}/mpich/lib/libboost_mpi_python3.so

%files graph-mpich
%license LICENSE_1_0.txt
%{_libdir}/mpich/lib/libboost_graph_parallel.so.%{sonamever}

%endif

%files build
%license LICENSE_1_0.txt
%{_datadir}/boost-build/

%files doctools
%license LICENSE_1_0.txt
%{_bindir}/quickbook
%{_datadir}/boostbook/

%files jam
%license LICENSE_1_0.txt
%{_bindir}/bjam
%{_mandir}/man1/bjam.1*

%changelog
* Wed Jun 22 2022 Jonathan Wakely <jwakely@redhat.com> - 1.66.0-13
- Remove unused libzstd-devel dependency (#2069831)
- Preserve hardening flags when building bjam

* Tue Jun 21 2022 Jonathan Wakely <jwakely@redhat.com> - 1.66.0-12
- Build with lzma and zstd support (#2069831)

* Wed Jan 20 2021 Stephan Bergmann <sbergman@redhat.com> - 1.66.0-11
- Disable openmpi and mpich for Flatpak-bundled builds (#1895928)

* Tue Aug 04 2020 Jonathan Wakely <jwakely@redhat.com> - 1.66.0-10
- Revert changes for s390x support in Boost.Context

* Fri May 29 2020 Jonathan Wakely <jwakely@redhat.com> - 1.66.0-9
- Actually apply the patches added to the spec in 1.66.0-8

* Fri May 01 2020 Jonathan Wakely <jwakely@redhat.com> - 1.66.0-8
- Add patches from IBM for s390x support in Boost.Context (#1782292)

* Fri Jan 31 2020 Jonathan Wakely <jwakely@redhat.com> - 1.66.0-8
- Add patches to fix covscan defects (#1638070)

* Tue Nov 19 2019 Jonathan Wakely <jwakely@redhat.com> - 1.66.0-7
- Add patch to annotate objects built from assembly code (#1630552)

* Tue Oct 09 2018 Jonathan Wakely <jwakely@redhat.com> - 1.66.0-6
- Add explicit Requires to subpackages that depend on other parts of boost

* Thu Sep 20 2018 Jonathan Wakely <jwakely@redhat.com> - 1.66.0-5
- Add RPM_LD_FLAGS to user-config.jam (#1630552)

* Thu Sep 06 2018 Jonathan Wakely <jwakely@redhat.com> - 1.66.0-4
- Remove libboost_python3.so and libboost_numpy3.so from boost-devel

* Wed Aug 15 2018 Jonathan Wakely <jwakely@redhat.com> - 1.66.0-3
- Remove boost-python3 and boost-numpy3 from boost metapackage (#1616244)

* Wed Jul 18 2018 Jonathan Wakely <jwakely@redhat.com> - 1.66.0-2
- Patch numpy for Python 3 (#1596468)

* Thu May 10 2018 Jonathan Wakely <jwakely@redhat.com> - 1.66.0-1
- Add patch to change shebang to python3

* Fri Apr 27 2018 Jonathan Wakely <jwakely@redhat.com> - 1.66.0-1
- Rebase to Boost 1.66.0
