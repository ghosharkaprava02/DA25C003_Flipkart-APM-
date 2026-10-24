const {test} = require('node:test');
const assert = require('node:assert/strict');
const {actions,defaults,evaluate,authorize,NOW} = require('../engine.js');
const copy=x=>JSON.parse(JSON.stringify(x));
test('routine reversible work executes without interruption',()=>assert.equal(evaluate(actions.routine,defaults().routine).route,'EXECUTE'));
test('Tokyo stale preference requires human review',()=>{
 const e=evaluate(actions.tokyo,defaults().career);
 assert.equal(e.route,'REVIEW');assert(e.ruleIds.includes('INT-02'));assert(e.ruleIds.includes('CONS-01'));
});
test('Tokyo cannot execute with no approval or an unscoped approval',()=>{
 assert.equal(authorize(actions.tokyo,defaults().career,null).allowed,false);
 for(const changes of [{actionId:'other'},{at:'2036-01-01'},{explicit:false},{choice:'explore'}]) {
  assert.equal(authorize(actions.tokyo,defaults().career,{actionId:actions.tokyo.id,at:NOW,explicit:true,choice:'approve',...changes}).allowed,false);
 }
});
test('current exact authorization permits a simulated rejection',()=>assert.equal(authorize(actions.tokyo,defaults().career,{actionId:actions.tokyo.id,at:NOW,explicit:true,choice:'approve'}).allowed,true));
test('investment is blocked at 25,000; raised cap returns REVIEW',()=>{
 const c=defaults().finance;
 assert.equal(evaluate(actions.finance,c).route,'BLOCK');
 c.cap=200000;
 assert.equal(evaluate(actions.finance,c).route,'REVIEW');
 assert.equal(authorize(actions.finance,c,null).allowed,false);
 assert.equal(authorize(actions.finance,c,{actionId:actions.finance.id,at:NOW,explicit:true,choice:'approve'}).allowed,true);
});
test('confirmation toggle never removes mandatory high-stakes review',()=>{
 const c=defaults().finance;c.cap=300000;c.confirmationRequired=false;
 assert.equal(evaluate(actions.finance,c).route,'REVIEW');
});
test('approval cannot override cap, expiry or recipient block',()=>{
 for(const mutation of [c=>c.cap=100,c=>c.expires='2040-10-23',c=>c.allowedRecipients=[]]) {
  const c=defaults().finance;c.cap=300000;mutation(c);
  assert.equal(authorize(actions.finance,c,{actionId:actions.finance.id,at:NOW,explicit:true,choice:'approve'}).allowed,false);
 }
});
test('third-party private data blocks; user cannot invent consent',()=>{
 const c=defaults().privacy;c.thirdPartyConsent=true;
 assert.equal(evaluate(actions.privacy,c).route,'BLOCK');
 assert(evaluate(actions.privacy,c).ruleIds.includes('PRIV-01'));
 assert.equal(authorize(actions.privacy,c,{actionId:actions.privacy.id,at:NOW,explicit:true,choice:'approve'}).allowed,false);
});
test('minimized alternative executes only within active permissions',()=>{
 const c=defaults().privacy;
 assert.equal(evaluate(actions.minimized,c).route,'EXECUTE');
 c.allowedRecipients=[];assert.equal(evaluate(actions.minimized,c).route,'BLOCK');
});
test('disabled, absent and mismatched contracts fail closed',()=>{
 for(const c of [undefined,{...defaults().career,enabled:false},defaults().finance]) assert.equal(evaluate(actions.tokyo,c).route,'BLOCK');
});
test('expiry uses inclusive demo calendar date; invalid expiry blocks',()=>{
 const c=defaults().routine;
 c.expires='2040-10-24';assert.equal(evaluate(actions.routine,c).route,'EXECUTE');
 for(const expiry of ['2040-10-23','invalid','']) {c.expires=expiry;assert.equal(evaluate(actions.routine,c).route,'BLOCK');}
});
test('recipient changes take effect immediately',()=>{
 const c=defaults().routine;c.allowedRecipients=['calendar.local'];
 assert.equal(evaluate(actions.routine,c).route,'BLOCK');
});
test('invalid financial limits never grant authority',()=>{
 for(const cap of [-1,NaN,Infinity,undefined,'300000']) assert.equal(evaluate(actions.finance,{...defaults().finance,cap}).route,'BLOCK');
});
test('routine confirmation option and cap changes affect routing',()=>{
 const c=defaults().routine;c.confirmationRequired=true;
 assert.equal(evaluate(actions.routine,c).route,'REVIEW');
 c.cap=100;assert.equal(evaluate(actions.routine,c).route,'BLOCK');
});
test('future or invalid source preference fails into review',()=>{
 for(const date of ['invalid','2041-01-01']) {
  const a=copy(actions.routine);a.sourcePreference.date=date;
  assert.equal(evaluate(a,defaults().routine).route,'REVIEW');
 }
});
test('engine is pure and deterministic',()=>{
 const c=defaults().career,a=copy(actions.tokyo),before=JSON.stringify({a,c});
 assert.deepEqual(evaluate(a,c),evaluate(a,c));assert.equal(JSON.stringify({a,c}),before);
});
