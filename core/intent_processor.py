# core/intent_processor.py
from datetime import datetime, timedelta
import re
from core.utils import extract_date, extract_meal_type, extract_recipient

class IntentProcessor:
    def __init__(self, meal_planner, message_assistant):
        self.meal_planner = meal_planner
        self.message_assistant = message_assistant
        
    def process_request(self, text):
        """Procesira korisnički zahtev i usmerava ga na odgovarajući servis."""
        intent_category, intent_details = self._classify_intent(text)
        
        if intent_category == "meal_planning":
            return self._handle_meal_planning(intent_details, text)
            
        elif intent_category == "messaging":
            return self._handle_messaging(intent_details, text)
            
        else:
            return {
                "response_type": "general",
                "message": "Trenutno mogu da vam pomognem oko planiranja obroka i poruka. Kako vam mogu pomoći u vezi sa tim?"
            }
            
    def _classify_intent(self, text):
        """Klasifikuje nameru korisničkog zahteva."""
        text_lower = text.lower()
        
        # Meal planning intenti
        meal_keywords = ["obrok", "jelo", "recept", "ručak", "večera", "doručak", "hrana", "jesti", "rucak", "vecera", "dorucak"]
        if any(keyword in text_lower for keyword in meal_keywords):
            if any(action in text_lower for action in ["planiraj", "predloži", "preporuči", "napravi", "predlozi", "preporuci", "daj", "spremiti"]):
                return "meal_planning", "suggest"
            elif any(action in text_lower for action in ["pokaži", "prikaži", "vidi", "pokazi", "prikazi", "videti"]):
                return "meal_planning", "view"
            else:
                return "meal_planning", "general"
                
        # Messaging intenti
        message_keywords = ["poruka", "odgovori", "napiši", "pošalji", "mail", "email", "komuniciranje", "napisi", "posalji"]
        if any(keyword in text_lower for keyword in message_keywords):
            if any(action in text_lower for action in ["sastavi", "napiši", "odgovori", "napisi"]):
                return "messaging", "draft"
            elif any(action in text_lower for action in ["pogledaj", "prikaži", "vidi", "pokazi", "prikazi"]):
                return "messaging", "view"
            else:
                return "messaging", "general"
                
        # General intenti / fallback
        return "unknown", None
        
    def _handle_meal_planning(self, intent_type, text):
        """Obrađuje zahteve vezane za planiranje obroka."""
        if intent_type == "suggest":
            # Izvuci relevantne informacije iz teksta
            date_str = extract_date(text)
            meal_type = extract_meal_type(text)
            
            # Pretvori string datum u objekat datuma ili koristi današnji datum
            if not date_str:
                date = datetime.now().date()
            else:
                date = date_str
                
            # Generiši predlog obroka
            if "nedelj" in text.lower() or "sedmic" in text.lower():
                meal_plan = self.meal_planner.generate_weekly_plan(date)
                return {
                    "response_type": "meal_plan_weekly",
                    "plan": meal_plan
                }
            else:
                meal_types_to_include = [meal_type] if meal_type else None
                meal_plan = self.meal_planner.generate_daily_plan(date, meal_types_to_include)
                return {
                    "response_type": "meal_plan_daily",
                    "plan": meal_plan
                }
                
        elif intent_type == "view":
            # Logika za prikaz postojećih planova obroka - za sada vraćamo generičku poruku
            return {
                "response_type": "general",
                "message": "Funkcionalnost pregleda postojećih planova obroka će biti dostupna uskoro."
            }
            
        return {
            "response_type": "general",
            "message": "Mogu vam pomoći da isplanirate obroke. Recite mi za koji dan ili obrok želite predlog."
        }
        
    def _handle_messaging(self, intent_type, text):
        """Obrađuje zahteve vezane za poruke."""
        if intent_type == "draft":
            # Izvuci ime primaoca i sadržaj poruke
            recipient = extract_recipient(text)
            original_message = self._extract_message_content(text)
            
            if recipient and original_message:
                draft = self.message_assistant.draft_response(
                    original_message, 
                    recipient
                )
                return {
                    "response_type": "message_draft",
                    "draft": draft
                }
            else:
                return {
                    "response_type": "general",
                    "message": "Možete li mi reći kome i na koju poruku želite da odgovorite?"
                }
                
        return {
            "response_type": "general",
            "message": "Mogu vam pomoći da sastavite odgovor na poruke. Molim vas da mi kažete čiju poruku i kako da odgovorim."
        }
        
    def _extract_message_content(self, text):
        """Ekstrahuje sadržaj poruke na koju treba odgovoriti."""
        # Traži poruku između navodnika ili nakon "na poruku", "odgovori na"
        message_patterns = [
            r'"([^"]*)"',  # Tekst između navodnika
            r'na poruku[:\s]+(.+?)(?=\s*$|\s+od|\s+kome)',  # Tekst nakon "na poruku"
            r'odgovori na[:\s]+(.+?)(?=\s*$|\s+od|\s+kome)'  # Tekst nakon "odgovori na"
        ]
        
        for pattern in message_patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                return match.group(1).strip()
                
        return None