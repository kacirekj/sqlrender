"""
pybatis: Simple SQL + Jinja templating library
Author: Jiri Kacirek
"""

import boto3
import jinja2

def render_sql(template_str, context):
    template = jinja2.Template(template_str)
    return template.render(**context)

# Add your core logic here
