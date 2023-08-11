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

locale.setlocale(locale.LC_COLLATE, 'pt_BR.UTF-8')

cor_vermelha = '\033[91m'
cor_verde = '\033[92m'
cor_azul = '\033[94m'
cor_reset = '\033[0m'
estilo_negrito = '\033[1m'
reset = '\033[0m'
cor_ciano = '\033[36m'
PdfNome = "PalavrasStermizadas.pdf"

stop_words = stopwords.words('portuguese');
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
stop_words.append('');
stop_words.append('');
stop_words.append('');
stop_words.append('');
stop_words.append('');
stop_words.append('');
stop_words.append('');
stop_words.append('');

cont = 0;

pdfs = ['A_Canção_dos_tamanquinhos_Cecília_Meireles.pdf','A_Centopeia_Marina_Colasanti.pdf',
        'A_porta_Vinicius_de_Moraes.pdf','Ao_pé_de_sua_criança_Pablo_Neruda.pdf','As_borboletas_Vinicius_de_Moraes.pdf',
        'Convite_José_Paulo_Paes.pdf','Pontinho_de_Vista_Pedro_Bandeira.pdf'];


lista1 = []; lista2 = []; lista3 = []; lista4 = []; lista5 = []; lista6 = []; lista7 = []; listamae=[]; listamaePrint=[];
antesdeStemizar1 = []; antesdeStemizar2=[]; antesdeStemizar3=[]; antesdeStemizar4=[];antesdeStemizar5=[];antesdeStemizar6=[]
antesdeStemizar7=[]; dicionario = [] ; antesDicionario = [];


listapalavraPDF = [];  # Parte gerar PDF


def geradordelista(lista_destino, palavras):
    for palavra in palavras:
        lista_destino.append(palavra);


def lerPDF(lista, pos):
    pdf = open(pdfs[pos], 'rb');
    reader = PyPDF2.PdfReader(pdf);
    pagina = reader.pages[0];
    texto = pagina.extract_text();
    texto = texto.replace('…', ' …');
    palavras = word_tokenize(texto.lower());
    geradordelista(lista, palavras);


def removerStopWords(lista, type):
    lista.sort()
    print(cor_azul + "-+-+-+-+-+-+-+-+-+-+-+-+-+-" + estilo_negrito + f"+Palavras depois de removerStopWord lista{type}:+" + reset + "" + cor_azul + "-+-+-+-+-+-+-+-+-+-+-+-+-+-\n")
    palavras_impressas = set()
    lista_aux = [palavra for palavra in lista if palavra.lower() not in stop_words]  # List comprehension

    for i in lista:
        if i in lista_aux and i not in palavras_impressas:
            print(reset+ f"'{i}' ----> "+cor_ciano+f" '{i}'")
            palavras_impressas.add(i)  # Adiciona a palavra ao conjunto de palavras impressas

        elif i not in lista_aux and i not in palavras_impressas:
            print(reset+ f"'{i}' -----> "+cor_ciano+""+"stopWord")
            palavras_impressas.add(i)  # Adiciona a palavra ao conjunto de palavras impressas
    print(f"-+-+-+-+-+-+-+-+-+-+-+-+-+-.................................................-+-+-+-+-+-+-+-+-+-+-+-+-+-\n")
    return lista_aux



def Stemizar(lista, type):
    lista_stemizada = [palavra if len(palavra) <= 3 else stemmer.stem(palavra) for palavra in lista]
    return lista_stemizada



def IndiceIv(lists_of_words):

    print(cor_ciano+f"\n-+-+-+-+-+-+-+-+-+-+-+-+-+-"+estilo_negrito+"Discionario:"+reset+""+cor_ciano+"-+-+-+-+-+-+-+-+-+-+-+-+-+-\n")

    # Criar um dicionário para armazenar a contagem de ocorrências das palavras
    word_count = defaultdict(int)
    # Preencher a contagem de ocorrências
    for word_list in lists_of_words:
        for word in word_list:
            word_count[word] += 1

    # Criar um dicionário para armazenar as listas em que cada palavra aparece
    inverted_index = defaultdict(list)
    for list_index, word_list in enumerate(lists_of_words):
        for word in word_list:
            inverted_index[word].append(list_index)

    # Mostrar a quantidade de vezes que cada palavra aparece e em quais listas
    sorted_words = sorted(word_count.keys())
    for word in sorted_words:
        lists = inverted_index[word]
        print(f"\n{word}/ {word_count[word]}->", end=" ")
        contador = Counter(lists)
        for item, cont in contador.items():
            print(f"Doc{item+1} / {cont}'", end=" ")
            palavraPDF = (word + "/" + str(word_count[word]) + "-> Doc " + str(item+1) + " / " + str(cont))
            listapalavraPDF.append(palavraPDF)
    print("\n-+-+-+-+-+-+-+-+-+-+-+-+-+-..................-+-+-+-+-+-+-+-+-+-+-+-+-+-\n"+cor_reset)

def formatar_palavra(lista, palavraAntiga, palavraNova):
    for i, palavra in enumerate(lista):
        if palavra == palavraAntiga:
            lista[i] = palavraNova  # Atualiza com a palavraNova, não palavraAntiga


def PrintDicionario(Dicionario, AntesDicionario):
    Dicionario = sorted(Dicionario)
    AntesDicionario = sorted(AntesDicionario)

    print(cor_azul + "-+-+-+-+-+-+-+-+-+-+-+-+-+-" + estilo_negrito + f"+Palavras depois de juntar as listas:+" + reset + "" + cor_azul + "-+-+-+-+-+-+-+-+-+-+-+-+-+-\n")
    for palavra_antiga, palavra_nova in zip(AntesDicionario, Dicionario):
        print(reset+""+ palavra_antiga + " ------> "+cor_ciano+""+ palavra_nova+""+reset)
    print("-+-+-+-+-+-+-+-+-+-+-+-+-+-.............................................-+-+-+-+-+-+-+-+-+-+-+-+-+-\n")


def printarStermizado(lista_nova,lista_antiga, tipo):
    lista_antiga = sorted(lista_antiga)
    lista_nova = sorted(lista_nova)
    print(f""+cor_verde+"-+-+-+-+-+-+-+-+-+-+-+-+-+-"+estilo_negrito+f"+Palavras depois de Stemizar as listas {tipo}:+"+reset+""+cor_verde+"-+-+-+-+-+-+-+-+-+-+-+-+-+-\n")
    for palavra_antiga, palavra_nova in zip(lista_antiga, lista_nova):
        print(reset+""+ palavra_antiga + " ------> "+cor_ciano+""+ palavra_nova+""+reset)
    print("-+-+-+-+-+-+-+-+-+-+-+-+-+-.............................................-+-+-+-+-+-+-+-+-+-+-+-+-+-\n")


def removeRepetidos(lista, lista2):
    palavras_unicas = set()
    indices_a_remover = []

    for i, palavra in enumerate(lista):
        if palavra not in palavras_unicas:
            palavras_unicas.add(palavra)
        else:
            indices_a_remover.append(i)

    # Remove elements from both lists using the correct approach
    for i in reversed(indices_a_remover):
        lista.pop(i)
        lista2.pop(i)




#Funçao com o objetivo de gerar o pdf com o resultado final
def criar_pdf_com_lista_de_texto(lista_de_texto):
    c = canvas.Canvas(PdfNome, pagesize=letter)
    width, height = letter

    x, y = 100, height - 100
    espaco_entre_linhas = 20

    for texto in lista_de_texto:
        # Verifica se o texto cabe na página atual
        if y - espaco_entre_linhas < 50:  # Deixa uma margem na parte inferior
            c.showPage()  # Cria uma nova página
            y = height - 100  # Reinicia a posição vertical

        c.drawString(x, y, texto)
        y -= espaco_entre_linhas

    c.save()

