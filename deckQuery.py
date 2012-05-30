# -*- coding: utf-8 -*-

import sqlite3
import localConfig

tag_clozeFIX = 1 # hardcoding: it's like magic, but worse!

class DeckQuery:
    
    def __init__(self):
        self.conn = sqlite3.connect(localConfig.DECK_PATH)
        self.conn.row_factory = sqlite3.Row
        self.c = self.conn.cursor()
            
        self.fieldIds = {}
        self.fieldNames = {}
        
        s = 'SELECT id, name FROM fieldModels'
        fieldsModels = self.c.execute(s)
        for fieldModel in fieldsModels:
            self.fieldIds[fieldModel['name']] = fieldModel['id']
            self.fieldNames[fieldModel['id']] = fieldModel['name']
    
    
    def getDbCursor(self):
        return self.c
    
    
    def getFieldModelIdOfField(self, fieldName):
        s = '''SELECT id
               FROM fieldModels
               WHERE name=?
         '''
        row = self.c.execute(s, [fieldName]).fetchone()
        return row['id'] 
    
    
    def getAllFactsWithTag(self, tag):
        facts = []
        s = '''
            SELECT cards.factId
            FROM cardTags
            LEFT OUTER JOIN cards
            ON cardTags.cardId=cards.id
            WHERE tagId=?
            '''
        cards = self.c.execute(s, [tag]).fetchall()
        for card in cards:
            factId = card['factId'].__str__()
            fact = self.getFactDict(factId)
            facts.append(fact)
        return facts        


    def getFactByCoreIndex(self, coreIndex):
        factId = self.getFactIdForCoreIndex(coreIndex)
        return self.getFactDict(factId)


    def getFactIdForCoreIndex(self, coreIndex):
        fieldModelId = self.getFieldModelIdOfField('Core-Index')
        s = '''
            SELECT factId
            FROM fields
            WHERE fieldModelId=? AND value=?'''
        row = self.c.execute(s, [fieldModelId, coreIndex]).fetchone()
        return row['factId']


    def getFactDict(self, factId):
        s = '''
            SELECT fields.value, fieldModels.name
            FROM fields
            LEFT OUTER JOIN fieldModels
            ON fields.fieldModelId=fieldModels.id
            WHERE factId=?
            '''
        fieldsOfFact = self.c.execute(s, [factId]).fetchall()
        fact = {}
        for fields in fieldsOfFact:
            fact[fields['name']] = fields['value']
        return fact


    def updateFieldByCoreIndex(self, coreIndex, fieldName, fieldValue):
        factId = self.getFactIdForCoreIndex(coreIndex)
        fieldModelId = self.getFieldModelIdOfField(fieldName)
        s = '''
            UPDATE fields
            SET value=?
            WHERE factId=? AND fieldModelId=?
            '''
        field = self.c.execute(s, [fieldValue, factId, fieldModelId]) 
        #self.conn.commit()
        

    def printCoreIndexOfClozeFixed(self):
        clozeFixFacts = self.getAllFactsWithTag(tag_clozeFIX)
        for fixedFact in clozeFixFacts:
            print "\n -------- ", fixedFact['Core-Index'], " -------- " 
            for (fieldName, fieldValue) in fixedFact.items():
                print fieldName, " :: ", fieldValue


    def commit(self):
        self.conn.commit()

if __name__ == "__main__":
    dq = DeckQuery()
    #dq.printCoreIndexOfClozeFixed()
    factId = dq.getFactIdForCoreIndex('1')
    dq.updateField(factId, 'Hint', 'TESTING STUFF!')
