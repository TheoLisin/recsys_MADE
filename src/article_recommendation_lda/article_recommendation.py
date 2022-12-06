import os
import pickle

from gensim.models import LdaModel
from gensim.similarities.docsim import MatrixSimilarity


class ArticleRecommendation:
    def __init__(self, model_path):
        self.model_path = model_path

        self._id_to_internal_id = None
        self._internal_id_to_id = None
        self._lda_model = None
        self._matrix_similarity = None
        self._bow_corpus = None
        self._corpus_tfidf = None

        self._load_objects()

    def _load_objects(self):
        self._id_to_internal_id = self._load_pickle(
            os.path.join(self.model_path, 'id_to_internal_id.pkl')
        )

        self._internal_id_to_id = self._load_pickle(
            os.path.join(self.model_path, 'internal_id_to_id.pkl')
        )

        self._lda_model = LdaModel.load(
            os.path.join(self.model_path, 'model.lda')
        )

        self._matrix_similarity = MatrixSimilarity.load(
            os.path.join(self.model_path, 'matrix_similarity')
        )

        self._bow_corpus = self._load_pickle(
            os.path.join(self.model_path, 'bow_corpus.pkl')
        )

    def _load_pickle(self, path):
        with open(path, 'rb') as file:
            obj = pickle.load(file)
        return obj

    def get_recommendations(self, external_id, count=10, skip=0, keep_source=False):
        source_internal_id = self._id_to_internal_id[external_id]
        article_vector = self._lda_model[self._bow_corpus[source_internal_id]]
        sims = self._matrix_similarity[article_vector]
        sims = sorted(enumerate(sims), key=lambda item: -1 * item[1])

        internal_ids = [x[1][0] for x in sims[skip:skip + count]]
        if not keep_source:
            internal_ids = [x for x in internal_ids if x != source_internal_id]

        return [self._internal_id_to_id[x] for x in internal_ids]

