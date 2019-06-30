def transform_to_pos(text):
    import os
    #os.environ['JAVAHOME'] = java_path
    from nltk.corpus import sentiwordnet as swn
    from nltk.tag.stanford import StanfordPOSTagger
    from nltk import word_tokenize

    path_to_model = "./training/postagging/english-bidirectional-distsim.tagger"
    path_to_jar = "./training/postagging/stanford-postagger.jar"
    tagger=StanfordPOSTagger(path_to_model, path_to_jar)
    tagger.java_options='-mx4096m'          ### Setting higher memory limit for long sentences
    tokens = word_tokenize(text)
    size = len(tokens)
    from collections import Counter
    pos = tagger.tag(tokens)
    counts = Counter( tag for word,  tag in pos)
    for key in counts:
        counts[key]/=size
    counts["totalWordsCount"]=size
    counts[";"]=tokens.count(";")/size
    counts["questionmarks"]=tokens.count("?")/size
    counts["exclamationmarks"]=tokens.count("!")/size
    counts["Quotes"]=tokens.count("\"")/size
    try:
        counts.pop(".")
    except:
        pass
    from collections import OrderedDict
    counts = OrderedDict(counts)
    return counts
