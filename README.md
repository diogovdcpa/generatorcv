# GeneratorCV ✨

GeneratorCV e um gerador de curriculo em Flask que cria um PDF elegante a partir de um formulario simples.
O usuario comeca em uma landing page, segue para o formulario e faz o download do
curriculo pronto em segundos. 🚀

## Destaques 🌟

- Landing page com apresentacao da aplicacao
- Formulario completo para dados profissionais
- Geracao de PDF com layout limpo
- Templates Jinja + Tailwind via CDN
- Pronto para deploy no Vercel

## Stack 🧰

- Flask
- Jinja2
- Tailwind CSS (CDN)
- ReportLab para PDF

## Rotas 🔗

- GET `/` landing page
- GET `/form` formulario de curriculo
- POST `/generate` gera e baixa o PDF

## Rodar localmente 🧪

```bash
python -m venv .venv
source .venv/bin/activate
pip install flask gunicorn reportlab
flask --app main run
```

A aplicacao fica disponivel em `http://127.0.0.1:5000`.

## Deploy ☁️

Deploy com Vercel usando a runtime Python. Basta conectar o repositorio e publicar.
