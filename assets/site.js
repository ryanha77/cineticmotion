document.documentElement.classList.add('js');
// Reload always starts at the top of the page (browser would otherwise restore the old scroll position).
if('scrollRestoration' in history){history.scrollRestoration='manual';}
if(!location.hash){window.scrollTo(0,0);}
document.addEventListener('DOMContentLoaded',function(){
  // Scroll reveal: .reveal elements fade in from below when they enter the viewport.
  var rv=document.querySelectorAll('.reveal');
  if(rv.length){
    if('IntersectionObserver' in window){
      var io=new IntersectionObserver(function(es){es.forEach(function(e){if(e.isIntersecting){e.target.classList.add('in');io.unobserve(e.target);}});},{threshold:.2,rootMargin:'0px 0px -8% 0px'});
      rv.forEach(function(el){io.observe(el);});
    } else { rv.forEach(function(el){el.classList.add('in');}); }
  }

  var h=document.querySelector('.site-header'),t=document.querySelector('.nav-toggle');
  if(t){t.addEventListener('click',function(){var o=h.classList.toggle('open');t.setAttribute('aria-expanded',o);});}

  // Analytics helper: no-op when GA is not configured.
  function track(name,params){if(typeof gtag==='function'){gtag('event',name,params||{});}}
  // Outbound / mail link clicks
  document.querySelectorAll('a[href^="mailto:"],a[href^="http"]').forEach(function(a){
    if(a.host===location.host&&a.protocol!=='mailto:')return;
    a.addEventListener('click',function(){track(a.protocol==='mailto:'?'email_click':'outbound_click',{link_url:a.href});});
  });

  var f=document.querySelector('.contact-form');
  if(f){f.addEventListener('submit',function(e){
    e.preventDefault();
    var page=document.body.className.replace('page-','');
    if(f.action.indexOf('YOUR_FORM_ID')>-1){
      // No form backend configured (GitHub Pages is static): open the visitor's mail client with the form content.
      var fd=new FormData(f),lines=[];
      ['name','company','address','email','phone','subject','message'].forEach(function(k){var v=fd.get(k);if(v)lines.push(k+': '+v);});
      var subj=encodeURIComponent('[cineticmotion.com] '+(fd.get('subject')||'Contact')+' - '+(fd.get('name')||''));
      track('form_submit',{method:'mailto',page:page});
      location.href='mailto:'+f.dataset.mailto+'?subject='+subj+'&body='+encodeURIComponent(lines.join('\n'));
      return;
    }
    fetch(f.action,{method:'POST',body:new FormData(f),headers:{Accept:'application/json'}})
      .then(function(r){if(!r.ok)throw 0;f.reset();f.querySelector('.thanks').hidden=false;track('form_submit',{method:'formspree',page:page});})
      .catch(function(){track('form_error',{page:page});alert('Send failed. Please email '+f.dataset.mailto);});
  });}
});
