import TrabalhoORI as t

#Ler as palavras dos PDF
t.lerPDF(t.lista1, 0);
t.lista1.remove('uinhos')


t.lerPDF(t.lista2,1);
t.lerPDF(t.lista3,2);
t.lerPDF(t.lista4,3);
t.lerPDF(t.lista5,4);
t.lerPDF(t.lista6,5);
# juntando a palavra novas que por algum motivo saiu em duas partes sendo elas "nova" "s"
for i in range(len(t.lista6) - 1):
    if t.lista6[i] == "nova" and i < len(t.lista6) - 1:
        t.lista6[i] += t.lista6[i + 1]
        del t.lista6[i + 1]
        break
t.lerPDF(t.lista7, 6);

t.formatar_palavra(t.lista6, 'água', 'agua');#Atualiza as palavras água, pois com acentuação a ordem alafabetica não funciona corretamente



#Remover StopWords
t.lista1 = t.removerStopWords(t.lista1,1);
t.lista2 = t.removerStopWords(t.lista2,2);
t.lista3 = t.removerStopWords(t.lista3,3);
t.lista4 = t.removerStopWords(t.lista4,4);
t.lista5 = t.removerStopWords(t.lista5,5);
t.lista6 = t.removerStopWords(t.lista6,6);
t.lista7 = t.removerStopWords(t.lista7,7);



# guarda em lista auxiliares as palavras antes de serem estemizadas
t.antesdeStemizar1  = t.lista1;
t.antesdeStemizar2  = t.lista2;
t.antesdeStemizar3  = t.lista3;
t.antesdeStemizar4  = t.lista4;
t.antesdeStemizar5  = t.lista5;
t.antesdeStemizar6  = t.lista6;
t.antesdeStemizar7  = t.lista7;




t.antesDicionario = t.lista1+ t.lista2 + t.lista3+ t.lista4 + t.lista5+t.lista6 + t.lista7 #dicionario recebe as palavras antes de ser  estemizadas, juntando todas as listas



#Stemizar
t.lista1 = t.Stemizar(t.lista1);
t.lista2 = t.Stemizar(t.lista2);
t.lista3 = t.Stemizar(t.lista3);
t.lista4 = t.Stemizar(t.lista4);
t.lista5 = t.Stemizar(t.lista5);
t.lista6 = t.Stemizar(t.lista6);
t.lista7 = t.Stemizar(t.lista7);

#Atualiza as palavras que não foram estemizadas corretamentes
t.formatar_palavra(t.lista1, "tamanq", "tamanco");
t.formatar_palavra(t.lista1, "tamanquinh", "tamanco");
t.formatar_palavra(t.lista3, 'devagarinh', 'devagar');
t.formatar_palavra(t.lista7, 'grandã', 'grand');
t.formatar_palavra(t.lista5, 'amarelinh', 'amarel');
t.formatar_palavra(t.lista2, 'bichinh', 'bich');
t.formatar_palavra(t.lista3, 'menininh','menin')


t.dicionario = t.lista1+ t.lista2 + t.lista3+ t.lista4 + t.lista5+  t.lista6 + t.lista7 # dicionario recebe as palavras stemizadas, juntando todas as listas
t.listamae = [t.lista1, t.lista2 , t.lista3, t.lista4,t.lista5, t.lista6 , t.lista7 ]; # lista de listas(mae) com as palavras já tratadas, posteriormente ultilizada para o indice invertido

#Printaas listas juntas Stemizadas
t.printarStermizado(t.lista1,t.antesdeStemizar1,1);
t.printarStermizado(t.lista2,t.antesdeStemizar2,2);
t.printarStermizado(t.lista3,t.antesdeStemizar3,3);
t.printarStermizado(t.lista4,t.antesdeStemizar4,4);
t.printarStermizado(t.lista5,t.antesdeStemizar5,5);
t.printarStermizado(t.lista6,t.antesdeStemizar6,6);
t.printarStermizado(t.lista7,t.antesdeStemizar7,7);


t.removeRepetidos(t.dicionario,t.antesDicionario); #Remove as palavras repetidas do dicionario

print(t.dicionario)

t.PrintDicionario(t.dicionario, t.antesDicionario); #Exibe o dicionario com a palavra não estematizada para estematizada

t.IndiceIv(t.listamae);#Gera Indice Invertido

t.criar_pdf_com_lista_de_texto(t.listapalavraPDF); #gera PDF com indice Invertido


t.idf = t.lerPDFIndice(0)


print(t.idf)

print(t.wtf)


t.geradordeidfVSwtf()

t.escolhaPalavra()




