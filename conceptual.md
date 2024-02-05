### Conceptual Exercise

Answer the following questions below:

- What is PostgreSQL?
Its used to relate databases and manage them. It supports SQL too.
- What is the difference between SQL and PostgreSQL?
SQL is the language and PostgreSQL is a specific management system RDBMS of the SQL language.
- In `psql`, how do you connect to a database?
\c database_name

- What is the difference between `HAVING` and `WHERE`?
where is used to filter rows before they are grouped and having is used with grouped rows. 
- What is the difference between an `INNER` and `OUTER` join?
inner join has rows where there is a match in both tables base on the join condition and outer join returns all rows from one table and matching rows from another.
- What is the difference between a `LEFT OUTER` and `RIGHT OUTER` join?
both are forms of outer joins. in left outer join, all rows from the left table are included with matching rows from the right table. in right outer join all rows from the right table are included with matching fows from the left table. the difference is the side from which they are included.
- What is an ORM? What do they do?
Object relational mapping. it is a programming technique that allows for conversion between different types of data models. it maps objects in code to tables in a database and proves more efficient ways to interact with the database using objects and classes rather than sql queries.
- What are some differences between making HTTP requests using AJAX 
  and from the server side using a library like `requests`?
AJAX does requests from browser to a server and updates the web page without requiring a full page reload. Using requests in python invloves making HTTP requests from the server itself to other external servers or APIs. the difference is the origin of the request. AJAX is from the client side.
- What is CSRF? What is the purpose of the CSRF token?
Cross site request forgery is a security vulnerability where a hacker trickes a user's browser into making uninteded requests on a website where the user is authenticated. The tokens are unique and specific to a user's session and  the server checks the token to make sure the request is legit and originates from the same site. 
- What is the purpose of `form.hidden_tag()`?
it makes an HTML input tag of type hidden that has a CSRF token.