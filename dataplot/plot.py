import matplotlib.pyplot as plt 
import pandas, numpy, time
from matplotlib.backends.backend_pdf import PdfPages

data = pandas.read_csv('data/raw_log.csv')
truth = pandas.read_csv('data/ground-truth.csv')

_min = min(data['time'])
_max = max(data['time'])

m = 21
stepsize = (_max - _min) / m

print('starting calibration')
print('nr of steps set to', m, 'and stepsize set to', stepsize)

buckets = {}
for i in range(0, m):
    _next = _min+stepsize*(i+1)
    _prev = _min+stepsize*(i)
    bucket = data[((data.time > _prev)&(data.time <= _next))]
    mean = numpy.mean(bucket.value)

    start = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(min(bucket.time)))
    end = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(max(bucket.time)))

    buckets.update({'%s-%s'%(start[11:16], end[11:16]):mean})

import math

xs = 2616.9222614840987-1452.0035211267605
ys = 84.4-23.2

print('y/x', ys/xs)

g = lambda x: 0.05253585325722113*(x-1452.0035211267605)+23.2

result = pandas.DataFrame.from_dict({'calculated': [g(buckets[x]) for x in buckets.keys()],'truth': truth['celcius']})

fig, ax = plt.subplots(nrows=1, ncols=2, figsize=(10,4))

ax[0].set_title('Average measurement per time-bucket')
ax[0].bar(list(buckets.keys()), [buckets[x] for x in buckets.keys()])
ax[0].plot(list(buckets.keys()), [buckets[x] for x in buckets.keys()], zorder=1, color='r')
ax[0].set_ylabel('measuremnts [average]')
ax[0].set_xticklabels(list(buckets.keys()), rotation=90)

ax[1].set_title('Groundtruth vs raw measurements')
ax[1].plot([buckets[x] for x in buckets.keys()], truth['celcius'], zorder=2)
ax[1].scatter([buckets[x] for x in buckets.keys()], truth['celcius'], zorder=2)
ax[1].set_ylabel('ground truth [calcius]')
ax[1].set_xlabel('measurements [average]')

plt.tight_layout()

pp = PdfPages('plots/analyze.pdf') 
plt.savefig(pp, format='pdf', bbox_inches="tight") #
pp.close()
plt.close()

print('exported 1')
fig, ax = plt.subplots(nrows=1, ncols=2, figsize=(10,4))

ax[0].set_title('Trendline')
ax[0].plot([buckets[x] for x in buckets.keys()], result['calculated'], linestyle = '--', label='trendline: 0.0525*(x-1452.0035)+23.2', color='r', zorder=1)
ax[0].scatter([buckets[x] for x in buckets.keys()], truth['celcius'], zorder=2)
ax[0].set_ylabel('ground truth [calcius]')
ax[0].set_xlabel('measurements [average]')

l = len(result['calculated'])
ax[1].set_title('Conversion formula curvature')
ax[1].plot(list(range(0,l)), result['calculated'], linestyle = '--', label='converted', color='r', zorder=1)
ax[1].plot(list(range(0,l)), truth['celcius'], linestyle = '--', label='ground-truth', color='b', zorder=1)
ax[1].set_xticks([(i) for i in range(0, 21)]) 
ax[1].set_ylabel('degrees [calcius]')
ax[1].set_xlabel('time [minutes/10]')

plt.tight_layout()
plt.legend()

from matplotlib.backends.backend_pdf import PdfPages

pp = PdfPages('plots/analyze2.pdf') 
plt.savefig(pp, format='pdf', bbox_inches="tight") #
pp.close()
plt.close()

result.to_csv('data/converted.csv')

