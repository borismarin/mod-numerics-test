from neuron import h
from itertools import product


def template(mech, cvode=True):
    cvodes = 1 if cvode else 0
    return '''
create soma_%(suffix)s
access soma_%(suffix)s
insert hh_%(suffix)s

objref iclamp
iclamp = new IClamp(.5)
iclamp.del = 200
iclamp.dur = 100
iclamp.amp = 10


dt = 0.05
tstop = 500
finitialize(-65)
cvode_active(%(cvode)s)

objref tvec, vvec, mvec
tvec = new Vector()
vvec = new Vector()
mvec = new Vector()
vvec.record(&soma_%(suffix)s.v(0.5))
mvec.record(&soma_%(suffix)s.m_hh_%(suffix)s(0.5))
tvec.record(&t)

run()

objref TV
TV = new Matrix()
TV.resize(tvec.size(),3)
TV.setcol(0, tvec)
TV.setcol(1, vvec)
TV.setcol(2, mvec)

objref dump
dump = new File()
dump.wopen("/tmp/hh_%(suffix)s_cvode%(cvode)s.dat")
TV.fprint(dump, " %%g")
dump.close()
''' % {'suffix': mech, 'cvode': cvodes}


for m in product(['cnexp', 'derivimplicit'], ['rates', 'inline']):
    n = '_'.join(m)
    h(template(n, cvode=True))
    h(template(n, cvode=False))
