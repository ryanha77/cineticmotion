#!/usr/bin/env python3
"""Generates the static site (ko at /, en at /en/) from the content below.
Run:  python3 src/build.py
"""
import os, html

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE = "https://www.cineticmotion.com"
FORM_ENDPOINT = "https://formspree.io/f/YOUR_FORM_ID"   # TODO: replace after creating a Formspree form (until then the form falls back to mailto:)
GA_ID = "G-N6YCD6YCRB"   # Google Analytics 4 measurement ID (Admin > Data streams > Web). Set to "" to disable.
IG_MAIN = "https://www.instagram.com/cineticmotion"
IG_POSTME = "https://www.instagram.com/post___me/"
EMAIL = "info@cineticmotion.com"

T = {
 "ko": dict(
   lang="ko", other="en", other_label="EN", prefix="",
   nav=[("제품","products"),("CM-1","cm-1"),("RADIUS","radius"),("POST-ME","contact-post-me"),("문의","contact")],
   footer="©2026 주식회사 씨네틱모션, 서울시 강남구 테헤란로77길 11-15, 1001호 06159",
   home=dict(title="Home", h1="하이테크 필름메이킹 솔루션",
             sub="복잡한 무빙을 구현하는 정밀한 제어, 필름메이킹의 한계를 뛰어넘는 모션", cta="자세히 보기 →"),
   products=dict(title="PRODUCTS",
     cm1="영상 전문가를 위해 고도화된 로봇 제어 기능을 최적화하여 다양하고 창의적인 촬영으로 작업 영역을 넓혀줍니다.",
     radius="단 몇 번의 터치로 하드웨어와 소프트웨어를 가장 직관적으로 연결합니다.",
     more="자세히 보기 →", h2="영상 크리에이터의 상상을 실현하는 로봇 카메라 시스템",
     p="단 몇 번의 직관적인 조작만으로 6축 모션(팬·틸트·붐·트랙·더치롤)과 렌즈 제어(FIZ)를 정밀하게 연동하여 완벽한 미장센을 완성합니다. 손끝에서 펼쳐지는 섬세한 컨트롤과 무한한 앵글의 자유도로 로봇 카메라 시스템 CM-1은 촬영의 새로운 기준을 제시합니다."),
   cm1=dict(title="CM-1",
     lead="영상 전문가를 위해 고도화된 로봇 제어 기능을 최적화하여 다양하고 창의적인 촬영으로 작업 영역을 넓혀줍니다.",
     p="시네틱모션(Cinetic Motion)의 CM-1은 정밀한 촬영, 뛰어난 사용 편의성, 그리고 다재다능함을 겸비한 최첨단 전문가용 로봇 카메라 시스템입니다. 고도화된 로봇 기술을 영상 제작에 접목하여 오차 없는 초정밀 촬영과 반복 촬영 작업을 안정적으로 수행합니다.",
     features=["상용 영상 제작 툴과 유사한 직관적인 타임라인 컨트롤","완벽한 초점, 정밀한 조리개 및 줌 제어","6축 로봇이 선사하는 광범위한 카메라 워크","조이스틱으로 조정하는 로봇 카메라 앵글","제공된 거리로 원터치 회전 운동","6축 토크센서 적용으로 높은 안정성","리프트로 확장된 높이와 활동 범위","버튼 하나로 직접 조절하는 카메라 앵글","자동 수평, 수직 제어로 완벽해지는 화면 구도","다중 모션 구현에 최적화된 직관적인 프로젝트 관리 UI","정밀한 반복 촬영으로 정교한 합성 구현","라이브 모니터링으로 정확한 프레이밍 구현"],
     quote="견적문의", spec_title="SPECIFICATION"),
   radius=dict(title="RADIUS",
     lead="단 몇 번의 터치로 하드웨어와 소프트웨어를 가장 직관적으로 연결합니다.",
     p="키프레임, 클립, 타임라인 등 필름메이커에게 친숙한 인터페이스를 그대로 이식하여 직감적이고 강력한 모션 컨트롤을 수행할 수 있습니다.",
     kf="KEY FEATURES",
     features=[("로봇 시뮬레이터","실제 하드웨어를 구동하기 전, 가상환경에서 모션의 궤적을 미리 시뮬레이션하여 동작 가능성과 시스템 안정성을 완벽하게 사전 확보합니다."),
               ("직관적 제어","팬, 틸트, 붐, 트랙, 더치롤 등 전통적인 촬영 기법은 물론, 이전에는 구사할 수 없었던 독창적인 카메라 무빙까지 손쉽게 구현할 수 있습니다."),
               ("타임라인 컨트롤","상용 영상 툴과 동일한 키프레임 및 타임라인 방식으로 별도의 학습 없이 로봇을 손쉽게 제어합니다."),
               ("세부 조정","섬세한 카메라 워크를 위해 로봇 모션과 키프레임 값을 정교하게 튜닝할 수 있습니다."),
               ("프로젝트 매니지먼트","복잡한 키프레임과 프로젝트를 효율적으로 관리할 수 있습니다."),
               ("라이브 모니터링","정확한 동작을 위한 라이브 모니터링은 효율적인 작업환경을 제공합니다.")]),
   contact=dict(title="문의", h1="문의하기", ig="@cineticmotion",
     f=dict(name="성함",company="회사명",address="주소",email="이메일",phone="전화",subject="주제",choose="Choose an option",msg="내용",submit="제출",
            thanks="문의 감사드립니다. 곧 답변 드리겠습니다."),
     subjects=["CM-1","RADIUS","POST-ME","기타"]),
   postme=dict(title="CONTACT POST-ME", explore="Explore Products →", h1="Contact Us", ig="@cineticmotion", tag="@POST-ME"),
 ),
 "en": dict(
   lang="en", other="ko", other_label="KO", prefix="../",
   nav=[("PRODUCTS","products"),("CM-1","cm-1"),("RADIUS","radius"),("POST-ME","contact-post-me"),("CONTACT","contact")],
   footer="©2026 by Cinetic Motion Inc. Suite #1001, 11-15 Teheran-ro 77-gil, Gangnam-gu, Seoul 06159, Korea",
   home=dict(title="Home", h1="The Next Generation of Filmmaking",
             sub="Redefining complex camera movements with precision control, engineered to push the limits of motion.", cta="Learn More →"),
   products=dict(title="PRODUCTS",
     cm1="CM-1 optimizes high-level robot control for film/video professionals, extending the scope of work to diverse and creative shooting.",
     radius="The powerful RADIUS-based timeline controls go hand in hand with video professionals' intuition.",
     more="Learn More →", h2="A Robot Camera System Empowering Creative Visions",
     p="With a few clicks, the camera angle, FIZ (Focus/Iris/Zoom), pan, tilt, boom, track, and Dutch roll are accurately implemented to create the best shot. Above all, the intelligent robot camera CM-1 that provides delicate control and free angles presents a new standard for filming."),
   cm1=dict(title="CM-1",
     lead="CM-1 optimizes high-level robot control for film/video professionals, extending the scope of work to diverse and creative shooting.",
     p="Cinetic Motion's CM-1 is a state-of-the-art professional robot camera system that provides accurate shooting, easy usability and versatility. By incorporating advanced robot technology into filmmaking, repetitive and ultra-precise imaging is performed reliably.",
     features=["Intuitive timeline control familiar with existing video tools","Perfect focus/Iris/Zoom control","6-axis robot control providing freedom of movements","Controller makes camera angle adjustment faster and easier","One-touch rotation movement with a provided distance","Maximum safety with torque sensors applied to all motors","Extended height and range of activity with additional lift","Adjust the angle you want with your hands","Precise automatic horizontal/vertical adjustment for any distortions","Intuitive project management for multiple motion implementations","Pixel accurate repetitive motion for seamless compositing","Live monitoring integrated into the interface for accurate framing"],
     quote="Ask for Quote", spec_title="SPECIFICATION"),
   radius=dict(title="RADIUS",
     lead="The powerful RADIUS-based timeline controls go hand in hand with video professionals' intuition.",
     p="Familiar interface and architecture with contemporary editing and animation tools, such as keyframes, clips, timelines, and projects, to connect most intuitively between virtual (software) and reality (hardware).",
     kf="KEY FEATURES",
     features=[("ROBOT SIMULATOR","Virtual environment to ensure real-world behavior in a simulation."),
               ("INTUITIVE CONTROL","In addition to the traditional shooting grammar such as Boom/Track/Dutchroll/Pan/Tilt, you can implement a completely new and free camera motion."),
               ("TIMELINE CONTROL","Easily operate the robot with keyframes and timelines similar to imaging tools."),
               ("DETAILED ADJUSTMENTS","Detailed adjustment of motion and keyframe is possible for delicate camera work."),
               ("PROJECT MANAGEMENT","Organize complex keyframes and projects efficiently."),
               ("LIVE MONITORING","Live monitoring for accurate behavior provides an efficient working environment.")]),
   contact=dict(title="CONTACT", h1="Contact Us", ig="@cineticmotion",
     f=dict(name="Name",company="Company Name",address="Address",email="Email",phone="Phone",subject="Subject",choose="Choose an option",msg="Message",submit="Submit",
            thanks="Thanks for submitting! We will get back to you shortly."),
     subjects=["CM-1","RADIUS","POST-ME","Other"]),
   postme=dict(title="CONTACT POST-ME", explore="Explore Products →", h1="Contact Us", ig="@cineticmotion", tag="@POST-ME"),
 ),
}

SPEC = [("Spherical Reach","2,200 mm in diameter"),("Vertical Reach","2,700 mm in height (lift stroke 700mm)"),
        ("Load Capability","10 Kg"),("Robot Speed","1,000 mm/s"),("Total Weight","90 kg"),("Robot","32 kg"),
        ("Controller","9 kg"),("Lift","20 kg"),("Base","20 kg"),("Power","700W (nominal) AC 220v")]

E = html.escape

def analytics():
    """Google Analytics 4 (gtag.js). Emits nothing while GA_ID is still the placeholder."""
    if not GA_ID or "XXXX" in GA_ID:
        return "<!-- analytics: set GA_ID in src/build.py and rebuild -->"
    return f"""<!-- Google Analytics 4 -->
<script async src="https://www.googletagmanager.com/gtag/js?id={GA_ID}"></script>
<script>
window.dataLayer=window.dataLayer||[];function gtag(){{dataLayer.push(arguments);}}
gtag('js',new Date());gtag('config','{GA_ID}',{{anonymize_ip:true}});
</script>"""

def video(P):
    """Autoplay background loop (second home section on Wix). Skipped while assets/video/home-loop.mp4 is missing."""
    if not os.path.exists(os.path.join(ROOT, "assets/video/home-loop.mp4")):
        return "<!-- home video: run scripts/fetch-assets.sh to download assets/video/home-loop.mp4 -->"
    return f"""<section class="full visual"><video autoplay muted loop playsinline preload="metadata" src="{P}assets/video/home-loop.mp4"></video></section>"""

def layout(L, slug, title, body, cur):
    P = L["prefix"]
    other_href = ("en/" if L["lang"]=="ko" else "../") + ("" if slug=="index" else slug + ".html")
    nav = "".join(f'<li><a href="{s}.html"{" class=active" if s==cur else ""}>{E(n)}</a></li>' for n,s in L["nav"])
    canonical = SITE + ("/" if L["lang"]=="ko" else "/en/") + ("" if slug=="index" else slug)
    return f"""<!DOCTYPE html>
<html lang="{L['lang']}">
<head>
<meta charset="utf-8">
{analytics()}
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{E(title)} | Cinetic Motion</title>
<meta name="description" content="Cinetic Motion – high-tech robotic camera systems (CM-1, RADIUS) for filmmaking.">
<link rel="canonical" href="{canonical}">
<link rel="alternate" hreflang="ko-kr" href="{SITE}/{'' if slug=='index' else slug}">
<link rel="alternate" hreflang="en-us" href="{SITE}/en/{'' if slug=='index' else slug}">
<link rel="icon" href="{P}assets/img/favicon.png">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Jost:wght@300;400;500&display=swap" rel="stylesheet">
<link rel="stylesheet" href="https://cdn.jsdelivr.net/gh/orioncactus/pretendard@v1.3.9/dist/web/static/pretendard.min.css">
<link rel="stylesheet" href="{P}assets/style.css">
</head>
<body class="page-{slug}">
<header class="site-header">
  <a class="logo" href="index.html"><img src="{P}assets/img/logo-white.png" alt="Cinetic Motion"></a>
  <button class="nav-toggle" aria-label="Menu" aria-expanded="false">☰</button>
  <nav><ul>{nav}<li><a class="lang" href="{other_href}">{L['other_label']}</a></li></ul></nav>
</header>
<main>
{body}
</main>
<footer class="site-footer">
  <p><a href="mailto:{EMAIL}">{EMAIL}</a> <a class="ig" href="{IG_MAIN}" target="_blank" rel="noopener"><img src="{P}assets/img/instagram.png" alt="Instagram"></a></p>
  <p class="copy">{E(L['footer'])}</p>
</footer>
<script src="{P}assets/site.js"></script>
</body>
</html>
"""

def home(L):
    P=L["prefix"]; c=L["home"]
    return f"""
<section class="hero full" style="background-image:url('{P}assets/img/home-hero.jpg')">
  <div class="hero-text">
    <h1>{E(c['h1'])}</h1>
    <p>{E(c['sub'])}</p>
    <a class="cta" href="products.html">{E(c['cta'])}</a>
  </div>
</section>
{video(P)}
"""

def products(L):
    P=L["prefix"]; c=L["products"]
    return f"""
<section class="product-row">
  <div class="product-card">
    <img class="wordmark" src="{P}assets/img/cm1-wordmark.png" alt="CM-1">
    <img class="product-visual" src="{P}assets/img/products-cm1.jpg" alt="CM-1 robot camera system">
    <p>{E(c['cm1'])}</p>
    <a class="more" href="cm-1.html">{E(c['more'])}</a>
  </div>
  <div class="product-card">
    <img class="wordmark" src="{P}assets/img/radius-wordmark.png" alt="RADIUS">
    <img class="product-visual" src="{P}assets/img/products-radius.jpg" alt="RADIUS software">
    <p>{E(c['radius'])}</p>
    <a class="more" href="radius.html">{E(c['more'])}</a>
  </div>
</section>
<section class="statement" style="background-image:url('{P}assets/img/products-bg.jpg')">
  <h2>{E(c['h2'])}</h2>
  <p>{E(c['p'])}</p>
</section>
"""

def cm1(L):
    P=L["prefix"]; c=L["cm1"]
    # Wix lists the 12 feature captions column-wise but the icon sprite is row-wise; this maps caption i -> icon file.
    icon_order=[1,2,3,4,9,10,11,12,5,6,7,8]
    feats="".join(f'<li><img src="{P}assets/img/cm1-icon-{icon_order[i]:02d}.png" alt=""><span>{E(t)}</span></li>' for i,t in enumerate(c["features"]))
    spec="".join(f'<tr><th>{E(k)}</th><td>{E(v)}</td></tr>' for k,v in SPEC)
    return f"""
<section class="hero product-hero" style="background-image:url('{P}assets/img/cm1-bg.jpg')">
  <img class="wordmark big" src="{P}assets/img/cm1-title.png" alt="CM-1">
  <p class="lead">{E(c['lead'])}</p>
</section>
<section class="intro two-col">
  <img src="{P}assets/img/cm1-product.png" alt="CM-1 robot camera system">
  <p>{E(c['p'])}</p>
</section>
<section class="features-grid dark">
  <ul>{feats}</ul>
  <a class="btn" href="contact.html">{E(c['quote'])}</a>
</section>
<section class="spec grey">
  <h2>{E(c['spec_title'])}</h2>
  <table>{spec}</table>
</section>
"""

def radius(L):
    P=L["prefix"]; c=L["radius"]
    cards="".join(f'<li><img src="{P}assets/img/radius-feature-{i+1}.jpg" alt=""><h3>{E(h)}</h3><p>{E(p)}</p></li>' for i,(h,p) in enumerate(c["features"]))
    return f"""
<section class="hero product-hero" style="background-image:url('{P}assets/img/radius-hero.jpg')">
  <img class="wordmark big" src="{P}assets/img/radius-title.png" alt="RADIUS">
  <p class="lead">{E(c['lead'])}</p>
</section>
<section class="intro two-col">
  <img src="{P}assets/img/radius-product.png" alt="RADIUS controller">
  <p>{E(c['p'])}</p>
</section>
<section class="screenshot"><img src="{P}assets/img/radius-screen.png" alt="RADIUS timeline interface"></section>
<section class="key-features">
  <h2>{E(c['kf'])}</h2>
  <ul>{cards}</ul>
</section>
"""

def form(L, ig_handle, with_subject=True):
    f=L["contact"]["f"]; subj=L["contact"]["subjects"]
    opts="".join(f'<option>{E(s)}</option>' for s in subj)
    subject = f"""<label class="half">{E(f['subject'])} *<select name="subject" required><option value="" disabled selected>{E(f['choose'])}</option>{opts}</select></label>""" if with_subject else f"""<label>{E(f['subject'])}<input name="subject"></label>"""
    return f"""
<form class="contact-form" action="{FORM_ENDPOINT}" method="POST" data-thanks="{E(f['thanks'])}" data-mailto="{EMAIL}">
  <input type="hidden" name="_subject" value="[cineticmotion.com] Contact">
  <input type="text" name="_gotcha" style="display:none" tabindex="-1" autocomplete="off">
  <label class="half">{E(f['name'])} *<input name="name" required></label>
  <label class="half">{E(f['company'])}<input name="company"></label>
  <label>{E(f['address'])}<input name="address"></label>
  <label class="half">{E(f['email'])} *<input type="email" name="email" required></label>
  <label class="half">{E(f['phone'])}<input type="tel" name="phone"></label>
  {subject}
  <label>{E(f['msg'])}<textarea name="message" rows="8"></textarea></label>
  <button type="submit" class="btn">{E(f['submit'])}</button>
  <p class="thanks" hidden>{E(f['thanks'])}</p>
</form>"""

def contact(L):
    c=L["contact"]
    return f"""
<section class="contact two-col">
  <div class="contact-info">
    <h1>{E(c['h1'])}</h1>
    <p><a href="mailto:{EMAIL}">{EMAIL}</a></p>
    <p><a href="{IG_MAIN}" target="_blank" rel="noopener">{E(c['ig'])}</a></p>
  </div>
  {form(L, c['ig'])}
</section>
"""

def postme(L):
    c=L["postme"]
    return f"""
<section class="postme-top"><a class="cta" href="products.html">{E(c['explore'])}</a></section>
<section class="contact two-col">
  <div class="contact-info">
    <h1>{E(c['h1'])}</h1>
    <p><a href="mailto:{EMAIL}">{EMAIL}</a></p>
    <p><a href="{IG_MAIN}" target="_blank" rel="noopener">{E(c['ig'])}</a></p>
    <p><a href="{IG_POSTME}" target="_blank" rel="noopener">{E(c['tag'])}</a></p>
  </div>
  {form(L, c['tag'], with_subject=False)}
</section>
"""

PAGES = [("index","home",home),("products","products",products),("cm-1","cm1",cm1),("radius","radius",radius),
         ("contact","contact",contact),("contact-post-me","postme",postme)]

def main():
    for lang,L in T.items():
        outdir = ROOT if lang=="ko" else os.path.join(ROOT,"en")
        os.makedirs(outdir, exist_ok=True)
        for slug,key,fn in PAGES:
            title = L[key]["title"]
            with open(os.path.join(outdir, slug+".html"),"w",encoding="utf-8") as fh:
                fh.write(layout(L, slug, title, fn(L), slug))
            print("wrote", os.path.relpath(os.path.join(outdir, slug+".html"), ROOT))
    # sitemap
    urls=[SITE+"/"]+[f"{SITE}/{s}" for s,_,_ in PAGES[1:]]+[SITE+"/en/"]+[f"{SITE}/en/{s}" for s,_,_ in PAGES[1:]]
    with open(os.path.join(ROOT,"sitemap.xml"),"w") as fh:
        fh.write('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'+
                 "".join(f"  <url><loc>{u}</loc></url>\n" for u in urls)+"</urlset>\n")

if __name__=="__main__":
    main()
