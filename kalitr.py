import mysql.connector
import mysql.connector.errors
import mysql.connector.errorcode
from bs4 import BeautifulSoup
import requests
import time

mysql_username = input("Mysql | Kullanıcı Adı :")
mysql_password = input("Mysql | Parola :")
mysql_hostname = input("Mysql | Hostname :")
mysql_database = input("Mysql | Oluşturulacak DB İsmini Belirleyin :")
mydb = mysql.connector.connect(host=mysql_hostname,
                                user=mysql_username,
                                    password=mysql_password)








def auto_db(dbname):
    try:
        mydb = mysql.connector.connect(user=mysql_username,
                                       password=mysql_password,
                                       host=mysql_hostname)
        cursor = mydb.cursor()
        query = ("CREATE DATABASE {};".format(dbname))
        cursor.execute(query)
        mydb.commit()
        cursor.close()
        mydb.close()
    except:
        print("[-] Hata ! Aynı isimde başka bir veritabanı mevcut!")
        sor = input("""Varolan veritabanı silinip yeninden yapılandırılsın mı ?
        BİLGİ : Bu sorgu çalıştırılırsa varolan veritabanı silinecektir!

        1 -) Evet
        2 -) Hayır
        """)
        if sor == "1":
            mydb = mysql.connector.connect(user=mysql_username,
                                           password=mysql_password,
                                           host=mysql_hostname)
            cursor = mydb.cursor()
            delete = ("DROP DATABASE {};".format(dbname))
            cursor.execute(delete)
            create = ("CREATE DATABASE {};".format(dbname))
            cursor.execute(create)
            cursor.close()
            mydb.close()

        elif sor == "2":

            pass
        else:
            print("Hatalı Değer Girildi!")


def tablo_olustur(table_name,dbname):
    mydb = mysql.connector.connect(user=mysql_username,
                                   password=mysql_password,
                                   host=mysql_hostname,
                                   database=dbname)
    cursor = mydb.cursor()

    try:
        query = (
            "CREATE TABLE {} (Kullanici_ID VARCHAR(255), Konu_Başlık VARCHAR(255), Yazar VARCHAR(255), Kategori VARCHAR(255), Yanit VARCHAR(255), Gosterim VARCHAR(255), Tarih VARCHAR(255))".format(
                table_name))
        cursor.execute(query)
        cursor.close()
        mydb.close()
    except:
        print("Aynı isimde başka bir tablo mevcut. Yeninden yapılandırılıyor.")
        sql = ("DROP TABLE {}".format(table_name))
        cursor.execute(sql)
        mydb.commit()
        query = (
            "CREATE TABLE {} (Kullanici_ID VARCHAR(255), Konu_Başlık VARCHAR(255), Yazar VARCHAR(255), Kategori VARCHAR(255), Yanit VARCHAR(255), Gosterim VARCHAR(255), Tarih VARCHAR(255))".format(
                table_name))
        cursor.execute(query)
        cursor.close()
        mydb.close()

def veri_ekle(dbname,table, idi, baslik, yazar, kategori, yanit, gosterim, tarih):
    mydb = mysql.connector.connect(user=mysql_username,
                                   password=mysql_password,
                                   host=mysql_hostname,
                                   database=dbname)
    cursor = mydb.cursor()
    sql = (
        "INSERT INTO {} (Kullanici_ID, Konu_Başlık, Yazar, Kategori, Yanit, Gosterim, Tarih) VALUES (%s, %s, %s, %s, %s, %s, %s)".format(
            table))
    val = (idi, baslik, yazar, kategori, yanit, gosterim, tarih)
    cursor.execute(sql, val)
    mydb.commit()
    cursor.close()
    mydb.close()


def sabit_konular(url):
    try:
        id = 1
        site = requests.get(url)
        soup = BeautifulSoup(site.content, "lxml")
        sayfa = soup.find("div", attrs={"class": "PageNav"}).get("data-last")
        while id < int(sayfa) + 1:
            site = requests.get("{}page-{}".format(url, id))
            soup = BeautifulSoup(site.content, "lxml")
            konular = soup.find_all("li", attrs={"class": "discussionListItem visible sticky"})
            kategori = soup.find_all("meta", attrs={"property": "og:title"})
            print("Sayfa : {} Çekiliyor...".format(id))
            for konu in konular:
                yazar = konu.find("a", attrs={"title": "Konuyu açan"}).text
                baslik = konu.find("a", attrs={"class": "PreviewTooltip"}).text
                tarih = konu.find("a", attrs={"class": "dateTime"}).text
                yanit = konu.find("dl", attrs={"class": "major"}).find("dd").text
                goruntulenme = konu.find("dl", attrs={"class": "minor"}).find("dd").text
                kullanici = konu.find("div", attrs={"class": "posterDate muted"}).find("a").get("href")
                for cate in kategori:
                    categor = cate.get("content")
                veri_ekle(mysql_database,"Sabit_Konular", kullanici, baslik, yazar, categor, yanit, goruntulenme, tarih)
            id += 1
    except:
        site = requests.get("{}".format(url))
        soup = BeautifulSoup(site.content, "lxml")
        konular = soup.find_all("li", attrs={"class": "discussionListItem visible sticky"})
        kategori = soup.find_all("meta", attrs={"property": "og:title"})
        for konu in konular:
            yazar = konu.find("a", attrs={"title": "Konuyu açan"}).text
            baslik = konu.find("a", attrs={"class": "PreviewTooltip"}).text
            tarih = konu.find("a", attrs={"class": "dateTime"}).text
            yanit = konu.find("dl", attrs={"class": "major"}).find("dd").text
            goruntulenme = konu.find("dl", attrs={"class": "minor"}).find("dd").text
            kullanici = konu.find("div", attrs={"class": "posterDate muted"}).find("a").get("href")
            for cate in kategori:
                categor = cate.get("content")
            veri_ekle(mysql_database,"Sabit_Konular", kullanici, baslik, yazar, categor, yanit, goruntulenme, tarih)


def konular(url):
    try:
        id = 1
        site = requests.get(url)
        soup = BeautifulSoup(site.content, "lxml")
        sayfa = soup.find("div", attrs={"class": "PageNav"}).get("data-last")
        while id < int(sayfa) + 1:
            site = requests.get("{}page-{}".format(url, id))
            soup = BeautifulSoup(site.content, "lxml")
            konular = soup.find_all("li", attrs={"class": "discussionListItem visible"})
            kategori = soup.find_all("meta", attrs={"property": "og:title"})
            print("Sayfa : {} Çekiliyor...".format(id))
            for konu in konular:
                yazar = konu.find("a", attrs={"title": "Konuyu açan"}).text
                baslik = konu.find("a", attrs={"class": "PreviewTooltip"}).text
                tarih = konu.find("a", attrs={"class": "dateTime"}).text
                yanit = konu.find("dl", attrs={"class": "major"}).find("dd").text
                goruntulenme = konu.find("dl", attrs={"class": "minor"}).find("dd").text
                kullanici = konu.find("div", attrs={"class": "posterDate muted"}).find("a").get("href")
                for cate in kategori:
                    categor = cate.get("content")

                veri_ekle(mysql_database,"Konular", kullanici, baslik, yazar, categor, yanit, goruntulenme, tarih)
            id += 1
    except AttributeError:
        site = requests.get("{}".format(url))
        soup = BeautifulSoup(site.content, "lxml")
        konular = soup.find_all("li", attrs={"class": "discussionListItem visible"})
        kategori = soup.find_all("meta", attrs={"property": "og:title"})
        for konu in konular:
            yazar = konu.find("a", attrs={"title": "Konuyu açan"}).text
            baslik = konu.find("a", attrs={"class": "PreviewTooltip"}).text
            tarih = konu.find("a", attrs={"class": "dateTime"}).text
            yanit = konu.find("dl", attrs={"class": "major"}).find("dd").text
            goruntulenme = konu.find("dl", attrs={"class": "minor"}).find("dd").text
            kullanici = konu.find("div", attrs={"class": "posterDate muted"}).find("a").get("href")
            for cate in kategori:
                categor = cate.get("content")
            veri_ekle(mysql_database,"Konular", kullanici, baslik, yazar, categor, yanit, goruntulenme, tarih)


def sabit_konu_kategoriler():
    print("Sabit Konular Veritabanına Çekiliyor... ")
    brute = ["https://kali-linuxtr.net/forums/kali-linux-hakk%C4%B1nda.4/",
             "https://kali-linuxtr.net/forums/kali-linux-s%C3%BCr%C3%BCmleri.5/",
             "https://kali-linuxtr.net/forums/soru-cevap.6/", "https://kali-linuxtr.net/forums/video.7/",
             "https://kali-linuxtr.net/forums/d%C3%B6k%C3%BCmanlar.8/", "https://kali-linuxtr.net/forums/temalar.9/",
             "https://kali-linuxtr.net/forums/s-s-s.14/", "https://kali-linuxtr.net/forums/information-gathering.94/",
             "https://kali-linuxtr.net/forums/exploitation-tools.98/",
             "https://kali-linuxtr.net/forums/sniffing-spoofing.101/", "https://kali-linuxtr.net/forums/ubuntu.22/",
             "https://kali-linuxtr.net/forums/linux-mint.29/", "https://kali-linuxtr.net/forums/bugtraq.16/",
             "https://kali-linuxtr.net/forums/backbox.23/", "https://kali-linuxtr.net/forums/pardus.24/",
             "https://kali-linuxtr.net/forums/fedora.25/", "https://kali-linuxtr.net/forums/backtrack.26/",
             "https://kali-linuxtr.net/forums/linux-haberleri.27/",
             "https://kali-linuxtr.net/forums/linux-di%C4%9Fer.28/", "https://kali-linuxtr.net/forums/tools.38/",
             "https://kali-linuxtr.net/forums/document.39/", "https://kali-linuxtr.net/forums/video.40/",
             "https://kali-linuxtr.net/forums/centos.48/", "https://kali-linuxtr.net/forums/docker.92/",
             "https://kali-linuxtr.net/forums/di%C4%9Fer.50/", "https://kali-linuxtr.net/forums/raspberry-pi.67/",
             "https://kali-linuxtr.net/forums/arduino.68/", "https://kali-linuxtr.net/forums/ekran-kartlar%C4%B1.69/",
             "https://kali-linuxtr.net/forums/ses-kartlar%C4%B1.70/",
             "https://kali-linuxtr.net/forums/a%C4%9F-ara%C3%A7lar%C4%B1.71/",
             "https://kali-linuxtr.net/forums/%C4%B0%C5%9Flemci.72/",
             "https://kali-linuxtr.net/forums/di%C4%9Fer-donan%C4%B1mlar.73/",
             "https://kali-linuxtr.net/forums/duyurular.31/", "https://kali-linuxtr.net/forums/off-topic.33/",
             "https://kali-linuxtr.net/forums/yeni-%C3%9Cyelerimiz.32/",
             "https://kali-linuxtr.net/forums/hack-haberleri.36/",
             "https://kali-linuxtr.net/forums/e%C4%9Flence-geyik-mizah.34/",
             "https://kali-linuxtr.net/forums/beyin-f%C4%B1rt%C4%B1nas%C4%B1.35/",
             "https://kali-linuxtr.net/forums/web-application-exploits.42/",
             "https://kali-linuxtr.net/forums/exploit-shellcode-archive.43/",
             "https://kali-linuxtr.net/forums/0day-exploitleri.44/",
             "https://kali-linuxtr.net/forums/local-root-exploits.45/",
             "https://kali-linuxtr.net/forums/bug-researchers.46/",
             "https://kali-linuxtr.net/forums/web-g%C3%BCvenlik-a%C3%A7%C4%B1klar%C4%B1.52/",
             "https://kali-linuxtr.net/forums/windows-ailesi.58/",
             "https://kali-linuxtr.net/forums/sosyal-m%C3%BChendislik.59/",
             "https://kali-linuxtr.net/forums/writeup.110/", "https://kali-linuxtr.net/forums/metasploit.53/",
             "https://kali-linuxtr.net/forums/tools.54/", "https://kali-linuxtr.net/forums/adli-bili%C5%9Fim.55/",
             "https://kali-linuxtr.net/forums/kriptografi.60/",
             "https://kali-linuxtr.net/forums/tersine-m%C3%BChendislik.61/",
             "https://kali-linuxtr.net/forums/di%C4%9Fer.56/", "https://kali-linuxtr.net/forums/c-c.75/",
             "https://kali-linuxtr.net/forums/ruby.87/", "https://kali-linuxtr.net/forums/php.91/",
             "https://kali-linuxtr.net/forums/c.77/", "https://kali-linuxtr.net/forums/java.79/",
             "https://kali-linuxtr.net/forums/python.81/", "https://kali-linuxtr.net/forums/perl.83/",
             "https://kali-linuxtr.net/forums/delphi.89/", "https://kali-linuxtr.net/forums/android.85/",
             "https://kali-linuxtr.net/forums/gtk-3-x.10/", "https://kali-linuxtr.net/forums/gtk-2-x.11/",
             "https://kali-linuxtr.net/forums/gtk-1-x.12/", "https://kali-linuxtr.net/forums/wallpaper.13/",
             "https://kali-linuxtr.net/forums/bugtraq-hakkında.17/",
             "https://kali-linuxtr.net/forums/bugtraq-sürümleri.18/", "https://kali-linuxtr.net/forums/soru-cevap.19/",
             "https://kali-linuxtr.net/forums/video.20/", "https://kali-linuxtr.net/forums/dökümanlar.21/",
             "https://kali-linuxtr.net/forums/centos-gpg-keys.49/"]
    for i in brute:
        sabit_konular(i)
        print("[+] Kategori {} Eklendi".format(i))


def normal_konular():
    print("Konular Veritabanına Çekiliyor... ")
    brute = ["https://kali-linuxtr.net/forums/kali-linux-hakk%C4%B1nda.4/",
             "https://kali-linuxtr.net/forums/kali-linux-s%C3%BCr%C3%BCmleri.5/",
             "https://kali-linuxtr.net/forums/soru-cevap.6/", "https://kali-linuxtr.net/forums/video.7/",
             "https://kali-linuxtr.net/forums/d%C3%B6k%C3%BCmanlar.8/", "https://kali-linuxtr.net/forums/temalar.9/",
             "https://kali-linuxtr.net/forums/s-s-s.14/", "https://kali-linuxtr.net/forums/information-gathering.94/",
             "https://kali-linuxtr.net/forums/exploitation-tools.98/",
             "https://kali-linuxtr.net/forums/sniffing-spoofing.101/", "https://kali-linuxtr.net/forums/ubuntu.22/",
             "https://kali-linuxtr.net/forums/linux-mint.29/", "https://kali-linuxtr.net/forums/bugtraq.16/",
             "https://kali-linuxtr.net/forums/backbox.23/", "https://kali-linuxtr.net/forums/pardus.24/",
             "https://kali-linuxtr.net/forums/fedora.25/", "https://kali-linuxtr.net/forums/backtrack.26/",
             "https://kali-linuxtr.net/forums/linux-haberleri.27/",
             "https://kali-linuxtr.net/forums/linux-di%C4%9Fer.28/", "https://kali-linuxtr.net/forums/tools.38/",
             "https://kali-linuxtr.net/forums/document.39/", "https://kali-linuxtr.net/forums/video.40/",
             "https://kali-linuxtr.net/forums/centos.48/", "https://kali-linuxtr.net/forums/docker.92/",
             "https://kali-linuxtr.net/forums/di%C4%9Fer.50/", "https://kali-linuxtr.net/forums/raspberry-pi.67/",
             "https://kali-linuxtr.net/forums/arduino.68/", "https://kali-linuxtr.net/forums/ekran-kartlar%C4%B1.69/",
             "https://kali-linuxtr.net/forums/ses-kartlar%C4%B1.70/",
             "https://kali-linuxtr.net/forums/a%C4%9F-ara%C3%A7lar%C4%B1.71/",
             "https://kali-linuxtr.net/forums/%C4%B0%C5%9Flemci.72/",
             "https://kali-linuxtr.net/forums/di%C4%9Fer-donan%C4%B1mlar.73/",
             "https://kali-linuxtr.net/forums/duyurular.31/", "https://kali-linuxtr.net/forums/off-topic.33/",
             "https://kali-linuxtr.net/forums/yeni-%C3%9Cyelerimiz.32/",
             "https://kali-linuxtr.net/forums/hack-haberleri.36/",
             "https://kali-linuxtr.net/forums/e%C4%9Flence-geyik-mizah.34/",
             "https://kali-linuxtr.net/forums/beyin-f%C4%B1rt%C4%B1nas%C4%B1.35/",
             "https://kali-linuxtr.net/forums/web-application-exploits.42/",
             "https://kali-linuxtr.net/forums/exploit-shellcode-archive.43/",
             "https://kali-linuxtr.net/forums/0day-exploitleri.44/",
             "https://kali-linuxtr.net/forums/local-root-exploits.45/",
             "https://kali-linuxtr.net/forums/bug-researchers.46/",
             "https://kali-linuxtr.net/forums/web-g%C3%BCvenlik-a%C3%A7%C4%B1klar%C4%B1.52/",
             "https://kali-linuxtr.net/forums/windows-ailesi.58/",
             "https://kali-linuxtr.net/forums/sosyal-m%C3%BChendislik.59/",
             "https://kali-linuxtr.net/forums/writeup.110/", "https://kali-linuxtr.net/forums/metasploit.53/",
             "https://kali-linuxtr.net/forums/tools.54/", "https://kali-linuxtr.net/forums/adli-bili%C5%9Fim.55/",
             "https://kali-linuxtr.net/forums/kriptografi.60/",
             "https://kali-linuxtr.net/forums/tersine-m%C3%BChendislik.61/",
             "https://kali-linuxtr.net/forums/di%C4%9Fer.56/", "https://kali-linuxtr.net/forums/c-c.75/",
             "https://kali-linuxtr.net/forums/ruby.87/", "https://kali-linuxtr.net/forums/php.91/",
             "https://kali-linuxtr.net/forums/c.77/", "https://kali-linuxtr.net/forums/java.79/",
             "https://kali-linuxtr.net/forums/python.81/", "https://kali-linuxtr.net/forums/perl.83/",
             "https://kali-linuxtr.net/forums/delphi.89/", "https://kali-linuxtr.net/forums/android.85/",
             "https://kali-linuxtr.net/forums/gtk-3-x.10/", "https://kali-linuxtr.net/forums/gtk-2-x.11/",
             "https://kali-linuxtr.net/forums/gtk-1-x.12/", "https://kali-linuxtr.net/forums/wallpaper.13/",
             "https://kali-linuxtr.net/forums/bugtraq-hakkında.17/",
             "https://kali-linuxtr.net/forums/bugtraq-sürümleri.18/", "https://kali-linuxtr.net/forums/soru-cevap.19/",
             "https://kali-linuxtr.net/forums/video.20/", "https://kali-linuxtr.net/forums/dökümanlar.21/",
             "https://kali-linuxtr.net/forums/centos-gpg-keys.49/"]
    for i in brute:
        konular(i)
        print("[+] Kategori {} Eklendi".format(i))

try:

    if mydb.is_connected():
            db_Info = mydb.get_server_info()
            print("Bağlantı Başarılı... MySQL Version:", db_Info)
            time.sleep(3)
            cursor = mydb.cursor()
            auto_db(mysql_database)
            print("SabitKonular Çekiliyor...")
            tablo_olustur("Sabit_Konular", mysql_database)
            sabit_konu_kategoriler()
            tablo_olustur("Konular", mysql_database)
            normal_konular()
            print("İşlem Tamamlandı...")

except NameError:
    print("Hata MySQL'e bağlantı kurulamadı! Bağlantınızı yada bilgilerini kontrol edin.")
except mysql.connector.errorcode as error:
    print("Hata MySQL'e bağlantı kurulamadı! Bağlantınızı yada bilgilerini kontrol edin. Hata Kodu:", error)
except mysql.connector.errors.ProgrammingError:
    print("Erişim Engellendi! Bilgilerinizi Kontrol Ediniz. ")

finally:
    if (mydb.is_connected()):
        cursor.close()
        mydb.close()
        print("MySQL Bağlantısı Kapatıldı.")

