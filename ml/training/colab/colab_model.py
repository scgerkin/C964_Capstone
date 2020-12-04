import tensorflow as tf
from tensorflow.keras.models import Model
from tensorflow.keras.layers import Input, Dense
from tensorflow.keras.applications.densenet import DenseNet201

train_gen = "..."
sample_labels = "..."


def init_model():
    _input = Input(train_gen.image_shape)
    densenet = DenseNet201(include_top=False,
                           weights="imagenet",
                           input_tensor=_input,
                           input_shape=train_gen.image_shape,
                           pooling="avg")

    predictions = Dense(len(sample_labels), activation='sigmoid')(
            densenet.output)

    base = Model(inputs=_input, outputs=predictions)

    optimizer = tf.keras.optimizers.Nadam(learning_rate=0.001)
    base.compile(optimizer=optimizer,
                 loss="categorical_crossentropy",
                 metrics=["accuracy", "mae"])
    return base
