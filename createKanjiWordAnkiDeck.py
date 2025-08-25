import csv
from openai import OpenAI
import genanki
import voicevoxAudioFiles
import ankiDeckTemplates
import time
import os
from dotenv import load_dotenv

load_dotenv()

# Access an environment variable
OPENAI_APIKEY = os.getenv("OPENAI_APIKEY") 

def createAnkiDeck(fields, media_files, deckPath, deckName, addSentenceTTS=False):
    # Model WITHOUT Sentence TTS
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
        # Model WITH Sentence TTS
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

def getVocabCardFields(vocabListFile, grammarListFile, outputFileName, addSentenceTTS):
    with open(vocabListFile, newline='', encoding='utf-8') as vocab_list_file, \
         open(grammarListFile, newline='', encoding='utf-8') as grammar_list_file, \
         open(outputFileName, 'w', newline='', encoding='utf-8') as output_file:
        
        vocab_reader = csv.reader(vocab_list_file)
        grammar_reader = csv.reader(grammar_list_file)
        writer = csv.writer(output_file)

        vocabData = {}

        all_vocab_string = ""
        for row in vocab_reader:
            currentVocab = row[1]
            vocabTranslation = row[2]
            all_vocab_string += currentVocab + ": " + vocabTranslation + "; "

        all_grammar_string = ""
        grammar_for_ex_sentence = ""
        grammar_file_length = 0
        grammar_file_list = []
        for row in grammar_reader:
            all_grammar_string = all_grammar_string + "{" + row[0] + "}, "
            grammar_file_list.append(row[0])
            grammar_file_length += 1
        if len(all_grammar_string) > 2:
            all_grammar_string = all_grammar_string[:-2]
        
        vocab_list_file.seek(0)

        fields = []

        i = 0
        media_files = []
        for row in vocab_reader:
            currentVocab = row[1]
            start = currentVocab.find("（")
            end = currentVocab.find("）")
            pronunciation = row[0]
            print(type(currentVocab))
            print(currentVocab, start, end)
            print(pronunciation)
            # Extract the text inside the parentheses
            if start != -1 and end != -1:
                pronunciation = currentVocab[start + 1:end]
                currentVocab = currentVocab[0:start]

            vocabTranslation = row[2]
            vocabFuriganaHtml = getFuriganaHtml(currentVocab, pronunciation)
            print("VOCAB FURIGANA")
            print(vocabFuriganaHtml)
            kanji_meanings = getAllKanjiMeanings(currentVocab)

            if grammar_file_length > 0:
                grammar_for_ex_sentence = "{" + grammar_file_list[(i%grammar_file_length)] + "}"

            try:
                example_sentence, sentence_translation = getExampleSentence(currentVocab, vocabTranslation, all_vocab_string, all_grammar_string)
            except:
                print("Error")
                time.sleep(60)
                example_sentence, sentence_translation = getExampleSentence(currentVocab, vocabTranslation, all_vocab_string, all_grammar_string)
            # example_sentence = "EXAMPLE SENTENCE"
            # sentence_translation =  "sentence translation"
            #example_sentence_furigana_html = to_html(example_sentence)

            randomNumber = "1"

            TTS_filename = f'read_aloud{currentVocab}{randomNumber}.mp3'
            voicevoxAudioFiles.createVoiceVoxTTSFile('16', pronunciation, TTS_filename)
            media_files.append(f"{TTS_filename}")

            current_vocab_row = [currentVocab, vocabTranslation, vocabFuriganaHtml, kanji_meanings, example_sentence, sentence_translation, f"[sound:{TTS_filename}]"]

            if addSentenceTTS:
                TTS_sentence_filename = f'read_aloud_sentence{currentVocab}{randomNumber}.mp3'
                voicevoxAudioFiles.createVoiceVoxTTSFile('16', example_sentence, TTS_sentence_filename)
                media_files.append(f"{TTS_sentence_filename}")
                #adds sentence audio AND removes furigana from sentence
                current_vocab_row = [currentVocab, vocabTranslation, vocabFuriganaHtml, kanji_meanings, example_sentence, sentence_translation, f"[sound:{TTS_filename}]", f"[sound:{TTS_sentence_filename}]"]
            
            fields.append(current_vocab_row)
            i = i + 1
        return fields,media_files

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

def getFuriganaHtml(wordKanji, wordReading):
    return f"<ruby>{wordKanji}<rt>{wordReading}</rt></ruby>"

def getExampleSentence(word, meaning, all_vocab_string, grammar_string): 
    userWordMessage = "" + word + ': ' + meaning
    messages = [ {"role": "system", "content":  
              "When the user gives a Japanese word and its meaning, you must respond only with a short, simple N3 example sentence in natural and correct japanese using that word. You may conjugate the word if it is a verb. "
               +"You must use this format: \'Japanese Sentence (English Translation)\' "} ]
    print(messages)
    messages.append( 
                {"role": "user", "content": userWordMessage}, 
            ) 
    client = OpenAI(
        # This is the default and can be omitted
        api_key=OPENAI_APIKEY,
    )

    chat_completion = client.chat.completions.create(
        messages=messages,
        model="gpt-4-turbo",
    )
    reply = chat_completion.choices[0].message.content 
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

    #createVocabAnkiCSV(vocab_file, outputFile)
    #print(getExampleSentence('試合','match; game'))

    fields, media_files = getVocabCardFields(vocab_file, grammar_file, outputFile, addSentenceTTS)
    createAnkiDeck(fields, media_files, outputFile, deckName, addSentenceTTS)

    print("VOCAB anki deck file has been created successfully.")