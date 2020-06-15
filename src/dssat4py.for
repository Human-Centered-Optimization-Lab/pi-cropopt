
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
     &    PATHEX, FILEX, TRTNUM)

      USE ModuleData
      USE ModuleDefs

      IMPLICIT NONE

      INCLUDE 'COMSWI.blk'
      INCLUDE 'COMIBS.blk'

C     Input variables

      CHARACTER*1   RNMODE
      CHARACTER*8   MODELARG
      CHARACTER*12  FILEX   
      CHARACTER*30  FILEIO
      CHARACTER*80  PATHEX
      CHARACTER*120 FILECTL
      INTEGER ROTNUM, RUN, TRTNUM, LUNIO, REPNO

      TYPE (ControlType) CONTROL
      TYPE (SwitchType)  ISWITCH

      RUN     = 1
      RNMODE  = 'B'
      ROTNUM  = 0
      REPNO   = 1
      MEWTH   = 'M'

C      DSSATP = TRIM(PATHEX)//'DSSATPRO.L47'



      CONTROL % REPNO = REPNO
      CONTROL % RUN = RUN
      CONTROL % YRDOY = 0
      CONTROL % FILEX   = FILEX
      CONTROL % RNMODE  = RNMODE
      CONTROL % ROTNUM  = ROTNUM
      CONTROL % TRTNUM  = TRTNUM
      CONTROL % ERRCODE = 0

      CALL PUT(CONTROL)

      CALL GETLUN('FILEIO', LUNIO)
      FILEIO = 'DSSAT47.INP'

C     TODO in the future, split this into a read function and a
C     write function 

        CALL INPUT_SUB(
     &    FILECTL, FILEIO, FILEX, MODELARG, PATHEX,       !Input
     &    RNMODE, ROTNUM, RUN, TRTNUM,                    !Input
     &    ISWITCH, CONTROL)                               !Output



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


      SUBROUTINE SETWSTA(NWSTA)

      USE ModuleData
      USE ModuleDefs

      IMPLICIT NONE

      INCLUDE 'COMSWI.blk'
      INCLUDE 'COMIBS.blk'
      CHARACTER *4 NWSTA  

      WSTA = NWSTA 

      END SUBROUTINE
