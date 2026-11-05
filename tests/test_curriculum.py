"""Contract tests for the intentionally small ML -> DL -> NLP curriculum."""
import numpy as np
import pytest
from ml_universe.core.labs import LABS,run_lab
from ml_universe.core.maths import loss_and_grad,numerical_gradient
from ml_universe.core.regression import RegressionExperiment

PRUNED={'pca','statistics','validation','scaling','ranking','recommendations','graph','causal','fairness','interpretability','diffusion','anomaly','leakage','timeseries','probability','rl'}
FOCUSED={'losses','regularization_path','sweep','activation','neural_dynamics','rnn','embeddings','text_classification','multihead','rag','bandits','clustering','math','algebra','norms','information','schedulers','classification','neural','neuron','cnn','bpe','nlp','attention','decoding','optimizer_gallery'}

def test_curriculum_only():
    assert FOCUSED==set(LABS)
    assert not PRUNED.intersection(LABS)

@pytest.mark.parametrize('kind', ['mse','sse','rmse','mae','huber','smooth_l1','logcosh','quantile','weighted_mse'])
def test_loss_gradients_against_finite_difference(kind):
    y=np.array([-1.,.2,2.]); p=np.array([.1,1.4,3.3]);weights=np.array([1.,2.,3.]);delta=.8
    def f(q):return loss_and_grad(y,q,kind,delta,.4,weights)[0]
    analytic=loss_and_grad(y,p,kind,delta,.4,weights)[1]
    np.testing.assert_allclose(analytic,numerical_gradient(f,p),atol=1e-5)

def test_smooth_l1_transition():
    loss,grad=loss_and_grad([0,0],[.5,2],'smooth_l1',1.)
    assert loss==pytest.approx((.125+1.5)/2)
    np.testing.assert_allclose(grad,[.25,.5])

def test_weighted_mse_regression_changes_objective():
    a=RegressionExperiment({'loss':'weighted_mse','weight_mode':'uniform'})
    b=RegressionExperiment({'loss':'weighted_mse','weight_mode':'edge'})
    assert a.history[0]['loss']!=pytest.approx(b.history[0]['loss'])

def test_regression_compatible_smooth_l1():
    s=RegressionExperiment({'loss':'smooth_l1','delta':1.3,'optimizer':'adamw'})
    s.run(12)
    assert s.step_count==12
    assert np.isfinite(s.history[-1]['loss'])

def test_regularization_paths():
    for kind in ('ridge','lasso','elastic'):
        d=run_lab('regularization_path',{'kind':kind})
        assert len(d['details']['alpha'])==34
        assert len(d['details']['coefficients'])==34

def test_sweep_grid():
    d=run_lab('sweep',{'steps':20})
    assert len(d['table'])==25
    assert len(d['charts'][0]['traces'][0]['z'])==5

def test_rnn_state_shape_and_determinism():
    a=run_lab('rnn',{'text':'кот кот собака','hidden':5})
    b=run_lab('rnn',{'text':'кот кот собака','hidden':5})
    assert a['details']['hidden_states']==b['details']['hidden_states']
    assert np.asarray(a['details']['hidden_states']).shape==(3,5)

def test_dropout_keep_equals_one():
    d=run_lab('neural_dynamics',{'keep':1})
    assert d['stats']['dropout_rate']==0

def test_embedding_ppmi_finite():
    d=run_lab('embeddings',{})
    array=np.asarray(d['charts'][0]['traces'][0]['z'])
    assert np.isfinite(array).all() and (array>=0).all()

def test_multinomial_text_classifier():
    d=run_lab('text_classification',{'text':'тренер футбол команда'})
    assert d['stats']['prediction']=='спорт'
    assert np.sum(d['charts'][0]['traces'][0]['y'])==pytest.approx(1.)

def test_multihead_attention_causal_mask():
    d=run_lab('multihead',{'text':'a b c d','causal':True,'heads':4})
    for att in d['details']['attention_matrices']:
        a=np.asarray(att)
        np.testing.assert_allclose(a.sum(axis=1),np.ones(4),atol=2e-4)
        assert np.max(abs(np.triu(a,1)))<1e-7

def test_rag_retrieval_not_fake_generation():
    d=run_lab('rag',{'documents':'кот ест рыбу|оптимизатор adam обновляет веса|птица летит','query':'adam обновляет','top_k':1})
    assert d['table'][0]['document']==2
    assert len(d['table'])==1
    assert 'генерация' in d['explain'].lower()

def test_bandit_reproducibility_epsilon():
    a=run_lab('bandits',{'seed':18,'steps':100,'epsilon':0})
    b=run_lab('bandits',{'seed':18,'steps':100,'epsilon':0})
    assert a['stats']==b['stats']
    assert sum(r['pulls'] for r in a['table'])==100
    assert a['stats']['pseudo_regret']>=0

def test_neural_gradient_check_real():
    d=run_lab('neural',{'steps':10})
    check=d['details']['gradient_check_w1_00']
    assert check['abs_diff']<1e-5

def test_softmax_is_multiclass():
    d=run_lab('classification',{'algorithm':'softmax'})
    assert d['stats']['classes']==3
    assert d['stats']['macro_f1']>=.6

def test_roc_pr_both_present():
    d=run_lab('classification',{'algorithm':'logistic'})
    titles=[c['title'] for c in d['charts']]
    assert any('ROC' in t for t in titles)
    assert any('Precision–Recall' in t for t in titles)

def test_projected_gd_stays_inside_ball_after_first_step():
    d=run_lab('optimizer_gallery',{'function':'sphere','optimizers':['projected'],'x0':2,'y0':2,'steps':10,'radius':1.})
    trace=d['charts'][0]['traces'][1]
    for a,b in list(zip(trace['x'],trace['y']))[1:]:
        assert np.hypot(a,b)<=1.000001

def test_greedy_sampling():
    a=run_lab('decoding',{'strategy':'greedy','seed':7})
    b=run_lab('decoding',{'strategy':'greedy','seed':22})
    assert a['stats']['sampled_token']==b['stats']['sampled_token']

def test_hessian_two_dimensional():
    d=run_lab('math',{'dimension':'2d','expression':'x*x+3*y*y','at':1})
    np.testing.assert_allclose(d['details']['hessian'],[[2,0],[0,6]],atol=1e-3)
