# core/utils.py
import re
from datetime import datetime, timedelta

def extract_date(text):
    """Ekstrahuje datum iz teksta."""
    text_lower = text.lower()
    
    # Prepoznavanje relativnih datuma
    if "danas" in text_lower:
        return datetime.now().date()
    elif "sutra" in text_lower:
        return (datetime.now() + timedelta(days=1)).date()
    elif "prekosutra" in text_lower:
        return (datetime.now() + timedelta(days=2)).date()
    
    # Prepoznavanje dana u nedelji
    days_of_week = {
        "ponedeljak": 0, "utorak": 1, "sreda": 2, "četvrtak": 3, 
        "petak": 4, "subota": 5, "nedelja": 6
    }
    
    for day, day_num in days_of_week.items():
        if day in text_lower:
            # Izračunaj koliko dana treba dodati da se dođe do tog dana
            today = datetime.now().weekday()
            days_ahead = day_num - today
            if days_ahead <= 0:  # Ako je dan već prošao ove nedelje, uzmi sledeći
                days_ahead += 7
            return (datetime.now() + timedelta(days=days_ahead)).date()
    
    # Prepoznavanje datuma u formatu dd.mm ili dd.mm.yyyy
    date_patterns = [
        r'(\d{1,2})\.(\d{1,2})(?:\.(\d{4}))?',  # 15.8 ili 15.8.2023
        r'(\d{1,2})\/(\d{1,2})(?:\/(\d{4}))?'   # 15/8 ili 15/8/2023
    ]
    
    for pattern in date_patterns:
        match = re.search(pattern, text)
        if match:
            day, month, year = match.groups()
            year = year or datetime.now().year  # Ako godina nije navedena, uzmi trenutnu
            try:
                return datetime(int(year), int(month), int(day)).date()
            except ValueError:
                continue  # Ako datum nije validan, probaj sledeći pattern
    
    return None

def extract_meal_type(text):
    """Ekstrahuje tip obroka iz teksta."""
    text_lower = text.lower()
    
    meal_types = {
        "doručak": ["doručak", "dorucak", "jutarnji obrok", "ujutru", "dorucak", "jutro"],
        "ručak": ["ručak", "rucak", "podnevni obrok", "popodne", "rucak"],
        "večera": ["večera", "vecera", "večernji obrok", "uveče", "uvece", "vecera"],
        "užina": ["užina", "uzina", "snack", "međuobrok", "međuobrok", "uzina"]
    }
    
    for meal_type, keywords in meal_types.items():
        if any(keyword in text_lower for keyword in keywords):
            return meal_type
            
    return None

def extract_recipient(text):
    """Ekstrahuje primaoca poruke iz teksta."""
    # Traži paterne kao "odgovori Marku", "poruka za Janu"
    recipient_patterns = [
        r'odgovori (?:za|na)?\s+(.+?)(?=\s+na|\s*$)',
        r'(?:poruka|odgovor|mail) (?:za|od)\s+(.+?)(?=\s+na|\s*$)'
    ]
    
    for pattern in recipient_patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            return match.group(1).strip()
            
    return None