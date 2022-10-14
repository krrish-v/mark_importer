
from models.parser import Parse
from models.embd import Encoder
from models.clustering_model import Model

parse = Parse() # parse the text for the link
encode = Encoder() # vectorizing the text to vector
model = Model() # pridicting a tags

def Load_tags(link):
    get_text = parse.parse_text(link)
    if get_text is not None:
        get_vector = encode.encode_text(get_text)
        get_tag = model.get_topic(get_vector)

        return get_tag

    else: return False


# Demonstration

#print(Load_tags('https://towardsdatascience.com/principal-component-analysis-pca-with-scikit-learn-1e84a0c731b0'))
# >>> [['Data', 'Science', 'Machine', 'Learning']]
