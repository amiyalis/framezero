<div align="center">

# framezero 🇧🇷

### O melhor quadro do seu vídeo é o quadro zero.

**Faça vídeos verticais de divulgação do seu app (TikTok, Reels, Shorts) com HTML, um pouco de JavaScript e música gerada por código.**
**Sem editor de vídeo, sem música de banco, sem assinatura. Sai em 4K60, até numa máquina de 1 GB de RAM.**

Feito para **pessoas** e para **agentes de IA** (Claude Code, Codex, Cursor, Copilot, Gemini CLI…).

[English](README.md) · **Português**

<img src="media/estuda-tour-hook.gif" width="230" alt="vídeo do estuda+">&nbsp;&nbsp;<img src="media/starter.gif" width="230" alt="template">&nbsp;&nbsp;<img src="media/estuda-tour-challenge.gif" width="230" alt="desafio do dia">

</div>

---

## Por que existe

Sou um dev independente do Brasil. Criei um app de estudos gratuito, o **estuda+**, e precisava de vídeos para o TikTok e o Instagram. Editor de vídeo era lento e o resultado ficava com cara de template. Então pensei: *e se o vídeo fosse só uma página web que sabe o que desenhar em cada instante `t`?*

Virou um sistema pequeno. Com ele fiz 5 vídeos em duas semanas, cada um melhor que o anterior. Este repositório junta **o sistema**, **as regras de roteiro** que aprendi (algumas apanhando) e **instruções que um agente de IA consegue seguir** para fazer o vídeo do *seu* app do zero.

## Como funciona

```
cena.html  ──seek(t)──▶  Playwright fotografa cada quadro  ──▶  ffmpeg  ──▶  video.mp4 (1080p ou 4K60)
trilha.py  ──numpy──▶  música lo-fi + whoosh/pop sincronizados na mesma linha do tempo  ──▶  junta no vídeo
```

1. **Cada cena é um arquivo HTML** (1080×1920) com `const DURATION` e uma função pura `seek(t)`, que posiciona tudo para o instante `t`. Não usa timer nem animação CSS.
2. **`kit/render.py`** abre a cena no Chromium, chama `seek` quadro a quadro, tira print e manda para o ffmpeg.
3. **`kit/sound.py`** cria música e efeitos com matemática, então **não há risco de direitos autorais**.
4. **`--stills`** gera fotos de qualquer instante em segundos, para você (ou o agente) conferir antes da gravação completa.

## Começar

```bash
git clone https://github.com/matheusvibecoder-vibecodas/framezero && cd framezero
pip install -r requirements.txt && python3 -m playwright install chromium

python3 kit/render.py templates/starter.html out/foto --stills 0,3.5,6.6,10.9      # fotos (2 s)
python3 templates/soundtrack.py out/trilha.wav                                     # trilha
python3 kit/render.py templates/starter.html out/video.mp4 --audio out/trilha.wav  # vídeo 1080p
python3 kit/render.py templates/starter.html out/video-4K.mp4 --scale 2 --fps 60 --crf 16 \
        --audio out/trilha.wav --frames-dir /tmp/quadros                           # 4K60
```

## Com um agente de IA

Abra o repositório no seu agente e peça, por exemplo:

> *"Leia o AGENTS.md. Faça um vídeo vertical de 20 s para o meu app (prints em `./prints`), com gancho POV, música lo-fi e texto em português. Me mostre as fotos antes de gravar."*

O [`AGENTS.md`](AGENTS.md) é o manual completo: perguntas, roteiro em tabela, regras, conferência por fotos, som e erros comuns.

## As regras que prendem a atenção

| Regra | Por quê |
|---|---|
| **O quadro 0 é a capa e o gancho.** Todo o texto do gancho já aparece em t=0. | A pessoa decide em menos de 1 segundo |
| **Contexto até o segundo 3** ("5 coisas que ele faz") | Promete o que vem e abre um "loop" ("a última é a melhor") |
| **Algo muda a cada 2–4 s** | Cor nova, zoom, etiqueta e som seguram a atenção |
| **Mostre o app de verdade** | Tela real convence mais que adjetivo |
| **Só texto, grande, na área segura** | A maioria assiste sem som, e os botões do TikTok cobrem as bordas |
| **Todo movimento tem som** | Whoosh antes do corte, impacto na batida, pop na etiqueta |
| **CTA verdadeiro + loop** | Antes de lançar: "em breve · segue pra saber quando lançar" |

O guia completo está em [`docs/`](docs/) (em inglês).

## Licença

O código e a documentação são [MIT](LICENSE). A marca, a logo e as telas do **estuda+** são do autor e servem só de exemplo. Não use nos seus vídeos ([NOTICE.md](NOTICE.md)).

<div align="center"><sub>Feito no Brasil 🇧🇷 por <a href="https://github.com/matheusvibecoder-vibecodas">@matheusvibecoder</a>. Se te ajudou, deixa uma ⭐!</sub></div>
