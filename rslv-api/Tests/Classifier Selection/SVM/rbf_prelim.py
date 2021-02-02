import numpy as np
import matplotlib.pyplot as plt
from sklearn.svm import SVC

x = np.c_[
    #Negative classes
    (.3, -.8),
    (-1.5, -1),
    (-1.3, -.8),
    (-1.1, -1.3),
    (-1.2, -.3),
    (-1.3, -.5),
    (-.6, 1.1),
    (-1.4, 2.2),
    (1, 1),
    #Positive classes
    (1.3, .8),
    (1.2, .5),
    (.2, -2),
    (.5, -2.4),
    (.2, -2.3),
    (0, -2.7),
    (1.3, 2.1)
].T

y = [-1] * 8 + [1] * 8

gamma_option = [1, 2, 4]

plt.figure(1, figsize=(4 * len(gamma_option), 4))
for i, gamma in enumerate(gamma_option, 1):
    svm = SVC(kernel="rbf", gamma=gamma)
    svm.fit(x, y)

    plt.subplot(1, len(gamma_option), i)
    plt.scatter(x[:, 0], x[:, 1], c=y, zorder=10, cmap=plt.cm.Paired)
    plt.axis("tight")

    xx, yy = np.mgrid[-3:3:200j, -3:3:200j]
    z = svm.decision_function(np.c_[xx.ravel(), yy.ravel()])
    z = z.reshape(xx.shape)

    plt.pcolormesh(xx, yy, z > 0, cmap=plt.cm.Paired)
    plt.contour(xx, yy, z, colors=['k', 'k', 'k'], linestyles=['--', '-', '--'], levels=[-.5, 0, .5])
    plt.title('gamma = %d' % gamma)

plt.show()
