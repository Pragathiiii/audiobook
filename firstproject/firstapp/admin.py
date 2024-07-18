from django.contrib import admin
from .models import adminuser,appusers,genre,book,chapters,userprogress,playlist,feedback,requestbook
# Register your models here.

@admin.register(adminuser)
class adminuser(admin.ModelAdmin):
    list_display = ('emailid','password',)

@admin.register(appusers)
class appusers(admin.ModelAdmin):
    list_display = ('usercode','username','emailid','phone','regdate','password')

@admin.register(genre)
class genre(admin.ModelAdmin):
    list_display = ('genrename',)

@admin.register(book)
class book(admin.ModelAdmin):
    list_display = ('genrename','emailiduploadedby','uploadeddate','title','author','bookdesc','bookcode', 'imagefilename', )



@admin.register(chapters)
class chapters(admin.ModelAdmin):
    list_display = ('bookcode','chapterno','chapterfilename','chapteraudiofilename')

# @admin.register(userprogress)
# class userprogress(admin.ModelAdmin):
#     list_display = ('usercode','bookcode','startedon','chapterscompleted')

@admin.register(playlist)
class playlist(admin.ModelAdmin):
    list_display = ('playlistid','usercode','bookcode','addedon')

@admin.register(feedback)
class feedback(admin.ModelAdmin):
    list_display = ('feedbackid','usercode','feedbackdate','bookcode','feedback')

@admin.register(requestbook)
class requestbook(admin.ModelAdmin):
  list_display = ('requestid','usercode','requestdate','bookname','authorname','bookgenre')