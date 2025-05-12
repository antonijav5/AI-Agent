# ui/cli.py
import sys

import traceback

class CLI:
    def __init__(self, assistant):
        self.assistant = assistant
        self.running = False
        
    def run(self):
        """Pokreće CLI interfejs."""
        self.running = True
        self._print_welcome()
        
        while self.running:
            try:
                # Čitaj korisnički unos
                user_input = input("\n> ")
                
                # Obradi komande za izlaz
                if user_input.lower() in ["exit", "quit", "q", "kraj", "izlaz"]:
                    self._exit()
                    continue
                
                if not user_input.strip():
                    continue
                    
                # Obradi korisnički unos
                response = self.assistant.process_command(user_input)
                
                # Prikaži odgovor
                print(f"\n{response}")
                
            except KeyboardInterrupt:
                self._exit()
            except Exception as e:
                print(f"\nDošlo je do greške: {str(e)}")
                traceback.print_exc()
                sys.exit(1)
                
    def _print_welcome(self):
        """Prikazuje poruku dobrodošlice."""
        print("=" * 50)
        print(f"Dobrodošli u vašeg personalnog asistenta!")
        print("Napišite 'exit' ili 'kraj' za izlaz.")
        print("=" * 50)
        print("\nKako vam mogu pomoći danas?")
        
    def _exit(self):
        """Zatvara aplikaciju."""
        print("\nDoviđenja! Hvala što ste koristili vašeg personalnog asistenta.")
        self.running = False
        sys.exit(0)
        