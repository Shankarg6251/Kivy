from kivy.app import App
from kivy.uix.relativelayout import RelativeLayout
from kivy.lang import Builder
 
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.properties import ObjectProperty
from KivyCalendar import CalendarWidget
from KivyCalendar import DatePicker
from kivy.uix.dropdown import DropDown
from kivy.uix.screenmanager import ScreenManager, Screen
import mysql.connector as sql
from openpyxl import Workbook
import re

class loginWindow(Screen):
    email = ObjectProperty(None)
    pwd = ObjectProperty(None)
        
    def login(self):
        mail=self.email.text
        password=self.pwd.text
        print(mail)
        print(password)
        regex = '^[A-Za-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'
        if mail!="" and password!="":
            if re.search(regex,mail):
                print("Verifying...")
                con=sql.connect(host="localhost",user="root",password="",database="kivy")
                cur=con.cursor()
                query="SELECT * From wise WHERE Email=%s AND Password=%s;"
                val=(mail,password)
                cur.execute(query,val)
                result=cur.fetchall()
                count=cur.rowcount
                con.commit()
                con.close()
                print(count)
                if count>=1:
                    print("Successfully Login")
                    #homepage.fun()
                    sm.current='mainpage'
                    """pop = Popup(title='Success',content=Label(text='Logging in...'),size_hint=(None, None), size=(200, 200))
                    pop.open()"""
                else:
                    print("Invalid Mail or Password")
                    pop = Popup(title='Error !!',content=Label(text='Invalid Mail'),size_hint=(None, None), size=(200, 200))
                    pop.open()
            else:
                print("Invalid Mail")
                pop = Popup(title='Error !!',content=Label(text='Invalid Mail'),size_hint=(None, None), size=(200, 200))
                pop.open()
                                
        else:
            print("No Account")
            pop = Popup(title='Error !!',content=Label(text='Enter Mail id and Password'),size_hint=(None, None), size=(200, 200))
            pop.open()
                                
        

class homepage(Screen):

    def fun(self,value):
        con=sql.connect(host="localhost",user="root",password="",database="students")
        cur=con.cursor()
        """query="SHOW TABLES"
        cur.execute(query)
        result=cur.fetchall()
        print(type(result))
        print(result)
        for x in result:
            print(x)"""
        cur.execute("""
        SELECT COUNT(*)
        FROM information_schema.tables
        WHERE table_name = '{0}'
        """.format(value.replace('\'', '\'\'')))
        if cur.fetchone()[0] == 1:
            #dbcur.close()
            print(True)
            wb=Workbook()
            query="SELECT * From (%s);"%value
            cur.execute(query)
            result=cur.fetchall()
            ws=wb.create_sheet(0)
            ws.title="Students"
            ws.append(cur.column_names)
            for row in result:
                ws.append(row)
                print(row)
            wb.save(value+".xlsx")
            print("Success")
            pop = Popup(title='Success !!',content=Label(text='Exported Successfully'),size_hint=(None, None), size=(200, 200))
            pop.open()
            con.commit()
            con.close()
        else:
            print("No table exist")
            pop = Popup(title='Err-404 !!',content=Label(text='Table Not Found'),size_hint=(None, None), size=(200, 200))
            pop.open()
        
        """mainbtn=Button(text="Select class",
                       size_hint=(0.5,0.1),
                       pos_hint={'center_x':0.75,'center_y':0.75})
        dropdown=DropDown()
        for i in range(5):
            btn=Button(text='value %d'%i,size_hint_y=None,height=40)
            btn.bind(on_release=lambda btn:dropdown.select(btn.text))
            dropdown.add_widget(btn)
        mainbtn.bind(on_release=dropdown.open)
        dropdown.bind(on_select= lambda instance,x : setattr(mainbtn,'text',x))"""
class WindowManager(ScreenManager):
    pass

class signupWindow(Screen):
    firstname = ObjectProperty(None)
    lname = ObjectProperty(None)
    email = ObjectProperty(None)
    phno = ObjectProperty(None)
    password = ObjectProperty(None)
    current_password = ObjectProperty(None)
    address = ObjectProperty(None)
    dob = ObjectProperty(None)
    gen=""


    def db(self):
        fn=self.firstname.text
        ln=self.lastname.text
        email=self.mail.text
        phno=self.phone_no.text
        password=self.pswd.text
        address=self.addr.text
        dob=self.d_o_b.text
        gender=self.gen
        con=sql.connect(host="localhost",user="root",password="",database="kivy")
        cur=con.cursor()
        query="INSERT INTO wise(FirstName,LastName,Email,PhoneNumber,Password,Gender,DateOfBirth,Address) VALUES(%s,%s,%s,%s,%s,%s,%s,%s);"
        val=(fn,ln,email,phno,password,gender,dob,address)
        cur.execute(query,val)
        #cur.execute("INSERT INTO wts(FirstName) VALUES (%s)"%(fn,))
        con.commit()
        con.close()



    
    def checkbox_click(self, instance, value,gender):
        self.gen=gender
    def val(self):
        print(self.firstname.text)
        print(self.lastname.text)
        print(self.mail.text)
        print(self.phone_no.text)
        print(self.pswd.text)
        print(self.c_pswd.text)
        print(self.addr.text)
        print(self.d_o_b.text)
        print(self.gen)
        SpecialSym =['$', '@', '#', '%']
        regex = '^[A-Za-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'
        if self.firstname.text!="" and self.lastname.text!="" and self.mail.text!="" and self.phone_no.text!="" and self.pswd.text!="" and self.c_pswd.text!="" and self.c_pswd.text!="" and self.addr.text!="" and self.d_o_b.text!="" and self.gen!="" :
            if self.pswd.text==self.c_pswd.text:
                if len(self.phone_no.text)==10:
                    if len(self.pswd.text)>=8:
                        if any(char.isdigit() for char in self.pswd.text):
                            if any(char.isupper() for char in self.pswd.text):
                                if any(char.islower() for char in self.pswd.text):
                                    if any(char in SpecialSym for char in self.pswd.text):
                                        if re.match("^[A-Za-z]+$",self.firstname.text):
                                            if re.match("^[A-Za-z]+$",self.lastname.text):
                                                if re.search(regex,self.mail.text):
                                                    self.db()
                                                    print("Success")
                                                    pop = Popup(title='Success !!',content=Label(text='Account Created'),size_hint=(None, None), size=(200, 200))
                                                    pop.open()

                                                else:
                                                    pop = Popup(title='Error !!',content=Label(text='Invalid Mail'),size_hint=(None, None), size=(200, 200))
                                                    pop.open()
                                                    print("Invalid Mail")
                                            else:
                                                pop = Popup(title='Error !!',content=Label(text='Invalid Last Name\nPlease Enter Valid Name'),size_hint=(None, None), size=(200, 200))
                                                pop.open()
                                                print("Invalid lastname")
                                        else:
                                            pop = Popup(title='Error !!',content=Label(text='Invalid First Name\nPlease Enter Valid Name'),size_hint=(None, None), size=(200, 200))
                                            pop.open()
                                            print("Invalid firstname")
                                    else:
                                        pop = Popup(title='Error !!',content=Label(text='   Password\nshould have at least\none of the symbols $@#'),size_hint=(None, None), size=(200, 200))
                                        pop.open()
                                        print('Password should have at least one of the symbols $@#')
                                else :
                                    pop = Popup(title='Error !!',content=Label(text='   Password\nshould have at least\none lowercase letter'),size_hint=(None, None), size=(200, 200))
                                    pop.open()
                                    print('Password should have at least one lowercase letter')
                            else:
                                pop = Popup(title='Error !!',content=Label(text='   Password\nshould have at least\none Uppercase letter'),size_hint=(None, None), size=(200, 200))
                                pop.open()
                                print('Password should have at least one uppercase letter')
                        else:
                            pop = Popup(title='Error !!',content=Label(text='   Password\nshould have atleast\none numeral'),size_hint=(None, None), size=(200, 200))
                            pop.open()
                            print('Password should have at least one numeral')
                    else:
                        pop = Popup(title='Error !!',content=Label(text='   Password\nlength must be atleast 8'),size_hint=(None, None), size=(200, 200))
                        pop.open()
                        print('length should be at least 8')
                else:
                    pop = Popup(title='Error !!',content=Label(text='Invalid Phone Number'),size_hint=(None, None), size=(200, 200))
                    pop.open()
                    print('Invalid Phone Number')
            else:
                pop = Popup(title='Error !!',content=Label(text="Password and Current Password\n Doesn't Match"),size_hint=(None, None), size=(200, 200))
                pop.open()
                print("Password and Current Password\n Doesn't Match")
        else:
            pop = Popup(title='Error !!',content=Label(text="Please Enter All Required Fields"),size_hint=(None, None), size=(300, 300))
            pop.open()
            print("Please Enter All required Fields")
            
                                            
kv = Builder.load_file('Test.kv') 
sm = WindowManager()

# adding screens 
sm.add_widget(loginWindow(name='login')) 
sm.add_widget(signupWindow(name='signup')) 
sm.add_widget(homepage(name='mainpage'))

class TestApp(App):
    def build(self):
        return sm

if __name__=='__main__':
    TestApp().run()
