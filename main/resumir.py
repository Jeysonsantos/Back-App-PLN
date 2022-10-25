from copyreg import remove_extension
from urllib.request import Request, urlopen
from bs4 import BeautifulSoup
from nltk.tokenize import word_tokenize
from nltk.tokenize import sent_tokenize
from nltk.probability import FreqDist
from collections import defaultdict
from heapq import nlargest

stopwords = {'aquelas', '|', 'também', 'essa', 'depois', 'foi', 'ser', 'terá', 'teve', '`', 'este', '}', 'nem', 'tinham', 'me', 'suas', 'tenha', 'às', 'teríamos', 'um', '>', 'são', '(', '_', 'aquela', 'muito', 'quem', 'tivesse', 'à', 'é', 'meu', 'houveremos', 'a', 'nossas', 'tinha', 'foram', 'estiver', 'pelas', 'só', 'houverão', 'esta', 'seja', 'haver', 'estiveram', '#', 'hajam', 'esses', 'ele', 'por', 'de', 'fora', 'em', 'e', 'fosse', 'hão', 'houveria', 'teremos', 'fomos', '*', 'aos', '/', '%', 'estavam', 'houvermos', '=', 'não', 'fôramos', 'hajamos', 'houverá', 'tivéramos', '<', 'éramos', 'com', 'houver', 'serão', 'já', ';', 'qual', 'seria', 'os', 'tenhamos', 'tínhamos', 'das', 'que', 'está', 'estive', 'estes', '[', 'estejamos', 'nos', 'sou', 'tua', 'nossos', 'seriam', ':', 'aquilo', 'até', 'estão', 'no', '?', ')', 'tu', 'nós', '.', 'sem', 'houveríamos', '\\', 'elas', 'vocês', 'tiveram', 'vos', 'houvemos', 'teus', 'eram', 'esse', 'aquele', 'essas', 'estiverem', 'dele', 'fossem', 'se', 'na', 'o', 'como', 'estivermos', 'será', 'estivessem', 'tiverem', 'forem', 'sejamos', 'houverem', 'temos', 'estava', 'uma', '+', 'numa', 'era', ']', 'tivessem', 'lhe', 'seremos', 'tenho', 'houveram', 'tivermos', 'mesmo', 'houve', 'houvesse', 'estou', 'estas', 'esteja', 'nosso', 'havemos', 'haja', 'mas', 'sejam', 'lhes', 'você', 'esteve', 'terão', 'formos', 'nossa', 'tém', '~', 'sua', 'ela', '$', 'quando', 'fôssemos', '"', '&', 'terei', 'houverei', 'pelo', 'estivemos', 'minhas', 'do', 'teriam', 'deles', 'pela', 'entre', 'eles', 'somos', '^', 'estivéramos', 'estávamos', 'tiver', 'teria', 'delas', '-', "'", 'pelos', 'mais', '{', 'minha', 'seríamos', 'num', 'estejam', 'isso', 'te', 'tivera', 'houvéramos', 'tive', 'for', 'estar', 'houvéssemos', '!', 'estamos', 'seu', 'há', 'houvera', ',', 'estivéssemos', 'tivéssemos', 'para', 'nas', 'ou', '@', 'as', 'dela', 'dos', 'da', 'houvessem', 'teu', 'seus', 'tuas', 'fui', 'tem', 'eu', 'houveriam', 'tivemos', 'aqueles', 'hei', 'estivera', 'tenham', 'serei', 'estivesse', 'ao', 'meus', 'isto'}

def resumir(link1):
    try:
        link = Request(link1,
                    headers={'User-Agent': ""})
        pagina = urlopen(link).read().decode('utf-8', 'ignore')

        soup = BeautifulSoup(pagina, "lxml")

        if("cnn" in link1):
            for paragraph in soup.select('div[class^=post__content]'):
                texto=paragraph.find_all('p')
            full_text=[]
            texto1=''
            for i in range(len(texto)):
                full_text.append(texto[i].get_text() + "\n\n")
            for i in full_text:
                texto1=texto1+i

        elif("bbc" in link1):
            for paragraph in soup.select('main'):
                texto=paragraph.find_all('p')
            full_text=[]
            texto1=''
            for i in range(len(texto)):
                if "Crédito," not in (texto[i].get_text()):
                    full_text.append(texto[i].get_text() + "\n\n")
            for i in full_text:
                texto1=texto1+i
        elif("g1" in link1):
            
            for paragraph in soup.select('div[class^=mc-article-body]'):
                texto=paragraph.find_all('p')
            full_text=[]
            texto1=''
            for i in range(len(texto)):
                if "Foto:" not in (texto[i].get_text()):
                    full_text.append(texto[i].get_text() + "\n\n")
            for i in full_text:
                texto1=texto1+i

        elif("r7" in link1):
            
            for paragraph in soup.select('article[class^=toolkit-media-content]'):
                texto=paragraph.find_all('p')
            full_text=[]
            texto1=''
            for i in range(len(texto)):
                if ("VEJA A COBERTURA COMPLETA") not in (texto[i].get_text()) and ("Luce Costa") not in (texto[i].get_text()):
                    full_text.append(texto[i].get_text() + "\n\n")
            for i in full_text:
                texto1=texto1+i

        
        elif("uol" in link1):
            
            for paragraph in soup.select('div[class^=text]'):
                texto=paragraph.find_all('p')
            full_text=[]
            texto1=''
            for i in range(len(texto)):
                full_text.append(texto[i].get_text() + "\n\n")
            for i in full_text:
                texto1=texto1+i
        else:
            return 'Não foi possível resumir, Tente um dos seguintes sites : R7, UOL, CNN, BCC ou G1.'


        sentencas = sent_tokenize(texto1)
        palavras = word_tokenize(texto1.lower())
        
        
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




link="https://www.cnnbrasil.com.br/internacional/exclusivo-cnn-autoridade-dos-eua-diz-que-russia-esta-queimando-suas-armas-de-alta-tecnologia-na-ucrania/"

link1="https://www.bbc.com/portuguese/geral-63317987"

link2="https://g1.globo.com/al/alagoas/eleicoes/2022/noticia/2022/10/20/ipec-em-al-paulo-dantas-tem-49percent-e-rodrigo-cunha-40percent.ghtml"

link3="https://noticias.r7.com/eleicoes-2022/fachin-nega-liminar-de-aras-para-derrubar-resolucao-que-da-poder-a-moraes-para-remover-postagens-22102022"

resumir(link3)