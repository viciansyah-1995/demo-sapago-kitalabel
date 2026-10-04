document.querySelectorAll('.e-con').forEach(e=>e.classList.add('e-lazyloaded'));
document.querySelectorAll('.eael-tabs-content > div').forEach((e,i)=>{e.style.display=i===0?'block':'none';e.classList.toggle('active',i===0);});
document.querySelectorAll('.eael-tabs-nav li[aria-selected="true"]').forEach(e=>e.classList.add('active'));
document.querySelectorAll('.eael-tabs-content .elementor-tab-title').forEach(e=>{e.setAttribute('aria-expanded','true');e.classList.add('elementor-active');if(e.nextElementSibling)e.nextElementSibling.style.display='block';});
document.querySelectorAll('.eael-accordion-header').forEach(e=>{e.setAttribute('role','button');e.setAttribute('aria-expanded','false');});
// The official SapaGo embed owns the chat interface and conversation state.
document.querySelectorAll('a[data-chat], a[href="#form"]').forEach(link => {
  link.addEventListener('click', event => {
    event.preventDefault();
    const frame = document.querySelector('iframe[title="Sapago Live Chat"]');
    if (frame) {
      frame.focus();
      frame.animate([{filter:'drop-shadow(0 0 0 #ed913c)'},{filter:'drop-shadow(0 0 10px #ed913c)'},{filter:'drop-shadow(0 0 0 #ed913c)'}],{duration:900});
    }
  });
});
// Native, dependency-free replacements for the original Elementor interactions.
document.querySelectorAll('.eael-advance-tabs').forEach(tabs=>{const triggers=[...tabs.querySelectorAll('.eael-tabs-nav li')],contents=[...tabs.querySelectorAll('.eael-tabs-content > div')];triggers.forEach((t,i)=>{t.tabIndex=0;function select(){triggers.forEach((x,j)=>{x.classList.toggle('active',i===j);x.setAttribute('aria-selected',String(i===j));});contents.forEach((x,j)=>{x.classList.toggle('active',i===j);x.style.display=i===j?'block':'none';});}t.addEventListener('click',select);t.addEventListener('keydown',e=>{if(e.key==='Enter'||e.key===' '){e.preventDefault();select();}});});});
document.querySelectorAll('.eael-accordion-header,.elementor-tab-title').forEach(h=>{h.tabIndex=0;const toggle=()=>{const c=h.nextElementSibling;if(!c)return;const expanded=h.getAttribute('aria-expanded')==='true';h.setAttribute('aria-expanded',String(!expanded));h.classList.toggle('active',!expanded);h.classList.toggle('elementor-active',!expanded);c.style.display=expanded?'none':'block';};h.addEventListener('click',toggle);h.addEventListener('keydown',e=>{if(e.key==='Enter'){e.preventDefault();toggle();}});});
document.querySelectorAll('.elementor-counter-number').forEach(n=>{n.textContent=n.dataset.toValue||n.textContent;});
document.querySelectorAll('.swiper,.swiper-container').forEach(carousel=>{const w=carousel.querySelector('.swiper-wrapper');if(!w)return;const slides=[...w.children].filter(s=>!s.classList.contains('swiper-slide-duplicate'));let index=0;function show(i){index=(i+slides.length)%slides.length;w.scrollTo({left:slides[index].offsetLeft-w.offsetLeft,behavior:'smooth'});}carousel.parentElement.querySelectorAll('.elementor-swiper-button-next,.swiper-button-next').forEach(b=>{b.setAttribute('aria-label','Gambar berikutnya');b.tabIndex=0;b.addEventListener('click',()=>show(index+1));b.addEventListener('keydown',e=>{if(e.key==='Enter')show(index+1);});});carousel.parentElement.querySelectorAll('.elementor-swiper-button-prev,.swiper-button-prev').forEach(b=>{b.setAttribute('aria-label','Gambar sebelumnya');b.tabIndex=0;b.addEventListener('click',()=>show(index-1));b.addEventListener('keydown',e=>{if(e.key==='Enter')show(index-1);});});});
