document.addEventListener('DOMContentLoaded',function(){
  var h=document.querySelector('.site-header'),t=document.querySelector('.nav-toggle');
  if(t){t.addEventListener('click',function(){var o=h.classList.toggle('open');t.setAttribute('aria-expanded',o);});}
  var f=document.querySelector('.contact-form');
  if(f){f.addEventListener('submit',function(e){
    if(f.action.indexOf('YOUR_FORM_ID')>-1){e.preventDefault();alert('Form endpoint not configured yet. Please email info@cineticmotion.com');return;}
    e.preventDefault();
    fetch(f.action,{method:'POST',body:new FormData(f),headers:{Accept:'application/json'}})
      .then(function(r){if(!r.ok)throw 0;f.reset();f.querySelector('.thanks').hidden=false;})
      .catch(function(){alert('Send failed. Please email info@cineticmotion.com');});
  });}
});
