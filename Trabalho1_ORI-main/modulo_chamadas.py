import TrabalhoORI as t

#Ler StopWords
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

#Remover StopWords
t.lista1 = t.removerStopWords(t.lista1,1);
t.antesdeStemizar1  = t.lista1;
t.lista2 = t.removerStopWords(t.lista2,2);
t.antesdeStemizar2  = t.lista2;
t.lista3 = t.removerStopWords(t.lista3,3);
t.antesdeStemizar3  = t.lista3;
t.lista4 = t.removerStopWords(t.lista4,4);
t.antesdeStemizar4  = t.lista4;
t.lista5 = t.removerStopWords(t.lista5,5);
t.antesdeStemizar5  = t.lista5;
t.lista6 = t.removerStopWords(t.lista6,6);
t.antesdeStemizar6  = t.lista6;
t.lista7 = t.removerStopWords(t.lista7,7);
t.antesdeStemizar7  = t.lista7;




t.listamaePrint = [t.lista1, t.lista2 , t.lista3, t.lista4,t.lista5, t.lista6 , t.lista7 ] ;

#Stemizar
t.lista1 = t.Stemizar(t.lista1,1);
t.lista2 = t.Stemizar(t.lista2,2);
t.lista3 = t.Stemizar(t.lista3,3);
t.lista4 = t.Stemizar(t.lista4,4);
t.lista5 = t.Stemizar(t.lista5,5);
t.lista6 = t.Stemizar(t.lista6,6);
t.lista7 = t.Stemizar(t.lista7,7);


t.listamae = [t.lista1, t.lista2 , t.lista3, t.lista4,t.lista5, t.lista6 , t.lista7 ] ;
t.formatar_palavra(t.listamae, 'tamanq', 'tamanco');
t.formatar_palavra(t.listamae, 'tamanquinh', 'tamanco');
t.formatar_palavra(t.listamae, 'ligeirinh', 'ligeir');

#Printar a lista Stemizar

t.printarStermizado(t.lista1,t.antesdeStemizar1,1);
t.printarStermizado(t.lista2,t.antesdeStemizar2,2);
t.printarStermizado(t.lista3,t.antesdeStemizar3,3);
t.printarStermizado(t.lista4,t.antesdeStemizar4,4);
t.printarStermizado(t.lista5,t.antesdeStemizar5,5);
t.printarStermizado(t.lista6,t.antesdeStemizar6,6);
t.printarStermizado(t.lista7,t.antesdeStemizar7,7);




t.PrintPalavra(t.listamaePrint, t.listamae);

#Gera Indice Invertido
t.IndiceIv(t.listamae)







