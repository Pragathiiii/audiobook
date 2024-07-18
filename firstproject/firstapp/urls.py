from django.urls import re_path
from.import views, adminviews

urlpatterns = [
    #templates
re_path(r'^index/$', views.index, name="index page "),

#userURLS
re_path(r'^userregistration', views.userregistration, name="load userregistration form"),
re_path(r'^userloginform/$', views.userloginform, name="userlogin form "),
re_path(r'^userlogin/$', views.userlogin, name="userlogin code "),
re_path(r'^userhome/$', views.userhome, name="user displaygenre "),
re_path(r'^userviewbooks/([\w\s]+)/$', views.userviewbooks, name="get filtered books on genre"),
re_path(r'^download/([\d]+)/([\w\s]+)/$', views.download, name='download'),
re_path(r'^viewmylist/$', views.viewmylist, name=' user viewmylist'),
re_path(r'^changepassword/$', views.changepassword, name="changepwd"),
re_path(r'^addfeedback/([\d]+)/$', views.addfeedback, name="load feedback"),
re_path(r'^addrequest/$', views.addrequest, name="load request"),
re_path(r'^signout/$', views.signout, name="signout"),
re_path(r'^forgotpasswordform/$', views.forgotpasswordform, name="forgotpasswordform"),
re_path(r'^forgotpassword/$', views.forgotpassword, name="forgotpassword"),

#AdminURLS
re_path(r'^playaudio/$', adminviews.playaudio, name="playaudio"),
re_path(r'^addgenre', adminviews.addgenre, name="load addgenre form"),
re_path(r'^adminhome', adminviews.adminhome, name="load admin home"),
re_path(r'^viewgenreadmin/$', adminviews.viewgenreadmin, name="user displaygenre for admin"),
re_path(r'^viewappusers/$', adminviews.viewappusers, name="user displayappusers for admin"),
re_path(r'^adminloginform/$', adminviews.adminloginform, name="adminlogin form "),
re_path(r'^adminlogin/$', adminviews.adminlogin, name="adminlogin code "),
re_path(r'^addbook/$', adminviews.addbook, name="load addbookform "),
re_path(r'^getbooks/([\w\s]+)/$', adminviews.getbooks, name="load viewbookform "),
re_path('^addchapters/([\d]+)/([\w\s]+)/$',adminviews.addchapters,name="add chapters of selected bookcode"),
re_path(r'^playaudio/([\w\s.]+)/?$', adminviews.playaudio, name="playaudio"),
re_path(r'^admingetchapters/([\d]+)/([\w\s]+)/$', adminviews.admingetchapters, name="getchapters of selected bookcode"),
re_path(r'^adminchangepassword/$', adminviews.changepassword, name="changepwd admin"),
re_path(r'^viewfeedback/$', adminviews.viewfeedback, name="view feedback "),
re_path(r'^viewrequest/$', adminviews.viewrequest, name="view request "),
re_path(r'^adminsignout/$', adminviews.adminsignout, name="admin signout"),

]
