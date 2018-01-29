from tkinter import *
from tkinter import simpledialog
import json


def writeToWtf(realm):
    f = open('realmlist.wtf', 'w')
    f.write('set realmlist ' + realm)
    f.close()

class App:

    def __init__(self, master):

        master.minsize(width=300, height=80)

        with open('data.json') as json_file:
            self.data = json.load(json_file)

        mainFrame = Frame(master, width=300, height=100)
        mainFrame.grid(row=0, column=0, padx=20)

        self.title = Message(mainFrame, text="WoW-Realm-Changer", width=400, font=("Helvetica", 18, "bold"))
        self.title.grid()


        inputFrame = Frame(mainFrame)
        inputFrame.grid(row=1, column=0)

        self.realmInitText = Message(inputFrame, text="set realmlist:", width=100, font=("Helvetica", 11))
        self.realmInitText.grid(row=1, column=1)

        self.realmInput = Entry(inputFrame)
        self.realmInput.grid(row=1, column=2)

        self.changeButton = Button(inputFrame, text="CHANGE", command=self.changeRealm)
        self.changeButton.grid(row=1, column=3)

        self.saveButton = Button(inputFrame, text="SAVE",  command=self.saveRealm)
        self.saveButton.grid(row=1, column=4)


        self.currentRealmFrame = Frame(mainFrame)
        self.currentRealmFrame.grid(row=2, column=0)
        self.realmInitText = Message(self.currentRealmFrame, text=self.readCurrentRealm(), width=300, font=("Helvetica", 11))
        self.realmInitText.grid(row=2, column=0)

        self.savedRealmsFrame = Frame(mainFrame)
        self.savedRealmsFrame.grid(row=3, pady=(20, 10))

        self.savedRealmsMessage = Message(self.savedRealmsFrame, text='Saved Realms', width=300, font=("Helvetica", 15, "bold"))
        self.savedRealmsMessage.grid()

        for idx, realm in enumerate(self.data['savedRealms']):
            savedRealmName = Message(self.savedRealmsFrame, text=realm['serverName'], width=250)
            savedRealmName.grid(column=0, row=idx + 1)

            savedRealmRealm = Message(self.savedRealmsFrame, text=realm['realmList'], width=250)
            savedRealmRealm.grid(column=1, row=idx + 1)

            selectRealmButton = Button(self.savedRealmsFrame, text="SET", command=lambda x=realm: self.setSavedRealm(x))
            selectRealmButton.grid(row=idx + 1, column=2)

        self.totalRealmItens = len(self.data['savedRealms'])

    def changeRealm(self):
        writeToWtf(self.realmInput.get())
        self.changeCurrentRealmText(self.realmInput.get())

    def readCurrentRealm(self):
        f = open('realmlist.wtf', 'r')
        fullRealm = f.readline()
        return 'Current realm is: ' + fullRealm.split('set realmlist ')[1];

    def changeCurrentRealmText(self, text):
     self.realmInitText.configure(text = 'Realm changed to: ' + text)

    def setSavedRealm(self, realm):
        writeToWtf(realm['realmList'])
        self.changeCurrentRealmText(realm['realmList'])

    def saveRealm(self):
        serverName = simpledialog.askstring("Input", "What is the name of the realm?", parent=root)

        if serverName is None:
            return

        realmList = self.realmInput.get()
        self.data['savedRealms'].append({"realmList": realmList, "serverName": serverName})
        with open('data.json', 'w') as outfile:
            json.dump(self.data, outfile)

        savedRealmName = Message(self.savedRealmsFrame, text=serverName, width=250)
        savedRealmName.grid(column=0, row=self.totalRealmItens + 1)

        savedRealmRealm = Message(self.savedRealmsFrame, text=realmList, width=250)
        savedRealmRealm.grid(column=1, row=self.totalRealmItens + 1)

        selectRealmButton = Button(self.savedRealmsFrame, text="SET", command=lambda x=realmList: self.setSavedRealm(x))
        selectRealmButton.grid(row=self.totalRealmItens + 1, column=2)

        self.totalRealmItens = self.totalRealmItens + 1

root = Tk()
root.wm_title("WoW-Realm-Changer")

app = App(root)

root.mainloop()
