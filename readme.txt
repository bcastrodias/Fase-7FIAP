
# FIAP - Faculdade de Informática e Administração Paulista

Projeto Visão Computacional + Integrações Agrícolas

## 👨‍🎓 Integrantes
- Bruno Castro - RM558359: https://www.linkedin.com/in/bruno-castro-dias/
- Hugo Mariano - RM560688: https://www.linkedin.com/in/hugomariano191628150/
- Matheus Castro - RM559293: https://www.linkedin.com/in/matheus-castro-63644b224/

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
