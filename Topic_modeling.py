from gensim.models.nmf import Nmf
from sklearn.decomposition import LatentDirichletAllocation
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from sklearn.model_selection import GridSearchCV
from matplotlib import pyplot as plt
from wordcloud import WordCloud

import matplotlib.colors as mcolors
import gensim
import gensim.corpora as corpora
import pyLDAvis.gensim_models
import pyLDAvis.sklearn

pyLDAvis.enable_notebook()


class TopicModeling:
    def __init__(self, csv_path, n_components=None, learning_decay=None, max_iter=None):

        self.documents = []
        with open(csv_path, "r", encoding="utf8") as file:
            for row in file:
                self.documents.append(row)
        file.close()

        data_words = [doc.split() for doc in self.documents]

        self.id2word = corpora.Dictionary(data_words)
        self.corpus = [self.id2word.doc2bow(text) for text in data_words]

        self.n_components, self.learning_decay, self.max_iter = n_components, learning_decay, max_iter

        self.tf, self.tf_feature_names, self.tf_vector = self.count_vec()
        self.tfidf, self.idf_feature_names, self.tfidf_vector = self.tfidf_vec()

        self.best_values = self.cross_validation(self.n_components, self.learning_decay, self.max_iter)

    def count_vec(self):  # TODO: aggiungere la possibilità di scegliere i parametri del vectorizer?
        make_vector = CountVectorizer(max_df=0.70,
                                      min_df=0.10,
                                      stop_words='english')
        term_freq = make_vector.fit_transform(self.documents)
        term_freq_features_names = make_vector.get_feature_names()
        return term_freq, term_freq_features_names, make_vector

    def tfidf_vec(self):  # TODO: aggiungere la possibilità di scegliere i parametri del vectorizer?
        make_vector = TfidfVectorizer(max_df=0.70,
                                      min_df=0.10,
                                      stop_words='english')
        tfidf_freq = make_vector.fit_transform(self.documents)
        tfidf_freq_features_names = make_vector.get_feature_names()
        return tfidf_freq, tfidf_freq_features_names, make_vector

    def cross_validation(self, n_components=None, learning_decay=None, max_iter=None):
        if learning_decay is None:
            learning_decay = [.5, .7, .9]
        if n_components is None:
            n_components = [n_topic for n_topic in range(5, 20)]
        if max_iter is None:
            max_iter = [iterations for iterations in range(1, 10)]  # numeri alti inficiano sul carico computazionale

        lda = LatentDirichletAllocation()

        search_params = {'n_components': n_components,
                         'learning_decay': learning_decay,
                         'max_iter': max_iter}

        model = GridSearchCV(lda, param_grid=search_params)
        model.fit(self.tf)

        best_model = model.best_estimator_

        # Log Likelihood Score
        print("Log Likelihood Score: ", model.best_score_)

        # Perplexity
        print("Model Perplexity: ", best_model.perplexity(self.tf))

        # print(model.best_params_)  # check best params

        return model.best_params_

    ############ fino a qui coomenta leo
    def lda_model(self):
        lda = gensim.models.ldamodel.LdaModel(corpus=self.corpus,
                                              id2word=self.id2word,
                                              num_topics=self.best_values['n_components'],
                                              decay=self.best_values['learning_decay'],
                                              iterations=self.best_values['max_iter'],
                                              random_state=100,
                                              update_every=1,
                                              chunksize=100,
                                              passes=10,
                                              alpha="auto")

        # TODO: aggiungere un print dei topics

        site = pyLDAvis.gensim_models.prepare(lda, self.corpus, lda.id2word)
        pyLDAvis.save_html(site, "link_grafici/LDATopicModeling.html")

        return self.make_graphs(lda)

    def nmf_model(self):
        nmf = Nmf(corpus=self.corpus,
                  id2word=self.id2word,
                  num_topics=self.best_values['n_components'],
                  random_state=100,
                  chunksize=100,
                  passes=10)

        # TODO: aggiungere un print dei topics
        return self.make_graphs(nmf)

    def make_graphs(self, model):
        cols = [color for name, color in mcolors.TABLEAU_COLORS.items()]  # more colors: 'mcolors.XKCD_COLORS'

        cloud = WordCloud(background_color='white',
                          width=2500,
                          height=1800,
                          max_words=10,
                          colormap='tab10',
                          color_func=lambda *args, **kwargs: cols[i],
                          prefer_horizontal=1.0)

        topics = model.show_topics(formatted=False)

        n_col = 1
        if self.best_values['n_components'] % 2 == 0:
            n_col = 2

        fig, axes = plt.subplots(self.best_values['n_components'] // n_col, n_col, figsize=(10, 10))

        for i, ax in enumerate(axes.flatten()):
            fig.add_subplot(ax)
            topic_words = dict(topics[i][1])
            cloud.generate_from_frequencies(topic_words, max_font_size=300)
            plt.gca().imshow(cloud)
            plt.gca().set_title('Topic ' + str(i + 1), fontdict=dict(size=16))
            plt.gca().axis('off')

        plt.subplots_adjust(wspace=0, hspace=0)
        plt.axis('off')
        plt.margins(x=0, y=0)
        plt.tight_layout()
        plt.show()


if __name__ == "__main__":
    test = TopicModeling("Deposito_contratti/cleaned_dataset_lemma.csv",
                         n_components=[6],
                         learning_decay=[.75],
                         max_iter=[2])

    test.lda_model()
    test.nmf_model()
