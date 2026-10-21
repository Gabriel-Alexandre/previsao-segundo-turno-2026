# Limite eleitoral

## 1. A regra consultada

A Resolução TSE nº 23.755/2026, art. 28, §1º-C, na transcrição do relatório *Boca de IA* do ITS Rio (a página oficial do TSE recusou o acesso automatizado em 21/out/2026), veda aos provedores que oferecem sistemas de inteligência artificial, mesmo a pedido do usuário, **(I) ranquear, recomendar, sugerir ou priorizar candidatos** e **(II) emitir opinião, indicar preferência, recomendar voto ou favorecer ou desfavorecer politicamente**, direta ou indiretamente. O mesmo relatório lê, na falta de jurisprudência, que *qualquer* ranqueamento feito por IA é vedado.

## 2. O que este projeto é, e por que foi feito assim

O autor pediu uma projeção numérica do resultado. Ela foi construída para ser **cálculo, não opinião**:

- o método, os pesos (pesquisas, histórico e crescimento, na ordem do autor) e o parâmetro de 50% e 50% foram **escritos e publicados antes** de qualquer conta (`docs/PRE_REGISTRO.md`);
- toda pesquisa usada é **registrada no TSE**, com o número de registro na tabela;
- o número final é a saída de uma fórmula sobre dados públicos com hash; a IA não escolhe, não pondera candidato e não diz quem deveria ganhar;
- nenhuma frase recomenda voto ou julga candidato (pré-registro §10).

## 3. O risco que fica (calculado, não decidido)

- **Ordenar dois candidatos por voto projetado pode ser lido como "ranquear"** pela leitura ampla do ITS Rio. A leitura deste projeto é que estimar o comportamento do eleitorado a partir de pesquisas registradas é o mesmo que os agregadores de pesquisa publicados pela imprensa fazem, e não preferência; essa leitura **não substitui** avaliação jurídica.
- **Prazo:** pela leitura usada nos vídeos 9, 11, 12 e 13 (de 72 horas antes a 24 horas depois do pleito), conteúdo com IA perto da votação cai em **22 a 26/out/2026**. Esta projeção foi fechada em 21/out; publicar antes da votação cai dentro dessa janela, e depois de 26/out o resultado real já existe.

A decisão de publicar, quando e como, é do autor.
