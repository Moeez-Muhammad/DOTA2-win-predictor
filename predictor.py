import opendota
import json
from joblib import load
import sys
from tkinter import Tk, Label, Button, Entry, StringVar

class Predictor:
	def __init__(self, master):
		self.random_forest = load('rf.joblib')
		self.api = opendota.API()
		with open('heroes.json', 'r') as infile:
			self.api.heroes = json.load(infile)
			self.api.generate_hero_ids_dict()
			self.api.generate_hero_dict()
		self.data = [[0]*(len(self.api.heroes)*2)]
		self.status_text = StringVar()

		self.master = master
		master.title("DOTA 2 Predictor")
		
		self.radiant = Label(master, text="Radiant Team:")
		self.radiant1 = Entry(master)
		self.radiant2 = Entry(master)
		self.radiant3 = Entry(master)
		self.radiant4 = Entry(master)
		self.radiant5 = Entry(master)
		self.radiant.pack()
		self.radiant1.pack()
		self.radiant2.pack()
		self.radiant3.pack()
		self.radiant4.pack()
		self.radiant5.pack()

		self.dire = Label(master, text="Dire Team:")
		self.dire1 = Entry(master)
		self.dire2 = Entry(master)
		self.dire3 = Entry(master)
		self.dire4 = Entry(master)
		self.dire5 = Entry(master)
		self.dire.pack()
		self.dire1.pack()
		self.dire2.pack()
		self.dire3.pack()
		self.dire4.pack()
		self.dire5.pack()



		self.button = Button(master, text="Predict", command=self.predict)
		self.button.pack()

		self.status = Label(master, textvariable=self.status_text)
		self.status.pack()


	def predict(self):
		print("predicting bois")
		self.data = [[0]*(len(self.api.heroes)*2)]

		radiant = [
			self.radiant1.get(),
			self.radiant2.get(),
			self.radiant3.get(),
			self.radiant4.get(),
			self.radiant5.get()
		]
		dire = [
			self.dire1.get(),
			self.dire2.get(),
			self.dire3.get(),
			self.dire4.get(),
			self.dire5.get()
		]
		heroes = dire + radiant
		for hero in radiant:
			if hero not in self.api.heroes_dict:
				self.status_text.set(hero+" is not a valid hero!")
				return 1
			if len(heroes) != len(set(heroes)):
				self.status_text.set("NO duplicate heroes")
				return 1 
			zero = self.get_hero_zero_index(hero)
			print(zero)
			self.data[0][zero] = 1

		for hero in dire:
			if hero not in self.api.heroes_dict:
				self.status_text.set(hero+" is not a valid hero!")
				return 1
			if len(heroes) != len(set(heroes)):
				self.status_text.set("NO duplicate heroes")
				return 1 
			zero = self.get_hero_zero_index(hero)
			print(zero)
			self.data[0][zero + len(self.api.heroes)] = 1

		prediction = self.random_forest.predict(self.data)
		if int(prediction[0]) == 0:
			winner = "Radiant"
		else:
			winner = "Dire"
		self.status_text.set(winner+" wins!")

	def get_hero_zero_index(self, hero):
		hero_id = self.api.heroes_dict[hero]
		hero_zero_id = self.api.hero_ids_dict[hero_id]
		return hero_zero_id

root = Tk()
my_gui = Predictor(root)
root.mainloop()


# api = opendota.API()
# with open('heroes.json', 'r') as infile:
#     api.heroes = json.load(infile)
# api.generate_hero_ids_dict()
# api.generate_hero_dict()

# random_forest = load('rf.joblib')
# dire = []
# radiant = []

# print("Welcome to DOTA 2 predictor!")
# print("Type EXIT at any time to exit")
# print("Press ENTER to begin", end='')
# input()

# def get_hero_zero_index(hero):
# 	hero_id = api.heroes_dict[hero]
# 	hero_zero_id = api.hero_ids_dict[hero_id]
# 	return hero_zero_id

# while True:
# 	radiant = []
# 	dire = []
# 	data = []
# 	print("Enter Radiant Team: ")
# 	while len(radiant) != 5:
# 		hero = input(str(len(radiant) + 1) + ": ")
# 		if hero.upper() == "EXIT":
# 			sys.exit()
# 		if hero not in api.heroes_dict:
# 			print("Invalid hero")
# 			continue
# 		if hero not in radiant and hero not in dire:
# 			radiant.append(hero)
# 		else:
# 			print("NO duplicate heroes")
# 			continue
# 		zero = get_hero_zero_index(hero)
# 		print(zero)
# 		data.append(zero)
# 	print(radiant)

# 	print("Enter Dire team: ")
# 	while len(dire) != 5:
# 		hero = input(str(len(dire) + 1) + ": ")
# 		if hero.upper() == "EXIT":
# 			sys.exit()
# 		if hero not in api.heroes_dict:
# 			print("Invalid hero!")
# 			continue
# 		if hero not in dire and hero not in radiant:
# 			dire.append(hero)
# 		else:
# 			print("No duplicate heroes")
# 			continue
# 		zero = get_hero_zero_index(hero)
# 		print(zero)
# 		data.append(zero)
# 	print(dire)
# 	prediction = random_forest.predict(data)
# 	print(prediction)
