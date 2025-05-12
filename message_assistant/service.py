# message_assistant/service.py

class MessageAssistantService:
    def __init__(self, user_profile):
        self.user_profile = user_profile
        self.communication_style = user_profile.get("communication_style", "casual")
        
    def draft_response(self, incoming_message, sender):
        """Generiše predlog odgovora na poruku."""
        # Analiza poruke
        message_intent = self._analyze_message_intent(incoming_message)
        
        # Generiši odgovor na osnovu stila komunikacije korisnika
        response = self._generate_response(
            message_intent, 
            incoming_message, 
            sender
        )
        
        return {
            "original_message": incoming_message,
            "sender": sender,
            "draft_response": response,
            "confidence": 0.8  # Za sada fiksna vrednost
        }
        
    def _analyze_message_intent(self, message):
        """Analizira nameru poruke (pitanje, poziv, poziv na akciju, itd.)"""
        # Jednostavna implementacija za početak
        message_lower = message.lower()
        
        if "?" in message:
            return "question"
        elif any(keyword in message_lower for keyword in ["sastanak", "poziv", "čujemo se", "vidimo se", "cujemo se", "vidimo se"]):
            return "meeting_request"
        elif any(keyword in message_lower for keyword in ["hvala", "zahvaljujem"]):
            return "gratitude"
        else:
            return "general_statement"
        
    def _generate_response(self, intent, message, sender):
        """Generiše odgovor na poruku."""
        # Osnovna implementacija za MVP
        if intent == "question":
            templates = {
                "formal": f"Poštovani {sender},\n\nHvala Vam na upitu. Razmotriću i odgovoriti što pre.\n\nS poštovanjem,\n{self.user_profile.get('name', 'Korisnik')}",
                "casual": f"Zdravo {sender},\n\nHvala na pitanju! Razmisliću i javiću ti uskoro.\n\nPozdrav,\n{self.user_profile.get('name', 'Korisnik')}",
                "friendly": f"Hej {sender}! 😊\n\nSuper pitanje! Vidim šta mogu da saznam i javljam ti se ubrzo.\n\nPozdrav!\n{self.user_profile.get('name', 'Korisnik')}"
            }
            
        elif intent == "meeting_request":
            templates = {
                "formal": f"Poštovani {sender},\n\nHvala Vam na predlogu za sastanak. Proveriću svoju dostupnost i javiti Vam se uskoro.\n\nS poštovanjem,\n{self.user_profile.get('name', 'Korisnik')}",
                "casual": f"Zdravo {sender},\n\nSvakako možemo da se nađemo! Pogledaću kalendar i javiti ti se za termin.\n\nPozdrav,\n{self.user_profile.get('name', 'Korisnik')}",
                "friendly": f"Hej {sender}! 😊\n\nDa, ajde da se vidimo! Baciću pogled na kalendar i predložiću ti neke termine.\n\nČujemo se!\n{self.user_profile.get('name', 'Korisnik')}"
            }
            
        elif intent == "gratitude":
            templates = {
                "formal": f"Poštovani {sender},\n\nNema na čemu, drago mi je da sam mogao/la da pomognem.\n\nS poštovanjem,\n{self.user_profile.get('name', 'Korisnik')}",
                "casual": f"Zdravo {sender},\n\nNema frke, drago mi je da sam mogao/la da pomognem! 🙂\n\nPozdrav,\n{self.user_profile.get('name', 'Korisnik')}",
                "friendly": f"Hej {sender}! 😊\n\nMa nema na čemu! Uvek sam tu ako ti treba još nešto!\n\nPozdrav!\n{self.user_profile.get('name', 'Korisnik')}"
            }
            
        else:  # general_statement
            templates = {
                "formal": f"Poštovani {sender},\n\nHvala Vam na poruci. Uzeo/la sam to u obzir.\n\nS poštovanjem,\n{self.user_profile.get('name', 'Korisnik')}",
                "casual": f"Zdravo {sender},\n\nHvala na poruci! Razmotriću to.\n\nPozdrav,\n{self.user_profile.get('name', 'Korisnik')}",
                "friendly": f"Hej {sender}! 😊\n\nSuper, hvala ti na poruci! Bacam pogled na to.\n\nPozdrav!\n{self.user_profile.get('name', 'Korisnik')}"
            }
            
        return templates.get(self.communication_style, templates["casual"])