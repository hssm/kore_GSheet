#!/usr/bin/python2

import time
import gdata.spreadsheet.service
import deckQuery
import localConfig
from fieldToColumnMapper import gColumnToField, fieldToGColumn


class DiffablePrint:
    
    origFilename = 'spreadsheet.txt'
    newFilename = 'deck.txt'
    
    columnOrder = [
                'core-index',
                'opt-voc-index',
                'opt-sen-index',
                'vocab-expression',
                'vocab-kana',
                'vocab-meaning',
                'vocab-sound-local',
                'vocab-pos',
                'sentence-expression',
                'sentence-kana',
                'sentence-meaning',
                'sentence-sound-local',
                'sentence-image-local',
                'vocab-furigana',
                'sentence-furigana',
                'sentence-cloze',
                'jlpt',
                'sent-ko-index',
                'vocab-ko-index',
                ]
    
    def __init__(self):
        self.oldColumnValues = {}
        self.newColumnValues = {}
        
    def prepareFiles(self):
        orig = open(self.origFilename, 'w')
        new = open(self.newFilename, 'w')
        for column in self.columnOrder:
            orig.write(column + '\t')
            new.write(column + '\t')
        orig.write('\n')
        new.write('\n')
        
    def prepareConsole(self):
        for column in self.columnOrder:
            print column + '\t',
        print
    
    def addColumnValue(self, column, oldValue, newValue):    
        self.oldColumnValues[column] = oldValue
        self.newColumnValues[column] = newValue
        
    def printToFile(self):
        orig = open(self.origFilename, 'a')
        new = open(self.newFilename, 'a')

        for column in self.columnOrder:
            try:
                orig.write(self.oldColumnValues.get(column, '') + '\t')
            except:
                orig.write('' + '\t')

            new.write(self.newColumnValues.get(column, '') + '\t')

        orig.write('\n')
        new.write('\n')
    
    def printToConsole(self):
        print '-',
        for column in self.columnOrder:
            try:
                print self.oldColumnValues.get(column, '') + '\t',
            except:
                print '' + '\t',
        print
        print '+',
        for column in self.columnOrder:
            print self.newColumnValues.get(column, '') + '\t',
        print

    
dq = deckQuery.DeckQuery()
factsOfInterest = dq.getAllFactsWithTag(deckQuery.tag_clozeFIX)
factDictByCoreIndex = {}

for fact in factsOfInterest:
    factDictByCoreIndex[fact['Core-Index']] = fact

def changeCells(gd_client, spreadsheet_id, worksheet_id, deck):
    print 'Accessing spreadsheet...'
    rows = gd_client.GetListFeed(spreadsheet_id, worksheet_id).entry
    print 'Making changes to the spreadsheet...'
    for row in rows:
        coreIndex = row.custom['core-index'].text
        optVocIndex = row.custom['opt-voc-index'].text
        try:
            factDict = deck.getFactByCoreIndex(coreIndex)
        except:
            print "Tried to access invalid fact id for coreIndex ", coreIndex
            continue
        
        if factDict['Sentence-Image'] is not None and\
        factDict['Sentence-Image'] != "":
            row.custom['sentence-image-local'].text = factDict['Sentence-Image']
            newData = getNewRowDictFromExistingRow(row.custom)
            saved = False
            while not saved:
                try:
                    nrow = gd_client.UpdateRow(row, newData)
                    print "Saved: opt-voc-index[%s]\tcore-index[%s]" %\
                        (optVocIndex, coreIndex)
                    saved = True
                except gdata.service.RequestError, e:
                    print "Error saving row: %s\t::\t" % (e.message,
                                                          optVocIndex) 
                    print "Retrying in 30 seconds"
                    time.sleep(32)
    print "Done!"
                    


def getNewRowDictFromExistingRow(rowDict):
    newDict = {}
    for k,v in rowDict.iteritems():
        newDict[k] = v.text
    return newDict
    

def findDifferences(gd_client, spreadsheet_id, worksheet_id):
    rows = gd_client.GetListFeed(spreadsheet_id, worksheet_id).entry
    
    dp = DiffablePrint()
    dp.prepareConsole()
        
    for row in rows:
        coreIndex = row.custom['core-index'].text  
        if coreIndex in factDictByCoreIndex.keys():
            dp = DiffablePrint()
            gSheetValue = None
            deckValue = None
            
            for field in row.custom:
                gSheetValue = row.custom[field].text
                
                if field not in gColumnToField.keys():
                    deckValue = ''
                else:
                    deckFieldName = gColumnToField[field]
                    if deckFieldName is None:
                        deckValue = ''
                    else:
                        deckValue = factDictByCoreIndex[coreIndex][deckFieldName]
    
                dp.addColumnValue(field, gSheetValue, deckValue)
            dp.printToConsole()
    
def mergeColumnGsheetToDeck(gd_client, spreadsheet_id, worksheet_id, deck,
                            deckFieldName):
    rows = gd_client.GetListFeed(spreadsheet_id, worksheet_id).entry
    gSheetColumnName = fieldToGColumn[deckFieldName]
    dp = DiffablePrint()
    for row in rows:
        coreIndex = row.custom['core-index'].text
        if row.custom[gSheetColumnName] is not None:
            fieldValue = row.custom[gSheetColumnName].text
            if fieldValue is not None: 
                deck.updateFieldByCoreIndex(coreIndex, deckFieldName,
                                            fieldValue)
                print "Updated %s\t::\t%s" % (coreIndex, fieldValue)

# Ignore or delete this
def mergeColumnGsheetToDeckTweak(gd_client, spreadsheet_id, worksheet_id, deck,
                            deckFieldName):
    rows = gd_client.GetListFeed(spreadsheet_id, worksheet_id).entry
    gSheetColumnName = fieldToGColumn[deckFieldName]
    dp = DiffablePrint()
    for row in rows:
        coreIndex = row.custom['core-index'].text
        optVocIndex = row.custom['opt-voc-index'].text
        if row.custom[gSheetColumnName] is not None:
            fieldValue = row.custom[gSheetColumnName].text
            if fieldValue is not None: 
                deck.updateFieldByCoreIndex(optVocIndex, deckFieldName,
                                            fieldValue)
                print "Updated %s\t::\t%s" % (coreIndex, fieldValue)


if __name__ == "__main__":
    gd_client = gdata.spreadsheet.service.SpreadsheetsService()
    gd_client.email = localConfig.GOOGLE_USERNAME
    gd_client.password = localConfig.GOOGLE_PASSWORD
    gd_client.source = "I don't know what this does~"
    gd_client.ProgrammaticLogin()
    
    q = gdata.spreadsheet.service.DocumentQuery()
    q['title'] = localConfig.DOC_NAME
    q['title-exact'] = 'true'
    feed = gd_client.GetSpreadsheetsFeed(query=q)
    spreadsheet_id = feed.entry[0].id.text.rsplit('/',1)[1]
    feed = gd_client.GetWorksheetsFeed(spreadsheet_id)
    worksheet_id = feed.entry[0].id.text.rsplit('/',1)[1]
    
    #findDifferences(gd_client, spreadsheet_id, worksheet_id)
    changeCells(gd_client, spreadsheet_id, worksheet_id, dq)
    #mergeColumnGsheetToDeckTweak(gd_client, spreadsheet_id, worksheet_id, dq, 'Sentence-Image')
    
