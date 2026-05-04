# 📄 PDF to Markdown Converter

Aplicação web para converter arquivos **PDF, DOCX, TXT, XLS e XLSX** em **Markdown (.md)**, com interface gráfica acessada via browser e executada em container Docker.

---

## ✨ Funcionalidades

- Upload de arquivos via interface web (arrastar e soltar ou seleção)
- Conversão para Markdown preservando estrutura de títulos e tabelas
- Prévia do conteúdo convertido direto no browser
- Download do arquivo `.md` gerado
- Suporte a arquivos de até 50 MB
- Execução isolada em container Docker

---

## 📁 Formatos suportados

| Formato | Extensão |
|---------|----------|
| PDF     | `.pdf`   |
| Word    | `.docx`  |
| Texto   | `.txt`   |
| Excel   | `.xls`   |
| Excel   | `.xlsx`  |

---

## 🚀 Como usar

### Pré-requisitos

- [Docker](https://www.docker.com/products/docker-desktop) instalado
- [Docker Compose](https://docs.docker.com/compose/) (já incluso no Docker Desktop)

### 1. Clone o repositório

```bash
git clone https://github.com/tiagodracena/conversor_fmx_sdd.git
cd conversor_fmx_sdd
```

### 2. Construa a imagem

```bash
docker compose build
```

### 3. Suba o container

```bash
docker compose up -d
```

### 4. Acesse no browser
http://localhost:5000

### 5. Para encerrar

```bash
docker compose down
```

---

## 🗂️ Estrutura do projeto
conversor_fmx_sdd/ 
├── Dockerfile 
├── docker-compose.yml 
├── requirements.txt 
├── app.py # Servidor web Flask 
├── convert.py # Lógica de conversão dos arquivos 
└── templates/ 
└── index.html # Interface web

---

## 🛠️ Tecnologias utilizadas

- **Python 3.12**
- **Flask** — servidor web
- **PyMuPDF (fitz)** — leitura de PDF
- **python-docx** — leitura de DOCX
- **openpyxl** — leitura de XLSX
- **xlrd** — leitura de XLS
- **Docker** — containerização

---

## ⚙️ Variáveis e configurações

Por padrão a aplicação roda na porta `5000`. Para mudar, edite o `docker-compose.yml`:

yaml
ports:
  - "OUTRA_PORTA:5000"

O tamanho máximo de upload é **50 MB**. Para alterar, edite a linha abaixo em `app.py`:

python
app.config["MAX_CONTENT_LENGTH"] = 50 * 1024 * 1024

---

## 📌 Observações

- Arquivos PDF baseados em imagem (escaneados) terão texto vazio, pois não há OCR.
- Os arquivos temporários são armazenados em `/tmp/converter/` dentro do container e não persistem após reinicialização.
- O formato `.doc` (Word antigo) não é suportado — use `.docx`.

---

## 📄 Licença

MIT License — sinta-se livre para usar, modificar e distribuir.
