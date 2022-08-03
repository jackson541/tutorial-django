Link para artigo oficial:
https://www.tabnews.com.br/jackson541/tutorial-de-django-introducao

## O que ele é
Seja bem-vindo(a)! :smile: 

Se você chegou até aqui, provavelmente está buscando aprender sobre como funciona o Django e já sabe o que ele é, mas aqui está uma breve descrição caso não saiba:

Django é um framework web escrito em Python que tem como objetivo acelerar o processo de desenvolvimento e trazer mais comodidades aos desenvolvedores. Seu [site oficial](https://www.djangoproject.com/) contém a seguinte descrição: 
> "Django é um framework web Python de alto nível que encoraja o desenvolvimento rápido e design limpo e pragmático. Construído por desenvolvedores experientes, ele cuida de grande parte do incômodo do desenvolvimento da Web, para que você possa se concentrar em escrever seu aplicativo sem precisar reinventar a roda. É gratuito e de código aberto."

Em resumo, ele irá nos trazer diversas ferramentas para acelerar o processo de desenvolvimento de forma fácil e rápida.

## Arquitetura
A arquitetura do Django (a famosa MTV) é simples de entender e fácil para trabalhar, ela é divida em três partes:
- **Model**: Responsável por se comunicar com o banco de dados e mapear as tabelas dele por meio de classes
- **Template**: Local que armazena a parte visual da aplicação, nesse caso irá salvar o HTML do nosso projeto
- **View**: O último dos 3 pilares é o responsável por salvar as regras de negócio do projeto, onde iremos armazenar o que deve acontecer após o usuário acessar determinada rota X ou Y

No exemplo abaixo, é possível ver como eles 3 se comportam: o usuário acessar uma URL do sistema que está diretamente ligada a uma View, já a View se comunica com o Model para buscar informações no banco de dados para verificar as regras de negócio e fazer as tratativas e, por fim, encaminha o usuário para um Template com os dados necessários para a visualização.

![exemplo-mtv](https://ik.imagekit.io/6sszyq45h/django-mvt-based-control-flow_j9NKVR9eW.png?ik-sdk-version=javascript-1.4.3&updatedAt=1659546265669)

Provavelmente você já deve ter visto outra arquitetura muito semelhante chamada [MVC](https://pt.wikipedia.org/wiki/MVC), os conceitos são os mesmos no MTV só que algumas alterações nos nomes.

## Projeto base
Durante a nossa sequência de artigos vamos desenvolver um pequeno sistema de administração de uma biblioteca, ele servirá tanto para nos guiar praticamente nos conceitos como também para ter algo concreto construído ao final do processo. Abaixo está uma breve descrição do sistema final caso tenha interesse:

<details><summary>Dados gerais do projeto</summary>
    
Requisitos do sistema:
<ul>
    <li>usuários são divididos em leitores (usuários comuns) e administradores</li>
    <li>ações dos administradores:</li>
    <ul>
        <li>login</li>
        <li>logout</li>
        <li>cadastrar e remover livros</li>
        <li>adicionar novos administradores</li>
        <li>alterar username, senha, nome e email próprio</li>
        <li>ver conta de leitores</li>
        <li>reservar livros para leitores</li>
        <li>pesquisar por livros disponíveis na biblioteca</li>
        <li>ver leitores que estão com livros atrasados</li>
    </ul>
    <li>ações dos leitores:</li>
    <ul>
        <li>cadastro</li>
        <li>login</li>
        <li>logout</li>
        <li>alterar username, senha, nome e email próprio</li>
        <li>ver livros reservados no momento e quando deve devolver</li>
        <li>ver histórico de livros reservados</li>
        <li>pesquisar por livros disponíveis na biblioteca</li>
    </ul>
</ul>

Com base nesses requisitos, montei o seguinte esquema de relações do banco de dados:
    
![relacoes-db](https://ik.imagekit.io/6sszyq45h/diagrama_biblioteca_ejDRrNqdK.png?ik-sdk-version=javascript-1.4.3&updatedAt=1659547856181)

As relações foram definidas com base na descrição desse outro sistema, mas com simplicações para não dificultar o processo:
https://www.educative.io/courses/grokking-the-object-oriented-design-interview/RMlM3NgjAyR
    
Sinta-se a vontade caso queira fazer a versão completa do sistema, é um excelente treino e desafio para seguir!
    
</details>

## Início do projeto
Todo o código desse artigo pode ser acompanhado no repositório final:
https://github.com/jackson541/tutorial-django/tree/main/artigo_1

### Instalação
Você já deve estar ansioso(a) para colocar a mão na massa, então esse é o momento!

Antes de criar um novo projeto, precisamos instalar o Django em nossa máquina. Você pode fazer isso globalmente ou, como eu prefiro fazer, dentro de um ambiente virtual (virtual env). Os ambientes virtuais nos permitem instalar os pacotes externos, como o Django, separadamente para cada projeto, dessa forma as versões das dependências de um projeto não irão afetar as de outro. As formas mais utilizadas para criar um ambiente virtual em python é utilizando o módulo [venv](https://docs.python.org/pt-br/3/library/venv.html) ou o anaconda, fique a vontade para escolher o seu.

Vamos utilizar o PIP, o gerenciador de pacotes do Python, para fazer a instalação do django:
```
pip install django
```

Para garantir que foi instalado corretamente, verifique qual versão está instalada (A minha versão é a 4.1):
```
python -m django --version
```

### Criação do projeto
Agora podemos realmente iniciar, o nosso primeiro passo é criar um projeto utilizando a ferramenta do `django-admin`. Caso você rode o apenas o comando `django-admin` em seu terminal, irá receber uma lista de comandos disponíveis para realizar, o comando que nos interessa agora é o `startproject` que irá criar toda a configuração de arquivos do Django de forma automática para nós. Para utilizar ele, basta executar esse comando em seu terminal:
```
django-admin startproject <nome_do_projeto>
```

O nome do meu projeto será "adm_biblioteca", mas você pode dar o nome que desejar ao seu.

Se tudo ocorreu bem, ele gerou uma pasta com o nome do seu projeto e dentro dela você irá encontrar uma estrutura de arquivos semelhante a essa:
<p align="center">
    <img src="https://ik.imagekit.io/6sszyq45h/estrutura_inicial_django_HMdmThCL7.png?ik-sdk-version=javascript-1.4.3&updatedAt=1659549838190" alt="estrutura-inicial-projeto">
</p>

Uma breve descrição de cada arquivo:
- asgi.py: arquivo para as configurações de ASGI do projeto
- wsgi.py: arquivo para as configurações de WSGI do projeto
- settings.py: é o arquivo principal de configurações, iremos utilizar ele bastante para realizar configurações de IPs permitidos, apps instalados, banco de dados, etc. 
- urls.py: armazena o caminho de todas as URLs do projeto
- manage.py: nos permitir interagir via linha de comando com o projeto que criamos, irá substituir o `django-admin` a partir de agora

Podemos verificar o nosso projeto rodando com o seguinte comando:
```
python manage.py runserver
```
Por padrão, ele irá rodar na porta 8000 do seu computador, mas você pode passar uma outra porta como parâmetro ou até mesmo um outro endereço IP além do localhost, como o IP da sua rede local por exemplo para deixar o projeto visível para todos da rede local. Para saber mais sobre o comando, execute `python manage.py runserver --help`

Após rodar o projeto, você deve receber a seguinte mensagem em seu terminal:
![imagem-terminal](https://ik.imagekit.io/6sszyq45h/projeto_rodando_jYr9WtNSP.png?ik-sdk-version=javascript-1.4.3&updatedAt=1659550874544)

E pode acessar o endereço http://localhost:8000/ para ver esta página:
![projeto-rodando](https://ik.imagekit.io/6sszyq45h/Screenshot_2022-08-03_at_15-26-51_The_install_worked_successfully_Congratulations__9uxJAT6lA.png?ik-sdk-version=javascript-1.4.3&updatedAt=1659551227007)

### Criação do app
Um app em Django é uma parte individual de um projeto e que é alto suficiente, ou seja, ele é sozinho uma aplicação completa que não depende de outros apps para funcionar. Para ficar mais claro, imagine que você quer construir um blog sobre moda e um e-commerce para vender roupas, você pode criar essas 2 aplicações dentro de um mesmo projeto de forma separada, cada um deles seria um app e não teriam dependências entre si porque são coisas distintas. Um projeto pode conter diversos apps.

Caso ainda não tenha ficado claro, essa é a descrição que a página do Django trás sobre esse assunto:
> "Qual é a diferença entre um projeto e um aplicativo? 
Um aplicativo é um aplicativo da web que faz algo – por exemplo, um sistema de blog, um banco de dados de registros públicos ou um pequeno aplicativo de pesquisa. Um projeto é uma coleção de configurações e aplicativos para um determinado site. Um projeto pode conter vários aplicativos. Um aplicativo pode estar em vários projetos."

No caso do nosso sistema, será necessário criar apenas 1 app pois apenas o que queremos é um sistema de administração para bibliotecas. 

Para adicionar um app ao projeto, é preciso executar esse comando:
```
python manage.py startapp <nome_do_app>
```

Vou escolher o nome "app_biblioteca" para o meu, mas novamente você pode ficar a vontade para escolher o seu.
Por padrão, ele irá criar a pasta com os arquivos do app dentro do projeto que criamos, mas você pode alterar o local de criação passando mais um parâmetro opcional com o caminho do novo diretório.

Essa é a estrutura do projeto:
<p align="center">
    <img src="https://ik.imagekit.io/6sszyq45h/estrutura-app_j_9Ma_Z9T.png?ik-sdk-version=javascript-1.4.3&updatedAt=1659552308847" alt="estrutura-app-django">
</p>

Detalhamento dos arquivos:
- admin.py: salva as configurações da dashboad de administração do app, veremos sobre isso posteriormente
- apps.py: armazena as configurações gerais do app
- models.py: salva os Models do banco de dados desse app
- tests.py: guarda as funções para testes automatizados
- views.py: salva as Views do app

Com o app em mãos, podemos fazer o nosso primeiro teste de acesso a uma view.
Dentro do seu app no arquivo `views.py`, digite o seguinte código:
![primeira-view-django](https://ik.imagekit.io/6sszyq45h/image_1__0H8Veybii.png?ik-sdk-version=javascript-1.4.3&updatedAt=1659552760927)

O que fizemos aqui foi definir uma função que irá receber uma requisição e retornará uma resposta por meio do método `HttpResponse` nativo do Django. Ela também recebe um parâmetro `request` com dados da requisição, veremos mais sobre ele futuramente.

Após isso, vamos criar um arquivo `urls.py` dentro da pasta do app, faremos isso para centralizar as URLs do nosso app dentro dele, assim teremos uma boa divisão caso futuramente queira adicionar um novo app.

O conteúdo desse arquivo é bem semelhante ao arquivo `urls.py` que tem dentro das configurações do projeto:
![arquivo-urls-django-app](https://ik.imagekit.io/6sszyq45h/image_1__VYZrwEzUp.png?ik-sdk-version=javascript-1.4.3&updatedAt=1659554338528)

Note que estamos importando o nosso arquivo de views na linha 2 e na linha 6 estamos declarando uma rota com o caminho `primeira_rota/` e com o nome `primeira_rota_do_app`. O caminho será utilizado na URL e o nome da rota será utilizado posteriormente quando quisermos fazer redirecionamentos.

Com isso, precisamos importar essas URLs do app dentro das URLs gerais do projeto:
![arquivo-urls-django-projeto](https://ik.imagekit.io/6sszyq45h/image_MI0p6OEKw.png?ik-sdk-version=javascript-1.4.3&updatedAt=1659554478902)

Para fazer a inclusão das URLs do app utilizamos o método `include` do Django, que é importado do módulo `django.urls`. Repare que a rota está iniciando com `meu_app/`, isso significa que todas as rotas do app terão o como prefixo essa rota. Logo, a rota que criamos terá que ser acessada pela URL `meu_app/primeira_rota/`.

Então podemos ver finalmente o que gerou o nosso trabalho! Rode o projeto com o `runserver` e acesse a rota http://localhost:8000/meu_app/primeira_rota/ . Você deverá ver algo como isso:
![tela-olá-mundo](https://ik.imagekit.io/6sszyq45h/image_2__50_049cHC.png?ik-sdk-version=javascript-1.4.3&updatedAt=1659554853785)

Como só temos 1 app em nosso projeto, não vejo a necessidade de termos um prefixo em nossas rotas, então podemos retirar esse prefixo substituindo a o `path` de inclusão no arquivo `urls.py`:
![novo-path](https://ik.imagekit.io/6sszyq45h/image_3__RtJRMIQsf.png?ik-sdk-version=javascript-1.4.3&updatedAt=1659555014306)

E a nossa rota agora pode ser acessada pelo caminho http://localhost:8000/primeira_rota/


## Próximos passos
Parabéns por chegar até aqui! Pegue o seu café e relaxe um pouco porque você já aprendeu muito até aqui.

Em nosso próximo artigo iremos abordar como realizar o CRUD com as tabelas do banco de dados. Link para o artigo:
- (ainda em construção)

Para ficar por dentro das atualizações, conecte-se comigo no Linkedin :smile:
https://www.linkedin.com/in/jackson-alves541/

Link do repositório final desse artigo:
https://github.com/jackson541/tutorial-django/tree/main/artigo_1

## Fontes
Essas foram algumas fontes utilizadas para a construção desse artigo:
- https://docs.djangoproject.com/en/4.1/intro/tutorial01/
- https://pt.wikipedia.org/wiki/Django_(framework_web)
- https://www.treinaweb.com.br/blog/entendendo-o-mtv-do-django
- https://pt.wikipedia.org/wiki/MVC
- https://www.educative.io/courses/grokking-the-object-oriented-design-interview/RMlM3NgjAyR