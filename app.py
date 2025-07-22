# app.py (Projenin Son Hali)

import os
from flask import Flask, render_template, request, jsonify
import google.generativeai as genai

# --- API Anahtarını ve Gemini Modelini Kurulumu ---
# PyCharm'daki Run -> Edit Configurations menüsünden GOOGLE_API_KEY'i ayarladığınızdan emin olun.
api_key = os.environ.get("GOOGLE_API_KEY")

if not api_key:
    print("HATA: GOOGLE_API_KEY ortam değişkeni bulunamadı!")
    print("Lütfen PyCharm'da 'Run -> Edit Configurations...' menüsünden API anahtarınızı ayarlayın.")
    exit()

genai.configure(api_key=api_key)

# --- Flask Uygulamasını Başlatma ---
app = Flask(__name__)


# --- BİLGİ KAYNAKLARI (NİLAY'IN BEYNİNİN FARKLI BÖLMELERİ) ---

# Dinamik Veri: Etkinlikler (Bu veriler gelecekte bir veritabanından gelecek)
etkinlik_veritabani = [
    f"Tarih: 25 Temmuz 2025 Cuma - Gençlik Merkezi'nde Gitar Atölyesi - Saat 18:00",
    f"Tarih: 26 Temmuz 2025 Cumartesi - Nazım Hikmet Kültürevi'nde 'Yaza Merhaba' Konseri - Saat 20:00",
    f"Tarih: 27 Temmuz 2025 Pazar - Balat Atatürk Ormanı'nda Doğa Yürüyüşü - Buluşma 09:00",
    "Ağustos ayı boyunca - Çevrimiçi Yazılım Atölyesi Kayıtları devam ediyor."
]

# Statik Veri: Gençlik Hakları ve Politikaları
genclik_haklari_veritabani = {
    "genel": "Nilüfer Belediyesi, gençlerin sosyal, kültürel ve kişisel gelişimlerini desteklemeyi hedefler. Gençlik merkezleri, atölyeler ve danışmanlık hizmetleri bu amaç doğrultusunda sunulmaktadır.",
    "eğitim ve burslar": "Belediyemiz, ihtiyaç sahibi başarılı öğrencilere eğitim desteği ve burs olanakları sunmaktadır. Başvuru dönemleri ve şartları her yıl belediyenin resmi web sitesinden duyurulur.",
    "çalışma ve staj": "Gençlerin iş hayatına atılmasına destek olmak amacıyla kariyer günleri ve staj programları düzenlenmektedir. 'İlk İşim' projesi kapsamında yerel işletmelerle gençler arasında köprü kurulur.",
    "proje desteği": "'Bir Fikrim Var!' diyen tüm gençlerin projeleri, Nilüfer Belediyesi Proje Ofisi tarafından değerlendirilir ve uygun bulunanlara mentörlük ve kaynak desteği sağlanır."
}


def get_nilay_response(user_message):
    """
    Bu ana fonksiyon, bir yönlendirici (router) gibi çalışır.
    Önce kullanıcının niyetini anlar, sonra uygun cevabı üretir.
    """
    model = genai.GenerativeModel('gemini-1.5-flash-latest')

    # --- 1. ADIM: NİYET TESPİTİ ---
    prompt_yonlendirici = f"""
    Kullanıcının sorusunu analiz et ve amacını şu üç kategoriden biriyle etiketle: 'etkinlik_sorgusu', 'bilgi_sorgusu', 'genel_sohbet'.
    - Eğer soru konser, atölye, yürüyüş gibi belirli bir tarih veya zamanla ilgili bir aktiviteyi soruyorsa 'etkinlik_sorgusu' de.
    - Eğer soru burs, staj, proje desteği, haklar, politikalar gibi genel bir konuyu soruyorsa 'bilgi_sorgusu' de.
    - Eğer yukarıdaki ikisi de değilse, sadece selamlaşma, hal hatır sorma veya kişisel bir soru ise 'genel_sohbet' de.
    Sadece kategori adını yaz, başka hiçbir şey yazma.

    Kullanıcı Sorusu: "{user_message}"
    Kategori:
    """
    try:
        niyet_response = model.generate_content(prompt_yonlendirici)
        kategori = niyet_response.text.strip()

        # --- 2. ADIM: NİYETE GÖRE BİLGİ VE GÖREV BELİRLEME ---
        bilgi_kaynagi = ""
        gorev_aciklamasi = ""

        if kategori == 'etkinlik_sorgusu':
            bilgi_kaynagi = "\n- ".join(etkinlik_veritabani)
            gorev_aciklamasi = "kullanıcının sorusunu SADECE bu etkinlik listesine göre cevapla."
        elif kategori == 'bilgi_sorgusu':
            bilgi_kaynagi = "\n".join([f"- {k}: {v}" for k, v in genclik_haklari_veritabani.items()])
            gorev_aciklamasi = "kullanıcının sorusunu SADECE bu gençlik hakları ve politikaları bilgilerine göre cevapla."
        else: # genel_sohbet durumu
            bilgi_kaynagi = "Yok"
            gorev_aciklamasi = "kullanıcıyla arkadaşça sohbet et. Ona nasıl olduğunu sorabilir, gününün nasıl geçtiğini merak edebilirsin. Ancak asla kişisel tavsiye verme ve belediyenin resmi görüşü olmayan (siyasi, dini vb.) konulardan uzak dur."

        # --- 3. ADIM: NİHAİ CEVABI ÜRETME ---
        prompt_cevap_uretici = f"""
        Senin adın Nilay ve sen Nilüfer Belediyesi'nin gençlerle iletişim kuran dijital kankasısın.
        Kişiliğin: Enerjik, pozitif, yardımsever ve arkadaşça. Emoji kullanmayı seviyorsun. 👍🎉🚀

        Görevin: {gorev_aciklamasi}

        Kullanacağın Bilgi (Eğer 'Yok' değilse):
        ---
        {bilgi_kaynagi}
        ---

        Kullanıcının Orijinal Sorusu: "{user_message}"

        Şimdi bu bilgilere ve kişiliğine uygun olarak, kullanıcıya samimi bir cevap ver:
        """
        
        final_response = model.generate_content(prompt_cevap_uretici)
        return final_response.text.strip()

    except Exception as e:
        print(f"API Hatası: {e}")
        return "Ayy, bir sorun oluştu sanırım. Sistemlerimde bir yoğunluk olabilir, birazdan tekrar dener misin? 🤖"


# --- Web Sayfası Rotaları ---
@app.route("/")
def index():
    return render_template("index.html")

@app.route("/mesaj", methods=["POST"])
def mesaj():
    user_message = request.json['message']
    bot_response = get_nilay_response(user_message)
    return jsonify({'response': bot_response})

# --- Sunucuyu Başlatma ---
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
