from django.db import models

# Create your models here.

class adminuser (models.Model):
    emailid = models.CharField(primary_key=True,max_length=50)
    password = models.CharField(max_length=10,blank=True,null=True)
    Objects = models.Manager()



class appusers(models.Model):
    usercode = models.AutoField(primary_key=True)
    username = models.CharField(max_length=30,blank=True,null=True)
    emailid = models.CharField(unique=True,max_length=50,blank=True,null=True)
    phone = models.CharField(max_length=10,blank=True,null=True)
    regdate = models.DateField(blank=True,null=True)
    password = models.CharField(max_length=10,blank=True,null=True)
    Objects = models.Manager()

    def __str__(self):
        return str(self.usercode)


class genre (models.Model):
    genrename = models.CharField(primary_key=True,max_length=20)
    Objects = models.Manager()

    def __str__(self):
        return self.genrename



class book (models.Model):
    genrename = models.ForeignKey('genre', models.DO_NOTHING, db_column='genrename',blank=True, null=True)
    emailiduploadedby = models.CharField( max_length=50, blank=True, null=True)
    uploadeddate = models.DateField(blank=True, null=True)
    title = models.CharField(max_length=30)
    author = models.CharField(max_length=30)
    bookcode = models.AutoField(primary_key=True)
    bookdesc = models.CharField(max_length=500)
    imagefilename = models.FileField(upload_to='./')
    Objects = models.Manager()
    def __str__(self):
        return str(self.bookcode)


class chapters (models.Model):
    bookcode = models.ForeignKey('book', models.DO_NOTHING, db_column='bookcode', blank=True, null=True)
    chapterno = models.IntegerField(blank=True, null=True)
    chapterfilename = models.FileField(upload_to='./')
    chapteraudiofilename = models.FileField(upload_to='./')
    Objects = models.Manager()
    def __str__(self):
        return str(self.chapterno)


class playlist(models.Model):
    playlistid = models.AutoField(primary_key=True)
    usercode = models.ForeignKey('appusers', models.DO_NOTHING, db_column='usercode', blank=True, null=True)
    bookcode = models.ForeignKey('book', models.DO_NOTHING, db_column='bookcode', blank=True, null=True)
    addedon = models.DateField(blank=True, null=True)
    Objects = models.Manager()

    def _str_(self):
         return str(self.playlistid)

    # contains multiple rows for eachbook of each user
class userprogress(models.Model):
    progressid = models.AutoField(primary_key=True)
    usercode = models.ForeignKey('appusers', models.DO_NOTHING, db_column='usercode', blank=True, null=True)
    bookcode = models.ForeignKey('book', models.DO_NOTHING, db_column='bookcode', blank=True, null=True)
    startedon = models.DateField(blank=True, null=True)
    chapterscompleted = models.IntegerField(blank=True, null=True)
    Objects = models.Manager()

    def _str_(self):
        return str(self.progressid)

class feedback(models.Model):
    feedbackid = models.AutoField(primary_key=True)
    usercode = models.ForeignKey('appusers', models.DO_NOTHING, db_column='emailid', blank=True, null=True)
    feedbackdate = models.DateField(blank=True, null=True)
    bookcode = models.ForeignKey('book', models.DO_NOTHING, db_column='bookcode', blank=True, null=True)
    feedback = models.CharField(max_length=100, blank=True, null=True)
    Objects = models.Manager()

class requestbook(models.Model):
    requestid = models.AutoField(primary_key=True)
    usercode = models.ForeignKey('appusers', models.DO_NOTHING, db_column='emailid', blank=True, null=True)
    requestdate = models.DateField(blank=True, null=True)
    bookname = models.CharField(max_length=30, blank=True, null=True)
    authorname = models.CharField(max_length=30, blank=True, null=True)
    bookgenre = models.CharField(max_length=30, blank=True, null=True)

    Objects = models.Manager()


