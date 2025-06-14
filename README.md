# pybatis

A simple SQL templating library using Jinja2, inspired by MyBatis.

## Installation

```bash
pip install .
```

## Example

```python
import pybatis

sql = pybatis.render_sql("SELECT * FROM users WHERE id={{ user_id }}", {"user_id": 42})
print(sql)  # Outputs: SELECT * FROM users WHERE id=42
```
