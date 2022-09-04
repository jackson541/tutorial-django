Seja bem-vindo(a)! :smile:

Vamos finalmente iniciar a parte principal do nosso projeto e desenvolver o CRUD do nosso sistema da biblioteca.

Se você caiu aqui de paraquedas e não entende o que é ou como funciona o Django, recomendo que pare um pouco para ver os artigos anteriores que irão te explicar melhor antes de continuar:

- [Artigo 1: Introdução](https://www.tabnews.com.br/jackson541/tutorial-de-django-introducao)
- [Artigo 2: Models e consultas](https://www.tabnews.com.br/jackson541/models-e-consultas-em-django)

## Criação dos usuários
A base do nosso projeto são os usuários que, como falamos antes, são divididos em administradores e leitores. Um bom ponto de partida é criando as ações de cadastro, login e logout deles.

Tínhamos criado anteriormente alguns models e rotas (como o model `Carro`) para fins didáticos, então irei remover eles do nosso projeto porque não irão servir para o que precisamos agora.

Como foi definido, essa será a relação entre os models do nosso projeto:

![models do projeto](https://ik.imagekit.io/6sszyq45h/diagrama_biblioteca_ejDRrNqdK.png?ik-sdk-version=javascript-1.4.3&updatedAt=1659547856181)

Veja que os administradores e os leitores compartilham os mesmos dados vindos da tabela `usuário`. Comodamente, o Django tem nativamente suporte para um sistema de usuários muito parecido com o que precisamos.

Esse suporte vem dentro da classe `User` que pode ser importado do módulo `django.contrib.auth.models`. Esses são alguns atributos dessa classe:
- **username**: Nome de usuário, é único dentro de toda a aplicação,
- **first_name**: Primero nome do usuário,
- **last_name**: Sobrenome do usuário,
- **email**: Email do usuário,
- **password**: Senha da conta, esse campo é salvo no formato de um hash para garantir a segurança,
- **superuser**: Define se o usuário tem acesso super, ou seja, tem todas as permissões e acessos possíveis (veremos sobre isso posteriormente),
- **is_staff**: Salva se o usuário tem acesso ao painel de administração (veremos sobre isso posteriormente),
- **is_active**: Define se a conta está ativa,
- **groups**: Relação com os grupos aos quais o usuário pertence (veremos sobre isso posteriormente),
- **permissions**: Permissões que usuário tem (veremos sobre isso posteriormente),

O model `User` tem vários outros atributos e métodos úteis que podem ser utilizados, você pode [conferir eles aqui.](https://docs.djangoproject.com/en/4.1/ref/contrib/auth/#django.contrib.auth.models.User)

Os atributos acima são os mesmos que precisamos para os nossos usuários (nome, email, username e senha). Sendo assim, vamos utilizar essa poderosa ferramenta do Django para administrar eles.

Podemos de forma simples fazer uma herança do model `User` para o `Administrador` e o `Leitor`:

<p align="center">
    <img src="https://ik.imagekit.io/6sszyq45h/image_nld6hCG2E.png?ik-sdk-version=javascript-1.4.3&updatedAt=1661263304272" alt="models dos usuarios">
</p>

<details><summary>Código da imagem</summary>
Recomendo que escreva o código em vez de copiar para fixar melhor! 😉
    
```python
from django.db import models
from django.contrib.auth.models import User


class Administrador(User):
    pass


class Leitor(User):
    pass
```
    
</details>


Lembre-se que esse código deve ser inserido dentro do seu arquivo `models.py` do seu app. Caso não esteja lembrando disso, recomendo que volte e dê uma rápida olhada [no primeiro artigo](https://www.tabnews.com.br/jackson541/tutorial-de-django-introducao) dessa série.

Após criar e executar as migrações desses models, podemos entrar na `shell` para verificar se está tudo correto:

<p align="center">
    <img src="https://ik.imagekit.io/6sszyq45h/image_1__aA3hnlmMz.png?ik-sdk-version=javascript-1.4.3&updatedAt=1661263800472" alt="criando adm pela shell">
</p>

<details><summary>Código da imagem</summary>
Recomendo que escreva o código em vez de copiar para fixar melhor! 😉
    
```python
    
>>> adm = Administrador.objects.create(username='nome_usuario1', email='emailteste@gmail.com', first_name='jackson', last_name = 'alves')
>>> 
>>> adm.__dict__
{'_state': <django.db.models.base.ModelState object at 0x7f74754338b0>, 'id': 2, 'password': '', 'last_login': None, 'is_superuser': False, 'username': 'nome_usuario1', 'first_name': 'jackson', 'last_name': 'alves', 'email': 'emailteste@gmail.com', 'is_staff': False, 'is_active': True, 'date_joined': datetime.datetime(2022, 8, 23, 14, 9, 35, 185906, tzinfo=datetime.timezone.utc), 'user_ptr_id': 2}
    
```
    
</details>

Se tudo funcionou, deve ter um retorno como acima em que criamos um objeto do model `Administrador`, mas com os atributos do `User` graças a herança. 

Repare que não definimos a senha do usuário diretamente em sua criação, fizemos isso porque o `User` possui o método `set_password` que irá salvar ela passando por um algoritmo de criptografia:
    
<p align="center">
    <img src="https://ik.imagekit.io/6sszyq45h/image_wnHcKhsZ3.png?ik-sdk-version=javascript-1.4.3&updatedAt=1661264648940" alt="alterando senha do usuário">
</p>

    
<details><summary>Código da imagem</summary>
Recomendo que escreva o código em vez de copiar para fixar melhor! 😉
    
```python
    
>>> adm.set_password('alguma_senha')
>>> adm.save()
>>> 
>>> 
>>> adm.password
'pbkdf2_sha256$390000$rGHj6jAeTY8FzI29UDADqN$/eel0RJ57OV9dJCGobvRsIFYd4oZxjCjHDOgT1ysgcc='
>>>     
```
    
</details>
    
Por padrão, o Django utiliza o algoritmo [PBKDF2](https://en.wikipedia.org/wiki/PBKDF2) para a criptografia das senhas, mas pode ser alterado para outros caso deseje. Aqui está a [documentação oficial](https://docs.djangoproject.com/en/4.1/topics/auth/passwords/) sobre senhas.

E como faremos para verificar se as senhas digitadas quando criamos o site?
    
Para isso existe mais um método, o `check_password` que irá verificar a senha com base no algoritmo do projeto:
    
<p align="center">
    <img src="https://ik.imagekit.io/6sszyq45h/image_tewWlD2bX.png?ik-sdk-version=javascript-1.4.3&updatedAt=1661265180706" alt="verificando senha do usuário">
</p>

<details><summary>Código da imagem</summary>
Recomendo que escreva o código em vez de copiar para fixar melhor! 😉
    
```python
    
>>> adm.check_password('senha123')
False
>>> 
>>> adm.check_password('alguma_senha')
True
```
    
</details>
    
## Utilizando os templates
    
Agora que já sabemos como criar nossos usuários, que são o coração do nosso sistema, vamos partir para deixar isso mais fácil e automático com as páginas HTML.
    
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
   
## Fontes
Essas foram algumas fontes utilizadas para a construção desse artigo:
- https://docs.djangoproject.com/en/4.1/ref/contrib/auth/#django.contrib.auth.models.User
- https://docs.djangoproject.com/en/4.1/topics/auth/passwords/
- https://en.wikipedia.org/wiki/PBKDF2