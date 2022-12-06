from nltk.corpus import stopwords


stopwords_list = [
    *stopwords.words('english'),
    'propos', 'u', 'allow',
    'also', 'approach', 'ha',
    'one', 'two', 'three',
    'different', 'upper', 'bound',
    'show', 'based', 'propose',
    'describe', 'present', 'paper',
    'demonstrate', 'result', 'ad',
    'hoc', 'better', 'proposed',
    'commonly', 'used', 'et',
    'al', 'different', "'s",
    'address', 'effectiveness', 'recent',
    'user', "'", 'taking',
    'well', 'known', 'take',
    'showed', 'using', 'high'
]
