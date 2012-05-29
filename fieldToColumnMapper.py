# -*- coding: utf-8 -*-

#spreadsheet order
fieldToGColumn = {
    'Core-Index'            :    'core-index',
    None                    :    'vocab-ko-index',
    None                    :    'sent-ko-index',  
    'Optimized-Voc-Index'   :    'opt-voc-index',
    'Optimized-Sent-Index'  :    'opt-sen-index',
    None                    :    'jlpt',
    'Vocabulary-Kanji'      :    'vocab-expression',
    'Vocabulary-Kana'       :    'vocab-kana',
    'Vocabulary-English'    :    'vocab-meaning',
    'Vocabulary-Audio'      :    'vocab-sound-local',
    'Vocabulary-Pos'        :    'vocab-pos',
    'Expression'            :    'sentence-expression',
    'Sentence-Kana'         :    'sentence-kana',
    'Sentence-English'      :    'sentence-meaning',
    'Sentence-Audio'        :    'sentence-sound-local',
    'Sentence-Image'        :    'sentence-image-local',
    'Vocabulary-Furigana'   :    'vocab-furigana',
    'Reading'               :    'sentence-furigana',
    'Sentence-Clozed'       :    'sentence-cloze',
        
    ## In deck, not in spreadsheet ##
    'Notes'                 :    None,
    'Hint'                  :    None,
}

# Another dict with the keys/values swapped
gColumnToField = {}
for key, value in fieldToGColumn.iteritems():
    gColumnToField[value] = key

def getGSheetColumnFromDeckField(fieldName):
    return fieldToGColumn[fieldName]

def getDeckFieldFromGSheetColumn(column):
    return gColumnToField[column]
