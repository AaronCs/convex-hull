#Johnny Li and Aaron Chan
#11-1-2018
#CS 350 Project

#http://adultstudylife.blogspot.com/2016/06/quick-hull-in-python.html
import matplotlib
matplotlib.use('TkAgg')
import numpy
import pylab


def qhull(sample):
    link = lambda a, b: numpy.concatenate((a, b[1:]))
    edge = lambda a, b: numpy.concatenate(([a], [b]))

    def dome(sample, base):
        h, t = base
        dists = numpy.dot(sample - h, numpy.dot(((0, -1), (1, 0)), (t - h)))
        outer = numpy.repeat(sample, dists > 0, axis=0)

        if len(outer):
            pivot = sample[numpy.argmax(dists)]
            return link(dome(outer, edge(h, pivot)),
                        dome(outer, edge(pivot, t)))
        else:
            return base

    if len(sample) > 2:
        axis = sample[:, 0]
        base = numpy.take(sample, [numpy.argmin(axis), numpy.argmax(axis)], axis=0)
        return link(dome(sample, base),
                    dome(sample, base[::-1]))
    else:
        return sample


