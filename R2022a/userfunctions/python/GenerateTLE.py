

# -*- coding: utf-8 -*-
"""
Created on Tue Jul 11 15:30:21 2017

@author: sphughe1
"""
import os
import time
import math
import datetime
#import TLEUtility
from datetime import timedelta




def GenerateTLEADV(meanMotion, orbitECC, orbitINC, orbitRAAN,
                   orbitAOP, orbitMA, UTCGregorian,Classification,Identifier,launchId,Ndot,Ndotdot,BStar):

    # Convert gregorian epoch to year and day of year
    epochTup = datetime.datetime.strptime(UTCGregorian, "%d %b %Y %H:%M:%S.%f")
    year = epochTup.timetuple().tm_year
    year = year % 100
    dayOfYear = epochTup.timetuple().tm_yday/1 + (epochTup.timetuple().tm_hour*3600+ epochTup.timetuple().tm_min*60+epochTup.timetuple().tm_sec + float(UTCGregorian[-3:])/1000.0)/86400
    # Generic SDO TLE to load and set basic properties
    tle = TLEUtility()
    line1nom = '1 36395U 10005A   17169.43316045 -.00000000  00000-0  00000-0 0 99991'
    line2nom = '2 36395  28.7658 140.4053 0000373 131.4574  49.2461  1.00271298999992'
    tle.SetFirstDataLine(line1nom)
    tle.SetSecondDataLine(line2nom)
    # tle.ReadFile('ReadTestForSDOTLE.txt')
    
    # Update Basic, Line 1 information
    tle.SetSatelliteNumberSTR(Identifier)
    tle.SetClassification(Classification)
    tle.SetDesignator(launchId)

    # Update the tle based on input orbit states
    tle.epochYear = year
    tle.epochDay = dayOfYear
    if orbitINC > 180:
        orbitINC -= 180
    elif orbitINC < 0:
        orbitINC += 180
    tle.orbitINC = orbitINC
    if orbitRAAN > 360:
        orbitRAAN -=  360
    elif orbitRAAN < 0:
        orbitRAAN += 360
    tle.orbitRAAN = orbitRAAN
    if orbitAOP > 360:
        orbitAOP -=  360
    elif orbitAOP < 0:
        orbitAOP += 360
    tle.orbitAOP = orbitAOP
    if orbitMA > 360:
        orbitMA -=  360
    elif orbitMA < 0:
        orbitMA += 360
    tle.orbitMA = orbitMA
    tle.orbitECC = orbitECC
    tle.orbitMeanMotion = meanMotion # Convert to revs/day
    tle.meanMotionDotByTwo = Ndot
    tle.meanMotionDotBySix = Ndotdot
    tle.dragCoefficient = BStar

    #tle.WriteFile('WriteTestForSDOTLE.txt')

    # Generate tle with updated data
    line1 = tle.GetFirstDataLine()
    line2 = tle.GetSecondDataLine()

    return line1, line2
		
def GenerateTLE(meanMotion, orbitECC, orbitINC, orbitRAAN,
                   orbitAOP, orbitMA, UTCGregorian,Classification,Identifier,launchId):

    # Convert gregorian epoch to year and day of year
    epochTup = datetime.datetime.strptime(UTCGregorian, "%d %b %Y %H:%M:%S.%f")
    year = epochTup.timetuple().tm_year
    year = year % 100
    
    dt = timedelta(days=epochTup.timetuple().tm_yday, hours=epochTup.timetuple().tm_hour, minutes=epochTup.timetuple().tm_min, seconds=epochTup.timetuple().tm_sec)
    dayOfYear = dt.total_seconds()/86400
    # Generic SDO TLE to load and set basic properties
    tle = TLEUtility()
    line1nom = '1 36395U 10005A   17169.43316045 -.00000000  00000-0  00000-0 0 99991'
    line2nom = '2 36395  28.7658 140.4053 0000373 131.4574  49.2461  1.00271298999992'
    tle.SetFirstDataLine(line1nom)
    tle.SetSecondDataLine(line2nom)
    # tle.ReadFile('ReadTestForSDOTLE.txt')
    
    # Update Basic, Line 1 information
    tle.SetSatelliteNumberSTR(Identifier)
    tle.SetClassification(Classification)
    tle.SetDesignator(launchId)

    # Update the tle based on input orbit states
    
    if orbitINC > 180:
        orbitINC -= 180
    elif orbitINC < 0:
        orbitINC += 180
    if orbitRAAN > 360:
        orbitRAAN -=  360
    elif orbitRAAN < 0:
        orbitRAAN += 360
    if orbitAOP > 360:
        orbitAOP -=  360
    elif orbitAOP < 0:
        orbitAOP += 360
    if orbitMA > 360:
        orbitMA -=  360
    elif orbitMA < 0:
        orbitMA += 360
    tle.epochYear = year
    tle.epochDay = dayOfYear
    tle.orbitINC = orbitINC
    tle.orbitRAAN = orbitRAAN
    tle.orbitECC = orbitECC
    tle.orbitAOP = orbitAOP
    tle.orbitMA = orbitMA
    tle.orbitMeanMotion = meanMotion*86400/2/math.pi  # Convert to revs/day
    #tle.WriteFile('WriteTestForSDOTLE.txt')

    # Generate tle with updated data
    line1 = tle.GetFirstDataLine()
    line2 = tle.GetSecondDataLine()

    return line1, line2
		
def GetTLEFromGMATReport(tleline1, tleline2,satName,location) :
    # Grabs the TLE from the temporary report file
    new = open(location + "TEMPTLE.txt","w")
    tle =[]
    #tle.append("TEMPORARY TLE DO NOT USE\n")
    tle.append(satName+ "\n")
    tle.append(tleline1+"\n")
    tle.append(tleline2+"\n"+"\n")
    #tle.append("TEMPORARY TLE DO NOT USE\n")
    for line in tle: 
        new.write(line)
    return location + "TEMPTLE.txt"
    	
def CreateTEMPTLE(location) :
    # Grabs the TLE from the temporary report file
    new = open(location + "TEMPTLE.txt","w")
    tle =[]
    # Dummy TLE Values
    line1nom = '1 36395U 10005A   17169.43316045 -.00000000  00000-0  00000-0 0 99991'
    line2nom = '2 36395  28.7658 140.4053 0000373 131.4574  49.2461  1.00271298999992'
    #tle.append("TEMPORARY TLE DO NOT USE\n")
    tle.append('TEMPORARYTLE'+ "\n")
    tle.append(line1nom+"\n")
    tle.append(line2nom+"\n"+"\n")
    #tle.append("TEMPORARY TLE DO NOT USE\n")
    for line in tle: 
        new.write(line)
    return location + "TEMPTLE.txt"
    
def GetTime(timeSTR):
    # Grabs the TLE from the temporary report file
    return float(timeSTR)

def JoinString(str1,str2):
    # Grabs the TLE from the temporary report file
    return str1+str2
    
    
def GetPath(path):
    # Appends the active GMAT directory to the string
    return os.path.normpath(os.getcwd()+"/../"+path)
    
    
class TLEUtility:

    def __init__(self):
        # Real. Orbital inclination.
        self.orbitINC = 0
        # Real. Orbital right ascention of ascending node.
        self.orbitRAAN = 0
        # Real. Orbital eccentricity.
        self.orbitECC = 0
        # Real. Orbital argument of periapsis.
        self.orbitAOP = 0
        # Real. Orbital mean anomaly.
        self.orbitMA = 0
        # Real. Orbital mean motion.
        self.orbitMeanMotion = 0
        # Integer.
        self.epochYear = 99
        self.epochDay = 99.9999


        # string of length 24. Title line of the TLE file
        self.tleTitle = 'USER SAT                '
        # Integer. The satellite ID number
        self.sateliteNumber = 99999          
        # Integer. The satellite ID number
        self.sateliteNumberSTR = '99999'
        # String Length 1. Classification of satellite
        self.classification = 'U'
        # String.
        self.designator = "00001A"
        # Integer.
        self.designatorYear = 99
        # Integer.
        self.designatorDOY = 1
        # String Length 1.
        self.designatorPiece = 'A'

        self.meanMotionDotByTwo = 0
        self.meanMotionDDotBySix = 0
        self.dragCoefficient = 0
        # Integer.
        self.ephemerisType = 0
        # Integer.
        self.elementSetNumber = 9999
        # Integer. Accumlated revolutoins at epoch
        self.revsAtEpoch = 99999


    def SetTitleLine(self, titleLine):
        # Sets the TLE title line
        if len(titleLine) > 24:
            raise Exception('TLE title must be less than or equal o 24 chars')
        else:
            self.tleTitle = titleLine  # + (23-len(titleLine))*' '

    def GetTitleLine(self):
        # Returns string containing the TLE title line
        return self.tleTitle

    def SetFirstDataLine(self, line):
        # Parses and sets the first line of data
        if len(line) > 70:
            raise Exception('Line length invalid')
        # Set the satellite number
        try:
            satNum = eval(line[2:7])
        except:
            raise Exception('Satellite number string not valid')
        self.SetSatelliteNumber(satNum)
        # Set the classification
        self.SetClassification(line[7])
        # Set designator year
        try:
            dYear = eval(line[9:11].lstrip('0'))
        except:
            raise Exception('Designator year not valid')
        try:
            dDOY = eval(line[11:14].lstrip('0'))
        except:
            raise Exception('Designator day of year not valid')
        self.SetDesignatorYear(dYear)
        # Set designator day of year
        self.SetDesignatorDOY(dDOY)
        self.designatorPiece = line[14:17].rstrip()
        self.epochYear = eval(line[18:20])
        self.epochDay = eval(line[20:32])
        self.meanMotionDotByTwo = eval(line[32:43])
        self.meanMotionDDotBySix = self.ParseAssumedDecimalPlace(line[44:52], True,False)
        self.dragCoefficient = self.ParseAssumedDecimalPlace(line[53:61], True,False)
        self.ephemerisType = eval(line[62])
        self.elementSetNumber = eval(line[64:68])
        self.checkSum = eval(line[68])

    def SetSecondDataLine(self, line):
        # Parses and sets the second line of data
        if len(line) > 70:
            raise Exception('Line length invalid')
        if self.satelliteNumber - eval(line[2:7]) != 0:
            raise Exception('Satellite ID is not the same in line1 and line2')
        self.orbitINC = eval(line[8:16])
        self.orbitRAAN = eval(line[17:25])
        self.orbitECC = self.ParseAssumedDecimalPlace(line[26:33], False,True)
        self.orbitAOP = eval(line[34:42])
        self.orbitMA = eval(line[43:51])
        self.orbitMeanMotion = eval(line[52:63])
        self.revsAtEpoch = eval(line[63:68])

    def ReadFile(self, fileName):
        # Reads a TLE file given the path and filename

        # Open the file
        with open(fileName, 'r') as TLE_file:
            # Reading file
            i = 0
            for line in TLE_file:
                if i == 0:  # Read and parse the first line
                    self.SetTitleLine(line)
                if i == 1:  # Read and parse the second line
                    self.SetFirstDataLine(line)
                if i == 2:  # Read and parse the third line
                    self.SetSecondDataLine(line)
                i += 1

    def WriteFile(self, fileName):
        # Writes a TLE file given the path and filename

        # Open the file
        with open(fileName, 'w') as TLE_file:
            # Read and parse the first line
            line1 = self.GetTitleLine()

            # Read and parse the second line
            line2 = self.GetFirstDataLine()

            # Read and parse the third line
            line3 = self.GetSecondDataLine()

            #Write lines to file
            print(line1, file=TLE_file)
            print(line2, file=TLE_file)
            print(line3, file=TLE_file)

    def GetFirstDataLine(self):
        # Returns string containing first data line of TLE

        str1 = '1 '
        str1 += '{0:>05}'.format(self.sateliteNumberSTR)
        str1 += '{0}'.format(self.classification)
        str1 += ' '
        str1 += '{0:<8}'.format(self.designator)
        str1 += ' '
        str1 += '{0:>02d}'.format(self.epochYear)
        tempString = '{0:>011.8f}'.format(self.epochDay)

        while tempString.index('.') < 3:
            tempString = '0' + tempString
        while len(tempString) > 12:
            tempString = tempString[:len(tempString)-1]
        str1 += tempString
        str1 += ' '
        # Mean motion derivative string handling
        tempString = '{0:<8.8f}'.format(self.meanMotionDotByTwo)
        # Remove leading zero to be consistent with spec
        tempString = tempString.replace('0.', '.')
        # Pad with space if the number is positive
        if tempString[0] != '-':
            tempString = ' ' + tempString
        str1 += tempString
        # Mean motion derivative string handling
        if self.meanMotionDDotBySix == 0:
            tempString = ' 00000-0'
        else:
            tempString = self.DoubleToAssumedDecimalPlace(self.meanMotionDDotBySix, 5)
        str1 += ' '
        str1 += tempString

        # Drag coefficient handling
        tempString = self.DoubleToAssumedDecimalPlace(self.dragCoefficient, 5)
        str1 += ' '
        str1 += tempString

        str1 += ' '
        str1 += '{0:1d}'.format(self.ephemerisType)
        str1 += ' '
        str1 += "9999" #'{0:4d}'.format(self.elementSetNumber)
        str1 += '{0:1d}'.format(self.CheckSum(str1))

        return str1

    def GetSecondDataLine(self):
        # Returns string containing second data line of TLE

        str2 = '2 '
        str2 += '{0:>05}'.format(self.sateliteNumberSTR)
        str2 += ' '
        # Inclination
        tempString = '{0:7.4f}'.format(self.orbitINC)
        while tempString.index('.') < 3:
            tempString = ' ' + tempString
        str2 += tempString
        str2 += ' '
        # RAAN
        tempString = '{0:7.4f}'.format(self.orbitRAAN)
        while tempString.index('.') < 3:
            tempString = ' ' + tempString
        str2 += tempString
        str2 += ' '
        # ECC
        tempString = '{0:8.7f}'.format(self.orbitECC)
        # Remove leading zero and decimal
        if tempString[0] == '-':
            tempString = "0.0000001"
        tempString = tempString[2:]
        while len(tempString) > 7:
            tempString = tempString[:len(tempString)-1]
        while len(tempString) < 7:
            tempString = tempString + '0'
        str2 += tempString
        str2 += ' '
        # AOP
        tempString = '{0:7.4f}'.format(self.orbitAOP)
        while tempString.index('.') < 3:
            tempString = ' ' + tempString
        str2 += tempString
        str2 += ' '
        # MA
        tempString = '{00:7.4f}'.format(self.orbitMA)
        while tempString.index('.') < 3:
            tempString = ' ' + tempString
        str2 += tempString
        str2 += ' '
        # Mean Motion
        #tempString = str(self.orbitMeanMotion)
        tempString = '{0:11.8f}'.format(self.orbitMeanMotion)
        while len(tempString) > 11:
            tempString = tempString[:len(tempString)-1]
        while len(tempString) < 11:
            tempString = tempString + '0'
        str2 += tempString
        # Revs at epoch
        tempString = "99999" 
        str2 += tempString
        str2 += '{0:1d}'.format(self.CheckSum(str2))

        return str2

    def DoubleToAssumedDecimalPlace(self, doubleIn, sigFigsInString):
        # Convert string containing "assumed" decimal place to a double
        # Parse depending upon if case has an exponent

        formatSpec = str(sigFigsInString) + '.' + str(sigFigsInString-1) + 'e'
        fullString = '{0:{1}}'.format(doubleIn, formatSpec)
        if doubleIn < 0:
            numSign = '-'
        else:
            numSign = ' '

        multiplyBy = 0
        # Handle the exponent
        hasExponent = 'e' in fullString
        if hasExponent:
            expstringStart = fullString.index('e')
            expSign = fullString[expstringStart+1]
            if fullString[expstringStart+2] == '0' and fullString[expstringStart+3] == '0':
                expValue = 0
            else:
                expValue = eval(fullString[expstringStart+2:].lstrip('0'))
            if expValue == 0:
                if (abs(doubleIn) < 10.0) and (abs(doubleIn) > 1.0):
                    expSign = '-'
                    exponent = '1' 
                else:
                    exponent = '0'
            elif abs(expValue) >= 10 and abs(expValue) < 14:
                multiplyBy = expValue - 9
                expValue = 10
                if numSign == '-':
                    expValue = expValue
                exponent = '{0:d}'.format(expValue-1)
            else:
                
                if numSign == '-':
                    expValue = expValue
                exponent = '{0:d}'.format(expValue-1)
        else:
            expSign = ''
            exponent = ''
        # Handle the numeric part of the string
        if hasExponent:
            numString = fullString[:expstringStart]
        else:
            numString = fullString

        # Remove the minus sign if there is one
        hasMinusSign = '-' in numString
        if hasMinusSign:
            numString = numString.replace('-', '')

        # Remove the decimal
        hasDecimal = '.' in numString
        if hasDecimal:
            numString = numString.replace('.', '')

        # Remove leading zeros
        while len(numString) > sigFigsInString and numString[0] == '0':
            numString = numString[1:]

        # Remove trailing zeros
        while len(numString) > sigFigsInString and numString[len(numString)-1] == '0':
            numString = numString[:len(numString)-1]

        # Pad with leading blanks
        while len(numString) < sigFigsInString:
            numString = ' ' + numString
        while multiplyBy > 0:
            numString = "0" + numString[:len(numString)-1]
            multiplyBy -= 1
        outString = numSign + numString + expSign + exponent

        return outString

    def ParseAssumedDecimalPlace(self, string, hasExponent,isECC):
        # Convert string containing "assumed" decimal place to a double
        # Parse depending upon if case has exponent

        exponent = eval(string[len(string)-1])
        if hasExponent:
            numString = string[:len(string)-2]
        else:
            numString = string

        # Handle leading decimal
        if string[0] == '-' and isEcc:
            number = "0000010"
        elif string[0] == '-':
            number = eval('-0.' + numString[2:].strip())
        else:
            number = eval('0.' + numString.strip())

        # Handle exponent string
        if hasExponent:
            if string[len(string)-2] == '-':
                number = number * 10 ** (-exponent)
            elif string[len(string)-2] == '+':
                number = number * 10 ** exponent
        return number

    def CheckSum(self, string):
        # Performs checksum on TLE data line
        sum = 0
        for char in string:
            if not (char.isalpha() or char == ' ' or char == '.' or char == '+'):
                if char == '-':
                    sum = sum + 1
                else:
                    sum = sum + eval(char)
        sum = sum % 10

        return sum


    def SetSatelliteNumber(self, satNum):
        # Sets the satellite integer id number
        if satNum > 99999:
            raise Exception('Satellite number must be <= 99999')
        self.satelliteNumber = satNum
        
    def SetSatelliteNumberSTR(self, satNumstr):
        # Sets the satellite integer id number
        if len(satNumstr) != 5:
            raise Exception('Satellite number must be five digits long E.G. \'12345\'')
        self.sateliteNumberSTR = satNumstr

    def GetSatelliteNumber(self):
        out = self.satelliteNumber
        return out

    def SetClassification(self, classification):
        # Sets the object classification
        if classification.isalpha() or len(classification) == 1:
            self.classification = classification
        else:
            raise Exception('Classification must be a single letter')

    def GetClassification(self):
        # Returns the object classification
        classification = self.classification
        return classification

    def SetDesignatorYear(self, year):
        # Set designator year given 2 digit integer
        if year == 0 or year == year % 100:
            self.designatorYear = year
        else:
            raise Exception('Designator Year must be a two digit number')

    def GetDesignatorYear(self):
        # Returns the designator year
        year = self.designatorYear
        return year

    def SetDesignatorDOY(self, doy):
        #Set designator day of year given integer
        self.designatorDOY = doy

    def GetDesignatorDOY(self):
        # Returns the designator year
        doy = self.designatorDOY
        return doy
        
        
    def SetDesignator(self, designatorID):
        # Set designator year given 2 digit integer
        if len(designatorID) > 6 or len(designatorID) < 8:
            self.designator = designatorID
        else:
            raise Exception('Launch Designator ID not ')