Seja bem-vindo(a)! :smile:

Vamos finalmente iniciar a parte principal do nosso projeto e desenvolver o CRUD do nosso sistema da biblioteca.

Se você caiu aqui de paraquedas e não entende o que é ou como funciona o Django, recomendo que pare um pouco para ver os artigos anteriores que irão te explicar melhor antes de continuar:

- [Artigo 1: Introdução](https://www.tabnews.com.br/jackson541/tutorial-de-django-introducao)
- [Artigo 2: Models e consultas](https://www.tabnews.com.br/jackson541/models-e-consultas-em-django)
    
## Utilizando os templates
    
Agora que já sabemos como criar e utilizar os models do Django, vamos iniciar o desenvolvimento do nosso sistema.
    
Iniciaremos criando uma página de cadastro para os leitores. Por motivos de segurança os administradores não terão um parte de cadastro livre, já pensou se qualquer pessoa pudesse se tornar adm da biblioteca? 
    
Um bom ponto de partida é ter uma view para realizar esse cadastro:
    
<p align="center">
    <img src="https://ik.imagekit.io/6sszyq45h/image_5MJbRdvc7.png?ik-sdk-version=javascript-1.4.3&updatedAt=1662162677737" alt="inicio tela cadastro leitores">
</p>
    
<details><summary>Código da imagem</summary>
Recomendo que escreva o código em vez de copiar para fixar melhor! 😉
    
```python
def cadastro_leitores(request):
    return HttpResponse("aqui é a página de cadastro")
```
    
</details>

E também uma rota para poder acessar essa view:

<p align="center">
    <img src="https://ik.imagekit.io/6sszyq45h/image_Al-_1vcNW.png?ik-sdk-version=javascript-1.4.3&updatedAt=1662163093714" alt="URL tela cadastro leitores">
</p>
    
<details><summary>Código da imagem</summary>
Recomendo que escreva o código em vez de copiar para fixar melhor! 😉
    
```python
urlpatterns = [
    path('cadastro/', cadastro_leitores, name='cadastro_leitores_view'),
]
```
    
</details>
    
Após rodar o projeto e acessar a rota http://localhost:8000/cadastro/ , devemos ver essa tela:
    
<p align="center">
    <img src="https://ik.imagekit.io/6sszyq45h/image_ubgTaDtkg.png?ik-sdk-version=javascript-1.4.3&updatedAt=1662163189386" alt="URL tela cadastro leitores">
</p>
    
Nós poderiamos colocar todo o HTML da nossa tela dentro da função `HttpResponse`, mas isso iria precisar de um código HTML razoável dentro de uma string, o que precisamos concordar que não fica nem um pouco legal. 
    
Então precisamos criar um arquivo HTML de verdade para poder utilizar ele em nossa view e é justamente para isso que existem os **templates**, aqueles mesmo que citamos do padrão MVC e que fica responsável pela parte visual.
    
Por padrão nós salvamos os nossos templates (arquivos HTML) dentro de uma pasta também chamada **templates** dentro no nosso app. Então crie uma pasta com esse nome e um arquivo para cadastro dos leitores dentro dela, dessa forma:

<p align="center">
    <img src="https://ik.imagekit.io/6sszyq45h/image_Cu_69lbKl.png?ik-sdk-version=javascript-1.4.3&updatedAt=1662164073982" alt="pasta de templates">
</p>
   
Vamos adicionar um pouco de texto a nossa página recém criada (dentro do arquivo HTML que você criou agora):
    
```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Administração da biblioteca</title>
</head>
<body>

<h1>Administração da biblioteca</h1>
    
<p>Seja bem-vindo! Realize seu cadastro e desfrute da nossa biblioteca.</p>

</body>
</html>
```
    
Com o arquivo criado, precisamos importar ele de alguma forma na view para retornar para o usuário. Como sempre, o Django provém um método para importarmos os templates de forma fácil.
    
O método `loader` vai nos permitir fazer isso:
    
<p align="center">
    <img src="https://ik.imagekit.io/6sszyq45h/image_o_7ISLnjm.png?ik-sdk-version=javascript-1.4.3&updatedAt=1662164742042" alt="importando template dentro da view">
</p>
    
<details><summary>Código da imagem</summary>
Recomendo que escreva o código em vez de copiar para fixar melhor! 😉
    
```python
from django.template import loader


def cadastro_leitores(request):
    template = loader.get_template('leitores_cadastro.html')
    
    context = {}

    return HttpResponse(template.render(context, request))
```
    
</details>
    
Na linha 5 o template está sendo importado de dentro da pasta, a variável `context` da linha 8 é um dicionário que pode levar outras variáveis para serem utilizadas dentro do template (veremos sobre isso mais a frente) e, por fim, na linha 9 estamos renderizando o template e devolvendo ele com o HttpResponse.
    
Com o template importado e sendo retornado, veremos o resultado da página de cadastro depois de rodar o projeto:
    
<p align="center">
    <img src="https://ik.imagekit.io/6sszyq45h/image_4iGBPo-Yw.png?ik-sdk-version=javascript-1.4.3&updatedAt=1662165095538" alt="importando template dentro da view">
</p>
    
Viu como é simples utilizar os templates do Django?
    
Existe ainda uma forma mais prática de utilizar eles sem precisar importar diretamente com o método `render`:
    
<p align="center">
    <img src="https://ik.imagekit.io/6sszyq45h/image_phRIJdoW8.png?ik-sdk-version=javascript-1.4.3&updatedAt=1662165442815" alt="método render do django">
</p>
    
<details><summary>Código da imagem</summary>
Recomendo que escreva o código em vez de copiar para fixar melhor! 😉
    
```python
from django.shortcuts import render


def cadastro_leitores(request):
    context = {}

    return render(request, 'leitores_cadastro.html', context)
```
    
</details>

Fizemos a mesma coisa de uma forma muito mais simples, se você entrar na tela de cadastro deve ter o mesmo retorno que antes.
   
## Conteúdos dinâmicos nos templates
Em nosso sistema será necessário passar conteúdo dinâmico para várias páginas, a final as páginas vão ser montadas de acordo com os dados do usuário logado, livros disponíveis, etc. Para realizar essas mudanças, os templates nos ajudam muito com uma sintaxe fácil de entender.

Agora posso explicar para o quê serve aquela variável `context` que adicionamos a view no código anterior. Como falei, ela serve para levar outras variáveis para dentro do template e, por meio disso, podemos montar os conteúdos dinâmicos que precisamos.

Para entender melhor, vamos bagunçar um pouco o nosso template de cadastro com dados aleatórios. Digamos que você queira passar para dentro do template uma variável com o nome do sistema atual que será definido na view e assim deve ser feito:

<p align="center">
    <img src="https://ik.imagekit.io/6sszyq45h/image_c17LbjOIS.png?ik-sdk-version=javascript-1.4.3&updatedAt=1662227410718" alt="variável dentro do context">
</p>
    
<details><summary>Código da imagem</summary>
Recomendo que escreva o código em vez de copiar para fixar melhor! 😉
    
```python
def cadastro_leitores(request):
    sistema_atual = 'Administração da biblioteca do Django'

    context = {
        'nome_sistema': sistema_atual
    }

    return render(request, 'leitores_cadastro.html', context)
```
    
</details>

Na linha 2 definimos uma variável com o nome do sistema e na linha 5 inserimos ela no dicionário `context`, a chave `nome_sistema` será interpretada como uma variável dentro do template (coloquei um nome diferente apenas para você entender que o nome da variável passada para o template não precisa ser o mesmo da view)

E, para utilizar variáveis dentro do template, temos a sintaxe de duas chaves `{{ nome_da_variavel }}`, tudo dentro dessa sintaxe será interpretado como uma variável. Sendo assim, vamos passar o nome do sistema para essa forma:

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Administração da biblioteca</title>
</head>
<body>

<h1>{{ nome_sistema }}</h1>
    
<p>Seja bem-vindo! Realize seu cadastro e desfrute da nossa biblioteca.</p>

</body>
</html>
```

Agora recarregue a sua página e veja a alteração acontecer, as mudanças dentro dos templates não recarregam o sistema assim como acontece com os arquivos python:

<p align="center">
    <img src="https://ik.imagekit.io/6sszyq45h/image_Pq6QdgAbS.png?ik-sdk-version=javascript-1.4.3&updatedAt=1662227968459" alt="variável dentro do template">
</p>
    
E se quisermos mudar o conteúdo exibido no nome, basta mudar dentro da variável na view:

<p align="center">
    <img src="https://ik.imagekit.io/6sszyq45h/image_1aGvlXBjQ.png?ik-sdk-version=javascript-1.4.3&updatedAt=1662228142361" alt="alterando variável da view">
</p>

<p align="center">
    <img src="https://ik.imagekit.io/6sszyq45h/image_akFfdKhWb.png?ik-sdk-version=javascript-1.4.3&updatedAt=1662228248872" alt="resultado da mudança no template">
</p>

Mas o template nos permite passar muito mais do que uma simples string para dentro, também aceita objetos, listas, dicionários e vários outras estruturas de dados.

Vamos criar uma classe fictícia para mostrar como exibir dados dos objetos:

<p align="center">
    <img src="https://ik.imagekit.io/6sszyq45h/image_GHof_LKgb.png?ik-sdk-version=javascript-1.4.3&updatedAt=1662230281640" alt="classe de teste para o template">
</p>
    
<details><summary>Código da imagem</summary>
Recomendo que escreva o código em vez de copiar para fixar melhor! 😉
    
```python
class Carro:
    def __init__(self, nome, marca, cor):
        self.nome = nome
        self.marca = marca
        self.cor = cor

def cadastro_leitores(request):
    sistema_atual = 'Outro nome do sistema'

    carro = Carro('fusca', 'Volkswagen', 'azul')

    context = {
        'nome_sistema': sistema_atual,
        'carro': carro
    }

    return render(request, 'leitores_cadastro.html', context)
```
    
</details>

Criamos a classe `Carro` e passamos um objeto seu para o template por meio do context e assim podemos utilizar ele:

```html

<h2>Dados do carro</h2>
<table border="1px solid black">
    <thead>
        <tr>
            <th>Nome</th>
            <th>Marca</th>
            <th>Cor</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td>{{ carro.marca }}</td>
            <td>{{ carro.cor }}</td>
            <td>{{ carro.nome }}</td>
        </tr>
    </tbody>
</table>

```

A mesma sintaxe das variáveis, com duas chaves, é utilizada e acessamos os atributos da mesma forma com o ponto (`.`). Esse será o resultado:

<p align="center">
    <img src="https://ik.imagekit.io/6sszyq45h/image_CIqZre1vG.png?ik-sdk-version=javascript-1.4.3&updatedAt=1662231303438" alt="classe de teste dentro do template">
</p>

Veremos que com as listas e os dicionários a sintaxe vai permanecer a mesma:

<p align="center">
    <img src="https://ik.imagekit.io/6sszyq45h/image_YIbeCOqwp.png?ik-sdk-version=javascript-1.4.3&updatedAt=1662231597718" alt="teste com lista e dicionário na view">
</p>
    
<details><summary>Código da imagem</summary>
Recomendo que escreva o código em vez de copiar para fixar melhor! 😉
    
```python
def cadastro_leitores(request):
    sistema_atual = 'Outro nome do sistema'

    carro = Carro('fusca', 'Volkswagen', 'azul')

    carros_nomes = ['fusca', 'hb20', 'honda fit']

    ano_lancamento_carros = {
        'fusca': 1959,
        'hb20': 2012,
        'honda_fit': 2003
    }

    context = {
        'nome_sistema': sistema_atual,
        'carro': carro,
        'carros_nomes': carros_nomes,
        'ano_lancamento_carros': ano_lancamento_carros
    }

    return render(request, 'leitores_cadastro.html', context)
```
    
</details>

```html

<h2>Lista de carros</h2>
<ul>
    <li>{{ carros_nomes.0 }}</li>
    <li>{{ carros_nomes.1 }}</li>
    <li>{{ carros_nomes.2 }}</li>
</ul>

<h2>Ano de lançamento dos carros</h2>

<ul>
    <li>Fusca: {{ ano_lancamento_carros.fusca }}</li>
    <li>HB20: {{ ano_lancamento_carros.hb20 }}</li>
    <li>Honda Fit: {{ ano_lancamento_carros.honda_fit }}</li>
</ul>

```

Repare como a forma que em acessamos os dados da lista e do dicionários são diferentes do que fazemos em códigos python e bem semelhantes a forma como se acessa dados dos objetos. Nas listas sempre utiliza `nome_da_lista.indice` e para os dicionários sempre é `nome_do_dicionario.nome_da_chave`.

Por fim, esse será o resultado gerado em nossa página:

<p align="center">
    <img src="https://ik.imagekit.io/6sszyq45h/image__qvZFY20-.png?ik-sdk-version=javascript-1.4.3&updatedAt=1662231940543" alt="teste com lista e dicionário na view">
</p>

## Condicionais e repetições

Você viu como é simples passar dados para dentro dos templates, mas, assim como na programação normal, geralmente precisamos usar estruturas de repetição (como o FOR) ou condicionais (como o IF) para saber qual caminho tomar e essa questão não é diferente dentro dos templates na hora de exibir algo. Dessa forma, também somos capazes de utilizar essas estruturas com o Django e vou te mostrar nesse instante.

Quando falamos de tags que executam alguma ação dentro dos templates, sempre utilizamos a sintaxe de chaves e porcentagem: `{% nome_da_tag %}`. Sendo assim, a sintaxe `{{ }}` é reservada para variáveis e a `{% %}` para tags como veremos a frente.

Sabemos que a melhor forma de exibir todos os dados de uma lista não é chamando um a um manualmente, fazer isso com um FOR é muito mais simples. Logo, vamos precisar do `{% for %}` para nos ajudar:

```html

<h2>Nova lista de carros</h2>
<ul>
    {% for nome_carro in carros_nomes %}
        <li>{{ nome_carro }}</li>
    {% endfor %}
</ul>

```

Repare como escrevemos o FOR, ele itera sobre a lista `carros_nomes` e cada elemento da lista será guardado na variável `nome_carro` a cada iteração, assim como acontece em um FOR normalmente no python. A variável `nome_carro` vem na linha seguinte no formato `{{ }}` para exibir o seu conteúdo. Por fim, temos a tag `{% endfor %}` que delimita o fim da execução do FOR, então tudo que estiver entre o `{% for %}` e o `{% endfor %}` será executado a quantidade de elementos que tiver na lista.

Esse será o nosso resultado:

<p align="center">
    <img src="https://ik.imagekit.io/6sszyq45h/image_n6SqtCfIA.png?ik-sdk-version=javascript-1.4.3&updatedAt=1662299730776" alt="resultado ao utilizar o FOR">
</p>

Exatamente o mesmo que tivemos antes quando escrevemos cada elemento por vez da lista em um `li`, mas de forma melhor.

E se quiséssemos fazer com que apenas a linha com o valor "fusca" tenha a cor azul?
É ai que entram as condicionais e o nosso famoso IF, que pode ser criado com uma sintaxe muito semelhante a do FOR:

```html
<h2>Nova lista de carros com IF</h2>
<ul>
    {% for nome_carro in carros_nomes %}
        <li 
            {% if nome_carro == 'fusca' %} style="color: blue;" {% endif %}
        > {{ nome_carro }} </li>
    {% endfor %}
</ul>
```

Dentro das propriedades do `li` adicionamos a condicional desejada do fuscal azul, o trecho `{% if nome_carro == 'fusca' %}` verifica se o valor da lista atual é o que desejamos e, caso seja, a estilização da cor azul será aplicada. Assim como existem o `{% endfor %}`, também é preciso ter um `{% endif %}` para dizer ao template qual é o fim do IF e tudo entre o `{% if %}` e `{% endif %}` será executado se a condicional for verdadeira. Assim fica a nossa página:

<p align="center">
    <img src="https://ik.imagekit.io/6sszyq45h/image_A88GPrmKm.png?ik-sdk-version=javascript-1.4.3&updatedAt=1662300451125" alt="resultado ao utilizar o IF">
</p>

Geralmente um IF pode ser muito complexo tendo vários ELSE IF (ELIF no python) ou um ELSE e é assim que fazemos nos templates:

```html
<h2>Nova lista de carros com IF e ELSE</h2>
<ul>
    {% for nome_carro in carros_nomes %}
        <li 
            {% if nome_carro == 'fusca' %} 
                style="color: blue;" 
            {% elif nome_carro == 'hb20' %} 
                style="color: red;" 
            {% else %}
                style="color: yellowgreen;" 
            {% endif %}
        > {{ nome_carro }} </li>
    {% endfor %}
</ul>
```

A forma de se escrever é fácil de entender, os ELIFs funcionam como no python, assim como o ELSE. E esse é o nosso resultado:

<p align="center">
    <img src="https://ik.imagekit.io/6sszyq45h/image_-SGo93F5M.png?ik-sdk-version=javascript-1.4.3&updatedAt=1662300952257" alt="resultado ao utilizar o IF e ELSE">
</p>

Essas são apenas algumas das tags que temos para os templates, existe uma lista completa na [documentação oficial](https://docs.djangoproject.com/en/4.1/ref/templates/builtins/).

## Próximos passos
Parabéns por chegar até aqui! Pegue o seu café e relaxe um pouco porque você já aprendeu muito.

Você aprendeu aqui uma parte essencial para trabalhar com os templates, ainda existem outras coisas importantes como utilizar [filtros nas tags](https://docs.djangoproject.com/en/4.1/topics/templates/#filters) ou como [importar outros templates dentro do template atual](https://docs.djangoproject.com/en/4.1/ref/templates/builtins/#extends) para reaproveitar código.

Em nosso próximo artigo iremos continuar a construção da página de cadastro e entender como funcionam os formulários. Link para o artigo:
- (ainda em construção)

Para ficar por dentro das atualizações, conecte-se comigo no Linkedin :smile:
https://www.linkedin.com/in/jackson-alves541/

Link do repositório final desse artigo:
https://github.com/jackson541/tutorial-django/tree/main/artigo_2


## Fontes
Essas foram algumas fontes utilizadas para a construção desse artigo:
- https://docs.djangoproject.com/en/4.1/intro/tutorial03/
- https://docs.djangoproject.com/en/4.1/topics/templates/
- https://docs.djangoproject.com/en/4.1/ref/templates/builtins/