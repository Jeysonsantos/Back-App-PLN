from urllib.request import Request, urlopen
from bs4 import BeautifulSoup
from nltk.tokenize import word_tokenize
from nltk.tokenize import sent_tokenize
from nltk.probability import FreqDist
from collections import defaultdict
from heapq import nlargest

stopwords = {'aquelas', '|', 'também', 'essa', 'depois', 'foi', 'ser', 'terá', 'teve', '`', 'este', '}', 'nem', 'tinham', 'me', 'suas', 'tenha', 'às', 'teríamos', 'um', '>', 'são', '(', '_', 'aquela', 'muito', 'quem', 'tivesse', 'à', 'é', 'meu', 'houveremos', 'a', 'nossas', 'tinha', 'foram', 'estiver', 'pelas', 'só', 'houverão', 'esta', 'seja', 'haver', 'estiveram', '#', 'hajam', 'esses', 'ele', 'por', 'de', 'fora', 'em', 'e', 'fosse', 'hão', 'houveria', 'teremos', 'fomos', '*', 'aos', '/', '%', 'estavam', 'houvermos', '=', 'não', 'fôramos', 'hajamos', 'houverá', 'tivéramos', '<', 'éramos', 'com', 'houver', 'serão', 'já', ';', 'qual', 'seria', 'os', 'tenhamos', 'tínhamos', 'das', 'que', 'está', 'estive', 'estes', '[', 'estejamos', 'nos', 'sou', 'tua', 'nossos', 'seriam', ':', 'aquilo', 'até', 'estão', 'no', '?', ')', 'tu', 'nós', '.', 'sem', 'houveríamos', '\\', 'elas', 'vocês', 'tiveram', 'vos', 'houvemos', 'teus', 'eram', 'esse', 'aquele', 'essas', 'estiverem', 'dele', 'fossem', 'se', 'na', 'o', 'como', 'estivermos', 'será', 'estivessem', 'tiverem', 'forem', 'sejamos', 'houverem', 'temos', 'estava', 'uma', '+', 'numa', 'era', ']', 'tivessem', 'lhe', 'seremos', 'tenho', 'houveram', 'tivermos', 'mesmo', 'houve', 'houvesse', 'estou', 'estas', 'esteja', 'nosso', 'havemos', 'haja', 'mas', 'sejam', 'lhes', 'você', 'esteve', 'terão', 'formos', 'nossa', 'tém', '~', 'sua', 'ela', '$', 'quando', 'fôssemos', '"', '&', 'terei', 'houverei', 'pelo', 'estivemos', 'minhas', 'do', 'teriam', 'deles', 'pela', 'entre', 'eles', 'somos', '^', 'estivéramos', 'estávamos', 'tiver', 'teria', 'delas', '-', "'", 'pelos', 'mais', '{', 'minha', 'seríamos', 'num', 'estejam', 'isso', 'te', 'tivera', 'houvéramos', 'tive', 'for', 'estar', 'houvéssemos', '!', 'estamos', 'seu', 'há', 'houvera', ',', 'estivéssemos', 'tivéssemos', 'para', 'nas', 'ou', '@', 'as', 'dela', 'dos', 'da', 'houvessem', 'teu', 'seus', 'tuas', 'fui', 'tem', 'eu', 'houveriam', 'tivemos', 'aqueles', 'hei', 'estivera', 'tenham', 'serei', 'estivesse', 'ao', 'meus', 'isto'}

def resumir(link,stopwords):
    try:
        link = Request(link,
                    headers={'User-Agent': ""})
        pagina = urlopen(link).read().decode('utf-8', 'ignore')
        
        soup = BeautifulSoup(pagina, "lxml")
        try:
            texto = soup.find(id="noticia").text
        except:
            texto = ""
            for paragraph in soup.find_all('p'):
                texto += paragraph.text

        sentencas = sent_tokenize(texto)
        palavras = word_tokenize(texto.lower())
        
        
        palavras_sem_stopwords = [palavra for palavra in palavras if palavra not in stopwords]
        palavras_sem=[]
        for w in palavras:
            if w not in stopwords:
                palavras_sem.append(w)
        
        frequencia = FreqDist(palavras_sem_stopwords)
        
        sentencas_importantes = defaultdict(int)
        
        for i, sentenca in enumerate(sentencas):
            for palavra in word_tokenize(sentenca.lower()):
                if palavra in frequencia:
                    sentencas_importantes[i] += frequencia[palavra]
        
        
        idx_sentencas_importantes = nlargest(10, sentencas_importantes, sentencas_importantes.get)
        resumo_texto=''
        for i in sorted(idx_sentencas_importantes):
                resumo_texto=resumo_texto + sentencas[i]
            
        return resumo_texto
    except:
        return 'Não foi possível resumir esta URL, verifique-a.'