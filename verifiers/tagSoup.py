# -*- coding: utf-8 -*-

import re
from deckQuery import DeckQuery

dq = DeckQuery()
c = dq.getDbCursor()


def removeRichTextEmpty(doFix=False):
    empty_span = re.compile(ur'<span style="font-weight:600;"> </span>',
                            re.UNICODE)
    
    print '######### Tag soup (empty) #########'
    found = 0
    s = 'SELECT id FROM facts'
    facts = c.execute(s).fetchall()
    for fact in facts:
        fact_id = fact['id'].__str__()
        s = '''
            SELECT * FROM fields
            WHERE factId=?
            '''
        fields = c.execute(s, [fact_id]).fetchall()       
        
        for field in fields:
            field_value = field['value']
            hasJunk = empty_span.search(field_value)
            if hasJunk is not None:
                print "Fixing: ", field_value
                found += 1
                clean_field = re.sub(empty_span, '', field_value)
                     
                s = '''UPDATE fields
                       SET value=?
                       WHERE id=?
                    '''
                c.execute(s, [clean_field, field['id']])
    print "Found: ", found 


def removeRichTextWithContent(doFix=False):
    span_re = re.compile(ur'<span style="font-weight:600;">(.+)</span>',
                            re.UNICODE)
    
    print '######### Tag soup (with content) #########'
    found = 0
    s = 'SELECT id FROM facts'
    facts = c.execute(s).fetchall()
    for fact in facts:
        fact_id = fact['id'].__str__()
        s = '''
            SELECT * FROM fields
            WHERE factId=?
            '''
        fields = c.execute(s, [fact_id]).fetchall()       
        
        for field in fields:
            field_value = field['value']
            span = span_re.search(field_value)
            if span is not None:
                print "Fixing: ", field_value
                found += 1
                clean_field = re.sub(span_re, '<b>'+span.group(1)+'</b>',
                                       field_value)
                     
                s = '''UPDATE fields
                       SET value=?
                       WHERE id=?
                    '''
                c.execute(s, [clean_field, field['id']])
    print "Found: ", found 


if __name__ == "__main__":
   
    removeRichTextEmpty(doFix=False)
    removeRichTextWithContent(doFix=False)
    #dq.commit()