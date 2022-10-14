
try:
    import nltk
    import numpy as np
    import pickle
    from nltk.tokenize import word_tokenize, sent_tokenize, RegexpTokenizer
    from nltk import SnowballStemmer, WordNetLemmatizer, pos_tag
    from nltk.corpus import stopwords
    from string import punctuation
    import re

    import tensorflow.compat.v1 as tf
    tf.disable_v2_behavior()

    import tensorflow_hub as hub
    import sentencepiece as spm
    import numpy as np
    from absl import logging

except: ImportError('Packages missing, see requirement.txt')


global graph
graph = tf.get_default_graph()


class Use_model:
    
    def __init__(self):
        '''
        THis uses the lite version of universal sentence encoder
            ~ https://tfhub.dev/google/universal-sentence-encoder-lite/2

        Also see here: https://www.tensorflow.org/hub/tutorials/semantic_similarity_with_tf_hub_universal_encoder_lite
        '''

        spm_path = "univ_sent_encoder/universal-sentence-encoder-lite_2"

        module = hub.Module(spm_path)

        self.input_placeholder = tf.sparse_placeholder(tf.int64, shape=[None, None])
        self.encodings = module(
            inputs=dict(
                values=self.input_placeholder.values,
                indices=self.input_placeholder.indices,
                dense_shape=self.input_placeholder.dense_shape))

        with tf.Session() as sess:
            spm_path = sess.run(module(signature="spm_path"))

        self.sp = spm.SentencePieceProcessor()
        
        with tf.io.gfile.GFile(spm_path, mode="rb") as f:
            self.sp.LoadFromSerializedProto(f.read())
        
        #print("SentencePiece model loaded at {}.".format(spm_path))

    def process_to_IDs_in_sparse_format(self, sp, sentences):

        '''
         An utility method that processes sentences with the sentence piece processor
         'sp' and returns the results in tf.SparseTensor-similar format:
         (values, indices, dense_shape)
        '''
        ids = [sp.EncodeAsIds(x) for x in sentences]
        max_len = max(len(x) for x in ids)
        dense_shape=(len(ids), max_len)
        values=[item for sublist in ids for item in sublist]
        indices=[[row,col] for row in range(len(ids)) for col in range(len(ids[row]))]
        return (values, indices, dense_shape)

    def text_vector(self, sentence):

        self.sentence = sentence
        messages = [self.sentence]

        values, indices, dense_shape = self.process_to_IDs_in_sparse_format(self.sp, messages)

        # Reduce logging output.
        logging.set_verbosity(logging.ERROR)

        input_placeholder = self.input_placeholder

        with graph.as_default():
            with tf.Session() as session:
                session.run([tf.global_variables_initializer(), tf.tables_initializer()])
                message_embeddings = session.run(
                    self.encodings,
                    feed_dict={input_placeholder.values: values,
                                input_placeholder.indices: indices,
                                input_placeholder.dense_shape: dense_shape})

        self.vector = np.array(message_embeddings).tolist()

        return self.vector

model = Use_model()

#Demostration
#print(model.text_vector('i love creating useful project'))


class Encoder:
    def __init__(self):
        self.stop_words = stopwords.words('english')

    def cleaning_text(self, text: str):
        '''
        Input Parameter: text

        Output Parameter: cleaned_tokens => all the list of a sentences
        '''
        cleaned_tokens = []

        sentence_tokenize = sent_tokenize(text)

        for sent_token in sentence_tokenize:
                
            new_sen = []

            words_tokenize = word_tokenize(sent_token)
            prasser_tags = pos_tag(words_tokenize)
            
            for token, tag in prasser_tags:
                token = re.sub("[!$%&'()*+,-./:;<=>?@[\]^_`{|} ~0-9]","", token)

                if len(token) != 1:

                    if tag.startswith("NN"):
                        pos = 'n'
                    elif tag.startswith('VB'):
                        pos = 'v'
                    else:
                        pos = 'a'

                    lemmatizer = WordNetLemmatizer()
                    token = lemmatizer.lemmatize(token, pos)
            
                    filtered_word = token.lower()

                    if len(token) > 0 and filtered_word not in self.stop_words:
                        new_sen.append(filtered_word)

            cleaned_tokens.append(' '.join(new_sen))

        whole_reformed_text = [' '.join(cleaned_tokens)]

        return whole_reformed_text
    

    def encode_text(self, text: str):
        '''
        input parameter : [text] => whole single string

        Output value: embeddings of the text in 512 dimensions
        '''

        self.text = text

        self.cleaned_text = self.cleaning_text(text)

        return model.text_vector(self.cleaned_text[0])


#encode = Encoder().encode_text('''Hi! there this is a AI project which aims to create
#a model which will pridict catogarical data that is tags 
#with the input text form''')

#print(encode)
