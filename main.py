# main.py - sa detaljnijim logiranjem
import sys
import traceback
from ui.cli import CLI
from assistant.main import PersonalAssistant

def main():
    """Glavna funkcija aplikacije."""
    print("Inicijalizacija personalnog asistenta...")
    try:
        assistant = PersonalAssistant()
        
        print("Pokretanje korisničkog interfejsa...")
        ui = CLI(assistant)
        ui.run()
    except Exception as e:
        print("\n=== DETALJI GREŠKE ===")
        print(f"Tip greške: {type(e).__name__}")
        print(f"Poruka greške: {str(e)}")
        print("\nStack trace:")
        traceback.print_exc(file=sys.stdout)
        print("=" * 50)
        sys.exit(1)

if __name__ == "__main__":
    main()