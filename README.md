# Ecommerce_App
Command to Activate the Virtual env-</br></br>
For Linux Environment & [Git Bash on Window](https://git-scm.com/download/win)</br>
 `. vcommerce/Scripts/activate` (my virtual env name- vcommerce)</br></br>
For Windows-</br>
`vcommerce\Scripts\activate`
</br></br>
For Mac-</br>
`. vcommerce/bin/activate` or `vcommerce myvenv/bin/activate`
</br></br>
To Run django Server- `python manage.py runserver`</br></br>
To Run the django Interactive interpreter (shell)- `python manage.py shell`</br></br>
Any changes to db/models, run following code</br>
```
python manage.py makemigrations
python manage.py migrate
```
</br></br>
Any changes to static files, we need to collect static files (as result your new files will be added to static_cdn folder)</br>
```
python manage.py collectstatic
```
</br></br>
To Know the work flow and progress, follow the branch in series
1. [Master](https://github.com/ycv005/Ecommerce)- In Starting implement basic model. (All the work will be merged to this branch)
2. [Search_bar](https://github.com/ycv005/Ecommerce/tree/search_bar)- Implemented Search_bar, include tags to the product.
3. [Cart](https://github.com/ycv005/Ecommerce/tree/cart)- Implemented Cart feature for authenticated as well unauthenticated people.
4. [Checkout](https://github.com/ycv005/Ecommerce/tree/checkout)- Implemented Checking out process of each Order per User.
5. [Address](https://github.com/ycv005/Ecommerce/tree/address)- Implementing Address section of the user.
6. [AutoSearch](https://github.com/ycv005/Ecommerce/tree/autosearch)- Implementing Auto Search to the search bar.