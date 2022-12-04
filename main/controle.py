from main.encontrartag import encontrar_tag_para_resumir
from main.models import Portal


def verificar_nome_portal(link):
    link_separado = link.split('.')    
    portal_coletado = link_separado[1]    
    if (portal_coletado != 'com'):
        portal_filtrado = portal_coletado
    else:
        portal_coletado = link_separado[0]
        portal_coletado = portal_coletado.split("//")
        portal_filtrado = portal_coletado[1]
    return portal_filtrado

def consultar_banco(portal_filtrado,link):
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