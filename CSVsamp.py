import logging
import unittest
import pytest
from datetime import datetime
import math
from os.path import join

logging.basicConfig(filename = 'CSVsamp.log',level=logging.INFO)
logging.info(40*'=')
logging.info(f"Sample Taken {datetime.now()} ")

MAXSTR = 200
# MAXSAMP = 1000
MAXSAMP =80 # for debugging
EMPTYSTR = ""


class CSVsampCell:
   def __init__(self,):
       self.reset()
       self.linecomplete = False
              
   def reset(self):
       self.cellcomplete = False
       self.cellbuf = []
       self.data = []
       self.charno = 0
       self.eol = False

   def getcellstr(self): 
       self.data = ''.join(self.cellbuf)
       return self.data
   
   def __str__(self):
       return self.getcellstr()          
 
   def addchar(self,achar):
#       print('*** at 34 >',achar,'<')
#       print('*** at 35 len ',len(achar))
       if achar == ',': 
           self.cellcomplete = True
#          print('*** 38',self.cellbuf)
           return self.charno
       if achar == '\n':
           self.eol = True
           self.cellcomplete = True
           self.linecomplete = True
           return self.charno
       self.cellbuf += achar
       self.charno += 1
       
       return self.charno
     

class CSVsampFile: 
   def __init__(self,InPth,outfile='Samp.csv'):
       self.setTarget(0,math.nan,0,math.nan)
       # list of cells to be output to outfile
       self.sampLst = []
       # max number of cells before output
       self.SAMPBUF = math.nan
       # input file to be sampled from
       self.InPth = InPth
       self.InHdl = math.nan
       self.InCntRow = 0 # set to number of rows used as headers
       self.InMaxCol = 0
       # output file to store the sampled
       self.OutPth = outfile
       self.OutHdl = math.nan
       self.retstr = "" 

   def setTarget(self,minrow,maxrow,mincol,maxcol):

       self.minrow = minrow
       self.maxrow = maxrow
       self.mincol = mincol
       self.maxcol = maxcol 

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


   
   def isInSamp(self,therow,thecol):

        """  
        Determine if newcell is to be stored in sample
        """
        if therow < self.minrow:
           return False
        if therow > self.maxrow:
           return False
        if thecol < self.mincol:
           return False
        if thecol > self.maxcol:
           return False   
        return True

   def getCellStr(self,newcell):
        
       charcnt = 0
       lbrackno = 0
        
       while charcnt < MAXSTR :
           try:
               thechar = self.InHdl.read(1)
               if thechar == '':
                   return 0
           except:
               print('failed to read input file')
               logging.warning(f'Could not read input file {self.InPth}')
               exit(0)
           charcnt += 1
           if thechar == '{':
              continue
           if thechar == '}':
              continue
           charno = newcell.addchar(thechar)
           if newcell.cellcomplete:
               retcell = newcell.getcellstr()
#               print('***148 ',newcell)
               break              
       return charcnt

   def getSamp(self):
       
       self.openInPath()
       self.openOutPath()
       EndLoop = False
       loopcnt = 0
       # row being processed
       currow = 0  
       # column being processed.
       curcol = 0
       # cell for which data is being colled
       newcell = CSVsampCell()
       while not EndLoop:
          # fill new cell with data
          charcount = self.getCellStr(newcell)
#          print('*** 178 charcount = ',charcount)
#          print('*** 179 >',newcell.data,'<')
          if charcount == 0: 
              break
          # if successfull process the data
          if newcell.eol :
              self.cellSave(currow,curcol,newcell.data,endLine=True)
              self.InMaxCol = max(self.InMaxCol,curcol)
              newcell.reset()
              currow += 1
              curcol = 0
              newcell.eol = False
          elif self.isInSamp(currow,curcol):
#              print('*** 190',newcell.data)
#              print('*** 191',currow,' ',curcol)
              self.cellSave(currow,curcol,newcell.data)
              newcell.reset()
              curcol += 1
          else:  
              curcol += 1
              newcell.reset()
#          print('***194 at bottom of loop curcol =',curcol)
#          print('***195                   currow =',currow)
#          print('***196                 InMaxCol =',self.InMaxCol) 
          loopcnt += 1
          if loopcnt > MAXSAMP:
              print('MAXSAMP exceeded loopcnt=',loopcnt)
              break

   def cellSave(self,currow,curcol,celldata,endLine = False):
       
          retval = 0
#          print('******************207')
#          print(currow,' , ',curcol,' , ',celldata, ' ',endLine)
          if self.isInSamp(currow,curcol):
#              print('*** 211 ',currow,' ',curcol,' in sample')
              self.OutHdl.write(celldata)
              retval = len(celldata) 
          if endLine:
              if currow >= self.minrow and currow <= self.maxrow:
                  self.OutHdl.write('\n')
          else:
              if curcol >= self.mincol and curcol < self.maxcol:
                  self.OutHdl.write(',')
                  retval += 1
#          print('*** 217 in cell save retval = ',retval)
          return retval
      

 

             