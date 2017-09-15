#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy
import smtplib
import pygtk
import os
import time
pygtk.require('2.0')
import gtk
from VideoCapture import Device
from email import encoders
from email.header import Header
from email.mime.text import MIMEText
from email.utils import parseaddr, formataddr
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage

supervisors = ('Zhao Meijun', 'Kevin Lim', 'Lui WoeiWen', 'Noel Teo', 'Tay HockLeong', 'Lai ChoeYin',
               'Teo ChengYong', 'Kassim Saat', 'Steven Ng', 'Chin YeowHong', 'Edwin Foo', 'Lee TeckHeng',
               'Tan KianSin', 'Wong Yau', 'Kang LiatHong', 'Koh KahEng', 'Lai YewKwong', 'Lim SockLip')
sender = 'FYP_Attendence@nyp.edu.sg'
receivers = {'Zhao Meijun': 'Zhao_Meijun@nyp.edu.sg', 'Kevin Lim': 'Kevin_LIM@nyp.edu.sg', 'Lui WoeiWen': 'LUI_Woei_Wen@nyp.edu.sg',
             'Noel Teo': 'Noel_TEO@nyp.edu.sg', 'Tay HockLeong': 'TAY_Hock_Leong@nyp.edu.sg', 'Lai ChoeYin': 'LAI_Choe_Yin@nyp.edu.sg',
             'Teo ChengYong': 'TEO_Cheng_Yong@nyp.edu.sg', 'Kassim Saat': 'Kassim_SATT@nyp.edu.sg', 'Steven Ng': 'Steven_NG@nyp.edu.sg',
             'Chin YeowHong': 'CHIN_Yeow_Hong@nyp.edu.sg', 'Edwin Foo': 'Edwin_Foo@nyp.edu.sg', 'Lee TeckHeng': 'LEE_Teck_Heng@nyp.edu.sg',
             'Tan KianSin': 'TAN_Kian_Sin@nyp.edu.sg', 'Wong Yau': 'WONG_Yau@nyp.edu.sg', 'Kang LiatHong': 'KANG_Liat_Hong@nyp.edu.sg',
             'Koh KahEng': 'KOH_Kah_Eng', 'Lai YewKwong': 'LAI_Yew_Kwong@nyp.edu.sg', 'Lim SockLip': 'LIM_Sock_Lip@nyp.edu.sg'}

current_receiver = ''
current_remarks = ''

cam = Device()
cam.setResolution(320,240)

t = time.localtime()

class PyApp(gtk.Window):
    def __init__(self):
        super(PyApp, self).__init__()
        
        self.set_title("Attendence System")
        self.resize(500, 300)
        self.set_position(gtk.WIN_POS_CENTER)
        self.connect("destroy", gtk.main_quit)

        self.supervisor = gtk.combo_box_entry_new_text()
        self.supervisor.append_text('Select Supervisior')
        for name in supervisors:
            self.supervisor.append_text(name)
        self.supervisor.set_active(0)
        self.supervisor.set_size_request(130, 35)
        self.supervisor.child.connect('changed', self.dropmenu)
        
        self.sign_in = gtk.Button("Sign In")
        self.sign_in.set_size_request(60, 35)
        self.sign_in.connect("clicked", self.signin)
        
        self.sign_out = gtk.Button("Sign Out")
        self.sign_out.set_size_request(60, 35)
        self.sign_out.connect("clicked", self.signout)

        self.capture = gtk.Button('Take Photo')
        self.capture.set_size_request(120,35)
        self.capture.connect("clicked", self.takephoto)

        self.remarks_label = gtk.Label('Remarks:')

        self.remarks_entry = gtk.Entry(max = 300)
        self.remarks_entry.set_size_request(140,20)
        self.remarks_entry.set_text("")

        self.status_label = gtk.Label('Status:')
        self.status_info = gtk.Label('Please Select Supervisior')

        self.image = gtk.Image()
        self.image.set_size_request(320, 240)
        self.image.set_from_file("initial.jpg")
        self.image.show()
        
        fixed = gtk.Fixed()
        fixed.put(self.supervisor, 10, 30)
        fixed.put(self.sign_in, 10, 80)
        fixed.put(self.sign_out, 75, 80)
        fixed.put(self.capture, 10,120)
        fixed.put(self.image, 160, 30)
        fixed.put(self.remarks_label, 10, 165)
        fixed.put(self.remarks_entry, 10, 185)
        fixed.put(self.status_label, 10, 225)
        fixed.put(self.status_info, 10, 245)

        self.add(fixed)
        self.show_all()

    def dropmenu(self, entry):
        global current_receiver
        # print "You click", entry.get_text()
        current_receiver = entry.get_text()
        self.status_info.set_text('Please Take Photo')
    
    def signin(self, button):
        global current_remarks
        # print "Sign In"
        # print self.remarks_entry.get_text()
        current_remarks = self.remarks_entry.get_text()
        SendMail()
        self.status_info.set_text('You have signed in!')
        self.image.set_from_file("initial.jpg")
        self.image.show()
        
        

    def signout(self, button):
        global current_remarks
        # print "Sign Out"
        # print self.remarks_entry.get_text()
        current_remarks = self.remarks_entry.get_text()
        SendMail()
        self.status_info.set_text('You have signed Out!')
        self.image.set_from_file("initial.jpg")
        self.image.show()

    def takephoto(self, button):
        TakePhoto()
        # print "Captured"
        self.status_info.set_text('Capture Finished')
        
def TakePhoto():
    cam.saveSnapshot('image.jpg', timestamp=3,boldfont=1)
    newUI.image.set_from_file("image.jpg")
    #pilimage = cam.getImage(timestamp=3,boldfont=1)
    #arr = numpy.array(pilimage)
    #newUI.image.set_from_pixbuf(gtk.gdk.pixbuf_new_from_array(arr, gtk.gdk.COLORSPACE_RGB, 8))
    newUI.image.show()


def SendMail():
    global current_remarks
    # print 'You have sent mail to', receivers[current_receiver]
    # print 'Remarks is', current_remarks

    Signiture_Time = " Sign at: " + repr(t.tm_hour)+ ":" + repr(t.tm_min) + ":" + repr(t.tm_sec) + " D" + repr(t.tm_mday) + "M" + repr(t.tm_mon) + "Y" + repr(t.tm_year)
    current_remarks = current_remarks + Signiture_Time
    img_data = open('image.jpg', 'rb').read()
    msg = MIMEMultipart()
    msg['Subject'] = 'FYP Attendence'
    msg['From'] = sender
    msg['To'] = receivers[current_receiver]

    text = MIMEText(current_remarks)
    msg.attach(text)
    image = MIMEImage(img_data, name=os.path.basename('image.jpg'))
    msg.attach(image)
    
    try:
       smtpObj = smtplib.SMTP('172.17.192.201')
       smtpObj.sendmail(sender, receivers[current_receiver], msg.as_string())         
       print "Successfully sent email"
    except SMTPException:
       print "Error: unable to send email"
       
newUI = PyApp()
gtk.main()
