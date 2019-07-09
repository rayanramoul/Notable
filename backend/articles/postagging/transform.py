def transform_to_pos(text):
    import os
    #os.environ['JAVAHOME'] = java_path
    from nltk.corpus import sentiwordnet as swn
    from nltk.tag.stanford import StanfordPOSTagger
    from nltk import word_tokenize

    path_to_model = "./postagging/english-bidirectional-distsim.tagger"
    path_to_jar = "./postagging/stanford-postagger.jar"
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
    ot = ['NNP', 'VBD', 'VBN', 'IN', 'CD', 'VBP', ',', 'DT', 'NN', 'JJ', 'RB', 'TO', 'SYM', 'PRP', 'NNS', 'CC', 'PRP$', 'POS', 'FW', 'VBG', ':', 'WRB', 'EX', 'JJR', 'WDT', 'totalWordsCount', ';', 'questionmarks', 'exclamationmarks', 'Quotes']
    counts = OrderedDict(counts)
    for key in ot:
        if key in counts:
            pass
        else:
            counts[key] = 0
    tmp = counts.copy()
    for key in tmp:
        if key not in ot:
            counts.pop(key, None)
    dab = {}
    for i in ot:
        dab[i]=counts[i]
    counts = dab.copy()
    return counts
