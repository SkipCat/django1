# django1

## Requirements

```
pip install django
pip install markdown2
pip install wikipedia
```

Then, edit the line 398 in file wikipedia/wikipedia.py file to avoid a warning:
```
lis = BeautifulSoup(html, 'html.parser').find_all('li')
```

## Launching

Run `python manage.py runserver PORT`

Then open `localhost:PORT` in your browser or simply click on the link provided by Django.

## Available apps

- Elementary Cellular Automata
- Paste as Markdown
- Hashid
- Admin zone

## Admin zone

To log in as a superadmin, use below informations:
- username: `superadmin`
- password: `adminroot`