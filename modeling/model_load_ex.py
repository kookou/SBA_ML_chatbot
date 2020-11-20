from keras.models import load_model
import numpy as np

fname = r'recommender_mf.h5'
model = load_model(fname)
# model.compile(optimizer = 'adam', loss = 'logcosh', metrics=['accuracy'])


predict = model.predict([np.array([777]), np.array([778])])

print(predict[0])

