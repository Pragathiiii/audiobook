from django.shortcuts import render
from .models import appusers, adminuser
from .models import appusers, genre, book, chapters,feedback,requestbook
from .forms import bookForm,addgenreForm,chapterForm,AdminChangePasswordForm,ChangePasswordForm
import datetime, os
from django.conf import settings
from PyPDF2 import PdfReader
import PyPDF2
import os
import tempfile
from gtts import gTTS

def addgenre(request):
    genre = addgenreForm(request.POST or None)
    if genre.is_valid():
        genre.save()
        msg = "Genre added Successfully!"

        return render(request, 'firstapp/adminoutput.html', {'message': msg})
    return render(request, 'firstapp/addgenre.html', {'genre': genre})
def viewgenreadmin(request):
    genreobj = genre.Objects.all()
    return render(request, 'firstapp/viewgenreadmin.html', {'genre': genreobj})

def viewappusers(request):
    appusersobj = appusers.Objects.all()
    return render(request, 'firstapp/viewappusers.html', {'appusers': appusersobj})


def adminloginform(request):
    return render(request,'firstapp/adminloginform.html')
def adminhome(request):
    return render(request,'firstapp/adminhome.html')

def adminlogin(request):
    varemailid = request.POST.get("emailid")
    varpassword = request.POST.get("password")
    try:
        admindata= adminuser.Objects.get(emailid=varemailid,password=varpassword)
        request.session["emailid"]=varemailid
        request.session["password"]=varpassword
        return render(request,'firstapp/adminhome.html')
    except:
        return render(request, 'firstapp/adminoutput.html',{'message':'INVALID LOGIN'})

def addbook(request):

        form = bookForm(request.POST,request.FILES)
        if form.is_valid():
            book_obj = form.save(commit=False)
            book_obj.emailiduploadedby=request.session["emailid"]
            book_obj.uploadeddate=datetime.date.today()
            book_obj.save()
            return render(request, 'firstapp/adminoutput.html', {'message': 'Book Added'})
        return render(request, 'firstapp/addbook.html', {'form': form})

def getbooks(request,genrename):
    books_obj = book.Objects.filter(genrename=genrename)
    return render(request, 'firstapp/viewbooks.html', {'books_obj': books_obj})


def extract_text_from_pdf(pdf_path):
    with open(pdf_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        text = ''
        for page in reader.pages:
            text += page.extract_text()
        return text


def addchapters(request, vbookcode, title):
    if request.method == 'POST':
        form = chapterForm(request.POST, request.FILES)
        if form.is_valid():
            chapter_obj = form.save(commit=False)
            book_obj = book.Objects.get(bookcode=vbookcode)

            chapter_obj.bookcode = book_obj
            chapter_obj.save()
            chapterno = form.cleaned_data['chapterno']

            #################
            # Get the uploaded PDF file
            pdf_file = request.FILES['chapterfilename']
            pdf_path = os.path.join(tempfile.gettempdir(), pdf_file.name)

            # Save the PDF file temporarily
            with open(pdf_path, 'wb') as file:
                for chunk in pdf_file.chunks():
                    file.write(chunk)

            # Extract text from PDF
            text = extract_text_from_pdf(pdf_path)

            # Generate audio from extracted text using gTTS
            tts = gTTS(text=text, lang='en')
            mp3_filename = f'chapter_{vbookcode}_{chapterno}.mp3'
            mp3_filepath = os.path.join('images', mp3_filename)


            # Update the row in the database
            chapter_obj.chapteraudiofilename = mp3_filename
            chapter_obj.save()

            # Delete the temporary PDF file
            os.remove(pdf_path)

            ##################
            return render(request, 'firstapp/adminoutput.html', {'message': 'Upload done'})
    else:
        initial_data = {'bookcode': vbookcode, 'title': title}  # Provide initial value for the extra field
        form = chapterForm(initial=initial_data)
    return render(request, 'firstapp/addchapters.html', {'form': form})


def playaudio(request, audiofilename):
    audio_url = os.path.join(settings.MEDIA_URL, audiofilename)
    return render(request, 'firstapp/playaudio.html', {'audio_url': audio_url})

# display all chapters list of selected book
def admingetchapters(request, bookcode,title):
    chapters_obj = chapters.Objects.filter(bookcode=bookcode)
    return render(request, 'firstapp/adminviewchapters.html', {'chapters_obj': chapters_obj,'title':title})

def changepassword(request):
    if request.method == 'POST':
        form = AdminChangePasswordForm(request.POST)

        if form.is_valid():
            admincurrent_password = form.cleaned_data['admincurrent_password']
            adminnew_password = form.cleaned_data['adminnew_password']

            # Retrieve the user from the database using the session information
            emailid = request.session['emailid']
            password = request.session['password']

            try:
                admin = adminuser.Objects.get(emailid=emailid)

                if password == admincurrent_password:
                    admin.password = adminnew_password
                    admin.save()

                    return render(request, 'firstapp/adminoutput.html', {'message': 'Password updated successfully.'})
                else:
                    form.add_error('current_password', 'Current password is incorrect.')
            except appusers.DoesNotExist:
                form.add_error(None, 'Admin does not exist.')
    else:
        form = AdminChangePasswordForm()

    return render(request, 'firstapp/adminchangepassword.html', {'form': form})

def viewfeedback(request):
    usercode=request.session["usercode"]
    # playlist_obj = get_object_or_404(playlist, usercode=usercode)
    fb_obj=feedback.Objects.select_related('usercode').select_related('bookcode').filter(usercode=usercode)
    return render(request, 'firstapp/viewfeedback.html', {'fb_obj': fb_obj})

def viewrequest(request):
    usercode=request.session["usercode"]
    # playlist_obj = get_object_or_404(playlist, usercode=usercode)
    r_obj=requestbook.Objects.select_related('usercode').filter(usercode=usercode)
    return render(request, 'firstapp/viewrequest.html', {'r_obj': r_obj})

def adminsignout(request):
    request.session.flush()
    return render(request, 'firstapp/adminloginform.html')