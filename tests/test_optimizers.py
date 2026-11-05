import numpy as np
import pytest
from ml_universe.core.optimizers import update,scheduler_lr,SUPPORTED

@pytest.mark.parametrize('name',SUPPORTED)
def test_every_optimizer_decreases_quadratic_locally(name):
    theta=np.array([2.,-1.]);state={}
    losses=[]
    for i in range(70):
        theta,state,details=update(theta,2*theta,state,name=name,lr=.06)
        losses.append(float(theta@theta))
        assert len(theta)==2 and 'gradient_norm' in details
    assert losses[-1]<5.0

def test_sgd_exact():
    p,s,info=update([1.,-2.],[3.,-4.],{},'sgd',lr=.1)
    np.testing.assert_allclose(p,[.7,-1.6]);np.testing.assert_allclose(info['update'],[-.3,.4])

def test_adam_first_step():
    p,s,d=update([2.,3.],[.4,-.2],{},'adam',lr=.1)
    np.testing.assert_allclose(d['m_hat'],[.4,-.2],atol=1e-12)
    np.testing.assert_allclose(d['v_hat'],[.16,.04],atol=1e-12)
    np.testing.assert_allclose(p,[1.9,3.1],atol=1e-7)

def test_adamw_decoupled():
    p,s,d=update([2.,3.],[.4,-.2],{},'adamw',lr=.1,decay=.05)
    np.testing.assert_allclose(p,[1.89,3.085],atol=1e-7)
    np.testing.assert_allclose(d['decoupled_decay'],[-.01,-.015])

def test_momentum_exact():
    p,s,_=update([1.,1.],[1.,2.],{},'momentum',lr=.1)
    p,s,_=update(p,[1.,2.],s,'momentum',lr=.1,momentum=.9)
    np.testing.assert_allclose(s['velocity'],[-.19,-.38])

@pytest.mark.parametrize('name',['constant','cosine','step','warmup_cosine','cyclic','inverse','polynomial','exponential'])
def test_schedulers(name):
    assert np.isfinite(scheduler_lr(10,.1,name))
