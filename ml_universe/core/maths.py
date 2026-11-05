"""Safe mathematical expressions, analytic losses, gradients and activations."""
import ast, math
import numpy as np

FUNCTIONS={k:getattr(np,k) for k in ('sin','cos','tan','exp','log','log1p','sqrt','abs','maximum','minimum','tanh','sinh','cosh','arctan','sign','floor','ceil')}
FUNCTIONS.update(sigmoid=lambda x:1/(1+np.exp(-np.clip(x,-60,60))),relu=lambda x:np.maximum(x,0))
BINARY={ast.Add:lambda a,b:a+b,ast.Sub:lambda a,b:a-b,ast.Mult:lambda a,b:a*b,ast.Div:lambda a,b:a/b,ast.Pow:lambda a,b:a**b,ast.Mod:lambda a,b:a%b}
class UnsafeExpression(ValueError): pass

def safe_evaluate(expr,**variables):
    if not isinstance(expr,str) or len(expr)>300:raise UnsafeExpression('Недопустимая длина выражения')
    try:tree=ast.parse(expr,mode='eval')
    except SyntaxError as e:raise UnsafeExpression('Синтаксическая ошибка') from e
    if len(list(ast.walk(tree)))>80:raise UnsafeExpression('Слишком сложное выражение')
    def walk(n):
        if isinstance(n,ast.Expression):return walk(n.body)
        if isinstance(n,ast.Constant) and type(n.value) in (int,float) and math.isfinite(n.value) and abs(n.value)<1e8:return float(n.value)
        if isinstance(n,ast.Name):
            if n.id in variables:return variables[n.id]
            if n.id=='pi':return np.pi
            if n.id=='e':return np.e
            raise UnsafeExpression(f'Неизвестная переменная {n.id}')
        if isinstance(n,ast.BinOp) and type(n.op) in BINARY:
            if isinstance(n.op,ast.Pow) and isinstance(n.right,ast.Constant) and abs(n.right.value)>12:raise UnsafeExpression('Степень слишком велика')
            return BINARY[type(n.op)](walk(n.left),walk(n.right))
        if isinstance(n,ast.UnaryOp) and isinstance(n.op,(ast.USub,ast.UAdd)):return -walk(n.operand) if isinstance(n.op,ast.USub) else walk(n.operand)
        if isinstance(n,ast.Call) and isinstance(n.func,ast.Name) and n.func.id in FUNCTIONS and not n.keywords and len(n.args) in (1,2):return FUNCTIONS[n.func.id](*(walk(a) for a in n.args))
        raise UnsafeExpression('Небезопасная или неизвестная операция')
    with np.errstate(all='ignore'):out=walk(tree)
    a=np.asarray(out)
    if a.size>400000 or not np.all(np.isfinite(a)):raise UnsafeExpression('Некорректный результат (NaN/Inf)')
    return out

def numerical_gradient(fn,theta,eps=1e-5):
    t=np.asarray(theta,dtype=float);g=np.empty_like(t)
    for j in range(len(t)):
        v=np.zeros_like(t);v[j]=eps*max(1,abs(t[j]));g[j]=(fn(t+v)-fn(t-v))/(2*v[j])
    return g

def numerical_hessian(fn,theta,eps=1e-4):
    t=np.asarray(theta,dtype=float);H=np.empty((len(t),len(t)))
    for j in range(len(t)):
        v=np.zeros_like(t);v[j]=eps*max(1,abs(t[j]));H[:,j]=(numerical_gradient(fn,t+v)-numerical_gradient(fn,t-v))/(2*v[j])
    return (H+H.T)/2

def loss_and_grad(y,p,kind='mse',delta=1.,quantile=.5,weights=None):
    y=np.asarray(y,dtype=float);p=np.asarray(p,dtype=float);r=p-y;n=len(y)
    if n==0:raise ValueError('Пустой датасет')
    if kind=='mse':return float(np.mean(r*r)),2*r/n
    if kind=='sse':return float(np.sum(r*r)),2*r
    if kind=='mae':return float(np.mean(abs(r))),np.sign(r)/n
    if kind=='rmse':v=float(np.sqrt(np.mean(r*r)));return v,r/(n*max(v,1e-12))
    if kind=='huber':d=max(float(delta),1e-9);a=abs(r);return float(np.mean(np.where(a<=d,.5*r*r,d*(a-.5*d)))),np.clip(r,-d,d)/n
    if kind=='logcosh':return float(np.mean(np.logaddexp(r,-r)-np.log(2))),np.tanh(r)/n
    if kind=='quantile':q=np.clip(float(quantile),.001,.999);t=y-p;return float(np.mean(np.maximum(q*t,(q-1)*t))),np.where(t>0,-q,1-q)/n
    if kind=='weighted_mse':
        w=np.ones(n) if weights is None else np.asarray(weights,dtype=float)
        if len(w)!=n or (w<0).any() or w.sum()<=0:raise ValueError('Недопустимые веса наблюдений')
        return float(np.sum(w*r*r)/sum(w)),2*w*r/sum(w)
    raise ValueError('Неизвестная функция потерь')

def regularization(w,kind='none',lam=0.,ratio=.5):
    w=np.asarray(w,dtype=float);lam=max(0.,float(lam));ratio=float(np.clip(ratio,0,1))
    if kind=='none':return 0.,np.zeros_like(w)
    if kind=='l1':return float(lam*sum(abs(w))),lam*np.sign(w)
    if kind=='l2':return float(lam*np.dot(w,w)),2*lam*w
    if kind=='elastic':return float(lam*(ratio*sum(abs(w))+(1-ratio)*np.dot(w,w))),lam*(ratio*np.sign(w)+2*(1-ratio)*w)
    raise ValueError('Неизвестная регуляризация')

def activation(x,name):
    x=np.asarray(x,dtype=float)
    if name=='linear':return x
    if name=='sigmoid':return 1/(1+np.exp(-np.clip(x,-60,60)))
    if name=='tanh':return np.tanh(x)
    if name=='relu':return np.maximum(x,0)
    if name=='leaky_relu':return np.where(x>0,x,.01*x)
    if name=='softplus':return np.logaddexp(0,x)
    if name=='swish':return x*activation(x,'sigmoid')
    if name=='gelu':return .5*x*(1+np.tanh(np.sqrt(2/np.pi)*(x+.044715*x**3)))
    if name=='elu':return np.where(x>0,x,np.expm1(np.clip(x,-100,0)))
    raise ValueError('Неизвестная активация')

def activation_prime(x,name):
    if name=='linear':return np.ones_like(x)
    if name=='sigmoid':s=activation(x,name);return s*(1-s)
    if name=='tanh':return 1-np.tanh(x)**2
    if name=='relu':return (x>0).astype(float)
    if name=='leaky_relu':return np.where(x>0,1.,.01)
    if name=='softplus':return activation(x,'sigmoid')
    if name=='swish':s=activation(x,'sigmoid');return s+x*s*(1-s)
    if name=='elu':return np.where(x>0,1.,np.exp(np.clip(x,-100,0)))
    return numerical_gradient(lambda z:sum(activation(z,name)),x)

BENCHMARKS={
 'sphere':('x² + y²',lambda x,y:x*x+y*y),
 'rosenbrock':('(1−x)² + 100(y−x²)²',lambda x,y:(1-x)**2+100*(y-x*x)**2),
 'himmelblau':('(x²+y−11)² + (x+y²−7)²',lambda x,y:(x*x+y-11)**2+(x+y*y-7)**2),
 'rastrigin':('20+x²+y²−10(cos2πx+cos2πy)',lambda x,y:20+x*x+y*y-10*(np.cos(2*np.pi*x)+np.cos(2*np.pi*y))),
 'saddle':('x²−y²+0.05(x⁴+y⁴)',lambda x,y:x*x-y*y+.05*(x**4+y**4)),
 'anisotropic':('x²+25y²',lambda x,y:x*x+25*y*y)
}
