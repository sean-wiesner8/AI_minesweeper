from keras.models import Model
from keras.layers import Input, Multiply
from keras.layers.convolutional import Conv2D

board_size = 22
channel_size = 11

# 11 channels, and 22x22 board
inputShape = (channel_size, board_size, board_size)

in1 = Input(shape=inputShape)
in2 = Input(shape=(1, board_size, board_size))

in1 = Input(shape=inputShape)
in2 = Input(shape=(1, board_size, board_size))
conv = Conv2D(75, (4, 4), padding='same', data_format='channels_first',
              activation='relu', use_bias=True)(in1)
conv = Conv2D(75, (4, 4), padding='same', data_format='channels_first',
              activation='relu', use_bias=True)(conv)
conv = Conv2D(75, (4, 4), padding='same', data_format='channels_first',
              activation='relu', use_bias=True)(conv)
conv = Conv2D(75, (4, 4), padding='same', data_format='channels_first',
              activation='relu', use_bias=True)(conv)
conv = Conv2D(1, (1, 1), padding='same', data_format='channels_first',
              activation='softsign', use_bias=True)(conv)
out = Multiply()([conv, in2])
model = Model(inputs=[in1, in2], outputs=out)
model.compile(loss='binary_crossentropy', optimizer='adam')
