## Chat em Python com Identicador de Discurso de Odio com auxilio do BERTimbau.

#### Olá. Me chamo Gabriel Barreto e sou estudante de Segurança da Informação pela Universidade Federal do Ceará - Campus Jardins de Anita. Hoje, lhes apresento o seguinte projeto que desenvolvi ao longo de minha graduação com apoio do Dr. Prof. Juan Sebastian Toquica, docente pela mesma universidade citada anteriormente.

<div style="text-align: justify;">
O seguinte ReadMe (leia-me) detalha como se deu a criação do projeto em questão que se baseia em um chat interativo feito na linguagem de programação Python. O referido, funciona via IntraNet (Rede Interna) onde o usuário que deseja se conectar é requerido seu nome de usuário e o IP (Internet Protocol) do servidor. Esse por sua vez, o servidor, acompanha o chat de maneira ineterrupta durante toda a comunicação entre os usuários, apelidamos eles de clientes para melhor entendimento do processo de criação dos códigos. Esse projeto tem por finalidade, além de promover a comunicação entre dois usuários ou mais, um ambiente social saudável, visto que o foco do mesmo se fundamenta no combate a identificação do discurso de ódio, por ventura o mesmo traz consigo consequências danosas se assim for deixado somente como pauta de debate filosófico e não prática ativa dentro da sociedade. Tais medidas, tem como fim tornar a comunicação acolhedora para todos os seus participantes.
</div>
### Funcionalidades Disponíveis (até o momento 18/06/2024):

- Cliente(s) e servidor se conectam através de um IP e portas pré-definidos via código Python (Ambos mostrados na tela do servidor);
- Envio de mensagens de um para o outro, ambos os conectados podem observar as mensagens;
- Mensagem de Boas-vindas quando um novo cliente se conecta;
- Acompanhamento do Bate-papo pelo servidor;
- Registro do Bate-papo em um arquivo *.txt contendo: Data e Hora de todas as mensagens para posterior análise pelo administrador do servidor - apenas a titulo de “auditoria” posteriormente pelo administrador;
- Banimento manual pelo servidor tanto por IP (ainda a ser implementado, visto que o chat é somente IntraNet e tal funcionalidade não há ainda a urgência para ser realizada, restringindo-se somente ao banimento por nome) do cliente conectado quanto pelo seu nome de usuário, impossibilitando que este venha a se conectar em caso de alterar o nome ou variação do nome em caso de banimento tente se reconectar ao servidor - letras maiúsculas ou minusculas como exemplo. ex: gabriel; gAbriel);
- Tentativas falhas de conexão do usuário banido são mostradas na aba reservada ao servidor.
- Regionalismo para com palavras que possuam duplo sentido da região Nordeste;
- As mensagens são analisadas pelo BERTimbau (classificador) e é exibiido na tela do servidor sua respectiva classificação, como sendo 0 - Negativo, 1 - Positivo, ou se nenhum dos conceitos assim se aplicar, é classificado como sentimento neutro.
- Além da funcionalidade citada acima, a respeito do classificador de sentimentos (positivos, negativos e/ou neutros) o BERTimbau foi usado para dar ênfase e combater o discurso de ódio, visto que o mesmo, aplica uma multa (funcionalidade implementada posteriormente) ao usuário que assim optar por continuadamente insistir em usar dessa linguagem;

### Observações:
1ª. É entendido que, apesar de todo o esforço dedicado a este projeto, o dataset referido não comporta totalmente todas as possibilidades existentes de como uma palavra ou conjunto de frases tendem a se apresentar em meio a um contexto complexo na rede, isso posto, entende-se que muitas frases ainda apresentem divergência quanto ao entendimento humano se comparado a como o código entende como fixa ou não alterável;

2ª. O projeto tem como data final (30/12/2024), visto que é a data aproximadada de término de minha graduação no curso citado anteriormente no começo desse ReadMe (Leia-me);

3ª. "Variações imprevisíveis de comportamento guardam a chave para as portas da mente, onde tudo é nada e nada é tudo. - Chuck Schuldiner (DEATH)"
