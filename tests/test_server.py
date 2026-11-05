import json,threading,urllib.request
from ml_universe.server import create_server

def test_api_end_to_end():
    server=create_server();thread=threading.Thread(target=server.serve_forever,daemon=True);thread.start();base=f'http://127.0.0.1:{server.server_port}'
    def call(path,body):
        data=json.dumps(body).encode();req=urllib.request.Request(base+'/api/'+path,data=data,headers={'Content-Type':'application/json'})
        with urllib.request.urlopen(req,timeout=10) as r:return json.load(r)
    try:
        with urllib.request.urlopen(base+'/') as r:assert b'ML Universe' in r.read()
        s=call('init',{'n':33});assert len(s['x'])==33
        s=call('step',{});assert s['steps']==1
        s=call('run',{'steps':5});assert s['steps']==6
        s=call('seek',{'step':2});assert s['steps']==2
        saved=call('save',{});loaded=call('load',saved);assert loaded['steps']==2
        assert call('lab',{'name':'attention','config':{'text':'a b'}})['stats']['tokens']==2
        assert call('health',{})['ok']
    finally:server.shutdown();server.server_close()

def test_csv_import_and_replay():
    server=create_server();thread=threading.Thread(target=server.serve_forever,daemon=True);thread.start();base=f'http://127.0.0.1:{server.server_port}'
    def call(path,body):
        req=urllib.request.Request(base+'/api/'+path,data=json.dumps(body).encode(),headers={'Content-Type':'application/json'})
        with urllib.request.urlopen(req,timeout=10) as r:return json.load(r)
    try:
        state=call('import_csv',{'x':[0,1,2,3,4],'y':[1,3,5,7,9]})
        assert state['config']['n']==5
        assert len(state['surface']['z'])==52
        before=state['current']['loss']
        state=call('run',{'steps':20})
        assert state['current']['loss']<before
    finally:server.shutdown();server.server_close()


def test_local_plotly_bundle_serves_complete_javascript():
    import threading
    import urllib.request
    from ml_universe.server import create_server

    server = create_server(0)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    try:
        with urllib.request.urlopen(f'http://127.0.0.1:{server.server_port}/plotly.min.js', timeout=20) as response:
            data = response.read()
            assert response.status == 200
            assert response.headers['Content-Type'] == 'application/javascript'
            assert b'plotly.js' in data[:100]
            assert len(data) > 4_000_000
    finally:
        server.shutdown()
        server.server_close()
