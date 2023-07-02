import requests
import json


# Base URI
URI = "https://world.openfoodfacts.org/api/v2/product/"

# Barcode
Barcode = "5060225570301"
Barcode = "51000005"
Barcode = "5000177449638"
# Barcode = "9120077855271"

# Combine URI and Barcode to get product information from API
api_url = URI + Barcode

# Make API request
api_request = requests.get(api_url)

# Parse JSON to Python
json_result = json.loads(api_request.text)
# pprint.pprint(json_result)

product = json_result["product"]

# Product name

brand_present = False
try:
    brand = product['brands']
    brand_present = True
except:
    pass


product_name = product['product_name']

if brand_present:
    print(f"{brand} {product_name}\n")
else:
    print(product_name)

# Allergens
allergens = product["allergens"]
print(f"Allergens: {allergens}\n")

contains = product["allergens_from_ingredients"]
print(f"Contains: {contains}\n")

# Nutritional Information
nutriments_dictionary = product["nutriments"]

nutritional_info_list = [
    "energy",
    "energy-kcal",
    "fat",
    "saturated-fat",
    "carbohydrates",
    "sugars",
    "proteins",
    "salt"
]
print("Nutritional Information per 100g")
for items in nutriments_dictionary:
    if items in nutritional_info_list:
        # print("Y")
        if items == "energy":
            print(f"{items}: {nutriments_dictionary[items]} kJ")
        elif items == "energy-kcal":
            print(f"{items}: {nutriments_dictionary[items]} kcal")
        else:
            print(f"{items}: {nutriments_dictionary[items]} g")

print("\nFront of packaging labels:")
for items in product["nutrient_levels"]:
    print(f'{items} :' + product["nutrient_levels"][items])


print("\nIngredients:")
print(product["ingredients_text"])

print("\nMore Information:")
for tag in product["ingredients_analysis_tags"]:
    print(tag.split(":")[1])

if product['nova_group'] == 4:
    print(f"Nova group rating: {product['nova_group']} Ultra-processed food "
          f"and drink products")
elif product['nova_group'] == 3:
    print(f"Nova group rating: {product['nova_group']} Processed foods")
elif product['nova_group'] == 2:
    print(f"Nova group rating: {product['nova_group']} Processed culinary "
          f"ingredients")
elif product['nova_group'] == 1:
    print(f"Nova group rating: {product['nova_group']} Unprocessed or "
          f"minimally processed foods")
else:
    print("Unknown")


# pprint.pprint(product["ecoscore_data"])




