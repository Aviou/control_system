from django.core.management.base import BaseCommand, CommandError
from control import startup  # Passen Sie den Importpfad entsprechend Ihrer Projektstruktur an

class Command(BaseCommand):
    help = 'Startet den Telegram Bot'

    def handle(self, *args, **options):
        try:
            self.stdout.write(self.style.SUCCESS('Versuche, den Telegram Bot zu starten...'))
            # Hier rufen Sie die Funktion zum Starten Ihres Bots auf
            startup.start_bot()
            self.stdout.write(self.style.SUCCESS('Der Telegram Bot wurde erfolgreich gestartet!'))
        except Exception as e:
            raise CommandError(f'Fehler beim Starten des Telegram Bots: {e}')
            self.stdout.write(self.style.ERROR('Fehler beim Starten des Telegram Bots.'))
