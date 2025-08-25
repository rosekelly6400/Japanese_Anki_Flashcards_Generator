
#With TTS
VocabCardTTSFields = [
    {'name': 'japanese word'},
    {'name': 'english meaning'},
    {'name': 'vocab furigana html'},
    {'name': 'kanji meanings'},
    {'name': 'sentence html'},
    {'name': 'sentence translation'},
    {"name": "TTS"}, # [sound:sound.mp3]
    {"name": "sentence TTS"} # [sound:sound.mp3]
]
VocabCardTTSTemplate = {
    'name': 'Card 1',
    'qfmt': '<span style="font-family:YUGOTHB;font-size:75px;"> {{japanese word}}</span><span style="font-family:KanjiStrokeOrders; font-size: 75px; ">{{japanese word}}</span>',
    'afmt': """
        <span style="font-family:YUGOTHB;font-size:75px;"> {{TTS}} {{vocab furigana html}}</span>
        <span style="font-family:KanjiStrokeOrders; font-size: 75px; ">{{vocab furigana html}}</span>
        <hr id=answer>
        <span style="font-family: Mincho; font-size: 22px; font-weight: bold;">{{english meaning}}</span>
        <span style="font-family: Mincho; font-size: 24px;"><br> {{kanji meanings}}
        <br><br>

        <span style="font-size: 40px;">{{sentence TTS}}{{sentence html}}</span>
        <br><br><br><br><br>

        <span style="color: gray; font-size: 18px;">{{sentence translation}}</span>
        </span>"""
}

#Without TTS
VocabCardNoTTSFields = [
    {'name': 'japanese word'},
    {'name': 'english meaning'},
    {'name': 'vocab furigana html'},
    {'name': 'kanji meanings'},
    {'name': 'sentence html'},
    {'name': 'sentence translation'}
]

VocabCardNoTTSTemplate = {
    'name': 'Card 1',
    'qfmt': '<span style="font-family:YUGOTHB;font-size:75px;"> {{japanese word}}</span><span style="font-family:KanjiStrokeOrders; font-size: 75px; ">{{japanese word}}</span>',
    'afmt': """
        <span style="font-family:YUGOTHB;font-size:75px;"> {{vocab furigana html}}</span>
        <span style="font-family:KanjiStrokeOrders; font-size: 75px; ">{{vocab furigana html}}</span>
        <hr id=answer>
        <span style="font-family: Mincho; font-size: 22px; font-weight: bold;">{{english meaning}}</span>
        <span style="font-family: Mincho; font-size: 24px;"><br> {{kanji meanings}}
        <br><br>

        <span style="font-size: 40px;">{{sentence html}}</span>
        <br><br><br><br><br>

        <span style="color: gray; font-size: 18px;">{{sentence translation}}</span>
        </span>"""
} 


VocabCardCSS = """
    .card {
    font-family: arial;
    font-size: 20px;
    text-align: center;
    color: black;
    background-color: white;
    }

    .card1 { background-color: #ffffff; }

    @font-face { font-family: YUMIN; src: url('_YUMIN.ttf'); }
    @font-face { font-family: KanjiStrokeOrders; src: url('_KanjiStrokeOrders.ttf'); }
    @font-face { font-family: HGRKK; src: url('_HGRKK.ttc'); }
    @font-face { font-family: YUGOTHB; src: url('_YUGOTHB.ttc'); }
    """