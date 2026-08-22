# Versao Dourada

**Pokemon Gold e Silver em portugues brasileiro, num download so.** O mod
reconhece qual cartucho esta rodando e usa a POKeDEX daquela versao.

Roda em dois motores a partir do mesmo pacote: `gen1recomp` e
[Gen2Recomped](https://github.com/UNDERdecoded/Gen2Recomped).

Nao acompanha nenhum byte de ROM. **Todo o texto e traducao propria, escrita a
partir do ingles original de cada versao** -- nao ha uma linha derivada de
outra traducao no pacote.

## Quanto chega a tela

| | so o mod | com o patch de motor |
|---|---|---|
| **Total** | **90%** | **97%** |

Sao 5312 entradas medidas por jogo. So com o mod instalado o jogo ja fica
jogavel e majoritariamente em portugues: falas de NPC, golpes, itens, tipos,
classes de treinador, nomes de lugar e tres quartos dos menus.

| categoria | total | so o mod | com o patch |
|---|---|---|---|
| Falas de NPC | 2994 | 2994 | 2994 |
| Menus e batalha | 1085 | 791 | 933 |
| POKeDEX | 251 | 0 | 251 |
| Nomes e descricoes de golpe | 504 | 504 | 504 |
| Nomes e descricoes de item | 325 | 325 | 325 |
| Classes de treinador | 66 | 66 | 66 |
| Nomes de lugar | 70 | 70 | 70 |
| Nomes de tipo | 17 | 17 | 17 |

**Nada quebra sem o patch.** Uma chave que o motor nao pede simplesmente nao e
usada, e um registro sem rota e pulado. O que nao chega **aparece em ingles**,
nunca em branco nem cortado.

O que depende do patch e a **POKeDEX inteira** (o motor de fabrica ainda nao
tem a rota de catalogo que entrega as fichas) e 152 rotulos de menu e batalha.
Esse patch e um PR pendente no `gen1recomp`, escrito e testado, e pode nao ser
aceito -- por isso os dois numeros aparecem separados aqui.

## Gold e Silver no mesmo pacote

O texto de NPC e **identico** nas duas ROMs -- 3134 falas, zero diferentes --,
e itens, golpes, lugares e treinadores tambem. So oito falas mudam de endereco,
e o catalogo carrega as duas chaves.

A POKeDEX e a excecao: as 251 especies tem ficha propria em cada versao, e as
502 descricoes do Silver foram escritas do zero a partir do ingles daquela ROM.
Quem responde qual jogo esta rodando e a propria ROM -- ENTEI e TYRANITAR tem a
altura trocada entre as versoes, a unica diferenca numerica entre as duas
fichas.

## Duas coisas voce escolhe

Em **MODS -> Versao Dourada -> OPTIONS**:

| linha | escolhas | o que muda |
|---|---|---|
| NOME DOS GOLPES | PORTUGUES / ENGLISH | so o **nome** do golpe |
| NOME DOS ITENS | PORTUGUES / ENGLISH | so o **nome** do item |

Sao os nomes, e so eles: a descricao do golpe, da TM e do item continua em
portugues nos dois modos. As duas existem porque quem joga com guia aberto quer
o nome que o guia usa.

**A troca vale no proximo boot** -- o mod decide no carregamento o que
registrar. Com o patch a propria tela avisa (`RESTART TO APPLY`); sem ele a
escolha funciona igual, so o aviso nao aparece.

## O que fica no original, de proposito

**Nomes de POKeMON** (BULBASAUR, GYARADOS), **nomes de personagem** (LANCE,
WHITNEY) e as siglas **TM/HM**. Sao os nomes oficiais no mundo inteiro,
inclusive nos jogos em portugues, e traduzi-los quebraria a comunicacao com
qualquer guia, video ou amigo.

**Cidade, Rota e Vila traduzem a palavra generica**, mantendo o nome proprio:
"VIOLET CITY" -> "CIDADE DE VIOLET", "ROUTE 30" -> "ROTA 30". Pontos que nao
sao cidade, vila ou rota (SPROUT TOWER, UNION CAVE) ficam inteiros em ingles.

**A interface do aplicativo** -- launcher, importacao de ROM, espacos de save,
gerenciador de mods -- fica em ingles por largura: ali os botoes tem tamanho
fixo e o portugues, mais longo, saia cortado.

A terminologia segue a localizacao oficial em portugues do Brasil, com a
**carta de TCG pt-BR** como fonte primaria para golpes e itens (GRANDE BOLA, e
nao "Otima Bola", que e do Pokemon GO). Altura e peso da POKeDEX aparecem em
**metro e quilo**, e o numero vem da tabela canonica da franquia, nao de
converter a libra de volta.

## Acentuacao

A fonte da ROM internacional so tem tres caracteres acentuados uteis, entao o
mod acrescenta uma **pagina propria de 25 glifos** acima das paginas da ROM --
acrescenta, nao substitui. Cada letra acentuada vale exatamente uma coluna de
texto, como qualquer outra.

## Joga Crystal?

E outro mod:
[versaocristal-ptbr](https://github.com/LordSangreal/versaocristal-ptbr). Ali
as falas de NPC realmente divergem das do Gold -- centenas de rotulos existem
nos dois jogos com texto diferente --, e um catalogo unico mostrava a fala do
jogo errado. Entre Gold e Silver isso nao acontece, e por isso os dois cabem
aqui.
