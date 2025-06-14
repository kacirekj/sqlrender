# sqlrender

A simple SQL templating library using Bottle Simple Template. Inspired by MyBatis.

## Installation

```bash
pip3 install sqlrender
```

## Example

```python
from sqlrender

sql = pybatis.render_sql("SELECT * FROM users WHERE id={{ user_id }}", {"user_id": 42})
print(sql)  # Outputs: SELECT * FROM users WHERE id=42
```
