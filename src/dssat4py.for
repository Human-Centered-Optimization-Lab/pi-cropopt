
C
C     PATHEX  ?? path to experiment file
C     FILEX   Experiment file, e.g., UFGA7801.SBX 
C     RUN     Change in date between two observations for linear interpolation 
C     RNMODE  Simulation run mode (I=Interactive, A=All treatments, 
C               B=Batch mode, E=Sensitivity, D=Debug, N=Seasonal, Q=Sequence)
C     TRTNUM  Treatment number being simulated (from FILEX) 
C     ROTNUM  ?? rotation num? 
C     CONTROL Composite variable containing variables related to control and/or 
C               timing of simulation.  The structure of the variable 
C               (ControlType) is defined in ModuleDefs.for. 
C     ISWITCH Composite variable containing switches which control flow of 
C               execution for model.  The structure of the variable 
C               (SwitchType) is defined in ModuleDefs.for. 
C

      SUBROUTINE READFILEX(
     &    PATHEX, FILEX, TRTNUM, IVARVALS, IVARNAMS)

      USE ModuleData
      USE ModuleDefs

      IMPLICIT NONE

      INCLUDE 'COMSWI.blk'
      INCLUDE 'COMIBS.blk'

C     Output variables

      INTEGER,      dimension(27) :: IVARVALS
      CHARACTER*6,  dimension(27) :: IVARNAMS

C     Input variables

      CHARACTER*  1 WMODI, RNMODE
      CHARACTER*  2 CROP
      CHARACTER*  6 VARNO
      CHARACTER*  8 MODEL, MODELARG
      CHARACTER* 10 SLNO ! this had no declaration in input_sub, but I
C     found a d declaration in a different file for 10 char
      CHARACTER* 12 FILEX
      CHARACTER* 25 TITLET
      CHARACTER* 42 CHEXTR(NAPPL) !declared as CHEXTR(NAPPL) in inputub
      CHARACTER* 80 PATHEX
      CHARACTER* 92 FILEX_P
      CHARACTER*120 FILECTL

      CHARACTER*9 WSTAT

      INTEGER RUN,NYRS,FROP,TRTN,EXPP,EXPN,TRTALL,FTYPEN,NFORC,NDOF,PMTYPE
      INTEGER LNSIM,LNCU,LNHAR,LNTIL,LNCHE,LNFLD,LNIC,LNPLT,LNIR
      INTEGER LNFER,LNRES,ROTNUM,TRTNUM,LNENV,LNSA,REPNO
      INTEGER IIRV(NAPPL)  ! this is declared as IIRV(NAPPL) in input_sub

      LOGICAL UseSimCtr

      REAL PLTFOR

      TYPE (ControlType) CONTROL
      TYPE (SwitchType)  ISWITCH

      RUN     = 1
      RNMODE  = 'B'
      ROTNUM  = 0
      REPNO   = 1
      MEWTH   = 'M'

      FILEX_P = TRIM(PATHEX)//FILEX
      CALL Join_Trim(PATHEX, FILEX, FILEX_P)

      DSSATP = TRIM(PATHEX)//'DSSATPRO.L47'

      CONTROL % REPNO = REPNO
      CONTROL % RUN = RUN
      CONTROL % YRDOY = 0
      CONTROL % FILEX   = FILEX
      CONTROL % RNMODE  = RNMODE
      CONTROL % ROTNUM  = ROTNUM
      CONTROL % TRTNUM  = TRTNUM
      CONTROL % ERRCODE = 0

      CALL PUT(CONTROL)


       CALL IPEXP (MODEL, RUN, RNMODE, FILEX,PATHEX,FILEX_P, FILECTL,
     &     SLNO,NYRS,VARNO,CROP,WMODI,
     &     FROP,TRTN,EXPP,EXPN,TITLET,TRTALL,TRTNUM,ROTNUM, 
     &     IIRV,FTYPEN,CHEXTR,NFORC,PLTFOR,NDOF,PMTYPE,
     &     LNSIM,LNCU,LNHAR,LNENV,LNTIL,LNCHE,
     &     LNFLD,LNSA,LNIC,LNPLT,LNIR,LNFER,LNRES, 
     &     CONTROL, ISWITCH, UseSimCtr, MODELARG)


      print *, '---'
      print *, WSTA
      print *, '---'

      IVARVALS(1) = RUN
      IVARVALS(2) = NYRS
      IVARVALS(3) = FROP
      IVARVALS(4) = TRTN
      IVARVALS(5) = EXPP
      IVARVALS(6) = EXPN
      IVARVALS(7) = TRTALL
      IVARVALS(8) = FTYPEN
      IVARVALS(9) = NFORC
      IVARVALS(10) = NDOF
      IVARVALS(11) = PMTYPE
      IVARVALS(12) = LNSIM
      IVARVALS(13) = LNCU
      IVARVALS(14) = LNHAR
      IVARVALS(15) = LNTIL
      IVARVALS(16) = LNCHE
      IVARVALS(17) = LNFLD
      IVARVALS(18) = LNIC
      IVARVALS(19) = LNPLT
      IVARVALS(20) = LNIR
      IVARVALS(21) = LNFER
      IVARVALS(22) = LNRES
      IVARVALS(23) = ROTNUM
      IVARVALS(24) = TRTNUM
      IVARVALS(25) = LNENV
      IVARVALS(26) = LNSA
      IVARVALS(27) = REPNO


      IVARNAMS(1) = "RUN"
      IVARNAMS(2) = "NYRS"
      IVARNAMS(3) = "FROP"
      IVARNAMS(4) = "TRTN"
      IVARNAMS(5) = "EXPP"
      IVARNAMS(6) = "EXPN"
      IVARNAMS(7) = "TRTALL"
      IVARNAMS(8) = "FTYPEN"
      IVARNAMS(9) = "NFORC"
      IVARNAMS(10) = "NDOF"
      IVARNAMS(11) = "PMTYPE"
      IVARNAMS(12) = "LNSIM"
      IVARNAMS(13) = "LNCU"
      IVARNAMS(14) = "LNHAR"
      IVARNAMS(15) = "LNTIL"
      IVARNAMS(16) = "LNCHE"
      IVARNAMS(17) = "LNFLD"
      IVARNAMS(18) = "LNIC"
      IVARNAMS(19) = "LNPLT"
      IVARNAMS(20) = "LNIR"
      IVARNAMS(21) = "LNFER"
      IVARNAMS(22) = "LNRES"
      IVARNAMS(23) = "ROTNUM"
      IVARNAMS(24) = "TRTNUM"
      IVARNAMS(25) = "LNENV"
      IVARNAMS(26) = "LNSA"
      IVARNAMS(27) = "REPNO"

      END SUBROUTINE

      SUBROUTINE PRINTTEST()

      USE ModuleData
      USE ModuleDefs

      IMPLICIT NONE

      INCLUDE 'COMSWI.blk'
      INCLUDE 'COMIBS.blk'

      print *, '***'
      print *, WSTA
      print *, '***'


      END SUBROUTINE

