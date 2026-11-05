"""Optional offline Chromium smoke test; requires playwright + system Chromium.

Uses an in-memory transport instead of a network request to bypass environments
that forbid browser navigation. The real Controller computes each API response.
"""
from __future__ import annotations
import argparse
import gzip
from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parent.parent))
from playwright.sync_api import sync_playwright
from ml_universe.server import Controller

ROOT=Path(__file__).resolve().parent.parent
STATIC=ROOT/'ml_universe'/'static'

def main():
    p=argparse.ArgumentParser()
    p.add_argument('--chromium',default='/usr/bin/chromium')
    p.add_argument('--nav-start',type=int,default=0)
    p.add_argument('--nav-stop',type=int,default=29)
    args=p.parse_args()
    controller=Controller()
    with sync_playwright() as browser_api:
        browser=browser_api.chromium.launch(headless=True,executable_path=args.chromium,args=['--no-sandbox','--disable-gpu','--use-gl=swiftshader'])
        page=browser.new_page(viewport={'width':1512,'height':960})
        errors=[]
        page.on('pageerror',lambda exc:errors.append(str(exc)))
        page.expose_function('python_api',lambda path,body:controller.handle(path,body))
        page.set_content((STATIC/'index.html').read_text(encoding='utf-8'))
        page.add_style_tag(content=(STATIC/'app.css').read_text())
        page.evaluate('''window.fetch=async(url, options)=>{
          try {const body=JSON.parse(options?.body||'{}');
            const result=await window.python_api(url,body);
            return {ok:true,json:async()=>result};
          }catch(e){return {ok:false,json:async()=>({error:String(e)})}}
        };''')
        page.add_script_tag(content=gzip.decompress((STATIC/'plotly.min.js.gz').read_bytes()).decode('utf-8'))
        page.add_script_tag(content=(STATIC/'app.js').read_text(encoding='utf-8'))
        page.wait_for_function("document.querySelectorAll('.js-plotly-plot').length >= 4", timeout=25000)
        # A real browser verifies that the graph toolbar contains only the useful controls.
        page.locator('#plot-0').hover()
        page.wait_for_timeout(150)
        buttons=page.locator('#plot-0 .modebar-btn').evaluate_all('(items)=>items.map(x=>x.getAttribute("data-title"))')
        assert buttons==['Zoom in','Zoom out','Reset axes'],buttons
        assert page.locator('input[type="file"]').count()==0
        assert page.locator('.mode').count()==0
        assert page.locator('#modeBar').count()==0
        assert page.locator('#runMainButton').count()==0
        assert page.locator('#paramsFooter').count()==0
        # Defaults show only the learning essentials; parameters are added explicitly.
        assert page.locator('#parameters .config-field').count()==3
        assert page.locator('#parameters .config-field[data-key="optimizer"]').count()==0
        page.locator('#addModuleButton').click()
        page.locator('.module-choice',has_text='Оптимизатор').click()
        assert page.locator('#parameters .config-field[data-key="optimizer"]').count()==1
        assert page.locator('#parameters .config-field[data-key="beta1"]').count()==0
        page.locator('#parameters select[data-key="optimizer"]').select_option('adam')
        assert page.locator('#parameters .config-field[data-key="beta1"]').count()==1
        assert page.locator('#parameters .config-field[data-key="rho"]').count()==0
        page.locator('.added-module[data-module="optimizer"] .module-remove').click()
        assert page.locator('#parameters .config-field[data-key="optimizer"]').count()==0
        assert page.evaluate('cfg.optimizer')=='sgd'
        page.locator('#addModuleButton').click()
        page.locator('.module-choice',has_text='Регуляризация').click()
        assert page.locator('#parameters .config-field[data-key="lam"]').count()==0
        page.locator('#parameters select[data-key="regularizer"]').select_option('elastic')
        assert page.locator('#parameters .config-field[data-key="lam"]').count()==1
        assert page.locator('#parameters .config-field[data-key="ratio"]').count()==1
        page.locator('.added-module[data-module="regularization"] .module-remove').click()
        assert page.evaluate('cfg.regularizer')=='none'
        page.locator('.nav-item[data-page="classification"]').click()
        assert page.locator('#parameters .config-field').count()==2
        page.locator('#parameters select[data-key="algorithm"]').select_option('knn')
        page.locator('#addModuleButton').click()
        page.locator('.module-choice',has_text='Параметры модели').click()
        assert page.locator('#parameters .config-field[data-key="k"]').count()==1
        assert page.locator('#parameters .config-field[data-key="depth"]').count()==0
        page.locator('.nav-item[data-page="attention"]').click()
        assert page.locator('#parameters .config-field').count()==1
        page.locator('#addModuleButton').click()
        page.locator('.module-choice',has_text='Размерность внимания').click()
        assert page.locator('#parameters .config-field[data-key="d"]').count()==1
        page.locator('.nav-item[data-page="regression"]').click()
        assert page.locator('#parameters .config-field').count()==3
        # Reset removes optional modules while retaining the core laboratory.
        page.locator('#resetButton').click()
        assert page.locator('#parameters .added-module').count()==0
        assert page.locator('#toStep').is_visible()
        assert page.locator('#inspectorPanel').evaluate('(x)=>!x.open')
        page.locator('#toast').evaluate('(x)=>x.classList.remove("show")')
        page.locator('#status-text').hover()
        navs=page.locator('.nav-item').count()
        assert navs==29,navs
        page.screenshot(path=str(ROOT/'docs'/'ui-light.png'),full_page=False)
        page.locator('#themeButton').click()
        page.wait_for_timeout(850)
        page.screenshot(path=str(ROOT/'docs'/'ui-dark.png'),full_page=False)
        assert not page.locator('html').get_attribute('class')
        # Clear user-level theme and run every available lab in real Python.
        failed=[]
        for i in range(args.nav_start,min(navs,args.nav_stop)):
            item=page.locator('.nav-item').nth(i)
            name=item.get_attribute('data-page')
            item.click()
            page.wait_for_timeout(400)
            print(' checked:',i,name,flush=True)
            if page.locator('.chart-card').count()==0 or page.locator('#inspector').inner_text().startswith('Ошибка:'):
                failed.append((name,page.locator('#inspector').inner_text()[:100]))
        assert not failed,failed
        assert not errors,errors
        print(f'OK: {args.nav_start}..{min(navs,args.nav_stop)-1} of {navs} pages, opt-in modules, conditional optimizer fields, both themes, 0 JS exceptions')
        browser.close()

if __name__=='__main__':main()
