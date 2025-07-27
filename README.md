<div align="center">

# 🎬 Sistema de Premiação Oscar 🎬

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

**Um sistema completo em Python que dá vida ao processo de indicações e votações da maior premiação do cinema, com uma interface gráfica amigável e uma arquitetura de software robusta.**

</div>

---

### **Como o Oscar da Vida Real se Conecta ao Nosso Software?**
> Para apreciar o nosso sistema, é legal entender como a premiação de verdade funciona. A grande sacada do nosso projeto foi transformar as regras complexas do Oscar em funcionalidades claras e diretas.

<br>

| Na Vida Real 🌎                                                                                                                                                                                                                                                            | No Nosso Software 💻                                                                                                                                                                                                                                                                             |
| :----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | :----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Fase 1: Indicações (Os Especialistas Escolhem)** <br/> Membros da Academia votam dentro de suas áreas: atores indicam atores, diretores indicam diretores, etc. Para **Melhor Filme**, todos os membros podem indicar.                                                    | **Simulando a Fase 1: "Registrar Indicações"** <br/> Nosso sistema aplica essa regra: um `Ator` pode indicar para categorias de atuação, um `Diretor` para direção, e qualquer membro (incluindo `Membro Academia`) pode indicar para "Melhor Filme".                               |
| **Fase 2: Votação Final (Todos Votam)** <br/> Após os finalistas serem definidos, a votação é aberta para **todos** os membros da Academia em **todas** as categorias. É aqui que os vencedores são decididos.                                                             | **Simulando a Fase 2: "Registrar Votos"** <br/> Após o clique no botão **"Avançar Fase"**, nosso sistema simula com precisão a votação final, onde qualquer membro cadastrado pode votar em qualquer um dos finalistas.                                                              |
| **A Preparação e o Grand Finale** <br/> Atores, diretores e filmes precisam ser elegíveis. No final, os envelopes são abertos e os vencedores anunciados.                                                                                                                   | **A Preparação e o Grand Finale** <br/> Em **"Gerenciar Pessoas"**, **"Filmes"** e **"Categorias"**, você prepara o cenário. E em **"Ver Resultados Finais"**, você tem o nosso "E o Oscar vai para...", mostrando quem venceu. |

---

## 🚀 Funcionalidades Principais

-   **🗳️ Gestão Completa:** Cadastre, edite e remova Filmes, Categorias e Membros da Academia (Atores, Diretores, etc.).
-   **🏆 Ciclo de Premiação:** Simule o processo real com uma fase de **Indicações** e uma fase de **Votação**.
-   **📊 Relatórios Inteligentes:** Gere e visualize relatórios com os resultados da votação e outras pesquisas, como filmes agrupados por nacionalidade.
-   **💾 Persistência de Dados:** Todas as informações são salvas em arquivos locais (`.pkl`), garantindo que seu progresso nunca seja perdido.

---

## 🧱 O Coração do Projeto: Arquitetura

O grande foco deste trabalho foi construir um software bem organizado. Para isso, utilizamos padrões de mercado:

* **MVC (Model-View-Controller):**
    * **Model (`Entidades`, `DAOs`):** A nossa "cozinha". Representa os dados e sabe como guardá-los nos arquivos.
    * **View (`Limites`):** O "salão do restaurante". É a interface gráfica (feita com PySimpleGUI), responsável apenas por mostrar e coletar informações.
    * **Controller (`Controladores`):** O "gerente". É o cérebro que contém toda a lógica de negócio, validações e que orquestra a comunicação entre a Tela e os Dados.
* **Exceções Personalizadas:** Criamos nossas próprias classes de erro para um tratamento mais claro e profissional.

---

## ▶️ Como Executar

Você só precisa do Python 3 instalado.

1.  **Clone o repositório:**
    ```bash
    git clone [https://github.com/joaopaulodecker/VotacaoOscar.git](https://github.com/joaopaulodecker/VotacaoOscar.git)
    cd VotacaoOscar
    ```

2.  **Instale as dependências:**
    ```bash
    pip install PySimpleGUI
    ```

3.  **Execute o programa:**
    ```bash
    python main.py
    ```

---

## 📁 Estrutura do Projeto
    VotacaoOscar/
    ├── Controladores/  # A Lógica (O Cérebro)
    ├── DAOs/           # A Persistência de Dados
    ├── Entidades/      # Os Moldes dos Objetos
    ├── Excecoes/       # Nossas Classes de Erro
    ├── Limites/        # A Interface Gráfica (As Telas)
    ├── testes/         # Testes Automatizados
    ├── .gitignore      # Arquivos a serem ignorados pelo Git
    └── main.py         # Ponto de partida da aplicação


---
## 👥 Desenvolvedores

-   João Paulo Decker
-   Cecília Zica Camargo

<br>
<hr>
<br>

<div align="center">

# 🇬🇧 English Version

</div>

# 🎬 Academy Awards Voting System

A complete Python system that brings the nomination and voting process of the world's biggest film awards to life, featuring a user-friendly graphical interface and a robust software architecture.

---

### **How Do the Real-Life Oscars Connect to Our Software?**

> Understanding how the awards work in real life helps to see the intelligence behind our system. Our project's main goal was to turn the complex Oscar rules into clear, direct features.

<br>

| In Real Life 🌎                                                                                                                                                                 | In Our Software 💻                                                                                                                                                                                          |
| :------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | :---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Phase 1: Nominations (The Specialists Choose)** <br/> Academy members vote within their areas of expertise: actors nominate actors, directors nominate directors, etc. For **Best Picture**, all members can nominate. | **Simulating Phase 1: "Register Nominations"** <br/> Our system enforces this rule: an `Actor` can nominate for acting categories, a `Director` for directing, and any member can nominate for "Best Picture".         |
| **Phase 2: Final Voting (Everyone Votes)** <br/> After finalists are announced, voting is opened to **all** Academy members in **all** categories. This is where the winners are decided. | **Simulating Phase 2: "Register Votes"** <br/> After clicking the **"Advance Phase"** button, our system accurately simulates the final voting, where any registered member can vote for any finalist.              |
| **The Setup & The Grand Finale** <br/> Actors, directors, and films must be eligible. In the end, envelopes are opened and winners are announced.                               | **The Setup & The Grand Finale** <br/> In **"Manage People"**, **"Movies"**, and **"Categories"**, you set the stage. And in **"View Final Results"**, you get our "And the Oscar goes to...". |

---

## ✨ Demo

*[PASTE YOUR DEMONSTRATION GIF LINK HERE]*

---

## 🚀 Key Features

-   **🗳️ Full Management:** Create, edit, and delete Movies, Categories, and Academy Members (Actors, Directors, etc.).
-   **🏆 Awards Cycle:** Simulate the real process with a **Nomination** phase and a **Voting** phase.
-   **📊 Smart Reports:** Generate and view reports with voting results and other queries, such as movies grouped by nationality.
-   **💾 Data Persistence:** All information is saved to local files (`.pkl`), ensuring your progress is never lost.

---

## 🧱 The Heart of the Project: Architecture

The main focus of this project was to build a well-organized piece of software. To achieve this, we used industry-standard patterns:

* **MVC (Model-View-Controller):**
    * **Model (`Entidades`, `DAOs`):** Our "kitchen." It represents the data and knows how to store it in files.
    * **View (`Limites`):** The "dining room." It's the graphical user interface (built with PySimpleGUI), responsible only for displaying and collecting information.
    * **Controller (`Controladores`):** The "manager." It's the brain that contains all the business logic, validations, and orchestrates the communication between the View and the Data.
* **Custom Exceptions:** We created our own error classes for clearer and more professional error handling.

---

## ▶️ How to Run

You just need Python 3 installed.

1.  **Clone the repository:**
    ```bash
    git clone [https://github.com/joaopaulodecker/VotacaoOscar.git](https://github.com/joaopaulodecker/VotacaoOscar.git)
    cd VotacaoOscar
    ```

2.  **Install dependencies:**
    ```bash
    pip install PySimpleGUI
    ```

3.  **Run the program:**
    ```bash
    python main.py
    ```

---

## 📁 Project Structure

    VotacaoOscar/
    ├── Controladores/  # The Logic (The Brain)
    ├── DAOs/           # The Data Persistence
    ├── Entidades/      # The Object Blueprints
    ├── Excecoes/       # Our Custom Error Classes
    ├── Limites/        # The GUI (The Screens)
    ├── testes/         # Automated Tests
    ├── .gitignore      # Files to be ignored by Git
    └── main.py         # Application entry point
    

---

## 👥 Developers

-   João Paulo Decker
-   Cecília Zica Camargo
