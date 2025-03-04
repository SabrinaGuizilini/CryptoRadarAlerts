# CryptoRadarAlerts - Alertas de Criptomoedas 🚀

CryptoRadarAlerts é um script automatizado que monitora os preços de criptomoedas e envia alertas por e-mail quando um valor predefinido de alta ou baixa é atingido. O projeto utiliza Firebase Firestore para armazenar os dados para os alertas, o pycoingecko para obter cotações em tempo real e um workflow do GitHub Actions para execução programada três vezes ao dia.

## 🔧 Tecnologias e Bibliotecas Utilizadas

- **Python 3.9+**
- **Firebase Firestore** (armazenamento de alertas)
- **pycoingecko** (obtenção de preços)
- **smtplib** (envio de e-mails)
- **ssl** (segurança no envio de e-mails)
- **babel** (formatação de valores monetários)
- **pytz** (garantia de fuso horário do Brasil)
- **GitHub Actions** (execução programada do script)

## 📂 Estrutura do Projeto

```
CryptoRadarAlerts/
│── retrieve_data.py      # Busca alertas ativos no Firestore e obtém cotações
│── send_email.py         # Envia e-mails com os alertas
│── .github/workflows/    # Configuração do GitHub Actions
│── requirements.txt      # Lista de dependências do projeto
│── README.md             # Documentação do projeto
```

## 🚀 Como Rodar o Projeto Localmente

### 1. Clone o repositório:

```sh
git clone https://github.com/SabrinaGuizilini/CryptoRadarAlerts.git
cd CryptoRadarAlerts
```

### 2. Crie um ambiente virtual e instale as dependências:

```sh
python -m venv venv  # Criação do ambiente virtual
source venv/bin/activate  # Ativação do ambiente no Linux/macOS
venv\Scripts\activate  # Ativação do ambiente no Windows
pip install -r requirements.txt  # Instalação das dependências
```

### 3. Crie um projeto no Firebase

- Acesse <https://console.firebase.google.com/>, crie um projeto e um banco de dados no Firestore.
- Em seguida crie uma coleção com o nome "alerts".
- Cada documento da coleção deve ter os campos utilizados na função "retrieve_active_alerts".
- Obtenha o arquivo json com as credenciais do projeto.

### 4. Configure as credenciais do Firebase e do e-mail (deve ser gmail):

- Salve as credenciais do Firebase em `firebase.json` na raiz do projeto.
- Altere a variável "from_email" do arquivo send_email.py para o seu e-mail.
- Configure sua senha de app do e-mail no `.env`:
  ```env
  EMAIL_PASSWORD=suasenha
  FIREBASE_CREDENTIALS=base64_do_json_do_firebase
  ```

### 5. Execute o script manualmente:

```sh
python send_email.py
```

## ⚙️ Configuração do GitHub Actions

O workflow do GitHub Actions executa o script automaticamente três vezes ao dia.

### Como configurar:

1. Acesse **Settings > Secrets and variables > Actions** no GitHub.
2. Adicione as seguintes variáveis secretas:
   - `EMAIL_PASSWORD` (senha do e-mail remetente)
   - `FIREBASE_CREDENTIALS` (chave base64 do Firebase)

O workflow está localizado em `.github/workflows/send_emails.yml` e utiliza cron para rodar nos seguintes horários (UTC):

```yml
schedule:
  - cron: '0 9,15,21 * * *'  # 06h, 12h e 18h no horário de Brasília
```
