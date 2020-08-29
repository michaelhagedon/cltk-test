from cltk.corpus.utils.importer import CorpusImporter
from cltk.corpus.readers import get_corpus_reader
from cltk.stem.lemma import LemmaReplacer
from cltk.corpus.utils.formatter import cltk_normalize
from cltk.lemmatize.greek.backoff import BackoffGreekLemmatizer
from cltk.phonology.greek.transcription import Transcriber
from cltk.tag.pos import POSTag
from cltk.tag import ner

corpus_importer = CorpusImporter('greek')
corpus_importer.import_corpus('greek_models_cltk')

corpus_importer2 = CorpusImporter('greek')
corpus_importer2.import_corpus('greek_text_perseus')

philippians_reader = get_corpus_reader(corpus_name="greek_text_perseus", language="greek")

philippians_reader._fileids =['new-testament__letter-to-the-philippians__grc.json']

# print(list(perseus_reader.sents()))

sentences = list(philippians_reader.sents())
sentence = cltk_normalize(sentences[0])
lemmatizer = LemmaReplacer('greek')
word_list = lemmatizer.lemmatize(sentence)

tagger = POSTag('greek')

parts_of_speech = tagger.tag_ngram_123_backoff(sentence)

# This is not a great lemmatizer
standard_list = lemmatizer.lemmatize(list(philippians_reader.words()), return_raw=True)

lemmatizer2 = BackoffGreekLemmatizer()

# this one seems better
backoff_list = lemmatizer2.lemmatize(list(philippians_reader.words()))

# Find most names
names_in_first_sentence = ner.tag_ner('greek', input_text=sentence, output_type=list)

transcriber = Transcriber(dialect="Attic", reconstruction="Probert")
ipa = transcriber.transcribe(sentence)