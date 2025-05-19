# 🎬 Sistema de Votação do Oscar

## 📌 Objetivo

Desenvolver um sistema em Python com orientação a objetos para simular a votação do Oscar, permitindo o cadastro de filmes, categorias, membros da academia e o registro dos votos. O sistema adota o padrão MVC e conceitos fundamentais de POO.

---

## 🧠 Como funciona o Oscar na vida real?

O Oscar é a maior premiação do cinema mundial e acontece em duas etapas principais:

1. **Indicação**  
   Primeiro, os **membros da Academia** (cerca de 10.500 votantes em 2024) indicam seus favoritos em cada categoria — como Melhor Filme, Melhor Ator, Melhor Direção, etc. Essas indicações podem somar **milhares de votos por categoria**.

2. **Votação Final**  
   Após as indicações, os mais votados se tornam os **indicados oficiais** — geralmente os **top 5 de cada categoria**.  
   Aí acontece a segunda rodada: os membros votam novamente, mas agora **apenas entre os finalistas**.

3. **Resultado**  
   O indicado com **mais votos na segunda rodada** é o vencedor da estatueta dourada.

---

## 🖥️ O que o nosso sistema faz?

Este projeto simula esse processo todo de forma simples e didática:

- Você é um **membro da academia**.
- Pode **cadastrar indicações** de filmes, atores e diretores.
- Depois, o sistema **registra os votos** para os indicados de cada categoria.
- Por fim, você pode **ver relatórios com os vencedores** e várias outras informações.

---

## 🛠 Funcionalidades

- Cadastro de membros da academia
- Cadastro de filmes com diretor, ano e categorias indicadas
- Cadastro de categorias de premiação
- Indicação de atores e diretores
- Registro de votos por membros da academia
- Geração de relatórios, incluindo:
  - Indicações por ano e categoria
  - Votos por categoria e ano
  - Vencedores por categoria
  - Vencedores por nacionalidade
  - Top 3 filmes mais premiados

---

## 🧱 Arquitetura

O sistema utiliza o padrão de arquitetura **MVC**:
- **Model**: classes que representam entidades do sistema (como Filme, Membro, Categoria)
- **Controller**: lógica de negócio e controle do fluxo do sistema
- **View**: interface textual com o usuário (entrada e saída de dados)

Também foram utilizados:
- Herança e classes abstratas
- Associação, agregação e composição
- Tratamento de exceções

---

## ▶️ Como executar o projeto

1. Clone o repositório:
   ```bash
   git clone https://github.com/joaopaulodecker/VotacaoOscar.git
   cd VotacaoOscar
    ```

2. Execute o programa principal:
```bash
 python main.py
```
Recomendado: Python 3.10 ou superior

## 📁 Estrutura do Projeto
```bash
VotacaoOscar/
├── controller/        # Controladores das funcionalidades
├── model/             # Classes de domínio
├── view/              # Interface com o usuário
├── data/              # Simulação de armazenamento de dados
├── main.py            # Arquivo principal de execução
├── diagramas/         # Diagramas UML
└── README.md          # Documentação do projeto

```

## 👥 Integrantes
- João Paulo Decker 
- Cecília Zica Camargo


