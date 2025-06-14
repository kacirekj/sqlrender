# The Sqlrender

A simple SQL templating library using Bottle templating engine. Inspired by MyBatis.

## About

Sqlrender uses standard Python Bottle templating engine
to convert template into the parametrized Sql template, which can be then used in any database.

## Installation

```bash
pip3 install sqlrender
```

## Simple example

First, define the Sql query as a Bottle template. As you can see, we are using standard Bottle syntax:
```python
import sqlrender

# Define sql query as Bottle template

template = """
    SELECT 
        name, age, role, gender 
    FROM 
        users
    WHERE 1 = 1
        % if ageMin:
        AND age >= {{ageMin}}
        % end
        AND role IN {{Util.join(roles)}}
    ORDER BY
        {{!orderBy}}
    LIMIT
        {{!limit}}
    """
```
Next, we specify the input parameters for the Bottle template:

```python
# Define input template parameters

parameters = {
    'roles': ['Student', 'Graduate'],
    'ageMin': 18,
    'orderBy': 'name ASC',
    'limit': 100,
}
```
Call the render method to obtain the output sql template and the output sql parameters:
```python
# Call render method

sql_template, sql_params = sqlrender.render(template, parameters)

print(sql_template)
print(sql_params)
```
It will print the bellow sql query. As you can see, the query parameters are present as "?" symbols whereas the ORDER BY and LIMIT has value directly present (thanks to "!" symbol): 
```sql
SELECT 
    name, age, role, gender 
FROM 
    users
WHERE 1 = 1
    AND age >= ?
    AND role IN (?, ?)
ORDER BY
    name ASC
LIMIT
    100
```
Also, we can see that in the sql parameters tuple there are present values with corresponding "?" in the query: 
```sql
(18, 'Student', 'Graduate')
```
### Example Breakdown
Few points:
1. As has been said, the standard Bottle template is used, so read the Bottle docs to see how to use other features
2. As you can see, the LIMIT and ORDER BY has value directly rendered - this is achieved by symbol "!" used in template.
3. There is used custom util function "Util.join()" which is part of the library. You can create your own functions and call them in the template. However, see my function first and do it accordingly.
4. That's all

## Notes

- The Python Bottle template has been used because it is very simple and allows customizations which was not possible with Jinja2.
- Please give me a note about bugs
- The MyBatis is powerful and classical Java library which, unfortunately, is not known by many. That's sad because it can be way better than ORM. 