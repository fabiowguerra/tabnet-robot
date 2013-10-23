#!/usr/bin/python
import sys
import pandas as pd

columns_variables_to_filter = {
    "aih",
    "media_acompanhantes",
    "dias_acompanhantes",
    "custo"
}

column_variables = {
    "aih",
    "media_acompanhantes",
    "dias_acompanhantes",
    "custo",
    "obitos",
    "media_permanencia",
    "dias_permanencia"
}

#regions = {
#    "baia_da_ilha_grande", "baixada_litoranea", "centro-sul",
#    "medio_paraiba", "metropolitana_I", "metropolitana_II",
#    "noroeste", "norte", "serrana", "RJ"
#}
regions = {
    "Angra dos Reis", "Aperibé", "Araruama", "Areal", "Armação dos Búzios", "Arraial do Cabo",
    "Barra do Piraí", "Barra Mansa", "Belford Roxo", "Bom Jardim", "Bom Jesus do Itabapoana",
    "Cabo Frio", "Cachoeiras de Macacu", "Cambuci", "Campos dos Goytacazes", "Cantagalo",
    "Carapebus", "Cardoso Moreira", "Carmo", "Casimiro de Abreu", "Comendador Levy Gasparian",
    "Conceição de Macabu", "Cordeiro", "Duas Barras", "Duque de Caxias",
    "Engenheiro Paulo de Frontin", "Guapimirim", "Iguaba Grande", "Itaboraí", "Itaguaí",
    "Italva", "Itaocara", "Itaperuna", "Itatiaia", "Japeri", "Laje do Muriaé", "Macaé",
    "Macuco", "Magé", "Mangaratiba", "Maricá", "Mendes", "Mesquita", "Miguel Pereira",
    "Miracema", "Natividade", "Nilópolis", "Niterói", "Nova Friburgo", "Nova Iguaçu",
    "Paracambi", "Paraíba do Sul", "Paraty", "Paty do Alferes", "Petrópolis", "Pinheiral",
    "Piraí", "Porciúncula", "Porto Real", "Quatis", "Queimados", "Quissamã", "Resende",
    "Rio Bonito", "Rio Claro", "Rio das Flores", "Rio das Ostras", "Rio de Janeiro",
    "Santa Maria Madalena", "Santo Antônio de Pádua", "São Fidélis",
    "São Francisco de Itabapoana", "São Gonçalo", "São João da Barra", "São João de Meriti",
    "São José de Ubá", "São José do Vale do Rio Preto", "São Pedro da Aldeia",
    "São Sebastião do Alto", "Sapucaia", "Saquarema", "Seropédica", "Silva Jardim",
    "Sumidouro", "Tanguá", "Teresópolis", "Trajano de Moraes", "Três Rios", "Valença",
    "Varre-Sai", "Vassouras", "Volta Redonda", "Município ignorado/não preenchido", "RJ"
}

filters = {
    "idade" : [ "60a69", "70a79", "80+", "todos" ],
    "cor" : [ "branca", "preta", "parda", "amarela", "indigena", "ignorado", "todas" ],
    "sexo" : [ "masculino", "feminino", "todos" ]
}

for row_type in ["sab", "cap"]:
	if row_type == "cap":
		pivot = 'Diagnostico - capitulo'
	else:
		pivot = 'Diagnostico sensiv at.basica 1'

	for region in regions:
		for var in columns_variables_to_filter:
			for filter in filters:

				result = None
				for k in filters[filter]:
					print "%s_%s_%s_%s_%s.csv" % (row_type, region, var, filter, k)
					table = pd.read_csv("%s_%s_%s_%s_%s.csv" % (row_type, region, var, filter, k), sep=";")
					t = list(table.columns)
					for i in range (1, len(t)):
						t[i] = "%s %s %s" % (var, table.columns[i], k)
					table.columns = t
					if not result:
						result = table
					else:
						result = result.merge(table, on=pivot)

				result = result.sort(axis=1)
				result.to_csv("%s_%s_%s_por_%s.csv" % (row_type, region, var, filter), index=False, sep=";")

		# -----------

		all_result = None

		for var in column_variables:

			table = pd.read_csv("%s_%s_%s.csv" % (row_type, region, var), sep=";")
			t = list(table.columns)
			for i in range (1, len(t)):
				t[i] = "%s %s" % (table.columns[i], var)
			table.columns = t
			if not all_result:
				all_result = table
			else:
				all_result = all_result.merge(table, on=pivot)

		all_result = all_result.sort(axis=1)
		all_result.to_csv("%s_%s_aihs_demora_custo_obitos_acompanhante.csv" % (row_type, region), index=False, sep=";")

