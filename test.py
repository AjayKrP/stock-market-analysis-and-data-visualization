'''
    This module is only for testing purpose
'''

import plotly.plotly as plt
plt.sign_in('AjayKrP', 'pXVNFLoF2HykO9QYuWIN')
import plotly.graph_objs as go
# Create random data with numpy
import numpy as np

N = 500
random_x = np.linspace(0, 1, N)
random_y = np.random.randn(N)

# Create a trace
trace = go.Scatter(
    x = random_x,
    y = random_y
)
data = [trace]
plt.plot(data, filename='basic-line', auto_open=True)

