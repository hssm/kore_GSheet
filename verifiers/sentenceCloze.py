# -*- coding: utf-8 -*-

import re

from deckQuery import DeckQuery

dq = DeckQuery()
c = dq.getDbCursor()


def isKana(s):
    if s < u'\u3041' or s > u'\u30FF':
        return False
    return True

def checkInnerComma():
    innerComma_re = re.compile(ur'、\[', re.UNICODE)

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
    print "Found: ", found 
    
    
def checkNoCloze():
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
    

#        #print "::"+spaceBold.group(2)[:1] 
#        #clean_field = spaceBold.group(1)+'、'
#        #clean_field = re.sub(spaceBold_re, clean_field, field_value)
#        print spaceBold.group(0), ' :: ', field_value
#        count += 1
#        s = '''UPDATE fields
#               SET value=?
#               WHERE id=?
#            '''
#        #c.execute(s, [clean_field, field['id']])
#    #conn.commit()

if __name__ == "__main__":
    checkNoCloze()
    checkInnerComma()