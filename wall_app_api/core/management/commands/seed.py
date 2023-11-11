import secrets
from wall_app_api.users.models import User
from wall_app_api.entries.models import Entry
from django.core.management.base import BaseCommand


class Command(BaseCommand):

    help = "Seeds the database with some funny conversation."

    funny_conversation = [
        {"first_name": "Joey", "last_name": "Tribbiani", "message": "How you doin'?"},
        {
            "first_name": "Phoebe",
            "last_name": "Buffay",
            "message": "I just found a thumbtack on the ground. It's probably a sign from the universe."
        },
        {
            "first_name": "Monica",
            "last_name": "Geller",
            "message": "Can someone please explain to Joey what 'air quotes' mean?"
        },
        {"first_name": "Ross", "last_name": "Geller", "message": "Pivot!"},
        {"first_name": "Chandler", "last_name": "Bing", "message": "Could this BE any funnier?"}
    ]

    def seeding_already_done(self):
        return Entry.objects.exists()

    def handle(self, *args, **options):
        if self.seeding_already_done():
            print("Seeding already done previously. Nothing to be done.")
            return

        for participant in self.funny_conversation:
            username = participant['first_name'].lower()
            email = f"{username}@wall-app.friends.com"
            password = secrets.token_urlsafe(13)
            user = User.objects.create_user(
                email=email,
                password=password,
                first_name=participant['first_name'],
                last_name=participant['last_name']
            )
            Entry.objects.create(user=user, content=participant['message'])

        print("Seeding completed!")
