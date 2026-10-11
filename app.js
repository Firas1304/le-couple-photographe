(function(){
var $=function(s,c){return(c||document).querySelector(s)},$$=function(s,c){return[].slice.call((c||document).querySelectorAll(s))};
var reduce=matchMedia('(prefers-reduced-motion:reduce)').matches;
/* PHOTOS : remplacez null par l'URL de votre photo (ex. "photos/mariage-01.jpg"). L'index correspond à data-ph dans les pages. */
var PHOTOS=window.PHOTOS||[];
var HUES=[28,12,40,22,8,34,18,44,26,14,30,20,36,10,24,16,38,6,32,42];
function ph(i){var h=HUES[i%HUES.length];
 var svg="<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 600 800' preserveAspectRatio='xMidYMid slice'><defs><radialGradient id='a' cx='"+(30+i*7%50)+"%' cy='"+(25+i*11%40)+"%' r='80%'><stop offset='0' stop-color='hsl("+h+",62%,62%)'/><stop offset='.55' stop-color='hsl("+(h-12)+",45%,26%)'/><stop offset='1' stop-color='hsl("+(h-20)+",30%,9%)'/></radialGradient><filter id='n'><feTurbulence type='fractalNoise' baseFrequency='.8' numOctaves='2'/><feColorMatrix values='0 0 0 0 1 0 0 0 0 .9 0 0 0 0 .8 0 0 0 .18 0'/></filter></defs><rect width='600' height='800' fill='url(#a)'/><ellipse cx='300' cy='560' rx='120' ry='230' fill='rgba(0,0,0,.35)'/><circle cx='300' cy='310' r='62' fill='rgba(0,0,0,.35)'/><rect width='600' height='800' filter='url(#n)'/><text x='300' y='770' text-anchor='middle' font-family='sans-serif' font-size='18' letter-spacing='6' fill='rgba(255,255,255,.55)'>VOTRE PHOTO ICI</text></svg>";
 return"data:image/svg+xml;charset=utf-8,"+encodeURIComponent(svg)}
$$('[data-ph]').forEach(function(im){var i=+im.dataset.ph;im.src=PHOTOS[i]||ph(i)});
var yr=$('#yr');if(yr)yr.textContent=new Date().getFullYear();
/* intro appareil photo (accueil, une fois par session) */
var pre=$('#pre'),flash=$('#flash');
function openSite(){document.body.classList.remove('intro');document.body.classList.add('loaded')}
if(pre){
 var seen=false;try{seen=sessionStorage.getItem('intro')==='1'}catch(e){}
 if(reduce||seen){pre.remove();if(flash)flash.remove();openSite()}
 else{
  try{sessionStorage.setItem('intro','1')}catch(e){}
  document.body.classList.add('intro');
  var shot=false;
  var shoot=function(){if(shot)return;shot=true;pre.classList.add('shoot');flash.classList.add('go');
   setTimeout(function(){pre.classList.add('gone');openSite()},70);
   setTimeout(function(){flash.remove();pre.remove()},700)};
  setTimeout(shoot,1000);
  pre.addEventListener('click',shoot)}
}else document.body.classList.add('loaded');
/* reveal */
var io;
if('IntersectionObserver'in window){io=new IntersectionObserver(function(es){es.forEach(function(e){if(e.isIntersecting){e.target.classList.add('in');io.unobserve(e.target)}})},{threshold:.12});$$('.rv').forEach(function(el,i){el.style.transitionDelay=(i%4)*.08+'s';io.observe(el)})}
setTimeout(function(){$$('.rv').forEach(function(e){e.classList.add('in')})},6000);
/* menu */
var b=$('#burger'),m=$('#menu');
if(b&&m){b.onclick=function(){var o=m.classList.toggle('open');b.setAttribute('aria-expanded',o);b.textContent=o?'Fermer':'Menu'};
$$('#menu a').forEach(function(a){a.addEventListener('click',function(){m.classList.remove('open');b.textContent='Menu'})})}
/* cursor */
var cur=$('#cur'),cx=0,cy=0,tx=0,ty=0,mx=0,my=0;
addEventListener('mousemove',function(e){tx=e.clientX;ty=e.clientY;mx=e.clientX/innerWidth-.5;my=e.clientY/innerHeight-.5});
$$('[data-cursor],a,button').forEach(function(el){el.addEventListener('mouseenter',function(){cur&&cur.classList.add('big')});el.addEventListener('mouseleave',function(){cur&&cur.classList.remove('big')})});
/* manifesto */
var mp=$('#manifesto'),ws=[];
if(mp){var words=mp.textContent.trim().split(/\s+/);mp.innerHTML=words.map(function(w){return'<span class="w">'+w+'</span>'}).join(' ');ws=$$('.w',mp)}
/* gallery */
var gal=$('#galerie'),track=$('#track'),floats=$$('.float'),band=$('.band img'),desk=matchMedia('(min-width:821px)');
function setH(){if(gal&&track){gal.style.height=desk.matches?(track.scrollWidth-innerWidth+innerHeight+60)+'px':''}}
addEventListener('resize',setH);addEventListener('load',setH);setH();
function loop(){
 var vh=innerHeight;
 if(cur){cx+=(tx-cx)*.2;cy+=(ty-cy)*.2;cur.style.transform='translate('+cx+'px,'+cy+'px)'}
 if(mp){var r=mp.getBoundingClientRect(),p=Math.min(1,Math.max(0,(vh*.85-r.top)/(r.height+vh*.35)));ws.forEach(function(w,i){w.style.opacity=reduce?1:(i/ws.length<p?1:.14)})}
 if(gal&&track&&desk.matches){var g=gal.getBoundingClientRect(),prog=Math.min(1,Math.max(0,-g.top/(g.height-vh)));track.style.transform='translateX('+(-prog*(track.scrollWidth-innerWidth))+'px)'}
 if(!reduce){floats.forEach(function(f){var d=+f.dataset.depth;f.style.transform='translate('+(mx*d*600)+'px,'+(my*d*600+scrollY*d*-1.2)+'px)'});
  if(band){var br=band.parentNode.getBoundingClientRect();band.style.transform='translateY('+((br.top-vh/2)*-.12)+'px)'}}
 requestAnimationFrame(loop)}
loop();
/* formulaire : envoi Formspree si SITE_FORM, sinon copie du message ; bouton WhatsApp si SITE_WA */
var WA=window.SITE_WA||'',FE=window.SITE_FORM||'';
function waLink(t){return 'https://wa.me/'+WA+(t?'?text='+encodeURIComponent(t):'')}
if(WA){var w=document.createElement('a');w.className='wa';w.href=waLink('Bonjour, je souhaite un devis pour un photographe/vidéaste.');w.target='_blank';w.rel='noopener';w.setAttribute('aria-label','Écrire sur WhatsApp');
 w.innerHTML='<svg viewBox="0 0 32 32" width="26" height="26" fill="currentColor" aria-hidden="true"><path d="M16 3a13 13 0 0 0-11.2 19.6L3 29l6.6-1.7A13 13 0 1 0 16 3zm0 2.4a10.6 10.6 0 1 1-5.4 19.7l-.4-.2-3.9 1 1-3.8-.3-.4A10.6 10.6 0 0 1 16 5.4zm-4 5.4c-.3 0-.7.1-1 .5-.4.4-1.3 1.3-1.3 3.1s1.3 3.6 1.500 3.8c.2.300 2.600 4.100 6.4 5.6 3.100 1.200 3.700.9 4.400.9.700-.1 2.200-.9 2.500-1.800.3-.9.300-1.600.2-1.800-.1-.2-.4-.3-.8-.5l-2.300-1.100c-.3-.1-.6-.2-.8.200l-1 1.200c-.2.200-.4.300-.8.100-.4-.2-1.500-.6-2.900-1.800-1.100-1-1.800-2.200-2-2.600-.2-.4 0-.6.200-.8l.6-.6c.2-.2.200-.4.400-.6.100-.2 0-.5 0-.7l-1-2.400c-.3-.6-.5-.5-.8-.5z"/></svg>';
 document.body.appendChild(w)}
var f=$('#form');
if(f)f.addEventListener('submit',function(e){e.preventDefault();var v=function(i){var el=$('#'+i);return el?el.value.trim():''},note=$('#note');
 if(!v('nom')||!/\S+@\S+\.\S+/.test(v('mail'))){note.textContent='Indiquez vos prénoms et un email valide.';return}
 var txt='Bonjour, nous sommes '+v('nom')+' ('+v('mail')+'). Projet : '+v('type')+', lieu : '+v('zone')+(v('date')?', date : '+v('date'):'')+'. '+v('msg');
 var alt=function(){var m='Message copié. Collez-le dans un message à @le_couple_photographe sur Instagram.';
  try{navigator.clipboard.writeText(txt).then(function(){note.textContent=m},function(){note.textContent=txt})}catch(x){note.textContent=txt}
  if(WA)note.innerHTML+=' Ou <a href="'+waLink(txt)+'" target="_blank" rel="noopener">écrivez-nous sur WhatsApp</a>.'};
 if(!FE){alt();return}
 var btn=f.querySelector('button[type=submit]');btn.disabled=true;note.textContent='Envoi en cours…';
 fetch(FE,{method:'POST',headers:{'Content-Type':'application/json',Accept:'application/json'},body:JSON.stringify({name:v('nom'),email:v('mail'),_replyto:v('mail'),date:v('date'),lieu:v('zone'),projet:v('type'),message:v('msg')})})
 .then(function(r){if(!r.ok)throw 0;note.textContent='Merci, votre demande est bien envoyée. Nous revenons vers vous très vite.';f.reset()})
 .catch(function(){alt()}).then(function(){btn.disabled=false})});
/* Google Analytics 4 : chargé seulement après consentement (RGPD). Actif si GA_ID est renseigné dans build.py */
var GA=window.SITE_GA||'';
function loadGA(){if(window.__ga)return;window.__ga=1;var s=document.createElement('script');s.async=1;s.src='https://www.googletagmanager.com/gtag/js?id='+GA;document.head.appendChild(s);
 window.dataLayer=window.dataLayer||[];window.gtag=function(){dataLayer.push(arguments)};gtag('js',new Date());gtag('config',GA,{anonymize_ip:true})}
if(GA){var ch=null;try{ch=localStorage.getItem('consent')}catch(e){}
 if(ch==='yes')loadGA();
 else if(ch!=='no'){var bar=document.createElement('div');bar.className='cookie';bar.setAttribute('role','dialog');bar.setAttribute('aria-label','Cookies');
  bar.innerHTML='<p>Nous utilisons un outil de mesure d\'audience pour améliorer le site. Vous pouvez l\'accepter ou le refuser.</p><div><button type="button" id="ck-yes">Accepter</button><button type="button" id="ck-no">Refuser</button></div>';
  document.body.appendChild(bar);
  var set=function(v){try{localStorage.setItem('consent',v)}catch(e){}bar.remove();if(v==='yes')loadGA()};
  $('#ck-yes').onclick=function(){set('yes')};$('#ck-no').onclick=function(){set('no')}}}
})();
