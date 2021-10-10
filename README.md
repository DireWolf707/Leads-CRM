# **Leads-CRM**
Leads CRM is an easy to use and efficient web app to create and manage your agents and leads as an agent manager and your assigned leads as an agent.
Code is well documented and commented.

## **CI/CD Pipeline**
This web app is connected to **CI/CD** pipline for automatic linting, testing with provision of postgresql, creating test coverage reports and deployment on heroku using **github actions**.

### **Deployed App** : [dw-crm](https://dw-crm.herokuapp.com/)
*(May take some time on first request as it can be in sleeping state)*

- - - -
## **Project Structure**
- **.github**: Contains Github Actions Yaml File.
- **accounts app**: Contains Custom User Model *(which can be further extended if needed)* And Authentication Logic and Urls.
- **agents app**: Contains Logic And Urls For Managing Agent By Agent Manager.
- **backend**: Contains Project Level Settings, Urls And Deployment Configurations.
- **Leads**: 
  - Contains Logic And Urls For Managing Leads by Agent And Agent Manager Respectively.
  - Contains Models *(Agent, Agent Manager and Lead)* And Signals *(including images cleanup code)*.
- **Staic**: Contains Images/Css/Js Used In The Project.
- **templates**: Contains Templates *(and reusable html fragments)* For All The Apps Used In The Project.
- **Other Files**:
  - .gitignore: Contains File Names To Ignore By Git.
  - manage.py: Python Code To Manage Django Project.
  - Procfile: Contains Config For Heroku Deployment.
  - requirements.txt: Contains All Dependencies For The Project.
  - runtime.txt: Contains Python Version For Heroku Deployment.
- - - -
## **Local Deployment**
1. Make a virtual environment using you prefered tool and activate it.
2. $ pip install -r requirements.txt
3. $ python `manage.py` migrate
4. $ python `manage.py` runserver
   
**Note** :
- Always use different **SECRET KEY** in production.
- **DEBUG** is True by default, make sure to make it False in production for enabling security features provided in `settings.py`.
- **SQL lite** database is used by default but postgresql configs are provided in `setting.py`.
- For **Mail** service console is used as backend but smtp configs are provided for production in `setting.py`.