#!/usr/bin/python3

# This python script digest THERMOCALC logfile
# and put the data into a structure that can be easily manipulated in Python
# to understand how the code works, you need the following knowledge of Python:
# 1. The basic data types: string, float, integer
# 2. More advance data structure, in particular list and dictionary
# 3. 'function' and 'main function'
# 4. How to write functions in Python

# Carson Kinney and Qihang Wu
# Last modified: 15 Feb 2019 09:33:24 AM #

# modules to
import codecs
import re # regex operations


# GLOBAL CONSTS
MAINBLOCKSEPARATOR = '-----'
MAINBLOCKMINLENGTH = 17

############ FUNCTIONS #################
def processMainBlock(mainBlock):

    data = {}

    if len(mainBlock) >= MAINBLOCKMINLENGTH:
        data['PT'] = crunchPTBlock(mainBlock)

        #  Try implementing yourself :)
        #  crunchModeBlock(mainBlock)
        #  crunchElmtBlock(mainBlock)

        return data

    else:
        # length of main block shorter than expected
        # return nothing
        return


#--------------------------------------
def crunchPTBlock(mainBlock):

    # retrieve 1st line of main block
    speciesName = mainBlock[0]

    # replace paranthesis with underscore
    speciesName = speciesName.replace('(','_')
    speciesName = speciesName.replace(')',' ')
    # after all the replacement, P(kbar) will look like P_kbar

    # split the line into individual entries
    speciesName = speciesName.split()
    # retrieve 2nd line of main block and convert each entry to number
    speciesQuantity = [float(i) for i in mainBlock[1].split()]

    # internal check, species name and quatity must match up
    if len(speciesQuantity) != len(speciesName):
        raise ValueError('Species name and quantity must be a 1-to-1 match')

    # put data into a dictionary
    PTData = {}
    for i in range(0, len(speciesQuantity)):
        PTData[speciesName[i]] = speciesQuantity[i]

    return PTData


########## MAIN FUNCTION ############
if __name__ ==  '__main__':
    # separtor between each main block

    # list that contains nonempty lines of main block
    mainBlock = []
    alldata = []

    # ignore all the weird characters
    with codecs.open('logfile.txt', 'r', encoding='utf-8', errors='ignore') as lf:

        print('File opened. Processing data ...')

        # load contents of the file
        lfContents = lf.readlines()

        # loop through each line of the file
        for line in lfContents:

            if not re.match(r'^\s*$',line):

                # only append a nonempty line
                mainBlock.append(line.strip("\r\n"))

                # upon hitting the separator, pass the block to function to
                # digest its contents
                if  MAINBLOCKSEPARATOR in line:

                    # strip last line of '---'
                    dataThisBlock = processMainBlock(mainBlock[0:-1])
                    # if the main block data is valid, append it to alldata list
                    if dataThisBlock:
                        alldata.append(dataThisBlock)

                    # clean up mainBlock for next entry
                    mainBlock = []

        # upon completion report data set size
        print(str(len(alldata)) + ' datasets have been successfully processed.')

        # This gives you an example of how to access the data
        # For example, we need:
        # The 5th set of data, (notice base-0 indexing)
        #   => PT block
        #   => fsp(L) entry
        print(alldata[4]['PT']['fsp_L'])




