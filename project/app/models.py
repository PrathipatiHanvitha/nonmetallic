from django.db import models

class register(models.Model):
    Username = models.CharField(max_length=20)
    Email = models.CharField(max_length=20)
    Password = models.CharField(max_length=20)

class User(models.Model):
    user_id = models.CharField(max_length=100, unique=True)
    is_authorized = models.BooleanField(default=False)
    client = models.OneToOneField(register, null=True, on_delete=models.CASCADE)  # Ensure this is correct

    def __str__(self):
        return self.user_id


class EncryptedData(models.Model):
    data = models.BinaryField()
    key = models.BinaryField()
    created_at = models.DateTimeField(auto_now_add=True)
    client_details = models.CharField(max_length=255) 

    def __str__(self):
        return f"Data {self.id}"

class DencryptedData(models.Model):
    data = models.BinaryField()
    encrypted_data = models.ForeignKey(EncryptedData, on_delete=models.CASCADE)  # Link back to EncryptedData
    def __str__(self):
        return f"Decrypted Data {self.id} linked to {self.encrypted_data.id}"


    
