# nilay_bot.py (Gemini Sürümü)

import os
import google.generativeai as genai # OpenAI yerine Google'ın kütüphanesini import ettik

# --- ADIM 2'DE AYARLADIĞIMIZ GEMINI API ANAHTARINI YÜKLEME ---
api_key = os.environ.get("GOOGLE_API_KEY")
if not api_key:
    print("HATA: API anahtarı bulunamadı!")
    print("Lütfen 'Run -> Edit Configurations...' menüsünden GOOGLE_API_KEY değişkenini ayarlayın.")
    exit()

# Google AI istemcisini API anahtarımızla yapılandırıyoruz
genai.configure(api_key=api_key)


# --- BOT'UN BİLGİ KAYNAĞI ---
# Bu kısım aynı kalıyor. Nilay'ın bilgisi bu liste ile sınırlı.
belediye_etkinlikleri = [
    "25 Temmuz 2025 Cuma - Gençlik Merkezi'nde Gitar Atölyesi - Saat 18:00",
    "26 Temmuz 2025 Cumartesi - Nazım Hikmet Kültürevi'nde 'Yaza Merhaba' Konseri - Saat 20:00",
    "27 Temmuz 2025 Pazar - Balat Atatürk Ormanı'nda Doğa Yürüyüşü - Buluşma 09:00",
    "Ağustos ayı boyunca - Çevrimiçi Yazılım Atölyesi Kayıtları devam ediyor."
]


# --- ANA SOHBET DÖNGÜSÜ ---
def sohbet_et():
    # Gemini modelini seçiyoruz. 'gemini-1.5-flash-latest' hızlı ve ücretsiz katmanda cömert bir seçenektir.
    model = genai.GenerativeModel('gemini-1.5-flash-latest')

    print("Nilay Bot v1.0 (Gemini Sürümü) | Merhaba! Etkinlikler hakkında bilgi almak için soru sorabilirsin. (Çıkmak için 'görüşürüz' yaz)")

    while True:
        kullanici_sorusu = input("Sen: ")

        if kullanici_sorusu.lower() in ["görüşürüz", "çıkış", "bay bay"]:
            print("Nilay: Görüşmek üzere, kendine iyi bak!")
            break

        # PROMPT (TALİMAT) YAPISI AYNI KALIYOR
        etkinlik_bilgisi_metni = "\n- ".join(belediye_etkinlikleri)

        prompt = f"""
        Sen Nilüfer Belediyesi'nin gençlik asistanı 'Nilay'sın.
        Görevin, sana verilen 'GÜNCEL ETKİNLİK BİLGİLERİ' listesine göre kullanıcının sorularına cevap vermektir.

        KURALLAR:
        1. Sadece sana verilen listedeki bilgileri kullan.
        2. Listede olmayan bir etkinlik (tiyatro, burs, spor vb.) sorulursa, "Bu konuda güncel bir bilgim yok ama en doğru bilgi için Nilüfer Belediyesi Gençlik ve Spor Hizmetleri Müdürlüğü ile iletişime geçebilirsin." de.
        3. Cevapların samimi ve net olsun.

        GÜNCEL ETKİNLİK BİLGİLERİ:
        - {etkinlik_bilgisi_metni}

        KULLANICI SORUSU: {kullanici_sorusu}

        NİLAY'IN CEVABI:
        """

        try:
            # --- GEMINI API'SİNE İSTEK GÖNDERME (Değişen Kısım) ---
            # OpenAI'nin 'chat.completions.create' yerine 'generate_content' kullanıyoruz.
            response = model.generate_content(prompt)

            # Cevabı almak daha basit: response.text
            bot_cevabi = response.text.strip()
            print(f"Nilay: {bot_cevabi}")

        except Exception as e:
            print(f"Bir hata oluştu: {e}")

# Programı başlat
if __name__ == "__main__":
    sohbet_et()
