[Application Link](https://trading-inventory.adaptable.app)
<h1 style='color:red'> Tugas 3 </h1>

# Cara Implementasi

## Membuat Form (`forms.py`)

`APP/forms.py` akan mengimplementasikan library `django.forms` yang akan mempermudah pembuatan form kita. Seluruh html sudah dihandle oleh library form tersebut. Contoh isi `APP/forms.py` adalah.
```python
from main.models import Item
class ItemForm(ModelForm):
    class Meta:
        model = Item
        fields = ['name', 'amount', 'buy_price', 'description']
```
dimana `name`, `amount`, `buy_price`, dan `description` adalah field yang ada pada model `Item` yang sudah didefinisikan.

## Merender form yang dibuat

Untuk merender form yang sudah kita buat, kita dapat menggunakan kemudahan library django. Pada `html` yang akan kita buat, kita dapat menulis.
```html
<form method="POST">
    {% csrf_token %}
    <table>
        {{ form.as_table }}
        <tr>
            <td></td>
            <td>
                <input type="submit" value="Add Product"/>
            </td>
        </tr>
    </table>
</form>
```
`csrf_token` token wajib didefinisikan setiap definisi form, hal ini terkait dengan keamanan. `form.as_table` akan merender form secara keseluruhan kecuali button submit yang perlu kita tulis sendiri. Jika ingin memodifikasi form agar lebih estetik, kita dapat menggunakan attribut dari `form` seperti `form.visible_fiels`, `form.hidden_fields` dan sebagainya yang tertera pada [dokumentasinya](https://docs.djangoproject.com/en/4.2/topics/forms/).

## Menambahkan view untuk serializer json dan xml

Serializer digunakan untuk mengirim data dalam bentuk `json` dan `xml`. Data ini dapat digunakan sebagai interface program lain (API). Dalam django, serializer diimplementasikan pada `views.py` dengan mereturn `HTTPResponse` dengan `application_type` `application/json` atau `application/xml`. Berikut contoh kodenya.
```python
from django.core import serializers
from main.models import Item
def show_xml(request):
    data = Item.objects.all()
    return HttpResponse(serializers.serialize('xml', data), content_type='application/xml')
```
```python
def show_json(request):
    data = Item.objects.all()
    return HttpResponse(serializers.serialize('json', data), content_type='application/json')
```

## Membuat getter dengan dynamic routing

Dynamic routing digunakan untuk menyesuaikan data dengan input dari user melalui url. Contoh, jika kita ingin mendapatkan `Item` **pertama** pada database kita dapat menuju url `www.outapp/1`. Implementasinya pada django dengan mengubah `urls.py` dan `views.py`. Pada `urls.py`
```python
from django.urls import path

urlpatterns = [
    ...
    path('xml/<int:id>', views.show_xmlbyid, name='xmlbyid'),
    path('json/<int:id>', views.show_jsonbyid, name='jsonbyid'),
]
```
Sedangkan pada `views.py`
```python
def show_xmlbyid(request, id: int):
    data = Item.objects.filter(pk=id)
    print(data)
    return HttpResponse(serializers.serialize('xml', data), content_type='application/xml')

def show_jsonbyid(request, id: int):
    data = Item.objects.filter(pk=id)
    return HttpResponse(serializers.serialize('json', data), content_type='application/json')
```

## Perbedaan antara POST dan GET pada Django?

**POST** adalah method protokol `HTTP` yang berfokus pada pengiriman data. Pengiriman data pada `POST` dikirim melalui body request membuatnya tidak mudah terlihat. `POST` biasanya digunakan saat melakukan update data kepada server seperti *sign up*, upload file, dan sebagainya

**Get** adalah method protokol `HTTP` yang fokus pada simplisitas. Data yang dikirim akan disimpan pada `url` yang dituju. Contohnya pada saat mencari video pada youtube, url yang kita tuju akan berpola `youtube.com/results?search_query=[KEYWORD PENCARIAN]`. Dikarenakan pengiriman data yang terjadi pada url, method `GET` tidak cocok untuk mengirim data rahasia seperti data saat *sign up*. Bayangkan jika kalian `sign up` pada sebuah website dengan url `insta.com/signup/username=eryaw&passowrd=joget`, akan menjadi aneh bukan?. `GET` method cocok untuk mendapatkan data seperti file html website yang perlu kita render (yang biasa kita lakukan), query database `insta/user/eryawwww` untuk mendapatkan user `eryawww` dan sebagainya.

## Perbedaan utama antara XML, JSON, dan HTML dalam konteks pengiriman data?

**HTML** digunakan untuk mengirin sebuah halaman dengan segala peletakan desain, kontennya, script, dan sebagainya. `HTML` lebih cocok jika client adalah manusia yang menggunakan browser. Jika client merupakan sebuah applikasi untuk mengambil data otomatis (API), `HTML` akan lebih susah dipahami karena diperlukan parsing terlebih dahulu yang memakan waktu dan tidak efisien.
```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Document</title>
</head>
<body>
    <div class="row container-fluid bg-dark py-2 px-3 m-0">
        <a class="col text-white h-6" style="text-decoration: none;"><strong>Trading Inventory</strong></a>
        <a class="col text-end text-white" style="text-decoration: none;"><strong>69</strong> Saved Data</a>
    </div>
</body>
</html>
```

**XML** adalah format yang machine & human readable tidak seperti `HTML`. Struktur `XML` mirip seperti `tree` yang memiliki satu root. Struktur `XML` sangat mirip dengan `HTML` pada dasarnya. Setiap `node` pada `tree` ditandai dengan symbol `<>`. Setiap node dapat memiliki banyak `properti`. Karena format `XML` yang machine readable, `XML` sering dijadikan opsi untuk mengirim data sebagai **API**.
```xml
<django-objects version="1.0">
    <link type="text/css" rel="stylesheet" id="dark-mode-custom-link"/>
    <link type="text/css" rel="stylesheet" id="dark-mode-general-link"/>
    <style lang="en" type="text/css" id="dark-mode-custom-style"/>
    <style lang="en" type="text/css" id="dark-mode-native-style"/>
    <object model="main.item" pk="1">
        <field name="name" type="CharField">BBCA</field>
        <field name="amount" type="IntegerField">20</field>
        <field name="buy_price" type="FloatField">20000.0</field>
        <field name="time_buy" type="DateTimeField">2023-09-06T13:41:49.801270+00:00</field>
        <field name="description" type="TextField">fomo</field>
    </object>
</django-objects>
``` 

**JSON** adalah format machine & human readable. Format json adalah format yang paling sering digunakan baru-baru ini. Salah satu alasannya adalah dikarenakan simplisitasnya. Json tidak memakan banyak tempat sehingga sangat mudah untuk dibaca manusia. Container pada json yang menggunakan `Dictionary` dan `List` membuatnya sangat mudah untuk dibaca mesin/programmer API.
```json
[
    {
        "model": "main.item", 
        "pk": 1, 
        "fields": {
            "name": "BBCA", 
            "amount": 20, 
            "buy_price": 20000.0, 
            "time_buy": "2023-09-06T13:41:49.801Z", 
            "description": "fomo"
        }
    }
]
```

## Mengapa JSON sering digunakan dalam pertukaran data antara aplikasi web modern?

**JSON** sering digunakan sebagai pertukaran data antar applikasi (API) dikarenakan sifatnya yang machine readable. Pada `JSON`, terdapat `dictionary` dan `list` sebagai kontrainer yang merupakan container yang sering dipakai oleh para pemrogram. Penulisan **JSON** lebih singkat dibandingkan `XML` membuatnya efisien secara ukuran dan lebih human readable. 

# Screenshot Postman
Gambaran untuk response untuk endpoint `html`
<img src='doc/postman_html.png' width=100%>

Gambaran untuk response untuk endpoint `/xml` dan `/xml/1`
<div style='display: flex;'>
    <img src='doc/postman_xml.png' width=50%>
    <img src='doc/postman_xmlid.png' width=50%>
</div>

Gambaran untuk response untuk endpoint `/json` dan `/json/1`
<div style='display: flex;'>
    <img src='doc/postman_json.png' width=50%>
    <img src='doc/postman_jsonid.png' width=50%>
</div>

-----

<h1 style='color:red'> Tugas 2 </h1>

# Cara Implementasi

## Setup Library yang dibutuhkan

Membuat file `requirements.txt` yang berisi
```
django
gunicorn
whitenoise
psycopg2-binary
requests
urllib3
```
Installasi dapat dilakukan pada terminal dengan:
1. Tanpa Virtual Environment
```sh
pip install -r requirements.txt
```
2. Menggunakan Virtual Environment
```sh
python -m venv venv # Buat virtual env
./venv/Scripts/activate # pada windows atau
source venv/Scripts/activate # pada mac
pip install -r requirements.txt
```

## 1. Membuat sebuah proyek Django baru

Menggunakan `django-admin createproject NAME` kita akan membuat direktori baru dengan nama `NAME`. Direktori akan berisi `manage.py` dan folder `NAMA` yang berisi terkait setting dan routing dari proyek. `manage.py` adalah script python yang akan kita gunakan untuk memantain dan mengatur proyek kita. `python manage.py runserver` adalah command untuk menjalankan proyek kita (**Pastikan untuk menjalankan ini sebelum menuju `http://localhost:8000/hello` yang merupakan url web django kita**).

## 2. Membuat aplikasi dengan nama main

`python manage.py createapp APPNAME` digunakan untuk membuat applikasi pada proyek kita dengan nama `APPNAME`. Applikasi dalam bentuk folder baru dengan nama `APPNAME`. Setelah membuat applikasi, kita perlu mendaftarkannya pada `settings.py` yang terletak di folder proyek. Tambahkan `APPNAME` pada `INSTALLED_APPS` sehingaa berbentuk seperti
```python
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'APPNAME'
]
```
## 3. Melakukan routing proyek agar dapat menjalankan aplikasi
Konfigurasi link `APPNAME` pada proyek dengan cara menambahkan `path('aplikasi/', include('main.urls'))` pada `urls.py` yang terletak di direktori proyek. Sehingga kurang lebih seperti
```python
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('iniapp', include('main.urls'))
]

```
Buatlah `urls.py` pada folder `APPNAME` dengan kode:
```python
from django.urls import path
from . import views

urlpatterns = [
	path('hello/', views.hello),
]
```
Dengan begini ketika kita menuju `http://localhost:8000/iniapp/hello` pada browser, kita akan dihadapkan dengan apa yang direturn fungsi `hello` pada `views.py`
Jika kita ingin applikasi langsung berada pada main path seperti `http://localhost:8000/hello`, kita bisa set `urlpatterns` pada `urls.py` proyek dengan `path('', include('main.urls'))`

## 4. Membuat fungsi render pada views.py
Untuk mengatur apa yang ingin user lihat ketika menuju `http://localhost:8000/hello`, kita dapat mengembalikan html templates.
Buat direktori `templates` pada `APPNAME` dan masukan html yang akan dirender dengan nama `hello.html`. Contoh `hello.html` yang akan menampilkan nama dan kelas.
```html
<head>
<title>Trading Inventory</title>
</head>
<body>
<h1>Nama : Eryawan Presma Yulianrifat</h1>
<h1>Kelas : PBP D</h1>
</body>
```
pada `views.py` kita dapat mengembalikan `hello.html` dengan cara
```python
from django.shortcuts import render
from django.http import HttpResponse

def main(request):
    return render(request, 'hello.html')
```
Perubahan dapat dilihat langsung pada `http://localhost:8000/hello`.

## 5. Membuat model sebagai Database
Model adalah penghubung python dengan database kita. Model pada `APPNAME` berada pada `models.py`. Jika kita ingin membuat database yang berisi nama, amount, dan description masing-masing dengan tipe data character, integer, dan text kita dapat melakukannya dengan memodif `models.py` seperti
```python
from django.db import models

class Item(models.Model):
    name = models.CharField(max_length=4)
    amount = models.IntegerField()
    description = models.TextField()
```
    Mengkoneksikan database dengan view akan dibahas dikemudian hari setelah tutorial PBP selanjutnya xixi.
 
## Melakukan deployment ke Adaptable
Pastikan repository proyek sudah berada pada github dan bersifat public. Selanjutnya, pada adaptable, pilih opsi `deploy a new app`. Pilih repository sesuai proyek yang akan dideploy. Kemudian `Python App Template`. Selanjutnya adalah opsi database, sementara bisa menggunakan `PostgreSQL`. Sesuaikan versi python dengan versi lokal, `python --version` pada terminal lokal untuk melihat versi. Dan masukan `python manage.py migrate && gunicorn NAMA_PROYEK.wsgi` pada `Start Command`. Tentukan nama applikasi dan checklist `HTTP Listener on PORT`.

# Bagan Applikasi Berbasis Django
![Bagan](doc/django_architecture.png)

1. Client memerintahkan browser untuk mengunjungi situs berbasis django (ex: instagram.com)
2. Browser akan mengirimkan permintaan (HTTP Request) webpage/halaman web kepada server instagram.com
3. Request akan sampai pada routing yang dihandle pada `urls.py` yang akan mencari pattern url yang dituju oleh client
4. Setelah pattern ditemukan, django akan memanggil fungsi pada `views.py` terkait yang terikat terhadap url tersebut.
5. `views.py` dapat melakukan logika dan operasi database yang terdefinisi arsitekturnya pada `models.py`
6. Setelah operasi selesai, `views.py` akan mengirimkan webpage/halaman web yang diminta client dalam bentuk html yang terdapat pada direktori `templates/`.
7. Browser client merender `html` yang merupakan response (HTTP Response) dari server django.

# Mengapa Virtual Environment
Virtual Environment berguna untuk memanage package python secara terisolasi dari package python sistem kita. Dengan kata lain, kita semacam memiliki python yang berbeda-beda untuk tiap proyek kita. `./venv/Scripts/activate` berguna untuk memberikan instruksi pada shell bahwa kita akan menggunakan virtual environment python. `deactivate` memerintahkan shell untuk kembali ke python sistem. `pip install -r requirements.txt` berguna untuk menginstall package yang ada pada `requirements.txt` (library yang digunakan proyek kita). Isolasi virtual env berguna untuk membuat orang lain yang ingin menggunakan proyek kita mengetahui apa yang mereka perlukan. Sehingga mereka menginstall library secukupnya saja, tidak semuanya pada sistem python kita. Bayangkan jika hendak menjalankan proyek django tapi kita diminta untuk menginstall tensorflow.

Membuat proyek django tanpa virtual env dapat dilakukan asalkan python sistem kita kita memiliki semua depedensi yang akan digunakan.

# Apa itu MVC, MVT, MVVM
1. **MVC** (Model View Controller) adalah pattern desain framework yang memisahkan applikasi menjadi 3 komponen, yaitu model, view, dan controller. MVC adalah komponen yang sering digunakan industri untuk membuat applikasi yang scalable dan extensible.
<img src=https://miro.medium.com/v2/resize:fit:1400/1*hTlpGXMh9EFefBIT9NrTDQ.png width=500 height=250/>

2. **MVT** (Model View Template) adalah pattern desain yang mirip dengan MVC. Perbedaannya adalah controller diimplementasikan oleh framework sendiri sehingga kita hanya perlu membuat template. Memungkinkan untuk pengembangan yang lebih scalable, cepat, namun terdapat ketergantungan terhadap framework yang digunakan.
<img src=https://miro.medium.com/v2/resize:fit:1400/0*8ZFh-CsrMi7bQG0O.jpg width=500 height=250/>

3. **MVVM** (Model View ViewModel) adalah pattern desain yang fokus pada membedakan user interface (UI) dengan logic dari applikasi kita. Controller pada MVVM berada pada ViewModel. Memungkinkan untuk pemisahan kerja yang lebih baik antara UI dan logic sesuai dengan kelebihan pengembang. ViewModel dapat terlihat sangat kompleks dan susah didebug jika sudah terdapat banyak logic dan binding. 
<img src=https://media.geeksforgeeks.org/wp-content/uploads/20201002215007/MVVMSchema.png width=500 height=250/>