### ⚙️ Executar os testes automatizados

```bash
python manage.py test accounts
```

### ✅ Integração de Testes com GitHub Actions

Os testes automatizados foram integrados ao GitHub Actions para garantir a qualidade do código continuamente.

#### Como Funciona?

Sempre que um commit for enviado ou um pull request for aberto para as branches main ou develop, um workflow do GitHub Actions será acionado para rodar os testes automatizados.

O processo executa os seguintes passos:

- Configura um ambiente com Python e Django.
- Instala as dependências do projeto listadas no requirements.txt.
- Configura e aplica migrações no banco de dados SQLite.
- Executa os testes definidos no tests.py usando Django TestCase.
- Retorna um relatório indicando sucesso (✔️) ou falha (❌).

#### Como Verificar os Testes no GitHub?

1. No repositório do projeto, acesse a aba "Actions".
2. Selecione o workflow mais recente.
3. Confira os logs para ver se todos os testes passaram ou se há falhas.

Se um teste falhar, é possível visualizar o erro detalhado e corrigi-lo antes de fazer o merge no repositório principal.

Essa integração permite um fluxo de CI/CD eficiente, garantindo que novas alterações no código sejam testadas automaticamente antes de entrarem em produção. 🚀✅
