from gensim.models import word2vec

model = word2vec.Word2Vec.load("NaverMovie.model")

print(model.most_similar(positive=["짜장면"]))

print(model.most_similar(positive=["최고"]))