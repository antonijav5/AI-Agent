# meal_planner/service.py - ispravljena verzija
import random
from datetime import datetime, timedelta, date

class MealPlannerService:
    def __init__(self, recipe_db, user_preferences):
        self.recipe_db = recipe_db
        self.user_preferences = user_preferences
        
    def generate_daily_plan(self, date_obj, meal_types=None):
        """Generiše plan obroka za jedan dan."""
        default_meal_types = ["doručak", "ručak", "večera"]
        meal_types = meal_types or default_meal_types
        
        # Provera da li je date_obj tipa datetime.date i konverzija ako nije
        if isinstance(date_obj, str):
            try:
                date_obj = datetime.strptime(date_obj, "%Y-%m-%d").date()
            except ValueError:
                date_obj = datetime.now().date()
        elif not isinstance(date_obj, (datetime, date)):
            date_obj = datetime.now().date()
            
        # Ako je datetime, konvertuj u date
        if isinstance(date_obj, datetime):
            date_obj = date_obj.date()
            
        daily_plan = {
            "date": date_obj,
            "meals": {}
        }
        
        for meal_type in meal_types:
            suitable_recipes = self._find_suitable_recipes(meal_type)
            
            if not suitable_recipes:
                daily_plan["meals"][meal_type] = None
                continue
                
            # Odaberi recepte koji odgovaraju korisničkim preferencijama
            recommended = self._rank_recipes(suitable_recipes)
            
            if recommended:
                # Konvertujemo Recipe objekat u rečnik za lakše rukovanje
                daily_plan["meals"][meal_type] = recommended[0].to_dict()
            else:
                daily_plan["meals"][meal_type] = None
                
        return daily_plan
        
    def generate_weekly_plan(self, start_date):
        """Generiše plan obroka za nedelju dana."""
        # Provera i konverzija start_date
        if isinstance(start_date, str):
            try:
                start_date = datetime.strptime(start_date, "%Y-%m-%d").date()
            except ValueError:
                start_date = datetime.now().date()
        elif not isinstance(start_date, (datetime, date)):
            start_date = datetime.now().date()
            
        # Ako je datetime, konvertuj u date
        if isinstance(start_date, datetime):
            start_date = start_date.date()
            
        weekly_plan = {}
        current_date = start_date
        
        for _ in range(7):  # 7 dana
            daily_plan = self.generate_daily_plan(current_date)
            weekly_plan[current_date.strftime("%Y-%m-%d")] = daily_plan
            current_date += timedelta(days=1)
            
        return weekly_plan
        
    # Ostatak metoda ostaje isti
    def _find_suitable_recipes(self, meal_type=None):
        """Pronalazi recepte koji odgovaraju tipu obroka i dijetalnim ograničenjima."""
        suitable = []
        all_recipes = self.recipe_db.get_all_recipes()
        
        # Ako nema recepata, vrati praznu listu
        if not all_recipes:
            return suitable
            
        for recipe in all_recipes:
            # Ako je naveden tip obroka, filtriraj po tome
            if meal_type and recipe.meal_type:
                # Proveri da li navedeni tip obroka postoji u listi tipova za recept
                if meal_type.lower() not in recipe.meal_type.lower():
                    continue
                    
            # Proveri da li recept odgovara dijetalnim ograničenjima
            if not self._matches_dietary_restrictions(recipe):
                continue
                
            # Proveri da li sadrži sastojke koje korisnik ne voli
            if self._contains_disliked_ingredients(recipe):
                continue
                
            suitable.append(recipe)
            
        # Ako nakon filtriranja nema pogodnih recepata, vrati nekoliko nasumičnih
        if not suitable and all_recipes:
            suitable = random.sample(all_recipes, min(3, len(all_recipes)))
            
        return suitable
        
    def _matches_dietary_restrictions(self, recipe):
        """Proverava da li recept odgovara dijetalnim ograničenjima korisnika."""
        # Za sada jednostavna implementacija
        if not self.user_preferences.dietary_restrictions:
            return True  # Ako nema ograničenja, svi recepti odgovaraju
            
        # U pravoj implementaciji bismo proveravali sastojke i tagove recepta
        # prema korisničkim ograničenjima
        
        return True  # Za sada uvek vraćamo True
        
    def _contains_disliked_ingredients(self, recipe):
        """Proverava da li recept sadrži sastojke koje korisnik ne voli."""
        if not self.user_preferences.disliked_ingredients:
            return False  # Ako nema nevoljenih sastojaka, nijedan recept ne sadrži
            
        for ingredient in recipe.ingredients:
            # Proveri da li bilo koji od nevoljenih sastojaka postoji u tekstu sastojka
            for disliked in self.user_preferences.disliked_ingredients:
                if disliked.lower() in ingredient.lower():
                    return True
                    
        return False
        
    def _rank_recipes(self, recipes):
        """Rangira recepte na osnovu korisničkih preferencija."""
        ranked = []
        for recipe in recipes:
            score = 0
            
            # Povećaj skor ako je kuhinja među omiljenim
            if recipe.cuisine_type in self.user_preferences.favorite_cuisines:
                score += 2
                
            # Povećaj skor ako je među omiljenim receptima
            if recipe.id in self.user_preferences.favorite_recipes:
                score += 3
                
            # Smanji skor ako je nedavno korišćen
            # (Trebalo bi da imamo meal_history kao listu objekata sa id-om recepta)
            recently_used_ids = []
            for m in self.user_preferences.meal_history[-10:]:
                if isinstance(m, dict) and "id" in m:
                    recently_used_ids.append(m["id"])
                    
            if recipe.id in recently_used_ids:
                score -= 1
                
            ranked.append((recipe, score))
            
        # Sortiraj po skoru, od najvišeg ka najnižem
        ranked.sort(key=lambda x: x[1], reverse=True)
        
        # Ako su skorovi jednaki, pomešaj te recepte da bismo dobili različite preporuke
        final_ranked = []
        current_score = None
        current_group = []
        
        for recipe, score in ranked:
            if score != current_score:
                if current_group:
                    random.shuffle(current_group)
                    final_ranked.extend(current_group)
                current_score = score
                current_group = [recipe]
            else:
                current_group.append(recipe)
                
        if current_group:
            random.shuffle(current_group)
            final_ranked.extend(current_group)
            
        return final_ranked