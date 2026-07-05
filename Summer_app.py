import streamlit as st
import pandas as pd
import requests
from bs4 import BeautifulSoup
from datetime import datetime, date
from urllib.parse import urlparse, urljoin
from pathlib import Path
from PIL import Image


# ============================================================
# إعداد الصفحة
# ============================================================
st.set_page_config(
    page_title="Summer Calendar 2026",
    page_icon="🎓",
    layout="wide"
)


# ============================================================
# بيانات المطور
# ============================================================
DEVELOPER_NAME = "Osamah AL-murisi"
DEVELOPER_ROLE = "Developer of Summer Calendar 2026"
DEVELOPER_EMAIL = "osama715008285@gmail.com"
DEVELOPER_WHATSAPP = "+249117806804"

BASE_DIR = Path(__file__).parent
PROFILE_IMAGE = BASE_DIR / "profile.jpg"
PROFILE_DISPLAY_IMAGE = BASE_DIR / "profile_display.jpg"


def create_cropped_profile_image():
    if not PROFILE_IMAGE.exists():
        return None

    img = Image.open(PROFILE_IMAGE).convert("RGB")

    target_w = 360
    target_h = 280
    target_ratio = target_w / target_h

    w, h = img.size
    current_ratio = w / h

    if current_ratio > target_ratio:
        new_w = int(h * target_ratio)
        left = (w - new_w) // 2
        img = img.crop((left, 0, left + new_w, h))
    else:
        new_h = int(w / target_ratio)
        top = int((h - new_h) * 0.15)
        top = max(0, top)

        if top + new_h > h:
            top = h - new_h

        img = img.crop((0, top, w, top + new_h))

    img = img.resize((target_w, target_h))
    img.save(PROFILE_DISPLAY_IMAGE, quality=95)

    return PROFILE_DISPLAY_IMAGE


# ============================================================
# روابط YÖK
# ============================================================
YOK_PUBLIC_URL = "https://www.yok.gov.tr/tr/university?type=1"
YOK_PRIVATE_URL = "https://www.yok.gov.tr/tr/university?type=2"


# ============================================================
# الترجمة
# ============================================================
TEXTS = {
    "ar": {
        "language": "🌍 اللغة",
        "developer": "بيانات المطور",
        "app_title": " تقويم الفصل الصيفي 2026",
        "hero_text": "لكل جامعة تظهر ثلاثة روابط: موقع الجامعة الرسمي، إعلان الصيفي / شؤون الطلاب، وقائمة كل الجامعات في YÖK.",
        "official": "🌐 موقع الجامعة الرسمي",
        "summer": "📢 إعلان الصيفي / شؤون الطلاب",
        "yok": "📚 كل الجامعات في YÖK",
        "choose_title": "🔎 اختيار الجامعة",
        "choose_text": "اختر جامعة حكومية أو جامعة خاصة. إذا أردت الانتقال من حكومية إلى خاصة أو العكس اضغط زر مسح الاختيار.",
        "public_list": "قائمة الجامعات الحكومية",
        "private_list": "قائمة الجامعات الخاصة",
        "choose_public": "اختر جامعة حكومية",
        "choose_private": "اختر جامعة خاصة",
        "reset": "🔄 مسح الاختيار / اختيار جامعة جديدة",
        "result": "📌 نتيجة الاختيار",
        "city": "📍 المدينة",
        "type": "🏛️ النوع",
        "status": "📌 الحالة",
        "start": "بداية التسجيل",
        "end": "نهاية التسجيل",
        "time": "الوقت",
        "fee": "💰 الرسوم",
        "note": "📝 ملاحظة",
        "official_missing": "🌐 رابط موقع الجامعة غير مضاف",
        "summer_missing": "📢 رابط شؤون الطلاب / إعلان الصيفي غير مضاف",
        "update_title": "🔄 تحديث قائمة الجامعات",
        "update_text": "إذا لم تظهر كل الجامعات، اضغط الزر لتحديث البيانات من YÖK.",
        "update_btn": "🔄 تحديث البيانات من YÖK",
        "updated": "✅ تم تحديث البيانات.",
        "footer_1": "تم التطوير بواسطة أسامة المريسي",
        "footer_2": "زر مسح الاختيار يتيح الانتقال بين الجامعات الحكومية والخاصة بسهولة.",
        "no_result": "لا توجد نتيجة لهذه الجامعة.",
        "not_declared": "غير معلن",
        "no_date": "لا يوجد موعد مضاف",
        "not_started": "لم يبدأ",
        "open_now": "مفتوح الآن",
        "last_day": "آخر يوم",
        "finished": "منتهي",
        "starts_after": "يبدأ بعد",
        "days": "يوم",
        "ends_today": "ينتهي اليوم",
        "left": "متبقي",
        "ended_before": "انتهى قبل",
        "public_type": "حكومية",
        "private_type": "خاصة",
        "whatsapp": "📱 واتساب",
        "email": "✉️ الإيميل",
        "image_missing": "الصورة غير موجودة",
    },
    "en": {
        "language": "🌍 Language",
        "developer": "Developer Info",
        "app_title": "🎓 Summer Semester Calendar 2026",
        "hero_text": "For each university, three links are shown: official website, summer announcement / student affairs, and YÖK university list.",
        "official": "🌐 Official University Website",
        "summer": "📢 Summer Announcement / Student Affairs",
        "yok": "📚 All Universities in YÖK",
        "choose_title": "🔎 Choose University",
        "choose_text": "Choose a public or private university. To switch between lists, click reset selection.",
        "public_list": "Public Universities",
        "private_list": "Private Universities",
        "choose_public": "Choose public university",
        "choose_private": "Choose private university",
        "reset": "🔄 Reset Selection / Choose New University",
        "result": "📌 Selected University",
        "city": "📍 City",
        "type": "🏛️ Type",
        "status": "📌 Status",
        "start": "Registration Start",
        "end": "Registration End",
        "time": "Time",
        "fee": "💰 Fee",
        "note": "📝 Note",
        "official_missing": "🌐 Official website link is not added",
        "summer_missing": "📢 Student affairs / summer announcement link is not added",
        "update_title": "🔄 Update University List",
        "update_text": "If all universities do not appear, click the button to update data from YÖK.",
        "update_btn": "🔄 Update Data from YÖK",
        "updated": "✅ Data updated.",
        "footer_1": "Developed by Osamah AL-murisi",
        "footer_2": "Reset button helps switch between public and private universities easily.",
        "no_result": "No result found for this university.",
        "not_declared": "Not announced",
        "no_date": "No date added",
        "not_started": "Not started",
        "open_now": "Open now",
        "last_day": "Last day",
        "finished": "Finished",
        "starts_after": "Starts after",
        "days": "days",
        "ends_today": "Ends today",
        "left": "Left",
        "ended_before": "Ended before",
        "public_type": "Public",
        "private_type": "Private",
        "whatsapp": "📱 WhatsApp",
        "email": "✉️ Email",
        "image_missing": "Image not found",
    },
    "tr": {
        "language": "🌍 Dil",
        "developer": "Geliştirici Bilgileri",
        "app_title": "🎓 Yaz Okulu Takvimi 2026",
        "hero_text": "Her üniversite için üç bağlantı gösterilir: resmi web sitesi, yaz okulu duyurusu / öğrenci işleri ve YÖK üniversite listesi.",
        "official": "🌐 Üniversite Resmi Sitesi",
        "summer": "📢 Yaz Okulu Duyurusu / Öğrenci İşleri",
        "yok": "📚 YÖK'teki Tüm Üniversiteler",
        "choose_title": "🔎 Üniversite Seç",
        "choose_text": "Devlet veya vakıf üniversitesi seçin. Liste değiştirmek için seçimi sıfırla butonuna basın.",
        "public_list": "Devlet Üniversiteleri",
        "private_list": "Vakıf Üniversiteleri",
        "choose_public": "Devlet üniversitesi seç",
        "choose_private": "Vakıf üniversitesi seç",
        "reset": "🔄 Seçimi Sıfırla / Yeni Üniversite Seç",
        "result": "📌 Seçilen Üniversite",
        "city": "📍 Şehir",
        "type": "🏛️ Tür",
        "status": "📌 Durum",
        "start": "Kayıt Başlangıcı",
        "end": "Kayıt Bitişi",
        "time": "Zaman",
        "fee": "💰 Ücret",
        "note": "📝 Not",
        "official_missing": "🌐 Üniversite resmi sitesi eklenmemiş",
        "summer_missing": "📢 Öğrenci İşleri / Yaz Okulu duyuru bağlantısı eklenmemiş",
        "update_title": "🔄 Üniversite Listesini Güncelle",
        "update_text": "Tüm üniversiteler görünmüyorsa, YÖK verilerini güncellemek için butona basın.",
        "update_btn": "🔄 YÖK Verilerini Güncelle",
        "updated": "✅ Veriler güncellendi.",
        "footer_1": "Osamah AL-murisi tarafından geliştirildi",
        "footer_2": "Sıfırlama butonu devlet ve vakıf üniversiteleri arasında geçişi kolaylaştırır.",
        "no_result": "Bu üniversite için sonuç bulunamadı.",
        "not_declared": "Açıklanmadı",
        "no_date": "Tarih eklenmedi",
        "not_started": "Başlamadı",
        "open_now": "Şu an açık",
        "last_day": "Son gün",
        "finished": "Bitti",
        "starts_after": "Başlamasına",
        "days": "gün",
        "ends_today": "Bugün bitiyor",
        "left": "Kalan",
        "ended_before": "Şu kadar gün önce bitti",
        "public_type": "Devlet",
        "private_type": "Vakıf",
        "whatsapp": "📱 WhatsApp",
        "email": "✉️ E-posta",
        "image_missing": "Resim bulunamadı",
    },
    "fr": {
        "language": "🌍 Langue",
        "developer": "Informations développeur",
        "app_title": "🎓 Calendrier d'été 2026",
        "hero_text": "Pour chaque université, trois liens sont affichés : site officiel, annonce d'été / affaires étudiantes, et liste des universités YÖK.",
        "official": "🌐 Site officiel de l'université",
        "summer": "📢 Annonce d'été / Affaires étudiantes",
        "yok": "📚 Toutes les universités dans YÖK",
        "choose_title": "🔎 Choisir une université",
        "choose_text": "Choisissez une université publique ou privée. Pour changer de liste, cliquez sur réinitialiser.",
        "public_list": "Universités publiques",
        "private_list": "Universités privées",
        "choose_public": "Choisir une université publique",
        "choose_private": "Choisir une université privée",
        "reset": "🔄 Réinitialiser / Choisir une nouvelle université",
        "result": "📌 Université sélectionnée",
        "city": "📍 Ville",
        "type": "🏛️ Type",
        "status": "📌 Statut",
        "start": "Début d'inscription",
        "end": "Fin d'inscription",
        "time": "Temps",
        "fee": "💰 Frais",
        "note": "📝 Note",
        "official_missing": "🌐 Le lien du site officiel n'est pas ajouté",
        "summer_missing": "📢 Le lien affaires étudiantes / annonce d'été n'est pas ajouté",
        "update_title": "🔄 Mettre à jour la liste",
        "update_text": "Si toutes les universités n'apparaissent pas, cliquez pour mettre à jour les données depuis YÖK.",
        "update_btn": "🔄 Mettre à jour depuis YÖK",
        "updated": "✅ Données mises à jour.",
        "footer_1": "Développé par Osamah AL-murisi",
        "footer_2": "Le bouton de réinitialisation permet de passer facilement entre universités publiques et privées.",
        "no_result": "Aucun résultat pour cette université.",
        "not_declared": "Non annoncé",
        "no_date": "Aucune date ajoutée",
        "not_started": "Pas commencé",
        "open_now": "Ouvert maintenant",
        "last_day": "Dernier jour",
        "finished": "Terminé",
        "starts_after": "Commence après",
        "days": "jours",
        "ends_today": "Se termine aujourd'hui",
        "left": "Restant",
        "ended_before": "Terminé il y a",
        "public_type": "Publique",
        "private_type": "Privée",
        "whatsapp": "📱 WhatsApp",
        "email": "✉️ Email",
        "image_missing": "Image introuvable",
    },
}


# ============================================================
# Session State
# ============================================================
if "lang" not in st.session_state:
    st.session_state.lang = "ar"

if "selected_public" not in st.session_state:
    st.session_state.selected_public = "اختر جامعة حكومية"

if "selected_private" not in st.session_state:
    st.session_state.selected_private = "اختر جامعة خاصة"


def t(key):
    return TEXTS[st.session_state.lang].get(key, key)


def is_arabic():
    return st.session_state.lang == "ar"


def box_dir():
    return "rtl" if is_arabic() else "ltr"


def box_align():
    return "right" if is_arabic() else "left"


# ============================================================
# روابط المواقع الرسمية
# ============================================================
OFFICIAL_WEBSITES = {
    "KARABÜK ÜNİVERSİTESİ": "https://www.karabuk.edu.tr",
    "MARMARA ÜNİVERSİTESİ": "https://www.marmara.edu.tr",
    "İSTANBUL AYDIN ÜNİVERSİTESİ": "https://www.aydin.edu.tr",
    "ANADOLU ÜNİVERSİTESİ": "https://www.anadolu.edu.tr",
    "ANKARA ÜNİVERSİTESİ": "https://www.ankara.edu.tr",
    "EGE ÜNİVERSİTESİ": "https://www.ege.edu.tr",
    "AKDENİZ ÜNİVERSİTESİ": "https://www.akdeniz.edu.tr",
    "GAZİANTEP ÜNİVERSİTESİ": "https://www.gantep.edu.tr",
    "GEBZE TEKNİK ÜNİVERSİTESİ": "https://www.gtu.edu.tr",
    "ORTA DOĞU TEKNİK ÜNİVERSİTESİ": "https://www.metu.edu.tr",
    "BOĞAZİÇİ ÜNİVERSİTESİ": "https://www.boun.edu.tr",
    "DİCLE ÜNİVERSİTESİ": "https://www.dicle.edu.tr",
    "ABDULLAH GÜL ÜNİVERSİTESİ": "https://www.agu.edu.tr",
    "ADANA ALPARSLAN TÜRKEŞ BİLİM VE TEKNOLOJİ ÜNİVERSİTESİ": "https://www.atu.edu.tr",
    "İSTANBUL MEDİPOL ÜNİVERSİTESİ": "https://www.medipol.edu.tr",
    "BAHÇEŞEHİR ÜNİVERSİTESİ": "https://bau.edu.tr",
    "ALTINBAŞ ÜNİVERSİTESİ": "https://altinbas.edu.tr",
    "İSTANBUL GELİŞİM ÜNİVERSİTESİ": "https://www.gelisim.edu.tr",
    "İSTANBUL GEDİK ÜNİVERSİTESİ": "https://www.gedik.edu.tr",
    "İSTİNYE ÜNİVERSİTESİ": "https://www.istinye.edu.tr",
    "İSTANBUL NİŞANTAŞI ÜNİVERSİTESİ": "https://www.nisantasi.edu.tr",
    "HALİÇ ÜNİVERSİTESİ": "https://halic.edu.tr",
    "MALTEPE ÜNİVERSİTESİ": "https://www.maltepe.edu.tr",
    "DOĞUŞ ÜNİVERSİTESİ": "https://www.dogus.edu.tr",
    "KADİR HAS ÜNİVERSİTESİ": "https://www.khas.edu.tr",
    "ACIBADEM ÜNİVERSİTESİ": "https://www.acibadem.edu.tr",
    "BİRUNİ ÜNİVERSİTESİ": "https://www.biruni.edu.tr",
    "ATILIM ÜNİVERSİTESİ": "https://www.atilim.edu.tr",
    "BAŞKENT ÜNİVERSİTESİ": "https://www.baskent.edu.tr",
    "İHSAN DOĞRAMACI BİLKENT ÜNİVERSİTESİ": "https://w3.bilkent.edu.tr",
    "TED ÜNİVERSİTESİ": "https://www.tedu.edu.tr",
    "OSTİM TEKNİK ÜNİVERSİTESİ": "https://www.ostimteknik.edu.tr",
    "YAŞAR ÜNİVERSİTESİ": "https://www.yasar.edu.tr",
}


# ============================================================
# روابط Öğrenci İşleri / Duyurular
# ============================================================
OIDB_DUYURU_LINKS = {
    "KARABÜK ÜNİVERSİTESİ": "https://oidb.karabuk.edu.tr",
    "MARMARA ÜNİVERSİTESİ": "https://oidb.marmara.edu.tr",
    "ANKARA ÜNİVERSİTESİ": "https://oidb.ankara.edu.tr",
    "EGE ÜNİVERSİTESİ": "https://oidb.ege.edu.tr",
    "AKDENİZ ÜNİVERSİTESİ": "https://oidb.akdeniz.edu.tr",
    "ANADOLU ÜNİVERSİTESİ": "https://www.anadolu.edu.tr/duyurular",
    "DİCLE ÜNİVERSİTESİ": "https://www.dicle.edu.tr/tr/birimler/ogrenci-isleri-daire-baskanligi",
    "ABDULLAH GÜL ÜNİVERSİTESİ": "https://oidb.agu.edu.tr",
    "ADANA ALPARSLAN TÜRKEŞ BİLİM VE TEKNOLOJİ ÜNİVERSİTESİ": "https://oidb.atu.edu.tr",
    "İSTANBUL AYDIN ÜNİVERSİTESİ": "https://www.aydin.edu.tr/tr-tr/ogrenciler/Pages/duyurular.aspx",
    "İSTANBUL GELİŞİM ÜNİVERSİTESİ": "https://oidb.gelisim.edu.tr",
    "İSTİNYE ÜNİVERSİTESİ": "https://www.istinye.edu.tr/tr/duyurular",
    "BAHÇEŞEHİR ÜNİVERSİTESİ": "https://bau.edu.tr/duyurular",
    "ALTINBAŞ ÜNİVERSİTESİ": "https://www.altinbas.edu.tr/tr/duyurular",
    "İSTANBUL MEDİPOL ÜNİVERSİTESİ": "https://www.medipol.edu.tr/duyurular",
}


# ============================================================
# مواعيد الصيفي
# ============================================================
SUMMER_DATES = {
    "KARABÜK ÜNİVERSİTESİ": {
        "start": "2026-06-29",
        "end": "2026-07-03",
        "fee": "244.02 TL لكل ساعة",
        "note": "التسجيل والدفع من خلال OBS. تأكد من إعلان Öğrenci İşleri.",
    },
    "MARMARA ÜNİVERSİTESİ": {
        "start": "2026-07-01",
        "end": "2026-07-07",
        "fee": "حسب إعلان الجامعة",
        "note": "تأكد من إعلان Öğrenci İşleri.",
    },
    "İSTANBUL AYDIN ÜNİVERSİTESİ": {
        "start": "2026-06-22",
        "end": "2026-07-08",
        "fee": "حسب المادة والكلية",
        "note": "جامعة خاصة، الرسوم تختلف حسب المادة.",
    },
}


CITY_KEYWORDS = [
    "ADANA", "ADIYAMAN", "AFYONKARAHİSAR", "AĞRI", "AMASYA", "ANKARA",
    "ANTALYA", "ARTVİN", "AYDIN", "BALIKESİR", "BİLECİK", "BİNGÖL",
    "BİTLİS", "BOLU", "BURDUR", "BURSA", "ÇANAKKALE", "ÇANKIRI",
    "ÇORUM", "DENİZLİ", "DİYARBAKIR", "EDİRNE", "ELAZIĞ", "ERZİNCAN",
    "ERZURUM", "ESKİŞEHİR", "GAZİANTEP", "GİRESUN", "GÜMÜŞHANE",
    "HATAY", "ISPARTA", "MERSİN", "İSTANBUL", "İZMİR", "KARS",
    "KASTAMONU", "KAYSERİ", "KOCAELİ", "KONYA", "KÜTAHYA", "MALATYA",
    "MANİSA", "MARDİN", "MUĞLA", "ORDU", "RİZE", "SAKARYA", "SAMSUN",
    "SİVAS", "TRABZON", "ŞANLIURFA", "VAN", "ZONGULDAK", "KARABÜK",
    "DÜZCE", "KIRIKKALE", "KIRKLARELİ", "KIRŞEHİR", "NEVŞEHİR",
    "NİĞDE", "TOKAT", "UŞAK", "YOZGAT", "OSMANİYE", "KARAMAN",
    "BAYBURT", "ARDAHAN", "IĞDIR", "YALOVA", "KİLİS", "BATMAN",
    "ŞIRNAK", "SİİRT", "MUŞ", "HAKKARİ", "TUNCELİ", "BARTIN",
]


# ============================================================
# دوال مساعدة
# ============================================================
def format_date(value):
    if not value:
        return t("not_declared")
    try:
        return datetime.strptime(value, "%Y-%m-%d").strftime("%d/%m/%Y")
    except Exception:
        return t("not_declared")


def get_status(start_value, end_value):
    if not start_value or not end_value:
        return t("not_declared")
    try:
        today = date.today()
        start_date = datetime.strptime(start_value, "%Y-%m-%d").date()
        end_date = datetime.strptime(end_value, "%Y-%m-%d").date()

        if today < start_date:
            return t("not_started")
        if start_date <= today <= end_date:
            return t("last_day") if today == end_date else t("open_now")
        return t("finished")
    except Exception:
        return t("not_declared")


def get_days(start_value, end_value):
    if not start_value or not end_value:
        return t("no_date")
    try:
        today = date.today()
        start_date = datetime.strptime(start_value, "%Y-%m-%d").date()
        end_date = datetime.strptime(end_value, "%Y-%m-%d").date()

        if today < start_date:
            return f"{t('starts_after')} {(start_date - today).days} {t('days')}"
        if start_date <= today <= end_date:
            left = (end_date - today).days
            return t("ends_today") if left == 0 else f"{t('left')} {left} {t('days')}"
        return f"{t('ended_before')} {(today - end_date).days} {t('days')}"
    except Exception:
        return t("not_declared")


def clean_university_name(text):
    text = str(text).strip()
    words = text.split()
    cleaned = []

    for word in words:
        cleaned.append(word)
        upper_word = word.upper()
        if "ÜNİVERSİTESİ" in upper_word or "ENSTİTÜSÜ" in upper_word:
            break

    return " ".join(cleaned).strip()


def get_city_from_text(text):
    upper_text = str(text).upper()
    for city in CITY_KEYWORDS:
        if city in upper_text:
            return city.title()
    return "غير محدد"


def normalize_url(url):
    if not url:
        return ""
    url = str(url).strip()
    if not url.startswith("http"):
        url = "https://" + url
    return url


@st.cache_data(ttl=60 * 60 * 24, show_spinner=False)
def url_is_working(url):
    try:
        if not url:
            return False
        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(url, headers=headers, timeout=5, allow_redirects=True)
        return response.status_code < 400
    except Exception:
        return False


def build_oidb_candidates(official_site):
    candidates = []
    official_site = normalize_url(official_site)

    if not official_site:
        return candidates

    parsed = urlparse(official_site)
    scheme = parsed.scheme or "https"
    host = parsed.netloc.replace("www.", "")

    if not host:
        return candidates

    base = f"{scheme}://{host}"
    www_base = f"{scheme}://www.{host}"

    candidates.extend([
        f"{scheme}://oidb.{host}",
        f"{scheme}://ogrenci.{host}",
        f"{scheme}://ogrenciisleri.{host}",
        f"{base}/duyurular",
        f"{base}/tr/duyurular",
        f"{base}/ogrenci-isleri",
        f"{base}/tr/ogrenci-isleri",
        f"{base}/ogrenci-isleri-daire-baskanligi",
        f"{base}/tr/birimler/ogrenci-isleri-daire-baskanligi",
        f"{base}/ogrenciler/duyurular",
        f"{base}/tr/ogrenciler/duyurular",
        f"{www_base}/duyurular",
        f"{www_base}/tr/duyurular",
        f"{www_base}/ogrenci-isleri",
        f"{www_base}/tr/ogrenci-isleri",
        f"{www_base}/ogrenciler/duyurular",
        f"{www_base}/tr/ogrenciler/duyurular",
    ])

    clean = []
    for item in candidates:
        if item not in clean:
            clean.append(item)

    return clean


@st.cache_data(ttl=60 * 60 * 24, show_spinner=False)
def discover_oidb_link(official_site):
    for link in build_oidb_candidates(official_site):
        if url_is_working(link):
            return link
    return ""


@st.cache_data(ttl=60 * 60 * 24, show_spinner=False)
def extract_official_site_from_yok(yok_detail_link):
    try:
        if not yok_detail_link:
            return ""

        if "yok.gov.tr" not in yok_detail_link:
            return normalize_url(yok_detail_link)

        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(yok_detail_link, headers=headers, timeout=10)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, "html.parser")
        links = soup.find_all("a", href=True)

        for link in links:
            href = link.get("href", "").strip()

            if not href:
                continue

            if href.startswith("//"):
                href = "https:" + href

            if href.startswith("/"):
                href = urljoin("https://www.yok.gov.tr", href)

            if href.startswith("http") and "edu.tr" in href and "yok.gov.tr" not in href:
                return normalize_url(href)

        return ""
    except Exception:
        return ""


@st.cache_data(ttl=60 * 60 * 24)
def fetch_yok_universities():
    universities = []

    sources = [
        {
            "url": YOK_PUBLIC_URL,
            "type": "حكومية",
            "official_type": "Devlet Üniversiteleri",
            "all_link": YOK_PUBLIC_URL,
        },
        {
            "url": YOK_PRIVATE_URL,
            "type": "خاصة",
            "official_type": "Vakıf Üniversiteleri",
            "all_link": YOK_PRIVATE_URL,
        },
    ]

    headers = {"User-Agent": "Mozilla/5.0"}

    for source in sources:
        try:
            response = requests.get(source["url"], headers=headers, timeout=30)
            response.raise_for_status()
            response.encoding = response.apparent_encoding

            soup = BeautifulSoup(response.text, "html.parser")
            blocks = soup.find_all(["a", "li", "div", "span", "p", "h1", "h2", "h3", "h4"])

            for block in blocks:
                text = block.get_text(" ", strip=True)

                if not text:
                    continue

                upper_text = text.upper()

                if "ÜNİVERSİTESİ" not in upper_text and "ENSTİTÜSÜ" not in upper_text:
                    continue

                name = clean_university_name(text)

                if len(name) < 8:
                    continue

                city = get_city_from_text(name + " " + text)
                yok_detail_link = source["url"]

                if block.name == "a" and block.get("href"):
                    href = block.get("href")
                    if href.startswith("http"):
                        yok_detail_link = href
                    elif href.startswith("/"):
                        yok_detail_link = "https://www.yok.gov.tr" + href

                universities.append({
                    "university": name,
                    "city": city,
                    "type": source["type"],
                    "official_type": source["official_type"],
                    "yok_detail_link": yok_detail_link,
                    "all_universities_link": source["all_link"],
                })

        except Exception:
            pass

    df = pd.DataFrame(universities)

    if df.empty:
        return pd.DataFrame(columns=[
            "university",
            "city",
            "type",
            "official_type",
            "yok_detail_link",
            "all_universities_link",
        ])

    df["university"] = df["university"].astype(str).str.strip()
    df = df.drop_duplicates(subset=["university", "type"]).reset_index(drop=True)

    return df


def add_summer_info(input_df):
    rows = []

    for _, row in input_df.iterrows():
        university_name = row["university"]
        summer = SUMMER_DATES.get(university_name, {})

        start = summer.get("start", "")
        end = summer.get("end", "")

        rows.append({
            "university": university_name,
            "city": row["city"],
            "type": row["type"],
            "official_type": row["official_type"],
            "yok_detail_link": row["yok_detail_link"],
            "all_universities_link": row["all_universities_link"],
            "start": start,
            "end": end,
            "start_display": format_date(start),
            "end_display": format_date(end),
            "status": get_status(start, end),
            "days": get_days(start, end),
            "fee": summer.get("fee", t("not_declared")),
            "note": summer.get("note", t("not_declared")),
        })

    return pd.DataFrame(rows)


def get_links_for_university(row):
    university_name = row["university"]

    official_site = OFFICIAL_WEBSITES.get(university_name, "")

    if not official_site:
        official_site = extract_official_site_from_yok(row["yok_detail_link"])

    official_site = normalize_url(official_site) if official_site else ""

    summer_link = OIDB_DUYURU_LINKS.get(university_name, "")

    if not summer_link and official_site:
        summer_link = discover_oidb_link(official_site)

    summer_link = normalize_url(summer_link) if summer_link else ""

    return official_site, summer_link


# ============================================================
# تحميل البيانات
# ============================================================
base_df = fetch_yok_universities()

if base_df.empty:
    st.error("لم يتم سحب الجامعات من YÖK. تأكد من الإنترنت ثم أعد تشغيل الصفحة.")
    st.stop()

df = add_summer_info(base_df)


# ============================================================
# CSS
# ============================================================
direction = "rtl" if is_arabic() else "ltr"
align = "right" if is_arabic() else "left"

st.markdown(
    f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Tajawal:wght@400;500;700;800;900&display=swap');

* {{
    font-family: 'Tajawal', sans-serif !important;
}}

html, body, [class*="css"] {{
    direction: {direction};
    text-align: {align};
}}

.stApp {{
    background:
        radial-gradient(circle at 10% 10%, rgba(37, 99, 235, 0.15), transparent 35%),
        radial-gradient(circle at 90% 20%, rgba(14, 165, 233, 0.13), transparent 30%),
        linear-gradient(135deg, #eef6ff 0%, #f8fbff 50%, #ffffff 100%);
}}

.block-container {{
    max-width: 1400px;
    padding-top: 30px;
}}

.rtl-box {{
    direction: {box_dir()};
    text-align: {box_align()};
}}

.rtl-box .title,
.rtl-box .sub {{
    direction: {box_dir()};
    text-align: {box_align()};
}}

.developer-title-box {{
    background: linear-gradient(120deg, #123d7a, #1f78d1);
    border-radius: 34px;
    padding: 30px;
    margin-bottom: 25px;
    box-shadow: 0 18px 45px rgba(15, 47, 95, 0.22);
    text-align: center;
    color: white;
    font-size: 42px;
    font-weight: 900;
}}

.developer-card {{
    background: #ffffff;
    border: 1px solid #dbeafe;
    border-radius: 34px;
    padding: 35px;
    margin-bottom: 28px;
    box-shadow: 0 18px 45px rgba(15, 47, 95, 0.12);
    text-align: center;
}}

.developer-name-fixed {{
    text-align: center;
    color: #0f2f5f;
    font-size: 40px;
    font-weight: 900;
    margin-top: 18px;
    margin-bottom: 8px;
}}

.developer-role-fixed {{
    text-align: center;
    color: #2563eb;
    font-size: 23px;
    font-weight: 800;
    margin-bottom: 20px;
}}

.main-hero {{
    background: linear-gradient(120deg, #123d7a, #1f78d1);
    border-radius: 34px;
    padding: 60px 45px;
    box-shadow: 0 25px 60px rgba(15, 47, 95, 0.25);
    margin-bottom: 28px;
    text-align: center;
}}

.hero-title {{
    color: #ffffff !important;
    font-size: 58px;
    font-weight: 900;
    line-height: 1.35;
    margin-bottom: 22px;
    text-align: center;
}}

.hero-desc {{
    color: #ffffff !important;
    font-size: 24px;
    font-weight: 800;
    line-height: 1.8;
    text-align: center;
}}

.badge-clean {{
    background: rgba(255,255,255,0.60);
    color: #0f2f5f !important;
    border: 1px solid rgba(255,255,255,0.85);
    padding: 16px 24px;
    border-radius: 999px;
    font-size: 20px;
    font-weight: 900;
    text-align: center;
    display: block;
    box-shadow: 0 10px 25px rgba(0,0,0,0.08);
}}

.box {{
    background: #ffffff;
    border: 1px solid #dceafd;
    border-radius: 28px;
    padding: 28px;
    box-shadow: 0 15px 35px rgba(15, 47, 95, 0.08);
    margin-bottom: 24px;
}}

.result-box {{
    background: #ffffff;
    border: 1px solid #dceafd;
    border-right: 8px solid #0e73d8;
    border-radius: 26px;
    padding: 28px;
    box-shadow: 0 14px 35px rgba(15, 47, 95, 0.08);
    margin-bottom: 20px;
    direction: {box_dir()};
    text-align: {box_align()};
}}

.title {{
    color: #0f2f5f !important;
    font-size: 30px;
    font-weight: 900;
    margin-bottom: 10px;
}}

.sub {{
    color: #334155 !important;
    font-size: 17px;
    font-weight: 700;
    margin-bottom: 20px;
    line-height: 1.9;
}}

.stSelectbox div[data-baseweb="select"] {{
    border-radius: 18px !important;
}}

.stButton > button {{
    background: linear-gradient(120deg, #0b4da2, #0e73d8) !important;
    color: white !important;
    border: none !important;
    border-radius: 18px !important;
    min-height: 55px !important;
    font-size: 18px !important;
    font-weight: 900 !important;
    box-shadow: 0 12px 28px rgba(14, 115, 216, 0.25);
}}

.footer {{
    background: #0f2f5f;
    color: white;
    padding: 28px;
    border-radius: 28px;
    text-align: center;
    margin-top: 30px;
}}

.footer h3 {{
    color: white;
    font-weight: 900;
}}

.footer p {{
    color: #dbeafe;
    font-weight: 700;
}}
</style>
""",
    unsafe_allow_html=True,
)


# ============================================================
# اختيار اللغة
# ============================================================
lang_col1, lang_col2, lang_col3 = st.columns([1, 1, 2])

with lang_col1:
    lang_choice = st.selectbox(
        t("language"),
        ["العربية", "English", "Türkçe", "Français"],
        index={"ar": 0, "en": 1, "tr": 2, "fr": 3}[st.session_state.lang],
    )

lang_map = {
    "العربية": "ar",
    "English": "en",
    "Türkçe": "tr",
    "Français": "fr",
}

new_lang = lang_map[lang_choice]

if new_lang != st.session_state.lang:
    st.session_state.lang = new_lang
    st.rerun()


# ============================================================
# بيانات المطور
# ============================================================
st.markdown(
    f"""
<div class="developer-title-box">
    👨‍💻 {t("developer")}
</div>
""",
    unsafe_allow_html=True,
)

st.markdown('<div class="developer-card">', unsafe_allow_html=True)

cropped_image = create_cropped_profile_image()

if cropped_image:
    img_col1, img_col2, img_col3 = st.columns([1, 1, 1])
    with img_col2:
        st.image(str(cropped_image), width=360)
else:
    st.error(f"{t('image_missing')}: {PROFILE_IMAGE}")

st.markdown(
    f"""
<div class="developer-name-fixed">
    {DEVELOPER_NAME}
</div>

<div class="developer-role-fixed">
    {DEVELOPER_ROLE}
</div>
""",
    unsafe_allow_html=True,
)

whatsapp_number = DEVELOPER_WHATSAPP.replace("+", "").replace(" ", "").replace("-", "")

btn_col1, btn_col2, btn_col3, btn_col4 = st.columns([1, 1, 1, 1])

with btn_col2:
    st.link_button(
        t("whatsapp"),
        f"https://wa.me/{whatsapp_number}",
        use_container_width=True,
    )

with btn_col3:
    st.link_button(
        t("email"),
        f"mailto:{DEVELOPER_EMAIL}",
        use_container_width=True,
    )

st.markdown("</div>", unsafe_allow_html=True)


# ============================================================
# الهيدر الرئيسي - محلول نهائيًا
# ============================================================
st.markdown(
    f"""
<div class="main-hero">
    <div class="hero-title">{t("app_title")}</div>
    <div class="hero-desc">{t("hero_text")}</div>
</div>
""",
    unsafe_allow_html=True,
)

badge_col1, badge_col2, badge_col3 = st.columns(3)

with badge_col1:
    st.markdown(
        f'<div class="badge-clean">{t("official")}</div>',
        unsafe_allow_html=True,
    )

with badge_col2:
    st.markdown(
        f'<div class="badge-clean">{t("summer")}</div>',
        unsafe_allow_html=True,
    )

with badge_col3:
    st.markdown(
        f'<div class="badge-clean">{t("yok")}</div>',
        unsafe_allow_html=True,
    )

st.write("")


# ============================================================
# اختيار الجامعة
# ============================================================
st.markdown(
    f"""
<div class="box rtl-box">
    <div class="title">{t("choose_title")}</div>
    <div class="sub">{t("choose_text")}</div>
</div>
""",
    unsafe_allow_html=True,
)

reset_col1, reset_col2, reset_col3 = st.columns([1, 1.2, 1])

with reset_col2:
    if st.button(t("reset"), use_container_width=True):
        st.session_state.selected_public = "اختر جامعة حكومية"
        st.session_state.selected_private = "اختر جامعة خاصة"
        st.rerun()

col1, col2 = st.columns(2)

with col1:
    public_list = ["اختر جامعة حكومية"] + sorted(
        df[df["type"] == "حكومية"]["university"].dropna().unique().tolist()
    )

    selected_public = st.selectbox(
        t("public_list"),
        public_list,
        key="selected_public",
        format_func=lambda x: t("choose_public") if x == "اختر جامعة حكومية" else x,
    )

with col2:
    private_list = ["اختر جامعة خاصة"] + sorted(
        df[df["type"] == "خاصة"]["university"].dropna().unique().tolist()
    )

    selected_private = st.selectbox(
        t("private_list"),
        private_list,
        key="selected_private",
        format_func=lambda x: t("choose_private") if x == "اختر جامعة خاصة" else x,
    )


# ============================================================
# تطبيق الاختيار
# ============================================================
filtered_df = pd.DataFrame(columns=df.columns)

if st.session_state.selected_public != "اختر جامعة حكومية":
    filtered_df = df[df["university"] == st.session_state.selected_public].copy()

elif st.session_state.selected_private != "اختر جامعة خاصة":
    filtered_df = df[df["university"] == st.session_state.selected_private].copy()


# ============================================================
# عرض النتيجة
# ============================================================
if (
    st.session_state.selected_public != "اختر جامعة حكومية"
    or st.session_state.selected_private != "اختر جامعة خاصة"
):
    st.markdown(
        f"""
<div class="box rtl-box">
    <div class="title">{t("result")}</div>
</div>
""",
        unsafe_allow_html=True,
    )

    if filtered_df.empty:
        st.warning(t("no_result"))
    else:
        for _, row in filtered_df.iterrows():
            official_site, summer_link = get_links_for_university(row)

            st.markdown('<div class="result-box">', unsafe_allow_html=True)

            st.markdown(f"## {row['university']}")

            c1, c2, c3 = st.columns(3)

            with c1:
                st.info(f"{t('city')}: {row['city']}")

            with c2:
                shown_type = t("public_type") if row["type"] == "حكومية" else t("private_type")
                st.info(f"{t('type')}: {shown_type}")

            with c3:
                st.info(f"{t('status')}: {row['status']}")

            d1, d2, d3 = st.columns(3)

            with d1:
                st.metric(t("start"), row["start_display"])

            with d2:
                st.metric(t("end"), row["end_display"])

            with d3:
                st.metric(t("time"), row["days"])

            st.write("")

            link1, link2, link3 = st.columns(3)

            with link1:
                if official_site:
                    st.link_button(t("official"), official_site, use_container_width=True)
                else:
                    st.warning(t("official_missing"))

            with link2:
                if summer_link:
                    st.link_button(t("summer"), summer_link, use_container_width=True)
                else:
                    st.warning(t("summer_missing"))

            with link3:
                st.link_button(t("yok"), row["all_universities_link"], use_container_width=True)

            st.write(f"**{t('fee')}:** {row['fee']}")
            st.write(f"**{t('note')}:** {row['note']}")

            st.markdown("</div>", unsafe_allow_html=True)


# ============================================================
# تحديث البيانات
# ============================================================
st.markdown(
    f"""
<div class="box rtl-box">
    <div class="title">{t("update_title")}</div>
    <div class="sub">{t("update_text")}</div>
</div>
""",
    unsafe_allow_html=True,
)

refresh_clicked = st.button(t("update_btn"), use_container_width=True)

if refresh_clicked:
    st.cache_data.clear()
    st.session_state.selected_public = "اختر جامعة حكومية"
    st.session_state.selected_private = "اختر جامعة خاصة"
    st.success(t("updated"))
    st.rerun()


# ============================================================
# الفوتر
# ============================================================
st.markdown(
    f"""
<div class="footer">
    <h3>Summer Calendar 2026</h3>
    <p>{t("footer_1")}</p>
    <p>{t("footer_2")}</p>
</div>
""",
    unsafe_allow_html=True,
)