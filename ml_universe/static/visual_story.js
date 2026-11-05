/* ML Universe visual language v0.9 — charts are explanations, not dashboard widgets. */
(function () {
  'use strict';
  const $ = (selector, scope = document) => scope.querySelector(selector);
  const palette = {
    teaching: '#148579', model: '#C38249', secondary: '#637EAF', caution: '#BD6971',
    classes: ['#268B88', '#CA8451', '#8068AE', '#D0AA48', '#6596BD', '#B46A89', '#708B68', '#946F57'],
    sequential: [[0, '#f0f6f5'], [.25, '#c2dcd8'], [.55, '#75aca4'], [1, '#236a63']],
    sequentialDark: [[0, '#203331'], [.25, '#355a55'], [.55, '#5d938a'], [1, '#b1d7cc']],
    divergent: [[0, '#5e86ae'], [.5, '#f1f1ed'], [1, '#c27d63']]
  };
  // The brief answers *why* a learner should look at each visualization.
  const lessons = {
    regression: ['Почему предсказание ошибается?', 'Сначала сопоставь точки с линией модели. Затем исследуй, как изменение весов уменьшает функцию потерь.', ['Смотри на расстояние от точек до линии: это остаточные ошибки.', 'Минимум функции потерь находится в области с более низким значением цвета или высоты.', 'Кривая показывает, уменьшилась ли ошибка после каждого шага.']],
    losses: ['Почему разные ошибки дают разные градиенты?', 'Сравни, насколько сильно каждая функция штрафует большой остаток. Производная определяет направление обучения.', ['Дальше от нуля — сильнее штраф, но форма кривой зависит от выбранной функции.', 'Наклон функции определяет величину градиента.']],
    regularization_path: ['Как штраф меняет веса модели?', 'Увеличивай α и следи за коэффициентами. L1 может обнулять признаки, L2 обычно плавно уменьшает их вклад.', ['Следи, какие коэффициенты стремятся к нулю быстрее других.', 'Число ненулевых коэффициентов показывает разреженность модели.']],
    optimizer_gallery: ['Почему оптимизаторы приходят к минимуму по-разному?', 'Все алгоритмы стартуют из одной точки; сравни их траектории и фактическую скорость уменьшения ошибки.', ['На контурной карте видно, где алгоритм колеблется или меняет направление.', 'Сравни падение ошибки по шагам, а не только конечный результат.', 'Трёхмерный вид помогает увидеть высоту функции потерь.']],
    schedulers: ['Что происходит с шагом обучения?', 'Проследи, когда learning rate уменьшается и как это влияет на крупные и мелкие шаги.', ['В начале шага может быть больше, к концу — меньше.']],
    sweep: ['Какие гиперпараметры работают лучше на этой задаче?', 'Каждая клетка — отдельный запуск. Сравни результат при одинаковом бюджете обучения.', ['Сопоставляй клетки по цвету: он обозначает итоговое значение ошибки.']],
    classification: ['Где проходит граница между классами?', 'Области цвета — предсказание модели, точки — реальные объекты. Ошибки видны там, где точка оказывается «не в своей» области.', ['Сравни расположение точек с фоном вероятностей или решающей областью.', 'Матрица ошибок показывает правильные и неправильные ответы.', 'ROC и PR показывают качество при разных порогах.']],
    trees: ['Почему дерево выбрало именно это разбиение?', 'Следи за разделением пространства и качеством кандидатов split.', ['Граница каждого разбиения должна объясняться набором точек.', 'Больший выигрыш соответствует лучшему кандидату на этом узле.']],
    ensembles: ['Почему несколько деревьев лучше одного?', 'Сравни границы решений и ошибки ансамбля с результатом отдельной модели.', ['Смотри, какие участки пространства модель различает.', 'Матрица ошибок показывает типы промахов.']],
    clustering: ['Как центроиды находят группы точек?', 'Следи за положением центров и изменением состава кластеров.', ['Каждый цвет — полученный кластер; крестики показывают его центр.', 'Размеры кластеров помогут заметить неравномерность.', 'Уменьшение inertia показывает улучшение внутри кластеров.']],
    neuron: ['Как один нейрон преобразует вход?', 'Изменяй веса и смотри на точку активации; каждый вклад можно проверить численно.', ['Отмеченная точка — результат именно текущих входов и весов.', 'Столбики показывают вклад каждого входа в сумму.']],
    activation: ['Как активация меняет сигнал и градиент?', 'Сравни значение функции с её производной; некоторые функции почти гасят градиенты.', ['Кривая показывает выход нейрона для каждого z.', 'Производная говорит, насколько чувствителен выход к изменению входа.']],
    neural: ['Как MLP учится разделять нелинейные классы?', 'На поле решений видны предсказания сети, а кривая loss показывает реальное обучение.', ['Одинаковые по классу точки должны оказаться в одной области.', 'Проверь, уменьшается ли ошибка по эпохам.']],
    neural_dynamics: ['Почему градиенты исчезают или взрываются?', 'Сравни масштабы активаций и градиентов по глубине сети.', ['Резкое изменение масштаба по слоям — потенциальная проблема.', 'Числа показывают, насколько градиент доходит до ранних слоёв.']],
    cnn: ['Как свёртка создаёт карту признаков?', 'Сначала посмотри на вход, затем на ядро и полученную карту — это последовательные этапы одной операции.', ['Это исходная матрица пикселей.', 'Это коэффициенты применяемого фильтра.', 'Здесь результат умножений и сумм.']],
    rnn: ['Что рекуррентная сеть запоминает о последовательности?', 'Каждая строка показывает скрытое состояние после очередного токена.', ['Сравни строки: вектор состояния меняется по мере чтения токенов.', 'Норма состояния помогает увидеть, как растёт или затухает сигнал.']],
    nlp: ['Как текст превращается в числа?', 'Сравни веса слов в разных документах с похожестью самих документов.', ['Яркие клетки показывают более выраженную связь термина с документом.', 'Похожие документы обычно имеют большую cosine similarity.']],
    bpe: ['Как BPE уменьшает число токенов?', 'Слияния частых пар меняют разбиение слов. Сравни длины токенизации.', ['Более короткий столбик означает меньше токенов для слова.']],
    text_classification: ['Откуда берётся прогноз класса текста?', 'Сравни апостериорные вероятности классов и частоты слов учебных документов.', ['Самый высокий столбик — класс, который модель считает наиболее вероятным.', 'Матрица показывает исходные счётчики слов.']],
    embeddings: ['Какие слова похожи по контекстам?', 'Сопоставь совместную встречаемость с проекцией векторов слов.', ['Яркая клетка означает сильную контекстную связь.', 'Близость на проекции даёт подсказку, но она не полностью сохраняет высокую размерность.']],
    attention: ['На какие токены обращает внимание модель?', 'Строка — запрос (Query), столбец — ключ (Key). Чем ярче клетка, тем больше его вес после softmax.', ['Выбери строку: её веса внимания в сумме равны единице.', 'Это входные векторы токенов.', 'Это значения после смешивания по весам внимания.']],
    multihead: ['Зачем нужны несколько голов внимания?', 'Каждая голова строит собственную матрицу внимания. Сравни, что именно они выделяют.', ['Сравни распределения весов у разных голов.', 'Итоговый выход складывается из преобразованных результатов голов.']],
    decoding: ['Почему следующий токен меняется от температуры?', 'Сначала сравни исходные вероятности, затем эффект Top-K или Top-P.', ['Высота столбика — вероятность выбрать токен.']],
    rag: ['Как система выбирает полезные документы?', 'Сравни похожесть запроса и фрагментов; это поиск контекста, а не генерация ответа.', ['Более высокий столбик означает большую близость текста к запросу.']],
    bandits: ['Как стратегия балансирует исследование и награду?', 'Сравни истинные вероятности выигрыша с оценками агента и наблюдай накопленную потерю.', ['Сравни истинные и изученные вероятности каждой ручки.', 'Следи, сколько агент теряет из-за неоптимального выбора.']],
    math: ['Как функция меняется локально?', 'Наклон касательной и градиент показывают направление изменения функции.', ['Точка на графике показывает текущее значение.', 'Линии уровня помогают понять многомерную форму.']],
    algebra: ['Как векторы и матрицы меняют пространство?', 'Свяжи входные компоненты с результатом скалярного произведения или преобразования.', ['Каждый элемент отвечает определённой операции.']],
    norms: ['Почему у норм разная геометрия?', 'Сравни области равной нормы: они по-разному ограничивают вектор весов.', ['Форма единичного шара зависит от выбранной нормы.']],
    information: ['Как измерить неопределённость и различие распределений?', 'Наблюдай изменение энтропии и расстояний при изменении вероятностей.', ['Важно сравнивать распределения, а не отдельные несвязанные значения.']]
  };
  let current = null;
  let signature = '';
  let view = 'contour';
  let extrasExpanded = false;
  const unique = arr => [...new Set(arr)];
  const number = v => Number.isFinite(Number(v)) ? Number(v).toLocaleString('ru-RU',{maximumFractionDigits:4}) : String(v);
  const isSurface = trace => trace.type === 'scatter3d' || trace.type === 'surface';
  const isHeatmap = trace => trace.type === 'heatmap' || trace.type === 'contour';
  const text = (element, value) => {element.textContent = value; return element;};
  function el(tag,className,content){const node=document.createElement(tag);if(className)node.className=className;if(content!==undefined)text(node,content);return node;}
  function viewSet(next){view=next;signature='';if(current)render(current);}
  function showMore(){extrasExpanded=!extrasExpanded;signature='';if(current)render(current);}
  function prepareEntries(charts,page,webgl){
    if(page==='regression' && charts.length>=4){
      const chosen = view==='surface' && webgl ? 1 : 2;
      return [{index:0,kind:'hero',note:0},{index:chosen,kind:'secondary',note:1,toggle:true},{index:3,kind:'secondary',note:2}];
    }
    const entries=charts.map((_,i)=>({index:i,kind:i===0?'hero':'secondary',note:Math.min(i,2)}));
    if(entries.length>3 && !extrasExpanded)return entries.slice(0,3);
    return entries;
  }
  function createGuide(host,page,reg){
    const guide=lessons[page]||['Посмотри, как работает алгоритм','Меняй один параметр за раз и наблюдай результат на графике.',[]];
    const intro=el('section','visual-brief');intro.setAttribute('aria-label','Как читать эксперимент');
    const marker=el('div','visual-brief-kicker','ВОПРОС ЭКСПЕРИМЕНТА');
    const headline=el('h2','visual-brief-title',guide[0]);
    const desc=el('p','visual-brief-description',guide[1]);
    intro.append(marker,headline,desc);
    if(page==='regression' && reg && reg.current && Array.isArray(reg.history) && reg.history.length>1){
      const before=Number(reg.history[0].loss),after=Number(reg.current.loss);
      if(Number.isFinite(before)&&Number.isFinite(after)){
        const delta=before>0?Math.round((1-after/before)*100):null;
        const label=delta===null?'':delta>=0?'Ошибка уменьшилась на '+delta+'% от начала обучения':'Ошибка выросла на '+Math.abs(delta)+'% — попробуй меньший шаг обучения';
        if(label)intro.append(el('div','visual-brief-feedback',label));
      }
    }
    host.append(intro);
  }
  function drawFrame(host,entries,state){
    host.querySelectorAll('.js-plotly-plot').forEach(plot=>{try{Plotly.purge(plot)}catch(_){}});
    const guide=lessons[state.page]||['','',''];
    host.replaceChildren();
    createGuide(host,state.page,state.reg);
    entries.forEach((entry,slot)=>{
      const spec=state.charts[entry.index];
      const section=el('section','chart-card visual-chart '+(entry.kind==='hero'?'visual-hero':'visual-secondary'));
      section.dataset.index=String(entry.index);
      const head=el('div','chart-head visual-chart-head');
      const copy=el('div','visual-chart-copy');
      copy.append(el('div','visual-step',slot===0?'01 · ОСНОВНОЕ':'0'+(slot+1)+' · ДЕТАЛИ'));
      copy.append(el('h3','visual-chart-title',spec.title||'Результат вычисления'));
      head.append(copy);
      const actions=el('div','visual-actions');
      const help=el('p','visual-chart-intro',(guide[2]||[])[entry.note]||'Меняй параметры и наблюдай изменение данных.');
      if(entry.toggle){
        const tabs=el('div','visual-view-tabs');tabs.setAttribute('role','group');tabs.setAttribute('aria-label','Режим поверхности потерь');
        for(const [id,label] of [['contour','2D'],['surface','3D']]){
          if(id==='surface'&&!state.webgl)continue;
          const btn=el('button','visual-view-button'+(view===id?' active':''),label);btn.type='button';btn.setAttribute('aria-pressed',String(view===id));btn.addEventListener('click',()=>viewSet(id));tabs.append(btn);
        }
        actions.append(tabs);
      }
      const controls=el('div','visual-controls');controls.setAttribute('role','group');controls.setAttribute('aria-label','Управление масштабом графика');
      for(const [key,label,tip] of [['in','+','Приблизить'],['out','−','Отдалить'],['reset','↺','Вернуть исходный масштаб']]){
        const button=el('button','visual-plot-control',label);button.type='button';button.title=tip;button.setAttribute('aria-label',tip);button.dataset.action=key;
        button.addEventListener('click',()=>scale(section.querySelector('.chart-body'),key));controls.append(button);
      }
      actions.append(controls);head.append(actions);
      section.append(head,help);
      const canvas=el('div','chart-body visual-plot');canvas.id='plot-'+slot;canvas.setAttribute('role','img');canvas.setAttribute('aria-label',(spec.title||'График')+'. '+help.textContent);
      section.append(canvas);
      const hint=el('div','visual-chart-footer');hint.append(el('span','visual-key','●'),el('span','',entry.kind==='hero'?'Изменяй параметры справа: график пересчитывается по настоящей модели.':'Наведите курсор на график, чтобы увидеть точные значения.'));
      section.append(hint);host.append(section);
    });
    if(state.charts.length>3 && state.page!=='regression'){
      const rest=Math.max(0,state.charts.length-3);const more=el('button','visual-more',extrasExpanded?'− Свернуть дополнительные графики':'+ Ещё '+rest+' график'+(rest===1?'':'а'));
      more.type='button';more.setAttribute('aria-expanded',String(extrasExpanded));more.addEventListener('click',showMore);host.append(more);
    }
  }
  function classColors(trace){
    const array=trace.marker&&trace.marker.color;
    if(!Array.isArray(array)||!array.length||array.length>5000||!array.every(v=>['string','number'].includes(typeof v)))return null;
    const values=unique(array);
    if(values.length<2||values.length>8||!values.every(v=>Number.isInteger(Number(v))&&Number(v)>=0&&Number(v)<=7))return null;
    return values.map((v,i)=>({value:v,color:palette.classes[i%palette.classes.length]}));
  }
  function designTraces(chart,theme){
    const sequential=theme==='light'?palette.sequential:palette.sequentialDark;
    let expanded=[];
    for(const source of chart.traces||[]){
      let trace={...source};
      if(trace.type==='scatter'&&String(trace.mode||'markers').includes('markers')){
        const classes=classColors(trace);
        if(classes&&trace.x&&trace.y&&trace.x.length===trace.y.length&&trace.x.length===source.marker.color.length){
          classes.forEach((c,index)=>{
            const positions=source.marker.color.map((v,i)=>String(v)===String(c.value)?i:-1).filter(i=>i>=0);
            expanded.push({...trace,x:positions.map(i=>trace.x[i]),y:positions.map(i=>trace.y[i]),name:'Класс '+c.value,showlegend:true,marker:{...trace.marker,color:c.color,size:Math.max(7,Number(trace.marker.size)||7),line:{color:theme==='light'?'#fff':'#2a2a2a',width:1.3}},hovertemplate:'Класс '+c.value+'<br>x: %{x}<br>y: %{y}<extra></extra>'});
          });continue;
        }
      }
      if(trace.type==='surface'||trace.type==='heatmap'||trace.type==='contour'){
        if(trace.colorscale==='RdBu')trace.colorscale=palette.divergent;
        else if(trace.colorscale!=='Greys'&&trace.colorscale!=='Greys_r')trace.colorscale=sequential;
        trace.showscale=trace.type==='heatmap'&&expanded.length===0;
        if(trace.showscale)trace.colorbar={thickness:9,len:.72,outlinewidth:0,tickfont:{size:10},x:1.015};
        if(trace.type==='surface')trace.lighting={ambient:.82,diffuse:.75,specular:.07,roughness:.98};
        if(trace.type==='contour')trace.contours={...trace.contours,showlabels:false};
      }
      if(trace.type==='scatter'&&trace.mode&&trace.mode.includes('lines'))trace.line={width:2.5,...trace.line};
      if(trace.type==='scatter'&&trace.mode&&trace.mode.includes('markers'))trace.marker={size:7,opacity:.90,...trace.marker};
      if(trace.type==='bar'){
        trace.marker={color:palette.teaching,...trace.marker};
        if(!Array.isArray(trace.marker.color)&&typeof trace.marker.color==='string')trace.marker.color=palette.teaching;
        trace.marker.line={width:0};trace.opacity=.92;
      }
      expanded.push(trace);
    }
    return expanded;
  }
  function fallback3d(traces){return traces.map(t=>{
    if(t.type==='surface')return {type:'contour',x:t.x,y:t.y,z:t.z,colorscale:t.colorscale||palette.sequential,showscale:false,ncontours:18,hovertemplate:'w: %{x}<br>b: %{y}<br>Ошибка: %{z}<extra></extra>'};
    if(t.type==='scatter3d')return {type:'scatter',x:t.x,y:t.y,name:t.name,mode:t.mode,line:t.line,marker:{...t.marker,size:5}};
    return t;
  });}
  function plotLayout(spec,traces,theme,is3d,dimensions){
    const light=theme==='light';const axis=light?'#dadfe0':'#464a4c';const textColor=light?'#666c70':'#bbbdbf';
    const layout={
      paper_bgcolor:'rgba(0,0,0,0)',plot_bgcolor:'rgba(0,0,0,0)',autosize:true,
      height:dimensions.height,margin:{l:68,r:27,t:14,b:60,pad:0},
      font:{family:'Inter,system-ui,-apple-system,Segoe UI,sans-serif',size:12,color:textColor},
      colorway:[palette.teaching,palette.model,palette.secondary,palette.caution,'#9180A7','#647f74'],
      hoverlabel:{bgcolor:light?'#fff':'#333',bordercolor:axis,font:{size:12,color:light?'#242424':'#f2f2f2'}},hovermode:'closest',
      uirevision:current.page+'-'+spec.title,
      showlegend:traces.filter(t=>t.showlegend!==false&&t.name).length>1,
      legend:{orientation:'h',x:0,y:-.25,font:{size:11},bgcolor:'rgba(0,0,0,0)',itemsizing:'constant'},
      xaxis:{title:{text:spec.layout?.xaxis?.title||'',font:{size:11},standoff:10},gridcolor:axis,gridwidth:.5,zeroline:false,showline:false,ticks:'outside',ticklen:3,nticks:6,automargin:true,showspikes:false},
      yaxis:{title:{text:spec.layout?.yaxis?.title||'',font:{size:11},standoff:10},gridcolor:axis,gridwidth:.5,zeroline:false,ticks:'outside',ticklen:3,nticks:6,automargin:true,showspikes:false}
    };
    // Preserve mathematical intent, but never let a backend title duplicate the card heading.
    const custom=spec.layout||{};
    for(const [key,value] of Object.entries(custom))if(!['margin','height','title','xaxis','yaxis','scene','paper_bgcolor','plot_bgcolor'].includes(key))layout[key]=value;
    if(custom.xaxis)layout.xaxis={...layout.xaxis,...custom.xaxis,title:layout.xaxis.title};
    if(custom.yaxis)layout.yaxis={...layout.yaxis,...custom.yaxis,title:layout.yaxis.title};
    if(is3d){
      layout.margin={l:0,r:0,t:4,b:0};
      layout.scene={...custom.scene,bgcolor:'rgba(0,0,0,0)',aspectmode:'auto',camera:{eye:{x:1.50,y:1.42,z:1.18}},
        xaxis:{backgroundcolor:'rgba(0,0,0,0)',gridcolor:axis,zerolinecolor:axis,title:custom.scene?.xaxis?.title||'Вес w',tickfont:{size:10}},
        yaxis:{backgroundcolor:'rgba(0,0,0,0)',gridcolor:axis,zerolinecolor:axis,title:custom.scene?.yaxis?.title||'Bias b',tickfont:{size:10}},
        zaxis:{backgroundcolor:'rgba(0,0,0,0)',gridcolor:axis,zerolinecolor:axis,title:custom.scene?.zaxis?.title||'Ошибка',tickfont:{size:10}}};
      delete layout.xaxis;delete layout.yaxis;
    }
    // Candidate split labels are unreadable when crowded horizontally; use a ranked horizontal chart.
    const longBar=traces.find(t=>t.type==='bar'&&Array.isArray(t.x)&&t.x.length>=7&&t.x.some(v=>String(v).length>11));
    if(longBar&&!is3d&&traces.length===1){
      longBar.orientation='h';const names=longBar.x;longBar.x=longBar.y;longBar.y=names;layout.xaxis.title={text:spec.layout?.yaxis?.title||'Значение'};layout.yaxis.title={text:''};layout.margin.l=145;
      layout.yaxis.autorange='reversed';layout.height=Math.max(dimensions.height,Math.min(600,names.length*29+80));
    }
    const matrix=traces.find(t=>isHeatmap(t));
    if(matrix && matrix.type==='heatmap' && Array.isArray(matrix.z)){
      const rows=matrix.z.length,cols=Array.isArray(matrix.z[0])?matrix.z[0].length:0;
      if(rows>=2&&rows<=9&&cols>=2&&cols<=9&&Math.abs(rows-cols)<=2){
        layout.yaxis.scaleanchor='x';layout.yaxis.scaleratio=1;
      }
      if(cols>12)layout.xaxis.tickangle=-30;
    }
    return layout;
  }
  function scale(plot,action){
    if(!plot||!plot.layout||!window.Plotly)return;
    const plotly=window.Plotly;
    if(plot.layout.scene){
      if(action==='reset'){plotly.relayout(plot,{'scene.camera':{eye:{x:1.5,y:1.42,z:1.18}}});return;}
      const eye=plot.layout.scene.camera?.eye||{x:1.5,y:1.42,z:1.18};const f=action==='in'?.8:1.25;
      plotly.relayout(plot,{'scene.camera.eye':{x:eye.x*f,y:eye.y*f,z:eye.z*f}});return;
    }
    if(action==='reset'){plotly.relayout(plot,{'xaxis.autorange':true,'yaxis.autorange':true});return;}
    const update={};for(const axis of ['xaxis','yaxis']){
      const range=plot.layout[axis]?.range;
      if(!range||range.length!==2||!range.every(Number.isFinite))continue;
      const mid=(range[0]+range[1])/2,half=(range[1]-range[0])/2*(action==='in'?.77:1.30);
      update[axis+'.range']=[mid-half,mid+half];
    }
    if(Object.keys(update).length)plotly.relayout(plot,update);
  }
  function render(state){
    if(!Array.isArray(state.charts)||!window.Plotly)return;
    current=state;
    const host=$('#graphs');if(!host)return;
    const entries=prepareEntries(state.charts,state.page,state.webgl);
    const key=state.page+'|'+entries.map(e=>e.index).join(',')+'|'+String(state.webgl)+'|'+String(extrasExpanded);
    if(signature!==key){signature=key;drawFrame(host,entries,state);}
    else {const feedback=$('.visual-brief-feedback',host);if(feedback)feedback.remove();
      if(state.page==='regression' && state.reg && state.reg.history?.length>1){
        const intro=$('.visual-brief',host),start=state.reg.history[0].loss,end=state.reg.current.loss;
        if(intro&&start>0&&Number.isFinite(end)){const delta=Math.round((1-end/start)*100);intro.append(el('div','visual-brief-feedback',delta>=0?'Ошибка уменьшилась на '+delta+'%':'Ошибка выросла на '+(-delta)+'% — проверь learning rate'));}
      }
    }
    entries.forEach((entry,slot)=>{
      const target=$('#plot-'+slot,host),spec=state.charts[entry.index];if(!target)return;
      let traces=designTraces(spec,state.theme);
      const needs3d=traces.some(isSurface);
      if(needs3d&&!state.webgl)traces=fallback3d(traces);
      const th=target.clientHeight||((entry.kind==='hero')?450:320);
      const layout=plotLayout(spec,traces,state.theme,needs3d&&state.webgl,{height:th});
      const config={responsive:true,displaylogo:false,displayModeBar:false,scrollZoom:true,doubleClick:'reset',showTips:false};
      Plotly.react(target,traces,layout,config).catch(err=>console.error('ML Universe chart:',spec.title,err));
    });
  }
  window.MLStory={render,lessons,scale,plotLayout,designTraces};
})();
