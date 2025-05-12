# meal_planner/pdf_recipes.py
import os
from config.settings import RECIPE_IMAGES_PATH

def create_sample_recipes_from_pdf():
    """
    Kreira recepte na osnovu podataka iz PDF-a.
    """
    # Osiguraj da folder za slike postoji
    os.makedirs(RECIPE_IMAGES_PATH, exist_ok=True)
    
    recipes = []
    
    # Recept 1: AVOKADO-TUNA TOST
    avocado_toast = {
        "id": 1,
        "number": 1,
        "name": "AVOKADO-TUNA TOST",
        "nutritional_text": "366KCAL;23P,28UH,18M",
        "ingredients": [
            "1 integralni tost (45-50g)",
            "50g avokada",
            "55g tunjevine u salamuri",
            "10g miksa semenki"
        ],
        "instructions": [
            "Na integralni tost izgnjeckate avokado i na njega stavite par kapi limunovog soka.",
            "Zatim, na vrh dodati tunjevinu i semenke po vašoj želji."
        ],
        "meal_type": "doručak/užina/večera", 
        "tags": ["brzo", "jednostavno", "proteini"],
        "image_path": os.path.join(RECIPE_IMAGES_PATH, "avokado_tuna_tost.jpg")
    }
    
    # Recept 2: PUNJENA PILETINA
    stuffed_chicken = {
        "id": 2,
        "number": 2,
        "name": "PUNJENA PILETINA",
        "nutritional_text": "429KCAL;64P,5UH,17M",
        "ingredients": [
            "200g piletine",
            "10g žutog sira",
            "10g suve pečenice",
            "1 kašičica ulja",
            "1 šaka rukole",
            "4 čeri paradajza"
        ],
        "instructions": [
            "Pileće grudi preseći na sredini i napraviti 'džep' u kome ćete staviti pečenicu i žuti sir.",
            "Piletinu začiniti začinima koje volite i zatvoriti džep uz pomoć dve čačkalice.",
            "Staviti piletinu na tiganj da se peče 10-15 minuta na par kapi ulja.",
            "Nakon toga piletinu staviti na pek papir, u rernu, na 10-ak minuta i 180 stepeni.",
            "Napraviti sos od niskomasnog sira i žutog sira u tiganju.",
            "Preko piletine staviti sos, a pored dodati povrće po želji."
        ],
        "meal_type": "ručak/večera", 
        "tags": ["proteini", "meso", "piletina"],
        "image_path": os.path.join(RECIPE_IMAGES_PATH, "punjena_piletina.jpg"),
        "additional_sections": {
            "SOS": [
                "60g niskomasnog namaza",
                "20g žutog sira"
            ]
        }
    }
    
    # Recept 3: SLANE PALAČINKE
    savory_pancakes = {
        "id": 3,
        "number": 3,
        "name": "SLANE PALAČINKE",
        "nutritional_text": "504KCAL;42P,28UH,25M",
        "ingredients": [
            "3 jajeta",
            "30g pirinčanog brašna",
            "35g skyr jogurta",
            "4g masti/ulja za prženje"
        ],
        "instructions": [
            "Promešati jaja, brašno i skyr jogurt i posoliti smesu.",
            "Dobro zagrijati tiganj, premazati sa 2-3 kapi ulja/masti i praviti palačinke.",
            "Kada budu gotove, namazati ih niskomasnim namazom.",
            "Dodati iscepkanu pršutu i rukolu ili drugo povrće po želji."
        ],
        "meal_type": "doručak/ručak", 
        "tags": ["proteini", "brzo"],
        "image_path": os.path.join(RECIPE_IMAGES_PATH, "slane_palacinke.jpg"),
        "additional_sections": {
            "FIL ZA PALAČINKE": [
                "80g niskomasnog namaza",
                "2 lista pršute",
                "1 šaka rukole"
            ]
        }
    }
    
    # Recept 4: OVSENI MUG CAKE
    oat_mug_cake = {
        "id": 4,
        "number": 4,
        "name": "OVSENI MUG CAKE",
        "nutritional_text": "401KCAL;32P,31UH,15.5M",
        "ingredients": [
            "35g ovsenog brašna",
            "1 jaje",
            "15g whey proteina",
            "70g niskomasnog namaza",
            "1 kašičica zaslađivača",
            "1/3 kašičice praška za pecivo",
            "12g crne čokolade, 75%+ kakaa"
        ],
        "instructions": [
            "Promešati sve sastojke.", 
            "Staviti u posudu koja ide u rernu.",
            "Peći 20-ak minuta na 200 stepeni ili 10-ak minuta u prethodno zagrejanoj rerni."
        ],
        "meal_type": "desert/užina", 
        "tags": ["slatko", "proteini", "desert"],
        "image_path": os.path.join(RECIPE_IMAGES_PATH, "ovseni_mug_cake.jpg")
    }
    
    # Recept 5: PILEĆI BURITO
    chicken_burrito = {
        "id": 5,
        "number": 5,
        "name": "PILEĆI BURITO",
        "nutritional_text": "584KCAL;62P,43UH,17M",
        "ingredients": [
            "170g piletine",
            "1 tortilja (60g)",
            "60g niskomasnog namaza",
            "20g žutog sira",
            "20g kukuruza",
            "40g crvenog pasulja iz konzerve",
            "10g suve pečenice"
        ],
        "instructions": [
            "Iseckati pileći file na komadiće i začiniti ga po želji.",
            "Iseckano meso staviti na tiganj, na 2-3 kapi ulja/masti dok ne poprimi boju.",
            "Dodati niskomasni namaz i žuti sir u tiganj i mešati zajedno 1-2 minuta dok se ne dobije kremasta smesa.",
            "Prethodno staviti tortilju u tiganj na minut sa jedne strane i 30 sekundi sa druge da dobije boju.",
            "Staviti meso u tortilju, dodati crveni pasulj, kukuruz i malo suve pečenice.",
            "Zatvoriti burito i uživati!"
        ],
        "meal_type": "ručak/večera", 
        "tags": ["proteini", "meso", "piletina"],
        "image_path": os.path.join(RECIPE_IMAGES_PATH, "pileci_burito.jpg")
    }
    
    # Kreiranje objekata Recipe iz podataka
    from meal_planner.models import Recipe
    
    recipes.append(Recipe.from_pdf_format(avocado_toast))
    recipes.append(Recipe.from_pdf_format(stuffed_chicken))
    recipes.append(Recipe.from_pdf_format(savory_pancakes))
    recipes.append(Recipe.from_pdf_format(oat_mug_cake))
    recipes.append(Recipe.from_pdf_format(chicken_burrito))
    
    return recipes