import os


class GCloudSync:

    def sync_folder_to_gcloud(self, gcp_bucket_url, filepath, filename):

        full_path = os.path.join(filepath, filename)

        # Wrap in quotes so spaces in path don’t break the command
        command = f'gsutil cp -r "{full_path}" gs://{gcp_bucket_url}/'

        print(f"Running command: {command}")
        os.system(command)

    def sync_folder_from_gcloud(self, gcp_bucket_url, filename, destination):

        command = f"gsutil cp gs://{gcp_bucket_url}/{filename} {destination}/{filename}"
        # command = f"gcloud storage cp gs://{gcp_bucket_url}/{filename} {destination}/{filename}"
        os.system(command)