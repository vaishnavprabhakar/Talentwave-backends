from cloudinary import uploader
from django.conf import settings
from cloudinary.exceptions import Error


def upload_to_cloud(obj, folder, secure=True, overwrite=False):
    image_obj = obj
    folder_path = folder
    uploader.upload_image(file=image_obj, folder=folder_path, resource_type="image")


def update_image_resource(public_id, folder, overwrite=True, **options):
    try:
        print(options)
        _folder = folder
        updated_image = uploader.upload(
            public_id, folder=_folder, overwrite=overwrite, **options
        )
    except Exception as e:
        print(e)
    return updated_image
