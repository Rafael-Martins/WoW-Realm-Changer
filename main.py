from tkinter import *
from tkinter import simpledialog, filedialog
import json
import os.path


def writeToWtf(realm, realmPath):
    f = open(realmPath, 'w')
    f.write('set realmlist ' + realm)
    f.close()

class App:

    def __init__(self, master):

        master.minsize(width=300, height=80)

        if os.path.isfile('data.json'):
            with open('data.json') as json_file:
                self.data = json.load(json_file)
        else:
            newData = open("data.json","w+")
            defaultData = {
                "savedRealms": [
                    {
                        "serverName": "Warmane",
                        "realmList": "logon.warmane.com"
                    }
                ]
            }
            self.data = defaultData
            with open('data.json', 'w') as outfile: # Write to data file
                json.dump(self.data, outfile)


        if "realmPath" not in self.data or self.data["realmPath"] == "":
            realmPathChosen = filedialog.askopenfilename(parent=root,
                initialdir=os.getcwd(),
                title="Please select the realmlist.wtf",
                filetypes=[('realmlist files', '.wtf')])
            if realmPathChosen is "":
                root.destroy()
                return
            self.data["realmPath"] = realmPathChosen
            with open('data.json', 'w') as outfile: # Write to data file
                json.dump(self.data, outfile)

        self.savedRealmName = []
        self.savedRealmAddress = []
        self.selectRealmButton = []
        self.removeRealmButton = []

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
            self.savedRealmName.append(Message(self.savedRealmsFrame, text=realm['serverName'], width=250))
            self.savedRealmName[idx].grid(column=0, row=idx + 1)

            self.savedRealmAddress.append(Message(self.savedRealmsFrame, text=realm['realmList'], width=250))
            self.savedRealmAddress[idx].grid(column=1, row=idx + 1)

            self.selectRealmButton.append(Button(self.savedRealmsFrame, text="SET", command=lambda x=realm['realmList']: self.setSavedRealm(x)))
            self.selectRealmButton[idx].grid(row=idx + 1, column=2)

            self.removeRealmButton.append(Button(self.savedRealmsFrame, text="REMOVE", command=lambda y=idx: self.removeSavedRealm(y)))
            self.removeRealmButton[idx].grid(row=idx + 1, column=3)

        self.totalRealmItens = len(self.data['savedRealms'])

    def changeRealm(self):
        writeToWtf(self.realmInput.get(), self.data["realmPath"])
        self.changeCurrentRealmText(self.realmInput.get())

    def readCurrentRealm(self):
        f = open(self.data["realmPath"], 'r')
        fullRealm = f.readline()
        if fullRealm is "":
            return 'Current realm is: null'
        return 'Current realm is: ' + fullRealm.split('set realmlist ')[1];

    def changeCurrentRealmText(self, text):
        self.realmInitText.configure(text = 'Realm changed to: ' + text)

    def setSavedRealm(self, realm):
        writeToWtf(realm, self.data["realmPath"])
        self.changeCurrentRealmText(realm)

    def removeSavedRealm(self, idx):
        self.data['savedRealms'].pop(idx)
        with open('data.json', 'w') as outfile: # Write to data file
            json.dump(self.data, outfile)
        self.savedRealmName[idx].destroy()
        self.savedRealmAddress[idx].destroy()
        self.selectRealmButton[idx].destroy()
        self.removeRealmButton[idx].destroy()

    def saveRealm(self):
        serverName = simpledialog.askstring("Input", "What is the name of the realm?", parent=root) # Throw dialog

        if serverName is None: # Return if click in cancel
            return

        realmList = self.realmInput.get()
        self.data['savedRealms'].append({"realmList": realmList, "serverName": serverName})
        with open('data.json', 'w') as outfile: # Write to data file
            json.dump(self.data, outfile)

        self.savedRealmName.append(Message(self.savedRealmsFrame, text=serverName, width=250))
        self.savedRealmName[self.totalRealmItens].grid(column=0, row=self.totalRealmItens + 1)

        self.savedRealmAddress.append(Message(self.savedRealmsFrame, text=realmList, width=250))
        self.savedRealmAddress[self.totalRealmItens].grid(column=1, row=self.totalRealmItens + 1)

        self.selectRealmButton.append(Button(self.savedRealmsFrame, text="SET", command=lambda x=realmList: self.setSavedRealm(x)))
        self.selectRealmButton[self.totalRealmItens].grid(row=self.totalRealmItens + 1, column=2)

        self.removeRealmButton.append(Button(self.savedRealmsFrame, text="REMOVE", command=lambda y=self.totalRealmItens: self.removeSavedRealm(y)))
        self.removeRealmButton[self.totalRealmItens].grid(row=self.totalRealmItens + 1, column=3)

        self.totalRealmItens = self.totalRealmItens + 1

root = Tk()
root.wm_title("WoW-Realm-Changer")
root.wm_iconbitmap('icon/icon.ico')

app = App(root)

root.mainloop()
