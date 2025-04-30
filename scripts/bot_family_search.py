import pandas as pd
import requests
import time


# Metadata
data = pd.read_csv('/Users/saldanhaluizleonardo/Library/Mobile Documents/com~apple~CloudDocs/INDIGENOMICS/Pilot/Metabolomics_analysis/tima_output/pilot_metadata 2.csv')

# === 2) Adicionar coluna 'family' pelo POWO ===

# Extrai gênero
data["genus"] = data["ATTRIBUTE_species"].str.split().str[0]
unique_genera = data["genus"].dropna().unique()

# Função para buscar família
def get_family_from_powo(genus):
    try:
        url = f"https://powo.science.kew.org/api/2/search?q={genus}&perPage=1"
        resp = requests.get(url)
        if resp.status_code == 200:
            data = resp.json()
            if data["results"]:
                return data["results"][0].get("family")
    except:
        return None
    return None

# Monta dicionário e DataFrame
genus_family_mapping = {}
for g in unique_genera:
    genus_family_mapping[g] = get_family_from_powo(g)
    time.sleep(1)  # respeito ao servidor
genus_family_df = (
    pd.DataFrame.from_dict(genus_family_mapping, orient="index", columns=["family"])
      .reset_index()
      .rename(columns={"index": "genus"})
)

# Merge na metadata
data = data.merge(genus_family_df, on="genus", how="left")

# Salva de volta (opcional)
data.to_csv(
    "/Users/.../",
    index=False
)