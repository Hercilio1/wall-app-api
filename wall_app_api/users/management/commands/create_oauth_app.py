from django.core.management.base import BaseCommand
from oauth2_provider.models import get_application_model
import os


class Command(BaseCommand):
    help = 'Create an OAuth Application for Django OAuth Toolkit'

    def handle(self, *args, **options):
        Application = get_application_model()
        client_id = os.getenv('OAUTH_DEFAULT_APPLICATION_CLIENT_ID', 'client_id_for_dev_only')
        app, created = Application.objects.get_or_create(
            name="ROPC - Grant password flow",
            client_id=client_id,
            authorization_grant_type="password",
            client_type="public",
        )

        if created:
            self.stdout.write(self.style.SUCCESS('OAuth Application created successfully.'))
        else:
            self.stdout.write(self.style.SUCCESS('OAuth Application already exists.'))
