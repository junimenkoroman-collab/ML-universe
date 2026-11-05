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
        navs=page.locator('.nav-item').count()
        assert navs==29,navs
        page.screenshot(path=str(ROOT/'docs'/'ui-light.png'),full_page=False)
        page.locator('#themeButton').click()
        page.wait_for_timeout(850)
        page.screenshot(path=str(ROOT/'docs'/'ui-dark.png'),full_page=False)
        assert not page.locator('html').get_attribute('class')
        # Clear user-level theme and run every available lab in real Python.
        failed=[]
        for i in range(navs):
            item=page.locator('.nav-item').nth(i)
            name=item.get_attribute('data-page')
            item.click()
            page.wait_for_timeout(650)
            if page.locator('.chart-card').count()==0 or page.locator('#inspector').inner_text().startswith('Ошибка:'):
                failed.append((name,page.locator('#inspector').inner_text()[:100]))
        assert not failed,failed
        assert not errors,errors
        print(f'OK: {navs} pages, both themes, Plotly figures, 0 JS exceptions')
        browser.close()

if __name__=='__main__':main()
