

      SUBROUTINE TEST()

        USE ModuleDefs 
        USE ModuleData
        USE HeaderMod

        IMPLICIT NONE
C-----------------------------------------------------------------------
        CHARACTER*1   ANS,RNMODE,BLANK,UPCASE
        CHARACTER*6   ERRKEY,FINDCH,TRNARG
        CHARACTER*8   FNAME,DUMMY,MODELARG
        CHARACTER*12  FILEX   !,DSCSM,INPUT
        CHARACTER*30  FILEB,FILEIO,FILEIOH
        CHARACTER*78  MSG(10)
        CHARACTER*80  PATHEX
        CHARACTER*102 DSSATP
!     CHARACTER*120 INPUTX
        CHARACTER*120 FILECTL !12/11/08 control file includes path
        CHARACTER*120 PATHX
        CHARACTER*130 CHARTEST

        INTEGER       YRDOY,YRSIM,YRPLT,MDATE,YREND,YR,ISIM, YR0, ISIM0
        INTEGER       MULTI,NYRS,INCYD,YEAR,DOY,DAS,TIMDIF
        INTEGER       ERRNUM,LUNIO,TRTALL,TRTNUM,EXPNO,I,RUN
        INTEGER       YRSIM_SAVE, YRDIF, YRDOY_END !IP,IPX, 
        INTEGER       LUNBIO,LINBIO,ISECT,IFIND,LN
        INTEGER       NREPS, REPNO,END_POS, ROTNUM, TRTREP, NARG

        LOGICAL       FEXIST, DONE

        PARAMETER (ERRKEY = 'CSM   ')      
        PARAMETER (BLANK  = ' ')

C       The variable "CONTROL" is of type "ControlType".
        TYPE (ControlType) CONTROL

C       The variable "ISWITCH" is of type "SwitchType".
        TYPE (SwitchType) ISWITCH





        DONE = .FALSE.
        YRDOY_END = 9999999

!       Pick up model version for setting the name of some files
C        WRITE(ModelVerTxt,'(I2.2,I1)') Version%Major, Version%Minor

        !Delete existing output files
        CALL OPCLEAR

C        CALL GETLUN('FILEIO', LUNIO)
c        FILEIO = 'DSSAT47.INP'


      END SUBROUTINE




      SUBROUTINE ANUDDATEST()

        USE ModuleDefs 
        USE ModuleData
        USE HeaderMod



      END SUBROUTINE

C      PROGRAM MYLIB

C        CALL TEST       

C      END  PROGRAM  MYLIB
