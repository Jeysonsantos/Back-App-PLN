from main.models import Portal

from urllib.request import Request, urlopen
from bs4 import BeautifulSoup

global quantidade_paragrafos_por_tag
quantidade_paragrafos_por_tag = {}

# ------------------------------------------------------------------------------------------------

def verificar_nome_portal(link):

    # DADO UM LINK, RETORNA O NUCLEO DO LINK. EX: www.cnn.com.br -> retorna 'cnn'

    link_separado = link.split('.')
    portal_coletado = ''
    index = 0

    for i in link_separado:
        if (i == 'com'):
            index = link_separado.index('com')
            break
    if (index != 0):
        portal_coletado = link_separado[index-1]
    else:
        for string in link_separado:
            if 'com' in string:
                index = link_separado.index(string)
                portal_coletado = link_separado[index-1]

    portal_coletado = portal_coletado.split("//")

    if (len(portal_coletado) == 2):
        portal_filtrado = portal_coletado[1]
    else:
        portal_filtrado = portal_coletado[0]
    return portal_filtrado


def consultar_banco(link, portal_filtrado):
    query_coletado = []
    if (Portal.objects.filter(nomePortal=portal_filtrado)):
        query_coletado = Portal.objects.filter(
            nomePortal=portal_filtrado).values()

    else:
        Portal.objects.create(
            nomePortal=portal_filtrado, filtroTexto=encontrar_tag_para_resumir(link))
        query_coletado = Portal.objects.filter(
            nomePortal=portal_filtrado).values()

    dicio_coletado = query_coletado[0]
    tag_coletada = dicio_coletado['filtroTexto']
    return tag_coletada

# ------------------------------------------------------------------------------------------------

# def nucleo_link(link):

#     #DADO UM LINK, RETORNA O NUCLEO DO LINK. EX: www.cnn.com.br -> retorna 'cnn'

#     aux=''
#     nucleo=''
#     inicio=False
#     for i in link:
#         if i=='.':
#             if inicio==False:
#                 inicio=True
#             else:
#                 break
#         if inicio==True:
#             aux=aux+i
#     for i in aux:
#         if i!='.':
#             nucleo = nucleo + i
#     return nucleo

# ------------------------------------------------------------------------------------------------


def encontre(pagina):

    # RETORNA A TAG MAIN OU ARTICLE, QUE GERALMENTE OS TEXTOS FICAM DENTRO

    if '<main' in pagina:
        localizador = "main"
    elif '<article' in pagina:
        localizador = "article"

    return localizador

# ------------------------------------------------------------------------------------------------


def encontre_qual_tag_completa(tag_completa):

    # DADA UMA TAG COMPLETA, RETORNA A ABERTURA DA TAG COMPLETA, EX: '<div class="algumacoisa">'

    string_tag = str(tag_completa)
    tag_full = ''
    for i in string_tag[::1]:
        if i == '>':
            tag_full = tag_full+i
            break
        else:
            tag_full = tag_full+i

    return tag_full

# ------------------------------------------------------------------------------------------------


def encontre_qual_tag(tag_completa):

    # DADA UMA TAG COMPLETA, RETORNA O NOME DA TAG, EX: DADA  UMA TAG <p> Algo </p>. RETORNA 'p'

    string_tag = str(tag_completa)
    tag_contrario = ''
    tag = ''
    for i in string_tag[::-1]:
        if i == '/':
            break
        else:
            if i != '>':
                tag_contrario = tag_contrario+i
    for i in tag_contrario[::-1]:
        tag = tag+i

    return tag

# ------------------------------------------------------------------------------------------------


def is_tag(tag_teste):

    # DADA UMA POSSIVEL TAG, RETORNA TRUE SE FOR TAG E FALSO SE NÃO FOR.

    string_tag = str(tag_teste)
    if string_tag[0] == '<':
        return True
    else:
        return False

# ------------------------------------------------------------------------------------------------


def dif_algumas_tags(tag):

    # DADA UMA TAG, RETORNA FALSO SE A TAG FOR UMA DESSAS QUE ESTÃO NA LISTA

    string_tag = str(tag)
    retorno = True
    lista_retirar_tags = ['<a ', '<p>', '<h1', '<im',
                          '<ul', '<li', '<sp', '<sv', '<so', '<pi', '<pa']
    for i in lista_retirar_tags:
        if string_tag[0:3] != i:
            continue
        else:
            retorno = False
    return retorno

# ------------------------------------------------------------------------------------------------


def num_p(pagina):

    # RECEBE UMA TAG E FAZ UM DICIONARIO COM AS TAGS INTERNAS E QUANTOS PARAGRAFOS TEM CADA TAG INTERNA.

    for tag_1 in pagina:
        if is_tag(tag_1) and dif_algumas_tags(tag_1):
            tag_completa = encontre_qual_tag_completa(tag_1)
            quantidade_paragrafos_por_tag[tag_completa] = quant_paragraph(
                tag_1)
            num_p(tag_1)
    return quantidade_paragrafos_por_tag

# ------------------------------------------------------------------------------------------------


global quantidade_paragrafos_por_tag2
quantidade_paragrafos_por_tag2 = {}


def quant_p_geral_por_tag(pagina):
    pagina = pagina
    for i in pagina:
        if is_tag(i) and dif_algumas_tags(i):
            quantidade_paragrafos_por_tag = {}
            # IDENTIFICAR POR QUE O i NAO ES´TA FUNCIONANDO DA MANEIRA QUE DEVERIA
            quantidade_paragrafos_por_tag = num_p(i)
            result_final(i, quantidade_paragrafos_por_tag)
            quant_p_geral_por_tag(i)

# O PROBLEMA ESTÁ AQUI, num_p(i) não está funcionado como deveria, i é o problema

# ------------------------------------------------------------------------------------------------


def result_final(tag, quantidade_paragrafos_por_tag):

    # RECEBE A TAG E O DICIONARIO COM AS TAGS INTERNAS E QUANTOS P TEM EM CADA UMA E ADICIONA EM OUTRO DICIONARIO A TAG E A SOMA DE TODOS OS PARAGRAFOS DAS TAGS INTERNAS.

    tag_completa = encontre_qual_tag_completa(tag)
    global contador
    contador = 0
    for i in quantidade_paragrafos_por_tag:
        some = quantidade_paragrafos_por_tag[i]
        contador = contador + some
    quantidade_paragrafos_por_tag2[tag_completa] = contador

    contador = 0


# ------------------------------------------------------------------------------------------------

def quant_paragraph(tag):

    # DADA UMA TAG, VERIFICA QUANTOS PARAGRAFOS TEM COMO 'FILHOS' IMEDIATOS.

    cont = 0
    for i in tag:
        if encontre_qual_tag(i) == 'p':
            cont = cont+1
    return cont

# ------------------------------------------------------------------------------------------------


def encontrar_tag_para_resumir(link):
    link1 = Request(link,
                    headers={'User-Agent': ""})
    pagina = urlopen(link1).read().decode('utf-8', 'ignore')

    soup = BeautifulSoup(pagina, "lxml")

    global dicio_nucleo_tag
    dicio_nucleo_tag = {}
    # nucleo = nucleo_link(link)
    nucleo = verificar_nome_portal(link)
    cara = encontre(pagina)
    dicio_nucleo_tag[nucleo] = cara

    for i in dicio_nucleo_tag:
        if (i in link):
            for paragraph in soup.select(dicio_nucleo_tag[i]):
                num_p(paragraph)
                result_final(paragraph, quantidade_paragrafos_por_tag)
                quant_p_geral_por_tag(paragraph)
            break

    return dicio_nucleo_tag[nucleo]
