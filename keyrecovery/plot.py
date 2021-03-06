#!/usr/bin/env python
import matplotlib.pyplot as plt
import numpy as np
import operator, sys

MAX_MEASUREMENT = 50000

f_raw = open('plot.data', 'rb')
f_csv = open('plot.csv', 'w+')

def filter_value(v):
    if v < 43:
      return 0
    if v >= 43 and v < 50:
      return 1
    if v >= 50 and v < 56:
      return 2
    if v >= 56 and v < 63:
      return 3
    if v >= 63 and v < 70:
      return 4
    if v >= 70 and v < 75:
      return 5
    if v >= 75 and v < 79:
      return 6
    if v >= 79 and v < 84:
      return 7
    if v >= 84:    
      return 8


def export_csv(lst):
  csv = ""
  for n in lst:
#    if n >= 100:
#      csv += 'FF,'
#    else:
    csv += str(n) + ','

  f_csv.write(csv);    
  f_csv.write("\r\n");

sets_m = [] 

for i in xrange(MAX_MEASUREMENT):
  lst = map(ord, list(f_raw.read(64)))
  export_csv(lst)

  for j in xrange(len(lst)):
    if j >=len(sets_m):
      sets_m.append([])

    if int(sys.argv[1]) == 0:
      sets_m[j].append(filter_value(lst[j]))
    else:
      sets_m[j].append(lst[j])

sets_stats = []
for i in xrange(len(sets_m)):
  sets_stats.append({})
  for j in xrange(len(sets_m[i])):
    if sets_m[i][j] == 0 or j < int(sys.argv[2]):
      continue
    if sets_stats[i].has_key(sets_m[i][j]):
      sets_stats[i][sets_m[i][j]] += 1
    else:
      sets_stats[i].update({sets_m[i][j]: 1})

thresholds = []
for k in sets_stats:
  k_sorted = sorted(k.items(), key=operator.itemgetter(1), reverse=True)
  select = 0
  for tu in k_sorted:
    if tu[0] > select and tu[1] > 500:
      select = tu[0]
  thresholds.append(select)


sets_avg = []
for i in xrange(len(sets_m)):
  s = 0
  for j in xrange(len(sets_m[i])):
    s += sets_m[i][j]
  sets_avg.append((s) / MAX_MEASUREMENT)
print sets_avg


'''
  if select >= 80:
    thresholds.append(255) #blind threshold
  else:
    thresholds.append(select)
'''
print thresholds

sets_m_bool = []

for i in xrange(len(sets_m)):
  sets_m_bool.append([])
  for j in xrange(len(sets_m[i])):
    if sets_m[i][j] > thresholds[i]:
      sets_m_bool[i].append(1)
    else:
      sets_m_bool[i].append(0) 

#print sets_mmb

'''
start = 0
for j in xrange(len(set_sum)):
  if set_sum[j] > 60:
    start = j
    break

print start
for j in xrange(len(sets_m)):
  sets_m[j] = sets_m[j][start:]
'''


import matplotlib.pyplot as plt
import numpy as np

print len(sets_m)

fig, ax = plt.subplots()

if int(sys.argv[1]) == 0:
  ax.imshow(sets_m, cmap='Greys', interpolation='nearest')
else:
  ax.imshow(sets_m_bool, cmap='Greys', interpolation='nearest')



ax.set_xlabel('Measurement')
ax.set_ylabel('Set number')

plt.show()


  
f_raw.close()
f_csv.close()
