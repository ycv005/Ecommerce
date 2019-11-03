# Ecommerce_WebApp
Command to start the Virtual env-</br></br>
For Linux Environment & [Git Bash on Window](https://git-scm.com/download/win)</br>
 `. vcommerce/Scripts/activate` (my virtual env name- vcommerce)</br>
For Windows-</br>
`vcommerce\Scripts\activate`
</br>
For Mac-</br>
`. vcommerce/bin/activate` or `vcommerce myvenv/bin/activate`
</br></br>
To Run Python Server- `python manage.py runserver`</br></br>
To Run the Python Interactive interpreter (shell)- `python manage.py shell`</br></br>
Any changes to db/models, run following code</br>
```
python manage.py makemigrations
python manage.py migrate
```
</br></br>
To Know the work flow and progress, follow the branch in series
1. [Master](https://github.com/ycv005/Ecommerce)- In Starting implement basic model.
2. [Search_bar](https://github.com/ycv005/Ecommerce/tree/search_bar)- Implement Search_bar, include tags to the product.
3. [Cart](https://github.com/ycv005/Ecommerce/tree/cart)- Implementing Cart feature for authenticated as well unauthenticated people. (Still working)