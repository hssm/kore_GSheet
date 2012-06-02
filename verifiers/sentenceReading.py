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
        sentKanaField = factDict['Reading']
        
        commaPortion = innerComma_re.search(sentKanaField)
        if commaPortion is not None:
            # Comma inside furiganafied word!
            found += 1
            print factDict['Core-Index'], '\t::\t', sentKanaField
            if doFix:
                fixedComma = commaPortion.group(1) + '、'
                fixed = re.sub(innerComma_re, fixedComma, sentKanaField)
                print '\t-->\t', fixed
                dq.updateFieldByCoreIndex(factDict['Core-Index'],
                                          'Reading', fixed)
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
        sentKanaField = factDict['Reading']
        
        spaceMatch = innerSpace_re.search(sentKanaField)
        if spaceMatch is not None:
            # Space inside furiganafied word!
            found += 1
            print factDict['Core-Index'], '\t::\t', sentKanaField
            if doFix:
                firstWord = spaceMatch.group(1)
                secondWord = spaceMatch.group(2)
                firstFuri = spaceMatch.group(3)
                secondFuri = spaceMatch.group(4)
                
                fixedFuri = '%s[%s]、 %s[%s]' % (firstWord, firstFuri,
                                               secondWord, secondFuri) 
                
                fixed = re.sub(innerSpace_re, fixedFuri, sentKanaField)
                print '\t-->\t', fixed
                dq.updateFieldByCoreIndex(factDict['Core-Index'],
                                          'Reading', fixed)
    print "Found: ", found    

def extraSpace1(doFix=False):
    '''
    Prints out all cases of multiple spaces appearing together and
    optionally fix them.
    '''
    hasSpaces_re = re.compile(ur'\s\s+', re.UNICODE)

    print '######### Extra spaces1 #########'
    found = 0
    s = 'SELECT id FROM facts'
    facts = c.execute(s).fetchall()
    for fact in facts:
        fact_id = fact['id'].__str__()
        factDict = dq.getFactDict(fact_id)
        sentKanaField = factDict['Reading']
        
        spacedPortion = hasSpaces_re.search(sentKanaField)
        if spacedPortion is not None:
            found += 1
            print factDict['Core-Index'], '\t::\t', sentKanaField
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

    print '######### Extra spaces2 #########'
    found = 0
    s = 'SELECT id FROM facts'
    facts = c.execute(s).fetchall()
    for fact in facts:
        fact_id = fact['id'].__str__()
        factDict = dq.getFactDict(fact_id)
        sentKanaField = factDict['Reading']
        
        spacedPortion = hasSpaces_re.search(sentKanaField)
        if spacedPortion is not None:
            found += 1
            print factDict['Core-Index'], '\t::\t', sentKanaField
            if doFix:
                #TODO: add a fix rule for this case
                pass
    print "Found: ", found 

def extraSpace3(doFix=False):
    '''
    Prints out all cases of a space after a </b>,  where the next
    character is a kana (so no space should be there).
    From: <b>昨日[さくじつ]</b> は 雨[あめ]でしたね。
    To  : <b>昨日[さくじつ]</b>は 雨[あめ]でしたね。
    '''
    hasSpaces_re = re.compile(ur'(</b>)\s(\w)', re.UNICODE)

    print '######### Extra spaces3 #########'
    found = 0
    s = 'SELECT id FROM facts'
    facts = c.execute(s).fetchall()
    for fact in facts:
        fact_id = fact['id'].__str__()
        factDict = dq.getFactDict(fact_id)
        sentKanaField = factDict['Reading']
        
        spacedPortion = hasSpaces_re.search(sentKanaField)
        if spacedPortion is not None:
            nextChar = spacedPortion.group(2)
            if isKana(nextChar):
                found += 1
                print factDict['Core-Index'], '\t::\t', sentKanaField
                if doFix:
                    fixedSpace = spacedPortion.group(1) + spacedPortion.group(2) 
                    fixed = re.sub(hasSpaces_re, fixedSpace, sentKanaField)
                    print '\t-->\t', fixed
                    dq.updateFieldByCoreIndex(factDict['Core-Index'],
                                              'Reading', fixed)
                    pass
    print "Found: ", found 

def extraSpace4(doFix=False):
    '''
    Prints out all cases of a space after a ],  where the next
    character is a kana (so no space should be there).
    '''
    hasSpaces_re = re.compile(ur'(\])\s(\w)', re.UNICODE)

    print '######### Extra spaces4 #########'
    found = 0
    s = 'SELECT id FROM facts'
    facts = c.execute(s).fetchall()
    for fact in facts:
        fact_id = fact['id'].__str__()
        factDict = dq.getFactDict(fact_id)
        sentKanaField = factDict['Reading']
        
        spacedPortion = hasSpaces_re.search(sentKanaField)
        if spacedPortion is not None:
            nextChar = spacedPortion.group(2)
            if isKana(nextChar):
                found += 1
                print factDict['Core-Index'], '\t::\t', sentKanaField
                if doFix:
                    fixedSpace = spacedPortion.group(1) + spacedPortion.group(2) 
                    fixed = re.sub(hasSpaces_re, fixedSpace, sentKanaField)
                    print '\t-->\t', fixed
                    dq.updateFieldByCoreIndex(factDict['Core-Index'],
                                              'Reading', fixed)
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
        sentKanaField = factDict['Reading']
        
        spacedPortion = hasSpaces_re.search(sentKanaField)
        if spacedPortion is None:
            found += 1
            print factDict['Core-Index'], '\t::\t', sentKanaField

    print "Found: ", found 
    
if __name__ == "__main__":

    checkInnerComma(doFix=False)
    checkSpacedByCommaFurigana(doFix=False)
    extraSpace1(doFix=False)
    extraSpace2(doFix=False)
    extraSpace3(doFix=False)
    extraSpace4(doFix=False)
    checkNoBold(doFix=False)
    #dq.commit()