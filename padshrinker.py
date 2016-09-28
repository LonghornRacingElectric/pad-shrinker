# PadShrinker
# Python Script to modify SVG layer to shrink or grow rectangular pads for 
# use in laser cutting PCB stencils.

# Note that this assumes that the SVG file uses units of 0.0001 inch, or 0.1 mils.
# KiCAD seems to always save SVG files using these units, but other SVG files may
# vary.

import xml.etree.ElementTree as ET

# units: 0.1 mils
shrinkAmount = 20

def processShape(pointStrs):
  
  points = []
  
  for pt in pointStrs:
    point = {'x' : int(pt.split(',')[0]), 'y' : int(pt.split(',')[1])}
    points.append(point)

  xVals = [pt['x'] for pt in points]
  yVals = [pt['y'] for pt in points]

  xMin = min(xVals)
  xMax = max(xVals)
  yMin = min(yVals)
  yMax = max(yVals)

  xMin += shrinkAmount
  xMax -= shrinkAmount
  yMin += shrinkAmount
  yMax -= shrinkAmount

  points = [
    {'x' : xMax, 'y' : yMax},
    {'x' : xMin, 'y' : yMax},
    {'x' : xMin, 'y' : yMin},
    {'x' : xMax, 'y' : yMin},
    {'x' : xMax, 'y' : yMax}
  ]

  outStr = ''
  for pt in points:
    outStr += '{},{} '.format(pt['x'], pt['y'])

  return outStr

tree = ET.parse('test.svg')
root = tree.getroot()

polylines = root.findall('.//{http://www.w3.org/2000/svg}polyline')

print('{} polylines found'.format(len(polylines)))

procCount = 0

for polyline in polylines:
  points = polyline.attrib['points'].strip().split(' ')
  if len(points) != 5:
    print('Skipping a polyline with {} points'.format(len(pointStr) - 1))
    pass
  else:
    newStr = processShape(points)
    polyline.set('points', newStr)
    procCount += 1

print ('{} polylines processed'.format(procCount))

tree.write('out.svg')