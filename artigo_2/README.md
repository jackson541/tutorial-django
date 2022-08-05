Seja bem-vindo(a)! :smile:

Vamos continuar o projeto que iniciamos no [artigo anterior](https://www.tabnews.com.br/jackson541/tutorial-de-django-introducao) de administração de uma biblioteca. Se você não conferiu ele ainda, recomendo que volte lá para entender um pouco mais sobre o que estamos fazendo.
- [Artigo 1: Introdução](https://www.tabnews.com.br/jackson541/tutorial-de-django-introducao)

## Models
Antes de colocarmos a mão na massa, é importante que conhecermos como funciona a comunicação com o banco de dados dentro do Django.

Como expliquei antes, o `Model` é a parte da arquitetura que fica responsável por se conectar ao banco de dados, tanto na parte de gerar tabelas como a de fazer consultas ou inserção de dados.

No Django, não temos a necessidade de criarmos as tabelas do banco diretamente com SQL porque ele abstrai isso para a gente, apenas o que precisamos fazer é escrever classes em Python que serão convertidas em tabelas dentro do banco. Para fazer isso, devemos escrever a classe desejada dentro do arquivo `models.py` com o seguinte formato:

![exemplo-model-carro](https://ik.imagekit.io/6sszyq45h/image_5luNnuhGn.png?ik-sdk-version=javascript-1.4.3&updatedAt=1659701900045)

<details><summary>Código da imagem</summary>
Recomendo que escreva o código em vez de copiar para fixar melhor! 😉
    
```python
from django.db import models

class Carro(models.Model):
    cor = models.CharField(max_length=100)
    velocidade_maxima = models.IntegerField()
    data_lancamento = models.DateField()
```
    
</details>

Aqui estamos criando uma classe Carro com três atributos: cor, velocidade_maxima e data_lancamento. Todas as classes dentro do arquivo `models.py` precisam ser subclasses de `models.Model`, pois é assim que o Django irá reconhecê-las como tabelas do banco, e 
recebem o nome de "model" por padrão de nomenclatura.

Os atributos que definimos dentro dos models são convertidos em campos das tabelas, nesse caso `cor` será convertido em um varchar com limite 100, `velocidade_maxima` convertido em um campo do timpo integer e `data_lancamento` em um campo do tipo date.

Por padrão, o Django cria um campo `id` que é chave primária e auto incrementável para todos os models que não tiverem um chave primária explicitamente definida. Logo, a criação da nossa tabela em SQL (com um formato do PostgreSQL) ficaria como algo assim:

```SQL
CREATE TABLE nomedoapp_carro (
    "id" serial NOT NULL PRIMARY KEY,
    "cor" varchar(100) NOT NULL,
    "velocidade_maxima" integer NOT NULL,
    "data_lancamento" date NOT NULL
);
```

Existem diversos outros tipos de campos (campo de arquivos, URL, email, JSON, etc) e parâmetros que podemos passar para esses campos (nulo, valor padrão, campo único, etc) que podemos utilizar, você pode encontrar na documentação oficial do Django uma lista deles:
- https://docs.djangoproject.com/en/4.0/ref/models/fields/

Com o model definido, precisamos passar essas alterações para o banco e para fazer isso o projeto precisa identificar que existe um app com models criados, pois ele não faz isso automaticamente. Para realizar isso, edite a constante `INSTALLED_APPS` dentro do arquivo `settings.py` do projeto, devemos listar nele o app que criamos:

![apps-instalados-django](https://ik.imagekit.io/6sszyq45h/image_6dBFvcte5.png?ik-sdk-version=javascript-1.4.3&updatedAt=1659707536624)

É por meio dessa constante que o projeto irá reconhecer os apps que criamos em nosso projeto assim como as bibliotecas de terceiros que fomos instalar, sem isso os apps serão ignorados.

Agora utilizaremos 2 comandos, que você deve guardar bem em sua mente, para gerar as migrações (migrations) referentes aos nossos models. Se você não se lembra o que são as migrations, volte no [primeiro artigo](https://www.tabnews.com.br/jackson541/tutorial-de-django-introducao) da série para entender melhor.

O primeiro comando é o `makemigrations` que irá registrar as alterações que fizemos em cada model por meio de arquivos:

```
python manage.py makemigrations
```

Essa é a saída de sucesso dele:
![resultado-makemigrations](https://ik.imagekit.io/6sszyq45h/image_1__U5ttdG8Qn.png?ik-sdk-version=javascript-1.4.3&updatedAt=1659707982115)

Repare que ele criou um arquivo com o nome `0001_initial.py` dentro da pasta `migrations` do seu app. Se você abrir, encontrará um código semelhante a esse:

![codigo-migracao-inicial](https://ik.imagekit.io/6sszyq45h/image_2__Z8H_vF0mK.png?ik-sdk-version=javascript-1.4.3&updatedAt=1659708167970)

Esse o formato de uma migração:
- o parâmetro `initial` informa que aquela é a primeira migração do app, o django irá utilizar isso na hora de aplicar elas no banco de dados
- `dependencies` é uma lista de outras migrações que são dependências da atual, ou seja, a migração atual só pode ser executada depois que todas as suas dependências foram executadas. Como essa é a migração inicial do projeto, ela não tem dependências
- já `operations` é a lista de operações que devem ser realizadas no banco, como esperado ela está criando o model "Carro" com os 3 campos que definimos e o campo "ID" padrão como chave primária

Sempre que criar, alterar ou remover um model, você deve rodar o `makemigrations` para registrar as alterações realizadas. Quando tiver um conhecimento mais avançado, também poderá criar suas próprias migrações para realizar alterações personalizadas no banco, como rodar funções próprias, mas não recomendo ver isso agora para não se confundir.

Com a migração criada, precisamos aplicar ela no banco de dados e fazeremos isso com o segundo comando `migrate`. Ele irá verificar quais migrações ainda não foram aplicadas e irá realizar elas no banco:

```
python manage.py migrate
```

O resultado esperado é esse:

![aplicacao-migracoes](https://ik.imagekit.io/6sszyq45h/image_8nCggpg8qf.png?ik-sdk-version=javascript-1.4.3&updatedAt=1659709037044)

Várias migrações foram aplicadas de diferentes apps: contenttypes, auth, admin, sessions e app_biblioteca. Isso ocorre porque o Django tem vários apps internos que são criados junto com o nosso projeto e suas migrações são aplicadas ao rodar o primeiro `migrate`, mas o que nos interessa é que a migração do nosso app (app_biblioteca) foi aplicada e agora a nossa tabela "Carro" está no banco de dados.

Talvez você já tenha percebido que um arquivo `db.sqlite3` foi criado na raiz do projeto, o Django por padrão utiliza o SQLite3 como banco de dados, porém podemos alterar para qualquer outro banco suportado por meio das configurações do `settings.py` (e recomendo que seja feito). Faremos essa alteração posteriormente em outro artigo, por enquanto o SQLite será suficiente.

## Consultas e inserções no banco
O Django possui um [ORM](https://www.devmedia.com.br/orm-object-relational-mapper/19056) próprio que é muito poderoso e fácil de utilizar, com ele praticamente não precisamos escrever consultas diretamente com SQL porque tem uma grande variedade de métodos e faz toda a conversão para a linguagem de consulta por nós. Apesar de abstrair toda essa parte do SQL, é importante que você saiba como utilizar essa linguagem porque usaremos as mesma lógica para inserções e consultar com o ORM do Django e essa também é a linguagem universal para banco de dados relacionais. 

Ao criar um projeto, também ganhamos de brinde um playground para testarmos com as classes e funções que escrevemos no código. Para ter acesso a esse interpretador interativo basta utilizar o comando `shell`:

```
python manage.py shell
```

Ele irá abrir um interpretador como esse que podemos utilizar para testar funções ou outras coisas do python, além de poder interagir com o nosso banco de dados pelos models.

![django shell](https://ik.imagekit.io/6sszyq45h/image_KHlvinlE9.png?ik-sdk-version=javascript-1.4.3&updatedAt=1659718790482)

Para criar objetos de um determinado model, podemos importar o arquivo de models dentro da shell e utilizar o método `create`:

![django objects create](https://ik.imagekit.io/6sszyq45h/image_1__azcL715mK.png?ik-sdk-version=javascript-1.4.3&updatedAt=1659719176205)

<details><summary>Código da imagem</summary>
Recomendo que escreva o código em vez de copiar para fixar melhor! 😉
    
```python
from app_biblioteca.models import *
import datetime

Carro.objects.create(
    cor = 'cinza',
    velocidade_maxima = 120,
    data_lancamento = datetime.date(2020, 11, 26)
)
```
    
</details>

Temos alguns pontos importantes para se observar:
- o model `Carro` foi importado e utilizado para criar o objeto, afinal queriamos criar um objeto dessa classe
- o `objects` é o que chamamos de "manager", ele traz funções muito úteis que se comunicam com o banco de dados e sempre iremos utilizar ele quando quisermos fazer isso
- os campos cor, velocidade_maxima e data_lancamento receberam os tipos devidos que declaramos antes no model: string, integer e date
- a função `date` do módulo `datetime` foi utilizada para criarmos uma data
- tivemos como retorno um objeto do tipo Carro e que poderia ter sido salvo em uma variável se quiséssemos

Veja como foi simples adicionar um novo objeto ao banco, apenas precisamos chamar o seu model, o método `create()` e passar os atributos do model. Esse mesmo código poderia ter sido escrito assim em SQL:

```SQL
INSERT INTO app_biblioteca_carro 
    (cor, velocidade_maxima, data_lancamento)
VALUES
    ('cinza', 120, '2020-11-26')
```

Para aprendermos sobre como fazer consultas, vou inserir mais 2 objetos do tipo Carro no banco:

```Python
Carro.objects.create(
    cor = 'azul',
    velocidade_maxima = 120,
    data_lancamento = datetime.date(2020, 11, 30)
)

Carro.objects.create(
    cor = 'cinza',
    velocidade_maxima = 100,
    data_lancamento = datetime.date(2020, 11, 1)
)
```

Para pegar todos os objetos de um determinado model, utilizamos o método `all()`:

![django objects all](https://ik.imagekit.io/6sszyq45h/image_ZeWAirKV0.png?ik-sdk-version=javascript-1.4.3&updatedAt=1659720434020)

Ele retornou uma lista do tipo QuerySet contendo 3 objetos, os mesmos 3 que inserimos previamente. Um QuerySet é uma coleção de dados do banco e é sobre ele que realizamos as operações de buscas e filtro.

Podemos pegar essa lista que foi retornada e lidarmos como desejar:

<p align="center">
    <img src="https://ik.imagekit.io/6sszyq45h/image_0nnkby8eV.png?ik-sdk-version=javascript-1.4.3&updatedAt=1659720825910" alt="django queryset">
</p>

E para pegar apenas um objeto específico do banco?
Existe o método `get()` para nos ajudar, ele consegue buscar um objeto de um model desde que esse objeto que passamos exista e a condição informada seja única para todo o banco:

![django object get](https://ik.imagekit.io/6sszyq45h/image_ECRroRGeK.png?ik-sdk-version=javascript-1.4.3&updatedAt=1659721233031)

Acima buscamos o carro que tem o id 2 no banco, o método `__dict__` é nativo do `models.Model` e serve para passar todos os atributos de um objeto para JSON.

Veja o que acontece quando buscamos por um filtro que irá retornar mais de um objeto:

![erro get django](https://ik.imagekit.io/6sszyq45h/image_7HJyFzepE.png?ik-sdk-version=javascript-1.4.3&updatedAt=1659721388907)

Como é possível notar, recebemos um erro `get() returned more than one Carro -- it returned 2!`, o que ele próprio diz é que o método `get` retornou mais de um objeto da classe Carro (nesse caso 2). Sendo assim, só é recomendado utilizar o `get` quando temos certeza que só irá existir 1 único objeto com aquelas informações, isso geralmente irá acontecer quando buscamos por chaves primárias. Quando não há nenhum objeto com os parâmetros informados, ele também retornará um erro:

![error get django sem objetos](https://ik.imagekit.io/6sszyq45h/image_zifnVEblC.png?ik-sdk-version=javascript-1.4.3&updatedAt=1659721612041)

Bem, nem sempre queremos buscar todos os objetos de uma tabela ou apenas um objeto, as vezes precisamos buscas todos os objetos que atendam a um determinado filtro e para nos ajudar existe o método `filter()`:

<p align="center">
    <img src="https://ik.imagekit.io/6sszyq45h/image_TcuT4_BcC.png?ik-sdk-version=javascript-1.4.3&updatedAt=1659721956646" alt="django objects filter">
</p>

Ele retorna um QuerySet assim como o método `all`, mas nesse caso apenas com os objetos que atendem ao nosso filtro. No primeiro caso, ele retornou os carros com ID 1 e 3 que tem a cor igual a "cinza" e, no segundo caso, retornou os carros com ID 1 e 3 que tem velocidade_maxima igual a 120.

Uma coisa fantástica do ORM do Django é que podemos combinar consultas em diferentes momentos em um mesmo QuerySet:

<p align="center">
    <img src="https://ik.imagekit.io/6sszyq45h/image_doKyuir5Z.png?ik-sdk-version=javascript-1.4.3&updatedAt=1659722853894" alt="junção de filtros django">
</p>

Na primeira linha filtramos por carros com velocidade máxima igual a 120, o que nos deu 2 resultados, e na última linha pegamos o QuerySet resultante e filtramos em cima dele carros com a cor Azul, o que nos deu apenas 1 resultado. Essa mecânica é ideal quando precisamos filtrar algo de acordo com a entrada do usuário, por exemplo, pesquisamos apenas por livros do Brasil quando o leitor é brasileiro ou por livros da Argentina quando o leitor é Argentino.

Quando utilizamos o `WHERE` no SQL para realizar filtros, podemos buscar por atributos que sejam maior, menor que, diferente de, etc. Já no Django isso é feito por meio dos chamados "fields lookups". Um exemplo deles:

<p align="center">
    <img src="https://ik.imagekit.io/6sszyq45h/image_AQ1npNo1d.png?ik-sdk-version=javascript-1.4.3&updatedAt=1659724223761" alt="django lt lookup">
</p>

Aqui a query está filtrando por carros que tenha velocidade_maxima menor que 110, o parâmetro `__lt` que definimos após o `velocidade_maxima` é quem faz isso. `lt` é uma referência a "Less than", assim como também existe o `gt` que significa "Greater than". 
Todos os lookups são utilizados com  `__` (dois underlines) previamente. Aqui está uma lista com todos os lookups disponíveis:
- https://docs.djangoproject.com/en/4.0/ref/models/querysets/#field-lookups
 
Além de inserir e buscar dados no banco, uma operação extremamente necessária é atualizar os objetos previamente inseridos. Existem 2 formas principais para fazer isso:

A primeira é atualizar um único objeto com o método `save()`:

<p align="center">
    <img src="https://ik.imagekit.io/6sszyq45h/image_gH5G5mnS1.png?ik-sdk-version=javascript-1.4.3&updatedAt=1659724797846" alt="atualizando objeto com save django">
</p>

Pegamos o objeto com ID 1, que tinha a cor registrada como "cinza", e atualizamos o seu atributo cor para "Amarelo".

A segunda forma é atualizar vários objetos de uma vez por meio do método `update()`:

<p align="center">
    <img src="https://ik.imagekit.io/6sszyq45h/image_5UPC07TYc.png?ik-sdk-version=javascript-1.4.3&updatedAt=1659724991407" alt="atualizando objetos com update django">
</p>

Agora buscamos por todos os carros com velocidade máxima igual a 120 e atualizamos esse atributo deles para 150, todos de uma única vez.

Por fim, precisamos saber como apagar objetos do banco e para fazer isso usamos apenas o método `delete()`, ele pode ser utilizado tanto em um único objeto como em um QuerySet:

<p align="center">
    <img src="https://ik.imagekit.io/6sszyq45h/image_GCMXqKsQw.png?ik-sdk-version=javascript-1.4.3&updatedAt=1659725299597" alt="removendo objetos com delete django">
</p>

Ao deletar ele retornará um JSON com a relação de quantos objetos foram removidos e quais objetos foram esses.

Esses foram apenas alguns dos vários métodos e lookups que o Django nos forcene para trabalhar com os models, sugiro que dê uma olhada [nessa referência sobre QuerySet](https://docs.djangoproject.com/en/4.0/ref/models/querysets/) para ver outros métodos importantes como o `count()`, `first()`, `last()`, `exists()` e também os vários lookups disponíveis:
- https://docs.djangoproject.com/en/4.0/ref/models/querysets/


## Próximos passos
Parabéns por chegar até aqui! Pegue o seu café e relaxe um pouco porque você já aprendeu muito.

Em nosso próximo artigo iremos abordar como realizar o CRUD com as tabelas do banco de dados. Link para o artigo:
- (ainda em construção)

Para ficar por dentro das atualizações, conecte-se comigo no Linkedin :smile:
https://www.linkedin.com/in/jackson-alves541/

Link do repositório final desse artigo:
https://github.com/jackson541/tutorial-django/tree/main/artigo_2



## Fontes
Essas foram algumas fontes utilizadas para a construção desse artigo:
- https://docs.djangoproject.com/en/4.0/topics/db/models/
- https://docs.djangoproject.com/en/4.0/ref/models/fields/
- https://www.w3schools.com/sql/sql_create_table.asp
- https://www.postgresqltutorial.com/postgresql-tutorial/postgresql-data-types/
- https://www.alura.com.br/artigos/django-query-sets-e-orm
- https://www.w3schools.com/django/django_queryset.php