
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
     &    PATHEX, FILEX, 
     &    TRTNUM, ISWITCH)

      USE ModuleData
      USE ModuleDefs

      IMPLICIT NONE



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

      INTEGER RUN,NYRS,FROP,TRTN,EXPP,EXPN,TRTALL,FTYPEN,NFORC,NDOF,PMTYPE
      INTEGER LNSIM,LNCU,LNHAR,LNTIL,LNCHE,LNFLD,LNIC,LNPLT,LNIR
      INTEGER LNFER,LNRES,ROTNUM,TRTNUM,LNENV,LNSA,REPNO
      INTEGER IIRV(NAPPL)  ! this is declared as IIRV(NAPPL) in input_sub

      LOGICAL UseSimCtr

      REAL          PLTFOR

      TYPE (ControlType) CONTROL
      TYPE (SwitchType)  ISWITCH

      RUN = 1
      RNMODE = 'A'   ! TODO figure out if this is right
      ROTNUM = 0
      REPNO = 1

      CONTROL % REPNO = REPNO
      CONTROL % RUN = RUN
      CONTROL % YRDOY = 0
  
C     TODO Determine if I need FILEIO and DSSATP in here too
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



      END SUBROUTINE


