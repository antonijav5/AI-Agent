# meal_planner/models.py
import json
import os
from config.settings import RECIPES_PATH, RECIPE_IMAGES_PATH

class Recipe:
    def __init__(self, id, name, ingredients, instructions, 
                 nutritional_info=None, prep_time=None, 
                 cuisine_type=None, tags=None, meal_type=None, 
                 image_path=None, number=None, difficulty=None,
                 additional_sections=None):
        self.id = id
        self.name = name
        self.number = number  # Broj recepta (kao u PDF-u: 1, 2, 3, 4, 5)
        self.ingredients = ingredients  # Lista sastojaka sa tačnim količinama
        self.instructions = instructions  # Lista koraka pripreme
        
        # Nutritivne vrednosti
        self.nutritional_info = nutritional_info or {}
        
        self.prep_time = prep_time  # Vreme pripreme - opciono
        self.cuisine_type = cuisine_type  # Tip kuhinje - opciono
        self.tags = tags or []  # Tagovi/kategorije
        
        # Tip obroka (doručak, ručak, večera, užina)
        self.meal_type = meal_type
        
        # Putanja do slike
        self.image_path = image_path
        
        # Težina pripreme (jednostavno, srednje, kompleksno)
        self.difficulty = difficulty
        
        # Dodatne sekcije (npr. SOS, FIL ZA PALAČINKE)
        self.additional_sections = additional_sections or {}
        
    def to_dict(self):
        """Konvertuje recept u rečnik za serijalizaciju."""
        return {
            "id": self.id,
            "name": self.name,
            "number": self.number,
            "ingredients": self.ingredients,
            "instructions": self.instructions,
            "nutritional_info": self.nutritional_info,
            "prep_time": self.prep_time,
            "cuisine_type": self.cuisine_type,
            "tags": self.tags,
            "meal_type": self.meal_type,
            "image_path": self.image_path,
            "difficulty": self.difficulty,
            "additional_sections": self.additional_sections
        }
        
    @staticmethod
    def from_pdf_format(recipe_data):
        """Kreira Recipe objekat iz formata koji odgovara PDF-u."""
        # Parsiranje nutritivnih vrednosti iz formata "KCAL;P,UH,M"
        nutritional_info = {}
        if "nutritional_text" in recipe_data:
            try:
                nutri_text = recipe_data["nutritional_text"]
                calories_part, macros_part = nutri_text.split(';')
                
                # Izdvajanje kalorija
                calories = int(calories_part.replace("KCAL", "").strip())
                
                # Izdvajanje makronutrijenata
                macros = macros_part.strip().split(',')
                proteins = float(macros[0].replace("P", "").strip())
                carbs = float(macros[1].replace("UH", "").strip())
                fats = float(macros[2].replace("M", "").strip())
                
                nutritional_info = {
                    "calories": calories,
                    "proteins": proteins,
                    "carbs": carbs,
                    "fats": fats
                }
            except Exception as e:
                print(f"Greška pri parsiranju nutritivnih vrednosti: {e}")
        
        # Kreiranje recepta
        return Recipe(
            id=recipe_data.get("id"),
            name=recipe_data.get("name"),
            number=recipe_data.get("number"),
            ingredients=recipe_data.get("ingredients", []),
            instructions=recipe_data.get("instructions", []),
            nutritional_info=nutritional_info,
            meal_type=recipe_data.get("meal_type"),
            image_path=recipe_data.get("image_path"),
            tags=recipe_data.get("tags", []),
            additional_sections=recipe_data.get("additional_sections")
        )
        
class RecipeDatabase:
    def __init__(self, recipes_path=RECIPES_PATH):
        self.recipes_path = recipes_path
        self.recipes = []
        self._load_recipes()
        
    def _load_recipes(self):
        """Učitava recepte iz fajla ili inicijalizuje sa PDF receptima ako fajl ne postoji."""
        if not os.path.exists(self.recipes_path):
            print(f"Fajl sa receptima nije pronađen na: {self.recipes_path}")
            
            # Kreiraj direktorijum ako ne postoji
            os.makedirs(os.path.dirname(self.recipes_path), exist_ok=True)
            
            # Inicijalizuj sa receptima iz PDF-a
            from meal_planner.pdf_recipes import create_sample_recipes_from_pdf
            self.recipes = create_sample_recipes_from_pdf()
            
            # Sačuvaj recepte u JSON fajl
            self._save_recipes()
            return
            
        try:
            with open(self.recipes_path, 'r', encoding='utf-8') as f:
                recipes_data = json.load(f)
                
            self.recipes = []
            for recipe_data in recipes_data:
                recipe = Recipe(
                    id=recipe_data.get("id"),
                    name=recipe_data.get("name"),
                    number=recipe_data.get("number"),
                    ingredients=recipe_data.get("ingredients", []),
                    instructions=recipe_data.get("instructions", []),
                    nutritional_info=recipe_data.get("nutritional_info", {}),
                    prep_time=recipe_data.get("prep_time"),
                    cuisine_type=recipe_data.get("cuisine_type", ""),
                    tags=recipe_data.get("tags", []),
                    meal_type=recipe_data.get("meal_type"),
                    image_path=recipe_data.get("image_path"),
                    difficulty=recipe_data.get("difficulty"),
                    additional_sections=recipe_data.get("additional_sections")
                )
                self.recipes.append(recipe)
        except Exception as e:
            print(f"Greška pri učitavanju recepata: {str(e)}")
            self.recipes = []
            
    def get_all_recipes(self):
        """Vraća sve recepte."""
        return self.recipes
        
    def get_recipe_by_id(self, recipe_id):
        """Vraća recept po ID-u."""
        for recipe in self.recipes:
            if recipe.id == recipe_id:
                return recipe
        return None
        
    def add_recipe(self, recipe):
        """Dodaje novi recept u bazu."""
        # Proveri da li ID već postoji
        if self.get_recipe_by_id(recipe.id):
            raise ValueError(f"Recept sa ID {recipe.id} već postoji")
            
        self.recipes.append(recipe)
        self._save_recipes()
        
    def update_recipe(self, recipe):
        """Ažurira postojeći recept."""
        for i, existing_recipe in enumerate(self.recipes):
            if existing_recipe.id == recipe.id:
                self.recipes[i] = recipe
                self._save_recipes()
                return True
        return False
        
    def delete_recipe(self, recipe_id):
        """Briše recept iz baze."""
        for i, recipe in enumerate(self.recipes):
            if recipe.id == recipe_id:
                del self.recipes[i]
                self._save_recipes()
                return True
        return False
        
    def _save_recipes(self):
        """Čuva recepte u fajl."""
        recipes_data = [recipe.to_dict() for recipe in self.recipes]
        with open(self.recipes_path, 'w', encoding='utf-8') as f:
            json.dump(recipes_data, f, ensure_ascii=False, indent=2)
            
class UserPreferences:
    def __init__(self, user_id):
        self.user_id = user_id
        self.dietary_restrictions = []  # Npr. "vegetarijanac", "bez glutena"
        self.favorite_cuisines = []  # Npr. ["italijanska", "meksička"]
        self.disliked_ingredients = []  # Sastojci koje korisnik ne voli
        self.meal_history = []  # Prethodno planirani obroci
        self.favorite_recipes = []  # ID-jevi omiljenih recepata
        
    def update_preferences(self, field, values):
        """Ažurira korisničke preferencije."""
        if hasattr(self, field):
            setattr(self, field, values)
            return True
        return False
        
    def add_to_meal_history(self, meal):
        """Dodaje obrok u istoriju."""
        self.meal_history.append(meal)
        # Ograniči veličinu istorije
        if len(self.meal_history) > 50:
            self.meal_history = self.meal_history[-50:]