# This Python script was used in our paper "Edge Animation in Software
# Visualization" (Section V "Evaluation") and measures the time needed
# by TinySpline (https://github.com/msteinbeck/tinyspline) to compute
# the different operations of B-Spline morphing (spline alignment and
# the application of a morphism).
#
# In TinySpline, B-Spline morphisms are represented by the "Morphism"
# class. An instance of this class (i.e., a morphism from one spline
# to another) can be set up as follows:
#
#   origin = BSpline(...)
#   target = BSpline(...)
#   morphism = origin.morph_to(target)
#
# Once a morphism is set up, it can be evaluated at interpolation
# parameter `t' (0 <= t <= 1) with:
#
#   spline = morphism.eval(t)
#
# or with the overloaded operator `()':
#
#   spline = morphism(t)
#
# More details on the general usage of TinySpline can be found in our
# paper: "TinySpline: A Small, yet Powerful Library for Interpolating,
# Transforming, and Querying NURBS, B-Splines, and Bézier Curves".


# ====================================================================
# Imports
# ====================================================================
import time # for measuring the time
import pandas as pd # for plotting the results
from tinyspline import * # TinySpline


# ====================================================================
# Set up the origin spline. It will be used in the following steps.
# ====================================================================
origin = BSpline(2, 3, 1)
origin.control_points = [0, 0, 0, 1, 1, 1]


# ====================================================================
# Measure the time needed for setting up a morphism (i.e., the time
# needed to align the origin and target spline).
# ====================================================================
num = []
millis = []
ctrlps = [2, 2, 2,
          3, 3, 3,
          4, 4, 4]
for i in range(4, 1000):
    ctrlps.append(i)
    ctrlps.append(i)
    ctrlps.append(i)
    target = BSpline(i, 3, 3)
    target.control_points = ctrlps

    start = time.time()
    morphism = origin.morph_to(target)
    end = time.time()

    num.append(i)
    millis.append((end - start) * 1000)

# Create scatter plot.
df = pd.DataFrame(data = {'#Control Points': num,
                          'Time in Milliseconds': millis});
plt = df.plot.scatter(x = '#Control Points', y = 'Time in Milliseconds');
plt.figure.savefig('alignment_by_num_ctrlps.pdf')
plt.figure.clf()


# ====================================================================
# Measure the time needed to align the origin spline with a cubic
# spline with 20 control points.
# ====================================================================
millis = []
target = BSpline(20, 3, 3)
target.control_points = ctrlps[0:60] # 20 control points in 3D
for i in range(1000):
    start = time.time()
    morphism = origin.morph_to(target)
    end = time.time()
    millis.append((end - start) * 1000)

# Create boxplot.
df = pd.DataFrame({'Time in Milliseconds': millis})
plt = df.boxplot(grid=False)
plt.figure.savefig('alignment_with_cubic_20.pdf')
print("Average time for alignment: " + str(float(df.median())))
plt.figure.clf()


# ====================================================================
# Measure the time needed for applying the morphism (i.e., the time to
# interpolate between the origin and target spline).
# ====================================================================
millis = []
for i in range(1000):
    morphism = origin.morph_to(target)
    start = time.time()
    morphism(0.5)
    end = time.time()
    millis.append((end - start) * 1000)

# Create boxplot.
df = pd.DataFrame({'Time in Milliseconds': millis})
plt = df.boxplot(grid=False)
print("Average time for applying the morphism: " + str(float(df.median())))
plt.figure.savefig('apply_morphism_20.pdf')
plt.figure.clf()
