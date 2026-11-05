import numpy as np
import pytest
from ml_universe.core.regression import RegressionExperiment,compare
from ml_universe.core.maths import numerical_gradient

@pytest.mark.parametrize('loss',['mse','sse','rmse','mae','huber','logcosh','quantile'])
def test_model_gradient(loss):
    e=RegressionExperiment({'loss':loss,'regularizer':'l2','lam':.1})
    theta=np.array([1.5,-.5]);actual=e.objective(theta)[3]
    if loss not in ('mae','quantile'):
        numeric=numerical_gradient(lambda t:e.objective(t)[0],theta)
        np.testing.assert_allclose(actual,numeric,atol=1e-6,rtol=1e-5)

def test_reproducibility():
    a=RegressionExperiment();b=RegressionExperiment()
    for i in range(15):a.step();b.step()
    np.testing.assert_allclose(a.theta,b.theta)
    assert a.history[-1]['loss']==b.history[-1]['loss']

def test_seek_replay():
    a=RegressionExperiment()
    for _ in range(15):a.step()
    final=np.copy(a.theta);a.seek(5)
    for _ in range(10):a.step()
    np.testing.assert_allclose(a.theta,final)

def test_serialize_restore():
    a=RegressionExperiment({'optimizer':'adamw','regularizer':'elastic','lam':.01});a.run(9)
    b=RegressionExperiment.load(a.export());np.testing.assert_allclose(a.theta,b.theta)
    a.step();b.step();np.testing.assert_allclose(a.theta,b.theta)

def test_surface_correct():
    e=RegressionExperiment();surface=e.surface(20)
    assert len(surface['z'])==20
    assert float(np.max(surface['z']))>float(np.min(surface['z']))

def test_compare():
    d=compare({},['sgd','momentum','rmsprop','adam','adamw'],15)
    assert len(d['runs'])==5
    assert all(len(r['history'])==16 for r in d['runs'])

def test_gradient_descent_convergence():
    e=RegressionExperiment({'sampling':'full','optimizer':'sgd','lr':.04,'loss':'mse'})
    start=e.history[0]['loss'];e.run(160)
    assert e.history[-1]['loss']<start/50
    assert abs(e.theta[0]-2.7)<.35

@pytest.mark.parametrize('kind',['l1','l2','elastic'])
def test_penalty_carries_to_surface(kind):
    e=RegressionExperiment({'regularizer':kind,'lam':1.});e0=RegressionExperiment({'regularizer':'none'})
    assert e.objective([2.,3.])[0]>e0.objective([2.,3.])[0]
