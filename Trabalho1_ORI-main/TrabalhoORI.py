import locale

import PyPDF2
import nltk
#nltk.download('punkt')

#nltk.download('stopwords')
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import SnowballStemmer as snS
from collections import defaultdict, Counter
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import math
locale.setlocale(locale.LC_COLLATE, 'pt_BR.UTF-8') #UTF-8
import re
import pandas as pd
import numpy as np

#Cores para estilo de apresentação
cor_vermelha = '\033[91m';
cor_verde = '\033[92m';
cor_azul = '\033[94m';
cor_reset = '\033[0m';
estilo_negrito = '\033[1m';
reset = '\033[0m';
cor_ciano = '\033[36m';
PdfNome = "IndiceInv.pdf";


stop_words = stopwords.words('portuguese'); #Lista de StopWord
stemmer = snS('portuguese')
stop_words.append(",");
stop_words.append(':');
stop_words.append('.');
stop_words.append('-');
stop_words.append('!');
stop_words.append('—');
stop_words.append('oh');
stop_words.append('…');
stop_words.append('?');
stop_words.append('troc');
stop_words.append('lá');
stop_words.append('pra');
stop_words.append('tudo');
stop_words.append('entre');
stop_words.append('dos');
stop_words.append('ainda');
stop_words.append('então');
stop_words.append('pouco');
stop_words.append('então');
stop_words.append('cada');#determinante indefinido
stop_words.append('quanto'); #advérbio

cont = 0;

#Lista nome dos PDFs
pdfs = ['A_Canção_dos_tamanquinhos_Cecília_Meireles.pdf','A_Centopeia_Marina_Colasanti.pdf',
        'A_porta_Vinicius_de_Moraes.pdf','Ao_pé_de_sua_criança_Pablo_Neruda.pdf','As_borboletas_Vinicius_de_Moraes.pdf',
        'Convite_José_Paulo_Paes.pdf','Pontinho_de_Vista_Pedro_Bandeira.pdf'];

#Listas ultilizadas
lista1 = []; lista2 = []; lista3 = []; lista4 = []; lista5 = []; lista6 = []; lista7 = []; listamae=[]; listamaePrint=[];
antesdeStemizar1 = []; antesdeStemizar2=[]; antesdeStemizar3=[]; antesdeStemizar4=[];antesdeStemizar5=[];antesdeStemizar6=[]
antesdeStemizar7=[]; dicionario = [] ; antesDicionario = [];
listapalavraPDF = [];  # Parte gerar PDF

idf = {};
wtf = {};
idfVSwtf = {};
ProdutoInterno = {}
palavrasUser =[];
padrao = r'Doc\d+ / \d+'





def lerPDF(lista, pos): #leitura do PDF
    pdf = open(pdfs[pos], 'rb');
    reader = PyPDF2.PdfReader(pdf);
    pagina = reader.pages[0];
    texto = pagina.extract_text();
    texto = texto.replace('…', ' …');
    palavras = word_tokenize(texto.lower()); #tokeniza as palavras
    geradordelista(lista, palavras); # envia a lista e adiciona as palavras tokenizadas nela

def geradordelista(lista_destino, palavras): #geraLista
    for palavra in palavras: #percorre a lista de palavras tokenizadas e adiciona na lista de destino
        lista_destino.append(palavra);


def removerStopWords(lista, type): #remove as stopwords
    lista.sort(); #ordem alfabetica
    print(cor_azul + "-+-+-+-+-+-+-+-+-+-+-+-+-+-" + estilo_negrito + f"+Palavras depois de removerStopWord lista{type}:+" + reset + "" + cor_azul + "-+-+-+-+-+-+-+-+-+-+-+-+-+-\n")
    palavras_impressas = set();
    lista_aux = [palavra for palavra in lista if palavra.lower() not in stop_words];  # List comprehension que verifica se a palavra não está na lista de stopwords, caso esteja ela não é adicionada a lista

    for i in lista:
        if i in lista_aux and i not in palavras_impressas:
            print(reset+ f"'{i}' ----> "+cor_ciano+f" '{i}'"); #printa as palavras não stopword
            palavras_impressas.add(i) ; # Adiciona a palavra ao conjunto de palavras impressas

        elif i not in lista_aux and i not in palavras_impressas:
            print(reset+ f"'{i}' -----> "+cor_ciano+""+"stopWord");#printa as palavras stopword retiradas
            palavras_impressas.add(i) ; # Adiciona a palavra ao conjunto de palavras impressas
    print(f"-+-+-+-+-+-+-+-+-+-+-+-+-+-.................................................-+-+-+-+-+-+-+-+-+-+-+-+-+-\n")
    return lista_aux;



def Stemizar(lista): #estemiza as palavras
    lista_stemizada = [palavra if len(palavra) <= 3 else stemmer.stem(palavra) for palavra in lista]; # se a palavra for menor que 3letras, não é stemizada, apenas adicionada na lista
    return lista_stemizada; #retorna a lista stemizada


def IndiceIv(lists_of_words):
    print(cor_ciano + f"\n-+-+-+-+-+-+-+-+-+-+-+-+-+-" + estilo_negrito + "Discionario:" + reset + "" + cor_ciano + "-+-+-+-+-+-+-+-+-+-+-+-+-+-\n")

    # Criar um dicionário para armazenar a contagem de ocorrências das palavras
    word_count = defaultdict(int)
    # Preencher a contagem de ocorrências e também a contagem de documentos em que cada palavra ocorre
    word_document_count = defaultdict(int)
    for list_index, word_list in enumerate(lists_of_words):
        for word in set(word_list):  # Usamos set para contar apenas uma vez por documento
            word_count[word] += 1
            word_document_count[word] += 1

    # Mostrar a quantidade de vezes que cada palavra aparece e em quantos documentos
    sorted_words = sorted(word_count.keys())

    for word in sorted_words:
        doc_count = word_document_count[word]
        print(f"\n{word}/{doc_count}->", end="")
        word_info = f"{word} / {doc_count} -> "

        for list_index, word_list in enumerate(lists_of_words):
            if word in word_list:
                word_occurrences = word_list.count(word)
                print(f"Doc{list_index + 1}/{word_occurrences}", end=" ")
                word_info += f"Doc{list_index + 1} / {word_occurrences} "

        listapalavraPDF.append(word_info)

    print("\n-+-+-+-+-+-+-+-+-+-+-+-+-+-..................-+-+-+-+-+-+-+-+-+-+-+-+-+-\n" + cor_reset)


def formatar_palavra(lista, palavraAntiga, palavraNova): # Atualiza com a palavraNova a lista.
    for i, palavra in enumerate(lista):
        if palavra == palavraAntiga:
            lista[i] = palavraNova;


def PrintDicionario(Dicionario, AntesDicionario): #exibe o antes de depois do dicionario com as palavras estermizadas.
    Dicionario = sorted(Dicionario); #coloca a lista em ordem alfabetica.
    AntesDicionario = sorted(AntesDicionario); #coloca a lista em ordem alfabetica.

    print(cor_azul + "-+-+-+-+-+-+-+-+-+-+-+-+-+-" + estilo_negrito + f"+Palavras depois de juntar as listas:+" + reset + "" + cor_azul + "-+-+-+-+-+-+-+-+-+-+-+-+-+-\n");
    for palavra_antiga, palavra_nova in zip(AntesDicionario, Dicionario):
        print(reset+""+ palavra_antiga + " ------> "+cor_ciano+""+ palavra_nova+""+reset);
    print("-+-+-+-+-+-+-+-+-+-+-+-+-+-.............................................-+-+-+-+-+-+-+-+-+-+-+-+-+-\n")


def printarStermizado(lista_nova,lista_antiga, tipo):
    lista_antiga = sorted(lista_antiga) #coloca a lista em ordem alfabetica
    lista_nova = sorted(lista_nova) #coloca a lista em ordem alfabetica
    print(f""+cor_verde+"-+-+-+-+-+-+-+-+-+-+-+-+-+-"+estilo_negrito+f"+Palavras depois de Stemizar a lista {tipo}:+"+reset+""+cor_verde+"-+-+-+-+-+-+-+-+-+-+-+-+-+-\n");
    for palavra_antiga, palavra_nova in zip(lista_antiga, lista_nova):
        print(reset+""+ palavra_antiga + " ------> "+cor_ciano+""+ palavra_nova+""+reset);
    print("-+-+-+-+-+-+-+-+-+-+-+-+-+-.............................................-+-+-+-+-+-+-+-+-+-+-+-+-+-\n");


def removeRepetidos(lista, lista2): # remove as palavras repetidas da lista do dicionario e a lista antiga anstes da estermizar
    palavras_unicas = set();
    indices_a_remover = [];

    for i, palavra in enumerate(lista):
        if palavra not in palavras_unicas:
            palavras_unicas.add(palavra); #adiciona a palavra a lista
        else:
            indices_a_remover.append(i); #caso a palavra já esteja na lista, armazena seu indice


    for i in reversed(indices_a_remover): # se eu encontrar a palavra eu removo elas de traz para frente das duas listas pois, que possuem as mesmas posições
        lista.pop(i);
        lista2.pop(i);




#Funçao com o objetivo de gerar o pdf com o resultado final
def criar_pdf_com_lista_de_texto(lista_de_texto):
    c = canvas.Canvas(PdfNome, pagesize=letter)
    width, height = letter;

    x, y = 100, height - 100;
    espaco_entre_linhas = 20;

    for texto in lista_de_texto:
        # Verifica se o texto cabe na página atual
        if y - espaco_entre_linhas < 50:  # Deixa uma margem na parte inferior
            c.showPage() ; # Cria uma nova página
            y = height - 100  # Reinicia a posição vertical

        c.drawString(x, y, texto);
        y -= espaco_entre_linhas;

    c.save();


def lerPDFIndice(pos):
    pdf = open('IndiceInv.pdf', 'rb')
    reader = PyPDF2.PdfReader(pdf)

    # Dicionário para armazenar as palavras e seus valores


    # Variável para armazenar os resultados encontrados
    resultados = []

    # Iterar por todas as páginas
    for pagina in reader.pages:
        texto = pagina.extract_text()

        # Divida o texto da página em linhas
        linhas = texto.split('\n')

        # Iterar pelas linhas e faça o que desejar com cada linha
        for linha in linhas:
            # Verifique se a linha contém pelo menos três palavras
            palavras = linha.split()
            if len(palavras) >= 3:
                palavra = palavras[0]
                valor_palavra = palavras[2]
                valor_palavra = int(valor_palavra)
                idf[palavra] = math.log((7 / valor_palavra), 10)

            resultados = re.findall(padrao, linha)
            for resultado in resultados:
                partes = resultado.split(" / ")  # Divide a correspondência em partes usando " / "
                doc = partes[0]  # A primeira parte é o "Doc"
                valor = [partes[0], math.log(int(partes[1]), 10) +1]  # A segunda parte é o valor após " / "


                # Use a palavra encontrada como chave no dicionário e armazene o valor como uma lista
                if palavra in wtf:
                    wtf[palavra].append(valor)
                else:
                    wtf[palavra] = [valor]

    pdf.close()
    # Agora, idf é um dicionário onde a chave é a palavra e o valor é o valor_palavra
    return idf

def geradordeidfVSwtf():
    for palavra, valor_idf in idf.items():
        if palavra in wtf:
            idfVSwtf[palavra] = []
            for doc, valor_wtf in wtf[palavra]:
                idfVSwtf[palavra].append([doc, valor_idf * valor_wtf])

    print(idfVSwtf)


def escolhaPalavra():
    i = 0
    continuar = True
    palavrasUser = []  # Inicialize a lista palavrasUser
    while continuar:
        palavra = input(f"Digite a {i+1}ª palavra (ou digite 'sair' para encerrar): ")
        if palavra.lower() == 'sair':
            continuar = False
        else:
            palavrasUser.append(palavra)
        i += 1

    # Inicialize os vetores auxiliares com zeros
    doz1 = [0] * len(palavrasUser)
    doz2 = [0] * len(palavrasUser)
    doz3 = [0] * len(palavrasUser)
    doz4 = [0] * len(palavrasUser)
    doz5 = [0] * len(palavrasUser)
    doz6 = [0] * len(palavrasUser)
    doz7 = [0] * len(palavrasUser)
    Vcons = [0] * len(palavrasUser)


    for palavra in palavrasUser:
        if palavra in idfVSwtf:  # Verifique se a palavra está em idfVSwtf
            for doc, valor in idfVSwtf[palavra]:
                if doc == 'Doc1':
                    doz1[palavrasUser.index(palavra)] = valor
                    Vcons[palavrasUser.index(palavra)] = idf[palavra]
                elif doc == 'Doc2':
                    doz2[palavrasUser.index(palavra)] = valor
                    Vcons[palavrasUser.index(palavra)] = idf[palavra]
                elif doc == 'Doc3':
                    doz3[palavrasUser.index(palavra)] = valor
                    Vcons[palavrasUser.index(palavra)] = idf[palavra]
                elif doc == 'Doc4':
                    doz4[palavrasUser.index(palavra)] = valor
                    Vcons[palavrasUser.index(palavra)] = idf[palavra]
                elif doc == 'Doc5':
                    doz5[palavrasUser.index(palavra)] = valor
                    Vcons[palavrasUser.index(palavra)] = idf[palavra]
                elif doc == 'Doc6':
                    doz6[palavrasUser.index(palavra)] = valor
                    Vcons[palavrasUser.index(palavra)] = idf[palavra]
                elif doc == 'Doc7':
                    doz7[palavrasUser.index(palavra)] = valor
                    Vcons[palavrasUser.index(palavra)] = idf[palavra]


    matriz = pd.DataFrame({
        "doc1": doz1,
        "doc2": doz2,
        "doc3": doz3,
        "doc4": doz4,
        "doc5": doz5,
        "doc6": doz6,
        "doc7": doz7,
        "Vcons": Vcons

    }, index=palavrasUser)

    print("Matriz: ")
    print(matriz)

    for coluna in matriz.columns:
        print(f"Coluna '{coluna}':")
        valores_quadrados = matriz[coluna] ** 2
        soma_quadrados = valores_quadrados.sum()

        # Verifique se a soma dos quadrados não é zero antes de calcular a raiz quadrada
        if soma_quadrados != 0:
            raiz_soma_quadrados = np.sqrt(soma_quadrados)
            matriz[coluna] = matriz[coluna] / raiz_soma_quadrados
            print("Valores ao quadrado:", valores_quadrados.tolist())
            print("Soma dos quadrados:", soma_quadrados)
            print("Raiz da soma dos quadrados:", raiz_soma_quadrados)
        else:
            print("Todos os valores na coluna são zero, evitando divisão por zero.")

    print("Calculado a raiz da soma: ")
    print(matriz)

    print("Normatizazado: ")
    for coluna in matriz.columns:
        matriz[coluna] = matriz[coluna] * matriz['Vcons']
    print(matriz)

    for coluna in matriz.columns.tolist():
        if coluna != 'Vcons':
            ProdutoInterno[coluna] = matriz[coluna].sum();

    print("\nProduto Interno: ")
    print(ProdutoInterno)

    ProdutoInterno_ordenado = dict(sorted(ProdutoInterno.items(), key=lambda item: item[1], reverse=True)) #Valores do dicionario do maior para o menor
    i = 0;
    for chave,valor in ProdutoInterno_ordenado.items():
        i +=1
        print(f"O documento {chave} está na {i} posição com o valor {valor}\n");
