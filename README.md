## Chat em Python com Identicador de Discurso de Odio com auxilio do BERTimbau.

#### Olá. Me chamo Gabriel Barreto e sou estudante de Segurança da Informação pela Universidade Federal do Ceará - Campus Jardins de Anita. Hoje, lhes apresento o seguinte projeto que desenvolvi ao longo de minha graduação com apoio do Dr. Prof. Juan Sebastian Toquica, docente pela mesma universidade citada anteriormente.

O seguinte leia-me detalha como se deu a criação do projeto em questão que se baseia em um chat interativo funcional feito em linguagem de programação Python. O referido funciona via IntraNet(Rede Interna) onde o usuário que se deseja conectar é pedido seu nome de usuário e o IP(Internet Protocol) do servidor, que acompanha o Chat de maneira ineterrupta durante a comunicação. Esse tem por objetivo, além de promover a comunicação entre dois usuários, um ambiente social saudável visando a identificação do discurso de ódio e informações a respeito do mesmo, consequências e advertências. Tais medidas visando tornar a comunicação acolhedora para todos os seus participantes.

### Funcioalidades Disponíveis (até o momento 18/06/2024):

- Cliente(s) e servidor se conectam através de um IP e portas pré-definidos via código Python (Ambos mostrados na tela do servidor);
- Envio de mensagens de um para o outro, ambos os conectados podem observar as mensagens;
- Mensagem de Boas-vindas quando um novo cliente se conecta;
- Acompanhamento do Bate-papo pelo servidor;
- Registro do Bate-papo em um arquivo *.txt contendo: Data e Hora de todas as mensagens para posterior análise pelo administrador do servidor - apenas a titulo de “auditoria” posteriormente pelo administrador;
- Banimento manual pelo servidor tanto por IP (ainda a ser implementado, visto que o chat é somente IntraNet e tal funcionalidade não há ainda a urgência para ser realizada, restringindo-se somente ao banimento por nome) do cliente conectado quanto pelo seu nome de usuário, impossibilitando que este venha a se conectar em caso de alterar o nome ou variação do nome em caso de banimento tente se reconectar ao servidor - letras maiúsculas ou minusculas como exemplo. ex: gabriel; gAbriel);
- Tentativas falhas de conexão do usuário banido são mostradas na aba reservada ao servidor.

