# assistant/main.py
import json
import os
from datetime import datetime, date
from config.settings import USER_PROFILE_PATH
from core.intent_processor import IntentProcessor
from meal_planner.service import MealPlannerService
from meal_planner.models import RecipeDatabase, UserPreferences
from message_assistant.service import MessageAssistantService

class PersonalAssistant:
    def __init__(self):
        # Učitaj ili kreiraj korisnički profil
        self.user_profile = self._load_user_profile()
        
        # Inicijalizuj servise
        self.recipe_db = RecipeDatabase()
        self.user_preferences = UserPreferences(self.user_profile["id"])
        
        self.meal_planner = MealPlannerService(self.recipe_db, self.user_preferences)
        self.message_assistant = MessageAssistantService(self.user_profile)
        
        # Centralni procesor zahteva
        self.intent_processor = IntentProcessor(
            self.meal_planner,
            self.message_assistant
        )
        
    def process_command(self, text):
        """Obrađuje komandu korisnika i vraća odgovor."""
        # Logiraj zahtev
        self._log_interaction("user", text)
        
        # Procesiraj zahtev
        response_data = self.intent_processor.process_request(text)
        
        # Formatiraj odgovor
        formatted_response = self._format_response(response_data)
        
        # Logiraj odgovor
        self._log_interaction("assistant", formatted_response)
        
        return formatted_response
        
    def _load_user_profile(self):
        """Učitava korisnički profil iz fajla ili kreira novi ako ne postoji."""
        if os.path.exists(USER_PROFILE_PATH):
            try:
                with open(USER_PROFILE_PATH, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except json.JSONDecodeError:
                print("Greška pri čitanju korisničkog profila. Kreiranje novog.")
        
        # Kreiraj novi profil ako ne postoji ili je oštećen
        default_profile = {
            "id": "user1",
            "name": "Korisnik",
            "communication_style": "casual",
            "created_at": datetime.now().isoformat(),
            "preferences": {}
        }
        
        # Sačuvaj default profil
        os.makedirs(os.path.dirname(USER_PROFILE_PATH), exist_ok=True)
        with open(USER_PROFILE_PATH, 'w', encoding='utf-8') as f:
            json.dump(default_profile, f, ensure_ascii=False, indent=2)
            
        return default_profile
        
    def _format_recipe(self, recipe_dict):
        """Formatira recept za prikaz korisniku."""
        name = recipe_dict.get("name", "Nepoznato jelo")
        nutritional_info = recipe_dict.get("nutritional_info", {})
        
        # Sastavi nutritivne informacije
        nutrition_str = ""
        if nutritional_info:
            calories = nutritional_info.get("calories", "?")
            proteins = nutritional_info.get("proteins", "?")
            carbs = nutritional_info.get("carbs", "?")
            fats = nutritional_info.get("fats", "?")
            nutrition_str = f"{calories}KCAL; {proteins}P, {carbs}UH, {fats}M"
        
        # Sastavi sastojke
        ingredients = recipe_dict.get("ingredients", [])
        ingredients_str = "\n".join([f"• {ingredient}" for ingredient in ingredients])
        
        # Sastavi uputstva
        instructions = recipe_dict.get("instructions", [])
        instructions_str = "\n".join([f"{i+1}. {instruction}" for i, instruction in enumerate(instructions)])
        
        # Dodatne sekcije (npr. SOS, FIL)
        additional_sections_str = ""
        additional_sections = recipe_dict.get("additional_sections", {})
        for section_name, section_items in additional_sections.items():
            additional_sections_str += f"\n\n{section_name}:\n"
            additional_sections_str += "\n".join([f"• {item}" for item in section_items])
        
        # Formatiran recept
        formatted = f"""
{name}
{'=' * len(name)}
{nutrition_str}

SASTOJCI:
{ingredients_str}

PRIPREMA:
{instructions_str}
{additional_sections_str}
"""
        return formatted
        
    def _format_response(self, response_data):
        """Formatira odgovor za prikaz korisniku."""
        response_type = response_data.get("response_type", "general")
        
        if response_type == "general":
            return response_data.get("message", "Izvinite, došlo je do greške.")
            
        elif response_type == "meal_plan_daily":
            plan = response_data.get("plan", {})
            date_obj = plan.get("date", "danas")
            meals = plan.get("meals", {})
        
            if isinstance(date_obj, (date, datetime)):
              date_str = date_obj.strftime("%d.%m.%Y")
            else:
              date_str = str(date_obj)
            
            response = f"Evo predloga za {date_str}:\n"
            
            if not meals:
                return response + "Nema dostupnih predloga za taj dan."
                
            for meal_type, meal_info in meals.items():
                if meal_info:
                    response += f"\n===== {meal_type.upper()} =====\n"
                    response += self._format_recipe(meal_info)
                else:
                    response += f"\n{meal_type.capitalize()}: Nema predloga."
                    
            return response
            
        elif response_type == "meal_plan_weekly":
            weekly_plan = response_data.get("plan", {})
            
            if not weekly_plan:
                return "Nema dostupnih predloga za nedelju."
                
            response = "Nedeljni plan obroka:\n\n"
            
            for date_str, daily_plan in weekly_plan.items():
                date_obj = datetime.strptime(date_str, "%Y-%m-%d").date()
                day_name = ["Ponedeljak", "Utorak", "Sreda", "Četvrtak", "Petak", "Subota", "Nedelja"][date_obj.weekday()]
                response += f"--- {day_name} ({date_obj.strftime('%d.%m.%Y')}) ---\n"
                
                meals = daily_plan.get("meals", {})
                for meal_type, meal_info in meals.items():
                    if meal_info:
                        response += f"{meal_type.capitalize()}: {meal_info.get('name', 'Nepoznato jelo')}\n"
                    else:
                        response += f"{meal_type.capitalize()}: Nema predloga\n"
                        
                response += "\n"
                
            response += "Za detalje o receptu, pitajte za konkretan dan i obrok."
            return response
            
        elif response_type == "message_draft":
            draft = response_data.get("draft", {})
            return f"Predlog odgovora za {draft.get('sender', 'primaoca')}:\n\n{draft.get('draft_response', '')}"
            
        # Ostali tipovi odgovora...
            
        return "Izvinite, ne razumem vaš zahtev."
        
    def _log_interaction(self, sender, message):
        """Logira interakciju između korisnika i asistenta."""
        # Jednostavna implementacija logiranja na konzolu
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"[LOG] [{timestamp}] {sender}: {message}")
        
        # Ovde bi išla implementacija za čuvanje u fajl/bazu