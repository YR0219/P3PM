#!/usr/bin/env python
# coding: utf-8

# In[ ]:


from flask import Flask, render_template, request
import pandas as pd

app = Flask(__name__)

data = pd.read_csv(r'./base_nutri.csv', sep=';', decimal='.', low_memory=False)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        code = request.form['code']
        result, alternative_product = search_code(code)
        return render_template('index.html', result=result, alternative_product=alternative_product)
    return render_template('index.html')

def search_code(code):
    result = data.loc[data['code'] == code]

    if len(result) == 0:
        return {"not_found": True}, None

    product_info = {}
    alternative_product = None
    for index, row in result.iterrows():
        product_info = {
            "code": row['code'],
            "product_name": row['product_name'],
            "main_category_fr": row['main_category_fr'],
            "energy_100g": row['energy_100g'],
            "fat_100g": row['fat_100g'],
            "saturated_fat_100g": row['saturated_fat_100g'],
            "carbohydrates_100g": row['carbohydrates_100g'],
            "sugars_100g": row['sugars_100g'],
            "proteins_100g": row['proteins_100g'],
            "light_group": row['light_group']
        }

        if row['light_group'] != "Oui":
            same_category_light_products = data.loc[(data['main_category_fr'] == row['main_category_fr']) & (data['light_group'] == "Oui")]

            if not same_category_light_products.empty:
                alternative_product = same_category_light_products.sample(n=1)
            else:
                same_category_medium_products = data.loc[(data['main_category_fr'] == row['main_category_fr']) & (data['light_group'] == "Moyen")]

                if not same_category_medium_products.empty:
                    alternative_product = same_category_medium_products.sample(n=1)

    alternative_product = None if alternative_product is None or alternative_product.empty else alternative_product
    return product_info, alternative_product

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))



