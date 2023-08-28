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
            
            self.text_input_density = TextInput(hint_text='Enter density', multiline=True, input_type='number')
            self.text_input_velocity = TextInput(hint_text='Enter velocity', multiline=True, input_type='number')
            self.text_input_diameter = TextInput(hint_text='Enter diameter', multiline=True, input_type='number')
            self.text_input_viscosity = TextInput(hint_text='Enter viscosity', multiline=True, input_type='number')
            self.text_input_rougness = TextInput(hint_text='Enter rougness', multiline=True, input_type='number')
            self.text_input_length = TextInput(hint_text='Enter length', multiline=True, input_type='number')
            
            self.button_Re = Button(text = "Re",size_hint_y = .5)
            self.button_f = Button(text = "f",size_hint_y = .5)
            self.button_deltaP = Button(text = "deltaP",size_hint_y = .5)
            
            self.button_Re.bind(on_press=lambda instance: self.Reynolds(self.text_input_density.text , self.text_input_velocity.text , self.text_input_diameter.text , self.text_input_viscosity.text ))
            self.button_f.bind(on_press=lambda instance: self.colebrook_fd(self.rey, self.text_input_rougness.text))     
            self.button_deltaP.bind(on_press=lambda instance: self.delta_P(self.fd, self.text_input_length.text, self.text_input_density.text, self.text_input_diameter.text, self.text_input_velocity.text))
            
            self.govde.add_widget(self.reynolds)
            self.govde.add_widget(self.friction)
            self.govde.add_widget(self.deltaP)
            
            self.govde.add_widget(self.text_input_density)
            self.govde.add_widget(self.text_input_diameter)
            self.govde.add_widget(self.text_input_length)
            self.govde.add_widget(self.text_input_rougness)
            self.govde.add_widget(self.text_input_velocity)
            self.govde.add_widget(self.text_input_viscosity)
            
            self.govde.add_widget(self.button_Re)
            self.govde.add_widget(self.button_f)
            self.govde.add_widget(self.button_deltaP)
            
            return self.govde
            
    def Reynolds(self, rho, vel, dia, vis):
            self.rey = float(rho)*float(vel)*float(dia)/float(vis)
            print(f"reynolds: {self.rey}")
            self.reynolds.text = str(self.rey)
            
            return(self.rey)
            
    def colebrook_fd(self, rey, epsilon_over_D, initial_guess=0.01, max_iter=100, tol=1e-6):   
            self.epsilon_over_D = float(self.text_input_rougness.text) / float(self.text_input_diameter.text)
            
            self.fd = initial_guess
            for _ in range(max_iter):
                    self.f = 1.0/math.sqrt(self.fd) + 2.0*math.log10(self.epsilon_over_D/3.7 + 2.51/self.rey/math.sqrt(self.fd))
                    self.df = -0.5/self.fd**1.5 - 2.51/(self.rey*(self.fd**1.5)*math.log(10)*(self.epsilon_over_D/3.7 + 2.51/self.rey/math.sqrt(self.fd)))
                    self.fd_new = self.fd - self.f/self.df
                    if abs(self.fd_new - self.fd) < tol:
                        break
                    self.fd = self.fd_new
            print(f"friction coeff: {self.fd}")
            self.friction.text = str(self.fd)
            
            return(self.fd)
            
    def delta_P(self, fd, L, rho, D, vel):
            self.delta_p = float(self.fd) * float(L) /float(D) * 0.5 * float(rho) * float(vel)**2     
            print(f"delta P: {self.delta_p}")
            self.deltaP.text = str(self.delta_p)
            
            return self.delta_p

if __name__ == "__main__":   
    Program().run()