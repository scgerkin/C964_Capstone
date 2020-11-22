#%%
import pandas as pd

epoch_data = pd.read_csv("./logs/20201121230921.csv")

epoch_data.set_index("epoch", inplace=True)
epoch_data.describe()
#%%
print(epoch_data[epoch_data["val_loss"] < 6.34])
