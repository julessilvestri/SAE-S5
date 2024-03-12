import joblib
from datetime import datetime, timedelta

# Pour charger le modèle à partir du fichier plus tard
loaded_model = joblib.load('model.pkl')
# PREDICT

now = datetime.now().timestamp()
interval = timedelta(days=1).total_seconds()

value = ((now + interval) - 1676059200) / (1678604400 - 1676059200) # date courante + 1 jour (normalisé sur le model)

predict = loaded_model.predict([[value],[0.7]])

print(predict)