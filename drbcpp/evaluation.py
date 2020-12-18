import numpy as np
from tensorflow.keras.callbacks import Callback

from drbcython import metrics


class EvaluateCallback(Callback):
    def __init__(self, data_generator, prepend_str: str = 'val_'):
        super().__init__()
        self.data_generator = data_generator
        self.prepend_str = prepend_str
        self.metrics = metrics.py_Metrics()
        self._supports_tf_logs = True

    def evaluate(self):
        epoch_logs = {
            f'{self.prepend_str}top0.01': [],
            f'{self.prepend_str}top0.05': [],
            f'{self.prepend_str}top0.1': [],
            f'{self.prepend_str}kendal': [],
        }
        for gid, (x, y, idx_map) in enumerate(self.data_generator):
            result = self.model.predict_on_batch(x=x).flatten()
            betw_predict = [np.power(10, -pred_betweenness) if idx_map[i] >= 0 else 0
                            for i, pred_betweenness in enumerate(result)]

            betw_label = self.data_generator.betweenness[gid]
            epoch_logs[f'{self.prepend_str}top0.01'].append(self.metrics.RankTopK(betw_label, betw_predict, 0.01))
            epoch_logs[f'{self.prepend_str}top0.05'].append(self.metrics.RankTopK(betw_label, betw_predict, 0.05))
            epoch_logs[f'{self.prepend_str}top0.1'].append(self.metrics.RankTopK(betw_label, betw_predict, 0.1))
            epoch_logs[f'{self.prepend_str}kendal'].append(self.metrics.RankKendal(betw_label, betw_predict))
        return {k: np.mean(val) for k, val in epoch_logs.items()}

    def on_epoch_end(self, epoch, logs=None):
        super().on_epoch_end(epoch, logs)
        logs = logs or {}
        logs.update(self.evaluate())
