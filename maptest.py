import matplotlib
matplotlib.use('TkAgg')  # Use TkAgg backend for Matplotlib

import matplotlib.pyplot as plt

# Simple test plot
plt.plot([1, 2, 3, 4], [10, 20, 25, 30])
plt.ylabel('Test Data')
plt.title('Simple Plot Test')

plt.show()  # This will display the plot
