# used on Windows July 21, 2024

import logging
import unittest
import pytest
import sys
import math
from datetime import datetime
from dateutil import parser
import math
from os.path import join


logging.basicConfig(filename = 'CSVsamp.log',level=logging.INFO)
logging.info(40*'=')
logging.info(f"Sample Taken {datetime.now()} ")

MAXSTR = 20000 # as data input
MAXCELLPTR = 10 # maximum default cell contents print
MAXSAMP = 10000000
# MAXSAMP =80 # for debugging
EMPTYSTR = ""
WIN10 = True


class CSVcoors:
   """
   Coordinats for a CSVspreadsheet
   """
   def __init__(self,currow=1,curcol=1):
       self.currow = currow
       self.curcol = curcol
   def __str__(self):
       return f"({self.curcol},{self.curcol})"
   def incRow(self,incsize = 1):
       self.currow += incsize
       self.curcol = 1
   def incCol(self,incsize = 1):
       self.curcol += incsize   
   def __eq__(self,other):
       if isinstance(other,CSVcoors):
           return self.currow == other.currow and self.curcol == other.curcol 

class CSVsampCell:
   """
   Data for spreadsheet cell
   """
   def __init__(self,currow=1,curcol=1):
       """
       Basic initialization for cell
       """
       # the cell is reused frequently
       self.reset()
       self.linecomplete = False
       # if this object is created then there must be at least one cell
       self.coord = CSVcoors(currow,curcol)
       
       self.eof = False

              
   def reset(self,newrow=False,newcol=False):
       """ Reinitialize storage before processing cell """
       self.cellcomplete = False
       # cellbuf is an array of characters
       self.dataBuf = []
       # data is string
       self.dataStr = str(EMPTYSTR)
       self.charno = 0
       # used for two byte characters
       self.lastchar = ''
       self.eol = False
       if newrow:
           self.coord.incRow()
           self.linecomplete = False
       if newcol:
           inc.coord.incCol()
     
           

   def getCellStr(self): 
       """
       Converts arrary of characters in cellbuf to string

       Returns:
       str: array of characters in databuf as a string
       """ 

       self.dataStr = ''.join(self.dataBuf)

       return self.dataStr

   def __len__(self):
       return len(self.dataStr)

   def __str__(self,maxprint = MAXCELLPTR):
       """
       print up to maxprint character of cell data as string
       """
       if len(self.dataStr) > maxprint:
           retval = self.dataStr[:maxprint]
       else:
           retval = str(self.dataStr)

       return retval
         
               
 
   def addchar(self,achar):
       """
       collects characters to load into cellbuf
       special characters may require two passes
       """
       if self.lastchar == '/' and achar == 'n':
           # will need to be revised for linux
           achar == '\n'
           self.lastchar = ' '
       if achar == '/':
           # in windows not escape likely part of date
           pass
       if achar == ',': 
           self.cellcomplete = True
           return self.charno
       if achar == '\n':
           self.eol = True
           self.cellcomplete = True
           self.linecomplete = True
           return self.charno
       self.dataBuf += achar
       self.charno += 1
       
       return self.charno

class CumClass:
   def __init__(self,SrcCol=1):
       self.minchar = 100
       self.maxchar = 0
       self.misschar = "NA"
       # records missing data in sample range
       self.NAcnt = 0
       # records read in sample range
       self.recno = 0
       # column being accumulated
       self.SrcCol = SrcCol

   # two access functions
   # must be a better way
   def getrecno(self):
       return self.recno    
   def getnano(self):
       return self.NAcnt 

   def __str__(self):
       return f"cumulant with {self.recno} records and {self.NAcnt} NAs"

   def addCol(self,colno,coltype):
       """
       add column for accumulation
       returns the accumlation object which can be added to the dictionary
       Note that self for CSVsamp will be added and complement the alternative selfs
       """
       # originally done in primary CSVsampFile object
       # moved here during debug process 
       


   def addCell(self,DatStr):
       """
       Add cell data for cumulation processes
       """
       thelen = len(str(DatStr))
       if (thelen == 0):
           self.NAcnt += 1
           return False
       if thelen < self.minchar:
           self.minchar = thelen
       if thelen > self.maxchar:
           self.maxchar = thelen
       self.recno += 1
       return True 

   def SumIt(self):
       """
       Column specific accumulation info
       """
       recstr = f'{str(self.recno)} records were processed with {str(self.NAcnt)} missing \n'
       return recstr 

class CatCum(CumClass):
   """
   Cumulation class for column of categories
   """
   def __init__(self,SrcCol=1,CumArgs=''): 
       super().__init__(SrcCol)
       # catDict will contain catgories for the one column
       self.catDict = dict()
       # if category used not in dict
       self.catDict['NoCat']=0
       # number of categories being counted
       self.catnum = 1
       # test to see if the parent value if over writes
       self.colno = SrcCol

   def __str__(self):
       return f"cumulant category with potential {self.catnum} categories including Not Categorized"

   def addCat(self,catName):
       """
       add category used for counting

       """
       self.catDict[str(catName)] = 0
       self.catnum += 1
       print('*** 178',self.catDict)
       return self.catnum

   def addcelldata(self,celldata):
       """
       process cell data as a category
       return true if successfull
              false if fails fails for an reason
       """
       try:
           # all categories treated as numbers
           thecat = str(celldata) 
           print('*** 210 >',celldata,'<')
           print('*** 211 len of 210 should be one len=',len(celldata))
           super().addCell(thecat)
           print('*** 213 after super.addCell')
           catName = str(celldata) 
           print('*** 215 catName= ',catName)
           print('*** 216 catDict = ',self.catDict)
           catData = self.catDict[catName]
           print('*** 217',catData)
           # if category found increase by one
           self.catDict[str(catName)] = int(catData) + 1
           print('*** 220 ',self.catDict[str(catName)]) 
           return True
       except Exception as e:
           retval = self.catDict['NoCat']
           self.catDict['NoCat'] = (int(retval) + 1)
           logging.exception('Failed to process category ',repr(e))
           return False
   def SumIt(self):
       retval = super().SumIt()  
       retval += f'the column had {self.catDict["NoCat"]} unused categories'
       print(retval)


class DateCum(CumClass):
   """
   Cumulation class for a date column
   """
   def __init__(self,CumArgs=''): 
       super().__init__()
       self.minDate = None
       self.maxDate = None
       self.SepLst = list(('-','','/'))
       self.SepDef = '-'
       # DfFmt list of current possible Date formats
       self.DfFmt = list(('%Y-%m-%d','%d/%m/%y'))
       if CumArgs != '':
           FmtInt=int(CumArgs)
       else:
           FmtInt = 0
       self.TheDtFmt = self.DfFmt[FmtInt]
       self.isCumDate = True
   def addcelldata(self,celldata):
       """
       process cell data as a date
       return true if successfull
              false if fails fails for an reason
       """
       try:
           thedate = datetime.strptime(celldata, self.TheDtFmt).date()
           super().addCell(thedate) 
           if self.minDate is None :
               print('*** 151 ')
               self.minDate = thedate
           else:
               if self.minDate > thedate:
                   self.minDate = thedate
           if self.maxDate is None :
               self.maxDate = thedate
           else:
               if self.maxDate < thedate :
                   self.maxDate = thedate
           print('*** 156 after addcelldata min= ', self.minDate,' max=',self.maxDate) 
           return True
       except Exception as e:
           # logging.error('Failed to process date',repr(e))
           return False
   def SumIt(self):
       print('*** 161 to invoke Sumit for date class')
       retval = super().SumIt()  
       retval += f'the date records had a minimum of {self.minDate}'
       retval += f'    and a maximum of {self.maxDate}'
       print(retval)
   
class NumCum(CumClass):
   """
   Cumulation class for numeric column
   """
   def __init__(self,CumArgs=''):
       super().__init__()
       print('*** 259',self.NAcnt)
       self.minNum = math.nan
       self.maxNum = math.nan
       self.total = 0
   def addcelldata(self,celldata):
       """
       process cell data as a numeric value
       return true if successfull
              false if it fails for any reason
       """
       try:
           print('*** 144 in addcelldata celldata=',celldata)
           print('*** 145', self.minNum)
           thenum = float(celldata)
           self.total += thenum
           if math.isnan(self.minNum) :
               self.minNum = thenum
           else:
               self.minNum = min(self.minNum,thenum)
           print('*** 182 self.minNum',self.minNum)
           if math.isnan(self.maxNum)  :
               self.maxNum = thenum
           else:
               self.maxNum = max(self.maxNum,thenum)           
           print('*** 187 min max',self.minNum,self.maxNum)
           super().addCell(str(thenum))
           print('*** 189 just added colunn specific data recno = ',super().recno)
           return True
       except:         
           return False
  
   def SumIt(self):
       print('*** 143 tryint to invoke Sumit')
       retval = super().SumIt()
       recno = super().getrecno()
       nano = super().getnano()
       print('*** 294 trying to invoke Sumit ',recno)
       print('*** 295 trying to invoke Sumit ',nano)
       if recno != 0:
           meanval = self.total/recno
           retval += f'the quantitative records had a mean of {meanval}'
       else:
           retval += f'mean is Not Available'
       print(retval)     

       

class CSVsampFile: 
   def __init__(self,InPth,outfile='Samp.csv'):
       self.setTarget(0,math.nan,0,math.nan,1.0)
       # cell object
       self.CSVsampCell = CSVsampCell()
       # list of cells to be output to outfile
       self.sampLst = []
       # max number of cells before output
       self.SAMPBUF = math.nan
       # input file to be sampled from
       self.InPth = InPth
       self.InHdl = None  # initialize Python file object to isNone
       self.currow = 0 # address in current session
       self.curcol = 0 # address in current session
       # parameters used to specify session
       self.InCntRow = 0 # set to number of rows used as headers
       self.InMaxRow = self.InCntRow # number of rows read
       # number of columns in the widest apparent row
       self.InMaxCol = 0
       # output file to store the sampled
       self.OutPth = outfile
       self.OutHdl = None
       self.retstr = "" 
       self.cummod = ['asDate','asQuant','asCat'] 
       # dictionary of cummods
       self.CumDict = dict()
       self.cumErrs = 0   

   def __del__(self):
       try:
           self.InHdl.close()
           self.OutHdl.close()
       finally:
           print('Files closed')
       
   def setCumField(self,colno,cumAs,CumArgs=''):
       """
       Load cummulation field for colno in CumDict
       return True on success
       """
       if cumAs == 'asDate' :
           theDatCum = DateCum(CumArgs)
           self.CumDict[int(colno)] = theDatCum
           return True
       if cumAs == 'asQuant' :
           theNumCum = NumCum(CumArgs)
           self.CumDict[int(colno)] = theNumCum
           return True
       if cumAs == 'asCat' :
           # testing the passing of parent 'self' to child
           theCatCum = CatCum(colno,CumArgs)
           self.CumDict[int(colno)] = theCatCum
           return True   
       logging.warning(f"Will not cumulate column #  {colno} ")
       return False 

   def setTarget(self,minrow,maxrow,mincol,maxcol,samprob):
       """
       Designate data to be save as a sample.
       """
       self.minrow = minrow
       self.maxrow = maxrow
       self.mincol = mincol
       self.maxcol = maxcol 
       self.samprob = samprob
       logging.info(f"target range set to , {(minrow,mincol,maxrow,maxcol)}")
       
       return True

   def __del__(self):

       try:
           self.InHdl.close()
           logging.info(f"File '{self.InPth}' has been closed.")
       except:
           logging.warning(f"Unable to close '{self.InPth}' ")
       try:
           self.OutHdl.close()
           logging.info(f"File '{self.OutPth}' has been closed.")
       except:
           logging.warning(f"Unable to close '{self.OutPth}' ")     

   def __str__(self):
       return f'{self.InCntRow} rows, {self.InMaxCol} fields'

   def openInPath(self):
      
       try:
           self.InHdl = open(self.InPth,'r')
           logging.info(f'opened input file {self.InPth}')
           # use to initialize cell buffer
           self.linecomplete = False
           return True
       except IOError:
           logging.warning(f'Could not open InPath {self.InPth}')
           return False

   def openOutPath(self):

       try:       
           self.OutHdl = open(self.OutPth,'w')
           logging.info(f'opened output file {self.OutPth}')
           return True
       except IOError:
           logging.warning(f'Could not open outpath {self.OutPth}')
           return False                      


   
   def isInSamp(self,therow:int,thecol:int):

        """  
        Determine if therow and thecol are within the sample
        return Boolean
        """
       
        if therow < self.minrow:
           return False
        if therow > self.maxrow:
           return False
        if thecol < self.mincol:
           return False
        if thecol > self.maxcol:
           return False

        print('*** 382 isInSamp therow= ',therow,' thecol=',thecol)   
        return True

   def getCellBuff(self):

       """
       Manage byte level I/O with CSV file
       assume file self.InHdl already for read acccess
       will load data into self.cellbuf
       return True upon completion
       """
       self.thecell.reset() 
       thebyte = self.InHdl.read(1)
       self.thecell.charno += 1
       self.thecell.addchar(thebyte)
       print(f'*** 399 thechar = >{thebyte}<')
       print('*** 404 cellcomplete',self.thecell.cellcomplete)
       while not self.thecell.cellcomplete:
            if thebyte == '':
                logging.info(f'end of file encountered in cell at byte {self.thecell.charno}')
                self.thecell.eof = True
                self.linecomplete = True
                return self.thecell.charno
            self.thecell.charno += 1
            thebyte = self.InHdl.read(1)
            # check if file is finished
            self.thecell.addchar(thebyte)
       return self.thecell.charno


   def getSamp(self):
       """
       getSamp - retrieve sample
       return last row read
             - return -1 if either file cannot be openned
             - return currow number of lines read in CSV
       """
       if not self.openInPath():
           return -1
       if not self.openOutPath():
           return -1
       EndLoop = False
       loopcnt = 0
       # row being processed
       currow = 0  
       # column being processed.
       curcol = 0
       # cell for which data is being colled
       self.thecell = CSVsampCell()
       # number of records in file
       self.currow = 0
       # number of records in target frame
       self.obno = 0
       while not EndLoop:
           # fill new cell with data
           print('*** 514',currow,curcol,self.thecell.dataBuf)
           print('*** 515',self.thecell)
           self.thecell.reset()
           # getCellStr method fills up thecell
           print('*** 518',currow,curcol,self.thecell.dataBuf)
           charcount = self.getCellBuff()
           print('*** 520 charcount=',charcount)
           print('*** 521',currow,curcol,self.thecell.dataBuf)
           if charcount == 0: 
               print('*** 523 charcount= ',charcount)
               break
           if self.thecell.eof:
               return self.currow
           # if successfull process the data
           if self.thecell.linecomplete :
               currow += 1
               curcol = 1
               self.thecell.linecomplete = False
               self.InMaxRow += 1
           else:
               curcol += 1 
               if curcol > self.InMaxCol:
                  self.InMaxCol = curcol
           if self.isInSamp(currow,curcol):
               # print('*** 453',currow,curcol,self.thecell.dataStr)
               # print('*** 454',currow,curcol,self.thecell.dataBuf)
               self.thecell.getCellStr()
               # print('*** 456',currow,curcol,self.thecell.dataStr)
               # print('*** 457',currow,curcol,self.thecell.dataBuf)
               print('*** 527 self.InMaxRow = ',self.InMaxRow)
               if self.InMaxCol <= self.maxcol:
                   self.InMaxCol = curcol
               print('*** 530',currow,curcol,self.thecell.dataStr)
               self.cellSave(currow,curcol,self.thecell.dataStr)
               print('*** 532',currow,curcol,self.thecell.dataStr)
           self.thecell.reset()
           loopcnt += 1
           if loopcnt > MAXSAMP:
               logging.warning(f'MAXSAMP exceeded loopcnt=',loopcnt)
               currow = -1
           else:
               self.currow = currow
       return currow

   def cellSave(self,currow,curcol,celldata,endLine = False):
       """
       If cell data if it is in range defined by InSamp
           - save data to OutHdl
           - add comma to OutHdl
           - add new line if need be     
       return:
            tuble of new cell info
                  - row, col, len
       """
       therow = -1
       thecol = -1
       thelen = -1
       retval = therow, thecol, thelen
       if self.isInSamp(currow,curcol):
           print('*** 573 celldata >',celldata,'<')
           print('*** 574 curcol=',curcol)
           self.OutHdl.write(celldata)
           self.OutHdl.write(",")
           self.cumCell(curcol,celldata) 
           thelen = len(celldata) 
           retval = therow, thecol, thelen
       if endLine:
           if currow >= self.minrow and currow <= self.maxrow:
               self.OutHdl.write('\n')
           else:
               if curcol >= self.mincol and curcol < self.maxcol:
                   self.OutHdl.write(',')
       return retval
      
   def cumCell(self,curcol,celldata):
       """
       Make celldata available to cumulator object if 
          registered in CumDict
       Return
          True if cumulator object is found and can process data
          False no cumlator object for that column
       """
        
       
       try:
           print('*** 598 in cumCell curcol =',curcol)
           # thecumcell = self.CumDict[int(curcol)+1]
           thecumcell = self.CumDict[int(curcol)]
           print('*** 601 in thecumcell',thecumcell)
           print('*** 602 in cumCell >',celldata,'<')
           thecumcell.addcelldata(celldata)
           return True
       except:
           return False
           
   def showRes(self):
   
       res = 'Run has been completed \n'
       res += f'{int(self.InMaxRow)} processed \n'
       res += f'Starting at {self.minrow} \n' 
       res += f' {self.InMaxRow} records processed \n'
       print('*** 598 >',res,'<')
       print('***599 CumDict is',self.CumDict)
       # test if dictionary empty
       if not self.CumDict:
           return res
       for thecol in self.CumDict.keys():
           thecolint = int(thecol)
           print('*** 605 >',thecol,'<')
           thecumcell = self.CumDict[thecolint]
           print('*** 607 >',thecumcell,'<')
           if thecumcell is not None:
               curres = thecumcell.SumIt()
               if curres is not None:
                   res += curres
       return res
       
             
