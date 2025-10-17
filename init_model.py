import numpy as np
import keras
from keras import Input
from keras.layers import *
from keras import Model

inputs = Input((8, 8, 3))
x = Conv2D(64, (3, 3), padding='same', activation='relu')(inputs)
x = BatchNormalization()(x)
x = Conv2D(64, (3, 3), padding='same', activation='relu')(x)
x = BatchNormalization()(x)
x = Conv2D(64, (3, 3), padding='same', activation='relu')(x)
x = BatchNormalization()(x)

policy_flat = Flatten()(x)
policy_dense = Dense(128, activation='relu')(policy_flat)
policy_output = Dense(65, activation='softmax', name='policyHead')(policy_dense)

value_flat = Flatten()(x)
value_dense = Dense(64, activation='relu')(value_flat)
value_output = Dense(1, activation='tanh', name='valueHead')(value_dense)

model = Model(inputs, [policy_output, value_output])
bce = keras.losses.CategoricalCrossentropy(from_logits=False)
model.compile(optimizer='SGD', loss={'valueHead' : 'mean_squared_error', 'policyHead' : bce})
model.save('init_model.keras')