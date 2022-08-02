from django.core.management.base import BaseCommand
from rooms.models import Facility
class Command(BaseCommand):

    help = "This command creates facilities"
    
    """def add_arguments(self, parser) :
        
        parser.add_argument("--times",
        help = "How?")"""

    def handle(self, *args, **options):
        facilities = [
            "Private entrance",
            "Paid parking on premises",
            "Paid parking off premises",
            "Elevatior",
            "Cat",
            "Parking",
            "Gym",
        ]
        for a in facilities:
            Facility.objects.create(name = a)

        self.stdout.write(self.style.SUCCESS("Facilities created!"))

    
