
# FIAP - Faculdade de Informática e Administração Paulista

Projeto Visão Computacional + Integrações Agrícolas

## 👨‍🎓 Integrantes
- Bruno Castro - RM558359: https://www.linkedin.com/in/bruno-castro-dias/
- Hugo Mariano - RM560688: https://www.linkedin.com/in/hugomariano191628150/
- Matheus Castro - RM559293: https://www.linkedin.com/in/matheus-castro-63644b224/

## Vídeo
https://www.youtube.com/watch?v=gYE-0CWBojc

## 📜 Descrição

Este projeto aplica técnicas de visão computacional com YOLOv8 e integra soluções para automação agrícola. Além da detecção automática de objetos em imagens, ele permite simulações de plantio, leitura de sensores e visualização de código IoT, em uma interface multipage construída com Streamlit.

O projeto foi desenvolvido como parte do curso de Inteligência Artificial da FIAP.

## 📁 Estrutura do Projeto

- `models/`: Contém os modelos treinados com YOLOv8.
  - `model_30epochs.pt`, `model_60epochs.pt`, `yolov8n.pt`
  - Subpastas `yolo_30ep/` e `yolo_60ep/` com resultados e weights.

- `pages/`: Páginas do aplicativo multipage no Streamlit.
  - `1_assistente_plantacao.py`: Cálculo de insumos por cultura, safra e área.
  - `2_visualizacao_sensores.py`: Visualização de sensores pH, umidade e nutrientes.
  - `3_codigo_iot.py`: Exibe código .ino usado em ESP32/Arduino.
  - `4_inferencia_yolo.py`: Upload de imagem + inferência com modelo YOLOv8.

- `dados_farmtech.db`: Banco de dados SQLite local com as leituras dos sensores.
- `Home.py`: Página inicial da aplicação multipage no Streamlit.
- `README.md`: Descrição inicial do repositório.
- `requirements.txt`: Lista de dependências Python para execução do projeto.

## 🧭 Navegação via Dashboard

A `Home.py` fornece botões para navegar entre os seguintes módulos:

1️⃣ **Assistente de Plantação**  
> Estima insumos como fósforo e nitrogênio com base na cultura e área.

2️⃣ **Visualização de Sensores**  
> Mostra valores capturados de sensores de umidade, pH e nutrientes por zona.

3️⃣ **Código IoT**  
> Permite visualizar o sketch `.ino` usado no ESP32.

4️⃣ **Inferência com YOLOv8**  
> Permite upload de imagem e realiza detecção com `model_60epochs.pt`.

5️⃣ e 6️⃣  
> Reservados para expansão futura.


Documentação Técnica – Mensageria com AWS SNS + SQS + Streamlit
• Objetivo
Criar uma infraestrutura de mensageria para alertas críticos (ex: umidade abaixo de 50%) em uma aplicação de monitora• Arquitetura
[Aplicação Streamlit - Página Sensores] → (Detecta umidade < 50)
[SNS - Amazon Simple Notification Service] → (Publica mensagem)
[SQS - Amazon Simple Queue Service] → (Polling via boto3)
[Aplicação Streamlit - Página Principal] → Exibe alertas (st.toast)
• Passo a passo de configuração
1. Criar o tópico SNS:
 - Acesse o console do SNS e crie um tópico do tipo Standard.
 - Após criado, copie o ARN do tópico.
2. Criar a fila SQS:
 - Acesse o console do SQS e crie uma fila do tipo Standard.
 - Copie a Queue URL e o ARN da fila.
3. Assinar a fila SQS ao tópico SNS:
 - No console do SNS, crie uma assinatura usando o protocolo Amazon SQS.
 - Forneça o ARN da fila e aceite a política sugerida.
• Permissões
Configure um usuário IAM com as políticas:
- AmazonSNSFullAccess
- AmazonSQSFullAccess
Use aws configure para autenticar via CLI ou boto3.
• Integração com Streamlit
1. Enviar alerta ao SNS:
- Utilize boto3 para publicar mensagens usando o TopicArn.
- Exemplo de código disponível.
2. Receber alertas via SQS:
- Faça polling com boto3 para verificar mensagens na fila.
- Exiba mensagens com st.toast().
• Resultado
Ao detectar umidade < 50%, a aplicação publica um alerta no SNS.
Esse alerta é entregue à fila SQS assinada.
A página principal do Streamlit lê essa fila e exibe a notificação automaticamente.


## 🔧 Como Executar

1. Instale as dependências com:

   ```
   pip install -r requirements.txt
   ```

2. Rode o app com:

   ```
   streamlit run Home.py
   ```

3. Use o menu lateral ou botões para navegar entre as páginas do projeto.

## 🗃 Histórico de versões

- 1.0 - 30/04/2025

## 📋 Licença

Este projeto segue o modelo educacional FIAP e está licenciado sob Creative Commons Attribution 4.0 International.
