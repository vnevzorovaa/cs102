import csv
import random
import string
import typing as tp
from collections import Counter, defaultdict
from math import log

from db import News, session


class NaiveBayesClassifier:
    def __init__(self, alpha):
        self.alpha = alpha
        self.counters = defaultdict(lambda: defaultdict(int))
        self.words_set = set()
        self.class_counter = defaultdict(int)
        self.words_count = 0

    def fit(self, X, y):
        """Fit Naive Bayes classifier according to X, y."""
        for xi, yi in zip(X, y):
            self.class_counter[yi] += 1
            for word in xi.split():
                self.counters[yi][word] += 1
                self.words_set.add(word)
                self.words_count += 1

    def predict(self, X):
        """Perform classification on an array of test vectors X."""
        predicted = []
        for string in X:
            predicted.append(self._predict_class(string))
        return predicted

    def _predict_class(self, string):
        class_ind = None
        count_of_elements = sum(self.class_counter.values())
        best_val = float("-inf")
        for class_i in self.counters:
            curr_value = log(self.class_counter[class_i] / count_of_elements)
            for word in string.split():
                count_of_curr_word_in_class = self.counters[class_i][word]
                count_of_words_in_curr_class = sum(self.counters[class_i].values())
                curr_value += log(
                    (count_of_curr_word_in_class + self.alpha)
                    / (count_of_words_in_curr_class + self.alpha * len(self.words_set))
                )
            if best_val < curr_value:
                class_ind = class_i
                best_val = curr_value
        if class_ind is None:
            raise Exception("Classifier is not fitted")
        return class_ind

    def score(self, X_test, y_test):
        """Returns the mean accuracy on the given test data and labels."""
        results = self.predict(X_test)
        return sum(y_test[it] == results[it] for it in range(len(y_test))) / len(y_test)


def clean(s):
    translator = str.maketrans("", "", string.punctuation)
    return s.translate(translator)


def label_news():
    s = session()
    x_train = s.query(News.title).filter(News.label != None).all()
    # SELECT news.title FROM news WHERE NOT news.label IS NULL
    y_train = s.query(News.label).filter(News.label != None).all()
    # тут мы выбрали из таблицы тайтлы и лейблы у уже проставленных новостей
    x_train = [clean(str(x)).lower() for x in x_train]
    y_train = [clean(str(y)).lower() for y in y_train]
    print(x_train[0], y_train[0], sep="\n")
    # сделали их стрингами из нижних букв и без лишних символов
    model = NaiveBayesClassifier(1)
    model.fit(x_train, y_train)
    # инициализировали классификатор и обучили на уже отмеченных новостях
    x_label = s.query(News.title).filter(News.label == None).all()
    x_label = [clean(str(xx)).lower() for xx in x_label]
    # достали ТАЙТЛЫ новостей без лейбла и сделали их стрингами
    y_pred = model.predict(x_label)
    # создали лист с проставленными классификатором лейблами
    print(y_pred[0])
    rows = s.query(News).filter(News.label == None).all()
    # SELECT * FROM news WHERE news.label IS NULL
    # достали ряды таблицы без лейлбла целиком
    i = 0
    for row in rows:
        row.label = y_pred[i]
        s.add(row)
        s.commit()
        i += 1
        # проходим по всем рядвмс в выборке без лейбла и устонавливаем им лейбл, забирая его из
        # листа в котором лейблы от классификатора
        # Нам нужно перебирать и элементы rows (а это особый объект sqlalchemy а не лист)
        # поэтому приходится добавить переменную i

if __name__ == "__main__":
    with open("data/SMSSpamCollection") as f:
        data = list(csv.reader(f, delimiter="\t"))
    X, y = [], []
    for target, msg in data:
        X.append(msg)
        y.append(target)
    X = [clean(x).lower() for x in X]
    print(X[0], "|||", y[0])
    X_train, y_train, X_test, y_test = X[:3900], y[:3900], X[3900:], y[3900:]
    model = NaiveBayesClassifier(1)
    model.fit(X_train, y_train)
    print(model.score(X_test, y_test))
