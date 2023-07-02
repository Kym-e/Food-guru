# imports
import cv2
from pyzbar.pyzbar import decode
import requests
import json

# constants

# variables

# Open Camera, take photo and save photo
cv2.namedWindow("preview")
vc = cv2.VideoCapture(0)

if vc.isOpened(): # try to get the first frame
    rval, frame = vc.read()
else:
    rval = False

while rval:
    cv2.imshow("preview", frame)
    rval, frame = vc.read()
    key = cv2.waitKey(20)
    if key == 27: # exit on ESC
        cv2.imwrite("barcode_image.jpg", frame)
        break

vc.release()
cv2.destroyWindow("preview")

# Read Barcode
# Make one method to decode the barcode
def BarcodeReader(image):
    # read the image in numpy array using cv2
    img = cv2.imread(image)

    # Decode the barcode image

    detectedBarcodes = decode(img)

    # If not detected then print the message
    if not detectedBarcodes:
        print("Barcode Not Detected or your barcode is blank/corrupted!")
    else:

        # Traverse through all the detected barcodes in image
        for barcode in detectedBarcodes:

            # Locate the barcode position in image
            (x, y, w, h) = barcode.rect

            # Put the rectangle in image using
            # cv2 to highlight the barcode
            cv2.rectangle(img, (x - 10, y - 10),
                          (x + w + 10, y + h + 10),
                          (255, 0, 0), 2)

            if barcode.data != "":
                # Print the barcode data
                print(barcode.data)
                print(barcode.type)

    # Display the image
    cv2.imshow("Image", img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    return barcode.data

image = "barcode_image.jpg"
# BarcodeReader(image)

# Print Details
# Base URI
URI = "https://world.openfoodfacts.org/api/v2/product/"

# Barcode
Barcode = BarcodeReader(image)

# Combine URI and Barcode to get product information from API
api_url = URI + str(Barcode)

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
