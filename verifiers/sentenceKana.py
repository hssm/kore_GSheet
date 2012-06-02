# -*- coding: utf-8 -*-

import re

from deckQuery import DeckQuery

dq = DeckQuery()
c = dq.getDbCursor()


def isKana(s):
    if s < u'\u3041' or s > u'\u30FF':
        return False
    return True


def checkInnerSpace(doFix=False):
    '''
    Checks for spaces inside bold tags. We don't want them in the kana field
    '''
    hasSpacesLeft_re = re.compile(ur'<b>\s.+</b>', re.UNICODE)
    hasSpacesRight_re = re.compile(ur'<b>.+\s</b>', re.UNICODE)

    print '######### Inner spaces #########'
    found = 0
    s = 'SELECT id FROM facts'
    facts = c.execute(s).fetchall()
    for fact in facts:
        fact_id = fact['id'].__str__()
        factDict = dq.getFactDict(fact_id)
        sentKanaField = factDict['Sentence-Kana']
        
        leftSpacePortion = hasSpacesLeft_re.search(sentKanaField)
        rightSpacePortion = hasSpacesRight_re.search(sentKanaField)
        if leftSpacePortion is not None:
            found += 1
            print factDict['Core-Index'], '\t::\t', sentKanaField
        if rightSpacePortion is not None:
            found += 1
            print factDict['Core-Index'], '\t::\t', sentKanaField

    print "Found: ", found 


def checkNoBold(doFix=False):
    '''
    Prints out all cases where the key word isn't emboldened
    '''
    hasSpaces_re = re.compile(ur'<b>.+</b>', re.UNICODE)

    print '######### No bold #########'
    found = 0
    s = 'SELECT id FROM facts'
    facts = c.execute(s).fetchall()
    for fact in facts:
        fact_id = fact['id'].__str__()
        factDict = dq.getFactDict(fact_id)
        sentKanaField = factDict['Sentence-Kana']
        
        spacedPortion = hasSpaces_re.search(sentKanaField)
        if spacedPortion is None:
            found += 1
            print factDict['Core-Index'], '\t::\t', sentKanaField

    print "Found: ", found 
    
if __name__ == "__main__":

    checkInnerSpace(doFix=False)
    checkNoBold(doFix=False)
    #dq.commit()