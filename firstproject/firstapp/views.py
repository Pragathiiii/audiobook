from django.http import HttpResponse
from django.shortcuts import render
from .forms import appusersForm, addgenreForm,feedbackForm,requestForm
from .models import appusers, genre, book, chapters,playlist
import zipfile,datetime
from .forms import ChangePasswordForm
from django.shortcuts import get_object_or_404
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
import pyttsx3 as tts
# Create your views here.
def userregistration(request):
    form = appusersForm(request.POST or None)
    if form.is_valid():
        book_obj=form.save(commit=False)
        book_obj.regdate=datetime.date.today()

        form.save()
        msg = "Registration is Successfull! "

        return render(request, 'firstapp/output.html', {'message': msg})
    return render(request, 'firstapp/userregistration.html', {'form': form})


def userloginform(request):
    return render(request,'firstapp/userloginform.html')

def index(request):
    return render(request,'firstapp/index.html')
def userlogin(request):
    varemailid = request.POST.get("emailid")
    varpassword = request.POST.get("password")
    try:
        userobj= appusers.Objects.get(emailid=varemailid,password=varpassword)
        request.session["emailid"] = varemailid
        request.session["password"] = varpassword
        request.session["usercode"] = userobj.usercode
        genreobj = genre.Objects.all()
        return render(request,'firstapp/userhome.html', {'genre': genreobj})
    except:
        return render(request, 'firstapp/useroutput.html',{'message':'INVALID LOGIN'})

def userviewbooks(request, genrename):
    books_obj = book.Objects.filter(genrename=genrename)
    return render(request, 'firstapp/userviewbooks.html', {'books_obj': books_obj, 'genrename':genrename})

def userhome(request):
    try:
        # returns the entire row in userdata
        genreobj = genre.Objects.all()
        return render(request, 'firstapp/userhome.html',{'genre':genreobj})
    except:
        return render(request, 'firstapp/useroutput.html', {'message': 'Error'})

def download(request, bookcode,title):
    usercode = request.session["usercode"]
    addtoplaylist(bookcode,title,usercode)
    folder_path = 'images/'
    audio_files = chapters.Objects.filter(bookcode=bookcode).values_list('chapteraudiofilename', flat=True)
    zip_file_name = bookcode + '.zip'
    zip_file_path = folder_path + zip_file_name
    with zipfile.ZipFile(zip_file_path, 'w') as zip_file:
        for audio_file in audio_files:
            audio_file_path = folder_path + audio_file
            zip_file.write(audio_file_path, audio_file)
    response = HttpResponse(open(zip_file_path, 'rb'), content_type='application/zip')
    response['Content-Disposition'] = 'attachment; filename=%s' % zip_file_name
    return response

def addtoplaylist(bookcode,title,vusercode):
    playlist_obj = playlist()
    usercode=vusercode
    # Set the fields using the provided parameters and system date
    playlist_obj.addedon = datetime.date.today()

    books_obj = book.Objects.get(bookcode=bookcode)
    appusers_obj=appusers.Objects.get(usercode=vusercode)
    playlist_obj.bookcode = books_obj
    playlist_obj.usercode = appusers_obj
    playlist_obj.title = title

    # Save the Playlist instance
    playlist_obj.save()

def userviewbooks(request, genrename):
    books_obj = book.Objects.filter(genrename=genrename)
    return render(request, 'firstapp/userviewbooks.html', {'books_obj': books_obj, 'genrename':genrename})

def viewmylist(request):
    usercode=request.session["usercode"]
    # playlist_obj = get_object_or_404(playlist, usercode=usercode)
    playlist_obj=playlist.Objects.select_related('bookcode').filter(usercode=usercode)
    return render(request, 'firstapp/viewmylist.html', {'playlist_obj': playlist_obj})



def changepassword(request):
    if request.method == 'POST':
        form = ChangePasswordForm(request.POST)

        if form.is_valid():
            current_password = form.cleaned_data['current_password']
            new_password = form.cleaned_data['new_password']

            # Retrieve the user from the database using the session information
            usercode = request.session['usercode']
            emailid = request.session['emailid']
            password= request.session['password']

            try:
                user = appusers.Objects.get(usercode=usercode, emailid=emailid)

                if password == current_password:
                    user.password = new_password
                    user.save()

                    return render(request, 'firstapp/useroutput.html',{'message':'Password updated successfully.'})
                else:
                    form.add_error('current_password', 'Current password is incorrect.')
            except appusers.DoesNotExist:
                form.add_error(None, 'User does not exist.')
    else:
        form = ChangePasswordForm()

    return render(request, 'firstapp/changepassword.html', {'form': form})

def addfeedback(request,bookcode):
    form = feedbackForm(request.POST)
    if form.is_valid():
        fb_obj = form.save(commit=False)
        useremailid = request.session["emailid"]
        appuser_obj=appusers.Objects.get(emailid=useremailid)
        fb_obj.usercode=appuser_obj
        fb_obj.bookcode= book.Objects.get(bookcode=bookcode)
        fb_obj.feedbackdate = datetime.date.today()
        fb_obj.save()
        return render(request, 'firstapp/useroutput.html', {'message': 'Feedback Added'})
    return render(request, 'firstapp/feedbackform.html', {'form': form})

def signout(request):
    request.session.flush()
    return render(request,'firstapp/userloginform.html')

def addrequest(request):
    form = requestForm(request.POST)
    if form.is_valid():
        r_obj = form.save(commit=False)
        usercode = request.session["usercode"]
        appuser_obj=appusers.Objects.get(usercode=usercode)
        r_obj.usercode=appuser_obj
        r_obj.requestdate = datetime.date.today()
        form.save()
        return render(request, 'firstapp/useroutput.html', {'message': 'Request Added'})
    return render(request, 'firstapp/requestform.html', {'form': form})

def forgotpasswordform(request):
    return render(request, 'firstapp/forgotpassword.html')


def forgotpassword(request):
    emailid = request.POST.get("textemailid")
    appusersobj = appusers.Objects.get(emailid=emailid)
    password = appusersobj.password
    username = appusersobj.username

    #
    subject, from_email, to = 'reset password', 'pragatishettyy@gmail.com', emailid
    html_content = render_to_string('firstapp/mailhtml.html',
                                    {'username': username, 'pass': password})
    # render with dynamic value
    text_content = strip_tags(html_content)
    # Strip the html tag. So people can see the pure text at least.

    # create the email, and attach the HTML version as well.
    msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
    msg.attach_alternative(html_content, "text/html")
    msg.send()
    request.session["message"] = "Hi " + username + ", please check your mail for password"
    return render(request, 'firstapp/membersigninoutput.html', {'message': request.session["message"]})

