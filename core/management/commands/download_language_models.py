import os
import urllib
from urllib.request import urlretrieve

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError


class Command(BaseCommand):
    help = 'Closes the specified poll for voting'

    def add_arguments(self, parser):
        parser.add_argument('--source', type=str)
        parser.add_argument('--target', type=str)

    def handle(self, *args, **options):
        source, target = options['source'], options['target']
        model = f"opus-mt-{source}-{target}"
        print(">>>Downloading data for %s to %s model..." % (source, target))
        os.makedirs(os.path.join(settings.MODEL_PATH, model))
        for f in settings.ML_FILENAMES:
            try:
                print(os.path.join(settings.HUGGINGFACE_S3_BASE_URL, model, f))
                urlretrieve(
                    os.path.join(settings.HUGGINGFACE_S3_BASE_URL, model, f),
                    os.path.join(settings.MODEL_PATH, model, f)
                )
                print("Download complete!")
            except urllib.error.HTTPError:
                os.rmdir(os.path.join(settings.MODEL_PATH, model))
                CommandError(
                    "Error retrieving model from url."
                    " Please confirm model exists."
                )
                break
