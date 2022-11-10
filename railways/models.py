import datetime

from django.db import models


class Fare(models.Model):
    type = models.CharField(max_length=10)
    base_fare = models.IntegerField()
    sl_km = models.IntegerField()
    ac_km = models.IntegerField()

    def __int__(self):
        return self.base_fare


class Trains(models.Model):
    name = models.CharField(max_length=50)
    train_no = models.IntegerField()
    type = models.ForeignKey(Fare, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Stations(models.Model):
    code = models.CharField(max_length=50)
    train = models.ManyToManyField(Trains)

    def __str__(self):
        return self.code


class Distance(models.Model):
    st_from = models.ForeignKey(Stations, on_delete=models.CASCADE)
    st_to = models.ForeignKey(Stations, on_delete=models.CASCADE, related_name='to_st')
    distance = models.IntegerField()

    def __int__(self):
        return self.distance

    def __str__(self):
        return f'{self.st_from} to {self.st_to}'


class Days(models.Model):
    days = models.CharField(max_length=10)

    def __str__(self):
        return self.days


class TrainDays(models.Model):
    trains = models.ForeignKey(Trains, on_delete=models.CASCADE)
    train_days = models.ManyToManyField(Days)

    def __str__(self):
        return self.trains.name


class Timetable(models.Model):
    train_no = models.ForeignKey(Trains, on_delete=models.CASCADE)
    station_code = models.ForeignKey(Stations, related_name='stn', on_delete=models.CASCADE)
    timing = models.TimeField()

    def __str__(self):
        return f'{self.train_no.name}: {self.station_code}'


class Psg(models.Model):
    username = models.CharField(max_length=50)
    name = models.CharField(max_length=50)
    age = models.IntegerField()
    gender = models.CharField(max_length=5)
    train = models.IntegerField()
    coach = models.CharField(max_length=5)
    origin = models.CharField(max_length=10)
    destination = models.CharField(max_length=10)
    doj = models.CharField(max_length=50)
    created = models.DateTimeField(default=datetime.datetime.now)

    def __str__(self):
        return self.username


class Seats(models.Model):
    train_no = models.ForeignKey(Trains, on_delete=models.CASCADE)
    date = models.CharField(max_length=10)
    from_st = models.CharField(max_length=10)
    to_st = models.CharField(max_length=10)
    ac = models.PositiveSmallIntegerField(default=3)
    sl = models.PositiveSmallIntegerField(default=5)





