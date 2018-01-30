import os
from tkinter import Tk
from tkinter import simpledialog, filedialog, Button, Message, Entry, Frame
from realmManager import RealmManager
from configManager import ConfigManager


def chooseGameFolder():
    chosenRealmPath = filedialog.askopenfilename(
        parent=root,
        initialdir=os.getcwd(),
        title='Please select the realmlist.wtf',
        filetypes=[('realmlist files', '.wtf')]
    )

    if chosenRealmPath is '':
        root.destroy()
        return None

    return chosenRealmPath


class App:
    def __init__(self, master):
        master.minsize(width=300, height=80)

        self.savedRealmName = []
        self.savedRealmAddress = []
        self.selectRealmButton = []
        self.removeRealmButton = []

        self.rlmManager = RealmManager()
        self.cfgManager = ConfigManager()

        if not self.cfgManager.hasGameFolder():
            newGameFolder = chooseGameFolder()

            # Force user to choose a game folder
            while newGameFolder is None:
                isCanceled = simpledialog.askretrycancel(
                    'Question',
                    'You need to select a game folder',
                    parent=root
                )

                if isCanceled:
                    root.destroy()
                    return

                newGameFolder = chooseGameFolder()

            self.cfgManager.updateGameFolder(newGameFolder)

        self.mainFrame = Frame(master, width=300, height=100)
        self.mainFrame.grid(row=0, column=0, padx=20)

        self.title = Message(
            self.mainFrame,
            text='WoW Realm Changer',
            width=400,
            font=('Helvetica', 18, 'bold')
        )
        self.title.grid()

        inputFrame = Frame(self.mainFrame)
        inputFrame.grid(row=1, column=0)

        self.realmInputLabel = Message(
            inputFrame,
            text='set realmlist:',
            width=100,
            font=('Helvetica', 11)
        )
        self.realmInputLabel.grid(row=1, column=1)

        self.realmAddressInput = Entry(inputFrame)
        self.realmAddressInput.grid(row=1, column=2)

        self.saveButton = Button(
            inputFrame,
            text='SAVE',
            command=self.addRealm
        )
        self.saveButton.grid(row=1, column=4)

        self.currentRealmFrame = Frame(self.mainFrame)
        self.currentRealmFrame.grid(row=2, column=0)
        self.realmInitText = Message(
            self.currentRealmFrame,
            text=self.rlmManager.currentRealm(),
            width=300,
            font=('Helvetica', 11)
        )
        self.realmInitText.grid(row=2, column=0)
        self.buildSavedRealmsList()

    def buildSavedRealmsList(self):
        self.savedRealmsFrame = Frame(self.mainFrame)
        self.savedRealmsFrame.grid(row=3, pady=(20, 10))

        self.savedRealmsMessage = Message(
            self.savedRealmsFrame,
            text='Saved Realms',
            width=300,
            font=('Helvetica', 15, 'bold')
        )
        self.savedRealmsMessage.grid()

        for idx, realm in enumerate(self.cfgManager.savedRealms()):
            self.addRealmRow(realm)

    def setActiveRealm(self, realm):
        self.rlmManager.changeActiveRealm(realm)
        self.realmInitText.configure(text='Realm changed to: ' + realm['name'])

    def removeSavedRealm(self, idx):
        self.cfgManager.removeRealm(idx)
        self.removeRealmRow(idx)

    def addRealm(self):
        realmName = simpledialog.askstring(
            'Input',
            'What is the name of the realm?',
            parent=root
        )

        realmAddress = self.realmAddressInput.get()

        realm = {'address': realmAddress, 'name': realmName}

        self.cfgManager.addRealm(realm)
        self.addRealmRow(realm)

    def removeRealmRow(self, index):
        self.savedRealmName[index].destroy()
        self.savedRealmAddress[index].destroy()
        self.selectRealmButton[index].destroy()
        self.removeRealmButton[index].destroy()

    def addRealmRow(self, realm):
        if not realm:
            return

        index = len(self.savedRealmName)
        name = realm['name']
        address = realm['address']

        self.savedRealmName.append(
            Message(self.savedRealmsFrame, text=name, width=250)
        )
        self.savedRealmName[index].grid(column=0, row=index + 1)

        self.savedRealmAddress.append(
            Message(self.savedRealmsFrame, text=address, width=250)
        )
        self.savedRealmAddress[index].grid(column=1, row=index + 1)

        self.selectRealmButton.append(Button(
            self.savedRealmsFrame,
            text='SET',
            command=lambda rlm=realm: self.setActiveRealm(rlm)
        ))
        self.selectRealmButton[index].grid(column=2, row=index + 1)

        self.removeRealmButton.append(Button(
            self.savedRealmsFrame,
            text='REMOVE',
            command=lambda idx=index: self.removeSavedRealm(idx)
        ))

        self.removeRealmButton[index].grid(column=3, row=index + 1)
        self.totalRealmItems = index + 1


root = Tk()
root.wm_title('WoW Realm Changer')
root.wm_iconbitmap('icon/icon.ico')

app = App(root)

root.mainloop()
