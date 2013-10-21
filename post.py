#!/usr/bin/python
# -*- coding: utf-8 -*-
import httplib 
import urllib 
import urllib2 
import re
import itertools
import os.path
import time
import HTMLParser

url = 'http://sistemas.saude.rj.gov.br/tabnet/tabcgi.exe?sihsus/internr.def'

year_values = {}
for year in range(8,13):
    key = "ano_" + str(2000 + year)
    year_values[key] = []
    for month in range(12,0, -1):
        year_values[key] += [ ( "Arquivos" , "ihrj%02d%02d.dbf" % (year, month) ) ]

gender_values = {
    "sexo_masculino" : [ ( "SSexo" , "1") ],
    "sexo_feminino" : [ ( "SSexo" , "2") ],
#    "sexo_ignorado" : [ ( "SSexo" , "3") ]
    "sexo_todos" : [ ("SSexo" , "TODAS_AS_CATEGORIAS__") ]
}

age18_values = {
    "idade_60a69": [
        ( "SIdade_%2818_faixas%29" , "14"),
        ( "SIdade_%2818_faixas%29" , "15"),
    ],
    "idade_70a79": [
        ( "SIdade_%2818_faixas%29" , "16"),
        ( "SIdade_%2818_faixas%29" , "17"),
    ],
    "idade_80+": [
        ( "SIdade_%2818_faixas%29" , "18")
    ],
    "idade_todos": [
        ( "SIdade_%2818_faixas%29" , "14"),
        ( "SIdade_%2818_faixas%29" , "15"),
        ( "SIdade_%2818_faixas%29" , "16"),
        ( "SIdade_%2818_faixas%29" , "17"),
        ( "SIdade_%2818_faixas%29" , "18")
    ]
}

cap_values = {}
for cap in range(1,24):
    cap_values["cap%02d" % cap] = [ ( "SDiagn%F3stico_-_cap%EDtulo" , "%d" % cap) ]

region_values = {
    "baia_da_ilha_grande" : [ ( "SRegi%E3o_de_Sa%FAde_resid%EAncia", "1" ) ],
    "baixada_litoranea" : [ ( "SRegi%E3o_de_Sa%FAde_resid%EAncia", "2" ) ],
    "centro-sul" : [ ( "SRegi%E3o_de_Sa%FAde_resid%EAncia", "3" ) ],
    "medio_paraiba" : [ ( "SRegi%E3o_de_Sa%FAde_resid%EAncia", "4" ) ],
    "metropolitana_I" : [ ( "SRegi%E3o_de_Sa%FAde_resid%EAncia", "5" ) ],
    "metropolitana_II" : [ ( "SRegi%E3o_de_Sa%FAde_resid%EAncia", "6" ) ],
    "noroeste" : [ ( "SRegi%E3o_de_Sa%FAde_resid%EAncia", "7" ) ],
    "norte" : [ ( "SRegi%E3o_de_Sa%FAde_resid%EAncia", "8" ) ],
    "serrana" : [ ( "SRegi%E3o_de_Sa%FAde_resid%EAncia", "9" ) ],
    "RJ" : [ ( "SRegi%E3o_de_Sa%FAde_resid%EAncia", "TODAS_AS_CATEGORIAS__" ) ]
}

increment_values = {
    "aih": [ ( "Incremento" , "Quantidade_de_AIH" ) ],
    "acompanhantes": [ ( "Incremento" , "M%E9dia_de_di%E1rias_de_acompanh" ) ],
    "obitos": [ ( "Incremento" , "%D3bitos" ) ],
    "permanencia": [ ( "Incremento" , "M%E9dia_de_perman%EAncia" ) ],
    "custo": [ ( "Incremento" , "Valor_total" ) ]
}

original_values = [
    ( "Linha" , "Diagn%F3stico_-_cap%EDtulo"),
    ( "Coluna" , "Ano_do_processamento"),
    ( "SDiagn%F3stico_-_cap%EDtulo" , "TODAS_AS_CATEGORIAS__"),
    ( "SMunic%EDpio_de_resid%EAncia" , "TODAS_AS_CATEGORIAS__"),
    ( "SRegi%E3o_de_Sa%FAde_resid%EAncia" , "TODAS_AS_CATEGORIAS__"),
    ( "SRegi%E3o_de_Governo_resid%EAncia" , "TODAS_AS_CATEGORIAS__"),
    ( "SMicrorregi%E3o_IBGE_resid%EAncia" , "TODAS_AS_CATEGORIAS__"),
    ( "SMunic%EDpio_de_interna%E7%E3o" , "TODAS_AS_CATEGORIAS__"),
    ( "SRegi%E3o_de_Sa%FAde_interna%E7%E3o" , "TODAS_AS_CATEGORIAS__"),
    ( "SRegi%E3o_de_Governo_interna%E7%E3o" , "TODAS_AS_CATEGORIAS__"),
    ( "SMicrorregi%E3o_IBGE_interna%E7%E3o" , "TODAS_AS_CATEGORIAS__"),
    ( "SUF%2FMunic%EDpio_gestor" , "TODAS_AS_CATEGORIAS__"),
    ( "SHospital_RJ_%28CNES%29" , "TODAS_AS_CATEGORIAS__"),
    ( "SHospital_fora_do_RJ_%28CNES%29" , "TODAS_AS_CATEGORIAS__"),
    ( "SHospital_RJ_%28CNPJ%29" , "TODAS_AS_CATEGORIAS__"),
    ( "SHospital_fora_do_RJ_%28CNPJ%29" , "TODAS_AS_CATEGORIAS__"),
    ( "SMantenedora" , "TODAS_AS_CATEGORIAS__"),
    ( "SEstabelecimento_SES-RJ" , "TODAS_AS_CATEGORIAS__"),
    ( "STipo_de_Estabelecimento_SES-RJ" , "TODAS_AS_CATEGORIAS__"),
    ( "SNatureza" , "TODAS_AS_CATEGORIAS__"),
    ( "SEsfera" , "TODAS_AS_CATEGORIAS__"),
    ( "SGest%E3o" , "TODAS_AS_CATEGORIAS__"),
    ( "SIdade_%289_faixas%29" , "TODAS_AS_CATEGORIAS__"),
    ( "SIdade_detalhada" , "TODAS_AS_CATEGORIAS__"),
    ( "SCor%2Fra%E7a" , "TODAS_AS_CATEGORIAS__"),
    ( "SEspecialidade_do_leito" , "TODAS_AS_CATEGORIAS__"),
    ( "STipo_de_AIH" , "TODAS_AS_CATEGORIAS__"),
    ( "SIdentifica%E7%E3o_da_AIH" , "TODAS_AS_CATEGORIAS__"),
    ( "SCar%E1ter_do_atendimento" , "TODAS_AS_CATEGORIAS__"),
    ( "STeve_di%E1rias_de_UTI" , "TODAS_AS_CATEGORIAS__"),
    ( "STeve_di%E1rias_de_unid_intermed" , "TODAS_AS_CATEGORIAS__"),
    ( "STeve_di%E1rias_de_acompanhante" , "TODAS_AS_CATEGORIAS__"),
    ( "STipo_de_UTI%2Funidade_intermed" , "TODAS_AS_CATEGORIAS__"),
    ( "SAno_de_interna%E7%E3o" , "TODAS_AS_CATEGORIAS__"),
    ( "SAno_e_m%EAs_de_interna%E7%E3o" , "TODAS_AS_CATEGORIAS__"),
    ( "SAno_de_alta" , "TODAS_AS_CATEGORIAS__"),
    ( "SAno_e_m%EAs_de_alta" , "TODAS_AS_CATEGORIAS__"),
    ( "SMotivo_de_alta%2Fperman%EAncia" , "TODAS_AS_CATEGORIAS__"),
    ( "SMotivo_de_alta%2Fperman_%28detalh%29" , "TODAS_AS_CATEGORIAS__"),
    ( "SGrupo_de_procedimentos" , "TODAS_AS_CATEGORIAS__"),
    ( "SSubgrupo_de_procedimentos" , "TODAS_AS_CATEGORIAS__"),
    ( "SForma_de_organiza%E7%E3o" , "TODAS_AS_CATEGORIAS__"),
    ( "SProcedimento_realizado" , "TODAS_AS_CATEGORIAS__"),
    ( "SFinanciamento" , "TODAS_AS_CATEGORIAS__"),
    ( "SSubtipo_FAEC" , "TODAS_AS_CATEGORIAS__"),
    ( "SRegra_Contratual" , "TODAS_AS_CATEGORIAS__"),
    ( "SComplexidade" , "TODAS_AS_CATEGORIAS__"),
    ( "SDiagn%F3stico_-_grupo" , "TODAS_AS_CATEGORIAS__"),
    ( "SDiagn%F3stico_-_categoria" , "TODAS_AS_CATEGORIAS__"),
    ( "SDiagn%F3stico_-_lista_morbidade" , "TODAS_AS_CATEGORIAS__"),
    ( "SDiagn%F3stico_sens%EDv_at.b%E1sica" , "TODAS_AS_CATEGORIAS__"),
    ( "SCausas_externas_-_grande_grupo" , "TODAS_AS_CATEGORIAS__"),
    ( "SCausas_externas_-_grupo" , "TODAS_AS_CATEGORIAS__"),
    ( "SCausas_externas_-_categoria" , "TODAS_AS_CATEGORIAS__"),
    ( "zeradas" , "exibirlz"),
    ( "formato" , "prn"),
    ( "mostre" , "Mostra")
]

def process_values(v0, increment, region, gender, age18, filename):
    print filename

    values = list(v0)
    values += increment_values[increment]
    values += region_values[region]
    values += gender_values[gender]
    values += age18_values[age18]

    encoded_data = ""
    for value in values[:-1]:
        encoded_data = encoded_data + value[0] + "=" + value[1] + "&"

    encoded_data = encoded_data + values[-1][0] + "=" + values[-1][1]

    req = urllib2.Request(url, encoded_data)

    output_data = None
    while output_data == None:
        #try:
            response = urllib2.urlopen(req)
            the_page = response.read()

            regex = re.compile("<PRE>(.*)</PRE>", re.MULTILINE + re.DOTALL)
            match = re.search(regex, the_page)

            output_data = match.group(1)
            #output_data = HTMLParser.HTMLParser().unescape(output_data)

            csv = ""

            for l in output_data.splitlines():
                line = l.strip()
                if line and line != "&":
                    csv += line + "\n"

            with open(filename, "w") as text_file:
                # TODO: make it better
                csv = re.sub(r'&aacute;', 'a', csv)
                csv = re.sub(r'&eacute;', 'e', csv)
                csv = re.sub(r'&iacute;', 'i', csv)
                csv = re.sub(r'&oacute;', 'o', csv)
                csv = re.sub(r'&uacute;', 'u', csv)
                csv = re.sub(r'&Aacute;', 'A', csv)
                csv = re.sub(r'&Eacute;', 'E', csv)
                csv = re.sub(r'&Iacute;', 'I', csv)
                csv = re.sub(r'&Oacute;', 'O', csv)
                csv = re.sub(r'&Uacute;', 'U', csv)
                csv = re.sub(r'&acirc;', 'a', csv)
                csv = re.sub(r'&atilde;', 'a', csv)
                csv = re.sub(r'&ccedil;', 'c', csv)
                csv = re.sub(r'&ocirc;', 'o', csv)
                csv = re.sub(r'&otilde;', 'o', csv)

                text_file.write(csv)

        #except:
        #    print "error opening url"


values = original_values

for year in sorted(year_values):
    values += year_values[year]

v0 = list(values)

for region in region_values:

    for increment in increment_values:
        process_values(v0, increment, region, "sexo_todos", "idade_todos", "%s_%s.csv" % (region, increment) )

    for increment in ["aih", "acompanhantes", "custo"]:
        for k in gender_values:
            process_values(v0, increment, region, k, "idade_todos", "%s_%s_%s.csv" % (region, increment, k) )

        for k in age18_values:
            process_values(v0, increment, region, "sexo_todos", k, "%s_%s_%s.csv" % (region, increment, k) )

#
#counter = 0
#n = 0
#product = itertools.product (year_values, cap_values, gender_values, age18_values)
#for product_result in product:
#    n = n + 1
#
#product = itertools.product (year_values, cap_values, gender_values, age18_values)
#
#for product_result in product:
#    counter = counter + 1
#    filename = "%s-%s-%s-%s.csv" % ( product_result[0], product_result[1], product_result[2], product_result[3] )
#    if os.path.isfile(filename):
#        #print "skiped: [%d/%d] %s (file already exists) " % ( counter, n, filename )
#        continue
#    print "processing: [%d/%d] %s" % ( counter, n, filename )
#
#    values = original_values
#
#    year_key = product_result[0]
#    cap_key = product_result[1]
#    gender_key = product_result[2]
#    age18_key = product_result[3]
#
#    values += year_values[year_key]
#    values += cap_values[cap_key]
#    values += gender_values[gender_key]
#    values += age18_values[age18_key]
#
#    process_values(values)

