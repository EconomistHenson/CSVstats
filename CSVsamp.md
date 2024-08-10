# CSVsamp

This object provides raw samples of cvs files.  Usually, the practice is to read a 
downloaded file with the CSV library.  This usually works fine except in cases of very
large file where they paper trail is too voluminous to capture the problematic 
observation.

This utility uses Python to sample the problematic observations and save them as a 
more manageable subfile.  It should be noted that it does not use the csv library as 
often the problems with large administrative databases are associated with episodic 
changes in how basic files are defined.  

## globals

### logginfo

### MAXSTR
Will determine the maximum length of CSV cell.  
### MAXSAMP
Maximum number of bytes that will be processed
### EMPTYSTR
represents and empty string


## CSVsampFile (Rawsvs, Output)
There a relatively high percentage of the variables defined
as part of the class
### __init__
#### data related
The five parameters here define the target sampling area.  The 
current definitions should be considered.  The actual rows and
columns of each observation will be determined during the sampling
process. 
minrow - first row to start sampling
maxrow - last row of sample
mincol - first column to be sampled
maxcol - last column to be sample
samprob - probability that and observation is saved 0 to 100 
cumdict - columns in the sample region to collect data


### file related

#### file under analysis
InPath - pathname to be sampled
InHdl - file object to be sampled
InCntRow - number of rows read
InMaxCol - maximum number of columns
#### output file to store the sampled
OutPath - pathname of output file
OutHdl - file object to save the sample

Note that after repeated attempts, there may be a need to reboot. 
This is can be mitigated using a venv. 

### getCellStr
This method will read the next cell in the open file 
object.  If the cell is determined to be valid by 
isInSamp it is returned.
 
### isInSamp (newcell)
This method determins if a given cell should be
included in the sample

All CSV files start with the same structure.
currow - must count the newlines

## getSamp
Sets up the main loop for processing the data.  Will read in the 
data.  A new cell is created for the loop.  It is emptied and 
reset with each cell.  Each new cell data will force an increase
of curcol by one, or a reset of curcol to 0 and an increase in 
currow by one.

However, as getsamp iterates through the file while maintaining 
awareness of currow and curcol it is neccessary to see if the cell
needs to be saved.  This is performed by isInSamp routine

## cellSave 

Contains some key logic

## cumCell

Some columns that are saved will also be cummulated, if there is a routine in cumCell.
The default is for the dictionary to be empty.  To enable this feature an object must
be created and then added to the dictionary. Once it is created, then it is added
to the dictionary.




## CSVsampCell
This is the primary object.  It must process the text data one
char at a time.  Note that it is possible that very old data from
70s mainframes may use non-ASCII bytes.  To treat this fully, it
is likely that C would have to be used.

### CSVsample
The initial init simply calls a reset routine.  Within the loop
this may be better than creating a new cell for cell in the 
database.

#### reset
Basically plays the role of the init

#### cellbuf
An list of chars that contain data as it is obtained from the
raw file.

#### data
This is the CSV datapoint.

#### addchar
This is the crucial method that will likely the most often 
modified.  In its simplist form it reads one character at a
time.  If the character is a comma, then the cell has been read 
and the cell can be marked as complete. If the char is an end of
line, the cell again is market as complete but so it the end of
line. If it is just a regular char it is added to the buf.

#### getcellstr
This takes the list of chars and converts it into what would be
seen as the CSV cell.  Note that there may be cases where 
additional processing is required.  



## Endnotes

### Coordinate system 

The upper lefthand corner of a spreadsheet is A1. The 'A'
refers to the first column on the screen.  The '1' refers to
the first row.

The upper lefthand corner of a two-dimensional Python array is
0,0.  Another difference with a spreadsheet is that the first zero
refers to the row and not the column as is the case with spreadsheets
above. If we look at the spreadsheet cell B2, that cell would be found in the 
second column or the thirdrow.

In the test of the 5 by 5 matrix given in section xxx, a square 5 by 5
matrix is saved in csv matrix with the upper-left hand corner being 1 by 1 and the
lower right hand corner being 5 by 5.  The cell C2 on the spreadsheet would be 
the cell 3, 2 in the matrix. The lower right hand corner E5 would be 4, 4 on the 
matrix. Note that this scheme has the advantage, of allowing the column headers to
be interpreted as column names, or variable names as a statistical package would 
understand it.  More importantly, the rows would be seen as observation numbers. As
new observations are added, which is often the case with large adminstrative files, 
the columns can remain unchanged.  It is also important to note that adding observation
has a huge performance advantage as the underlying data will be organized by row.(check) 

However, for the rows to show as observation, the first row will be zero if there are
now header strings.  If header strings are present, then InCntRow can be reset.

### Logic Flow of getSamp

The getSamp routine can be considered the primary logic of
the package.  As it passes through the larger administrative
file, one cell at a time, the following points need to be 
considered.

- Even if the original file is a dataframe it is visualized as
a spreadsheet where the rows correspond to observations and
columns are fields.  
- Currow and curcol correspond to the current
cell that is being processed.  
- getCellStr gets the new data. cellcomplete member signals 
that the data is worth processing. There are three possibilities:
   - the data is valid and in the area where data is being saved
     as identified by isInSamp
   - the data is valid but not included in the saved data
   - A newline character has been encountered.  newcell.eol is
     true in this case
 
- if the data not worth processing. This may occur due to
some form of corruption of the source data.  Identifying these
problems is one of the reasons this package exists.  In such
cases it may be worth while to keep reading the data with the
intent of finding the valid data. loopcnt is implemented to guard
against infinite loops.

In this case:


- if the newcell was an end of the line
currow and curcol are the corrdinates of the current 



curcell - must count the non-quoted commas from the start
          of each line

stop when end of file, or min max achieved
