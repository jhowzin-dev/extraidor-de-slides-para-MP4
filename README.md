# 🎬 Extraidor de Slides para MP4

[![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white)]()
[![Flask](https://img.shields.io/badge/Flask-3.x-000000?style=for-the-badge&logo=flask&logoColor=white)]()
[![FFmpeg](https://img.shields.io/badge/FFmpeg-Necess%C3%A1rio-007808?style=for-the-badge&logo=ffmpeg&logoColor=white)]()
[![License](https://img.shields.io/badge/Licen%C3%A7a-MIT-blue.svg?style=for-the-badge)]()

Uma aplicação web intuitiva e eficiente para **extrair automaticamente slides estáticos de videoaulas, apresentações e gravações de reuniões em formato MP4**, eliminando a necessidade de tirar capturas de tela manualmente.

---

## 📌 Sumário

- [Visão Geral](#-visão-geral)
- [Funcionalidades](#-funcionalidades)
- [Como Funciona](#-como-funciona)
- [Estrutura do Projeto](#-estrutura-do-projeto)
- [Pré-requisitos](#-pré-requisitos)
- [Instalação](#-instalação)
- [Como Usar](#-como-usar)
- [Tecnologias Utilizadas](#-tecnologias-utilizadas)
- [Licença](#-licença)

---

## 🎯 Visão Geral

O **Extraidor de Slides** analisa arquivos de vídeo em busca de trocas de telas/slides utilizando algoritmos de comparação de imagem. Ao identificar que o conteúdo da apresentação mudou significativamente, ele captura o frame e o organiza para download direto em um arquivo `.zip`.

 Perfeito para estudantes, professores e profissionais que desejam converter gravações de chamadas ou aulas em material de estudo estático.

---

## ✨ Funcionalidades

- **Detecção de Mudança de Cena:** Identificação automática das transições de slide.
- **Intervalos de Amostragem Configuráveis:** Opção de checagem a cada **5s**, **8s** ou **15s** para equilibrar precisão e tempo de processamento.
- **Interface Intuitiva (Drag & Drop):** Arraste e solte o vídeo diretamente na página web.
- **Download Simplificado:** Exportação de todas as imagens capturadas compactadas em um arquivo `.ZIP`.
- **Suporte a Arquivos Grandes:** Suporta upload de arquivos de vídeo de até **2GB**.
- **Pré-visualização:** Exibição imediata dos slides extraídos na própria interface antes do download.

---

## 🔬 Como Funciona

A extração utiliza a técnica de **Hash Perceptual / Diferença de Pixels**:

1. **Amostragem:** O vídeo é processado em intervalos definidos pelo usuário (ex: a cada 5 segundos) extraindo frames via **FFmpeg**.
2. **Normalização:** A imagem é convertida para escala de cinza e redimensionada para uma resolução padrão de comparação.
3. **Comparação:** Cada frame é comparado pixel por pixel com o slide extraído anteriormente.
4. **Limiar de Tolerância (Threshold 8%):** Se a variação visual entre os frames for superior a **8%**, o algoritmo considera que um novo slide foi apresentado e salva a imagem.

---

## 📁 Estrutura do Projeto

```text
extraidor-slides/
├── app/
│   ├── __init__.py           # Inicialização do app Flask
│   ├── routes.py             # Rotas do sistema (Upload, Processamento, Download)
│   ├── services/
│   │   ├── extractor.py      # Lógica de extração e comparação de frames
│   │   └── ffmpeg_helper.py  # Wrapper para comandos do FFmpeg
│   ├── static/
│   │   ├── css/              # Estilos da interface
│   │   └── js/               # Lógica do front-end (Upload, Drag-and-Drop)
│   └── templates/
│       └── index.html        # Página principal da aplicação
├── uploads/                  # Diretório temporário para processamento dos vídeos
├── run.py                    # Script de inicialização da aplicação
├── requirements.txt          # Dependências do Python
└── README.md                 # Documentação do projeto
