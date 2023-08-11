import PyPDF2
import nltk
#nltk.download('punkt')

#nltk.download('stopwords')
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import SnowballStemmer as snS
from collections import defaultdict, Counter

cor_vermelha = '\033[91m'
cor_verde = '\033[92m'
cor_azul = '\033[94m'
cor_reset = '\033[0m'
estilo_negrito = '\033[1m'
reset = '\033[0m'
cor_ciano = '\033[36m'

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
stop_words.append('');
stop_words.append('');
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
antesdeStemizar7=[];

def geradordelista(lista_destino, palavras):
    for palavra in palavras:
        lista_destino.append(palavra);


def lerPDF(lista, pos):
    pdf = open(pdfs[pos], 'rb');
    reader = PyPDF2.PdfReader(pdf);
    pagina = reader.pages[0];
    texto = pagina.extract_text();
    texto = texto.replace('…', ' …');
    palavras = word_tokenize(texto);
    geradordelista(lista, palavras);


def removerStopWords(lista, type):
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
            print(f"Doc{item} / {cont}'", end=" ")
    print("\n-+-+-+-+-+-+-+-+-+-+-+-+-+-..................-+-+-+-+-+-+-+-+-+-+-+-+-+-\n"+cor_reset)

def formatar_palavra(lista, palavraAntiga, palavraNova):
    i = 0
    for lista_interna in lista:
        for j, elemento in enumerate(lista_interna):
            if elemento == palavraAntiga:
                lista[i][j] = palavraNova
    i = i + 1


def PrintPalavra(listaAntiga, listaNova):
    print(cor_azul + "-+-+-+-+-+-+-+-+-+-+-+-+-+-" + estilo_negrito + f"+Palavras depois de juntar as listas:+" + reset + "" + cor_azul + "-+-+-+-+-+-+-+-+-+-+-+-+-+-\n")
    i = 0
    for lista_interna in listaAntiga:
        for j, elemento in enumerate(lista_interna):
            print(""+reset+f"{listaAntiga[i][j]} ---->" + cor_ciano+""+ f"\t{listaNova[i][j]}")
        i = i + 1
    print("-+-+-+-+-+-+-+-+-+-+-+-+-+-.............................................-+-+-+-+-+-+-+-+-+-+-+-+-+-\n")







def printarStermizado(lista_nova,lista_antiga, tipo):
    print(f""+cor_verde+"-+-+-+-+-+-+-+-+-+-+-+-+-+-"+estilo_negrito+f"+Palavras depois de Stemizar as listas {tipo}:+"+reset+""+cor_verde+"-+-+-+-+-+-+-+-+-+-+-+-+-+-\n")
    for palavra_antiga, palavra_nova in zip(lista_antiga, lista_nova):
        print(reset+""+ palavra_antiga + " ------> "+cor_ciano+""+ palavra_nova+""+reset)
    print("-+-+-+-+-+-+-+-+-+-+-+-+-+-.............................................-+-+-+-+-+-+-+-+-+-+-+-+-+-\n")




