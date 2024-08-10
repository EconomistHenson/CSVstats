# download huge spread sheet
# Status column is key to decoding
# col1 contains date REF_DATE
# col2 contains GEO
# col6 contains Age-Group
# col7 contains SEX
# col15 the units


import math

import unittest
import logging
import csv
import time
import json
from datetime import datetime 

NAN = float('nan')
MAXSTR = 30
MAXRECS = 100000000

# default labels file for the install

# LABELS = '/media/henskyconsulting/easystore/Data/StatsCan/SDMX/code/catLab.json'
LABELS = '\Data\StatsCan\SDMX\code\catLab.json'

# establish logging for this script

logging.basicConfig(filename='extWeekMortInfo.log', level=logging.INFO)
logging.info(40*'=')
logging.info("extWeekMort.py")


class CSVcell:
    def __init__(self, colold: int, colnew , newname="",oldname="",lblpth=""):
        # position of column in source database
        self.posold = colold
        # position in database to be created
        self.posnew = colnew        
        # name of column in new database
        self.newname = newname
        # name of column in old database
        self.oldname = ""
        # default return value
        self.newval = ""
        # what was initial obtain
        self.oldval = ""
        # json of labels to use
        self.labels = NAN
        self.lblpth = lblpth
        retval = False
        if self.lblpth == "":
            # use global default
            self.lblpth = LABELS
        retval = self.loadlabels()
       
            
        if not retval:
            print('could not load label file')
       
    def loadlabels(self):
        if self.labels == NAN:
           return True   
        with open(self.lblpth, 'r') as file:
           self.labels = json.load(file)
           # print('*** at 55 json.load produced',self.labels)
           return True
        return False

class CSVint(CSVcell):
    def __init__(self,posold,posnew,newname):
        super().__init__(posold,posnew,newname)
        self.datnum = NAN
        self.min = NAN
        self.max = NAN
        self.newval = ""
    def getold(self, thestr = ""):     
        try: 
           self.oldval = thestr
           self.newval = self.oldval.strip()
           self.datnum = int(self.newval)
           return True
        except:
           self.newval = ""
           self.datnum = NAN
           return False
    def getnew(self, getstr = True):
        if getstr:
            return self.newval
        else:
            return self.datnum 

        
        
class CSVdate(CSVcell):
    def __init__(self,posold,posnew,newname ):
        super().__init__(posold,posnew,newname)
        self.day = self.month = self.year = NAN
        # store date at integer YYYYMMDD for sorting
        self.datnum = NAN
        self.newname = newname
        self.date_format = "%Y-%m-%d"
        self.newval = ""
    def __str__(self):
        retval = "newname: {self.newname} posold: {self.posnew} posnew: {self.posnew}"
        return retval
    def __repr__(self):
        return "newname: {self.newname} dateint {self.dataint}"
    def getold(self, thestr = ""):
        try:
           self.oldval = thestr
           self.newval = self.oldval.strip() 
           self.year = datetime.strptime(self.newval,self.date_format).year
           self.month = datetime.strptime(self.newval,self.date_format).month
           self.day = datetime.strptime(self.newval,self.date_format).day
           # used for sort
           self.dateint = int(thestr.replace("-",""))
           return True
        except:
           self.newval = ""
           self.day = self.month = self.year = NAN
           # not sure how this will react in sorts
           self.dateint = NAN
           return False
    def getnew(self, getstr = True,getdate=False):
        if getstr:
           return self.newval
        if not getstr and not getdate :
           return self.datnum 
        if getdate:
           return self.year,self.month,self.day
        return NAN

class CSVage(CSVdate):
    def __init__(self,posold,posnew,newname):
        super().__init__(posold,posnew,newname)
        self.minage = 0
        self.maxage = 200
        self.newname = newname
        # entry date may be used to adjust entries
        self.entrydate = NAN
        # date that the date of entry
        self.entrydate = NAN
        self.ageQuant = NAN
    def getold(self, thestr="", curage="",curbdate = ""):
        # age calculate from birthday
        try:
            if curage != "":
                thestr = curage
            self.oldval = thestr
            self.newval = self.oldval.strip()
            self.ageQuant = int(self.newval)
            if self.ageQuant < self.maxage and self.ageQuant > self.minage:
                return True
            if curbdate != "" :
                retval = super(CSVage,self).getold(thestr)
            if retval : return True
        except:
            self.newname = ""
            self.newval = ""
            self.ageQuant = NAN
    def getnew(self, getstr = True): 
        if getstr:
            # default is a string of the age 
            # at data entry as an integer
            return self.newval
        else:
            # return the number of days as an integer
            return self.ageQuant

class CSVsex(CSVcell):
    def __init__(self,posold,posnew,newname,lblpth=""):
        super().__init__(posold,posnew,newname,lblpth="") 
        self.SDMXval = ""
        if lblpth != "":
            self.lblpth = lblpth
        else:
            self.lblpth = LABELS
        # load labels for gender
        super().loadlabels()    
        self.SexLlb = self.labels['Sex2']
    def getold(self, thestr = ""):
        try:
            if(thestr == ""):
                return False
            if(len(thestr) > MAXSTR):
                return False
            self.oldval = thestr
            self.newval = self.oldval.strip()
            self.SDMXval = self.getSDMX(self.newval)
            if self.SDMXval != "":
                return True 
        except:
            self.newname = ""
            self.newval = ""
            self.SDMXval = ""  
            return False
            
    def getSDMX(self,theval):
        # linear search through the ten provinces
        for key, value in self.SexLlb.items():
            if value == theval:
                return key
        return ""
    
    def getnew(self, getstr=True):
        if getstr:
            return self.newval
        else:
            return self.SDMXval




        
class CSVgeo(CSVcell):
    def __init__(self,posold,posnew,newname,oldname="",lblpth=""):
        super().__init__(posold,posnew,newname,oldname,lblpth) 
        # will only focus on Canada
        self.newname = newname
        # a label file may be availalble
        print('*** 223',self.labels)
        self.ProLlb = self.labels['Pro10']  # only valid with Canadian Data
        print('*** 225',self.ProLlb)
        print('*** 226',self.ProLlb['T'])
    
    def getSDMX(self,theval):
        # linear search through the ten provinces
        for key, value in self.ProLlb.items():
            if value == theval:
                return key
        return ""    
        
    def getold(self,thestr = ""):
        try:
            self.oldval = thestr
            print('*** 232 test strip',self.oldval.strip())
            self.newval = self.oldval.strip()
            print('*** 232 ',print(self.newval))
            self.SDMXval = self.getSDMX(self.newval)
            print('*** 236',self.SDMXval)
            return True
        except:
            self.newval = ""
            return False
    def getnew(self, getstr = ""):
        if(getstr == ""):
            return False  
        if self.newval == getstr:
            return True
        return self.SDMXval
    
 
           
   
            
class CSVcat(CSVcell):
    def __init__(self,col,newname):
        CVScell().__init__(col,newname) 
        # will only focus on Canada
        self.istotage = False
    def getfld(self, thestr = ""):
        if(thestr == ""):
            return False
        if(len(thestr) > MAXSTR):
            return -1
        if thestr == "all ages":
           self.istotage = True
           return True

class CSVrow():
    def __init__(self,numcols):
    
        self.datrow = [NAN] * numcols
        self.numcols = numcols
        
    def reset(self):
        self.datrow = [NAN] * self.numcols
    
    def __repr__(self):
        return f'numcols: {1:2d} ,{2:d}  '.format(self.numcols, self.datrow)
    
    def __len__(self):
        return self.numcols
        
    def getfld(self,thecol,theCVSfld):
        self.datrow[thecol] = theCVSfld 

class CSVdata():

    def __init__(self,numcols):
    
        self.numcols = numcols
        self.numrows = 1
        self.rownum = 1
        self.row0header = True
        
        self.lstofrows =[(self.rownum,[])]
        
    def addrow(self,newrow: list):  
        therownum = self.numrows
        thenewrow = (therownum,newrow)
        self.listofrows.append((therownum,thenewrow))
        
        return True
              
        
class Test_CSVdate(unittest.TestCase):
    
    def test_JustInit(self):
        DateFld = CSVdate(1,1,'coldate')
        self.assertEqual(DateFld.posold,1)
        self.assertEqual(DateFld.posnew,1)
        self.assertEqual(DateFld.newname,"coldate")
    
    def test_getfld(self):
        DateFld2 = CSVdate(1,1,'coldate')
        retval = DateFld2.getold('1234567')
        self.assertFalse(retval)
        retval = DateFld2.getold("2024-03-14")
        self.assertTrue(retval)
        self.assertEqual(DateFld2.year,2024)  
        self.assertEqual(DateFld2.month,3) 
        self.assertEqual(DateFld2.day,14)
        self.assertEqual(DateFld2.dateint,20240314)  
      
    def test_getfromlist(self):
        DateFld0 =  CSVdate(1,3,'coldate')
        DateFld1 =  CSVdate(2,3,'coldate')
        DateFld2 =  CSVdate(3,3,'coldate')
        Lst0_2 = [DateFld0,DateFld1,DateFld2]
        thefld = Lst0_2[1]
        self.assertEqual(thefld.newname,'coldate')
        self.assertEqual(thefld.posold,2)
        self.assertEqual(thefld.posnew,3)    
        retval = DateFld2.getold("2024-03-14")
        # should be number 1 in list
        thefld.getold("2024-03-14")
        self.assertEqual(thefld.year,2024)  
        self.assertEqual(thefld.month,3)
        self.assertEqual(thefld.day,14)          
        self.assertEqual(thefld.dateint,20240314) 

class TestCSVfld(unittest.TestCase):
 
    def test_CSVcell(self):
        Cel1 = CSVcell(0,0,'coljunk')
        self.assertEqual(Cel1.posold,0)
        self.assertEqual(Cel1.posnew,0)
        self.assertEqual(Cel1.newname,"coljunk")
    def test_CSVcell(self):
        # test with loading labels
        catLabPth = LABELS
        Cel2 = CSVcell(0,0,'coljunk','newjunk',catLabPth)
                      
class Test_CSVint(unittest.TestCase):

    def test_CSVint(self):
        intFld1 = CSVint(2,3,'colint')
        retval = intFld1.getold('  4 ')
        self.assertEqual(intFld1.newval,"4")
        self.assertEqual(intFld1.datnum, 4)
        self.assertEqual(intFld1.getnew(getstr=False),4)
        self.assertEqual(intFld1.getnew(),"4")
        retval = intFld1.getold('  junk ')
        self.assertFalse(retval)

class Test_CSVrow(unittest.TestCase):

    def test_CSVrow(self):
        intCSVRow = CSVrow(4)
        intRow = [NAN] * 4
        self.assertEqual(len(intCSVRow),4)
        for ival in range(0,4):
           intRow[ival] = ival + 10
        intCSVRow.getfld(3,intRow[3])
        self.assertEqual(intCSVRow.datrow[3] , 13)
    
    def test_CVSintrow(self):
        intCSVrow1 = CSVrow(2)
        intFld1 = CSVint(0,2,'colint1')
        intFld1.getnew('1')
        intFld2 = CSVint(1,2,'colint2')
        intFld2.getnew('2')
        self.assertEqual(len(intCSVrow1),2)



class Test_CSVdata(unittest.TestCase):

    def test_CData_Init(self):
        CData = CSVdata(4)
        self.assertEqual(CData.numcols,4)
        junkrow = CSVrow(4)
        self.assertEqual(CData.numcols,4)
        for ival in range(0,3):
           junkrow.datrow[ival] = ival + 10
        
        
          

class Test_CSVgeo(unittest.TestCase):

    def test_getfldgeo(self):
        GeoFld =  CSVgeo(2,3,'colgeo')
        retval = GeoFld.getnew()
        self.assertFalse(retval)
        
    def test_getfromlist(self):
       
        GeoFld1 =  CSVgeo(1,3,'Canada')
        GeoFld2 =  CSVgeo(2,3,'Canada')
        GeoFld3 =  CSVgeo(3,3,'Canada')
        Lst1_3 = [GeoFld1,GeoFld2,GeoFld3]
        thefld0 = Lst1_3[0]
        self.assertEqual(thefld0.posold,1)
        self.assertEqual(thefld0.posnew,3)
        self.assertTrue(thefld0.getold("Canada"))
        self.assertTrue(thefld0.getnew("T"))
        thefld1 = Lst1_3[1]
        self.assertEqual(thefld1.posold,2)
        self.assertEqual(thefld1.posnew,3)
        self.assertTrue(thefld1.getold("Newfoundland"))
        self.assertTrue(thefld1.getnew("A"))
        thefld2 = Lst1_3[2]
        self.assertEqual(thefld2.posold,3)
        self.assertEqual(thefld2.posnew,3)
        self.assertTrue(thefld2.getold(" British Columbia "))
        self.assertTrue(thefld2.getnew("J"))        
        
class Test_CSVage(unittest.TestCase):
    
    def test_getCSVage1(self):
        AgeFld = CSVage(1,3,'Age')  
        self.assertEqual(AgeFld.minage,0)
    def test_getold1(self):
        AgeFld1 = CSVage(10,1,'AgeStr')
        self.assertTrue(AgeFld1.getold("67"))
        self.assertEqual(AgeFld1.getnew(),"67")
        self.assertTrue(AgeFld1.getnew(getstr=False),67)
        AgeFld2 = CSVage(10,1,'AgeStr')
        self.assertTrue(AgeFld2.getold("  67 "))
        self.assertEqual(AgeFld2.getnew(),"67")
    ## will test entering birthdates later

class Test_CSVsex(unittest.TestCase):
    
    def test_getCSVsex1(self):
        SexFld1 = CSVsex(1,3,'Sex')  
        self.assertEqual(SexFld1.SDMXval,"")
    def test_getCSVsex2(self):
        AgeFld2 = CSVsex(10,1,'Sex')
        self.assertTrue(AgeFld2.getold("Males"))
        self.assertEqual(AgeFld2.getnew(),"Males")
        self.assertEqual(AgeFld2.getnew(getstr=False),'M')
        AgeFld3 = CSVsex(10,1,'Sex')
        self.assertTrue(AgeFld3.getold("  Females "))
        self.assertEqual(AgeFld3.getnew(),"Females")
        self.assertEqual(AgeFld3.getnew(getstr=False),'F')
        AgeFld4 = CSVsex(10,1,'Sex')
        self.assertTrue(AgeFld4.getold(" Both sexes "))
        self.assertEqual(AgeFld4.getnew(),"Both sexes")
        self.assertEqual(AgeFld4.getnew(getstr=False),'T')
    
class Test_CSVlabel(unittest.TestCase):

   def testLabelData(self):
       # The first test is just the basic loading of the file
       CatLbs = LABELS
       with open(CatLbs, 'r') as file:
           loadedCategories = json.load(file)
       print(loadedCategories) 
       The13 = loadedCategories['Pro13']
       # 10 provinces, 3 territories and national total
       self.assertTrue(len(The13),14)  


 

if __name__ == '__main__':
    unittest.main()

