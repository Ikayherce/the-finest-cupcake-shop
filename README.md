

# The Finest Cupcake Shop
![AmIresponsiveCupcakeShop](readme_images/amiresponsivepp5.png)
[Deployed Link](https://the-finest-cupcake-shop-bc4f44f161e9.herokuapp.com/)

# Table of Contents

- [The Finest Cupcake Shop](#the-finest-cupcake-shop)
- [UX](#ux)
    - [Purpose](#purpose)
    - [User Stories](#user-stories)
    - [Wireframes](#wireframes)
- [Home Page](#home-page)
- [Shop App](#shop-app)
- [Cart App](#cart-app)
- [Payment App](#payment-app)
- [Agile Methodology](#agile-methodology)
- [Existing Features](#existing-features)
- [Features Left to Implement](#features-left-to-implement)
- [Web Marketing](#web-marketing)
- [Technologies Used](#technologies-used)

### UX
#### Purpose
The purpose of The Finest Cupcake Shop is to provide a platform for a small cupcake business to reach its audience and sell their products. The shop specializes in offering plant-based and allergy-friendly cupcakes, catering to a wide range of dietary needs and preferences.

### Agile Methodology

I started by planning out my user stories offline on a spreadsheet that is color-coded to group user stories into milestones. I then moved on to the Canban board on github and have been using both methods during the process, starting with the "must have" stories. 

- [Link to my User Stories in spreadsheet format]( https://docs.google.com/spreadsheets/d/1pGTRyGdKJuW5GuSuWoNzlggfeXokuzwzf6P6scxlwEY/edit#gid=0)
- [Link to my Canban board on github](https://github.com/users/Ikayherce/projects/5/views/1)

![UserStoriesSegment1](readme_images/user_stories1.png)
![UserStoriesSegment2](readme_images/user_stories2.png)


### Existing Features
- Navbar and Footer
- Shop
- Cart
- Session 

### Features left to implement
Unfortunately due to time shortage some important features are left to implement or add to this project:
- Stripe payment implementation is not completed
- Robot.txt file is not included
- Subscription e-mail is not added
- Facebook mock-up page is not added

Other non-essential features that I wanted to add and didn't have time to are:
- Front End Admin Dashboard
- Delivery cost in order

### Web Marketing
- Subscription
Left to implement
- Facebook Page
Not added

### Technologies Used
Languages Used: 
- Python
- CSS
- HTML
- Javascript 

Technologies, Frameworks, APIs and Programs Used:
- django
- jquery
- Bootstrap
- AWS for storage
- Stripe 
- Google Fonts

### Tests
#### Code Validation: 
- HTML validation:
Not performed
- CSS validation
Not performed
- JavaScript validation
Not performed
- Python validator
Not performed
- Lighthouse
Not performed
- Manual tests
Not performed

### Project Bugs and Solutions:
#### Creating new branches
For this project I have created branches to test implementing solutions to different issues that have come up. The most relevant example is the change in my Product Model to add multiple categories (initially it was possible to just assign one category to each product). I carried out the changes in a second branch and then merged with main branch. 


### Deployment
#### Deployment to Heroku

#### In your app

1. Add the list of requirements by writing in the terminal:
    ```sh
    pip3 freeze --local > requirements.txt
    ```

2. Git add and git commit the changes made:
    ```sh
    git add .
    git commit -m "Add requirements.txt"
    ```

#### Log into Heroku

3. Log into Heroku or create a new account and log in.

4. In the top right-hand corner, click "New" and choose "Create new app." If you are a new user, the "Create new app" button will appear in the middle of the screen.

5. Name your app - it must be unique and different from this app.

6. Choose your region.

7. Click "Create App."

#### Configure Your Project

8. The project page will open.

9. Go to the Resources Tab, then Add-ons, search for and add "Heroku Postgres."

10. Choose "Settings" from the menu at the top of the page.

11. In the "Config Vars" section, click "Reveal Config Vars."

12. Add the following variables to the list:
    - `DATABASE_URL` will be added automatically.
    - `SECRET_KEY` - This is the Django secret key and can be generated [here](https://djecrety.ir/).

#### Go back to your code

13. Create a `Procfile` in your app:
    ```sh
    echo "web: gunicorn PROJ_NAME.wsgi" > Procfile
    ```

14. In your settings, add `Heroku` to `ALLOWED_HOSTS`.

15. Add and commit the changes in your code, then push to GitHub:
    ```sh
    git add .
    git commit -m "Configure for Heroku deployment"
    git push
    ```

#### Final step - deployment

16. Next, go to the "Deploy" tab in the menu bar at the top.

17. In the "Deployment method" section, choose "GitHub."

18. A new section will appear, "Connect to GitHub" - Search for your repository to connect to.

19. Type the name of your repository and click "Search."

20. Once Heroku finds your repository, click "Connect."

21. Scroll down to the "Automatic Deploys" section.

22. Click "Enable Automatic Deploys" or choose "Deploy Branch" to deploy manually.

23. Click "Deploy Branch."

24. Once the program runs, you should see the message "The app was successfully deployed."

25. Click the "View" button to see your live app. The live link can be found here.



#### Getting Stripe keys
1. Navigate to the Developers tab. Locate the API keys section in the sidebar menu.
   - Duplicate `STRIPE_PUBLIC_KEY` and `STRIPE_SECRET_KEY`.

2. Proceed to the Webhooks section. Click the "Add Endpoint" button situated in the upper-right corner.
   - Enter your endpoint URL (either local or deployed).
   - Choose "All Events".
   - After clicking "Add Endpoint", you'll be redirected to the webhook's page.
   - Retrieve the webhook signing secret and input it into both your application's settings and Heroku as the `STRIPE_WH_SECRET` environment variable.


#### Setting AWS bucket
1. Visit the Amazon Web Services page and log in or create an account.
2. You should be redirected to the AWS Management Console. If not, click the AWS logo in the top-left corner or select "Services" and choose "Console Home".
3. Below the header, click "All Services" and find "S3" under "Storage".
4. Create a new bucket by clicking the "Create Bucket" button in the top-right corner.
   - Provide a unique name for your bucket (ideally matching your Heroku app name) and select the nearest AWS region.
   - Set "Object Ownership" to "ACLs Enabled" and "Bucket Owner Preferred".
   - Disable "Block Public Access" to allow public access, acknowledging the potential for objects within the bucket to become publicly accessible.
5. After creation, click on the name of your newly created bucket.
6. Navigate to the "Properties" tab and enable "Static Website Hosting" at the bottom.
   - Specify "index.html" as the index document and "error.html" for errors.
7. Configure CORS by pasting the following JSON into the "CORS Configuration" field:
. Within the "Permissions" tab, edit the bucket policy using the AWS Policy Generator.
   - Select "S3 Bucket Policy", generate a policy allowing all actions on the bucket, and adjust the "Resource" key to include "/*" for full access.
9. Adjust the Access Control List (ACL) to grant public read access.
10. In the Identity and Access Management (IAM) section, create a new group and attach a policy granting full access to S3 resources.
11. Create a new user within this group and assign them programmatic access.
12. Download the user's credentials as a `.csv` file.

## Connecting Django to AWS S3

1. Install `boto3` and `django-storages`.
2. Add `storages` to your `INSTALLED_APPS` in `settings.py`.
3. Configure AWS settings in `settings.py`.
4. Set environment variables in Heroku using the values from the downloaded `.csv` file.
5. Create a `custom_storages.py` file in your project root.
6. Update `settings.py` to use the custom storage classes for static and media files.


### Resources, credits and acknowledgements. 
For the code, I followed the following tutorials: 

- Code Institute's Boutique Ado walkthrough tutorial
- https://www.youtube.com/watch?v=_ELCMngbM0E&list=PL-51WBLyFTg0omnamUjL1TCVov7yDTRng
- https://www.youtube.com/watch?v=5n8FKv19os0&list=PL_KegS2ON4s53FNSqgXFdictTzUbGjoO-
- https://www.youtube.com/watch?v=u6R4vBa7ZK4&list=PLCC34OHNcOtpRfBYk-8y0GMO4i1p1zn50
- https://www.youtube.com/watch?v=UqSJCVePEWU&list=PLOLrQ9Pn6caxY4Q1U9RjO1bulQp5NDYS_


For the readme I got inspiration from these projects: 
https://github.com/JoGorska/bonsai-shop
https://github.com/ValeP314/pp5-tangled-treasures-v2

User stories template inspired in https://www.smartsheet.com/user-story-templates

For the images I used www.unsplash.com 

The texts in the website are written by me. 