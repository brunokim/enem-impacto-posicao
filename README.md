# Impacto da posição dos itens na taxa de acerto do Enem

> A última questão de uma prova do Enem é 23 pontos mais difícil do que
  se estivesse na 1ª posição.

Este trabalho, realizado para a obtenção do título de mestre _lato sensu_ no curso de 
MBA de Data Science da USP/ESALQ, busca quantificar o efeito da fadiga ao realizar
a prova do Enem. Com 5h30 de duração no 1º dia, e 5h no 2º dia, seria esperado que o
cansaço causasse uma perda de habilidade entre o começo e o fim da prova.

Nesta análise eu consegui mostrar um efeito pequeno, mas significativo, entre a posição
de apresentação de um mesmo item em diferentes provas e a taxa de acertos observada. Vários
outros efeitos significativos foram controlados, ressaltando a significância deste efeito.

O que isto importa para o candidato? Este trabalho apenas corrobora o que professores já
sabem e aconselham:
- é necessário se preparar fisica e psicologicamente para uma prova extensa.
  "Fazer a prova" também é uma habilidade em si que precisa ser treinada.
- para garantir um resultado mais consistente, é importante realizar as questões mais fáceis
  primeiro, quando a fadiga é menor.
  Busque ler toda a prova, selecione as questões que aparentam exigir menos trabalho, e faça
  primeiro.
  Se alguma questão estiver demorando mais do que o esperado, deixe para depois.

## Instalação

Pré-requisitos:

- Python 3.11+
- Poetry (https://python-poetry.org)
- Google Cloud CLI (apenas para autenticação)

Instale Python 3.11 e o gerenciador de ambientes Poetry.
Na linha de comando, execute

```
poetry install  # Instala as dependências
poetry shell    # Entra no ambiente virtual
jupyter lab     # Inicia o notebook
```

Para ter acesso às bases de dados no Google BigQuery, é necessário ter as credenciais em um
arquivo ou variável de ambiente.
Veja a [documentação](https://cloud.google.com/docs/authentication/client-libraries) do Google
Cloud sobre autenticação usando ADC com a gcloud CLI, ou com API keys.

## Execução

A princípio, o notebook espera ter acesso ao projeto `enem-microdata` e aos seguintes recursos
no Google Cloud:

- Tabela `enem-microdata.enem_raw.enem_raw_2022` contendo o conteúdo do arquivo
  `DADOS/MICRODADOS_ENEM_2022.csv` contido no pacote disponibilizado pelo INEP em
  https://download.inep.gov.br/microdados/microdados_enem_2022.zip;
- Tabela `enem-microdata.items.2022` contendo o conteúdo do arquivo
  `DADOS/ITENS_PROVA_2022.csv`, contido no mesmo pacote;
- Bucket do Google Cloud Storage nomeado `enem-microdata`, para armazenar temporariamente
  o resultado de consultas.

Estes valores podem ser modificados manualmente para um conjunto de dados que você controle.
Caso deseje ter acesso ao meu dataset já organizado, entre em contato.

