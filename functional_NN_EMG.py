import keras
from keras.models import Model
from keras.layers import Input, Dense, Dropout, Flatten
from keras.layers import Conv2D, MaxPooling2D
from keras.layers import BatchNormalization
from keras.layers import PReLU


def conv_block(input_tensor, num_filters):
    x_parallel = input_tensor
    x_parallel = MaxPooling2D((2, 2), padding='same')(x_parallel)

    x = Conv2D(
                        num_filters,
                        (3, 3),
                        padding='same',
                        )(input_tensor)
    x = BatchNormalization(
                        momentum=0.99,
                        epsilon=0.001,
                        center=True,
                        scale=True,
                        beta_initializer='zeros',
                        gamma_initializer='ones',
                        moving_mean_initializer='zeros',
                        moving_variance_initializer='ones'
                        )(x)
    x = PReLU()(x)
    x = Dropout(0.5)(x)
    x = Conv2D(
                        num_filters,
                        (3, 3),
                        strides=(2, 2),
                        padding='same',
                        )(x)

    x = keras.layers.Add()([x, x_parallel])

    x = BatchNormalization(
                        momentum=0.99,
                        epsilon=0.001,
                        center=True,
                        scale=True,
                        beta_initializer='zeros',
                        gamma_initializer='ones',
                        moving_mean_initializer='zeros',
                        moving_variance_initializer='ones'
                        )(x)
    x = PReLU()(x)

    x = Conv2D(
                        2*num_filters,
                        (3, 3),
                        padding='same',
                        )(x)

    x = BatchNormalization(
                        momentum=0.99,
                        epsilon=0.001,
                        center=True,
                        scale=True,
                        beta_initializer='zeros',
                        gamma_initializer='ones',
                        moving_mean_initializer='zeros',
                        moving_variance_initializer='ones'
                        )(x)
    x = PReLU()(x)

    x = Dropout(0.5)(x)
    x = Conv2D(
                        2*num_filters,
                        (3, 3),
                        padding='same',
                        )(x)
    return x


def define_NN_architecture():
    rms_inputs = Input(shape=(16, ), name='rms_input')
    rms_int = Dense(250,
                    activation='relu')(rms_inputs)
    rms_int = Dropout(0.5)(rms_int)
    RMS_out = BatchNormalization(
                        momentum=0.99,
                        epsilon=0.001,
                        center=True,
                        scale=True,
                        beta_initializer='zeros',
                        gamma_initializer='ones',
                        moving_mean_initializer='zeros',
                        moving_variance_initializer='ones'
                        )(rms_int)

    wavelet_inputs = Input(shape=(248, 16, 1), name='wavelet_input')

    x = Conv2D(
                        32,
                        (3, 4),
                        padding='valid',
                        )(wavelet_inputs)

    x = BatchNormalization(
                        momentum=0.99,
                        epsilon=0.001,
                        center=True,
                        scale=True,
                        beta_initializer='zeros',
                        gamma_initializer='ones',
                        moving_mean_initializer='zeros',
                        moving_variance_initializer='ones'
                        )(x)
    x = PReLU()(x)

    x = conv_block(x, 32)
    x = conv_block(x, 64)
    x = conv_block(x, 128)

    wavelet_out = Flatten()(x)

    combined_inputs = keras.layers.concatenate(
                [RMS_out, wavelet_out]
            )

    x = Dense(120,
              activation='relu'
              )(combined_inputs)

    x = Dropout(0.5)(x)

    predictions = Dense(18,
                        activation='softmax'
                        )(x)

    model = Model(inputs=[wavelet_inputs, rms_inputs],
                  outputs=predictions)
    return model
