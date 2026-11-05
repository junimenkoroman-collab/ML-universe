import pytest
import numpy as np
from ml_universe.core.labs import LABS,run_lab

@pytest.mark.parametrize('name',list(LABS))
def test_labs_return_real_charts(name):
    result=run_lab(name,{})
    assert result['charts']
    assert all(c['traces'] for c in result['charts'])
    assert result['explain']

@pytest.mark.parametrize('name', ['tree','forest','boosting','svm','knn','naive_bayes','logistic','softmax'])
def test_classifiers(name):
    result=run_lab('classification',{'algorithm':name})
    assert result['stats']['accuracy']>.45

@pytest.mark.parametrize('name',['kmeans'])
def test_clustering(name):
    result=run_lab('clustering',{'algorithm':name});assert result['charts']

def test_attention_softmax():
    m=run_lab('attention',{'causal':True,'text':'один два три'})
    a=np.array(m['details']['attention']);np.testing.assert_allclose(a.sum(axis=1),np.ones(3),atol=1e-3)
    assert np.allclose(np.triu(a,1),0.,atol=1e-6)

def test_bpe_actual_merges():
    one=run_lab('bpe',{'merges':0});ten=run_lab('bpe',{'merges':10})
    assert ten['details']['encoded']!=one['details']['encoded']

def test_neural_learns_xor():
    d=run_lab('neural',{'dataset':'xor','lr':.2,'steps':650})
    assert d['stats']['train_accuracy']>.85

