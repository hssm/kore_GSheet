# -*- coding: utf-8 -*-

import re

from deckQuery import DeckQuery

dq = DeckQuery()
c = dq.getDbCursor()


def isKana(s):
    if s < u'\u3041' or s > u'\u30FF':
        return False
    return True


def checkSpace(doFix=False):
    '''
    There should be no spaces in the expression field
    '''
    hasSpaces_re = re.compile(ur'\s+', re.UNICODE)

    print '######### Contain spaces #########'
    found = 0
    s = 'SELECT id FROM facts'
    facts = c.execute(s).fetchall()
    for fact in facts:
        fact_id = fact['id'].__str__()
        factDict = dq.getFactDict(fact_id)
        exprField = factDict['Expression']
        
        spacedPortion = hasSpaces_re.search(exprField)
        if spacedPortion is not None:
            found += 1
            print factDict['Core-Index'], '\t::\t', exprField
            if doFix:
                #TODO: add a fix rule for this case
                pass
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
        exprField = factDict['Expression']
        
        spacedPortion = hasSpaces_re.search(exprField)
        if spacedPortion is None:
            found += 1
            print factDict['Core-Index'], '\t::\t', exprField

    print "Found: ", found 


if __name__ == "__main__":

    checkSpace(doFix=False)
    checkNoBold(doFix=False)
    #dq.commit()