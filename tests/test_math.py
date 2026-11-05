import numpy as np
import pytest
from ml_universe.core.maths import safe_evaluate,UnsafeExpression,numerical_gradient,loss_and_grad,regularization

@pytest.mark.parametrize('expr',['__import__("os")','x.__class__','[x][0]','(lambda x: x)(2)','open("file")','x if x>0 else 0'])
def test_parser_blocks_code(expr):
    with pytest.raises(UnsafeExpression):safe_evaluate(expr,x=2.)

def test_safe_math():
    x=np.array([1.,2.]);np.testing.assert_allclose(safe_evaluate('sin(x)+x**2',x=x),np.sin(x)+x*x)

def test_mse_derivative():
    y=np.array([1.,3.,-1.]);p=np.array([2.,2.,0.]);loss,dp=loss_and_grad(y,p,'mse');assert loss==pytest.approx(1.)
    numerical=numerical_gradient(lambda q:loss_and_grad(y,q,'mse')[0],p)
    np.testing.assert_allclose(dp,numerical,atol=1e-8)

@pytest.mark.parametrize('kind',['mse','sse','rmse','mae','huber','logcosh','quantile','weighted_mse'])
def test_all_losses_finite(kind):
    y=np.array([1.,2.,5.]);pred=np.array([.4,2.4,4.]);loss,der=loss_and_grad(y,pred,kind)
    assert np.isfinite(loss) and np.all(np.isfinite(der))
    if kind not in ('mae','quantile'):
        np.testing.assert_allclose(der,numerical_gradient(lambda v:loss_and_grad(y,v,kind)[0],pred),rtol=1e-3,atol=1e-5)

@pytest.mark.parametrize('kind',['l1','l2','elastic','none'])
def test_regularizer(kind):
    w=np.array([-.9,.5]);p,g=regularization(w,kind,.4,.2)
    np.testing.assert_allclose(g,numerical_gradient(lambda q:regularization(q,kind,.4,.2)[0],w),atol=1e-7)
    assert p>=0
