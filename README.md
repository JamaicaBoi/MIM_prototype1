# Medicine Inspection Machine (Software Prototype)
For this project, the objective is to learn about the components of software used to create a software prototype of Medicine Inspection Machine, such as the GUI and Database. Python will be used as the main programming language for developing this basic software. The application will be developed using PyQt5 and the GUI will be designed using Qt Designer. It includes three main pages: LoginPage, Mainwindow Page, and HistoryPage. The Mainwindow Page also has a sub-page called SelectPresciptionWidget. Each page has its own features that help the user to examine the medication and show the examination history.


https://github.com/JamaicaBoi/MIM_prototype1/assets/122667170/912d7823-b259-4818-81cc-a331bd2fb844


## Installation
### Necessary library
The software developed in this project requires the PyQt5, MySQL, and Ultralytics libraries to launch. Use the following command to install these libraries:
```
pip install PyQt5 ultralytics mysql-connector-python
```
### Database construction
his prototype is available only with a local database connection. Therefore, to launch the software, you need to construct a local database in your workspace. You can import the database data and structure to your workspace by following these steps:

1. Download MySQL Workbench 8.0.36 >> https://dev.mysql.com/downloads/workbench/
2. Open MySQL Workbench, create account and set your connection password.
3. Click to the "Local instance MySQL80" in MySQL Connections. then create a new schema in the connected server to create schema.set the name of the schema to "software_onboard"
![image](https://github.com/JamaicaBoi/MIM_prototype1/assets/122667170/3f2d5346-8de2-4c70-a54f-32d36c768919)
4. Import data and database structure using file "Database_onboard" (SQL Text File) from "Database" folder. Then go to "server" on the top menu bar and select "Data Import".
![image](https://github.com/JamaicaBoi/MIM_prototype1/assets/122667170/f41df13e-02ae-4104-acb4-4a67271c497f)
5. The database construction is complete when there are the tables in created schema

### Conection configuration in software file
After constructing the database, there are some code configurations needed to define the connection. The files that need to be configured are **LoginPage.py, Mainwindow.py, HistoryPage.py, and SelectPrescription_Widget.py.** You need to change the password for the database connection in these files.

```python
#Define Database Connection
        self.connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password= << YOUR DATABASE PASSWORD >>,    # <---- Config here
            database="software_onboard"
        )
```

## Launch the prototype
1. Run "App.py" or executed the command in the workspace.
```
cd DIRECTORY\TO\THE\WORK\SPACE\MIM_prototype1
```
```
python App.py
```
2. The software will start at the LoginPage. You can use the following username and password to login.
   - Username: **Peter_10**
   - Password: **123456**
3. You can use images in the 'Dataset' folder to upload to the software and classify medication in the images. The model performance is very poor, but this is not within the current development scope and will be in the area of improvement.
