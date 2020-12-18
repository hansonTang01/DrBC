from drbcpp.betlearn import BetLearn
from drbcpp.util import fix_random_seed


def main():
    # Instructions to load the model later:
    # import tensorflow as tf
    # from tensorflow.keras.models import load_model
    # load_model('path/to/experiments/<DATE>/models/best.h5py', custom_objects={'tf': tf}, compile=False).summary()

    fix_random_seed(42)
    btl = BetLearn(min_nodes=200, max_nodes=300,
                   nb_train_graphs=100, nb_valid_graphs=100,
                   graphs_per_batch=16, nb_batches=50,
                   node_neighbors_aggregation='gcn',
                   graph_type='powerlaw', optimizer='adam', aggregation='max', combine='gru')
    btl.train(epochs=100)


if __name__ == "__main__":
    main()
