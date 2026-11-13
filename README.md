# Temel Linux Akademisi 

Linux temellerini tarayıcıda uygulamalı öğrenmek için hazırlanmış, bağımsız ve statik bir eğitim projesi. Sunucu tarafı veya çalışma zamanında internet bağlantısı gerektirmez.

- **47 modül** · **686 simülatör görevi** · **232 VM görevi** · **188 öz test sorusu**
- **Türkçe, Deutsch ve English**
- Harici JavaScript/CSS kitaplığı veya CDN bağımlılığı yok

## Hızlı başlangıç

Python 3 ile proje kökünde yerel bir web sunucusu başlat:

```bash
python3 -m http.server 8000
```

Tarayıcıda <http://localhost:8000/> adresini aç. Tux ikonlu dil seçicisinden Türkçe, Almanca veya İngilizceyi seç. Ana sayfadaki arama modül başlıklarını ve modüllerde özellikle öğretilen komutları bulur.

İlerleme ve tercihler tarayıcının `localStorage` alanında saklanır. Eğitim görevlerini kendi Linux VM'inde/WSL ortamında yapmak önerilir; yerleşik terminal isteğe bağlı bir simülatördür ve gerçek sistem komutlarını çalıştırmaz.

## Proje yapısı

```text
.
├── index.html              # Dil seçici
├── tr/ de/ en/             # Üretilmiş dil sayfaları
├── content/                # Modül kaynakları ve çeviriler
├── shared/                 # Tarayıcı arayüzü ve terminal simülatörü
├── manifest.webmanifest    # PWA kurulumu ve uygulama bilgileri
├── service-worker.js       # Çevrimdışı önbellek
├── icons/                  # Uygulama simgesi
├── tools/build.py          # Kaynak içerikten sayfa üretimi
├── tools/validate.py       # İçerik, sayfa ve dil doğrulaması
└── tests/test_terminal.js  # Terminal motoru testleri
```

`content/` altındaki JSON dosyaları kaynak içeriktir; `tr/`, `de/` ve `en/` altındaki HTML sayfaları `tools/build.py` ile üretilir. Üretilen sayfalar statik barındırmada doğrudan kullanılabilir.

## Geliştirme ve doğrulama

İçeriği yeniden üretmek ve doğrulamak için Python 3 gerekir:

```bash
python3 tools/build.py
python3 tools/validate.py
```

Terminal motoru testlerini Node.js ile çalıştır:

```bash
node tests/test_terminal.js
```

Alternatif olarak JavaScriptCore kullanabilirsin:

```bash
jsc shared/terminal.js tests/test_terminal.js
```

Doğrulayıcı JSON şemalarını, üç dildeki modül eşleşmelerini, üretilmiş sayfaları ve bağlantıları denetler; kullanılabilir bir JavaScript çalışma zamanı varsa motor öz testini de çalıştırır.

## Masaüstüne yükleme ve çevrimdışı kullanım

Site HTTPS üzerinden (ör. GitHub Pages) veya `localhost` üzerinde açıldığında PWA olarak yüklenebilir. Siteyi ilk kez çevrimiçiyken açıp önbelleğin kurulmasını bekle; ardından tarayıcının **Uygulamayı yükle** seçeneğini kullan. Modül sayfaları, stiller ve betikler çevrimdışı kullanım için önbelleğe alınır.

İçeriği yeniden oluşturduğunda `python3 tools/build.py`, çevrimdışı önbellek listesini de günceller. `precache-manifest.js` dosyasını değişikliklerle birlikte yayımla.

## GitHub Pages'de yayınlama

`index.html` ve dil klasörleri statik barındırmaya hazırdır. Değişiklikleri GitHub'a göndermeden önce üretilen sayfaları ve testleri doğrula:

```bash
python3 tools/build.py
python3 tools/validate.py
node tests/test_terminal.js
```

Depoyu GitHub'a gönderdikten sonra **Settings → Pages → Build and deployment** bölümünde **Deploy from a branch** seç; `main` dalını ve `/(root)` klasörünü yayın kaynağı yap. GitHub Actions doğrulama iş akışı, içerik ve testleri her push/PR'da çalıştırır ve üretilen HTML'in güncel kalmasını denetler.

## Katkıda bulunma

Yeni modül ekleme ve içerik kuralları için [CONTRIBUTING.md](CONTRIBUTING.md) dosyasına bak.

## Lisans

Bu projenin kodu ve eğitim içeriği MIT lisansı altındadır. Ayrıntılar için [LICENSE](LICENSE) dosyasına bak.


# Linux-Grundlagenakademie

Ein unabhängiges, statisches Lernprojekt, um Linux-Grundlagen praktisch im Browser zu erlernen. Es benötigt weder eine serverseitige Anwendung noch eine Internetverbindung zur Laufzeit.

- **47 Module** · **686 Simulatoraufgaben** · **232 VM-Aufgaben** · **188 Fragen zur Selbstüberprüfung**
- **Türkisch, Deutsch und Englisch**
- Keine Abhängigkeit von externen JavaScript-/CSS-Bibliotheken oder CDNs

## Schnellstart

Starte mit Python 3 einen lokalen Webserver im Projektverzeichnis:

```bash
python3 -m http.server 8000
```

Öffne im Browser <http://localhost:8000/>. Wähle über die Sprachauswahl mit dem Tux-Symbol Türkisch, Deutsch oder Englisch. Die Suche auf der Startseite findet Modultitel und Befehle, die in den Modulen gezielt vermittelt werden.

Fortschritt und Einstellungen werden im `localStorage` des Browsers gespeichert. Es wird empfohlen, die Lernaufgaben in einer eigenen Linux-VM oder WSL-Umgebung auszuführen. Das integrierte Terminal ist ein optionaler Simulator und führt keine echten Systembefehle aus.

## Projektstruktur

```text
.
├── index.html              # Sprachauswahl
├── tr/ de/ en/             # Generierte Sprachseiten
├── content/                # Modulquellen und Übersetzungen
├── shared/                 # Browseroberfläche und Terminalsimulator
├── manifest.webmanifest    # PWA-Installation und Anwendungsinformationen
├── service-worker.js       # Offline-Cache
├── icons/                  # Anwendungssymbol
├── tools/build.py          # Seitengenerierung aus Quellinhalten
├── tools/validate.py       # Validierung von Inhalten, Seiten und Sprachen
└── tests/test_terminal.js  # Tests der Terminal-Engine
```

Die JSON-Dateien unter `content/` enthalten die Quellinhalte. Die HTML-Seiten unter `tr/`, `de/` und `en/` werden mit `tools/build.py` generiert. Die generierten Seiten können direkt auf einem statischen Hosting-Dienst verwendet werden.

## Entwicklung und Validierung

Für die erneute Generierung und Validierung der Inhalte wird Python 3 benötigt:

```bash
python3 tools/build.py
python3 tools/validate.py
```

Führe die Tests der Terminal-Engine mit Node.js aus:

```bash
node tests/test_terminal.js
```

Alternativ kannst du JavaScriptCore verwenden:

```bash
jsc shared/terminal.js tests/test_terminal.js
```

Der Validator prüft die JSON-Schemata, die Übereinstimmung der Module in allen drei Sprachen sowie die generierten Seiten und Links. Wenn eine JavaScript-Laufzeitumgebung verfügbar ist, führt er auch den Selbsttest der Engine aus.

## Installation auf dem Desktop und Offline-Nutzung

Wenn die Website über HTTPS (z. B. GitHub Pages) oder über `localhost` aufgerufen wird, kann sie als PWA installiert werden. Öffne die Website beim ersten Mal mit Internetverbindung und warte, bis der Cache eingerichtet ist. Verwende anschließend die Browseroption **App installieren**. Modulseiten, Stylesheets und Skripte werden für die Offline-Nutzung zwischengespeichert.

Wenn du die Inhalte neu generierst, aktualisiert `python3 tools/build.py` auch die Liste für den Offline-Cache. Veröffentliche die Datei `precache-manifest.js` zusammen mit den Änderungen.

## Veröffentlichung auf GitHub Pages

`index.html` und die Sprachverzeichnisse sind für statisches Hosting vorbereitet. Validiere die generierten Seiten und führe die Tests aus, bevor du Änderungen an GitHub überträgst:

```bash
python3 tools/build.py
python3 tools/validate.py
node tests/test_terminal.js
```

Nachdem du das Repository auf GitHub hochgeladen hast, wähle unter **Settings → Pages → Build and deployment** die Option **Deploy from a branch**. Lege den Branch `main` und den Ordner `/(root)` als Veröffentlichungsquelle fest. Der GitHub-Actions-Validierungsworkflow prüft bei jedem Push und Pull Request die Inhalte und Tests und kontrolliert, ob das generierte HTML aktuell ist.

## Mitwirken

Informationen zum Hinzufügen neuer Module und zu den Inhaltsregeln findest du in [CONTRIBUTING.md](CONTRIBUTING.md).


# Linux Fundamentals Academy

An independent, static educational project for learning Linux fundamentals through hands-on practice in the browser. It requires no server-side application or internet connection at runtime.

- **47 modules** · **686 simulator tasks** · **232 VM tasks** · **188 self-test questions**
- **Turkish, German, and English**
- No dependencies on external JavaScript/CSS libraries or CDNs

## Quick start

Start a local web server in the project root using Python 3:

```bash
python3 -m http.server 8000
```

Open <http://localhost:8000/> in your browser. Use the language selector with the Tux icon to choose Turkish, German, or English. The search on the home page finds module titles and commands specifically taught in the modules.

Progress and preferences are stored in the browser’s `localStorage`. It is recommended to complete the training tasks in your own Linux VM or WSL environment. The built-in terminal is an optional simulator and does not execute real system commands.

## Project structure

```text
.
├── index.html              # Language selector
├── tr/ de/ en/             # Generated language pages
├── content/                # Module sources and translations
├── shared/                 # Browser interface and terminal simulator
├── manifest.webmanifest    # PWA installation and application information
├── service-worker.js       # Offline cache
├── icons/                  # Application icon
├── tools/build.py          # Page generation from source content
├── tools/validate.py       # Content, page, and language validation
└── tests/test_terminal.js  # Terminal engine tests
```

The JSON files under `content/` contain the source content. The HTML pages under `tr/`, `de/`, and `en/` are generated using `tools/build.py`. The generated pages can be used directly on a static hosting service.

## Development and validation

Python 3 is required to regenerate and validate the content:

```bash
python3 tools/build.py
python3 tools/validate.py
```

Run the terminal engine tests with Node.js:

```bash
node tests/test_terminal.js
```

Alternatively, you can use JavaScriptCore:

```bash
jsc shared/terminal.js tests/test_terminal.js
```

The validator checks the JSON schemas, module correspondence across all three languages, generated pages, and links. If a JavaScript runtime is available, it also runs the engine self-test.

## Desktop installation and offline use

The site can be installed as a PWA when opened over HTTPS (for example, on GitHub Pages) or on `localhost`. Open the site while online for the first time and wait for the cache to be set up. Then use your browser’s **Install app** option. Module pages, stylesheets, and scripts are cached for offline use.

When you regenerate the content, `python3 tools/build.py` also updates the offline cache list. Publish `precache-manifest.js` along with your changes.

## Publishing on GitHub Pages

`index.html` and the language directories are ready for static hosting. Validate the generated pages and run the tests before pushing changes to GitHub:

```bash
python3 tools/build.py
python3 tools/validate.py
node tests/test_terminal.js
```

After pushing the repository to GitHub, select **Deploy from a branch** under **Settings → Pages → Build and deployment**. Set the `main` branch and the `/(root)` folder as the publishing source. The GitHub Actions validation workflow checks the content and runs the tests on every push and pull request, and verifies that the generated HTML is up to date.

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for information on adding new modules and content guidelines.
````
