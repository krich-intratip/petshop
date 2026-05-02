"""
Unified seed script — creates ALL categories, products, blog posts, FAQs,
authors and downloads images from Unsplash.

Safe to run multiple times (idempotent via get_or_create + slug).

Usage:
    python manage.py shell -c "exec(open('scripts/seed_all.py', encoding='utf-8').read())"
"""
import os
import urllib.request
from decimal import Decimal

import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mysite.settings")
django.setup()

from django.conf import settings
from django.core.files import File

from blog.models import Author, Post
from products.models import Category, FAQ, Product

LINE = getattr(settings, "LINE_ORDER_URL", "https://line.me/R/ti/p/@Dr.peakmaker")
TMP = os.path.join(settings.MEDIA_ROOT, "_tmp_import")
os.makedirs(TMP, exist_ok=True)

UA = "Mozilla/5.0 (compatible; PetshopSeed/1.0)"


def fetch(url: str, dest: str) -> None:
    os.makedirs(os.path.dirname(dest), exist_ok=True)
    if os.path.isfile(dest) and os.path.getsize(dest) > 3000:
        return
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=90) as resp:
        data = resp.read()
    if len(data) < 2000:
        raise RuntimeError(f"Download too small: {url}")
    with open(dest, "wb") as f:
        f.write(data)
    print("  DL", os.path.basename(dest))


def save_img(obj, field: str, tmp_name: str, upload_name: str) -> None:
    src = os.path.join(TMP, tmp_name)
    with open(src, "rb") as f:
        getattr(obj, field).save(upload_name, File(f), save=True)


# fmt: off
DOWNLOADS = [
    ("_cat_litter_box.jpg",    "https://images.unsplash.com/photo-1727510153658-643787acb16a?w=1400&q=85&auto=format&fit=crop"),
    ("_cat_litter_granules.jpg","https://images.unsplash.com/photo-1724080241975-943438470755?w=1400&q=85&auto=format&fit=crop"),
    ("_cat_litter_sand.jpg",   "https://images.unsplash.com/photo-1614587469816-65f010b9d179?w=1400&q=85&auto=format&fit=crop"),
    ("_cat_litter_wet.jpg",    "https://images.unsplash.com/photo-1599760121427-118bed4a10a5?w=1400&q=85&auto=format&fit=crop"),
    ("_cat_litter_fine.jpg",   "https://images.unsplash.com/photo-1758467614651-02bad4840a42?w=1400&q=85&auto=format&fit=crop"),
    ("_cat_litter_silica.jpg", "https://images.unsplash.com/photo-1672090630681-e69da8006146?w=1400&q=85&auto=format&fit=crop"),
    ("_cat_litter_wood.jpg",   "https://images.unsplash.com/photo-1737202294763-4f5d087d139c?w=1400&q=85&auto=format&fit=crop"),
    ("_cat_litter_tofu.jpg",   "https://images.unsplash.com/photo-1639843606783-b2f9c50a7468?w=1400&q=85&auto=format&fit=crop"),
    ("_cat_litter_paper.jpg",  "https://images.unsplash.com/photo-1715522594847-67c90b5b8667?w=1400&q=85&auto=format&fit=crop"),
    ("_cat_litter_corn.jpg",   "https://images.unsplash.com/photo-1668350102568-d998ada9af9c?w=1400&q=85&auto=format&fit=crop"),
    ("_cat_litter_charcoal.jpg","https://images.unsplash.com/photo-1734415646846-c64d73f9f4f3?w=1400&q=85&auto=format&fit=crop"),
    ("_cat_blog_litter.jpg",   "https://images.unsplash.com/photo-1513360371669-4adf3dd7dff8?w=1400&q=85&auto=format&fit=crop"),

    ("_dry_kibble1.jpg",       "https://images.unsplash.com/photo-1764249453874-46864677b10e?w=1400&q=85&auto=format&fit=crop"),
    ("_dry_cat_bowl.jpg",      "https://images.unsplash.com/photo-1764576504536-dbdfa4cb1d9a?w=1400&q=85&auto=format&fit=crop"),
    ("_dry_cat_eating.jpg",    "https://images.unsplash.com/photo-1558993457-4bc6ec2c3734?w=1400&q=85&auto=format&fit=crop"),
    ("_dry_bowl_close.jpg",    "https://images.unsplash.com/photo-1695169954725-fa757fd7315c?w=1400&q=85&auto=format&fit=crop"),
    ("_dry_kibble2.jpg",       "https://images.unsplash.com/photo-1764249453850-faace6e57444?w=1400&q=85&auto=format&fit=crop"),
    ("_dry_p1.jpg",            "https://images.unsplash.com/photo-1583337130417-3346a1be7dee?w=1400&q=85&auto=format&fit=crop"),
    ("_dry_p2.jpg",            "https://images.unsplash.com/photo-1526336024174-e58f5cdd8e13?w=1400&q=85&auto=format&fit=crop"),
    ("_dry_p3.jpg",            "https://images.unsplash.com/photo-1583337130417-3346a1be7dee?w=1400&q=85&auto=format&fit=crop"),
    ("_dry_blog1.jpg",         "https://images.unsplash.com/photo-1558993457-4bc6ec2c3734?w=1400&q=85&auto=format&fit=crop"),
    ("_dry_blog2.jpg",         "https://images.unsplash.com/photo-1596854331442-3cf47265cefb?w=1400&q=85&auto=format&fit=crop"),

    ("_wet_food1.jpg",         "https://images.unsplash.com/photo-1526336024174-e58f5cdd8e13?w=1400&q=85&auto=format&fit=crop"),
    ("_wet_food2.jpg",         "https://images.unsplash.com/photo-1583337130417-3346a1be7dee?w=1400&q=85&auto=format&fit=crop"),
    ("_wet_food3.jpg",         "https://images.unsplash.com/photo-1526336024174-e58f5cdd8e13?w=1400&q=85&auto=format&fit=crop"),
    ("_wet_cat_hero.jpg",      "https://images.unsplash.com/photo-1526336024174-e58f5cdd8e13?w=1400&q=85&auto=format&fit=crop"),
    ("_wet_blog1.jpg",         "https://images.unsplash.com/photo-1526336024174-e58f5cdd8e13?w=1400&q=85&auto=format&fit=crop"),
    ("_wet_blog2.jpg",         "https://images.unsplash.com/photo-1596854331442-3cf47265cefb?w=1400&q=85&auto=format&fit=crop"),

    ("_lick_pouch.jpg",        "https://images.unsplash.com/photo-1750279785829-1369c41e8db2?w=1400&q=85&auto=format&fit=crop"),
    ("_lick_stick.jpg",        "https://images.unsplash.com/photo-1750279785897-ba67fd35dde1?w=1400&q=85&auto=format&fit=crop"),
    ("_lick_liquid.jpg",       "https://images.unsplash.com/photo-1603451757941-b11957205f69?w=1400&q=85&auto=format&fit=crop"),
    ("_lick_blog.jpg",         "https://images.unsplash.com/photo-1750279785829-1369c41e8db2?w=1400&q=85&auto=format&fit=crop"),

    ("_supp_vet.jpg",          "https://images.unsplash.com/photo-1725409796872-8b41e8eca929?w=1400&q=85&auto=format&fit=crop"),
    ("_supp_fish_oil.jpg",     "https://images.unsplash.com/photo-1603451757941-b11957205f69?w=1400&q=85&auto=format&fit=crop"),
    ("_supp_omega_caps.jpg",   "https://images.unsplash.com/photo-1765603732941-1a839b7f1d44?w=1400&q=85&auto=format&fit=crop"),
    ("_supp_pills.jpg",        "https://images.unsplash.com/photo-1596854331442-3cf47265cefb?w=1400&q=85&auto=format&fit=crop"),
    ("_supp_bottles.jpg",      "https://images.unsplash.com/photo-1749388930163-30e2eb45f86d?w=1400&q=85&auto=format&fit=crop"),
    ("_supp_omega_bottle.jpg", "https://images.unsplash.com/photo-1750279785829-1369c41e8db2?w=1400&q=85&auto=format&fit=crop"),
    ("_supp_blog.jpg",         "https://images.unsplash.com/photo-1596854331442-3cf47265cefb?w=1400&q=85&auto=format&fit=crop"),

    ("_author_vet.jpg",        "https://images.unsplash.com/photo-1725409796872-8b41e8eca929?w=400&q=85&auto=format&fit=crop"),
]
# fmt: on

print("=== Downloading images ===")
for fname, url in DOWNLOADS:
    fetch(url, os.path.join(TMP, fname))

# ── Author ──
print("\n=== Seeding Author ===")
author, _ = Author.objects.get_or_create(
    name="Dr.Meaw",
    defaults={"bio": "สัตวแพทย์และที่ปรึกษาด้านโภชนาการแมว"},
)

# ── Categories ──
print("\n=== Seeding Categories ===")
CATS = [
    {
        "slug": "cat-litter",
        "name": "ทรายแมว",
        "desc": "ทรายแมวทุกประเภท จับก้อน ซิลิกา เม็ดไม้ ท้อฟู กระดาษรีไซเคิล และข้าวโพด เลือกให้เหมาะกับไลฟ์สไตล์แมว",
        "img": ("_cat_litter_box.jpg", "cat-litter-category-hero.jpg"),
    },
    {
        "slug": "dry-cat-food",
        "name": "อาหารแมวชนิดเม็ด",
        "desc": "อาหารเม็ดคุณภาพ สูตรแซลมอน ไร้ธัญพืช ลดก้อนขน แมวสูงวัย และควบคุมน้ำหนัก",
        "img": ("_dry_kibble1.jpg", "dry-cat-food-kibble_MxS7CzB.jpg"),
    },
    {
        "slug": "wet-cat-food",
        "name": "อาหารแมวชนิดเปียก",
        "desc": "อาหารเปียกแมว ซอส เจลลี่ และเปียเต่ ช่วยเสริมน้ำสำหรับแมวที่ดื่มน้ำน้อย",
        "img": ("_wet_cat_hero.jpg", "wet-cat-food_Dr2VeAa.jpg"),
    },
    {
        "slug": "cat-lick-treats",
        "name": "ขนมแมวเลีย",
        "desc": "ขนมเลียรสชาติอร่อย ทูน่า ไก่ ตับ ใช้เป็นรางวัลหรือเสริมน้ำให้แมว",
        "img": ("_lick_pouch.jpg", "cat-lick-treats-hero.jpg"),
    },
    {
        "slug": "cat-supplements",
        "name": "อาหารเสริมแมว",
        "desc": "วิตามิน โอเมก้า โปรไบโอติก และเกลือแร่เสริมสุขภาพแมว ใช้เสริมจากอาหารหลักตามคำแนะนำสัตวแพทย์",
        "img": ("_supp_vet.jpg", "category-cat-supplements.jpg"),
    },
]

cat_map = {}
for c in CATS:
    obj, _ = Category.objects.get_or_create(
        slug=c["slug"],
        defaults={"name": c["name"], "description": c["desc"]},
    )
    obj.description = c["desc"]
    obj.save()
    save_img(obj, "image", c["img"][0], c["img"][1])
    cat_map[c["slug"]] = obj
    print(f"  Category: {obj.slug}")

# ── Products ──
print("\n=== Seeding Products ===")

PRODUCTS = [
    # ── ทรายแมว ──
    {"slug": "cat-litter-clumping-10kg", "cat": "cat-litter", "name": "ทรายแมวจับก้อน 10 กก.", "price": Decimal("259.00"), "desc": "ทรายดินเหนียวจับก้อนแน่น ขจัดกลิ่นได้ดี เปลี่ยนง่าย", "body": "<p>เหมาะสำหรับบ้านที่เลี้ยงแมวหลายตัว เก็บในที่แห้ง</p>", "img": ("_cat_litter_granules.jpg", "litter-clumping-granules.jpg")},
    {"slug": "cat-litter-natural-8kg", "cat": "cat-litter", "name": "ทรายแมวธรรมชาติ 8 กก.", "price": Decimal("199.00"), "desc": "ทรายธรรมชาติฝุ่นน้อย เหมาะแมวแพ้ฝุ่นและระบบทางเดินหายใจ", "body": "<p>ใช้ถุงซับใต้ถาดเพื่อความสะอาด</p>", "img": ("_cat_litter_sand.jpg", "litter-natural-sand.jpg")},
    {"slug": "cat-litter-light-5kg", "cat": "cat-litter", "name": "ทรายแมวน้ำหนักเบา 5 กก.", "price": Decimal("219.00"), "desc": "ดูดซับเร็ว น้ำหนักเบา ยกขนย้ายสะดวก", "body": "<p>เปลี่ยนทุก 1-2 สัปดาห์ตามจำนวนแมว</p>", "img": ("_cat_litter_wet.jpg", "litter-light-absorb.jpg")},
    {"slug": "cat-litter-premium-clump-8kg", "cat": "cat-litter", "name": "ทรายแมวพรีเมียมจับก้อนละเอียด 8 กก.", "price": Decimal("329.00"), "desc": "เม็ดละเอียดพิเศษ จับก้อนแน่น ไม่ติดก้นถาด", "body": "<p>เติมทรายใหม่ทับบนหลังตักก้อนออก</p>", "img": ("_cat_litter_fine.jpg", "litter-premium-fine.jpg")},
    {"slug": "cat-litter-silica-4kg", "cat": "cat-litter", "name": "ทรายแมวซิลิก้าเจล 4 กก.", "price": Decimal("289.00"), "desc": "เม็ดซิลิก้าดูดความชื้นและกลิ่นได้ดีเยี่ยม ไม่ต้องตักก้อน", "body": "<p>เปลี่ยนทั้งถาดเมื่อเม็ดเปลี่ยนสี ประมาณ 2-4 สัปดาห์</p>", "img": ("_cat_litter_silica.jpg", "litter-silica-crystals.jpg")},
    {"slug": "cat-litter-pine-5kg", "cat": "cat-litter", "name": "ทรายแมวเม็ดไม้สน 5 กก.", "price": Decimal("179.00"), "desc": "เม็ดไม้สนธรรมชาติ ย่อยสลายได้ กลิ่นไม้สนอ่อน", "body": "<p>เหมาะสำหรับบ้านที่ต้องการผลิตภัณฑ์เป็นมิตรกับสิ่งแวดล้อม</p>", "img": ("_cat_litter_wood.jpg", "litter-pine-pellets.jpg")},
    {"slug": "cat-litter-tofu-6kg", "cat": "cat-litter", "name": "ทรายแมวท้อฟู 6 กก.", "price": Decimal("279.00"), "desc": "ทรายจากเต้าหู้ จับก้อนได้ ย่อยสลายทิ้งลงโถส้วมได้", "body": "<p>ใส่ทีละน้อยในโถส้วมเพื่อป้องกันการอุดตัน</p>", "img": ("_cat_litter_tofu.jpg", "litter-tofu-pellets.jpg")},
    {"slug": "cat-litter-paper-5kg", "cat": "cat-litter", "name": "ทรายแมวกระดาษรีไซเคิล 5 กก.", "price": Decimal("289.00"), "desc": "ทรายจากกระดาษรีไซเคิล น้ำหนักเบา ฝุ่นน้อย เหมาะแมวแพ้ฝุ่น", "body": "<p>เม็ดกระดาษดูดซับความชื้นได้ดี เปลี่ยนทรายเป็นประจำ</p>", "img": ("_cat_litter_paper.jpg", "litter-recycled-paper.jpg")},
    {"slug": "cat-litter-corn-4kg", "cat": "cat-litter", "name": "ทรายแมวธัญพืช (ข้าวโพด) 4 กก.", "price": Decimal("319.00"), "desc": "ทรายจากแป้งข้าวโพดธรรมชาติ จับก้อนได้ กลิ่นอ่อน", "body": "<p>วัสดุจากพืช ลดผลกระทบต่อสิ่งแวดล้อม เก็บในที่แห้งปิดมิดชิด</p>", "img": ("_cat_litter_corn.jpg", "litter-corn-based.jpg")},
    {"slug": "cat-litter-charcoal-10kg", "cat": "cat-litter", "name": "ทรายแมวเบนทonite ผสมถ่านกัมมัน 10 กก.", "price": Decimal("359.00"), "desc": "เม็ดดินเหนียวจับก้อนแน่น ผสมถ่านกัมมันช่วยดูดกลิ่น เหมาะใช้หลายแมว", "body": "<p>เหมาะสำหรับผู้ที่ต้องการควบคุมกลิ่นในคอนโดหรือห้องแคบ</p>", "img": ("_cat_litter_charcoal.jpg", "litter-bentonite-charcoal.jpg")},

    # ── อาหารเม็ด ──
    {"slug": "dry-food-salmon-rice-2kg", "cat": "dry-cat-food", "name": "อาหารแมวเม็ด แซลมอนและข้าว 2 กก.", "price": Decimal("429.00"), "desc": "โปรตีนปลาแซลมอน รสชาติถูกปากแมวส่วนใหญ่ เม็ดพอดีคำ เคี้ยวง่าย", "body": "<p>เหมาะแมวโตที่ไม่แพ้อาหารทะเล แบ่งให้ตามคำแนะนำบนฉลาก</p>", "img": ("_dry_kibble1.jpg", "dry-salmon-rice.jpg")},
    {"slug": "dry-food-indoor-weight-1-5kg", "cat": "dry-cat-food", "name": "อาหารแมวเม็ด แมวในบ้าน ควบคุมน้ำหนัก 1.5 กก.", "price": Decimal("399.00"), "desc": "พลังงานพอเหมาะกับแมวขี้เกียจ ลดความเสี่ยงอ้วนเมื่อใช้ร่วมการควบคุมมื้อ", "body": "<p>แนะนำชั่งน้ำหนักเป็นระยะ ปรับปริมาณตามกิจกรรม</p>", "img": ("_dry_cat_bowl.jpg", "dry-indoor-weight.jpg")},
    {"slug": "dry-food-hairball-2kg", "cat": "dry-cat-food", "name": "อาหารแมวเม็ด ลดก้อนขน 2 กก.", "price": Decimal("459.00"), "desc": "สูตรช่วยระบบขับถ่ายและขน แมวฟีล์นยาวหรือเลียขนบ่อย", "body": "<p>ใช้ร่วมการหวีขนเป็นประจำ ดื่มน้ำให้เพียงพอ</p>", "img": ("_dry_cat_eating.jpg", "dry-hairball.jpg")},
    {"slug": "dry-food-senior-2kg", "cat": "dry-cat-food", "name": "อาหารแมวเม็ด แมวสูงวัย 7+ ปี 2 กก.", "price": Decimal("479.00"), "desc": "เม็ดนุ่มขึ้น โปรตีนคุณภาพ สารประกอบสำหรับแมววัยเก๋า", "body": "<p>หากมีโรคไตหรือข้อควรปรึกษาสัตวแพทย์ก่อนเปลี่ยนสูตร</p>", "img": ("_dry_bowl_close.jpg", "dry-senior.jpg")},
    {"slug": "dry-food-grain-free-duck-1-8kg", "cat": "dry-cat-food", "name": "อาหารแมวเม็ด ไร้ธัญพืช เนื้อเป็ด 1.8 กก.", "price": Decimal("519.00"), "desc": "โปรตีนเป็ดเป็นหลัก เหมาะแมวแพ้บางชนิดของธัญพืช", "body": "<p>เปลี่ยนสูตรค่อยเป็นค่อยไป 7-10 วัน</p>", "img": ("_dry_kibble2.jpg", "dry-grain-free-duck.jpg")},

    # ── อาหารเปียก ──
    {"slug": "wet-pouch-tuna", "cat": "wet-cat-food", "name": "อาหารแมวเปียก ซอสทูน่า 85 ก.", "price": Decimal("35.00"), "desc": "ซองซอสทูน่า แมวชอบ เสริมน้ำสำหรับแมวดื่มน้ำน้อย", "body": "<p>เปิดแล้วควรให้หมดภายในมื้อ</p>", "img": ("_wet_food1.jpg", "wet-pouch-tuna_EDDY2DZ.jpg")},
    {"slug": "wet-tray-chicken", "cat": "wet-cat-food", "name": "อาหารแมวเปียก เจลลี่ไก่ 100 ก.", "price": Decimal("39.00"), "desc": "ถาดเจลลี่ไก่ เนื้อชิ้นใหญ่ กลิ่นหอม", "body": "<p>เหมาะแมวที่ชอบเคี้ยวเนื้อชิ้น</p>", "img": ("_wet_food2.jpg", "wet-tray-chicken_lxCXEhE.jpg")},
    {"slug": "wet-pate-senior", "cat": "wet-cat-food", "name": "อาหารแมวเปียก เปียเต่ แมวสูงวัย 85 ก.", "price": Decimal("45.00"), "desc": "เปียเต่นุ่ม ง่ายต่อการเคี้ยว สูตรแมวสูงวัย 7+ ปี", "body": "<p>เหมาะแมวสูงวัยที่เคี้ยวลำบาก</p>", "img": ("_wet_food3.jpg", "wet-pate-senior_uPLqEwW.jpg")},

    # ── ขนมแมวเลีย ──
    {"slug": "lick-treat-tuna-4", "cat": "cat-lick-treats", "name": "ขนมเลียแมว รสทูน่า 4 แท่ง", "price": Decimal("59.00"), "desc": "ขนมเลียรสทูน่า ใช้เป็นรางวัลหรือเสริมน้ำ", "body": "<p>ไม่ควรให้เกิน 10% ของแคลอรี่ต่อวัน</p>", "img": ("_lick_pouch.jpg", "lick-treat-tuna.jpg")},
    {"slug": "lick-treat-chicken-6", "cat": "cat-lick-treats", "name": "ขนมเลียแมว รสไก่ 6 แท่ง", "price": Decimal("79.00"), "desc": "ขนมเลียรสไก่ กลิ่นหอม แมวชอบ", "body": "<p>กดออกจากแท่งให้แมวเลียหรือบีบลงจาน</p>", "img": ("_lick_stick.jpg", "lick-treat-chicken.jpg")},
    {"slug": "lick-treat-liver-6", "cat": "cat-lick-treats", "name": "ขนมเลียแมว รสตับ 6 แท่ง", "price": Decimal("79.00"), "desc": "ขนมเลียรสตับ โปรตีนสูง เสริมสารอาหาร", "body": "<p>เหมาะเป็นรางวัลฝึกพฤติกรรม</p>", "img": ("_lick_liquid.jpg", "lick-treat-liver.jpg")},

    # ── อาหารเสริม ──
    {"slug": "supp-omega3-oil-100ml", "cat": "cat-supplements", "name": "น้ำมันปลา Omega-3 สำหรับแมว 100 มล.", "price": Decimal("289.00"), "desc": "กรดไขมัน EPA/DHA ช่วยบำรุงผิวหนังและขน หยดผสมอาหาร", "body": "<p>เก็บในที่เย็น หลีกเลี่ยงแสง เริ่มจากปริมาณน้อยแล้วสังเกตการย่อย</p>", "img": ("_supp_fish_oil.jpg", "supp-omega3-oil.jpg")},
    {"slug": "supp-omega3-caps-60", "cat": "cat-supplements", "name": "แคปซูล Omega-3 สำหรับแมว 60 เม็ด", "price": Decimal("349.00"), "desc": "แคปซูลแบ่งฉีดผสมอาหารหรือตามวิธีใช้บนฉลาก", "body": "<p>ไม่แนะนำให้แมวกลืนทั้งเม็ดโดยไม่เจาะ</p>", "img": ("_supp_omega_caps.jpg", "supp-omega3-caps.jpg")},
    {"slug": "supp-multivitamin-chew-90", "cat": "cat-supplements", "name": "วิตามินรวมแมว แบบเคี้ยว 90 เม็ด", "price": Decimal("269.00"), "desc": "วิตามินและเกลือแร่เบื้องต้นเสริมจากอาหารหลัก", "body": "<p>ไม่ใช่ยารักษาโรค ห้ามเกินปริมาณแนะนำต่อวัน</p>", "img": ("_supp_pills.jpg", "supp-multivitamin.jpg")},
    {"slug": "supp-probiotic-powder-30", "cat": "cat-supplements", "name": "โปรไบโอติกผงสำหรับแมว 30 ซอง", "price": Decimal("319.00"), "desc": "จุลินทรีย์ช่วยสนับสนุนลำไส้ ผสมอาหารเปียกหรือเม็ด", "body": "<p>แมวป่วยฉับพลันหรือภูมิคุ้มกันต่ำควรปรึกษาหมอก่อน</p>", "img": ("_supp_bottles.jpg", "supp-probiotic.jpg")},
    {"slug": "supp-taurine-liquid-50ml", "cat": "cat-supplements", "name": "ทอรีนน้ำสำหรับแมว 50 มล.", "price": Decimal("199.00"), "desc": "กรดอะมิโนสำคัญต่อหัวใจและสายตาแมว หยดผสมอาหาร", "body": "<p>แมวกินอาหารสมดุลมักได้ทอรีนเพียงพอ — ใช้เสริมเมื่อมีเหตุผลทางการแพทย์</p>", "img": ("_supp_omega_bottle.jpg", "supp-taurine-liquid.jpg")},
]

for row in PRODUCTS:
    p, created = Product.objects.get_or_create(
        slug=row["slug"],
        defaults={
            "category": cat_map[row["cat"]],
            "name": row["name"],
            "description": row["desc"],
            "body": row["body"],
            "price": row["price"],
            "available": True,
            "line_contact_link": LINE,
        },
    )
    if not created:
        p.category = cat_map[row["cat"]]
        p.name = row["name"]
        p.description = row["desc"]
        p.body = row["body"]
        p.price = row["price"]
        p.line_contact_link = LINE
        p.save()
    save_img(p, "image", row["img"][0], row["img"][1])
    print(f"  Product: {p.slug} {'(new)' if created else '(updated)'}")

# ── Blog Posts ──
print("\n=== Seeding Blog Posts ===")

POSTS = [
    {
        "slug": "cat-litter-types-guide",
        "title": "คู่มือเลือกทรายแมว 10 ประเภท: ข้อดีข้อเสียแบบเปรียบเทียบ",
        "desc": "ทรายดินเหนียว ซิลิก้า เม็ดไม้ ท้อฟู กระดาษ ข้าวโพด — แบบไหนเหมาะกับแมวคุณ?",
        "body": """<h2>ทำไมทรายแมวสำคัญ</h2>
<p>แมวใช้เวลาในถาดทรายวันละหลายครั้ง ทรายที่ไม่เหมาะอาจทำให้แมวไม่ยอมถ่ายในถาด ส่งผลต่อสุขภาพทางเดินปัสสาวะและพฤติกรรม</p>
<h2>เปรียบเทียบ 10 ประเภททรายแมวยอดนิยม</h2>
<ol>
<li><strong>ดินเหนียวจับก้อน</strong> — จับก้อนแน่น ตักง่าย แต่ฝุ่นมาก</li>
<li><strong>ดินเหนียวไม่จับก้อน</strong> — ราคาถูก แต่ต้องเปลี่ยนทั้งถาดบ่อย</li>
<li><strong>ซิลิก้าเจล</strong> — ดูดกลิ่นดีเยี่ยม ไม่ต้องตักก้อน แต่ราคาสูง</li>
<li><strong>เม็ดไม้สน</strong> — ธรรมชาติ ฝุ่นน้อย แต่บางแมวไม่ชอบเหยียบ</li>
<li><strong>ท้อฟู</strong> — ย่อยสลาย ทิ้งลงโถส้วมได้ แต่บางสูตรจับก้อนไม่แน่น</li>
<li><strong>กระดาษรีไซเคิล</strong> — ฝุ่นน้อย เบา แต่ดูดกลิ่นไม่ดีเท่าดินเหนียว</li>
<li><strong>ข้าวโพด</strong> — จับก้อนได้ ธรรมชาติ แต่ราคาสูงกว่าดินเหนียว</li>
<li><strong>ถั่วเหลือง</strong> — คล้ายท้อฟู โปรตีนสูง</li>
<li><strong>เปลือกถั่ว</strong> — วัสดุรีไซเคิล ฝุ่นน้อย</li>
<li><strong>ผสมถ่านกัมมัน</strong> — ดูดกลิ่นดีเพิ่ม แต่เปื้อนเทแมวได้</li>
</ol>
<h2>สรุป: แบบไหนเหมาะกับคุณ?</h2>
<p>คอนโด/ห้องแคบ → ซิลิก้า หรือผสมถ่าน | แมวแพ้ฝุ่น → กระดาษ หรือเม็ดไม้ | งบจำกัด → ดินเหนียวจับก้อน | เน้นสิ่งแวดล้อม → ท้อฟู ข้าวโพด</p>""",
        "img": ("_cat_blog_litter.jpg", "blog-litter-types_mvxlV03.jpg"),
        "cats": ["cat-litter"],
    },
    {
        "slug": "wet-cat-food-life-stage",
        "title": "อาหารเปียกแมวทุกช่วงวัย: เลือกอย่างไรให้ถูกต้อง",
        "desc": "ซอส เจลลี่ เปียเต่ — แมวลูก โต สูงวัย ต้องการสูตรต่างกันอย่างไร",
        "body": """<h2>ทำไมต้องให้อาหารเปียก</h2>
<p>แมวเป็นสัตว์ที่ดื่มน้ำน้อยตามธรรมชาติ อาหารเปียกช่วยเสริมน้ำลดความเสี่ยงโรคไตและทางเดินปัสสาวะ</p>
<h2>แมวลูก (4-12 เดือน)</h2>
<p>ต้องการโปรตีนและแคลอรี่สูง เลือกซองหรือเปียเต่สูตรลูกแมว เนื้อนุ่มง่ายต่อการเคี้ยว</p>
<h2>แมวโต (1-7 ปี)</h2>
<p>เลือกสูตรครบถ้วนตามมาตรฐาน สลับรสชาติเพื่อไม่ให้เบื่อ ระวังแคลอรี่เกิน</p>
<h2>แมวสูงวัย (7+ ปี)</h2>
<p>เปียเต่นุ่มง่ายต่อการเคี้ยว สูตรเสริมสารสำหรับไตและข้อ ปรึกษาสัตวแพทย์หากมีโรคประจำตัว</p>""",
        "img": ("_wet_blog1.jpg", "wet-food-life-stage_P5vW3RV.jpg"),
        "cats": ["wet-cat-food"],
    },
    {
        "slug": "indoor-cat-food-tips",
        "title": "5 ข้อควรรู้ก่อนเลือกอาหารแมวเลี้ยงในบ้าน",
        "desc": "แมวในบ้านเคลื่อนไหวน้อย — ต้องการพลังงาน สารอาหาร และการดูแลต่างจากแมวข้างนอก",
        "body": """<h2>แมวในบ้านต่างจากแมวข้างนอกอย่างไร</h2>
<p>แมวในบ้านเผาผลาญพลังงานน้อยกว่า มีแนวโน้มอ้วน และเครียดง่ายกว่า อาหารต้องปรับให้เหมาะกับไลฟ์สไตล์</p>
<h2>5 ข้อควรรู้</h2>
<ol>
<li><strong>พลังงานต่ำกว่า</strong> — เลือกสูตร indoor หรือควบคุมน้ำหนัก</li>
<li><strong>เสริมใยอาหาร</strong> — ช่วยระบบขับถ่ายและลดก้อนขน</li>
<li><strong>น้ำเป็นสำคัญ</strong> — ใช้น้ำพุหรือสลับอาหารเปียก</li>
<li><strong>วัดปริมาณ</strong> — ใช้ชั่งหรือถ้วยตวง ไม่ใส่ทิ้งไว้ตลอด</li>
<li><strong>เปลี่ยนสูตรทีละน้อย</strong> — ผสมเก่า-ใหม่ 7-10 วัน</li>
</ol>""",
        "img": ("_dry_blog2.jpg", "indoor-cat-food-metal-bowl_gEQzUCl.jpg"),
        "cats": ["dry-cat-food"],
    },
    {
        "slug": "cat-food-bowl-tips",
        "title": "เทคนิคให้อาหารแมว: ถ้วย ชาม และปริมาณที่เหมาะสม",
        "desc": "ถ้วยแบบไหนดี? ให้กี่มื้อ? คำแนะนำจากสัตวแพทย์สำหรับแมวทุกวัย",
        "body": """<h2>ถ้วย/ชามแบบไหนดี</h2>
<p>ถ้วยเซรามิกหรือสแตนเลส ผิวเรียบ ลึกพอสมควร หลีกเลี่ยงพลาสติกเพราะเก็บกลิ่นและทำให้แมวเป็นสิว</p>
<h2>ให้กี่มื้อต่อวัน</h2>
<ul>
<li>ลูกแมว (2-6 เดือน): 3-4 มื้อ</li>
<li>แมวโต: 2 มื้อ (เช้า-เย็น)</li>
<li>แมวสูงวัย: 2-3 มื้อเล็ก</li>
</ul>
<h2>ปริมาณอาหาร</h2>
<p>อ่านฉลากเป็นฐาน ปรับตามน้ำหนักและกิจกรรม ชั่งน้ำหนักแมวทุก 2-4 สัปดาห์</p>""",
        "img": ("_dry_blog1.jpg", "cat-food-bowl-tips_PwwGSKY.jpg"),
        "cats": ["dry-cat-food", "wet-cat-food"],
    },
    {
        "slug": "cat-lick-treats-guide",
        "title": "ขนมเลียแมว: สนุกแค่ไหน และให้ได้กี่ชิ้นต่อวัน?",
        "desc": "คู่มือขนมเลียแมว ทูน่า ไก่ ตับ — ให้เท่าไรไม่เกิน และเลือกยังไงให้ปลอดภัย",
        "body": """<h2>ขนมเลียแมวคืออะไร</h2>
<p>ขนมเลีย (lick treat) เป็นขนมแมวรูปแบบแท่ง เลียจากมือหรือแท่งได้เลย ใช้เป็นรางวัลหรือสร้างความสัมพันธ์กับแมว</p>
<h2>ให้ได้กี่ชิ้นต่อวัน</h2>
<p>ขนมทุกชนิดรวมกันไม่ควรเกิน 10% ของแคลอรี่ต่อวัน ประมาณ 1-2 แท่งสำหรับแมว 4 กก.</p>
<h2>ข้อควรระวัง</h2>
<ul>
<li>ไม่แทนอาหารหลัก</li>
<li>อ่านส่วนผสม — หลีกเลี่ยงน้ำตาลและสีสังเคราะห์</li>
<li>แมวเบาหวานหรืออ้วนควรปรึกษาหมอก่อน</li>
</ul>""",
        "img": ("_lick_blog.jpg", "blog-lick-treat-guide-hero.jpg"),
        "cats": ["cat-lick-treats"],
    },
    {
        "slug": "cat-supplement-feeding-guide",
        "title": "วิธีให้อาหารเสริมแมวที่ถูกต้องและปลอดภัย",
        "desc": "คู่มือให้อาหารเสริมแบบไม่เกินจำเป็น ลดความเสี่ยงต่อไตและระบบทางเดินอาหาร",
        "body": """<h2>อาหารเสริมคืออะไร</h2>
<p>อาหารเสริมเป็นการเพิ่มสารอาหารหรือจุลินทรีย์นอกเหนือจากอาหารหลัก ไม่ใช่การรักษาโรคแทนยา และไม่ควรแทนที่อาหารที่มีคุณค่าครบถ้วน</p>
<h2>หลักการสำคัญ</h2>
<ol>
<li><strong>เลือกตามความจำเป็น</strong> แมวกินอาหารเม็ด/เปียกคุณภาพดีมักได้สารอาหารหลักครบแล้ว</li>
<li><strong>นับปริมาณรวม</strong> อย่าให้ซ้ำซ้อนหลายชนิดที่มีส่วนผสมคล้ายกัน</li>
<li><strong>แบ่งมื้อ</strong> ผสมกับอาหารมื้อเล็กๆ สังเกตอาการท้องเสียหรือไม่กิน</li>
<li><strong>โรคประจำตัว</strong> แมวไต หัวใจ หรือกำลังกินยา ต้องปรึกษาสัตวแพทย์ก่อนเสมอ</li>
</ol>
<h2>เมื่อไรควรปรึกษาหมอ</h2>
<p>ผมร่วงผิดปกติ ท้องเสียเรื้อรัง ซึม กินน้อยลง หรือวางแผนอาหารโฮมเมด — ควรให้หมอช่วยออกแบบ</p>""",
        "img": ("_supp_blog.jpg", "blog-cat-supplement-guide.jpg"),
        "cats": ["cat-supplements"],
    },
    {
        "slug": "cat-litter-indoor-health",
        "title": "สุขภาพแมวในบ้าน: ทรายแมวสะอาดลดความเสี่ยงโรคอย่างไร",
        "desc": "ทรายสะอาดไม่ใช่แค่กลิ่นดี — แต่สัมพันธ์กับสุขภาพทางเดินปัสสาวะและพฤติกรรมแมว",
        "body": """<h2>ทรายสะอาดกับสุขภาพแมว</h2>
<p>แมวที่ไม่ยอมถ่ายในถาดทรายสกปรก อาจกลั้นปัสสาวะ ซึ่งเสี่ยงต่อการอักเสบและนิ่วในทางเดินปัสสาวะ</p>
<h2>กี่ครั้งที่ควรเก็บทราย</h2>
<ul>
<li>จับก้อน: ตักวันละ 1-2 ครั้ง เปลี่ยนทั้งถาดทุก 2-3 สัปดาห์</li>
<li>ซิลิก้า: ตักอุจจาระทันที เปลี่ยนทั้งถาดเมื่อเม็ดเปลี่ยนสี</li>
<li>เม็ดไม้/ท้อฟู: ถ่ายเม็ดที่ชื้นออก เปลี่ยนทั้งถาดทุกสัปดาห์</li>
</ul>""",
        "img": ("_cat_blog_litter.jpg", "cat-litter-indoor-health_l8AMU7W.jpg"),
        "cats": ["cat-litter"],
    },
]

for row in POSTS:
    post, created = Post.objects.get_or_create(
        slug=row["slug"],
        defaults={
            "title": row["title"],
            "description": row["desc"],
            "body": row["body"],
            "author": author,
        },
    )
    if not created:
        post.title = row["title"]
        post.description = row["desc"]
        post.body = row["body"]
        post.author = author
        post.save()
    save_img(post, "featured_image", row["img"][0], row["img"][1])
    post.related_categories.set([cat_map[s] for s in row["cats"]])
    print(f"  Post: {post.slug} {'(new)' if created else '(updated)'}")

# ── FAQs ──
print("\n=== Seeding FAQs ===")

FAQS = {
    "cat-litter": [
        ("ทรายแมวเปลี่ยนบ่อยแค่ไหน?", "จับก้อน: ตักวันละ 1-2 ครั้ง เปลี่ยนทั้งถาดทุก 2-3 สัปดาห์ ซิลิก้า: เปลี่ยนเมื่อเม็ดเปลี่ยนสี ประมาณ 2-4 สัปดาห์"),
        ("ทรายแมวทิ้งลงโถส้วมได้ไหม?", "ท้อฟูและข้าวโพดบางสูตรสามารถทิ้งลงโถส้วมได้ แต่ดินเหนียวและซิลิก้าห้ามทิ้งเด็ดขาด"),
        ("แมวไม่ยอมใช้ถาดทรายทำไง?", "ลองเปลี่ยนชนิดทราย ขนาดถาด หรือตำแหน่ง หากยังไม่ยอมควรตรวจสุขภาพกับสัตวแพทย์"),
        ("แมวกินทรายเข้าไปอันตรายไหม?", "ทรายดินเหนียวอาจอุดตันลำไส้ ท้อฟูและข้าวโพดปลอดภัยกว่า แต่ควรปรึกษาหมอหากกินมาก"),
    ],
    "dry-cat-food": [
        ("อาหารเม็ดพอไหม ต้องเสริมเปียกไหม?", "อาหารเม็ดคุณภาพดีให้สารอาหารครบ แต่แนะนำสลับเปียกเพื่อเสริมน้ำ"),
        ("เปลี่ยนสูตรอาหารทำอย่างไร?", "ผสมเก่า-ใหม่ ค่อยๆ เพิ่มสัดส่วนใหม่ภายใน 7-10 วัน"),
        ("แมวอ้วนเลือกสูตรอาหารเม็ดอย่างไร?", "เลือกสูตร indoor หรือ weight control วัดปริมาณตามฉลาก ชั่งน้ำหนักทุก 2-4 สัปดาห์"),
    ],
    "wet-cat-food": [
        ("อาหารเปียกแทนอาหารเม็ดได้ไหม?", "ได้ หากเลือกสูตรครบถ้วนตามมาตรฐาน (AAFCO/FEDIAF) และให้ปริมาณเพียงพอ"),
        ("เปิดแล้วเก็บได้นานแค่ไหน?", "ซอง/ถาดเปิดแล้วเก็บตู้เย็นได้ 1-2 วัน ควรให้หมดภายในมื้อ"),
    ],
    "cat-lick-treats": [
        ("ขนมเลียให้ได้กี่แท่งต่อวัน?", "ขนมทุกชนิดรวมกันไม่ควรเกิน 10% แคลอรี่ต่อวัน ประมาณ 1-2 แท่งสำหรับแมว 4 กก."),
        ("ลูกแมวให้ขนมเลียได้ไหม?", "ขึ้นกับสูตร ส่วนใหญ่แนะนำแมวอายุ 3 เดือนขึ้นไป"),
    ],
    "cat-supplements": [
        ("อาหารเสริมแทนอาหารหลักได้ไหม?", "ไม่ควร อาหารเสริมไม่ได้ออกแบบให้ครบถ้วน ใช้เพิ่มเติมตามปริมาณที่ระบุเท่านั้น"),
        ("ลูกแมวให้อาหารเสริมได้ตั้งแต่อายุเท่าไร?", "ขึ้นกับชนิดสินค้า ควรอ่านฉลากและปรึกษาสัตวแพทย์ โดยเฉพาะลูกแมวต่ำกว่า 12 สัปดาห์"),
        ("ให้หลายชนิดพร้อมกันปลอดภัยไหม?", "ควรหลีกเลี่ยงการซ้อนส่วนผสมเดิม หากไม่แน่ใจให้ปรึกษาหมอ"),
        ("แมวไตควรเลือกอาหารเสริมอย่างไร?", "แมวไตมักต้องจำกัดฟอสฟอรัสและบางเกลือแร่ ห้ามให้เสริมเองโดยไม่มีคำแนะนำสัตวแพทย์"),
        ("ควรให้พร้อมอาหารหรือแยกเวลา?", "ส่วนใหญ่ผสมกับอาหารมื้อหลักจะกินง่ายกว่า เริ่มปริมาณน้อยแล้วค่อยๆ เพิ่ม"),
    ],
}

for cat_slug, faq_list in FAQS.items():
    cat_obj = cat_map[cat_slug]
    for q, a in faq_list:
        obj, created = FAQ.objects.get_or_create(
            category=cat_obj, question=q, defaults={"answer": a}
        )
        if not created:
            obj.answer = a
            obj.save()
        print(f"  FAQ: {q[:40]}... {'(new)' if created else '(updated)'}")

print("\n=== Seed complete! ===")
print(f"  Categories: {Category.objects.count()}")
print(f"  Products:   {Product.objects.count()}")
print(f"  Posts:      {Post.objects.count()}")
print(f"  FAQs:       {FAQ.objects.count()}")
print(f"  Authors:    {Author.objects.count()}")
