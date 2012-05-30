# -*- coding: utf-8 -*-

import re

from deckQuery import DeckQuery

dq = DeckQuery()
c = dq.getDbCursor()


def isKana(s):
    if s < u'\u3041' or s > u'\u30FF':
        return False
    return True

def checkInnerComma(doFix=False):
    '''
    Prints out and optionally fixes all cases of a poorly placed comma.
    E.g., 今日、[きょう] will be fixed as 今日[きょう]、
    '''
    innerComma_re = re.compile(ur'、(\[.+?])', re.UNICODE)

    print '######### Poorly placed commas #########'
    found = 0
    s = 'SELECT id FROM facts'
    facts = c.execute(s).fetchall()
    for fact in facts:
        fact_id = fact['id'].__str__()
        factDict = dq.getFactDict(fact_id)
        clozeField = factDict['Sentence-Clozed']
        
        commaPortion = innerComma_re.search(clozeField)
        if commaPortion is not None:
            # Comma inside furiganafied word!
            found += 1
            print factDict['Core-Index'], '\t::\t', clozeField
            if doFix:
                fixedComma = commaPortion.group(1) + '、'
                fixed = re.sub(innerComma_re, fixedComma, clozeField)
                print '\t-->\t', fixed
                dq.updateFieldByCoreIndex(factDict['Core-Index'],
                                          'Sentence-Clozed', fixed)
    print "Found: ", found 
    

def checkSpacedByCommaFurigana(doFix=False):
    '''
    Prints out and optionally fixes all cases of poorly combined furigana
    there resulted from commas (most likely confusing some automated tool) 
    E.g., 最近、銀行[さいきん ぎんこう] will be fixed as 
    最近[さいきん]、 銀行[ぎんこう]
    '''
    innerSpace_re = re.compile(ur'(\w+)、(\w+)\[(\w+)\s+(\w+)\]', re.UNICODE)

    print '######### Space inside furigana #########'
    found = 0
    s = 'SELECT id FROM facts'
    facts = c.execute(s).fetchall()
    for fact in facts:
        fact_id = fact['id'].__str__()
        factDict = dq.getFactDict(fact_id)
        clozeField = factDict['Sentence-Clozed']
        
        spaceMatch = innerSpace_re.search(clozeField)
        if spaceMatch is not None:
            # Space inside furiganafied word!
            found += 1
            print factDict['Core-Index'], '\t::\t', clozeField
            if doFix:
                firstWord = spaceMatch.group(1)
                secondWord = spaceMatch.group(2)
                firstFuri = spaceMatch.group(3)
                secondFuri = spaceMatch.group(4)
                
                fixedFuri = '%s[%s]、%s[%s]' % (firstWord, firstFuri,
                                               secondWord, secondFuri) 
                
                fixed = re.sub(innerSpace_re, fixedFuri, clozeField)
                print '\t-->\t', fixed
                dq.updateFieldByCoreIndex(factDict['Core-Index'],
                                          'Sentence-Clozed', fixed)
    print "Found: ", found    

def checkNoCloze():
    '''
    Prints out all cases of a missing cloze deletion
    '''
    hasCloze_re = re.compile(ur'<b>(.+)</b>', re.UNICODE)

    print '######### No cloze deletions #########'
    found = 0
    s = 'SELECT id FROM facts'
    facts = c.execute(s).fetchall()
    for fact in facts:
        fact_id = fact['id'].__str__()
        factDict = dq.getFactDict(fact_id)
        clozeField = factDict['Sentence-Clozed']
        
        clozedPortion = hasCloze_re.search(clozeField)
        if clozedPortion is None:
            # No cloze deletion in this field!
            found += 1
            print factDict['Core-Index'], '\t::\t', clozeField
                
    print "Found: ", found 

def extraSpace1(doFix=False):
    '''
    Prints out all cases of multiple spaces appearing together and
    optionally fix them.
    '''
    hasSpaces_re = re.compile(ur'\s\s+', re.UNICODE)

    print '######### Extra spaces #########'
    found = 0
    s = 'SELECT id FROM facts'
    facts = c.execute(s).fetchall()
    for fact in facts:
        fact_id = fact['id'].__str__()
        factDict = dq.getFactDict(fact_id)
        clozeField = factDict['Sentence-Clozed']
        
        spacedPortion = hasSpaces_re.search(clozeField)
        if spacedPortion is not None:
            found += 1
            print factDict['Core-Index'], '\t::\t', clozeField
            if doFix:
                #TODO: add a fix rule for this case
                pass
    print "Found: ", found 

def extraSpace2(doFix=False):
    '''
    Prints out all cases of multiple spaces occurring because one was
    inside <b> tags, and optionally fix them.
    '''
    hasSpaces_re = re.compile(ur'\s<b>\s', re.UNICODE)

    print '######### Extra spaces #########'
    found = 0
    s = 'SELECT id FROM facts'
    facts = c.execute(s).fetchall()
    for fact in facts:
        fact_id = fact['id'].__str__()
        factDict = dq.getFactDict(fact_id)
        clozeField = factDict['Sentence-Clozed']
        
        spacedPortion = hasSpaces_re.search(clozeField)
        if spacedPortion is not None:
            found += 1
            print factDict['Core-Index'], '\t::\t', clozeField
            if doFix:
                #TODO: add a fix rule for this case
                pass
    print "Found: ", found 


def spaceInFurigana(doFix=False):
    '''
    
    '''
    innerSpace_re = re.compile(ur'(\w+)\[(\w+)\s+(\w+)\]', re.UNICODE)

    print '######### Space inside furigana #########'
    found = 0
    s = 'SELECT id FROM facts'
    facts = c.execute(s).fetchall()
    for fact in facts:
        fact_id = fact['id'].__str__()
        factDict = dq.getFactDict(fact_id)
        clozeField = factDict['Sentence-Clozed']
        
        spaceMatch = innerSpace_re.search(clozeField)
        if spaceMatch is not None:
            # Space inside furiganafied word!
            found += 1
            print factDict['Core-Index'], '\t::\t', clozeField
            if doFix:
                fixed = re.sub(innerSpace_re, '', clozeField)
                print '\t-->\t', fixed
                #dq.updateFieldByCoreIndex(factDict['Core-Index'],
                #                          'Sentence-Clozed', fixed)
                
    print "Found: ", found  

if __name__ == "__main__":
    #It is likely that the order is important. It's best to follow this order,
    #just to be sure.
    
    #checkNoCloze()
    #checkInnerComma(doFix=False)
    #checkSpacedByCommaFurigana(doFix=False)
    #extraSpace1(doFix=False)
    #extraSpace2(doFix=False)
    spaceInFurigana(doFix=False)
    
    dq.commit()