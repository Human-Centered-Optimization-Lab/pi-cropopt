
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

C     --------------------------------
C     READFILEX
C     --------------------------------

      SUBROUTINE READFILEX(PATHEX, FILEX, TRTNUM)

      USE ModuleData
      USE ModuleDefs

      IMPLICIT NONE

      INCLUDE 'COMSWI.blk'
      INCLUDE 'COMIBS.blk'

C     Input variables



      INTEGER YRIC,EXPN,FROP,ISENS,LNCHE,LNCU,LNENV,LNSA,LNTIL
      INTEGER LNFER,LNFLD,LNHAR,LNIC, LNIR,LNPLT,LNRES,LNSIM,NDOF
      INTEGER NFORC,NYRS,PMTYPE,TRTN,TRTALL


      CHARACTER*1000 atline
      CHARACTER*42 CHEXTR(NAPPL)
      CHARACTER*16 VRNAME
      CHARACTER*8 MODEL
      CHARACTER*6 ECONO, VARNO
      CHARACTER*2 CROP,PRCROP

      REAL EFINOC, EFNFIX,PLTFOR,WRESND,WRESR
      REAL INO3(NL),INH4(NL)
      REAL SWINIT(NL)



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

C     --------------------------------
C     PRINTTEST
C     --------------------------------
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

C     --------------------------------
C     SETWSTA
C     --------------------------------
      SUBROUTINE SETWSTA(NWSTA)

      USE ModuleData
      USE ModuleDefs

      IMPLICIT NONE

      INCLUDE 'COMSWI.blk'
      INCLUDE 'COMIBS.blk'
      CHARACTER *4 NWSTA  

      WSTA = NWSTA 

      END SUBROUTINE

C     --------------------------------
C     WRITETEMPX
C     --------------------------------
      SUBROUTINE WRITETEMPX()

      USE ModuleData
      USE ModuleDefs

      IMPLICIT NONE

      INCLUDE 'COMSWI.blk'
      INCLUDE 'COMIBS.blk'



      INTEGER YRIC,EXPN,FROP,ISENS,LNCHE,LNCU,LNENV,LNSA,LNTIL
      INTEGER LNFER,LNFLD,LNHAR,LNIC, LNIR,LNPLT,LNRES,LNSIM,NDOF
      INTEGER NFORC,NYRS,PMTYPE,RUN,TRTN,TRTALL


      CHARACTER*1000 atline
      CHARACTER* 80 PATHEX
      CHARACTER*42 CHEXTR(NAPPL)
      CHARACTER*30  FILEIO
      CHARACTER*16 VRNAME
      CHARACTER*12  FILEX   
      CHARACTER*8 MODEL
      CHARACTER*6 ECONO, VARNO
      CHARACTER*2 CROP,PRCROP
      CHARACTER*1 RNMODE

      REAL EFINOC, EFNFIX,PLTFOR,WRESND,WRESR
      REAL INO3(NL),INH4(NL)
      REAL SWINIT(NL)
      
      PRINT *, '8888'
      print *,  FILEIO
      print *, VRNAME
      print *,  FILEX   
      print *, MODEL
      print *, ECONO, VARNO
      print *, CROP,PRCROP
      print *, RNMODE
      PRINT *, FILEIO
      print *, WSTA
      PRINT *, '8888'

C        CALL OPTEMPY2K(RNMODE,FILEX,PATHEX,
C     &            YRIC,PRCROP,WRESR,WRESND,EFINOC,EFNFIX,
C     &            SWINIT,INH4,INO3,NYRS,VARNO,VRNAME,CROP,MODEL,
C     &            RUN,FILEIO,EXPN,ECONO,FROP,TRTALL,TRTN,
C     &            CHEXTR,NFORC,PLTFOR,NDOF,PMTYPE,ISENS)
      
        CALL OPTEMPXY2K (YRIC,PRCROP,WRESR,WRESND,EFINOC,EFNFIX,
     &           SWINIT,INH4,INO3,NYRS,VARNO,VRNAME,CROP,
     &           FILEIO,FROP,ECONO,ATLINE,
     &           LNSIM,LNCU,LNHAR,LNENV,LNTIL,LNCHE,
     &           LNFLD,LNSA,LNIC,LNPLT,LNIR,LNFER,LNRES,
     &           NFORC,PLTFOR,PMTYPE,NDOF,CHEXTR, MODEL, PATHEX)



      END SUBROUTINE
