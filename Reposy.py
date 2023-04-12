
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from ttkbootstrap.tooltip import ToolTip
import os
import subprocess

class Controller: 
    def __init__(self, model, view):
        self.model = model
        self.view = view
        self.gitinitFlag = os.path.exists(self.model.directory+ "\\.git")
        self.defaultName = os.path.basename(self.model.directory)
        

    def gitinit(self):
        os.chdir(self.model.directory)

        self.initCommands = [
            'echo "# {name}" >> README.md'.format(name = self.view.name.get()),
            'echo "{name}" >> .gitignore'.format(name = __file__),
            'git init',
            'git add README.md',
            'git commit -m "first commit"',
            'git branch -M main',
            'git remote add origin https://github.com/reizarb/{name}.git'.format(name = self.view.name.get()),
            'git push -u origin main',
        ]
        for command in self.initCommands:
            subprocess.Popen(command, shell=True, stdout=subprocess.PIPE).stdout.read()
        self.view.gitinitDisable()
    
    def add(self):
        subprocess.Popen("git add *", shell=True, stdout=subprocess.PIPE).stdout.read()

    def commit(self):
        subprocess.Popen('git commit -m ' + '"' + self.view.CommitMessageEntry.get() +'"', shell=True, stdout=subprocess.PIPE).stdout.read()

    def push(self):
        subprocess.Popen("git push origin main", shell=True, stdout=subprocess.PIPE).stdout.read()


class Model:
    def __init__(self, directory):
        self.directory = directory


class View:
    def __init__(self):
        pass

    def gitinitDisable(self):
        self.gitinitButton.configure(state="disabled")
        ToolTip(self.gitinitButton, text="Git Repository already initiated here", bootstyle=(INFO, INVERSE))
    
    def setup(self, controller):
        self.controller = controller
        
        #Create Root window
        self.root = ttk.Window(themename="litera")
        self.root.title("GIT'N Click")
        self.root.geometry("250x300")

        #add set name

        self.nameLabel = ttk.Label(self.root, text = "Set Project Name", bootstyle=(PRIMARY))
        self.nameLabel.pack(fill = X) 
        self.name = ttk.StringVar(value= self.controller.defaultName)
        self.nameEntry = ttk.Entry(self.root, bootstyle = (PRIMARY), textvariable=self.name)
        self.nameEntry.pack(fill = X)
        ToolTip(self.nameEntry, text="This must match what you created in GIT HUB", bootstyle=(INFO, INVERSE))
        
        #add Git Init button 
        self.gitinitButton = ttk.Button(self.root, text="git init", bootstyle=(PRIMARY, OUTLINE), command=self.controller.gitinit)
        self.gitinitButton.pack(fill=X) 
        ToolTip(self.gitinitButton, text="Initiate a Git Repository here", bootstyle=(INFO, INVERSE))
        if self.controller.gitinitFlag:
            self.gitinitButton.configure(state="disabled")
            ToolTip(self.gitinitButton, text="Git Repository already initiated here", bootstyle=(INFO, INVERSE))

        #add add files
        self.addButton = ttk.Button(self.root, text = "git add *", bootstyle=(PRIMARY, OUTLINE), command=self.controller.add)
        self.addButton.pack(fill = X)

        #commit message and button 
        self.CommitLabel = ttk.Label(self.root, text = "Commit Message:", bootstyle=(INFO, INVERSE))
        self.CommitLabel.pack(fill = X)
        self.CommitMessage = ttk.StringVar(value = "First Commit" )
        self.CommitMessageEntry = ttk.Entry(self.root, bootstyle = (SECONDARY), textvariable=self.CommitMessage)
        self.CommitMessageEntry.pack(fill = X)
        ToolTip(self.CommitMessageEntry, text="Add Short Commit Message for refference", bootstyle=(SECONDARY, INVERSE))
        self.CommitButton =ttk.Button(self.root, text = "Create Staged Commit", bootstyle =(INFO), command = self.controller.commit)
        self.CommitButton.pack(fill = X)

        #push 
        self.PushButton =ttk.Button(self.root, text = "Push staged Commit", bootstyle =(DANGER), command = self.controller.push)
        self.PushButton.pack(fill = X)
        ToolTip(self.PushButton, text="UPLOAD staged Commit to Origin Main", bootstyle=(DANGER, INVERSE))



    def start(self):
        self.root.mainloop()   
       
   
        

    





## Main loop

dir = os.path.dirname(os.path.abspath(__file__))
app = Controller(Model(dir), View())
app.view.setup(app)
app.view.start()




