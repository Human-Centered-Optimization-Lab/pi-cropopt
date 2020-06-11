##########################################################################################
# CMake project file for DSSAT-CSM
##########################################################################################
# Define the project and the dependencies that it has
##########################################################################################

CMAKE_MINIMUM_REQUIRED(VERSION 2.8.5)

if("${CMAKE_SOURCE_DIR}" STREQUAL "${CMAKE_BINARY_DIR}")
   message(FATAL_ERROR "DSSAT in-source builds are not permitted. \nMake a separate folder"
   						"for building:\nmkdir build; cd build; cmake ..\nBefore that,"
   						"remove the files already created:\n"
   						"CMakeCache.txt and CMakeFiles\n")
endif("${CMAKE_SOURCE_DIR}" STREQUAL "${CMAKE_BINARY_DIR}")

PROJECT(DSSAT-CSM Fortran)

##########################################################################################
# DSSAT_VERSION
##########################################################################################

SET(MAJOR 4)
SET(MINOR 7)
SET(MODEL 5)
SET(BUILD 14)

# Get the current working branch
execute_process(
  COMMAND git rev-parse --abbrev-ref HEAD
  WORKING_DIRECTORY ${CMAKE_SOURCE_DIR}
  OUTPUT_VARIABLE BRANCH
  OUTPUT_STRIP_TRAILING_WHITESPACE
)

# Get the latest commit hash of the working branch
execute_process(
  COMMAND git log -1 --format=%H
  WORKING_DIRECTORY ${CMAKE_SOURCE_DIR}
  OUTPUT_VARIABLE GIT_COMMIT_HASH
  OUTPUT_STRIP_TRAILING_WHITESPACE
)
# Get the latest abbreviated commit hash of the working branch
execute_process(
  COMMAND git log -1 --format=%h
  WORKING_DIRECTORY ${CMAKE_SOURCE_DIR}
  OUTPUT_VARIABLE GIT_COMMIT_HASH_ABBR
  OUTPUT_STRIP_TRAILING_WHITESPACE
)

MESSAGE(STATUS "MAJOR: ${MAJOR} MINOR: ${MINOR} MODEL: ${MODEL} BUILD: ${BUILD} COMMIT: ${GIT_COMMIT_HASH_ABBR}")
MESSAGE(STATUS "BRANCH: ${BRANCH}")
MESSAGE(STATUS "COMMIT: ${GIT_COMMIT_HASH}")
# Set the version
SET(VERSION ${MAJOR}.${MINOR}.${MODEL})

IF(APPLE)
    SET(ENV{MACOSX_DEPLOYMENT_TARGET} 10.10)
ENDIF(APPLE)

##########################################################################################

# Add our local modlues to the module path
SET(CMAKE_MODULE_PATH "${CMAKE_SOURCE_DIR}/cmake/Modules/")

# Organize output files.  On Windows this also keeps .dll files next
# to the .exe files that need them, making tests easy to run.
set(CMAKE_RUNTIME_OUTPUT_DIRECTORY ${CMAKE_BINARY_DIR}/bin)
set(CMAKE_Fortran_MODULE_DIRECTORY ${CMAKE_BINARY_DIR}/mod)

# Keep Uncomment if Fortran 90 support is required
IF(NOT CMAKE_Fortran_COMPILER_SUPPORTS_F90)
    MESSAGE(FATAL_ERROR "Fortran compiler does not support F90")
ENDIF(NOT CMAKE_Fortran_COMPILER_SUPPORTS_F90)

# This INCLUDE statement executes code that sets the compile flags for DEBUG,
# RELEASE, and TESTING.  You should  review this file and make sure the flags
# are to your liking.
INCLUDE(${CMAKE_MODULE_PATH}/SetFortranFlags.cmake)

# There is an error in CMAKE with this flag for pgf90.  Unset it
GET_FILENAME_COMPONENT(FCNAME ${CMAKE_Fortran_COMPILER} NAME)
IF(FCNAME STREQUAL "pgf90")
    UNSET(CMAKE_SHARED_LIBRARY_LINK_Fortran_FLAGS)
ENDIF(FCNAME STREQUAL "pgf90")

##########################################################################################
# Define the actual files and folders that make the build
##########################################################################################

# Define the executable name and OSDefinitions file
SET(EXECUTABLE_NAME dscsm0${MAJOR}${MINOR})
configure_file(
    "/Users/iankropp/Projects/dssat-csm-os/Utilities/CSMVersion.for.in"
    "/Users/iankropp/Projects/dssat-csm-os/Utilities/CSMVersion.for"
)
IF(WIN32)
    SET(OSDefinitions "Utilities/OSDefsWINDOWS.for")
    add_definitions(-DWIN32=1})
ELSE()
    SET(DSSAT_INSTALL_DIR $CMAKE_INSTALL_PREFIX)
    SET(OSDefinitions "/Users/iankropp/Projects/dssat-csm-os/Utilities/OSDefsLINUX.for")
    configure_file(
        "/Users/iankropp/Projects/dssat-csm-os/Data/DSSATPRO.L47.in"
		"/Users/iankropp/Projects/dssat-csm-os/Data/DSSATPRO.L47"
    )
	configure_file(
		"/Users/iankropp/Projects/dssat-csm-os/Utilities/run_dssat.in"
		"/Users/iankropp/Projects/dssat-csm-os/Utilities/run_dssat"
	)
ENDIF(WIN32)

# /Users/iankropp/Projects/dssat-csm-os
# Add the source files
set(
    source_list
      "src/dssat4py.for"
      "src/mylib.for"
      "src/fart.for"
    	"${OSDefinitions}"
        "/Users/iankropp/Projects/dssat-csm-os/Utilities/CSMVersion.for"
        "/Users/iankropp/Projects/dssat-csm-os/Utilities/ModuleDefs.for"
        "/Users/iankropp/Projects/dssat-csm-os/Utilities/DATES.for"
        "/Users/iankropp/Projects/dssat-csm-os/Utilities/ERROR.for"
        "/Users/iankropp/Projects/dssat-csm-os/Utilities/Info.for"
        "/Users/iankropp/Projects/dssat-csm-os/Utilities/IPIBS.for"
        "/Users/iankropp/Projects/dssat-csm-os/Utilities/OPGeneric.for"
        "/Users/iankropp/Projects/dssat-csm-os/Utilities/OPSTRESS.for"
        "/Users/iankropp/Projects/dssat-csm-os/Utilities/OPSUM.for"
        "/Users/iankropp/Projects/dssat-csm-os/Utilities/OPVIEW.for"
        "/Users/iankropp/Projects/dssat-csm-os/Utilities/READS.for"
        "/Users/iankropp/Projects/dssat-csm-os/Utilities/RunList.for"
        "/Users/iankropp/Projects/dssat-csm-os/Utilities/CheckRunMode.f90"
        "/Users/iankropp/Projects/dssat-csm-os/Utilities/UTILS.for"
        "/Users/iankropp/Projects/dssat-csm-os/Utilities/Warning.for"
        "/Users/iankropp/Projects/dssat-csm-os/Utilities/CsvOuts/csvlinklist.f90"
        "/Users/iankropp/Projects/dssat-csm-os/Utilities/CsvOuts/csvoutput.f90" #       "/Users/iankropp/Projects/dssat-csm-os/CSM_Main/CSM.for"
        "/Users/iankropp/Projects/dssat-csm-os/CSM_Main/LAND.for"
        "/Users/iankropp/Projects/dssat-csm-os/InputModule/COMGEN.blk"
        "/Users/iankropp/Projects/dssat-csm-os/InputModule/COMIBS.blk"
        "/Users/iankropp/Projects/dssat-csm-os/InputModule/COMSOI.blk"
        "/Users/iankropp/Projects/dssat-csm-os/InputModule/COMSWI.blk"
        "/Users/iankropp/Projects/dssat-csm-os/InputModule/input_sub.for"
        "/Users/iankropp/Projects/dssat-csm-os/InputModule/INSOIL.for"
        "/Users/iankropp/Projects/dssat-csm-os/InputModule/INSTGE.for"
        "/Users/iankropp/Projects/dssat-csm-os/InputModule/INTRO.for"
        "/Users/iankropp/Projects/dssat-csm-os/InputModule/INVAR.for"
        "/Users/iankropp/Projects/dssat-csm-os/InputModule/IPCHEM.for"
        "/Users/iankropp/Projects/dssat-csm-os/InputModule/IPECO.for"
        "/Users/iankropp/Projects/dssat-csm-os/InputModule/IPENV.for"
        "/Users/iankropp/Projects/dssat-csm-os/InputModule/ipexp.for"
        "/Users/iankropp/Projects/dssat-csm-os/InputModule/IPMAN.for"
        "/Users/iankropp/Projects/dssat-csm-os/InputModule/IPSIM.for"
        "/Users/iankropp/Projects/dssat-csm-os/InputModule/IPSLIN.for"
        "/Users/iankropp/Projects/dssat-csm-os/InputModule/IPSOIL_Inp.for"
        "/Users/iankropp/Projects/dssat-csm-os/InputModule/IPTILL.for"
        "/Users/iankropp/Projects/dssat-csm-os/InputModule/IPVAR.for"
        "/Users/iankropp/Projects/dssat-csm-os/InputModule/OPGEN.for"
        "/Users/iankropp/Projects/dssat-csm-os/InputModule/OPHEAD.for"
        "/Users/iankropp/Projects/dssat-csm-os/InputModule/OPTEMPXY2K.for"
        "/Users/iankropp/Projects/dssat-csm-os/InputModule/optempy2k.for"
        "/Users/iankropp/Projects/dssat-csm-os/InputModule/PATH.for"
        "/Users/iankropp/Projects/dssat-csm-os/InputModule/WEATHR_Inp.for"
        "/Users/iankropp/Projects/dssat-csm-os/InputModule/WTHSET.for"
        "/Users/iankropp/Projects/dssat-csm-os/InputModule/SECLI.for"
        "/Users/iankropp/Projects/dssat-csm-os/InputModule/SECROP.for"
        "/Users/iankropp/Projects/dssat-csm-os/InputModule/SEFERT.for"
        "/Users/iankropp/Projects/dssat-csm-os/InputModule/SEFLD.for"
        "/Users/iankropp/Projects/dssat-csm-os/InputModule/SEFREQ.for"
        "/Users/iankropp/Projects/dssat-csm-os/InputModule/SEHARV.for"
        "/Users/iankropp/Projects/dssat-csm-os/InputModule/SEINIT.for"
        "/Users/iankropp/Projects/dssat-csm-os/InputModule/SEIRR.for"
        "/Users/iankropp/Projects/dssat-csm-os/InputModule/SENS.for"
        "/Users/iankropp/Projects/dssat-csm-os/InputModule/SEPEST.for"
        "/Users/iankropp/Projects/dssat-csm-os/InputModule/SEPLT.for"
        "/Users/iankropp/Projects/dssat-csm-os/InputModule/SERES.for"
        "/Users/iankropp/Projects/dssat-csm-os/InputModule/SESIM.for"
        "/Users/iankropp/Projects/dssat-csm-os/InputModule/SESOIL.for"
        "/Users/iankropp/Projects/dssat-csm-os/InputModule/SETIME.for"
        "/Users/iankropp/Projects/dssat-csm-os/InputModule/SEVAR.for"
        "/Users/iankropp/Projects/dssat-csm-os/InputModule/SEWTH.for"
        "/Users/iankropp/Projects/dssat-csm-os/Management/AUTHAR.for"
        "/Users/iankropp/Projects/dssat-csm-os/Management/AUTPLT.for"
        "/Users/iankropp/Projects/dssat-csm-os/Management/CHEMICAL.for"
        "/Users/iankropp/Projects/dssat-csm-os/Management/FertType_mod.for"
        "/Users/iankropp/Projects/dssat-csm-os/Management/Fert_Place.for"
        "/Users/iankropp/Projects/dssat-csm-os/Management/Flood_Irrig.for"
        "/Users/iankropp/Projects/dssat-csm-os/Management/IRRIG.for"
        "/Users/iankropp/Projects/dssat-csm-os/Management/MgmtOps.for"
        "/Users/iankropp/Projects/dssat-csm-os/Management/OM_Place.for"
        "/Users/iankropp/Projects/dssat-csm-os/Management/OpFlood.for"
        "/Users/iankropp/Projects/dssat-csm-os/Management/Paddy_Mgmt.for"
        "/Users/iankropp/Projects/dssat-csm-os/Management/Tillage.for"
        "/Users/iankropp/Projects/dssat-csm-os/Management/TillEvent.for"
        "/Users/iankropp/Projects/dssat-csm-os/Plant/plant.for"
        "/Users/iankropp/Projects/dssat-csm-os/Plant/ALOHA-Pineapple/Aloha_GROSUB.for"
        "/Users/iankropp/Projects/dssat-csm-os/Plant/ALOHA-Pineapple/Aloha_mod.f90"
        "/Users/iankropp/Projects/dssat-csm-os/Plant/ALOHA-Pineapple/Aloha_NFACTO.for"
        "/Users/iankropp/Projects/dssat-csm-os/Plant/ALOHA-Pineapple/Aloha_NUPTAK.for"
        "/Users/iankropp/Projects/dssat-csm-os/Plant/ALOHA-Pineapple/Aloha_OPGROW.f90"
        "/Users/iankropp/Projects/dssat-csm-os/Plant/ALOHA-Pineapple/Aloha_OPHARV.for"
        "/Users/iankropp/Projects/dssat-csm-os/Plant/ALOHA-Pineapple/Aloha_PHENOL.for"
        "/Users/iankropp/Projects/dssat-csm-os/Plant/ALOHA-Pineapple/Aloha_PINE.for"
        "/Users/iankropp/Projects/dssat-csm-os/Plant/ALOHA-Pineapple/Aloha_ROOTGR.for"
        "/Users/iankropp/Projects/dssat-csm-os/Plant/AROIDS/TR_Calcshk.for"
        "/Users/iankropp/Projects/dssat-csm-os/Plant/AROIDS/TR_Grosub.for"
        "/Users/iankropp/Projects/dssat-csm-os/Plant/AROIDS/TR_Ipcrop.for"
        "/Users/iankropp/Projects/dssat-csm-os/Plant/AROIDS/TR_Nfacto.for"
        "/Users/iankropp/Projects/dssat-csm-os/Plant/AROIDS/TR_Nuptak.for"
        "/Users/iankropp/Projects/dssat-csm-os/Plant/AROIDS/TR_OPGROW.for"
        "/Users/iankropp/Projects/dssat-csm-os/Plant/AROIDS/TR_Opharv.for"
        "/Users/iankropp/Projects/dssat-csm-os/Plant/AROIDS/TR_Phenol.for"
        "/Users/iankropp/Projects/dssat-csm-os/Plant/AROIDS/TR_Rootgr.for"
        "/Users/iankropp/Projects/dssat-csm-os/Plant/AROIDS/TR_SUBSTOR.for"
        "/Users/iankropp/Projects/dssat-csm-os/Plant/AROIDS/TR_Tillsub.for"
        "/Users/iankropp/Projects/dssat-csm-os/Plant/AROIDS/TR_Transpl_g.for"
        "/Users/iankropp/Projects/dssat-csm-os/Plant/AROIDS/TR_Transpl_p.for"
        "/Users/iankropp/Projects/dssat-csm-os/Plant/CANEGRO-Sugarcane/SC_Canop3.for"
        "/Users/iankropp/Projects/dssat-csm-os/Plant/CANEGRO-Sugarcane/SC_CCOUT.for"    
        "/Users/iankropp/Projects/dssat-csm-os/Plant/CANEGRO-Sugarcane/SC_CNGRO.for"
        "/Users/iankropp/Projects/dssat-csm-os/Plant/CANEGRO-Sugarcane/SC_CNG_mods.for"
        "/Users/iankropp/Projects/dssat-csm-os/Plant/CANEGRO-Sugarcane/SC_COEFFS.for"
        "/Users/iankropp/Projects/dssat-csm-os/Plant/CANEGRO-Sugarcane/SC_ETOUT.for"     
        "/Users/iankropp/Projects/dssat-csm-os/Plant/CANEGRO-Sugarcane/SC_GTP_SHOOTS.for"
        "/Users/iankropp/Projects/dssat-csm-os/Plant/CANEGRO-Sugarcane/SC_OPHARV.for"
        "/Users/iankropp/Projects/dssat-csm-os/Plant/CANEGRO-Sugarcane/SC_OUTPUT.for"
        "/Users/iankropp/Projects/dssat-csm-os/Plant/CANEGRO-Sugarcane/SC_PARTIT.for"
        "/Users/iankropp/Projects/dssat-csm-os/Plant/CANEGRO-Sugarcane/SC_PHENOL.for"
        "/Users/iankropp/Projects/dssat-csm-os/Plant/CANEGRO-Sugarcane/SC_PHOTOS.for"
        "/Users/iankropp/Projects/dssat-csm-os/Plant/CANEGRO-Sugarcane/SC_Poplt3.for"
        "/Users/iankropp/Projects/dssat-csm-os/Plant/CANEGRO-Sugarcane/SC_ROOTG.for"
        "/Users/iankropp/Projects/dssat-csm-os/Plant/CANEGRO-Sugarcane/SC_UM_WSTRESS.for"
        "/Users/iankropp/Projects/dssat-csm-os/Plant/CASUPRO-Sugarcane/CSP_CANOPY.for"
        "/Users/iankropp/Projects/dssat-csm-os/Plant/CASUPRO-Sugarcane/CSP_CASUPRO.for"
        "/Users/iankropp/Projects/dssat-csm-os/Plant/CASUPRO-Sugarcane/CSP_DEMAND.for"
        "/Users/iankropp/Projects/dssat-csm-os/Plant/CASUPRO-Sugarcane/CSP_GROW.for"
        "/Users/iankropp/Projects/dssat-csm-os/Plant/CASUPRO-Sugarcane/CSP_GROW_CANE.for"
        "/Users/iankropp/Projects/dssat-csm-os/Plant/CASUPRO-Sugarcane/CSP_HRes.for"
        "/Users/iankropp/Projects/dssat-csm-os/Plant/CASUPRO-Sugarcane/CSP_INCOMP.for"
        "/Users/iankropp/Projects/dssat-csm-os/Plant/CASUPRO-Sugarcane/CSP_INCOMP_OUT.for"
        "/Users/iankropp/Projects/dssat-csm-os/Plant/CASUPRO-Sugarcane/CSP_INPHENOL.for"
        "/Users/iankropp/Projects/dssat-csm-os/Plant/CASUPRO-Sugarcane/CSP_IPDMND_OUT.for"
        "/Users/iankropp/Projects/dssat-csm-os/Plant/CASUPRO-Sugarcane/CSP_IPPHENOL.for"
        "/Users/iankropp/Projects/dssat-csm-os/Plant/CASUPRO-Sugarcane/CSP_IPPLNT.for"
        "/Users/iankropp/Projects/dssat-csm-os/Plant/CASUPRO-Sugarcane/CSP_MOBIL.for"
        "/Users/iankropp/Projects/dssat-csm-os/Plant/CASUPRO-Sugarcane/CSP_NUPTAK.for"
        "/Users/iankropp/Projects/dssat-csm-os/Plant/CASUPRO-Sugarcane/CSP_OPGROW.for"
        "/Users/iankropp/Projects/dssat-csm-os/Plant/CASUPRO-Sugarcane/CSP_OPHARV.for"
        "/Users/iankropp/Projects/dssat-csm-os/Plant/CASUPRO-Sugarcane/CSP_PHENOL.for"
        "/Users/iankropp/Projects/dssat-csm-os/Plant/CASUPRO-Sugarcane/CSP_PHOTO.for"
        "/Users/iankropp/Projects/dssat-csm-os/Plant/CASUPRO-Sugarcane/CSP_RESPIR.for"
        "/Users/iankropp/Projects/dssat-csm-os/Plant/CASUPRO-Sugarcane/CSP_ROOTS.for"
        "/Users/iankropp/Projects/dssat-csm-os/Plant/CASUPRO-Sugarcane/CSP_SENES.for"
        "/Users/iankropp/Projects/dssat-csm-os/Plant/CASUPRO-Sugarcane/CSP_VEGGR.for"
        "/Users/iankropp/Projects/dssat-csm-os/Plant/CERES-IXIM-Maize/MZ_IX_GROSUB.for"
        "/Users/iankropp/Projects/dssat-csm-os/Plant/CERES-IXIM-Maize/MZ_IX_KNUMBER.for"
        "/Users/iankropp/Projects/dssat-csm-os/Plant/CERES-IXIM-Maize/MZ_IX_LEAFAREA.for"
        "/Users/iankropp/Projects/dssat-csm-os/Plant/CERES-IXIM-Maize/MZ_IX_NUPTAK.for"
        "/Users/iankropp/Projects/dssat-csm-os/Plant/CERES-IXIM-Maize/MZ_IX_PHENOL.for"
        "/Users/iankropp/Projects/dssat-csm-os/Plant/CERES-IXIM-Maize/MZ_IX_PHOTSYNT.for"
        "/Users/iankropp/Projects/dssat-csm-os/Plant/CERES-IXIM-Maize/MZ_IX_PLANTG.for"
        "/Users/iankropp/Projects/dssat-csm-os/Plant/CERES-IXIM-Maize/MZ_IX_RADABS.for"
        "/Users/iankropp/Projects/dssat-csm-os/Plant/CERES-IXIM-Maize/MZ_IX_RESPIR.for"
        "/Users/iankropp/Projects/dssat-csm-os/Plant/CERES-Maize/MZ_CERES.for"
        "/Users/iankropp/Projects/dssat-csm-os/Plant/CERES-Maize/MZ_GROSUB.for"
        "/Users/iankropp/Projects/dssat-csm-os/Plant/CERES-Maize/MZ_KUPTAK.for"
        "/Users/iankropp/Projects/dssat-csm-os/Plant/CERES-Maize/MZ_NFACTO.for"
        "/Users/iankropp/Projects/dssat-csm-os/Plant/CERES-Maize/MZ_NUPTAK.for"
        "/Users/iankropp/Projects/dssat-csm-os/Plant/CERES-Maize/MZ_OPGROW.for"
        "/Users/iankropp/Projects/dssat-csm-os/Plant/CERES-Maize/MZ_OPHARV.for"
        "/Users/iankropp/Projects/dssat-csm-os/Plant/CERES-Maize/MZ_OPNIT.for"
        "/Users/iankropp/Projects/dssat-csm-os/Plant/CERES-Maize/MZ_PHENOL.for"
        "/Users/iankropp/Projects/dssat-csm-os/Plant/CERES-Maize/MZ_ROOTS.for"
        "/Users/iankropp/Projects/dssat-csm-os/Plant/CERES-Millet/ML_CERES.for"
        "/Users/iankropp/Projects/dssat-csm-os/Plant/CERES-Millet/ML_GROSUB.for"
        "/Users/iankropp/Projects/dssat-csm-os/Plant/CERES-Millet/ML_NFACT.for"
        "/Users/iankropp/Projects/dssat-csm-os/Plant/CERES-Millet/ML_NUPTAK.for"
        "/Users/iankropp/Projects/dssat-csm-os/Plant/CERES-Millet/ML_OPGROW.for"
        "/Users/iankropp/Projects/dssat-csm-os/Plant/CERES-Millet/ML_opharv.for"
        "/Users/iankropp/Projects/dssat-csm-os/Plant/CERES-Millet/ML_PHASEI.for"
        "/Users/iankropp/Projects/dssat-csm-os/Plant/CERES-Millet/ML_PHENOL.for"
        "/Users/iankropp/Projects/dssat-csm-os/Plant/CERES-Millet/ML_rootgr.for"
        "/Users/iankropp/Projects/dssat-csm-os/Plant/CERES-Millet/ML_TILLSUB.for"
        "/Users/iankropp/Projects/dssat-csm-os/Plant/CERES-Rice/RICE.for"
        "/Users/iankropp/Projects/dssat-csm-os/Plant/CERES-Rice/RI_Calcshk.for"
        "/Users/iankropp/Projects/dssat-csm-os/Plant/CERES-Rice/RI_GNURSE.for"
        "/Users/iankropp/Projects/dssat-csm-os/Plant/CERES-Rice/RI_Grosub.for"
        "/Users/iankropp/Projects/dssat-csm-os/Plant/CERES-Rice/RI_Ipcrop.for"
        "/Users/iankropp/Projects/dssat-csm-os/Plant/CERES-Rice/RI_KUPTAK.for"
        "/Users/iankropp/Projects/dssat-csm-os/Plant/CERES-Rice/RI_Nfacto.for"
        "/Users/iankropp/Projects/dssat-csm-os/Plant/CERES-Rice/RI_Nuptak.for"
        "/Users/iankropp/Projects/dssat-csm-os/Plant/CERES-Rice/RI_Opgrow.for"
        "/Users/iankropp/Projects/dssat-csm-os/Plant/CERES-Rice/RI_Opharv.for"
        "/Users/iankropp/Projects/dssat-csm-os/Plant/CERES-Rice/RI_Phenol.for"
        "/Users/iankropp/Projects/dssat-csm-os/Plant/CERES-Rice/RI_Rootgr.for"
        "/Users/iankropp/Projects/dssat-csm-os/Plant/CERES-Rice/RI_Tillsub.for"
        "/Users/iankropp/Projects/dssat-csm-os/Plant/CERES-Rice/RI_Transpl_g.for"
        "/Users/iankropp/Projects/dssat-csm-os/Plant/CERES-Rice/RI_Transpl_p.for"
        "/Users/iankropp/Projects/dssat-csm-os/Plant/CERES-SharedFiles/HResCeres.for"
        "/Users/iankropp/Projects/dssat-csm-os/Plant/CERES-SharedFiles/SLigCeres.for"
        "/Users/iankropp/Projects/dssat-csm-os/Plant/CERES-Sorghum/SG_CERES.for"
        "/Users/iankropp/Projects/dssat-csm-os/Plant/CERES-Sorghum/SG_GROSUB.for"
        "/Users/iankropp/Projects/dssat-csm-os/Plant/CERES-Sorghum/SG_NFACT.for"
        "/Users/iankropp/Projects/dssat-csm-os/Plant/CERES-Sorghum/SG_NUPTAK.for"
        "/Users/iankropp/Projects/dssat-csm-os/Plant/CERES-Sorghum/SG_OPHARV.for"
        "/Users/iankropp/Projects/dssat-csm-os/Plant/CERES-Sorghum/SG_PHASEI.for"
        "/Users/iankropp/Projects/dssat-csm-os/Plant/CERES-Sorghum/SG_PHENOL.for"
        "/Users/iankropp/Projects/dssat-csm-os/Plant/CERES-Sorghum/SG_ROOTGR.for"
        "/Users/iankropp/Projects/dssat-csm-os/Plant/CERES-Sugarbeet/BS_CERES.for"
        "/Users/iankropp/Projects/dssat-csm-os/Plant/CERES-Sugarbeet/BS_GROSUB.for"
        "/Users/iankropp/Projects/dssat-csm-os/Plant/CERES-Sugarbeet/BS_NFACTO.for"
        "/Users/iankropp/Projects/dssat-csm-os/Plant/CERES-Sugarbeet/BS_NUPTAK.for"
        "/Users/iankropp/Projects/dssat-csm-os/Plant/CERES-Sugarbeet/BS_OPGROW.for"
        "/Users/iankropp/Projects/dssat-csm-os/Plant/CERES-Sugarbeet/BS_OPHARV.for"
        "/Users/iankropp/Projects/dssat-csm-os/Plant/CERES-Sugarbeet/BS_OPNIT.for"
        "/Users/iankropp/Projects/dssat-csm-os/Plant/CERES-Sugarbeet/BS_PHENOL.for"
        "/Users/iankropp/Projects/dssat-csm-os/Plant/CERES-Sugarbeet/BS_ROOTS.for"
        "/Users/iankropp/Projects/dssat-csm-os/Plant/CERES-SweetCorn/SW_FreshWt.for"
        "/Users/iankropp/Projects/dssat-csm-os/Plant/CERES-SweetCorn/SW_GROSUB.for"
        "/Users/iankropp/Projects/dssat-csm-os/Plant/CROPGRO/CANOPY.for"
        "/Users/iankropp/Projects/dssat-csm-os/Plant/CROPGRO/CROPGRO.for"
        "/Users/iankropp/Projects/dssat-csm-os/Plant/CROPGRO/DEMAND.for"
        "/Users/iankropp/Projects/dssat-csm-os/Plant/CROPGRO/FREEZE.for"
        "/Users/iankropp/Projects/dssat-csm-os/Plant/CROPGRO/FreshWt.for"
        "/Users/iankropp/Projects/dssat-csm-os/Plant/CROPGRO/GROW.for"
        "/Users/iankropp/Projects/dssat-csm-os/Plant/CROPGRO/HRes_CGRO.for"
        "/Users/iankropp/Projects/dssat-csm-os/Plant/CROPGRO/INCOMP.for"
        "/Users/iankropp/Projects/dssat-csm-os/Plant/CROPGRO/Ipphenol.for"
        "/Users/iankropp/Projects/dssat-csm-os/Plant/CROPGRO/IPPLNT.for"
        "/Users/iankropp/Projects/dssat-csm-os/Plant/CROPGRO/MOBIL.for"
        "/Users/iankropp/Projects/dssat-csm-os/Plant/CROPGRO/NFIX.for"
        "/Users/iankropp/Projects/dssat-csm-os/Plant/CROPGRO/NUPTAK.for"
        "/Users/iankropp/Projects/dssat-csm-os/Plant/CROPGRO/Opgrow.for"
        "/Users/iankropp/Projects/dssat-csm-os/Plant/CROPGRO/OPHARV.for"
        "/Users/iankropp/Projects/dssat-csm-os/Plant/CROPGRO/PHENOL.for"
        "/Users/iankropp/Projects/dssat-csm-os/Plant/CROPGRO/PHOTO.for"
        "/Users/iankropp/Projects/dssat-csm-os/Plant/CROPGRO/PlantNBal.for"
        "/Users/iankropp/Projects/dssat-csm-os/Plant/CROPGRO/PODDET.for"
        "/Users/iankropp/Projects/dssat-csm-os/Plant/CROPGRO/PODS.for"
        "/Users/iankropp/Projects/dssat-csm-os/Plant/CROPGRO/RESPIR.for"
        "/Users/iankropp/Projects/dssat-csm-os/Plant/CROPGRO/ROOTS.for"
        "/Users/iankropp/Projects/dssat-csm-os/Plant/CROPGRO/RStages.for"
        "/Users/iankropp/Projects/dssat-csm-os/Plant/CROPGRO/SDCOMP.for"
        "/Users/iankropp/Projects/dssat-csm-os/Plant/CROPGRO/SENES.for"
        "/Users/iankropp/Projects/dssat-csm-os/Plant/CROPGRO/VEGGR.for"
        "/Users/iankropp/Projects/dssat-csm-os/Plant/CSCER_CSCRP_CSCAS/CSCAS.for"
        "/Users/iankropp/Projects/dssat-csm-os/Plant/CSCER_CSCRP_CSCAS/CSCAS_Interface.for"
        "/Users/iankropp/Projects/dssat-csm-os/Plant/CSCER_CSCRP_CSCAS/CSCER.for"
        "/Users/iankropp/Projects/dssat-csm-os/Plant/CSCER_CSCRP_CSCAS/CSCERES_Interface.for"
        "/Users/iankropp/Projects/dssat-csm-os/Plant/CSCER_CSCRP_CSCAS/CSCRP.for"
        "/Users/iankropp/Projects/dssat-csm-os/Plant/CSCER_CSCRP_CSCAS/CSCRP_Interface.for"
        "/Users/iankropp/Projects/dssat-csm-os/Plant/CSCER_CSCRP_CSCAS/CSDISEASE.for"
        "/Users/iankropp/Projects/dssat-csm-os/Plant/CSCER_CSCRP_CSCAS/CSREADS.for"
        "/Users/iankropp/Projects/dssat-csm-os/Plant/CSCER_CSCRP_CSCAS/CSUTS.for"
        "/Users/iankropp/Projects/dssat-csm-os/Plant/CSYCA-Cassava/CSYCA.f90"
        "/Users/iankropp/Projects/dssat-csm-os/Plant/CSYCA-Cassava/CSYCA_Interface.for"
        "/Users/iankropp/Projects/dssat-csm-os/Plant/CSYCA-Cassava/YCA_Albedo_Check_m.f90"
        "/Users/iankropp/Projects/dssat-csm-os/Plant/CSYCA-Cassava/YCA_Control_Environment.f90"
        "/Users/iankropp/Projects/dssat-csm-os/Plant/CSYCA-Cassava/YCA_Control_Leaf.f90"
        "/Users/iankropp/Projects/dssat-csm-os/Plant/CSYCA-Cassava/YCA_Control_Photosynthesis.f90"
        "/Users/iankropp/Projects/dssat-csm-os/Plant/CSYCA-Cassava/YCA_Control_Plant.f90"
        "/Users/iankropp/Projects/dssat-csm-os/Plant/CSYCA-Cassava/YCA_Control_VPDEffect.f90"
        "/Users/iankropp/Projects/dssat-csm-os/Plant/CSYCA-Cassava/YCA_First_Trans_m.f90"
        "/Users/iankropp/Projects/dssat-csm-os/Plant/CSYCA-Cassava/YCA_Formats_m.f90"
        "/Users/iankropp/Projects/dssat-csm-os/Plant/CSYCA-Cassava/YCA_Growth.f90"
        "/Users/iankropp/Projects/dssat-csm-os/Plant/CSYCA-Cassava/YCA_Growth_Distribute.f90"
        "/Users/iankropp/Projects/dssat-csm-os/Plant/CSYCA-Cassava/YCA_Growth_Evapo.f90"
        "/Users/iankropp/Projects/dssat-csm-os/Plant/CSYCA-Cassava/YCA_Growth_Init.f90"
        "/Users/iankropp/Projects/dssat-csm-os/Plant/CSYCA-Cassava/YCA_Growth_NUptake.f90"
        "/Users/iankropp/Projects/dssat-csm-os/Plant/CSYCA-Cassava/YCA_Growth_Part.f90"
        "/Users/iankropp/Projects/dssat-csm-os/Plant/CSYCA-Cassava/YCA_Growth_Photo.f90"
        "/Users/iankropp/Projects/dssat-csm-os/Plant/CSYCA-Cassava/YCA_Growth_Rates.f90"
        "/Users/iankropp/Projects/dssat-csm-os/Plant/CSYCA-Cassava/YCA_Growth_Senesce.f90"
        "/Users/iankropp/Projects/dssat-csm-os/Plant/CSYCA-Cassava/YCA_Integrate.f90"
        "/Users/iankropp/Projects/dssat-csm-os/Plant/CSYCA-Cassava/YCA_Integ_AgesWts.f90"
        "/Users/iankropp/Projects/dssat-csm-os/Plant/CSYCA-Cassava/YCA_Integ_EndCrop.f90"
        "/Users/iankropp/Projects/dssat-csm-os/Plant/CSYCA-Cassava/YCA_Integ_HstFail.f90"
        "/Users/iankropp/Projects/dssat-csm-os/Plant/CSYCA-Cassava/YCA_Integ_LA.f90"
        "/Users/iankropp/Projects/dssat-csm-os/Plant/CSYCA-Cassava/YCA_Integ_N.f90"
        "/Users/iankropp/Projects/dssat-csm-os/Plant/CSYCA-Cassava/YCA_Integ_Nconc.f90"
        "/Users/iankropp/Projects/dssat-csm-os/Plant/CSYCA-Cassava/YCA_Integ_SeasEnd.f90"
        "/Users/iankropp/Projects/dssat-csm-os/Plant/CSYCA-Cassava/YCA_Integ_Stages.f90"
        "/Users/iankropp/Projects/dssat-csm-os/Plant/CSYCA-Cassava/YCA_Integ_WthrSum.f90"
        "/Users/iankropp/Projects/dssat-csm-os/Plant/CSYCA-Cassava/YCA_Node.f90"
        "/Users/iankropp/Projects/dssat-csm-os/Plant/CSYCA-Cassava/YCA_Output.f90"
        "/Users/iankropp/Projects/dssat-csm-os/Plant/CSYCA-Cassava/YCA_Out_CrpSim.f90"
        "/Users/iankropp/Projects/dssat-csm-os/Plant/CSYCA-Cassava/YCA_Out_Error.f90"
        "/Users/iankropp/Projects/dssat-csm-os/Plant/CSYCA-Cassava/YCA_Out_Eval.f90"
        "/Users/iankropp/Projects/dssat-csm-os/Plant/CSYCA-Cassava/YCA_Out_LfTier.f90"
        "/Users/iankropp/Projects/dssat-csm-os/Plant/CSYCA-Cassava/YCA_Out_ModFail.f90"
        "/Users/iankropp/Projects/dssat-csm-os/Plant/CSYCA-Cassava/YCA_Out_PlantSum.f90"
        "/Users/iankropp/Projects/dssat-csm-os/Plant/CSYCA-Cassava/YCA_Out_PlGrow.f90"
        "/Users/iankropp/Projects/dssat-csm-os/Plant/CSYCA-Cassava/YCA_Out_ReInit.f90"
        "/Users/iankropp/Projects/dssat-csm-os/Plant/CSYCA-Cassava/YCA_Out_Sens.f90"
        "/Users/iankropp/Projects/dssat-csm-os/Plant/CSYCA-Cassava/YCA_Out_StoreVars.f90"
        "/Users/iankropp/Projects/dssat-csm-os/Plant/CSYCA-Cassava/YCA_Out_Work.f90"
        "/Users/iankropp/Projects/dssat-csm-os/Plant/CSYCA-Cassava/YCA_Out_WrkPhenRes.f90"
        "/Users/iankropp/Projects/dssat-csm-os/Plant/CSYCA-Cassava/YCA_PrePlant.f90"
        "/Users/iankropp/Projects/dssat-csm-os/Plant/CSYCA-Cassava/YCA_RunInit.f90"
        "/Users/iankropp/Projects/dssat-csm-os/Plant/CSYCA-Cassava/YCA_SeasInit.f90"
        "/Users/iankropp/Projects/dssat-csm-os/Plant/CSYCA-Cassava/YCA_SeasInit_Final.f90"
        "/Users/iankropp/Projects/dssat-csm-os/Plant/CSYCA-Cassava/YCA_SeasInit_PlHarvDat.f90"
        "/Users/iankropp/Projects/dssat-csm-os/Plant/CSYCA-Cassava/YCA_SeasInit_ReadGeno.f90"
        "/Users/iankropp/Projects/dssat-csm-os/Plant/CSYCA-Cassava/YCA_SeasInit_ReadXfile.f90"
        "/Users/iankropp/Projects/dssat-csm-os/Plant/CSYCA-Cassava/YCA_SeasInit_SetStage.f90"
        "/Users/iankropp/Projects/dssat-csm-os/Plant/CSYCA-Cassava/YCA_SeasInit_VarInit.f90"
        "/Users/iankropp/Projects/dssat-csm-os/Plant/FORAGE/forage.for"
        "/Users/iankropp/Projects/dssat-csm-os/Plant/FORAGE/for_asmdm.for"
        "/Users/iankropp/Projects/dssat-csm-os/Plant/FORAGE/for_canopy.for"
        "/Users/iankropp/Projects/dssat-csm-os/Plant/FORAGE/for_ch2oref.for"
        "/Users/iankropp/Projects/dssat-csm-os/Plant/FORAGE/for_demand.for"
        "/Users/iankropp/Projects/dssat-csm-os/Plant/FORAGE/for_dormancy.for"
        "/Users/iankropp/Projects/dssat-csm-os/Plant/FORAGE/for_freeze.for"
        "/Users/iankropp/Projects/dssat-csm-os/Plant/FORAGE/for_grow.for"
        "/Users/iankropp/Projects/dssat-csm-os/Plant/FORAGE/for_harv.for"
        "/Users/iankropp/Projects/dssat-csm-os/Plant/FORAGE/for_hres_cgro.for"
        "/Users/iankropp/Projects/dssat-csm-os/Plant/FORAGE/for_incomp.for"
        "/Users/iankropp/Projects/dssat-csm-os/Plant/FORAGE/for_ipparm.for"
        "/Users/iankropp/Projects/dssat-csm-os/Plant/FORAGE/for_ippest.for"
        "/Users/iankropp/Projects/dssat-csm-os/Plant/FORAGE/for_ipphenol.for"
        "/Users/iankropp/Projects/dssat-csm-os/Plant/FORAGE/for_ipplnt.for"
        "/Users/iankropp/Projects/dssat-csm-os/Plant/FORAGE/for_ipprog.for"
        "/Users/iankropp/Projects/dssat-csm-os/Plant/FORAGE/for_lindm.for"
        "/Users/iankropp/Projects/dssat-csm-os/Plant/FORAGE/for_mobil.for"
        "/Users/iankropp/Projects/dssat-csm-os/Plant/FORAGE/for_nfix.for"
        "/Users/iankropp/Projects/dssat-csm-os/Plant/FORAGE/for_nuptak.for"
        "/Users/iankropp/Projects/dssat-csm-os/Plant/FORAGE/for_opgrow.for"
        "/Users/iankropp/Projects/dssat-csm-os/Plant/FORAGE/for_opharv.for"
        "/Users/iankropp/Projects/dssat-csm-os/Plant/FORAGE/for_opmob.for"
        "/Users/iankropp/Projects/dssat-csm-os/Plant/FORAGE/for_oppest.for"
        "/Users/iankropp/Projects/dssat-csm-os/Plant/FORAGE/for_opview.for"
        "/Users/iankropp/Projects/dssat-csm-os/Plant/FORAGE/for_pest.for"
        "/Users/iankropp/Projects/dssat-csm-os/Plant/FORAGE/for_pestcp.for"
        "/Users/iankropp/Projects/dssat-csm-os/Plant/FORAGE/for_phenol.for"
        "/Users/iankropp/Projects/dssat-csm-os/Plant/FORAGE/for_photo.for"
        "/Users/iankropp/Projects/dssat-csm-os/Plant/FORAGE/for_plantnbal.for"
        "/Users/iankropp/Projects/dssat-csm-os/Plant/FORAGE/for_poddet.for"
        "/Users/iankropp/Projects/dssat-csm-os/Plant/FORAGE/for_pods.for"
        "/Users/iankropp/Projects/dssat-csm-os/Plant/FORAGE/for_respir.for"
        "/Users/iankropp/Projects/dssat-csm-os/Plant/FORAGE/for_rootdm.for"
        "/Users/iankropp/Projects/dssat-csm-os/Plant/FORAGE/for_roots.for"
        "/Users/iankropp/Projects/dssat-csm-os/Plant/FORAGE/for_rstages.for"
        "/Users/iankropp/Projects/dssat-csm-os/Plant/FORAGE/for_sdcomp.for"
        "/Users/iankropp/Projects/dssat-csm-os/Plant/FORAGE/for_seeddm.for"
        "/Users/iankropp/Projects/dssat-csm-os/Plant/FORAGE/for_senmob.for"
        "/Users/iankropp/Projects/dssat-csm-os/Plant/FORAGE/for_vegdm.for"
        "/Users/iankropp/Projects/dssat-csm-os/Plant/FORAGE/for_veggr.for"
        "/Users/iankropp/Projects/dssat-csm-os/Plant/Generic-Pest/ASMDM.for"
        "/Users/iankropp/Projects/dssat-csm-os/Plant/Generic-Pest/IPPARM.for"
        "/Users/iankropp/Projects/dssat-csm-os/Plant/Generic-Pest/IPPEST.for"
        "/Users/iankropp/Projects/dssat-csm-os/Plant/Generic-Pest/IPPROG.for"
        "/Users/iankropp/Projects/dssat-csm-os/Plant/Generic-Pest/LINDM.for"
        "/Users/iankropp/Projects/dssat-csm-os/Plant/Generic-Pest/OPPEST.for"
        "/Users/iankropp/Projects/dssat-csm-os/Plant/Generic-Pest/PEST.for"
        "/Users/iankropp/Projects/dssat-csm-os/Plant/Generic-Pest/PESTCP.for"
        "/Users/iankropp/Projects/dssat-csm-os/Plant/Generic-Pest/ROOTDM.for"
        "/Users/iankropp/Projects/dssat-csm-os/Plant/Generic-Pest/SEEDDM.for"
        "/Users/iankropp/Projects/dssat-csm-os/Plant/Generic-Pest/VEGDM.for"
        "/Users/iankropp/Projects/dssat-csm-os/Plant/Generic-PlantP/OpPlantP.for"
        "/Users/iankropp/Projects/dssat-csm-os/Plant/Generic-PlantP/PPlantSubs.for"
        "/Users/iankropp/Projects/dssat-csm-os/Plant/Generic-PlantP/P_CASUPRO.for"
        "/Users/iankropp/Projects/dssat-csm-os/Plant/Generic-PlantP/P_CERES.for"
        "/Users/iankropp/Projects/dssat-csm-os/Plant/Generic-PlantP/P_CGRO.for"
        "/Users/iankropp/Projects/dssat-csm-os/Plant/Generic-PlantP/P_IPPLNT.for"
        "/Users/iankropp/Projects/dssat-csm-os/Plant/Generic-PlantP/P_Plant.for"
        "/Users/iankropp/Projects/dssat-csm-os/Plant/Generic-PlantP/P_Uptake.for"
        "/Users/iankropp/Projects/dssat-csm-os/Plant/Generic-PlantP/RootSoilVol.for"
        "/Users/iankropp/Projects/dssat-csm-os/Plant/NTEF/TF_APSIM.for"
        "/Users/iankropp/Projects/dssat-csm-os/Plant/NTEF/TF_COLD.for"
        "/Users/iankropp/Projects/dssat-csm-os/Plant/NTEF/TF_GROSUB.for"
        "/Users/iankropp/Projects/dssat-csm-os/Plant/NTEF/TF_KUPTAK.for"
        "/Users/iankropp/Projects/dssat-csm-os/Plant/NTEF/TF_module.f90"
        "/Users/iankropp/Projects/dssat-csm-os/Plant/NTEF/TF_NFACTO.for"
        "/Users/iankropp/Projects/dssat-csm-os/Plant/NTEF/TF_NUPTAK.for"
        "/Users/iankropp/Projects/dssat-csm-os/Plant/NTEF/TF_OPGROW.for"
        "/Users/iankropp/Projects/dssat-csm-os/Plant/NTEF/TF_OPHARV.for"
        "/Users/iankropp/Projects/dssat-csm-os/Plant/NTEF/TF_OPNIT.for"
        "/Users/iankropp/Projects/dssat-csm-os/Plant/NTEF/TF_PHENOL.for"
        "/Users/iankropp/Projects/dssat-csm-os/Plant/NTEF/TF_ROOTS.for"
        "/Users/iankropp/Projects/dssat-csm-os/Plant/NTEF/TF_SW_SUBS.for"
        "/Users/iankropp/Projects/dssat-csm-os/Plant/NTEF/TF_temp.for"
        "/Users/iankropp/Projects/dssat-csm-os/Plant/NWHEAT/WH_APSIM.for"
        "/Users/iankropp/Projects/dssat-csm-os/Plant/NWHEAT/WH_COLD.for"
        "/Users/iankropp/Projects/dssat-csm-os/Plant/NWHEAT/WH_GROSUB.for"
        "/Users/iankropp/Projects/dssat-csm-os/Plant/NWHEAT/WH_KUPTAK.for"
        "/Users/iankropp/Projects/dssat-csm-os/Plant/NWHEAT/WH_module.f90"
        "/Users/iankropp/Projects/dssat-csm-os/Plant/NWHEAT/WH_NFACTO.for"
        "/Users/iankropp/Projects/dssat-csm-os/Plant/NWHEAT/WH_NUPTAK.for"
        "/Users/iankropp/Projects/dssat-csm-os/Plant/NWHEAT/WH_OPGROW.for"
        "/Users/iankropp/Projects/dssat-csm-os/Plant/NWHEAT/WH_OPHARV.for"
        "/Users/iankropp/Projects/dssat-csm-os/Plant/NWHEAT/WH_OPNIT.for"
        "/Users/iankropp/Projects/dssat-csm-os/Plant/NWHEAT/WH_PHENOL.for"
        "/Users/iankropp/Projects/dssat-csm-os/Plant/NWHEAT/WH_ROOTS.for"
        "/Users/iankropp/Projects/dssat-csm-os/Plant/NWHEAT/WH_SW_SUBS.for"
        "/Users/iankropp/Projects/dssat-csm-os/Plant/NWHEAT/WH_temp.for"
        "/Users/iankropp/Projects/dssat-csm-os/Plant/SUBSTOR-Potato/PT_GROSUB.for"
        "/Users/iankropp/Projects/dssat-csm-os/Plant/SUBSTOR-Potato/PT_NFACTO.for"
        "/Users/iankropp/Projects/dssat-csm-os/Plant/SUBSTOR-Potato/PT_NUPTAK.for"
        "/Users/iankropp/Projects/dssat-csm-os/Plant/SUBSTOR-Potato/PT_OPGROW.for"
        "/Users/iankropp/Projects/dssat-csm-os/Plant/SUBSTOR-Potato/PT_OPHARV.for"
        "/Users/iankropp/Projects/dssat-csm-os/Plant/SUBSTOR-Potato/PT_PHASEI.for"
        "/Users/iankropp/Projects/dssat-csm-os/Plant/SUBSTOR-Potato/PT_PHENOL.for"
        "/Users/iankropp/Projects/dssat-csm-os/Plant/SUBSTOR-Potato/PT_ROOTGR.for"
        "/Users/iankropp/Projects/dssat-csm-os/Plant/SUBSTOR-Potato/PT_SUBSTOR.for"
        "/Users/iankropp/Projects/dssat-csm-os/Plant/SUBSTOR-Potato/PT_THTIME.for"
        "/Users/iankropp/Projects/dssat-csm-os/Soil/SOIL.for"
        "/Users/iankropp/Projects/dssat-csm-os/Soil/CENTURY_OrganicMatter/CENTURY.for"
        "/Users/iankropp/Projects/dssat-csm-os/Soil/CENTURY_OrganicMatter/CE_RATIO_C.for"
        "/Users/iankropp/Projects/dssat-csm-os/Soil/CENTURY_OrganicMatter/DECRAT_C.for"
        "/Users/iankropp/Projects/dssat-csm-os/Soil/CENTURY_OrganicMatter/EFLOW_C.for"
        "/Users/iankropp/Projects/dssat-csm-os/Soil/CENTURY_OrganicMatter/IMMOBLIMIT_C.for"
        "/Users/iankropp/Projects/dssat-csm-os/Soil/CENTURY_OrganicMatter/INCORPOR_C.for"
        "/Users/iankropp/Projects/dssat-csm-os/Soil/CENTURY_OrganicMatter/IPHedley_C.for"
        "/Users/iankropp/Projects/dssat-csm-os/Soil/CENTURY_OrganicMatter/LITDEC_C.for"
        "/Users/iankropp/Projects/dssat-csm-os/Soil/CENTURY_OrganicMatter/NCHECK_C.for"
        "/Users/iankropp/Projects/dssat-csm-os/Soil/CENTURY_OrganicMatter/OPSOMLIT_C.for"
        "/Users/iankropp/Projects/dssat-csm-os/Soil/CENTURY_OrganicMatter/PARTIT_C.for"
        "/Users/iankropp/Projects/dssat-csm-os/Soil/CENTURY_OrganicMatter/RPLACE_C.for"
        "/Users/iankropp/Projects/dssat-csm-os/Soil/CENTURY_OrganicMatter/SENESADD_C.for"
        "/Users/iankropp/Projects/dssat-csm-os/Soil/CENTURY_OrganicMatter/SoilCNPinit_C.for"
        "/Users/iankropp/Projects/dssat-csm-os/Soil/CENTURY_OrganicMatter/SoilNoBal_C.for"
        "/Users/iankropp/Projects/dssat-csm-os/Soil/CENTURY_OrganicMatter/SoilPoBal_C.for"
        "/Users/iankropp/Projects/dssat-csm-os/Soil/CENTURY_OrganicMatter/SOMDEC_C.for"
        "/Users/iankropp/Projects/dssat-csm-os/Soil/CENTURY_OrganicMatter/SOMFIX_C.for"
        "/Users/iankropp/Projects/dssat-csm-os/Soil/CENTURY_OrganicMatter/SOMINIT_c.for"
        "/Users/iankropp/Projects/dssat-csm-os/Soil/CENTURY_OrganicMatter/SOMLITPRINT_C.for"
        "/Users/iankropp/Projects/dssat-csm-os/Soil/CENTURY_OrganicMatter/TSOMLIT_C.for"
        "/Users/iankropp/Projects/dssat-csm-os/Soil/CERES_OrganicMatter/NCHECK_organic.for"
        "/Users/iankropp/Projects/dssat-csm-os/Soil/CERES_OrganicMatter/OpSoilOrg.for"
        "/Users/iankropp/Projects/dssat-csm-os/Soil/CERES_OrganicMatter/SoilOrg.for"
        "/Users/iankropp/Projects/dssat-csm-os/Soil/CERES_OrganicMatter/SoilOrg_init.for"
        "/Users/iankropp/Projects/dssat-csm-os/Soil/FloodN/FCHEM.for"
        "/Users/iankropp/Projects/dssat-csm-os/Soil/FloodN/FLOODI.for"
        "/Users/iankropp/Projects/dssat-csm-os/Soil/FloodN/Flood_Chem.for"
        "/Users/iankropp/Projects/dssat-csm-os/Soil/FloodN/OPFLOODN.for"
        "/Users/iankropp/Projects/dssat-csm-os/Soil/GHG/Denit_Ceres.for"
        "/Users/iankropp/Projects/dssat-csm-os/Soil/GHG/Denit_DayCent.for"
        "/Users/iankropp/Projects/dssat-csm-os/Soil/GHG/diffusiv.for"
        "/Users/iankropp/Projects/dssat-csm-os/Soil/GHG/N2O_mod.for"
        "/Users/iankropp/Projects/dssat-csm-os/Soil/GHG/nox_pulse.f90"
        "/Users/iankropp/Projects/dssat-csm-os/Soil/Inorganic_K/OpSoilKi.for"
        "/Users/iankropp/Projects/dssat-csm-os/Soil/Inorganic_K/SoilKi.for"
        "/Users/iankropp/Projects/dssat-csm-os/Soil/Inorganic_K/SoilK_init.for"
        "/Users/iankropp/Projects/dssat-csm-os/Soil/Inorganic_N/EQUIL2.for"
        "/Users/iankropp/Projects/dssat-csm-os/Soil/Inorganic_N/NCHECK_inorg.for"
        "/Users/iankropp/Projects/dssat-csm-os/Soil/Inorganic_N/NFLUX.for"
        "/Users/iankropp/Projects/dssat-csm-os/Soil/Inorganic_N/OPSOILNI.for"
        "/Users/iankropp/Projects/dssat-csm-os/Soil/Inorganic_N/OXLAYER.for"
        "/Users/iankropp/Projects/dssat-csm-os/Soil/Inorganic_N/SOILNI.for"
        "/Users/iankropp/Projects/dssat-csm-os/Soil/Inorganic_N/SoilNiBal.for"
        "/Users/iankropp/Projects/dssat-csm-os/Soil/Inorganic_N/SoilNi_init.for"
        "/Users/iankropp/Projects/dssat-csm-os/Soil/Inorganic_P/IPHedley_inorg.for"
        "/Users/iankropp/Projects/dssat-csm-os/Soil/Inorganic_P/OpSoilPi.for"
        "/Users/iankropp/Projects/dssat-csm-os/Soil/Inorganic_P/SoilPi.for"
        "/Users/iankropp/Projects/dssat-csm-os/Soil/Inorganic_P/SoilPiBal.for"
        "/Users/iankropp/Projects/dssat-csm-os/Soil/Inorganic_P/SoilPi_init.for"
        "/Users/iankropp/Projects/dssat-csm-os/Soil/Mulch/MULCHEVAP.for"
        "/Users/iankropp/Projects/dssat-csm-os/Soil/Mulch/MULCHLAYER.for"
        "/Users/iankropp/Projects/dssat-csm-os/Soil/Mulch/MULCHWAT.for"
        "/Users/iankropp/Projects/dssat-csm-os/Soil/Mulch/OPMULCH.for"
        "/Users/iankropp/Projects/dssat-csm-os/Soil/SoilUtilities/IPSOIL.for"
        "/Users/iankropp/Projects/dssat-csm-os/Soil/SoilUtilities/LMATCH.for"
        "/Users/iankropp/Projects/dssat-csm-os/Soil/SoilUtilities/SoilCBal.for"
        "/Users/iankropp/Projects/dssat-csm-os/Soil/SoilUtilities/SOILDYN.for"
        "/Users/iankropp/Projects/dssat-csm-os/Soil/SoilUtilities/SoilMixing.for"
        "/Users/iankropp/Projects/dssat-csm-os/Soil/SoilUtilities/SoilNBalSum.for"
        "/Users/iankropp/Projects/dssat-csm-os/Soil/SoilUtilities/SoilNoPoBal.for"
        "/Users/iankropp/Projects/dssat-csm-os/Soil/SoilUtilities/SoilPBalSum.for"
        "/Users/iankropp/Projects/dssat-csm-os/Soil/SoilUtilities/TextureClass.for"
        "/Users/iankropp/Projects/dssat-csm-os/Soil/SoilWater/INFIL.for"
        "/Users/iankropp/Projects/dssat-csm-os/Soil/SoilWater/OPWBAL.for"
        "/Users/iankropp/Projects/dssat-csm-os/Soil/SoilWater/RETC_VG.for"
        "/Users/iankropp/Projects/dssat-csm-os/Soil/SoilWater/RNOFF.for"
        "/Users/iankropp/Projects/dssat-csm-os/Soil/SoilWater/SATFLO.for"
        "/Users/iankropp/Projects/dssat-csm-os/Soil/SoilWater/TILEDRAIN.for"
        "/Users/iankropp/Projects/dssat-csm-os/Soil/SoilWater/WATBAL.for"
        "/Users/iankropp/Projects/dssat-csm-os/Soil/SoilWater/WBAL.for"
        "/Users/iankropp/Projects/dssat-csm-os/Soil/SoilWater/WBSUBS.for"
        "/Users/iankropp/Projects/dssat-csm-os/SPAM/ESR_SoilEvap.for"
        "/Users/iankropp/Projects/dssat-csm-os/SPAM/ETPHOT.for"
        "/Users/iankropp/Projects/dssat-csm-os/SPAM/ETPHR.for"
        "/Users/iankropp/Projects/dssat-csm-os/SPAM/OPETPHOT.for"
        "/Users/iankropp/Projects/dssat-csm-os/SPAM/OpStemp.for"
        "/Users/iankropp/Projects/dssat-csm-os/SPAM/PET.for"
        "/Users/iankropp/Projects/dssat-csm-os/SPAM/ROOTWU.for"
        "/Users/iankropp/Projects/dssat-csm-os/SPAM/SAL_Stemp.for"
        "/Users/iankropp/Projects/dssat-csm-os/SPAM/SOILEV.for"
        "/Users/iankropp/Projects/dssat-csm-os/SPAM/SPAM.for"
        "/Users/iankropp/Projects/dssat-csm-os/SPAM/SPSUBS.for"
        "/Users/iankropp/Projects/dssat-csm-os/SPAM/STEMP.for"
        "/Users/iankropp/Projects/dssat-csm-os/SPAM/STEMP_EPIC.for"
        "/Users/iankropp/Projects/dssat-csm-os/SPAM/TRANS.for"
        "/Users/iankropp/Projects/dssat-csm-os/Weather/CO2VAL.for"
        "/Users/iankropp/Projects/dssat-csm-os/Weather/HMET.for"
        "/Users/iankropp/Projects/dssat-csm-os/Weather/IPWTH_alt.for"
        "/Users/iankropp/Projects/dssat-csm-os/Weather/OPWEATH.for"
        "/Users/iankropp/Projects/dssat-csm-os/Weather/SOLAR.for"
        "/Users/iankropp/Projects/dssat-csm-os/Weather/weathr.for"
        "/Users/iankropp/Projects/dssat-csm-os/Weather/WGEN.for"
        "/Users/iankropp/Projects/dssat-csm-os/Weather/WTHMOD.for"
)
ADD_EXECUTABLE(${EXECUTABLE_NAME} ${source_list})

foreach(source IN LISTS source_list)
    get_filename_component(source_path "${source}" PATH)
    string(REPLACE "/" "\\" source_path_msvc "${source_path}")
    source_group("${source_path_msvc}" FILES "${source}")
endforeach()

ADD_LIBRARY(dssat4py SHARED ${source_list})
#install(TARGETS ${EXECUTABLE_NAME} DESTINATION
#  RUNTIME DESTINATION .)

install(FILES Utilities/run_dssat DESTINATION .
	PERMISSIONS OWNER_READ OWNER_WRITE OWNER_EXECUTE GROUP_READ GROUP_EXECUTE WORLD_READ WORLD_EXECUTE
	)

install(DIRECTORY Data/ DESTINATION .
	PATTERN "*.in" EXCLUDE)

##################################################
# Resume information about flags and option used #
##################################################

message( "-- Flags" )
message( "   FFLAGS       ${CMAKE_Fortran_FLAGS}" )
message( "   RELEASE      ${CMAKE_Fortran_FLAGS_RELEASE}" )
message( "   DEBUG        ${CMAKE_Fortran_FLAGS_DEBUG}")
message( "   LINKER       ${CMAKE_EXE_LINKER_FLAGS}")
message( "-- Build Info" )
message( "   BUILD TYPE   ${CMAKE_BUILD_TYPE}" )
message( "   VERSION      ${MAJOR}.${MINOR}.${MODEL}.${BUILD}" )
message( "   I. PREFIX    ${CMAKE_INSTALL_PREFIX}" )
message( "   Executable   ${EXECUTABLE_NAME}" )
