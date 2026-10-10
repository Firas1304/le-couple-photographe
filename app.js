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
/* preloader (accueil) */
var pre=$('#pre');
if(pre){var cnt=$('#cnt'),t0=performance.now(),dur=reduce?1:1500;
 (function tick(t){var p=Math.min(1,(t-t0)/dur);cnt.textContent=Math.round(p*100);if(p<1)requestAnimationFrame(tick);else{pre.classList.add('out');document.body.classList.add('loaded')}})(t0)}
else document.body.classList.add('loaded');
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
/* formulaire */
var f=$('#form');
if(f)f.addEventListener('submit',function(e){e.preventDefault();var v=function(i){var el=$('#'+i);return el?el.value.trim():''},note=$('#note');
 if(!v('nom')||!/\S+@\S+\.\S+/.test(v('mail'))){note.textContent='Indiquez vos prénoms et un email valide.';return}
 var txt='Bonjour, nous sommes '+v('nom')+' ('+v('mail')+'). Projet : '+v('type')+', lieu : '+v('zone')+(v('date')?', date : '+v('date'):'')+'. '+v('msg');
 var done=function(){note.textContent='Message copié. Collez-le dans un message à @le_couple_photographe sur Instagram.'};
 try{navigator.clipboard.writeText(txt).then(done,function(){note.textContent=txt})}catch(x){note.textContent=txt}});
})();
