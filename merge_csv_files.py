#!/usr/bin/python
import sys
import pandas as pd

columns_variables_to_filter = {
    "aih",
    "acompanhantes",
    "custo"
}

column_variables = {
    "aih",
    "acompanhantes",
    "custo",
    "obitos",
    "permanencia"
}

regions = {
    "baia_da_ilha_grande", "baixada_litoranea", "centro-sul",
    "medio_paraiba", "metropolitana_I", "metropolitana_II",
    "noroeste", "norte", "serrana", "RJ"
}

filters = {
    "idade" : [ "60a69", "70a79", "80+", "todos" ],
    "sexo" : [ "masculino", "feminino", "todos" ]
}

for region in regions:
    for var in columns_variables_to_filter:
        for filter in filters:

            result = None
            for k in filters[filter]:
                table = pd.read_csv("%s_%s_%s_%s.csv" % (region, var, filter, k), sep=";")
                t = list(table.columns)
                for i in range (1, len(t)):
                    t[i] = "%s %s %s" % (var, table.columns[i], k)
                table.columns = t
                if not result:
                    result = table
                else:
                    result = result.merge(table, on='Diagnostico - capitulo')

            result = result.sort(axis=1)
            result.to_csv("%s_%s_por_%s.csv" % (region, var, filter), index=False, sep=";")

    # -----------

    all_result = None

    for var in column_variables:

        table = pd.read_csv("%s_%s.csv" % (region, var), sep=";")
        t = list(table.columns)
        for i in range (1, len(t)):
            t[i] = "%s %s" % (table.columns[i], var)
        table.columns = t
        if not all_result:
            all_result = table
        else:
            all_result = all_result.merge(table, on="Diagnostico - capitulo")

    all_result = all_result.sort(axis=1)
    all_result.to_csv("%s_aihs_demora_custo_obitos_acompanhante.csv" % region, index=False, sep=";")

