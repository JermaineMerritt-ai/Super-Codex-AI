# engines/oracle.py
import numpy as np
from sklearn.linear_model import LinearRegression

class ORACLE:
    def foresight(self, series: list[float], horizon: int = 6) -> dict:
        # Simple trend forecast as placeholder; swap for transformers if desired
        X = np.arange(len(series)).reshape(-1,1)
        y = np.array(series)
        model = LinearRegression().fit(X, y)
        future_X = np.arange(len(series), len(series)+horizon).reshape(-1,1)
        preds = model.predict(future_X).tolist()
        return {"trend": "up" if preds[-1] > y[-1] else "down", "forecast": preds}