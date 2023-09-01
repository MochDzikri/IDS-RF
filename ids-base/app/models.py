from django.db import models

class Data(models.Model):
    source_ip = models.CharField(max_length=15)
    destination_ip = models.CharField(max_length=15)
    source_port = models.PositiveIntegerField()
    destination_port = models.PositiveIntegerField()
    protocol = models.CharField(max_length=10)
    packet_length = models.PositiveIntegerField()
    timestamp = models.DateTimeField()
    flag_packet = models.CharField(max_length=10)
    data_payload = models.TextField()
    label = models.CharField(max_length=10)

    class Meta:
        db_table = "tbldata"
