import math

from kivy.core.window import Window
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label

class Program(App):
    screen_width = 200
    screen_height = 500
    Window.size = (screen_width, screen_height)

    def build(self):
            self.govde = BoxLayout(orientation = "vertical", padding=30, spacing=5)
            
            self.reynolds = Label(text = "Re")
            self.friction = Label(text = "friction")
            self.deltaP = Label(text = "deltaP")
            
            self.text_input_density = TextInput(hint_text='Enter density (kg/m³)', multiline=True, input_type='number')
            self.text_input_velocity = TextInput(hint_text='Enter velocity (m/s)', multiline=True, input_type='number')
            self.text_input_diameter = TextInput(hint_text='Enter diameter (m)', multiline=True, input_type='number')
            self.text_input_viscosity = TextInput(hint_text='Enter viscosity (Pa·s)', multiline=True, input_type='number')
            self.text_input_roughness = TextInput(hint_text='Enter roughness', multiline=True, input_type='number')
            self.text_input_length = TextInput(hint_text='Enter length (m)', multiline=True, input_type='number')
            
            self.button_Re = Button(text = "Re",size_hint_y = .5)
            self.button_f = Button(text = "f",size_hint_y = .5)
            self.button_deltaP = Button(text = "deltaP",size_hint_y = .5)
            
            self.button_Re.bind(on_press=lambda instance: self.Reynolds(self.text_input_density.text , self.text_input_velocity.text , self.text_input_diameter.text , self.text_input_viscosity.text ))
            self.button_f.bind(on_press=lambda instance: self.colebrook_fd(self.rey, self.text_input_roughness.text))     
            self.button_deltaP.bind(on_press=lambda instance: self.delta_P(self.fd, self.text_input_length.text, self.text_input_density.text, self.text_input_diameter.text, self.text_input_velocity.text))
            
            self.govde.add_widget(self.reynolds)
            self.govde.add_widget(self.friction)
            self.govde.add_widget(self.deltaP)
            
            self.govde.add_widget(self.text_input_density)
            self.govde.add_widget(self.text_input_diameter)
            self.govde.add_widget(self.text_input_length)
            self.govde.add_widget(self.text_input_roughness)
            self.govde.add_widget(self.text_input_velocity)
            self.govde.add_widget(self.text_input_viscosity)
            
            self.govde.add_widget(self.button_Re)
            self.govde.add_widget(self.button_f)
            self.govde.add_widget(self.button_deltaP)
            
            return self.govde          
    def Reynolds(self, rho, vel, dia, vis):
            try:
                self.rey = float(rho)*float(vel)*float(dia)/float(vis)
                print(f"reynolds: {self.rey}")
                self.reynolds.text = str(self.rey)
                return(self.rey)
            except AttributeError:
                print("Beklenmeyen hata!")
                self.reynolds.text = "Beklenmeyen hata!"
            except ValueError:
                print("Lütfen sadece sayı girin!")
                self.reynolds.text = "Lütfen sadece sayı girin!"
                self.rey = None
                return(self.rey)
            except ZeroDivisionError:
                print("Bir sayıyı 0'a bölemezsiniz!")
                self.reynolds.text = "0'a bölünme Hatası!"
                self.rey = None
                return(self.rey)
                
    def colebrook_fd(self, rey, epsilon_over_D, initial_guess=0.01, max_iter=100, tol=1e-6):  
            try:
                self.roughness = float(self.text_input_roughness.text)
                self.diameter = float(self.text_input_diameter.text)            
                self.epsilon_over_D = self.roughness / self.diameter
                self.fd = initial_guess
                #Newton-Raphson
                for _ in range(max_iter):                        
                        self.f = 1.0/math.sqrt(self.fd) + 2.0*math.log10(self.epsilon_over_D/3.7 + 2.44/self.rey/math.sqrt(self.fd))
                        self.df = -0.5/self.fd**1.5 - 2.44/(self.rey*(self.fd**1.5)*math.log(10)*(self.epsilon_over_D/3.7 + 2.44/self.rey/math.sqrt(self.fd)))
                        self.fd_new = self.fd - self.f/self.df
  
                        if abs(self.fd_new - self.fd) < tol:
                                break
                        self.fd = self.fd_new
                        
                print(f"friction coeff: {self.fd}")
                self.friction.text = str(self.fd)
                
                return(self.fd)
            except AttributeError:
                print("Beklenmeyen hata!")
                self.friction.text = "Beklenmeyen hata!"
            except ValueError:
                print("Lütfen sadece sayı girin!")
                self.friction.text = "Lütfen sadece sayı girin!"
                self.fd = None
                return(self.fd)
            except ZeroDivisionError:
                print("Bir sayıyı 0'a bölemezsiniz!")
                self.friction.text = "0'a bölünme Hatası!"
                self.fd = None
                return(self.fd)
            except TypeError:
                print("Lütfen doğru giriş yapın!")
                self.friction.text = "Lütfen doğru giriş yapın!"
                self.fd = None
                return(self.fd)
                
    def delta_P(self, fd, L, rho, D, vel):
            #Darcy-Weisbach 
            try:
                self.delta_p = float(self.fd) * float(L) /float(D) * 0.5 * float(rho) * float(vel)**2     
                print(f"delta P: {self.delta_p}")
                self.deltaP.text = str(self.delta_p)+ " " + "Pa"
 
                return self.delta_p
            except AttributeError:
                print("Beklenmeyen hata!")
                self.deltaP.text = "Beklenmeyen hata!"          
            except ValueError:
                print("Lütfen sadece sayı girin!")
                self.deltaP.text = "Lütfen sadece sayı girin!"            
            except ZeroDivisionError:
                print("Bir sayıyı 0'a bölemezsiniz!")
                self.deltaP.text = "0'a bölünme Hatası!"         
            except TypeError:
                print("Lütfen doğru giriş yapın!")
                self.deltaP.text = "Lütfen doğru giriş yapın!"
                
if __name__ == "__main__":   
    Program().run()