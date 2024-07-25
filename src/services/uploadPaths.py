import os
from django.utils import timezone
from django.conf import settings

class UploadPaths:

    @staticmethod
    def get_file_name(filename):
        ext = filename.split('.')[-1]
        timestamp = timezone.now().strftime("%Y%m%d-%H%M%S")
        filename = f"{timestamp}.{ext}"
        return filename

    def get_upload_path(self, istance, filename, folder):
        new_filename = self.get_file_name(filename)
        path = os.path.join(settings.MEDIA_ROOT, folder)
        if not os.path.exists(folder):
            os.makedirs(path)
        else:
            for filename in os.listdir(path):
                file_path = os.path.join(path, filename)
                if os.path.isfile(file_path):
                    os.remove(file_path)

        return os.path.join(folder, new_filename)

    def avatar_upload_path(self, instance, filename):
        return self.get_upload_path(instance, filename, folder=f"profiles/profile_{instance.id}")

    def course_img_upload_path(self, instance, filename):
        return self.get_upload_path(instance, filename, folder=f"course/course_{instance.id}")

    def content_img_upload_path(self, instance, filename):
        return self.get_upload_path(instance, filename, folder=f"course/course_{instance.id}/content")
