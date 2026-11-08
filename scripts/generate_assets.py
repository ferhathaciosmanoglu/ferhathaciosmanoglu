#!/usr/bin/env python3
"""
GitHub profil README görsellerini üretir (assets/ klasörüne).

Kullanım:
    python scripts/generate_assets.py

Proje kartlarını değiştirmek için aşağıdaki PROJECTS listesini düzenleyip
betiği yeniden çalıştırmanız yeterli. Harici bağımlılık yoktur.
"""
from pathlib import Path
from textwrap import wrap
from xml.sax.saxutils import escape

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "assets"
OUT.mkdir(exist_ok=True)

SANS = "Inter, 'Segoe UI', -apple-system, BlinkMacSystemFont, 'Helvetica Neue', Arial, sans-serif"
MONO = "'JetBrains Mono', 'SFMono-Regular', Consolas, 'Liberation Mono', 'DejaVu Sans Mono', monospace"
MONO_W = 0.6  # tek aralıklı yazı karakter genişliği (em)

THEMES = {
    "dark": dict(
        bg="#0a0a0a", panel="#0f0f0f", panel2="#141414", border="#262626",
        grid="#ffffff", grid_op=".05", text="#fafafa", desc="#d4d4d4", muted="#a3a3a3",
        name_a="#ffffff", name_b="#ffd9b8", orb_op=".55", orb2_op=".22",
        pill_bg="#171717", pill_stroke="#2e2e2e", pill_text="#ffb26b",
        live_bg="#0f1f14", live_stroke="#1f3d29", live_text="#4ade80",
        tag_bg="#1f130a", tag_stroke="#3d2412", tag_text="#ffb26b",
        glow_op=".20",
    ),
    "light": dict(
        bg="#fafaf9", panel="#ffffff", panel2="#ffffff", border="#e7e5e4",
        grid="#000000", grid_op=".05", text="#0a0a0a", desc="#404040", muted="#57534e",
        name_a="#111111", name_b="#c2410c", orb_op=".30", orb2_op=".16",
        pill_bg="#fff7ed", pill_stroke="#fed7aa", pill_text="#c2410c",
        live_bg="#f0fdf4", live_stroke="#bbf7d0", live_text="#15803d",
        tag_bg="#fff7ed", tag_stroke="#fed7aa", tag_text="#c2410c",
        glow_op=".12",
    ),
}

ACCENT = ("#e8530a", "#ff7a2a", "#ffb26b")

# 24x24 çizgi ikonlar (stroke tabanlı, kendi çizimimiz)
ICONS = {
    "clipboard": '<rect x="5" y="4" width="14" height="17" rx="2.5"/><rect x="9" y="2" width="6" height="4" rx="1.2"/><path d="M8.5 13.5l2.5 2.5 4.5-5"/>',
    "camera": '<path d="M3.5 8.5h3.2l1.8-2.8h7l1.8 2.8h3.2v10.8h-17z"/><circle cx="12" cy="13.6" r="3.4"/>',
    "flame": '<path d="M12 2.8c.8 3.4 5.6 5.4 5.6 10.6a5.6 5.6 0 0 1-11.2 0c0-2.3 1.1-3.9 2.3-5 .1 2 .9 3.2 2.1 3.4-.4-3.4.3-6.2 1.2-9z"/>',
    "file": '<path d="M14 3H7.5A2.5 2.5 0 0 0 5 5.5v13A2.5 2.5 0 0 0 7.5 21h9a2.5 2.5 0 0 0 2.5-2.5V8z"/><path d="M14 3v5h5"/><path d="M8.5 13h7M8.5 16.5h4.5"/>',
    "calendar": '<rect x="3.5" y="5" width="17" height="15.5" rx="2.5"/><path d="M3.5 10h17M8 3v4M16 3v4"/><path d="M7.5 14h2M11 14h2M14.5 14h2M7.5 17h2M11 17h2"/>',
    "grid": '<rect x="3.5" y="3.5" width="7" height="7" rx="1.8"/><rect x="13.5" y="3.5" width="7" height="7" rx="1.8"/><rect x="3.5" y="13.5" width="7" height="7" rx="1.8"/><path d="M17 13.2v7.6M13.2 17h7.6"/>',
    "globe": '<circle cx="12" cy="12" r="8.5"/><path d="M3.5 12h17"/><path d="M12 3.5c2.6 2.4 3.8 5.2 3.8 8.5s-1.2 6.1-3.8 8.5c-2.6-2.4-3.8-5.2-3.8-8.5S9.4 5.9 12 3.5z"/>',
    "briefcase": '<rect x="3.5" y="7" width="17" height="12.5" rx="2.5"/><path d="M9 7V5.5A1.5 1.5 0 0 1 10.5 4h3A1.5 1.5 0 0 1 15 5.5V7"/><path d="M3.5 12.5h17"/>',
    "mail": '<rect x="3.5" y="5.5" width="17" height="13" rx="2.5"/><path d="M4.5 7l7.5 6 7.5-6"/>',
    "idcard": '<rect x="3" y="5" width="18" height="14" rx="2.5"/><circle cx="8.5" cy="11" r="2.2"/><path d="M5.6 16c.6-1.5 1.6-2.2 2.9-2.2s2.3.7 2.9 2.2"/><path d="M14 10h4M14 13.5h3"/>',
}


def defs_common(uid: str) -> str:
    a, b, c = ACCENT
    return f"""
    <linearGradient id="accent{uid}" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0" stop-color="{a}"/><stop offset=".5" stop-color="{b}"/><stop offset="1" stop-color="{c}"/>
    </linearGradient>
    <linearGradient id="icon{uid}" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0" stop-color="#ff6a1a"/><stop offset="1" stop-color="#ffb26b"/>
    </linearGradient>"""


# ----------------------------------------------------------------- banner
def banner(theme: str) -> str:
    t = THEMES[theme]
    W, H = 1280, 400
    line = "sahadaki sorunu → çevrimdışı çalışan uygulamaya"
    fs = 19
    cw = fs * MONO_W
    text_x = 46
    text_w = len(line) * cw
    box_w = int(text_x + text_w + 34)
    n = len(line)
    # Yazma efekti: karakter karakter açılan maske + imleç
    widths = [round(i * cw, 1) for i in range(n + 1)]
    key_times = [round(i / n, 4) for i in range(n + 1)]
    w_values = ";".join(str(w) for w in widths)
    x_values = ";".join(str(round(text_x + w + 2, 1)) for w in widths)
    kt = ";".join(str(k) for k in key_times)

    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-labelledby="title desc">
  <title id="title">Ferhat Hacıosmanoğlu</title>
  <desc id="desc">Mekatronik Mühendisi · PWA ve İş Uygulamaları Geliştirici</desc>
  <defs>{defs_common('')}
    <clipPath id="frame"><rect width="{W}" height="{H}" rx="24"/></clipPath>
    <pattern id="grid" width="40" height="40" patternUnits="userSpaceOnUse">
      <path d="M40 0H0V40" fill="none" stroke="{t['grid']}" stroke-opacity="{t['grid_op']}"/>
    </pattern>
    <radialGradient id="fade" cx="72%" cy="35%" r="75%">
      <stop offset="0" stop-color="#fff"/><stop offset="1" stop-color="#fff" stop-opacity="0"/>
    </radialGradient>
    <mask id="gridMask"><rect width="{W}" height="{H}" fill="url(#fade)"/></mask>
    <radialGradient id="orbA">
      <stop offset="0" stop-color="#ff7a2a" stop-opacity="{t['orb_op']}"/><stop offset="1" stop-color="#ff7a2a" stop-opacity="0"/>
    </radialGradient>
    <radialGradient id="orbB">
      <stop offset="0" stop-color="#ffb26b" stop-opacity="{t['orb2_op']}"/><stop offset="1" stop-color="#ffb26b" stop-opacity="0"/>
    </radialGradient>
    <linearGradient id="name" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0" stop-color="{t['name_a']}"/><stop offset=".55" stop-color="{t['name_a']}"/><stop offset="1" stop-color="{t['name_b']}"/>
    </linearGradient>
    <clipPath id="typing">
      <rect x="{text_x}" y="8" width="0" height="32">
        <animate attributeName="width" values="{w_values}" keyTimes="{kt}" dur="3.2s" begin="0.6s" calcMode="discrete" fill="freeze"/>
      </rect>
    </clipPath>
  </defs>

  <g clip-path="url(#frame)">
    <rect width="{W}" height="{H}" fill="{t['bg']}"/>
    <rect width="{W}" height="{H}" fill="url(#grid)" mask="url(#gridMask)"/>

    <circle cx="1090" cy="40" r="330" fill="url(#orbA)">
      <animateTransform attributeName="transform" type="translate" values="0 0; -36 24; 0 0" dur="14s" repeatCount="indefinite"/>
    </circle>
    <circle cx="120" cy="430" r="280" fill="url(#orbB)">
      <animateTransform attributeName="transform" type="translate" values="0 0; 40 -18; 0 0" dur="18s" repeatCount="indefinite"/>
    </circle>

    <!-- monogram halkası -->
    <g transform="translate(1078 200)">
      <circle r="142" fill="none" stroke="#ff7a2a" stroke-opacity=".28" stroke-dasharray="2 10">
        <animateTransform attributeName="transform" type="rotate" from="360" to="0" dur="60s" repeatCount="indefinite"/>
      </circle>
      <circle r="118" fill="none" stroke="{t['border']}" stroke-width="2"/>
      <circle r="118" fill="none" stroke="url(#accent)" stroke-width="4" stroke-linecap="round" stroke-dasharray="190 552">
        <animateTransform attributeName="transform" type="rotate" from="0" to="360" dur="9s" repeatCount="indefinite"/>
      </circle>
      <circle r="98" fill="{t['panel']}" stroke="{t['border']}"/>
      <text y="23" text-anchor="middle" font-family="{SANS}" font-size="66" font-weight="800" letter-spacing="-2" fill="url(#name)">FH</text>
    </g>

    <text x="80" y="116" font-family="{MONO}" font-size="17" letter-spacing="3" fill="#ff8a3d">// MERHABA, BEN</text>
    <text x="76" y="192" font-family="{SANS}" font-size="66" font-weight="800" letter-spacing="-1.5" fill="url(#name)">Ferhat Hacıosmanoğlu</text>
    <text x="80" y="240" font-family="{SANS}" font-size="25" fill="{t['muted']}">Mekatronik Mühendisi  ·  PWA &amp; İş Uygulamaları Geliştirici</text>

    <g transform="translate(80 284)">
      <rect width="{box_w}" height="48" rx="12" fill="{t['panel2']}" stroke="{t['border']}"/>
      <text x="20" y="31" font-family="{MONO}" font-size="{fs}" font-weight="700" fill="#ff7a2a">$</text>
      <g clip-path="url(#typing)">
        <text x="{text_x}" y="31" font-family="{MONO}" font-size="{fs}" fill="{t['text']}">{escape(line)}</text>
      </g>
      <rect x="{text_x + 2}" y="14" width="10" height="21" rx="2" fill="#ff7a2a">
        <animate attributeName="x" values="{x_values}" keyTimes="{kt}" dur="3.2s" begin="0.6s" calcMode="discrete" fill="freeze"/>
        <animate attributeName="opacity" values="1;1;0;0" keyTimes="0;.5;.5;1" dur="1s" repeatCount="indefinite"/>
      </rect>
    </g>

    <rect y="{H - 4}" width="{W}" height="4" fill="url(#accent)"/>
  </g>
</svg>
"""


# ----------------------------------------------------------------- proje kartı
CARD_W, CARD_H, PAD = 520, 280, 28


def pill_width(label: str, fs: float = 13.5) -> float:
    return len(label) * fs * MONO_W + 22


def project_card(p: dict, theme: str) -> str:
    t = THEMES[theme]
    W, H = CARD_W, CARD_H
    uid = p["slug"] + theme
    live = p["status"] == "CANLI"
    c_bg, c_st, c_tx = (t["live_bg"], t["live_stroke"], t["live_text"]) if live else (t["tag_bg"], t["tag_stroke"], t["tag_text"])
    chip_fs = 12
    chip_w = len(p["status"]) * (chip_fs * MONO_W + 1.4) + (42 if live else 28)
    chip_x = W - PAD - chip_w
    dot = (f'<circle cx="{chip_x + 16:.1f}" cy="48" r="4" fill="{c_tx}">'
           f'<animate attributeName="opacity" values="1;.35;1" dur="2s" repeatCount="indefinite"/></circle>') if live else ""
    chip_tx = chip_x + (28 if live else 14)

    lines = wrap(p["desc"], 47)
    if len(lines) > 3:
        raise SystemExit(f"'{p['slug']}' açıklaması 3 satıra sığmıyor, kısaltın.")
    desc = "".join(
        f'<text x="{PAD}" y="{130 + i * 27}" font-family="{SANS}" font-size="18" fill="{t["desc"]}">{escape(l)}</text>'
        for i, l in enumerate(lines)
    )

    pills, x = [], float(PAD)
    for tag in p["tags"]:
        w = pill_width(tag)
        if x + w > W - PAD - 44:
            break
        pills.append(
            f'<rect x="{x:.1f}" y="220" width="{w:.1f}" height="32" rx="9" fill="{t["pill_bg"]}" stroke="{t["pill_stroke"]}"/>'
            f'<text x="{x + 11:.1f}" y="241" font-family="{MONO}" font-size="13.5" fill="{t["pill_text"]}">{escape(tag)}</text>'
        )
        x += w + 8

    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-labelledby="t{uid} d{uid}">
  <title id="t{uid}">{escape(p['title'])}</title>
  <desc id="d{uid}">{escape(p['desc'])}</desc>
  <defs>{defs_common(uid)}
    <clipPath id="clip{uid}"><rect x="1" y="1" width="{W - 2}" height="{H - 2}" rx="20"/></clipPath>
    <radialGradient id="glow{uid}" cx="100%" cy="0%" r="75%">
      <stop offset="0" stop-color="#ff7a2a" stop-opacity="{t['glow_op']}"/><stop offset="1" stop-color="#ff7a2a" stop-opacity="0"/>
    </radialGradient>
  </defs>
  <g clip-path="url(#clip{uid})">
    <rect width="{W}" height="{H}" fill="{t['panel']}"/>
    <rect width="{W}" height="{H}" fill="url(#glow{uid})"/>
    <rect y="0" width="{W}" height="3" fill="url(#accent{uid})"/>
  </g>
  <rect x="1" y="1" width="{W - 2}" height="{H - 2}" rx="20" fill="none" stroke="{t['border']}" stroke-width="1.5"/>

  <rect x="{PAD}" y="28" width="52" height="52" rx="14" fill="url(#icon{uid})"/>
  <g transform="translate({PAD + 14} 42)" fill="none" stroke="#ffffff" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">{ICONS[p['icon']]}</g>

  <text x="{PAD + 68}" y="52" font-family="{SANS}" font-size="23" font-weight="700" fill="{t['text']}">{escape(p['title'])}</text>
  <text x="{PAD + 68}" y="75" font-family="{SANS}" font-size="15" fill="{t['muted']}">{escape(p['sub'])}</text>

  <rect x="{chip_x:.1f}" y="34" width="{chip_w:.1f}" height="28" rx="14" fill="{c_bg}" stroke="{c_st}"/>
  {dot}
  <text x="{chip_tx:.1f}" y="52.5" font-family="{MONO}" font-size="{chip_fs}" font-weight="700" letter-spacing="1.4" fill="{c_tx}">{escape(p['status'])}</text>

  {desc}
  {''.join(pills)}

  <g transform="translate({W - PAD - 22} 225)" fill="none" stroke="{t['muted']}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
    <path d="M3 19L19 3M8 3h11v11"/>
  </g>
</svg>
"""


# ----------------------------------------------------------------- iletişim düğmesi
def button(uid: str, label: str, icon: str) -> str:
    """Her iki temada da okunur, koyu düğme."""
    fs = 17
    W = int(len(label) * fs * 0.56 + 88)
    H = 52
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="{escape(label)}">
  <defs>{defs_common(uid)}</defs>
  <rect x="1" y="1" width="{W - 2}" height="{H - 2}" rx="14" fill="#111111" stroke="#2a2a2a" stroke-width="1.5"/>
  <rect x="8" y="8" width="36" height="36" rx="10" fill="url(#icon{uid})"/>
  <g transform="translate(14 14)" fill="none" stroke="#ffffff" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">{ICONS[icon]}</g>
  <text x="58" y="32.5" font-family="{SANS}" font-size="{fs}" font-weight="600" fill="#fafafa">{escape(label)}</text>
</svg>
"""


PROJECTS = [
    dict(slug="isform", icon="clipboard", status="AKTİF",
         title="ENORPA İş Formları", sub="Servis ve bakım yönetimi · PWA",
         desc="Servis formları, firma kartları, bakım takibi, harita destekli raporlar ve Gemini destekli asistan.",
         tags=["JavaScript", "Vite", "Firebase", "Gemini", "PWA"]),
    dict(slug="saha-raporu", icon="camera", status="CANLI",
         title="Dijital Saha Raporu", sub="ENORPA · Saha ziyareti raporlama",
         desc="Saha ziyaretlerini fotoğraflı raporlara dönüştürür; PDF dışa aktarma ve otomatik kayıtlı taslaklarla çevrimdışı çalışır.",
         tags=["Next.js", "React 19", "TypeScript", "Tailwind"]),
    dict(slug="brulor", icon="flame", status="PWA",
         title="Brülör Kontrol", sub="ENORPA · Brülör seçim ve kontrol",
         desc="Marka › seri › model seçimi, katalog ölçüleri ve teknik çizimli PDF rapor. Yakıt tipine göre kontrol listeleri.",
         tags=["JavaScript", "Firebase", "PDF", "Offline"]),
    dict(slug="ferconvert", icon="file", status="CANLI",
         title="FERCONVERT", sub="Gizlilik odaklı belge çalışma alanı",
         desc="PDF birleştirme ve düzenleme, QR, görsel ve veri araçları tamamen tarayıcıda; dosyalar sunucuya yüklenmez.",
         tags=["JavaScript", "pdf-lib", "PDF.js", "PWA"]),
    dict(slug="baron", icon="calendar", status="MASAÜSTÜ",
         title="BARON", sub="Ders programı · Web + Windows",
         desc="Öğretmen, sınıf ve ders dağıtımlarından çakışmasız haftalık program üretir. Bulut senkronu ve Windows sürümü.",
         tags=["Firebase", "Tauri v2", "GitHub Actions"]),
    dict(slug="effeyc", icon="grid", status="CANLI",
         title="effeyc", sub="Uygulamalar portfolyosu",
         desc="Günlük hayatı kolaylaştıran uygulamalarımın vitrini. Liquid Glass tasarım dili ve koyu / açık / loş tema.",
         tags=["React 19", "TypeScript", "Tailwind", "Cloudflare"]),
]

BUTTONS = [
    ("btn-portfolio", "Portfolyo", "globe"),
    ("btn-linkedin", "LinkedIn", "briefcase"),
    ("btn-email", "E-posta", "mail"),
    ("btn-card", "Dijital Kartvizit", "idcard"),
]


def main() -> None:
    for theme in THEMES:
        (OUT / f"banner-{theme}.svg").write_text(banner(theme), encoding="utf-8")
        for p in PROJECTS:
            (OUT / f"card-{p['slug']}-{theme}.svg").write_text(project_card(p, theme), encoding="utf-8")
    for name, label, icon in BUTTONS:
        (OUT / f"{name}.svg").write_text(button(name.replace("-", ""), label, icon), encoding="utf-8")
    print(f"{len(list(OUT.glob('*.svg')))} SVG üretildi → {OUT}")


if __name__ == "__main__":
    main()
