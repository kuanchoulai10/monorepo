import streamlit as st
import pandas as pd
import numpy as np
from scipy.stats import beta
import matplotlib.pyplot as plt
import seaborn as sns
import time

# prior = st.sidebar.slider("prior", min_value=0., max_value=1., step=0.05)
a = st.sidebar.slider("Alpha", min_value = 0., max_value=20., step=0.1)
b = st.sidebar.slider("Beta", min_value = 0., max_value=20., step=0.1)

st.title("Beta Distribution")

x = np.linspace(0, 1, 100)
y = beta.pdf(x, a, b)
# df = pd.DataFrame({
#     "x": x,
#     "y": y
# })
# plot = sns.displot(data=df, x="x", y="y", kind="kde")
# st.pyplot(plot.fig)

st.text(x)
st.text(y)
fig, ax = plt.subplots()
ax.plot(x, y)
ax.set_xlim(0, 1)
ax.set_ylim(0, 10)
ax.set_title("Beta Distribution")
st.pyplot(fig)