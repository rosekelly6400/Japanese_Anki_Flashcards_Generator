import csv
import genanki
import apiCallFuncs
import ankiDeckTemplates
import time
import os

def getFuriganaHtml(wordKanji, wordReading):
    return f"<ruby>{wordKanji}<rt>{wordReading}</rt></ruby>"

def getAllVocabStringFromReader(vocab_reader, vocab_list_file):
    all_vocab_string = ""
    for row in vocab_reader:
        currentVocab = row[1]
        vocabTranslation = row[2]
        all_vocab_string += currentVocab + ": " + vocabTranslation + "; "
    vocab_list_file.seek(0)
    return all_vocab_string

def getAllKanjiMeanings(word):
    with open('Kanji_Lists/all_Kanji.csv', newline='', encoding='utf-8') as all_kanji_file:
        word_kanji_meanings = ''
        all_kanji_reader = csv.reader(all_kanji_file)
        for character in word:
            for row in all_kanji_reader:
                if character in row[0]:
                    if word_kanji_meanings != '':
                        word_kanji_meanings += '<br> '
                    meaning = row[0] + ': '  + row[4]
                    reading = "Kun: " + row[2] + "; On: " + row[1]
                    story =  row[18]
                    word_kanji_meanings += meaning + "<br>"+ reading + "<br>" + story + "<br>"
            all_kanji_file.seek(0)
        return word_kanji_meanings
    
def createAnkiDeckFile(fields, media_files, deckPath, deckName, addSentenceTTS=False):
    my_model = genanki.Model(
    #put random number here
    13801240614,
    'newVocabDeck',
    fields=ankiDeckTemplates.VocabCardNoTTSFields ,
    templates=[
        ankiDeckTemplates.VocabCardNoTTSTemplate
    ],
    css=ankiDeckTemplates.VocabCardCSS)

    if addSentenceTTS:
        my_model = genanki.Model(
        #put random number here
        13801240614,
        'newVocabDeck',
        fields= ankiDeckTemplates.VocabCardTTSFields,
        templates=[
            ankiDeckTemplates.VocabCardTTSTemplate,
        ],
        css=ankiDeckTemplates.VocabCardCSS)

    my_deck = genanki.Deck(13801240614, deckName)

    for vocabFields in fields:
        print(vocabFields)
        note = genanki.Note(
            model=my_model, fields=vocabFields
        )
        my_deck.add_note(note)


    my_package = genanki.Package(my_deck)
    my_package.media_files = media_files
    my_package.write_to_file(deckPath)


def getVocabCardFields(vocabListFile, outputFileName, addSentenceTTS):
    with open(vocabListFile, newline='', encoding='utf-8') as vocab_list_file, \
         open(outputFileName, 'w', newline='', encoding='utf-8') as output_file:
        vocab_reader = csv.reader(vocab_list_file)
        writer = csv.writer(output_file)

        vocabData = {}
        all_vocab_string = getAllVocabStringFromReader(vocab_reader, vocab_list_file)
        fields = []
        i = 0
        media_files = []

        for row in vocab_reader:
            currentVocab = row[1]
            start = currentVocab.find("（")
            end = currentVocab.find("）")
            pronunciation = row[0]
            print(currentVocab, start, end)
            print(pronunciation)
            # Extract the text inside the parentheses
            if start != -1 and end != -1:
                pronunciation = currentVocab[start + 1:end]
                currentVocab = currentVocab[0:start]

            vocabTranslation = row[2]
            vocabFuriganaHtml = getFuriganaHtml(currentVocab, pronunciation)
            print(vocabFuriganaHtml)
            kanji_meanings = getAllKanjiMeanings(currentVocab)

            try:
                example_sentence, sentence_translation = getExampleSentence(currentVocab, vocabTranslation, all_vocab_string)
            except:
                print("Error with api call that may be due to too many calls per minute, retrying call after wait period")
                time.sleep(60)
                example_sentence, sentence_translation = getExampleSentence(currentVocab, vocabTranslation, all_vocab_string)

            TTS_filename = f'read_aloud{currentVocab}1.mp3'
            apiCallFuncs.createVoiceVoxTTSFile('16', pronunciation, TTS_filename)
            media_files.append(f"{TTS_filename}")

            current_vocab_row = [currentVocab, vocabTranslation, vocabFuriganaHtml, kanji_meanings, example_sentence, sentence_translation]

            if addSentenceTTS:
                TTS_sentence_filename = f'read_aloud_sentence{currentVocab}1.mp3'
                apiCallFuncs.createVoiceVoxTTSFile('16', example_sentence, TTS_sentence_filename)
                media_files.append(f"{TTS_sentence_filename}")
                #adds sentence audio AND removes furigana from sentence
                current_vocab_row = [currentVocab, vocabTranslation, vocabFuriganaHtml, kanji_meanings, example_sentence, sentence_translation, f"[sound:{TTS_filename}]", f"[sound:{TTS_sentence_filename}]"]
            
            fields.append(current_vocab_row)
            i = i + 1
        return fields,media_files

def getExampleSentence(word, meaning, all_vocab_string): 
    userWordMessage = "" + word + ': ' + meaning
    messages = [ {"role": "system", "content":  
              "When the user gives a Japanese word and its meaning, you must respond only with a short, simple N3 example sentence in natural and correct japanese using that word. You may conjugate the word if it is a verb. "
               +"You must use this format: \'Japanese Sentence (English Translation)\' "} ]

    messages.append( 
        {"role": "user", "content": userWordMessage}, 
    )
    reply = apiCallFuncs.openAiApiCall(messages)
    
    sentence, translation = "", ""
    if "(" in reply:
        sentence = reply.split("(", 1)[0]
        translation = "(" + reply.split("(", 1)[1]
        print("Creating Sentence with: ", word)
    return sentence, translation

if __name__ == "__main__":
    vocab_file = "Vocab_Lists/test.csv"
    grammar_file = "Grammar_Lists/JLPTN3.csv"
    outputFile = "Generated_Anki_Decks/test1.apkg"
    deckName = "test 1"

    addSentenceTTS = True

    fields, media_files = getVocabCardFields(vocab_file, outputFile, addSentenceTTS)
    createAnkiDeckFile(fields, media_files, outputFile, deckName, addSentenceTTS)

    print("VOCAB anki deck file has been created successfully.")