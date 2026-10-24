/* Controller/render tests in a deliberately small DOM stub. These do not claim visual browser QA. */
const {test}=require('node:test');
const assert=require('node:assert/strict');
const vm=require('node:vm');
const fs=require('node:fs');
const E=require('../engine.js');
function workspace(store={}) {
 const handlers={},elements=new Map(),location={hash:''};
 function element(id){if(!elements.has(id)) elements.set(id,{innerHTML:'',textContent:'',value:'',returnValue:'',classList:{add(){},remove(){}},focus(){},scrollIntoView(){},addEventListener(k,f){handlers[id+':'+k]=f;},showModal(){this.open=true;}});return elements.get(id);}
 const document={title:'',querySelector:element,addEventListener(k,f){handlers[k]=f;},createElement(){return {click(){}};}};
 const context={window:{Sovereignty:E,scrollTo(){},addEventListener(k,f){handlers['window:'+k]=f;}},document,location,localStorage:{getItem(k){return store[k]||null;},setItem(k,v){store[k]=v;}},navigator:{clipboard:{writeText:async()=>{}}},console,setTimeout:()=>0,clearTimeout(){},URL:{createObjectURL(){return 'blob:test';},revokeObjectURL(){}},Blob,FormData:class{constructor(target){this.values=target.values;}get(k){return this.values[k]??null;}has(k){return k in this.values;}}};
 vm.runInNewContext(fs.readFileSync('app.js','utf8'),context);
 return {store,html:()=>element('#main').innerHTML,el:element,state:()=>JSON.parse(store['unscripted.workspace.v1']),async click(data){await handlers.click({target:{closest(){return {dataset:data};}}});},route(route){location.hash='#'+route;handlers['window:hashchange']();},submit(id,values){handlers.submit({preventDefault(){},target:{id,values}});},reset(){element('#confirm-dialog').returnValue='reset';handlers['#confirm-dialog:close']();location.hash='#overview';handlers['window:hashchange']();}};
}
test('all seven routes render with no uncaught controller errors',()=>{
 const w=workspace();for(const r of ['overview','tokyo','finance','privacy','contracts','history','research']) {w.route(r);assert(w.html().length>1000);assert(!w.html().includes('undefined'));}
});
test('Tokyo hides recommendation before human choice; explore never accepts',async()=>{
 const w=workspace();w.route('tokyo');assert(!w.html().includes('Your agent was about to'));assert(!w.html().includes('2036'));
 w.submit('human-form',{choice:'explore',reason:'I might want something different.'});assert(w.html().includes('Your agent was about to'));assert(w.html().includes('Explore the opportunity'));
 await w.click({action:'tokyo-next'});await w.click({action:'tokyo-open'});
 assert.equal(w.state().tokyo.outcome,'open');assert(w.html().includes('You have not accepted the job'));
 const p=w.state().records.at(-1);assert.equal(p.humanFirstChoice.choice,'explore');assert.equal(p.authorization.choice,'request-details');assert.match(p.outcome,/Rejection not authorized/);
});
test('Tokyo rejection requires explicit click and records the approval',async()=>{
 const w=workspace();w.route('tokyo');w.submit('human-form',{choice:'reject',reason:''});await w.click({action:'tokyo-next'});await w.click({action:'tokyo-reject'});
 const p=w.state().records.at(-1);assert.equal(p.authorization.explicit,true);assert.equal(p.authorization.choice,'approve');assert.equal(w.state().tokyo.outcome,'rejected');
});
test('Tokyo deferral leaves offer unresolved and deadline visible',async()=>{
 const w=workspace();w.route('tokyo');w.submit('human-form',{choice:'information',reason:''});await w.click({action:'tokyo-next'});await w.click({action:'tokyo-later'});
 assert.equal(w.state().tokyo.outcome,'later');assert.match(w.state().records.at(-1).outcome,/no reply sent/);assert(w.html().includes('26 Oct'));
});
test('finance approval cannot bypass cap; editing cap changes live result and records snapshot',async()=>{
 const w=workspace();w.route('finance');await w.click({action:'finance-authorize'});assert.equal(w.store['unscripted.workspace.v1'],undefined);
 w.route('contracts');w.submit('contract-form',{enabled:'on',cap:'200000',expires:'2040-12-31',freshnessDays:'365',recipients:'investment-platform.example',context:'test',confirmationRequired:'on'});
 w.route('finance');assert(w.html().includes('Still your call'));await w.click({action:'finance-authorize'});
 assert.equal(w.state().records.at(-1).contractSnapshot.cap,200000);assert.match(w.state().records.at(-1).outcome,/no money moved/);
});
test('privacy minimization records denied original and safe alternative separately',async()=>{
 const w=workspace();w.route('privacy');await w.click({action:'privacy-safe'});const rec=w.state().records;
 assert.equal(rec.at(-2).evaluation.route,'BLOCK');assert.equal(rec.at(-1).evaluation.route,'EXECUTE');assert.deepEqual(rec.at(-1).agentProposal.dataCategories,[]);
});
test('contract and passports survive a simulated refresh',async()=>{
 const store={},w=workspace(store);await w.click({action:'routine'});assert.equal(w.state().records.length,48);
 const refreshed=workspace(store);refreshed.route('history');assert(refreshed.html().includes('1 from your interactions'));assert.equal(refreshed.state().records.length,48);
});
test('reset restores seeded state, contracts and hidden Tokyo recommendation',async()=>{
 const w=workspace();await w.click({action:'routine'});w.reset();assert.equal(w.state().records.length,47);assert.equal(w.state().contracts.finance.cap,25000);w.route('tokyo');assert(!w.html().includes('Your agent was about to'));
});
test('human-entered text is escaped before rendering and remains inert',async()=>{
 const w=workspace();w.route('tokyo');w.submit('human-form',{choice:'explore',reason:'<img src=x onerror=alert(1)>'});assert(!w.html().includes('<img src=x'));assert(w.html().includes('&lt;img'));
});
test('corrupt persisted data recovers to usable workspace with visible notice',()=>{
 const w=workspace({'unscripted.workspace.v1':'{broken'});assert(w.html().includes('Local storage could not be read'));assert(w.html().includes('A little less autopilot'));
});
