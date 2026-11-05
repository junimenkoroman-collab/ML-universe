"""Local-only HTTP application; safe JSON API; no internet services required."""
from __future__ import annotations
import argparse,json,webbrowser,threading,time,mimetypes,os,sys
from pathlib import Path
from http.server import BaseHTTPRequestHandler,ThreadingHTTPServer
from urllib.parse import urlparse
from .core.regression import RegressionExperiment,compare
from .core.labs import run_lab

STATIC=Path(__file__).resolve().parent/'static'
MIME={'.js':'application/javascript','.css':'text/css','.html':'text/html','.svg':'image/svg+xml','.png':'image/png','.woff2':'font/woff2'}

class Controller:
    def __init__(self):
        self.lock=threading.RLock();self.experiment=RegressionExperiment()
    def handle(self,path,body):
        with self.lock:
            if path=='/api/import_csv':
                self.experiment=RegressionExperiment(body.get('config',{}),body.get('x'),body.get('y'));return self.experiment.state(with_surface=True)
            if path=='/api/init':
                self.experiment=RegressionExperiment(body or {});return self.experiment.state(with_surface=True)
            if path=='/api/state':return self.experiment.state(with_surface=bool(body.get('surface',False)))
            if path=='/api/step':
                self.experiment.step();return self.experiment.state()
            if path=='/api/run':return self.experiment.run(body.get('steps',40))
            if path=='/api/seek':return self.experiment.seek(body.get('step',0))
            if path=='/api/set':return self.experiment.set_params(body or {})
            if path=='/api/surface':return {'surface':self.experiment.surface()}
            if path=='/api/compare':return compare({**self.experiment.cfg,**body.get('config',{})},body.get('names',['sgd','momentum','rmsprop','adam','adamw']),body.get('steps',90))
            if path=='/api/save':return self.experiment.export()
            if path=='/api/load':
                self.experiment=RegressionExperiment.load(body);return self.experiment.state(with_surface=True)
            if path=='/api/lab':return run_lab(body.get('name','math'),body.get('config',{}))
            if path=='/api/health':return {'ok':True,'version':'0.8.0','offline':True,'platform':sys.platform}
            raise ValueError('Неизвестная операция')

class Handler(BaseHTTPRequestHandler):
    controller=None
    def log_message(self,fmt,*args):
        if os.environ.get('ML_UNIVERSE_DEBUG'):super().log_message(fmt,*args)
    def respond(self,code,payload):
        data=json.dumps(payload,ensure_ascii=False,allow_nan=False).encode('utf-8')
        self.send_response(code);self.send_header('Content-Type','application/json; charset=utf-8');self.send_header('Cache-Control','no-store');self.send_header('X-Content-Type-Options','nosniff');self.send_header('Content-Length',str(len(data)));self.end_headers();self.wfile.write(data)
    def host_is_local(self):
        host=self.headers.get('Host','').split(':',1)[0].lower()
        return host in ('127.0.0.1','localhost')
    def do_POST(self):
        if not self.host_is_local():self.send_error(403);return
        if self.path not in ('/api/import_csv','/api/init','/api/state','/api/step','/api/run','/api/seek','/api/set','/api/surface','/api/compare','/api/save','/api/load','/api/lab','/api/health'):
            self.respond(404,{'error':'Неизвестный endpoint'});return
        if self.headers.get('Content-Type','').split(';')[0].strip()!='application/json':self.respond(415,{'error':'Требуется application/json'});return
        try:
            n=int(self.headers.get('Content-Length','0'))
            if n<0 or n>2_000_000:self.respond(413,{'error':'Слишком большой запрос'});return
            body=json.loads(self.rfile.read(n) or b'{}')
            if not isinstance(body,dict):raise ValueError('JSON-запрос должен быть объектом')
            data=self.controller.handle(urlparse(self.path).path,body)
            self.respond(200,data)
        except Exception as exc:
            self.respond(400,{'error':str(exc),'type':type(exc).__name__})
    def do_GET(self):
        if not self.host_is_local():self.send_error(403);return
        path=urlparse(self.path).path
        if path=='/api/health':self.respond(200,{'ok':True,'version':'0.8.0'});return
        target=(STATIC/('index.html' if path=='/' else path.lstrip('/'))).resolve()
        if not target.is_relative_to(STATIC.resolve()):self.send_error(404);return
        if target.name == 'plotly.min.js' and not target.is_file():
            compressed = Path(str(target) + '.gz')
            if not compressed.is_file():self.send_error(404);return
            import gzip
            data = gzip.decompress(compressed.read_bytes())
        else:
            if not target.is_file():self.send_error(404);return
            data=target.read_bytes()
        self.send_response(200);self.send_header('Content-Type',MIME.get(target.suffix,mimetypes.guess_type(str(target))[0] or 'application/octet-stream'))
        self.send_header('Content-Length',str(len(data)));self.send_header('Cache-Control','public, max-age=3600' if target.name=='plotly.min.js' else 'no-cache');self.end_headers();self.wfile.write(data)

def create_server(port=0):
    controller=Controller()
    class LocalHandler(Handler):pass
    LocalHandler.controller=controller
    return ThreadingHTTPServer(('127.0.0.1',int(port)),LocalHandler)

def main():
    parser=argparse.ArgumentParser(description='ML Universe — offline interactive machine learning laboratory')
    parser.add_argument('--port',type=int,default=0);parser.add_argument('--browser',action='store_true',help='Use external browser instead of native webview')
    parser.add_argument('--no-open',action='store_true',help='Start HTTP server without opening window')
    args=parser.parse_args();httpd=create_server(args.port);url=f'http://127.0.0.1:{httpd.server_port}/'
    runner=threading.Thread(target=httpd.serve_forever,daemon=True);runner.start()
    print(f'ML Universe: {url}',flush=True)
    if not args.no_open:
        if not args.browser:
            try:
                import webview
                webview.create_window('ML Universe — Interactive ML Laboratory',url,width=1500,height=900,min_size=(1100,700),background_color='#212121')
                webview.start(debug=False)
                httpd.shutdown();httpd.server_close();return
            except Exception as exc:
                print(f'Native WebView unavailable; falling back to browser: {exc}',file=sys.stderr,flush=True)
        webbrowser.open(url)
    try:
        while runner.is_alive():time.sleep(.35)
    except KeyboardInterrupt:pass
    finally:httpd.shutdown();httpd.server_close()
if __name__=='__main__':main()
