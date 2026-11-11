<div align="center">

# framezero

### Twoja najlepsza klatka to klatka zerowa.

**Twórz przykuwające uwagę pionowe wideo promocyjne swojej aplikacji za pomocą HTML, odrobiny JavaScriptu i generowanej kodem muzyki.**
**Bez edytora wideo, bez After Effects, bez muzyki stockowej, bez subskrypcji. Wynik w jakości 4K60 z laptopa lub piaskownicy chmurowej 1 GB.**

Napisane dla **ludzi** *oraz* dla **agentów kodujących AI** (Claude Code, Codex, Cursor, Copilot, Gemini CLI…).

[![smoke](https://github.com/matheusvibecoder-vibecodas/framezero/actions/workflows/smoke.yml/badge.svg)](https://github.com/matheusvibecoder-vibecodas/framezero/actions/workflows/smoke.yml)
[![License: MIT](https://img.shields.io/badge/license-MIT-FFC233)](LICENSE)
[![Agent Skill](https://img.shields.io/badge/Agent%20Skill-ready-6A4BFF)](skills/framezero/SKILL.md)
[![AGENTS.md](https://img.shields.io/badge/AGENTS.md-included-13D18C)](AGENTS.md)
[![PRs welcome](https://img.shields.io/badge/PRs-welcome-FF7A52)](CONTRIBUTING.md)

**[Strona główna](https://matheusvibecoder-vibecodas.github.io/framezero/)** · [English](README.md) · **Polski**

<img src="media/estuda-tour-hook.gif" width="230" alt="film z wycieczki estuda+ — hak">&nbsp;&nbsp;<img src="media/starter.gif" width="230" alt="szablon startowy">&nbsp;&nbsp;<img src="media/estuda-tour-challenge.gif" width="230" alt="film z wycieczki estuda+ — codzienne wyzwanie">

<sub>Lewa/prawa: prawdziwe filmy na TikTok/Reels dla <b>estuda+</b>, darmowej aplikacji do nauki (tekst na ekranie po portugalsku). Środek: angielski szablon startowy w tym repozytorium.</sub>

</div>

---

## Dlaczego to istnieje

Jestem niezależnym programistą z Brazylii. Stworzyłem darmową aplikację do nauki i potrzebowałem filmów na TikTok i Instagram. Edytory były powolne, a wyniki wyglądały powtarzalnie. Zadałem więc pytanie: *co gdyby wideo było po prostu stroną internetową, która wie, co narysować w dowolnym momencie `t`?*

To przekształciło się w mały potok przetwarzania (pipeline). Dzięki niemu w dwa tygodnie stworzyłem pięć filmów promocyjnych, z których każdy był lepszy od poprzedniego. To repozytorium zawiera **potok**, poznane przeze mnie **zasady opowiadania historii** (niektóre nauczone w trudny sposób) oraz **instrukcje, które agent AI może wykonać**, aby stworzyć od zera wideo dla *Twojej* aplikacji.

## Jak to działa (wersja w 30 sekund)
scene.html  ──seek(t)──▶  Zrzuty ekranu Playwright dla każdej klatki  ──▶  ffmpeg  ──▶  video.mp4 (1080p lub 4K60)
soundtrack.py  ──numpy──▶  Muzyka lo-fi + świsty/kliki zsynchronizowane z tą samą osią czasu  ──▶  zmiksowane razem

1. **Scena to jeden plik HTML** (1080×1920) z `const DURATION` oraz czystą funkcją `seek(t)`, która pozycjonuje wszystko dla danej chwili `t`. Nie ma tu żadnych liczników czasu ani animacji CSS. Ponieważ każda klatka jest deterministyczna, każda z nich może być renderowana i przeglądana indywidualnie.
2. **`kit/render.py`** otwiera ją w bezgłowym (headless) Chromium, wywołuje `seek(i/fps)` dla każdej klatki, wykonuje zrzut ekranu i przekazuje potokiem do ffmpeg.
3. **`kit/sound.py`** syntetyzuje muzykę i efekty dźwiękowe z matematyki, dzięki czemu **nie ma żadnego ryzyka naruszenia praw autorskich**. Umieszczasz każdy dźwięk w tej samej sekundzie, w której zachodzi animacja.
4. **`--stills`** renderuje pojedyncze klatki w kilka sekund, dzięki czemu Ty (lub Twój agent) możecie *obejrzeć* wideo przed poświęceniem minut na pełny render.

## Szybki start

```bash
git clone [https://github.com/matheusvibecoder-vibecodas/framezero](https://github.com/matheusvibecoder-vibecodas/framezero) && cd framezero
pip install -r requirements.txt && python3 -m playwright install chromium    # dodaj --with-deps na czystym Linuksie

# 1) obejrzyj kilka klatek (2 sekundy)
python3 kit/render.py templates/starter.html out/shot --stills 0,3.5,6.6,10.9
# 2) stwórz ścieżkę dźwiękową i pełne wideo (1080p30, ~2 min)
python3 templates/soundtrack.py out/soundtrack.wav
python3 kit/render.py templates/starter.html out/starter.mp4 --audio out/soundtrack.wav

# 3) ostateczna jakość: 4K60, tryb podzielony na chunki o niskim zużyciu RAM
python3 kit/render.py templates/starter.html out/starter-4K.mp4 --scale 2 --fps 60 --crf 16 \
        --audio out/soundtrack.wav --frames-dir /tmp/frames
Następnie skopiuj templates/ i dostosuj do siebie: zmień blok CONFIG, przerysuj appUI() (lub wklej zrzuty ekranu) i zachowaj synchronizację czasu ścieżki dźwiękowej.
Korzystanie z agenta kodującego AI
Skieruj swojego agenta na repozytorium i powiedz coś w stylu:

"Przeczytaj AGENTS.md. Zrób pionowe promo aplikacji trwające 15–25 s (zrzuty ekranu w ./shots). Hakiem ma być perspektywa pierwszoosobowa (POV). Muzyka lo-fi. Pokaż mi pojedyncze klatki (stills) przed wyrenderowaniem."

AGENTS.md to podręcznik operacyjny: przepływ pracy, twarde zasady, pętla kontroli jakości (QA) i znane pułapki. Claude Code, Codex, Cursor, Gemini CLI i Copilot od razu go wyłapują.

skills/framezero/SKILL.md to ta sama wiedza w formie instalowalnego Skillu Agenta. Skopiuj folder do ~/.claude/skills/ lub do katalogu umiejętności swojego agenta.

llms.txt to mapa repozytorium dla modeli językowych (LLM).

Przepływ pracy został zaprojektowany wokół tego, w czym agenci są dobrze wyszkoleni (pisanie kodu deterministycznego) i w czym są słabi (ocena ruchu, którego nie widzą). Rozwiązaniem są arkusze kontaktowe pojedynczych klatek: agenci mogą na nie spojrzeć i je ocenić. Jedna zasada ma największe znaczenie: "wzrok wskazuje, DOM decyduje." Użyj zrzutu ekranu, aby wykryć problem, a następnie potwierdź go, mierzć element.

Podręcznik (co naprawdę przyciąga uwagę odbiorców)
Zasada	Dlaczego
Klatka 0 to miniatura i hak. Cały tekst haka jest w pełni widoczny przy t=0. Bez rozjaśniania (fade-in) i bez czarnego wstępu.	Ludzie decydują w mniej niż sekundę, a pierwsza klatka pojawia się w siatce filmów.
Kontekst do 3. sekundy ("5 rzeczy, które robi"), a następnie przełamanie schematu co 2–4 s.	Użyj nowego koloru, przybliżenia, etykiety lub dźwięku, aby zresetować uwagę.
Pokaż prawdziwy produkt. Użyj prawdziwych ekranów w telefonie oraz ruchów kamery i etykiet.	Widzowie bardziej ufają interfejsowi użytkownika (UI) niż przymiotnikom.
Zostaw najlepsze na koniec i powiedz o tym ("ostatnia rzecz jest najlepsza").	Otwarta pętla utrzymuje uwagę oglądających.
Tylko tekst, duży, w bezpiecznej strefie (x 80–940, y 220–1480 przy 1080×1920).	Większość ludzi ogląda filmy bez dźwięku, a interfejs TikToka/Reels zasłania krawędzie.
Każdemu zdarzeniu wizualnemu towarzyszy dźwięk. Świst przed cięciami, uderzenie przy uderzeniach, kliknięcie przy etykietach, dźwięk monety przy nagrodach.	Dźwięk sprawia, że ruch wydaje się fizyczny, nawet przy niskiej głośności.
Płynna pętla. Ostatnie 0,4 s płynnie wraca do klatki 0.	Powtórzone odtworzenia się liczą.
Zakończ wezwaniem do działania (CTA) dopasowanym do Twojego etapu. Przed startem: "wkrótce · zaobserwuj, aby dowiedzieć się, kiedy wystartujemy".	Wezwanie typu "link w bio" prowadzące donikąd niszczy zaufanie.
Pełny przewodnik: docs/.

Prezentacja: seria estuda+
Wszystkie te materiały zostały stworzone za pomocą tego zestawu, a każdy z nich ma dźwięk i wzorzec 4K60.

#4 Wycieczka po aplikacji (39 s), "POV: Znalazłem aplikację, która uczy się ze mną". Pokazuje 5 funkcji na prawdziwych ekranach, z paskiem postępu w stylu Stories i ścieżką lo-fi. → examples/estuda-tour

#3 Quiz codzienne wyzwanie (33,5 s), "Założę się, że nie zdobędziesz wszystkich 3 punktów". Stworzony, aby prowokować komentarze.

#2 Korepetytor AI (25 s), "Utknąłeś przy zadaniu domowym o 23:47?"

Wnioski wyciągnięte po drodze, w tym niepowodzenia, znajdują się w docs/08-case-study-estuda.md.

Stworzyłeś coś za pomocą framezero?
Otwórz zgłoszenie w zakładce Show your video. Najlepsze z nich zostaną tu wyróżnione. Jesteś nowy w kodzie? Spróbuj rozwiązać good first issue lub przeczytaj CONTRIBUTING.md.

Chcesz zobaczyć film o framezero? Znajduje się w examples/framezero-promo/, a plik MP4 jest dołączony do wydania v0.1.0.

Mapa repozytorium
kit/          silnik — render.py, assemble.sh (4K w 1 GB RAM), motion.js (pomocnicy), sound.py (syntezator), base.css (Inter), icons.svg
templates/    starter.html + soundtrack.py — kompletne 12,6-sekundowe angielskie promo do skopiowania
examples/     estuda-tour/ — prawdziwy 39-sekundowy film z wycieczki (scena + zrzuty ekranu + ścieżka dźwiękowa)
docs/         01 metoda · 02 fabuła i haki · 03 animacja · 04 telefon i kamera · 05 dźwięk · 06 renderowanie · 07 publikacja · 08 studium przypadku · 09 lista kontrolna QA
skills/       framezero/SKILL.md — Skill Agenta
AGENTS.md     podręcznik operacyjny dla agentów AI
Często zadawane pytania (FAQ)
Dlaczego nie Remotion / After Effects / CapCut? Remotion jest świetny, ale wymaga Reacta i bundlera. After Effects i CapCut są manualne i trudne do obsłużenia przez agenta. framezero to zwykły HTML + JS + Python bez niczego do konfiguracji, a Twój agent zna już wszystkie trzy technologie.

Czy potrzebuję karty graficznej (GPU)? Nie. Renderowanie odbywa się wyłącznie na procesorze (CPU). 39-sekundowe wideo w rozdzielczości 4K60 zajmuje około 23 minut na malutkiej piaskownicy z 1 vCPU, a na laptopie znacznie mniej.

Czy mogę używać popularnych dźwięków z TikToka? Tak. Wyrenderuj wideo z wygenerowaną kodem ścieżką jako bezpiecznym domyślnym podkładem, a następnie wybierz popularny dźwięk w aplikacji podczas publikowania i ścisz oryginalne audio.

Czy muzyka jest naprawdę wolna od praw autorskich? Tak. Jest generowana przez kit/sound.py z fal sinusoidalnych i szumu, bez użycia sampli.

Licencja
Kod i dokumentacja: MIT. Dołączona czcionka Inter jest dostępna na licencji SIL Open Font License. Nazwa, logo oraz zrzuty ekranu aplikacji estuda+ w folderach examples/ i media/ należą do Matheusa Patricio Pessoa Santany. Są one dołączone jako materiał referencyjny i nie są objęte licencją MIT, więc nie używaj ich ponosząc własne materiały wideo. Zobacz NOTICE.md.
