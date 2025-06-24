# 🎬 Sistema de Votação do Oscar

## 📌 Objetivo

Desenvolver um sistema em Python com orientação a objetos para simular a votação do Oscar, permitindo o cadastro de filmes, categorias, membros da academia e o registro dos votos. O sistema adota o padrão MVC e conceitos fundamentais de POO.

---

## Como funciona o Oscar?

O Oscar é a maior premiação do cinema mundial e acontece em duas etapas principais: Indicações e as Votações. É possível o cadastramento de Membros de Academia, Filmes, Diretores, Atores e Categorias. Há todo um processo intenso para saber quem leva para casa a estatueta dourada!

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
- Geração de relatórios

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
├── Controladores/        # Controladores das funcionalidades
├── Entidades/            # Classes
├── Limites/              # Interface com o usuário
├── Utils/                # Métodos úteis ao projeto
├── Exceptions            # Utilizado no tratamento de exceções
├── main.py               # Arquivo principal de execução

```

## 👥 Integrantes
- João Paulo Decker 
- Cecília Zica Camargo
